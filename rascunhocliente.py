import socket
import time
import threading
import random

# Função cliente para enviar uma solicitação para o Cluster Sync
def client_request(client_id, host, port):
    
    #Conexão com o elemento do cluster
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
    
        requests_number = random.randit(10,50)
    
    for i in range(requests_number):
        timestamp = time.time()  # Gera o timestamp no cliente
        request = f"REQUEST"  # Formata a mensagem da solicitação com o timestamp
        s.sendall(request.encode('utf-8'))  # Envia a solicitação ao Cluster Sync
        print(f"Cliente {client_id}: Solicitação enviada com timestamp {timestamp}")
            
        # Aguarda a resposta COMMITED do Cluster Sync
        response = s.recv(1024).decode('utf-8')
        print(f"Cliente {client_id}: Resposta recebida - {response}")
            
        #Tempo de espera
        waiting_time = random.randit(1, 5)
        time.sleep(waiting_time)

# Função para criar e rodar múltiplos clientes
def run_clients():
    cluster_elements_ports = [12345, 12346, 12347, 12348, 12349]  # Cada cliente conhece um elemento específico
    for i in range(5):
        threading.Thread(target=client_request, args=(i+1, "localhost", cluster_elements_ports[i])).start()

if __name__ == "__main__":
    run_clients()
