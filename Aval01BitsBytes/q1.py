Para manipular endereços IPv4 em Python utilizando listas sem funções, você pode:
1. Receber o endereço IPv4 como uma string:
Use a função input() para obter o endereço IPv4 do usuário e armazene-o numa variável.
2. Dividir a string em partes:
Use o método split('.') para dividir a string em partes, onde cada parte será um dos quatro números do IPv4.
3. Converter as partes em números:
Use a função int() para converter cada parte da string em um número inteiro.
4. Armazenar os números numa lista:
Adicione cada número inteiro convertido à lista.
Python

# Recebe o endereço IPv4 do usuário
endereco_ipv4 = input("Digite um endereço IPv4: ")

# Divide a string em partes (octetos)
octetos = endereco_ipv4.split(".")

# Cria uma lista para armazenar os números
lista_octetos = []

# Converte os octetos em números e adiciona à lista
for octeto in octetos:
    numero = int(octeto)
    lista_octetos.append(numero)

# Imprime a lista
print("Lista de octetos:", lista_octetos)
Explicação:
A função input() espera que o utilizador insira um endereço IPv4.
split(".") divide a string endereco_ipv4 em partes usando o ponto como separador, devolvendo uma lista de strings.
int() converte cada string (que representa um octeto) num inteiro.
append() adiciona cada inteiro à lista lista_octetos.
Este código permite trabalhar com endereços IPv4 em Python usando listas sem recorrer a funções adicionais.
Exemplo:
Se o utilizador inserir "192.168.1.10", o código resultará na lista [192, 168, 1, 10].
