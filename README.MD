# Este é um Repositório Para Diffie-Hellman-ChatTCP
> Implementação de um chat TCP com criptografia utilizando o algoritmo Diffie-Hellman e a cifra de César em Python.

## Descrição

Este projeto implementa uma comunicação segura entre dois usuários utilizando o algoritmo **Diffie-Hellman** para a troca de chaves públicas e derivação de uma chave compartilhada. As mensagens trocadas entre os usuários são criptografadas utilizando a **Cifra de César**, onde o valor de deslocamento é derivado da chave compartilhada.

### Funcionalidades

1. **Estabelecimento da Conexão TCP**:
    - A comunicação ocorre via protocolo **TCP** entre o cliente e o servidor. O servidor fica aguardando uma conexão, e o cliente se conecta ao servidor para iniciar a troca de mensagens.

2. **Implementação do Algoritmo Diffie-Hellman**:
    - Cada usuário gera sua chave privada e pública.
    - As chaves públicas são trocadas entre os usuários.
    - Ambos os usuários calculam a chave compartilhada com base nas chaves públicas recebidas e suas chaves privadas.

3. **Cifra de César**:
    - Com a chave compartilhada derivada, é calculado o valor do deslocamento para a **Cifra de César** (o deslocamento será o valor da chave compartilhada).
    - As mensagens enviadas são cifradas com a Cifra de César usando o deslocamento calculado pela chave compartilhada.
    - Ao receber uma mensagem, o receptor a decifra utilizando a mesma chave compartilhada.

4. **Geração de Nova Chave a Cada Mensagem**:
    - A cada nova mensagem enviada, uma nova chave compartilhada é gerada, garantindo maior segurança nas trocas de mensagens.

5. **Logs das Operações**:
    - O console exibe informações sobre as chaves pública e privada de cada usuário.
    - A chave compartilhada derivada.
    - As mensagens cifradas e decifradas.

## Como Rodar?

### **Rodando o Servidor**

- Abra **3 PowerShell** ou terminais separados para rodar os seguintes comandos:

   - **No primeiro terminal, com 2 terminais**, execute o comando abaixo para iniciar o **cliente**:
     ```powershell
     python client.py
     ```

   - **No segundo terminal, com 1 terminal**, execute o comando abaixo para iniciar o **servidor**:
     ```powershell
     python server.py
     ```
