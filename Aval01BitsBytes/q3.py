print("=" * 70)
cabeçario = "Questão 03"
print(cabeçario.center(70))
print("=" * 70)

Nome_arquivo = "IMG_REDES.jpg"

# Abindo imagem
arquivo = open(Nome_arquivo, "rb")

# 6 primeiros bytes
bytes_lidos = arquivo.read(6)

# Fechando o arquivo
arquivo.close()

# Testando se leu os 6 bytes
if len(bytes_lidos) == 6:
    byte4 = bytes_lidos[4]
    byte5 = bytes_lidos[5]

    app1DataSize = (byte4 << 8 ) | byte5

    #print(f"Tamanho dos metadados APP1: {app1DataSize} bytes")
else:
    print(f"Erro: não foi possível leo os 6 primeiros bytes do arquivo")


# Abindo a imagem novamente
arquivo = open(Nome_arquivo, "rb")

# Ignorando os 4 primeiros bytes
arquivo.read(4)

# Lendo os proximos bytes
app1Data = arquivo.read(app1DataSize - 2)   # -2 porque app1DataSize inclui os 2 bytes do próprio tamanho

if len(app1Data) >= 18:     # verifando se app1Data é igual e maior que 18.
    byte16 = app1Data[16]   # Extraindo o bytes 16
    byte17 = app1Data[17]   # Extraindo o bytes

    num_metadados = (byte16 << 8) | byte17      # Calcular o num de metadados (big-endian)

    print(f"A) A imagem tem {num_metadados} metadados.")
else:
    print("Erro: Dados de APP1 insuficientes para extarir os metadados.")

# Fechando o arquivo
arquivo.close()

# Percorre os metadados a partir da posição 18
pos = 18
largura = None
altura = None

for _ in range(num_metadados):
    if pos + 12 > len(app1Data):
        break  # Evita leitura além dos dados disponíveis

    # Extrai os campos do metadado
    tag = (app1Data[pos] << 8) | app1Data[pos + 1]  # 2 bytes (identificador)
    tipo = (app1Data[pos + 2] << 8) | app1Data[pos + 3]  # 2 bytes (tipo)
    count = (app1Data[pos + 4] << 24) | (app1Data[pos + 5] << 16) | (app1Data[pos + 6] << 8) | app1Data[pos + 7]  # 4 bytes (contagem)
    valor = (app1Data[pos + 8] << 24) | (app1Data[pos + 9] << 16) | (app1Data[pos + 10] << 8) | app1Data[pos + 11]  # 4 bytes (valor/offset)

    # Verifica se é largura (0x0100) ou altura (0x0101)
    if tag == 0x0100:
        if tipo ==3:
            largura = valor # Inteiro curto (16 bits)
        elif tipo ==4:
            altura = valor # Inteiro longo (32 bits)
    elif tag == 0x0101:
        if tipo ==3:
            altura = valor # Inteiro curto (16 bits)
        elif tipo ==4:
            largura = valor # Inteiro longo (32 bits)

    pos += 12  # Avança para o próximo metadado

# Fecha o arquivo
arquivo.close()

# Exibe os resultados
if largura is not None and altura is not None:
    print(f"B) Largura da imagem: {largura} pixels")
    print(f"C) Altura da imagem: {altura} pixels")
else:
    print("B) Não foi possível encontrar largura e altura nos metadados.")