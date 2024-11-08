import socket
import threading
import json

class SecureServer:
    def __init__(self, host='localhost', port=1235):
        # Criação do socket e configuração inicial
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(2)
        self.active_clients = []  # Lista de clientes conectados
        print(f"Servidor iniciado em {host}:{port}")

    def handle_client(self, client_socket, client_address):
        # Envia mensagem inicial de configuração para o cliente
        initial_message = {
            "encryption_type": "DiffieHellman"
        }
        client_socket.send(json.dumps(initial_message).encode())

        # Loop para receber e retransmitir mensagens
        while True:
            try:
                incoming_data = client_socket.recv(1024).decode()
                if not incoming_data:
                    break
                
                # Carrega os dados recebidos e imprime informações para o administrador do servidor
                message_data = json.loads(incoming_data)
                print(f"\nServidor recebeu mensagem cifrada de {client_address}: {message_data['content']}")
                print(f"Parâmetros públicos recebidos Base: {message_data['base']}, Primo: {message_data['prime']}")

                # Aqui, o servidor gera sua chave compartilhada com a chave pública do cliente
                shared_key = self.generate_shared_key(message_data['public_key'], message_data['prime'], message_data['base'])
                message_data['shared_key'] = str(shared_key)  # Envia a chave compartilhada para o cliente

                # Envia a mensagem de volta ao cliente
                self.broadcast_message(json.dumps(message_data), client_socket)
            except Exception as e:
                print(f"Erro ao processar mensagem de {client_address}: {e}")
                break

        # Remove o cliente da lista e encerra a conexão
        self.remove_client(client_socket)
        client_socket.close()
        print(f"Cliente {client_address} foi desconectado.")

    def generate_shared_key(self, client_public_key, prime, base):
        # Geração da chave compartilhada utilizando a chave pública do cliente
        return (client_public_key ** 1) % prime  # Substitua 1 pela chave privada do servidor

    def broadcast_message(self, message, sender_socket):
        # Envia a mensagem para todos os clientes, exceto o remetente
        for client in self.active_clients:
            if client != sender_socket:
                try:
                    client.send(message.encode())
                except Exception as e:
                    print(f"Erro ao enviar mensagem para um cliente: {e}")
                    self.remove_client(client)

    def remove_client(self, client_socket):
        # Remove um cliente da lista de clientes conectados
        if client_socket in self.active_clients:
            self.active_clients.remove(client_socket)
            print("Cliente removido da lista de conexões ativas.")

    def start_server(self):
        print("Aguardando conexões de clientes...")
        while True:
            client_socket, client_address = self.server_socket.accept()
            self.active_clients.append(client_socket)
            print(f"Cliente conectado: {client_address}")
            
            # Cria e inicia uma thread para lidar com o cliente conectado
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
            client_thread.start()

if __name__ == "__main__":
    server = SecureServer()
    server.start_server()
