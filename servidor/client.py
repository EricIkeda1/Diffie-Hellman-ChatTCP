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

# Função de cifra de César
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
        modo = input("Digite 1 para criptografar ou 2 para descriptografar a mensagem: ")
        if modo not in ['1', '2']:
            print("Opção inválida! Tente novamente.")
            continue

        message = input("Digite a mensagem para enviar: ")
        if message.lower() == 'sair':
            print("Encerrando conexão.")
            break

        if modo == '1':  # Criptografar e enviar
            encrypted_message = cifra_cesar(message, shared_key, modo='criptografar')
            print(f"Mensagem cifrada enviada: {encrypted_message}")
            client_socket.send(encrypted_message.encode())
        elif modo == '2':  # Descriptografar a mensagem recebida
            decrypted_message = cifra_cesar(message, shared_key, modo='decifrar')
            print(f"Mensagem decifrada enviada: {decrypted_message}")
            client_socket.send(decrypted_message.encode())

        private_key, public_key = generate_keys()
        client_socket.send(str(public_key).encode())
        server_public_key = int(client_socket.recv(1024).decode())
        shared_key = compute_shared_key(private_key, server_public_key)
        print(f"Nova Chave Compartilhada: {shared_key}")

    client_socket.close()

if __name__ == "__main__":
    client_program()
