import socket
import random

# Parâmetros do algoritmo Diffie-Hellman
PRIME = 23  # Número primo
BASE = 5    # Base

# Função para gerar a chave privada e calcular a chave pública
def generate_keys():
    private_key = random.randint(1, PRIME - 1)
    public_key = (BASE ** private_key) % PRIME
    return private_key, public_key

# Função para calcular a chave compartilhada
def compute_shared_key(private_key, public_key_received):
    shared_key = (public_key_received ** private_key) % PRIME
    return shared_key

# Função de cifra de César usando ASCII
def caesar_cipher(text, shift):
    return ''.join(chr((ord(char) + shift) % 128) for char in text)

# Função de decifra da cifra de César usando ASCII
def caesar_decipher(text, shift):
    return ''.join(chr((ord(char) - shift) % 128) for char in text)

def client_program():
    client_socket = socket.socket()
    client_socket.connect(('localhost', 12345))
    
    private_key, public_key = generate_keys()
    print(f"Cliente - Chave Privada: {private_key}, Chave Pública: {public_key}")
    
    server_public_key = int(client_socket.recv(1024).decode())
    client_socket.send(str(public_key).encode())
    shared_key = compute_shared_key(private_key, server_public_key)
    print(f"Cliente - Chave Compartilhada: {shared_key}")
    
    while True:
        # Mensagem para enviar
        message = input("Digite a mensagem para enviar: ")
        if message.lower() == 'sair':
            print("Encerrando conexão.")
            break
        
        # Cifrar mensagem
        encrypted_message = caesar_cipher(message, shared_key)
        print(f"Mensagem cifrada enviada: {encrypted_message}")
        client_socket.send(encrypted_message.encode())
        
        # Gerar nova chave compartilhada para o próximo ciclo
        private_key, public_key = generate_keys()
        client_socket.send(str(public_key).encode())
        server_public_key = int(client_socket.recv(1024).decode())
        shared_key = compute_shared_key(private_key, server_public_key)

    client_socket.close()

if __name__ == "__main__":
    client_program()
