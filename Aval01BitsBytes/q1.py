IPv4 = input('Adicione o IPv4 conforme segue o exemplo: "200.17.143.131": ')
mascara_bits = int(input('Adicione a Máscara em bits, exemplo: "18" :'))

Octetos = IPv4.split(".")
Lista_Octetos = []

for octeto in Octetos:
    Num = decimal  = int(octeto)
    Lista_Octetos.append(decimal)
    binario = " "  # Inicializa uma string vazia para armazenar o resultado binário
    while decimal > 0:
            resto = decimal % 2  # Obtém o resto da divisão por 2
            binario = str(resto) + binario  # Converte o resto para string e adiciona ao início de 'binario'
            decimal = decimal // 2  # Realiza a divisão inteira por 2 (obtém o quociente)


# Cada Bloco de Ip separados por Octetos
ip_oct1 = Lista_Octetos[0]
ip_oct2 = Lista_Octetos[1]
ip_oct3 = Lista_Octetos[2]
ip_oct4 = Lista_Octetos[3]

# 1. Converter IP para número inteiro de 32 bits
ip_int = (ip_oct1 << 24) | (ip_oct2 << 16) | (ip_oct3 << 8) | ip_oct4

# 2. Calcular máscara de rede
mascara = (0xFFFFFFFF << (32 - mascara_bits)) & 0xFFFFFFFF

# a) Endereço de rede
rede = ip_int & mascara

# b) Endereço de broadcast
broadcast = rede | (1 << (32 - mascara_bits))- 1

# c) Endereço do gateway (Primeiro IP válido)
gateway = rede + 1

# d) Número de hosts possíveis
num_hosts = (1 << (32 - mascara_bits)) - 2

# Extraindo o endereço de rede
rede_oct1 = (rede >> 24) & 0xFF
rede_oct2 = (rede >> 16) & 0xFF
rede_oct3 = (rede >> 8) & 0xFF
rede_oct4 = rede & 0xFF

# Extraindo o broadcast
broadcast_oct1 = (broadcast >> 24) & 0xFF
broadcast_oct2 = (broadcast >> 16) & 0xFF
broadcast_oct3 = (broadcast >> 8) & 0xFF
broadcast_oct4 = broadcast & 0xFF

# Extraindo o gateway
gateway_oct1 = (gateway >> 24) & 0xFF
gateway_oct2 = (gateway >> 16) & 0xFF
gateway_oct3 = (gateway >> 8) & 0xFF
gateway_oct4 = gateway & 0xFF

# Resultados
print(f"a) Endereço da rede: {rede_oct1}.{rede_oct2}.{rede_oct3}.{rede_oct4}")
print(f"b) Endereço de broadcast: {broadcast_oct1}.{broadcast_oct2}.{broadcast_oct3}.{broadcast_oct4}")
print(f"c) Endereço do gateway: {gateway_oct1}.{gateway_oct2}.{gateway_oct3}.{gateway_oct4}")
print(f"d) Número de hosts possíveis: {num_hosts}")