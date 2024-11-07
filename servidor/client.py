import socket
import random

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

def factorize(n):
    factors = []
    d = 2
    while d * d <= n:
        while (n % d) == 0:
            factors.append(d)
            n //= d
        d += 1
    if n > 1:
        factors.append(n)
    return set(factors)

def is_primitive_root(q, a):
    phi_a = a - 1
    factors = factorize(phi_a)

    for factor in factors:
        k = phi_a // factor
        if pow(q, k, a) == 1:
            return False
    return True

PRIME = 353  # Define o número primo compartilhado
BASE = 3     # Define a base compartilhada

def generate_keys():
    private_key = random.randint(1, PRIME - 1)
    public_key = pow(BASE, private_key, PRIME)
    return private_key, public_key

def compute_shared_key(private_key, public_key_received):
    shared_key = pow(public_key_received, private_key, PRIME)
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

def client_program():
    client_socket = socket.socket()
    client_socket.connect(('localhost', 12345))

    private_key, public_key = generate_keys()
    print(f"Cliente - Chave Privada: {private_key}, Chave Pública: {public_key}")

    client_socket.send(str(public_key).encode())
    server_public_key = int(client_socket.recv(1024).decode())
    print(f"Cliente - Chave Pública do Servidor: {server_public_key}")

    shared_key = compute_shared_key(private_key, server_public_key)
    print(f"Cliente - Chave Compartilhada: {shared_key}")

    while True:
        print("\nEscolha uma opção:")
        print("1. Criptografar")
        print("2. Descriptografar")
        print("3. Sair")

        modo = input("Digite o número da opção desejada: ")

        if modo not in ['1', '2', '3']:
            print("Opção inválida! Tente novamente.")
            continue

        if modo == '3':  # Sair
            print("Encerrando conexão.")
            break

        message = input("Digite a mensagem para enviar: ")

        if modo == '1':  # Criptografar e enviar
            encrypted_message = cifra_cesar(message, shared_key, modo='criptografar')
            print(f"Mensagem cifrada enviada: {encrypted_message}")
            client_socket.send(encrypted_message.encode())

        elif modo == '2':  # Enviar e receber mensagem descriptografada
            print(f"Mensagem cifrada enviada: {message}")
            client_socket.send(message.encode())

            # Recebe a resposta criptografada do servidor e a descriptografa localmente
            encrypted_response = client_socket.recv(1024).decode()
            decrypted_response = cifra_cesar(encrypted_response, shared_key, modo='decifrar')
            print(f"Mensagem decifrada recebida: {decrypted_response}")

    client_socket.close()

if __name__ == "__main__":
    client_program()
