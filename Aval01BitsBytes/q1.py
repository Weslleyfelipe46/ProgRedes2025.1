# 1) Faça um programa que recebe um string com um número IPv4 (ex:“200.17.143.131”) e uma máscara em bits (ex: 18) e responda:
        # a) Qual o endereço da rede?
        # b) Qual o endereço de broadcast?
        # c) Qual o endereço do gateway (suponha que será usado o último número IP válido o para gateway)?
        # d) Quantos hosts podem existir nessa subrede?

        # Não use strings ou bibliotecas prontas do Python. Apenas operações com bits.

#128,64,32,16,8,4,2,1

IPv4 = input('Adicione o IPv4 conforme segue o exemplo: "200.17.143.131": ')
Mascara = int(input('Adicione a Máscara em bits, exemplo: "18" :'))
Host = 32 - Mascara



print()
print("IPv4: ", IPv4)
print("Máscara: ", Mascara)
print()

Octetos = IPv4.split(".")
Lista_Octetos = []




for octeto in Octetos:
    decimal  = int(octeto)
    Lista_Octetos.append(decimal)
    #decimal = Lista_Octetos[0]  # O número decimal que você deseja converter
    binario = " "  # Inicializa uma string vazia para armazenar o resultado binário
    while decimal > 0:
            resto = decimal % 2  # Obtém o resto da divisão por 2
            binario = str(resto) + binario  # Converte o resto para string e adiciona ao início de 'binario'
            decimal = decimal // 2  # Realiza a divisão inteira por 2 (obtém o quociente)          
print("Decimal: ",  decimal, " = ", binario, "(Binário)")  # Imprime "1010"



while decimal > 0:
    resto = decimal % 2  # Obtém o resto da divisão por 2
    binario = str(resto) + binario  # Converte o resto para string e adiciona ao início de 'binario'
    decimal = decimal // 2  # Realiza a divisão inteira por 2 (obtém o quociente)
    

print("Decimal: ",  Lista_Octetos[0], " = ", binario, "(Binário)")  # Imprime "1010"


print(Lista_Octetos)
print("Octeto1 = ", Lista_Octetos[0])
print("Octeto2 = ", Lista_Octetos[1])
print("Octeto3 = ", Lista_Octetos[2])
print("Octeto4 = ", Lista_Octetos[3])
print()

