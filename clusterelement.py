import socket
import threading
import time

# Simula o acesso ao recurso compartilhado (seção crítica)
def access_resource(element_id):
    print(f"Elemento {element_id} do Cluster Sync: Acessando o recurso R...")
    time.sleep(0.5)
    print(f"Elemento {element_id} do Cluster Sync: Saindo da seção crítica.")

# Função para processar o token e verificar se o elemento pode entrar na seção crítica
def process_token(token, timestamp, element_id):
    # Insere o timestamp do cliente no token
    token.append((timestamp, f"Elemento {element_id}"))
    print(f"Elemento {element_id} do Cluster Sync: Timestamp {timestamp} inserido no token.")

    # Verifica se o timestamp inserido é o menor
    valid_timestamps = [t for t, _ in token if t is not None]
    if valid_timestamps:
        min_timestamp = min(valid_timestamps)
        if timestamp == min_timestamp:
            print(f"Elemento {element_id} do Cluster Sync: Menor timestamp detectado ({timestamp}). Entrando na seção crítica.")
            access_resource(element_id)
            return True
    return False

# Função que simula um elemento do Cluster Sync recebendo solicitações de clientes
def handle_client(connection, address, token, element_id):
    with connection:
        print(f"Elemento do Cluster Sync {element_id}: Conectado ao cliente {address}")
        data = connection.recv(1024).decode('utf-8')

        if data.startswith("REQUEST"):
            # Extraindo o timestamp da solicitação do cliente
            timestamp = float(data.split()[1])
            print(f"Elemento do Cluster Sync {element_id}: Solicitação recebida com timestamp {timestamp}")

            # Aguardar o token e processá-lo
            if process_token(token, timestamp, element_id):
                response = f"Acesso concedido pelo Elemento {element_id} com timestamp {timestamp}"
            else:
                response = f"Acesso negado pelo Elemento {element_id} com timestamp {timestamp}"

            # Envia a resposta ao cliente
            connection.sendall(response.encode('utf-8'))

# Função principal de um elemento do Cluster Sync
def cluster_sync_element(element_id, port, next_element_port):
    token = []  # O token começa vazio
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
