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
        num = random.randint(0, 999)
        if is_prime(num):
            return num

PRIME = generate_random_prime()

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

clients = []

def handle_client(conn, address):
    print(f"Conectado a {address}")

    # Gera a chave privada e pública do servidor
    private_key, public_key = generate_keys()
    
    # Envia a chave pública do servidor para o cliente
    conn.send(str(public_key).encode())
    
    # Recebe a chave pública do cliente
    client_public_key = int(conn.recv(1024).decode())
    print(f"Chave Pública do Cliente ({address}): {client_public_key}")

    # Calcula a chave compartilhada
    shared_key = compute_shared_key(private_key, client_public_key)

    # Adiciona o cliente à lista de conexões
    clients.append(conn)

    while True:
        try:
            # Recebe a mensagem do cliente
            encrypted_message = conn.recv(1024).decode()
            if not encrypted_message:
                break

            # Exibe a mensagem criptografada recebida
            print(f"Mensagem criptografada recebida de {address}: {encrypted_message}")

            # Descriptografa a mensagem
            decrypted_message = cifra_cesar(encrypted_message, shared_key, modo='decifrar')
            print(f"Mensagem descriptografada: {decrypted_message}")

            # Não envia a mensagem para outros clientes
        except:
            break

    # Fecha a conexão e remove o cliente da lista
    conn.close()
    clients.remove(conn)
    print(f"Conexão com {address} encerrada.")

def server_program():
    server_socket = socket.socket()
    server_socket.bind(('localhost', 12345))
    server_socket.listen(5)  # Permite múltiplas conexões
    print("Servidor esperando conexão de clientes...")

    while True:
        conn, address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(conn, address))
        client_thread.start()

if __name__ == "__main__":
    server_program()
