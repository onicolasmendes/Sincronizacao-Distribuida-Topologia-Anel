import time
import pickle

def enviar_mensagem(socket,mensagem):
    socket.send(mensagem.encode('utf-8'))
    confirmacao_de_chegada = socket.recv(2048).decode('utf-8')
    if(confirmacao_de_chegada == "confirmado"):
        return
    else:
        print("algo de errado esta acontecendo")
        print(f"esperava \"confirmado\" entretanto foi recebido {confirmacao_de_chegada}")
        return

def enviar_estrutura(socket,dado):
    socket.send(dado)
    confirmacao_de_chegada = socket.recv(2048).decode('utf-8')
    if(confirmacao_de_chegada == "confirmado"):
        return
    else:
        print("algo de errado esta acontecendo")
        print(f"esperava \"confirmado\" entretanto foi recebido {confirmacao_de_chegada}")
        return


def receber_mensagem(socket):
    dado = socket.recv(2048).decode('utf-8')
    socket.send("confirmado".encode('utf-8'))
    return dado

def receber_estrutura(socket):
    dado = socket.recv(2048)
    socket.send("confirmado".encode('utf-8'))
    return dado

def conectar_endereco(sock,ip, port,retry_interval=5):
    while True:
        try:
            # Tenta conectar ao endereço IP e porta fornecidos
            sock.connect((ip, port))
            print(f"Conectado ao endereço {ip} na porta {port}")
            return sock
        except Exception as e:
            print(f"Erro ao conectar ao endereço {ip} na porta {port}: {e}")
            print(f"Tentando novamente em {retry_interval} segundos...")
            time.sleep(retry_interval)  # Aguarda antes de tentar novamente

def receber_id(sock):
    #recebe id do cliente
    id = receber_mensagem(sock)
    id = int(id)
    return id

def tratar_cliente(sock,variavel_compartilhada):
    while True:
        time = receber_estrutura(sock)
        time = pickle.loads(time)
        variavel_compartilhada[0] = True
        variavel_compartilhada[1] = time
        print(f'recebeu timestamp {time}')
        while variavel_compartilhada[0] != False:
            continue

        enviar_mensagem(sock,"COMMITED")


def countdown(segundos):
    while segundos > 0:
        print(f"Tempo restante: {segundos} segundos")
        time.sleep(1)
        segundos -= 1
    print("Tempo esgotado!")

def recebetoken(sock):
    dado = sock.recv(2048)
    sock.send("confirmado".encode('utf-8'))
    return pickle.loads(dado)

def enviatoken(sock,token):
    paraenviar = pickle.dumps(token)
    sock.send(paraenviar)
    confirmacao_de_chegada = sock.recv(2048).decode('utf-8')
    if(confirmacao_de_chegada == "confirmado"):
        return
    else:
        print("algo de errado esta acontecendo")
        print(f"esperava \"confirmado\" entretanto foi recebido {confirmacao_de_chegada}")
        return

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
