import socket
import random
import threading

def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

def generate_random_prime():
    while True:
        num = random.randint(2, 1000)
        if is_prime(num):
            return num

PRIME = generate_random_prime()  # Número primo aleatório gerado

def generate_keys():
    private_key = random.randint(1, PRIME - 1)
    public_key = (5 ** private_key) % PRIME
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

    private_key, public_key = generate_keys()
    print(f"Servidor - Chave Pública: {public_key}")  # Exibe a chave pública do servidor

    conn.send(str(public_key).encode())
    client_public_key = int(conn.recv(1024).decode())
    
    shared_key = compute_shared_key(private_key, client_public_key)

    while True:
        encrypted_message = conn.recv(1024).decode()
        if not encrypted_message:
            break
        print(f"Mensagem criptografada recebida de {address}: {encrypted_message}")

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
