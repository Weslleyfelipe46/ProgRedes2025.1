import hashlib, time, struct

def findNonce(dataToHash, bitsToBeZero):
    start_time = time.time() # Inicializa para medir o tempo de execução.
    prefixo = '0' * (bitsToBeZero // 4)
    if bitsToBeZero % 4 != 0:
        prefixo += '0'

    nonce = 0
    while True:
        # Concatena o nonce (como big-endian de 4 bytes) aos dados_com_nonce
        dados_com_nonce = struct.pack('>I', nonce) + dataToHash

        # Calcula o hash SHA-256
        hashed_data = hashlib.sha256(dados_com_nonce).hexdigest()

        # Verifica se o hash começa com o número desejado de bits zero
        if hashed_data.startswith(prefixo):
            end_time = time.time()
            return nonce, hashed_data, end_time - start_time

        nonce += 1
        # Adiciona uma condição de timeout para evitar loops infinitos (opcional, mas recomendado)
        if time.time() - start_time > 60:  # Por exemplo, timeout de 60 segundos
            return None, None, None

def converter_para_bytes(texto):
    """Converte uma string para bytes usando a codificação UTF-8."""
    return texto.encode('utf-8')

if __name__ == "__main__":
    tabela_dados = [
        ("Esse um texto elementar", 8),
        ("Esse um texto elementar", 10),
        ("Esse um texto elementar", 15),
        ("Textinho", 8),
        ("Textinho", 18),
        ("Textinho", 22),
        ("Meu texto médio", 18),
        ("Meu texto médio", 19),
        ("Meu texto médio", 20),
    ]

    print(f"{'Texto a validar':<30} | {'Bits em zero':<12} | {'Nonce':<10} | {'Tempo (em s)':<15}")
    print("-" * 70)

    for texto, bits in tabela_dados:
        data_bytes = converter_para_bytes(texto)
        nonce_encontrado, hash_encontrado, tempo_gasto = findNonce(data_bytes, bits)

        if nonce_encontrado is not None:
            print(f"{texto:<30} | {bits:<12} | {nonce_encontrado:<10} | {tempo_gasto:<15.4f}")
        else:
            print(f"{texto:<30} | {bits:<12} | {'N/A':<10} | {'Timeout':<15}")