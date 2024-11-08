import socket
import threading
import json
import random

class SecureServer:
    def __init__(self, host='localhost', port=1235):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(2)
        self.active_clients = []
        print(f"Servidor iniciado em {host}:{port}")

    def handle_client(self, client_socket, client_address):
        initial_message = {
            "encryption_type": "DiffieHellman"
        }
        client_socket.send(json.dumps(initial_message).encode())

        while True:
            try:
                incoming_data = client_socket.recv(1024).decode()
                if not incoming_data:
                    break

                message_data = json.loads(incoming_data)
                print(f"\nServidor recebeu mensagem cifrada de {client_address}: {message_data['content']}")
                print(f"Parâmetros públicos recebidos Base: {message_data['base']}, Primo: {message_data['prime']}")

                # Geração da chave compartilhada usando a chave pública do cliente
                shared_key = self.generate_shared_key(message_data['public_key'], message_data['prime'], message_data['base'])
                message_data['shared_key'] = str(shared_key)  # Envia a chave compartilhada para o cliente

                # Criptografar a mensagem
                encrypted_msg = self.encrypt(message_data['content'], shared_key)

                message_data['content'] = encrypted_msg
                self.broadcast_message(json.dumps(message_data), client_socket)

            except Exception as e:
                print(f"Erro ao processar mensagem de {client_address}: {e}")
                break

        self.remove_client(client_socket)
        client_socket.close()
        print(f"Cliente {client_address} foi desconectado.")

    def generate_shared_key(self, client_public_key, prime, base):
        # Geração da chave compartilhada utilizando a chave pública do cliente
        private_key = random.randint(1, prime - 1)
        shared_key = (client_public_key ** private_key) % prime
        print(f"Chave compartilhada gerada pelo servidor: {shared_key}")
        return shared_key

    def encrypt(self, message, shared_key):
        return self.cifra_cesar(message, shared_key % 26)

    def cifra_cesar(self, texto, chave):
        resultado = ""
        for char in texto:
            if char.isalpha():
                deslocamento = chave
                base = ord('A') if char.isupper() else ord('a')
                resultado += chr((ord(char) - base + deslocamento) % 26 + base)
            else:
                resultado += char
        return resultado

    def broadcast_message(self, message, sender_socket):
        for client in self.active_clients:
            if client != sender_socket:
                try:
                    client.send(message.encode())
                except Exception as e:
                    print(f"Erro ao enviar mensagem para um cliente: {e}")
                    self.remove_client(client)

    def remove_client(self, client_socket):
        if client_socket in self.active_clients:
            self.active_clients.remove(client_socket)

    def start_server(self):
        while True:
            client_socket, client_address = self.server_socket.accept()
            self.active_clients.append(client_socket)
            print(f"Novo cliente conectado: {client_address}")
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
            client_thread.start()

if __name__ == "__main__":
    server = SecureServer()
    server.start_server()
