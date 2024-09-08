import socket
import threading
import time

# Simula o acesso ao recurso compartilhado (seção crítica)
def access_resource(element_id):
    print(f"Elemento {element_id} do Cluster Sync: Acessando o recurso R...")
    time.sleep(0.5)
    print(f"Elemento {element_id} do Cluster Sync: Saindo da seção crítica.")

# Função para processar o token e verificar se o elemento pode entrar na seção crítica
def process_token(token, element_id):
    if token.get(element_id) == None:
        return False
            
    else:
        #verificar se sou o menor timestamp
        smallest_key = min(token, key=token.get)
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

# Função que simula um elemento do Cluster Sync recebendo solicitações de clientes
def iniciar_servidor(host, porta):
    # Cria um socket TCP/IP
    servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Liga o socket ao endereço e porta especificados
        servidor_socket.bind((host, porta))
        
        # Coloca o socket no modo de escuta
        servidor_socket.listen(5)
        print(f"Servidor iniciado em {host}:{porta}. Esperando por conexões...")
        
        while True:
            # Aceita uma conexão quando um cliente tenta se conectar
            conexao, endereco_cliente = servidor_socket.accept()
            print(f"Conexão aceita de {endereco_cliente}")
            
            # Cria uma nova thread para tratar a conexão
            thread = threading.Thread(target=tratar_conexao, args=(conexao, endereco_cliente))
            thread.start()
    
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
    
    finally:
        servidor_socket.close()
        print("Servidor encerrado.")

def tratar_conexao(conexao, endereco_cliente):
    try:
        while True:
            # Recebe dados do cliente
            dados = conexao.recv(1024)
            if not dados:
                print(f"Conexão encerrada por {endereco_cliente}")
                break
            elif dados.startswith("REQUEST"):
                #relacionado ao cliente
                continue
            elif dados.startswith("TOKEN"):
                #relacionado ao no anterior
                continue
            
            print(f"Recebido de {endereco_cliente}: {dados.decode('utf-8')}")
            # Responde ao cliente
            conexao.sendall(b"Mensagem recebida")
    
    except Exception as e:
        print(f"Erro na comunicação com {endereco_cliente}: {e}")
    
    finally:
        conexao.close()

# Função principal de um elemento do Cluster Sync
def cluster_sync_element(element_id, port, next_element_port):
    print(f"Elemento do Cluster Sync {element_id}: Esperando solicitações...")

    # Configura o socket para receber clientes
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(("localhost", port))
        server_socket.listen()

        while True:
            connection, address = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(connection, address, token, element_id))
            client_thread.start()

            # Simula o envio do token para o próximo elemento do Cluster
            time.sleep(1)  # Tempo para processar e repassar o token
            send_token_to_next_element(token, next_element_port, element_id)

# Função que envia o token para o próximo elemento no anel
def send_token_to_next_element(token, next_element_port, element_id):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("localhost", next_element_port))
        token_str = str(token)
        s.sendall(token_str.encode('utf-8'))
        print(f"Elemento {element_id} do Cluster Sync: Token enviado para o próximo elemento ({next_element_port}).")

# Função para rodar múltiplos elementos do Cluster Sync
def run_cluster_elements():
    ports = [12345, 12346, 12347, 12348, 12349]  # Cada elemento tem uma porta diferente
    next_ports = [12346, 12347, 12348, 12349, 12345]  # Anel fechado
    for i in range(5):
        threading.Thread(target=cluster_sync_element, args=(i+1, ports[i], next_ports[i])).start()

if __name__ == "__main__":
    run_cluster_elements()
