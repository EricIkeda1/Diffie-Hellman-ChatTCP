import socket 
import random

# Parâmetros do algoritmo Diffie-Hellman
PRIME = 23  # Número primo
BASE = 5    # Base

def generate_keys():
    private_key = random.randint(1, PRIME - 1)
    public_key = (BASE ** private_key) % PRIME
    return private_key, public_key

def compute_shared_key(private_key, public_key_received):
    shared_key = (public_key_received ** private_key) % PRIME
    return shared_key

def cifra_cesar(texto, chave, modo='criptografar'):
    resultado = ""
    for char in texto:
        if char.isalpha():
            deslocamento = chave
            base = ord('A') if char.isupper() else ord('a')
            if modo == 'criptografar':
                resultado += chr((ord(char) - base + deslocamento) % 26 + base)
            else:
                resultado += chr((ord(char) - base - deslocamento) % 26 + base)
        else:
            resultado += char
    return resultado

def server_program():
    server_socket = socket.socket()
    server_socket.bind(('localhost', 12345))
    server_socket.listen(1)
    print("Servidor esperando conexão do cliente...")

    conn, address = server_socket.accept()
    print(f"Conectado a {address}")

    # Gera a chave privada e pública apenas uma vez
    private_key, public_key = generate_keys()
    # Apenas imprime a chave pública
    print(f"Servidor - Chave Pública: {public_key}")

    # Troca de chaves públicas com o cliente
    conn.send(str(public_key).encode())
    client_public_key = int(conn.recv(1024).decode())
    shared_key = compute_shared_key(private_key, client_public_key)  # A chave compartilhada ainda é calculada, mas não é impressa

    while True:
        encrypted_message = conn.recv(1024).decode()
        if not encrypted_message:
            break
        print(f"Mensagem recebida: {encrypted_message}")

        # Decifrar a mensagem usando a chave compartilhada
        decrypted_message = cifra_cesar(encrypted_message, shared_key, modo='decifrar')
        print(f"Mensagem decifrada: {decrypted_message}")

    conn.close()

if __name__ == "__main__":
    server_program()
