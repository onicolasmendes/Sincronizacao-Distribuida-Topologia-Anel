import socket
import threading
import time
import pickle

#requests = False
#Dados do proximo nó



# Simula o acesso ao recurso compartilhado (seção crítica)
def access_resource(element_id):
    print(f"Elemento {element_id} do Cluster Sync: Acessando o recurso R...")
    time.sleep(0.5)
    print(f"Elemento {element_id} do Cluster Sync: Saindo da seção crítica.")

# Função para processar o token e verificar se o elemento pode entrar na seção crítica
def process_token(token, element_id):
    if token.get(element_id) is None:
        return False
            
    else:
        # Verificar se sou o menor timestamp, ignorando valores None
        smallest_key = min(
            (key for key in token if token[key] is not None), 
            key=token.get
        )
        
        if smallest_key == element_id:
            return True
        else:
            return False
        
def write_token(token,timestamp,element_id):
    if element_id in token:
        token[element_id] = timestamp
        return True
    
    else:
        print(f'a Chave não foi encontrada')
        return False
    

def conectar_prox_no(host, porta, store):
    # Cria um socket TCP/IP
    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    while True:
        try:
            # Tenta se conectar ao endereço fornecido
            cliente_socket.connect((host, porta))
            print(f"Conectado com sucesso a {host}:{porta}")
            
            # Armazena o socket na lista store
            store.append(cliente_socket)
            break  # Sai do loop após armazenar a conexão com sucesso
            
        except Exception as e:
            print(f"Falha ao conectar a {host}:{porta}: {e}")
            print("Tentando novamente em 1 segundo...")
            time.sleep(1)
            continue

# Função que simula um elemento do Cluster Sync recebendo solicitações de clientes
def iniciar_servidor(endereco,store):
    # Cria um socket TCP/IP
    servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Liga o socket ao endereço e porta especificados
        servidor_socket.bind((endereco[0], endereco[1]))
        
        # Coloca o socket no modo de escuta
        servidor_socket.listen(5)
        print(f"Servidor iniciado em {endereco[0]}:{endereco[1]}. Esperando por conexões...")
        
        i = 0
        while i < 2:
            # Aceita uma conexão quando um cliente tenta se conectar
            conexao, endereco_cliente = servidor_socket.accept()
            i = i + 1
            print(f"Conexão aceita de {endereco_cliente}")
            store.append(conexao)
            
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
    
    finally:
        print("Todas conexoes feitas.")
        return
        

def set_requests_true(requests):
    requests = True

def set_requests_false(requests):

    requests = False


def faz_tudo(conexao, element_id,requests):
    try:

        while True:
            # Recebe dados do cliente ou do cluster
            dados = conexao.recv(1024).decode('utf-8')
            if not dados:
                print(f"Conexão encerrada por {element_id}")
                break
            elif dados.startswith("REQUEST"):
                #relacionado ao cliente
                set_requests_true()
                while True:
                    if requests == False:
                        #enviando mensagem de commit para o cliente
                        conexao.sendall("COMMITTED".encode('utf-8'))
                        break



            if dados.startswith("TOKEN"):
                #relacionado ao cluster
                dadosdict = conexao.recv(1024)
                #extrai token da mensagem
                token = pickle.loads(dadosdict)
                
                process = process_token(token,element_id)
                if process == True:
                    access_resource()
                    set_requests_false()
                    write_token(token,None,element_id)
                    # passar token para o proximo
                    send_token_to_next_element(token,next_socket)

                elif process == False and requests == True:
                    write_token(token,time.time(),element_id)
                    # passar token para o proximo
                    send_token_to_next_element(token,next_socket)
                    
                elif process == False and requests == False:                    
                    # passar token para o proximo
                    send_token_to_next_element(token,next_socket)

    except Exception as e:
        print(f"Erro na comunicação com {element_id}: {e}")
    
    finally:
        conexao.close()


# Função que envia o token para o próximo elemento no anel
def send_token_to_next_element(token, next_node_con):
    next_node_con.sendall("TOKEN".encode('utf-8'))
    token = pickle.dumps(token)
    next_node_con.sendall(token)

def cluster_node(endereco, host, porta):
    conexoes_server = []
    conexao_cliente = []
    
    # Criar e iniciar a thread para o servidor
    server_thread = threading.Thread(target=iniciar_servidor, args=(endereco,))
    server_thread.start()

    # Criar e iniciar a thread para conectar ao próximo nó
    client_thread = threading.Thread(target=conectar_prox_no, args=(host, porta, conexao_cliente))
    client_thread.start()

    # Opcionalmente, você pode aguardar que as threads terminem
    client_thread.join()

    request = False
    #para cada conexao de server, iniciar uma thread da funcao:
    threads = []

    for conexao_server in conexoes_server:
        t = threading.Thread(target=faz_tudo, args=(conexao_server, conexao_cliente, request))
        t.start()
        threads.append(t)
