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

def server_program():
    server_socket = socket.socket()
    server_socket.bind(('localhost', 12345))
    server_socket.listen(1)
    print("Servidor esperando conexão do cliente...")
    
    conn, address = server_socket.accept()
    print(f"Conectado a {address}")
    
    private_key, public_key = generate_keys()
    print(f"Servidor - Chave Privada: {private_key}, Chave Pública: {public_key}")
    
    conn.send(str(public_key).encode())
    client_public_key = int(conn.recv(1024).decode())
    shared_key = compute_shared_key(private_key, client_public_key)
    print(f"Servidor - Chave Compartilhada: {shared_key}")
    
    while True:
        # Receber mensagem cifrada
        encrypted_message = conn.recv(1024).decode()
        if not encrypted_message:
            break
        print(f"Mensagem cifrada recebida: {encrypted_message}")
        
        # Decifrar mensagem
        decrypted_message = caesar_decipher(encrypted_message, shared_key)
        print(f"Mensagem decifrada: {decrypted_message}")
        
        # Gerar nova chave compartilhada para o próximo ciclo
        private_key, public_key = generate_keys()
        conn.send(str(public_key).encode())
        client_public_key = int(conn.recv(1024).decode())
        shared_key = compute_shared_key(private_key, client_public_key)

    conn.close()

if __name__ == "__main__":
    server_program()
