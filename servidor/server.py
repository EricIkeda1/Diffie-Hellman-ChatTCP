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

PRIME = generate_random_prime()  # Número primo aleatório gerado

def generate_keys():
    private_key = random.randint(1, PRIME - 1)
    base = 3  # Defina a base como 3
    public_key = (base ** private_key) % PRIME  # Use a base para calcular a chave pública
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

    # Gera a chave privada e pública do servidor
    private_key, public_key = generate_keys()
    print(f"Servidor - Chave Pública: {public_key}")  # Exibe a chave pública do servidor

    # Envia a chave pública para o cliente
    conn.send(str(public_key).encode())

    # Recebe a chave pública do cliente
    client_public_key = int(conn.recv(1024).decode())

    # Gera a chave compartilhada inicial
    shared_key = compute_shared_key(private_key, client_public_key)
    
    while True:
        encrypted_message = conn.recv(1024).decode()
        if not encrypted_message:
            break

        print(f"Mensagem recebida de {address}: {encrypted_message}")

        # Verifica se o cliente enviou "1" para criptografar
        if encrypted_message == '1':  # Quando o cliente enviar "1", o servidor gera nova chave
            # Regenera a chave compartilhada e imprime a troca de chave
            private_key, public_key = generate_keys()  # Nova chave privada e pública
            shared_key = compute_shared_key(private_key, client_public_key)  # Nova chave compartilhada
            print(f"Nova chave pública gerada: {public_key}")

            # Envia a nova chave para o cliente
            conn.send(f"Chave trocada com sucesso. Nova chave compartilhada: {shared_key}".encode())

        else:
            # Se não for "1", o servidor assume que o cliente está enviando uma mensagem normal
            decrypted_message = cifra_cesar(encrypted_message, shared_key, modo='decifrar')
            print(f"Mensagem descriptografada: {decrypted_message}")

            # Envia de volta a mensagem criptografada ao cliente
            encrypted_response = cifra_cesar(decrypted_message, shared_key, modo='criptografar')
            conn.send(encrypted_response.encode())
            print(f"Mensagem criptografada enviada ao cliente: {encrypted_response}")

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