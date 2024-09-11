import socket
import threading
import time
from funcoesauxiliares import *
def node(node_id, next_node_port,ip, listen_port):

    variavel_compartilhada = [False,None]

    # Cria um socket para receber conexões
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind((ip, listen_port))
    server_sock.listen()
    
    #socket para conectar com o proximo nó
    next_node_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    #iniciando thread para conectar com o proximo nó
    node_thread = threading.Thread(target=conectar_endereco, args=(next_node_sock,ip,next_node_port))
    node_thread.start()

    # Aceita conexão do nó anterior
    conn, addr = server_sock.accept()
    
    #espera o codigo conectar com o nó da frente
    node_thread.join()
    print(f"Nó {node_id} conectado ao nó anterior: {addr}")

    # Aceitar conexçao com o cliente
    print("esperando conexao do o cliente...")
    client_conn, client_addr = server_sock.accept()

    print(f"Cliente {client_addr} conectou!")
    print('esperando id do cliente')
    id_client = receber_id(client_conn)
    print("id recebido")
    
    # Criando thread para tratar o client
    client_thread = threading.Thread(target=tratar_cliente, args=(client_conn,variavel_compartilhada))
    client_thread.start()

    time.sleep(5)
    if node_id == 0:
        initialdict ={id_client:variavel_compartilhada[1]}
        countdown(5)
        enviatoken(next_node_sock,initialdict)
        print("token inicial enviado")

    while True:
        # Recebe a mensagem do nó anterior
        token = recebetoken(conn)
        
        print(f"Nó {node_id} recebeu o token: {token}")

        # alocar espaço no token caso nao exista
        if id_client not in token:
            print(f"alocando espaço no token")
            token[id_client] = variavel_compartilhada[1]

        # caso o meu timestamp seja o menor
        if process_token(token,id_client) == True:
            #acessar o recurso
            print("sou o menor")
            print("acessei o recurso")
            token[id_client] = None
            variavel_compartilhada[0] = False
            variavel_compartilhada[1] = None
        
        # caso nao tenha timestamp e o cliente esteja esperando uma mensagem
        elif variavel_compartilhada[0] == True and token[id_client] == None:
            token[id_client] = variavel_compartilhada[1]

        # se nao houver requisiçao nem nenhum timestamp no token, o token é passado para frente sem alteração
        # se houver requisiçao e o timestamp nao for o menor timestamp do token, o token é passado sem alteraçoes


        # Simula algum processamento
        time.sleep(3)
        # Envia token para o próximo nó
        print(f"enviando token para o proximo nó: {next_node_port}...")
        
        enviatoken(next_node_sock,token)