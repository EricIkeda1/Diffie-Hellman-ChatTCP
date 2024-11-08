import socket
import threading
import json
import random

class DiffieHellman:
    def __init__(self):
        self.generate_new_keys()

    def generate_new_keys(self):
        self.prime = self.generate_random_prime()
        self.base = random.randint(2, self.prime - 1)
        self.private_key = random.randint(1, self.prime - 1)
        self.public_key = self.mod_exp(self.base, self.private_key, self.prime)
        self.shared_key = None

    def generate_random_prime(self, min_val=0, max_val=999):
        def is_prime(n):
            if n < 2:
                return False
            for i in range(2, int(n ** 0.5) + 1):
                if n % i == 0:
                    return False
            return True

        while True:
            num = random.randint(min_val, max_val)
            if is_prime(num):
                return num

    def mod_exp(self, base, exp, mod):
        result = 1
        base = base % mod
        while exp > 0:
            if exp & 1:
                result = (result * base) % mod
            base = (base * base) % mod
            exp >>= 1
        return result

    def generate_shared_key(self, other_public_key):
        self.shared_key = self.mod_exp(other_public_key, self.private_key, self.prime)
        return self.shared_key

    def encrypt(self, message):
        if not self.shared_key:
            print("Chave compartilhada não gerada")
            return message
        return self.cifra_cesar(message, self.shared_key % 26)

    def decrypt(self, message, shared_key, prime):
        self.shared_key = shared_key
        self.prime = prime
        return self.cifra_cesar(message, 26 - (self.shared_key % 26))

    def cifra_cesar(self, texto, chave, modo='criptografar'):
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

class Client:
    def __init__(self, host='localhost', port=1235):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        self.diffie_hellman = DiffieHellman()

    def receive_messages(self):
        while True:
            try:
                message = self.socket.recv(1024).decode()
                if message:
                    data = json.loads(message)

                    if 'encryption_type' in data:
                        print("Chat-tcp | DiffieHellman")
                        self.server_public_key = data['public_key'] 
                        continue

                    if 'content' in data:
                        encrypted_msg = data['content']
                        shared_key = int(data['shared_key'])
                        prime = int(data['prime'])
                        decrypted_msg = self.diffie_hellman.decrypt(encrypted_msg, shared_key, prime)

                        print("\n" + "="*50)
                        print("Mensagem recebida:")
                        print("="*50)
                        print(f"\nMensagem cifrada: {encrypted_msg}")
                        print(f"Mensagem decifrada: {decrypted_msg}")
                        print(f"Base: {data['base']}")
                        print(f"Primo: {data['prime']}")
                        print(f"Chave compartilhada: {shared_key}")
                        print("="*50 + "\n")
            except Exception as e:
                print(f"Erro: {e}")
                break

    def send_message(self, message):
        self.diffie_hellman.generate_new_keys()

        shared_key = self.diffie_hellman.generate_shared_key(self.server_public_key)

        data = {
            'content': message,
            'base': self.diffie_hellman.base,
            'prime': self.diffie_hellman.prime,
            'public_key': self.diffie_hellman.public_key,
            'shared_key': shared_key
        }

        self.socket.send(json.dumps(data).encode())

        print("\n" + "="*50)
        print("Mensagem enviada:")
        print("="*50)
        print(f"\nMensagem original: {message}")
        print(f"Base: {self.diffie_hellman.base}")
        print(f"Primo: {self.diffie_hellman.prime}")
        print(f"Chave privada: {self.diffie_hellman.private_key}")
        print(f"Chave pública: {self.diffie_hellman.public_key}")
        print(f"Chave compartilhada: {shared_key}")
        print("="*50 + "\n")

    def start(self):
        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.daemon = True
        receive_thread.start()

        while True:
            message = input("Digite sua mensagem (ou 'sair' para desconectar): ")
            if message.lower() == 'sair':
                print("Saindo...")
                break
            self.send_message(message)

if __name__ == "__main__":
    client = Client()
    client.start()
