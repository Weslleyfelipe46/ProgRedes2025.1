# q2.py - Mostra no mapa o local em que uma foto foi tirada (se tiver dados de localização)

import sys          # Importa o módulo para ler argumentos da linha de comando
import subprocess   # Importa subprocess para rodar comandos no terminal
import webbrowser   # Importa para abrir o navegador

# Verifica se o usuário passou o nome do arquivo como argumento
if len(sys.argv) != 2:
    print("Uso: python3 q2.py nome_da_foto.jpg")
    sys.exit(1)  # Sai do programa com erro

# Pega o nome da foto passado como argumento
nome_arquivo = sys.argv[1]

try:
    # Executa o comando 'exif' no arquivo da foto e salva a saída
    resultado = subprocess.run(["exif", nome_arquivo], capture_output=True, text=True)

    # Salva a saída do comando exif em uma variável
    exif_saida = resultado.stdout

    # Cria variáveis para guardar os valores encontrados
    lat = None           # Vai armazenar a latitude convertida (graus decimais)
    lon = None           # Vai armazenar a longitude convertida (graus decimais)
    lat_dir = 'N'        # Direção da latitude ('N' ou 'S')
    lon_dir = 'E'        # Direção da longitude ('E' ou 'W')

    # Divide a saída em linhas para poder procurar as informações
    for linha in exif_saida.split('\n'):
        # Remove espaços no começo e no fim da linha
        linha = linha.strip()

        # Se a linha contiver Latitude
        if linha.startswith("Latitude"):
            # Pega os números da latitude (ex: 43, 27, 52.0380000)
            partes = linha.split('|')[1].strip().split(',')  # Separa os valores após a barra "|"
            graus = float(partes[0])     # Primeiro valor = graus
            minutos = float(partes[1])   # Segundo valor = minutos
            segundos = float(partes[2])  # Terceiro valor = segundos
            # Converte para graus decimais
            lat = graus + minutos/60 + segundos/3600

        # Se for Norte ou Sul
        if linha.startswith("North or South Latitude"):
            direcao = linha.split('|')[1].strip()  # Pega a letra 'N' ou 'S'
            if direcao == 'S':
                lat_dir = 'S'  # Atualiza para indicar hemisfério sul

        # Se a linha contiver Longitude
        if linha.startswith("Longitude"):
            partes = linha.split('|')[1].strip().split(',')  # Separa os valores de longitude
            graus = float(partes[0])     # Primeiro valor = graus
            minutos = float(partes[1])   # Segundo valor = minutos
            segundos = float(partes[2])  # Terceiro valor = segundos
            lon = graus + minutos/60 + segundos/3600  # Converte para graus decimais

        # Se for Leste ou Oeste
        if linha.startswith("East or West Longitude"):
            direcao = linha.split('|')[1].strip()  # Pega a letra 'E' ou 'W'
            if direcao == 'W':
                lon_dir = 'W'  # Atualiza para indicar hemisfério oeste

    # Verifica se encontrou latitude e longitude
    if lat is None or lon is None:
        print("Erro: a imagem não possui localização GPS.")
        sys.exit(1)  # Encerra o programa se não encontrar coordenadas

    # Ajusta os sinais conforme hemisfério
    if lat_dir == 'S':
        lat = -lat  # Se estiver no hemisfério sul, latitude fica negativa
    if lon_dir == 'W':
        lon = -lon  # Se estiver no hemisfério oeste, longitude fica negativa

    # Cria o link do OpenStreetMap com a posição
    url = f"https://www.openstreetmap.org/?mlat={lat}&mlon={lon}#map=15/{lat}/{lon}"

    print("Abrindo no navegador:", url)  # Mostra o link que será aberto

    # Abre o navegador com o mapa
    webbrowser.open(url)

except Exception as erro:
    # Caso ocorra algum erro (por exemplo, arquivo não encontrado), mostra mensagem
    print("Erro ao ler o arquivo ou arquivo inválido.")
    sys.exit(1)  # Sai do programa com erro
