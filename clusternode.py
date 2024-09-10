import socket
import threading
import time
from funcoesauxiliares import *
def node(node_id, next_node_port, listen_port):

    Variavel_compartilhada = False
    ID_cliente = ''

    # Cria um socket para receber conexões
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind(('localhost', listen_port))
    server_sock.listen()
    
    #socket para conectar com o proximo nó
    next_node_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    #iniciando thread para conectar com o proximo nó
    node_thread = threading.Thread(target=conectar_endereco, args=(next_node_sock,'localhost',next_node_port))
    node_thread.start()

    # Aceita conexão do nó anterior
    conn, addr = server_sock.accept()
    
    #espera o codigo conectar com o nó da frente
    node_thread.join()

    # Aceitar conexçao com o cliente
    print("esperando conexao do o cliente...")
    client_conn, client_addr = server_sock.accept()

    print(f"Cliente {client_addr} conectou!")
    # Criando thread para tratar o client
    client_thread = threading.Thread(target=tratar_cliente, args=(next_node_sock,varial_compartilhada_ai))


    print(f"Nó {node_id} conectado ao nó anterior: {addr}")
    if node_id == 0:
        initialdict ={node_id:None}
        countdown(5)
        enviatoken(next_node_sock,initialdict)
        print("token inicial enviado")

    while True:
        # Recebe a mensagem do nó anterior
        token = recebetoken(conn)
        
        print(f"Nó {node_id} recebeu o token: {token}")
        
        if node_id not in token:
            print(f"alocando espaço no token")
            token[node_id] = None
            
        
        # Simula algum processamento
        time.sleep(3)
        # Envia token para o próximo nó
        print(f"enviando token para o proximo nó: {next_node_port}...")
        
    
        enviatoken(next_node_sock,token)
        print(f"Enviado!")
    


#node(0,12346,12345)
#node(1,12347,12346)
#node(2,12345,12347)