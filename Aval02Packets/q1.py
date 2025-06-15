# q1.py - Programa para analisar pacotes de rede de um arquivo .pcap

import sys      # Usado para acessar os argumentos passados na linha de comando
import struct   # Usado para interpretar dados binários (ex: cabeçalhos dos pacotes)
import socket   # Usado para converter endereços IP em formato legível

# Verifica se o usuário passou exatamente 1 argumento além do nome do script (o nome do arquivo)
if len(sys.argv) != 2:
    print("Uso correto: python3 q1.py nome_do_arquivo.pcap")
    sys.exit(1)  # Encerra o programa com erro

# Pega o nome do arquivo informado pelo usuário na linha de comando
nome_arquivo = sys.argv[1]

# Abre o arquivo .pcap em modo de leitura binária
with open(nome_arquivo, 'rb') as arquivo:
    # Lê os primeiros 24 bytes do arquivo, que formam o cabeçalho global do pcap
    cabecalho_global = arquivo.read(24)

    # Loop que vai ler todos os pacotes do arquivo um por um
    while True:
        # Cada pacote tem um cabeçalho de 16 bytes (informações de tempo e tamanho)
        cabecalho_pacote = arquivo.read(16)

        # Se leu menos de 16 bytes, significa que chegou no final do arquivo
        if len(cabecalho_pacote) < 16:
            break

        # Desempacota os campos do cabeçalho do pacote usando struct.unpack
        # São quatro inteiros (4 bytes cada): tempo em segundos, microssegundos, tamanho capturado, tamanho original
        tempo_segundos, microssegundos, tam_capturado, tam_original = struct.unpack('IIII', cabecalho_pacote)

        # Lê os dados reais do pacote, com base no tamanho capturado
        dados = arquivo.read(tam_capturado)

        # Se o pacote tem menos de 14 bytes, não pode ter cabeçalho Ethernet, então ignora
        if len(dados) < 14:
            continue

        # ===== A) MAC Addresses =====

        # Extrai o MAC de destino (bytes 0 a 5) e formata como string hexadecimal separada por ':'
        mac_destino = ':'.join(f'{b:02x}' for b in dados[0:6])

        # Extrai o MAC de origem (bytes 6 a 11)
        mac_origem = ':'.join(f'{b:02x}' for b in dados[6:12])

        # Extrai o tipo de protocolo Ethernet (bytes 12 e 13), ex: 0x0800 = IPv4, 0x0806 = ARP
        tipo_ethernet = struct.unpack('!H', dados[12:14])[0]

        # Imprime informações do pacote atual
        print("\n----------------------------")
        print(f"PACOTE em {tempo_segundos}.{microssegundos}s")
        print(f"MAC Origem: {mac_origem}")
        print(f"MAC Destino: {mac_destino}")
        print(f"Tipo Ethernet: 0x{tipo_ethernet:04x}")

        # Define onde começa o conteúdo após o cabeçalho Ethernet (sempre após 14 bytes)
        inicio = 14

        # ===== B) ARP ou RARP =====
        if tipo_ethernet == 0x0806 or tipo_ethernet == 0x8035:
            # Verifica se há pelo menos 28 bytes após o início (tamanho do cabeçalho ARP)
            if len(dados) >= inicio + 28:
                # Extrai os campos iniciais do ARP: tipo hardware, tipo protocolo, tamanhos, operação
                tipo_hw, tipo_prot, tam_hw, tam_prot, operacao = struct.unpack('!HHBBH', dados[inicio:inicio+8])

                # Confirma se é protocolo IPv4 (0x0800), MAC tem 6 bytes, IP tem 4 bytes
                if tipo_prot == 0x0800 and tam_hw == 6 and tam_prot == 4:
                    # Extrai MAC e IP do remetente
                    mac_remetente = ':'.join(f'{b:02x}' for b in dados[inicio+8:inicio+14])
                    ip_remetente = socket.inet_ntoa(dados[inicio+14:inicio+18])

                    # Extrai MAC e IP do destinatário
                    mac_destinatario = ':'.join(f'{b:02x}' for b in dados[inicio+18:inicio+24])
                    ip_destinatario = socket.inet_ntoa(dados[inicio+24:inicio+28])

                    # Exibe informações do ARP ou RARP
                    print("ARP ou RARP:")
                    print(f"  Código da operação: {operacao}")
                    print(f"  Remetente: {mac_remetente} / {ip_remetente}")
                    print(f"  Destinatário: {mac_destinatario} / {ip_destinatario}")

        # ===== C) IPv4 =====
        elif tipo_ethernet == 0x0800:
            # Verifica se há pelo menos 20 bytes para o cabeçalho IPv4
            if len(dados) >= inicio + 20:
                # Primeiro byte tem versão (4 bits) e tamanho do cabeçalho (IHL, 4 bits)
                versao_e_ihl = dados[inicio]
                ihl = (versao_e_ihl & 0x0F) * 4  # Calcula tamanho do cabeçalho em bytes

                # Tamanho total do pacote IP
                tamanho_total = struct.unpack('!H', dados[inicio+2:inicio+4])[0]

                # Tempo de vida (TTL)
                ttl = dados[inicio+8]

                # Protocolo da camada de transporte (TCP = 6, UDP = 17, ICMP = 1)
                protocolo = dados[inicio+9]

                # Endereços IP de origem e destino
                ip_origem = socket.inet_ntoa(dados[inicio+12:inicio+16])
                ip_destino = socket.inet_ntoa(dados[inicio+16:inicio+20])

                # Imprime as informações do cabeçalho IPv4
                print("IPv4:")
                print(f"  IP Origem: {ip_origem}")
                print(f"  IP Destino: {ip_destino}")
                print(f"  IHL (Header Length): {ihl}")
                print(f"  TTL: {ttl}")
                print(f"  Protocolo IP: {protocolo}")

                # Obtém os dados da camada superior (TCP, UDP, ICMP)
                dados_ip = dados[inicio+ihl:inicio+tamanho_total]

                # ===== D) ICMP =====
                if protocolo == 1 and len(dados_ip) >= 8:
                    tipo_icmp = dados_ip[0]     # Tipo do ICMP (ex: 8 = Echo Request)
                    codigo_icmp = dados_ip[1]   # Código do ICMP (depende do tipo)
                    checksum_icmp = struct.unpack('!H', dados_ip[2:4])[0]  # Verificação

                    # Dicionário com nomes de alguns tipos de ICMP
                    nomes = {
                        0: "Echo Reply",
                        3: "Destination Unreachable",
                        5: "Redirect",
                        8: "Echo Request",
                        11: "Time Exceeded"
                    }
                    nome_icmp = nomes.get(tipo_icmp, "Outro")  # Pega o nome, se conhecido

                    # Exibe as informações
                    print("  ICMP:")
                    print(f"    Tipo: {tipo_icmp} ({nome_icmp})")
                    print(f"    Código: {codigo_icmp}")
                    print(f"    Checksum: {checksum_icmp}")

                    # Se for Echo Request (8) ou Echo Reply (0), mostra ID e sequência
                    if tipo_icmp in (0, 8):
                        identificador, sequencia = struct.unpack('!HH', dados_ip[4:8])
                        print(f"    Identificador: {identificador}")
                        print(f"    Sequência: {sequencia}")

                # ===== E) UDP =====
                elif protocolo == 17 and len(dados_ip) >= 8:
                    porta_origem, porta_destino = struct.unpack('!HH', dados_ip[0:4])
                    print("  UDP:")
                    print(f"    Porta Origem: {porta_origem}")
                    print(f"    Porta Destino: {porta_destino}")

                # ===== F) TCP =====
                elif protocolo == 6 and len(dados_ip) >= 20:
                    # Portas de origem e destino
                    porta_origem, porta_destino = struct.unpack('!HH', dados_ip[0:4])

                    # Número de sequência e número de reconhecimento (ACK)
                    numero_seq, numero_ack = struct.unpack('!II', dados_ip[4:12])

                    # Offset indica o tamanho do cabeçalho TCP
                    offset = (dados_ip[12] >> 4) * 4

                    # Flags (SYN, ACK, etc.)
                    flags = dados_ip[13]

                    # Tamanho da janela TCP
                    janela = struct.unpack('!H', dados_ip[14:16])[0]

                    # Checksum do TCP
                    checksum = struct.unpack('!H', dados_ip[16:18])[0]

                    # Exibe as informações do cabeçalho TCP
                    print("  TCP:")
                    print(f"    Porta Origem: {porta_origem}")
                    print(f"    Porta Destino: {porta_destino}")
                    print(f"    Número Seq: {numero_seq}")
                    print(f"    Número ACK: {numero_ack}")
                    print(f"    Offset (tamanho do cabeçalho TCP): {offset}")
                    print(f"    Flags: 0x{flags:02x}")
                    print(f"    Janela: {janela}")
                    print(f"    Checksum: 0x{checksum:04x}")

                    # Aqui você pode implementar a parte (G), que exibe dados da aplicação após o SYN

        else:
            # Tipo Ethernet não é ARP, RARP ou IPv4
            print("Tipo Ethernet desconhecido (não é ARP nem IPv4).")