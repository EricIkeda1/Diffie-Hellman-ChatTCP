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
            else:  # modo == 'decifrar'
                resultado += chr((ord(char) - base - deslocamento) % 26 + base)
        else:
            resultado += char
    return resultado

def receive_messages(client_socket):
    while True:
        try:
            response = client_socket.recv(1024).decode()
            if response:
                decrypted_response = cifra_cesar(response, shared_key, modo='decifrar')
                print(f"\nMensagem recebida do outro cliente (decifrada): {decrypted_response}")
            else:
                break
        except:
            print("Erro ao receber a mensagem.")
            break

def client_program():
    global shared_key
    client_socket = socket.socket()
    client_socket.connect(('localhost', 12345))

    private_key, public_key = generate_keys()
    print(f"Cliente - Chave Privada: {private_key}, Chave Pública: {public_key}")

    client_socket.send(str(public_key).encode())
    server_public_key = int(client_socket.recv(1024).decode())
    print(f"Cliente - Chave Pública do Servidor: {server_public_key}")

    shared_key = compute_shared_key(private_key, server_public_key)
    print(f"Cliente - Chave Compartilhada: {shared_key}")

    # Iniciar thread para receber mensagens
    threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()

    while True:
        print("\nEscolha uma opção:")
        print("1. Criptografar Mensagem")
        print("2. Descriptografar Mensagem")
        print("3. Sair")

        option = input("Digite o número da opção: ")
        if option == '1':
            message = input("Digite a mensagem para criptografar: ")
            encrypted_message = cifra_cesar(message, shared_key, modo='criptografar')
            print(f"Mensagem cifrada: {encrypted_message}")
            client_socket.send(encrypted_message.encode())

        elif option == '2':
            message = input("Digite a mensagem cifrada para descriptografar: ")
            decrypted_message = cifra_cesar(message, shared_key, modo='decifrar')
            print(f"Mensagem decifrada: {decrypted_message}")

        elif option == '3':
            print("Encerrando conexão.")
            break

        else:
            print("Opção inválida! Tente novamente.")

    client_socket.close()

if __name__ == "__main__":
    client_program()
