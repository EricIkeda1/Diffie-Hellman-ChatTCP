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

# Configuração do servidor TCP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 5000))
server.listen(1)
print("Servidor aguardando conexão...")

client_socket, addr = server.accept()
print(f"Conexão estabelecida com {addr}")

while True:
    # Geração da chave privada e pública do servidor
    server_private = random.randint(1, p-1)
    server_public = (g ** server_private) % p
    print(f"Chave privada do servidor: {server_private}")
    print(f"Chave pública do servidor: {server_public}")

    # Envia a chave pública do servidor para o cliente
    client_socket.send(str(server_public).encode())

    # Recebe a chave pública do cliente
    client_public = int(client_socket.recv(1024).decode())
    print(f"Chave pública do cliente recebida: {client_public}")

    # Cálculo da chave compartilhada
    shared_key = (client_public ** server_private) % p
    print(f"Chave compartilhada calculada: {shared_key}")

    # Define o deslocamento da cifra de César com base na chave compartilhada
    deslocamento = shared_key

    # Recebe e decifra a mensagem do cliente
    mensagem_cifrada = client_socket.recv(1024).decode()
    print(f"Mensagem cifrada recebida do cliente: {mensagem_cifrada}")
    mensagem_decifrada = decifra_cesar(mensagem_cifrada, deslocamento)
    print(f"Mensagem decifrada: {mensagem_decifrada}")

    # Envia uma resposta cifrada para o cliente
    resposta = input("Servidor: ")
    resposta_cifrada = cifra_cesar(resposta, deslocamento)
    client_socket.send(resposta_cifrada.encode())
    print(f"Mensagem cifrada enviada para o cliente: {resposta_cifrada}")

    if resposta.lower() == 'exit':
        print("Encerrando a conexão.")
        break

client_socket.close()
server.close()
    