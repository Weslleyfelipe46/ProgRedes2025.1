# Importa as bibliotecas necessárias
import socket  # Para conexões de rede
import os  # Para trabalhar com arquivos
import threading  # Para atender vários clientes ao mesmo tempo
import hashlib  # Para calcular hashes MD5
import glob  # Para buscar arquivos com máscaras

class FileServer:
    def __init__(self, host='localhost', port=5000):
        # Configurações básicas do servidor
        self.host = host  # Endereço onde o servidor vai rodar
        self.port = port  # Porta de comunicação
        self.server_socket = None  # Socket do servidor
        self.files_dir = os.path.join(os.path.dirname(__file__), 'arquivos')  # Pasta de arquivos
        
        # Cria a pasta se não existir
        os.makedirs(self.files_dir, exist_ok=True)

    def start(self):
        """Inicia o servidor principal"""
        try:
            # Cria o socket TCP
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # Associa o socket ao endereço e porta
            self.server_socket.bind((self.host, self.port))
            
            # Começa a ouvir conexões (máximo 5 na fila)
            self.server_socket.listen(5)
            print(f"Servidor pronto em {self.host}:{self.port}")
            
            # Loop principal para aceitar clientes
            while True:
                # Aceita uma nova conexão
                conn, addr = self.server_socket.accept()
                print(f"Cliente conectado: {addr}")
                
                # Cria uma thread para cada cliente
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(conn,)
                )
                client_thread.start()
                
        except Exception as e:
            print(f"Erro no servidor: {e}")
        finally:
            # Garante que o socket será fechado
            if self.server_socket:
                self.server_socket.close()

    def handle_client(self, conn):
        """Lida com as requisições de um cliente"""
        try:
            while True:
                # Recebe o comando do cliente
                data = conn.recv(1024).decode('utf-8').strip()
                if not data:
                    break
                
                # Divide o comando em partes
                parts = data.split()
                command = parts[0].upper()  # O comando é sempre a primeira palavra
                
                # Processa cada tipo de comando
                if command == "LIST":
                    self.send_file_list(conn)
                elif command == "DOW" and len(parts) == 2:
                    self.send_file(conn, parts[1])
                elif command == "MD5" and len(parts) == 3:
                    self.send_md5(conn, parts[1], int(parts[2]))
                elif command == "DRA" and len(parts) == 4:
                    self.resume_download(conn, parts[1], int(parts[2]), parts[3])
                elif command == "DMA" and len(parts) == 2:
                    self.send_matching_files(conn, parts[1])
                else:
                    conn.sendall(b"ERRO: Comando invalido")
                    
        except Exception as e:
            print(f"Erro com cliente: {e}")
        finally:
            conn.close()

    def send_file_list(self, conn):
        """Envia a lista de arquivos disponíveis"""
        try:
            files = []
            # Lista todos os arquivos na pasta
            for filename in os.listdir(self.files_dir):
                filepath = os.path.join(self.files_dir, filename)
                if os.path.isfile(filepath):
                    # Adiciona nome e tamanho do arquivo
                    size = os.path.getsize(filepath)
                    files.append(f"{filename} {size}")
            
            # Envia a lista para o cliente
            conn.sendall("\n".join(files).encode('utf-8'))
            
        except Exception as e:
            print(f"Erro ao listar arquivos: {e}")
            conn.sendall(b"ERRO: Falha ao listar arquivos")

    def send_file(self, conn, filename):
        """Envia um arquivo para o cliente"""
        try:
            filepath = self.get_valid_path(filename)
            filesize = os.path.getsize(filepath)
            
            # Informa o tamanho do arquivo primeiro
            conn.sendall(f"OK {filesize}".encode('utf-8'))
            
            # Envia o arquivo em pedaços de 4KB
            with open(filepath, 'rb') as f:
                while True:
                    data = f.read(4096)
                    if not data:
                        break
                    conn.sendall(data)
                    
        except Exception as e:
            print(f"Erro ao enviar arquivo: {e}")
            conn.sendall(b"ERRO: Falha ao enviar arquivo")

    def send_md5(self, conn, filename, position):
        """Calcula e envia o hash MD5 de parte de um arquivo"""
        try:
            filepath = self.get_valid_path(filename)
            
            # Verifica se a posição é válida
            if position > os.path.getsize(filepath):
                raise ValueError("Posição inválida")
            
            # Calcula o hash MD5
            md5_hash = hashlib.md5()
            with open(filepath, 'rb') as f:
                md5_hash.update(f.read(position))
                
            # Envia o hash para o cliente
            conn.sendall(f"OK {md5_hash.hexdigest()}".encode('utf-8'))
            
        except Exception as e:
            print(f"Erro ao calcular MD5: {e}")
            conn.sendall(b"ERRO: Falha ao calcular MD5")

    def resume_download(self, conn, filename, position, client_hash):
        """Continua um download a partir de uma posição específica"""
        try:
            filepath = self.get_valid_path(filename)
            filesize = os.path.getsize(filepath)
            
            # Verifica se o hash da parte existente confere
            md5_hash = hashlib.md5()
            with open(filepath, 'rb') as f:
                md5_hash.update(f.read(position))
                
            if md5_hash.hexdigest() != client_hash:
                conn.sendall(b"ERRO: Hash nao confere")
                return
                
            # Envia o restante do arquivo
            remaining = filesize - position
            conn.sendall(f"OK {remaining}".encode('utf-8'))
            
            with open(filepath, 'rb') as f:
                f.seek(position)
                while remaining > 0:
                    data = f.read(4096)
                    if not data:
                        break
                    conn.sendall(data)
                    remaining -= len(data)
                    
        except Exception as e:
            print(f"Erro ao continuar download: {e}")
            conn.sendall(b"ERRO: Falha ao continuar download")

    def handle_multi(self, conn, mask):
        try:
            files = glob.glob(os.path.join(self.files_dir, mask))
            valid_files = [f for f in files if os.path.isfile(f) and f.startswith(self.files_dir)]
            if not valid_files:
                conn.sendall(b"ERRO: Nenhum arquivo corresponde a mascara")
            else:
                conn.sendall("\n".join([os.path.basename(f) for f in valid_files]).encode('utf-8'))
        except Exception as e:
            conn.sendall(f"ERRO: {str(e)}".encode('utf-8'))

    def validate_filepath(self, filename):
        filepath = os.path.realpath(os.path.join(self.files_dir, filename))
        if not filepath.startswith(os.path.realpath(self.files_dir)):
            raise ValueError("Tentativa de acesso a caminho não permitido!")
        if not os.path.isfile(filepath):
            raise FileNotFoundError("Arquivo não existe")
        return filepath

if __name__ == "__main__":
    # Cria e inicia o servidor
    server = FileServer()
    server.start()
