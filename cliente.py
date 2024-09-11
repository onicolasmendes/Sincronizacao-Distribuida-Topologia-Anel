import socket
import threading
import time
import pickle
import random
from funcoesauxiliares import enviar_mensagem,receber_mensagem,enviar_estrutura,receber_estrutura

def cliente(id,node_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost',node_port))
    print(f"conectado ao nó {node_port}")

    # enviando id
    print(f"enviando id: {id}:")
    enviar_mensagem(sock,id)
    print(f'id enviado')
    # definindo quantidade de requests
    requests_number = random.randint(10,50)

    while True:
        # enviando time stamp
        print('enviando timestamp')
        timestamp = pickle.dumps(time.time())
        enviar_estrutura(sock, timestamp)
        print(f"time stamp enviado")
        # esperando mensagem de commit
        resposta = receber_mensagem(sock)
        
        print(f'recebeu resposta: {resposta}')
        time_sleep = random.randint(1,5)
        print(f"dormindo por {time_sleep} segundos")
        time.sleep(time_sleep)        

