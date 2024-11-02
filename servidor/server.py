import socket
import random
import threading

# Parâmetros do algoritmo Diffie-Hellman
PRIME = 23  # Número primo

def generate_keys():
    private_key = random.randint(1, PRIME - 1)
    public_key = (5 ** private_key) % PRIME  # Usando 5 diretamente aqui
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

def handle_client(conn, address):
    print(f"Conectado a {address}")

    # Gera a chave privada e pública
    private_key, public_key = generate_keys()
    print(f"Servidor - Chave Pública: {public_key}")

    # Troca de chaves públicas com o cliente
    conn.send(str(public_key).encode())
    client_public_key = int(conn.recv(1024).decode())
    
    # Exibe a chave pública do cliente
    print(f"Servidor - Chave Pública do Cliente ({address}): {client_public_key}")

    # Computa a chave compartilhada
    shared_key = compute_shared_key(private_key, client_public_key)

    while True:
        encrypted_message = conn.recv(1024).decode()
        if not encrypted_message:
            break
        # Exibir a mensagem criptografada recebida
        print(f"Mensagem criptografada recebida de {address}: {encrypted_message}")

        # Decifrar a mensagem usando a chave compartilhada
        decrypted_message = cifra_cesar(encrypted_message, shared_key, modo='decifrar')

        # Remova ou comente a linha abaixo para não exibir a mensagem decifrada
        # print(f"Mensagem decifrada de {address}: {decrypted_message}")

    conn.close()
    print(f"Conexão com {address} encerrada.")

def server_program():
    server_socket = socket.socket()
    server_socket.bind(('localhost', 12345))
    server_socket.listen(2)  # Permite até 2 conexões de clientes
    print("Servidor esperando conexão de clientes...")

    while True:
        conn, address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(conn, address))
        client_thread.start()

if __name__ == "__main__":
    server_program()
