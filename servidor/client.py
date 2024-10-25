import socket
import random
import hashlib

# Parâmetros Diffie-Hellman
g = 5  # Gerador
p = 23 # Número primo

# Função de cifra de César
def cifra_cesar(mensagem, deslocamento):
    return ''.join(chr((ord(char) + deslocamento - 32) % 95 + 32) for char in mensagem)

# Função de decifra de César
def decifra_cesar(mensagem, deslocamento):
    return ''.join(chr((ord(char) - deslocamento - 32) % 95 + 32) for char in mensagem)

# Configuração do cliente TCP
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 5000))

while True:
    # Geração da chave privada e pública do cliente
    client_private = random.randint(1, p-1)
    client_public = (g ** client_private) % p
    print(f"Chave privada do cliente: {client_private}")
    print(f"Chave pública do cliente: {client_public}")

    # Envia a chave pública do cliente para o servidor
    client.send(str(client_public).encode())

    # Recebe a chave pública do servidor
    server_public = int(client.recv(1024).decode())
    print(f"Chave pública do servidor recebida: {server_public}")

    # Cálculo da chave compartilhada
    shared_key = (server_public ** client_private) % p
    print(f"Chave compartilhada calculada: {shared_key}")

    # Define o deslocamento da cifra de César com base na chave compartilhada
    deslocamento = shared_key

    # Envia uma mensagem cifrada para o servidor
    mensagem = input("Cliente: ")
    mensagem_cifrada = cifra_cesar(mensagem, deslocamento)
    client.send(mensagem_cifrada.encode())
    print(f"Mensagem cifrada enviada para o servidor: {mensagem_cifrada}")

    if mensagem.lower() == 'exit':
        print("Encerrando a conexão.")
        break

    # Recebe e decifra a resposta do servidor
    resposta_cifrada = client.recv(1024).decode()
    print(f"Mensagem cifrada recebida do servidor: {resposta_cifrada}")
    resposta_decifrada = decifra_cesar(resposta_cifrada, deslocamento)
    print(f"Mensagem decifrada: {resposta_decifrada}")

client.close()
