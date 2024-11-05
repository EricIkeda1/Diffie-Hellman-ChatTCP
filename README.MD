# Este é um Repositório Para Diffie-Hellman-ChatTCP
> Implementando Diffie-Hellman-ChatTCP em Python. 
>
# Requisitos
>
> Estabelecimento da Conexão TCP: A comunicação deve ocorrer via protocolo TCP.
>
> Implementação do Algoritmo Diffie-Hellman: 
>
> Cada usuário deve:
>
> Calcular a chave pública e trocá-la com o outro usuário.
Gerar uma chave privada.
>
> Calcular a chave compartilhada de forma que ambos cheguem ao mesmo valor.
>
> Configuração da Cifra de César: Com a chave compartilhada derivada, defina o valor de deslocamento para a cifra de César (use o valor da chave compartilhada como base do deslocamento).
Cifrar e Decifrar as Mensagens: As mensagens enviadas devem ser cifradas com a cifra de César usando o deslocamento gerado pela chave compartilhada e, ao receber, devem ser decifradas pelo receptor.
>
> Deve gerar uma nova chave a cada mensagem enviada.
>
> Log das Operações: 
>
> Inclua mensagens no console:
>
> As chaves pública e privada de cada usuário.
>
> A chave compartilhada derivada.
>
> As mensagens cifradas e decifradas.
