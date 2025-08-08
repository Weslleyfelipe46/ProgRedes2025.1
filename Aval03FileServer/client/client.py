# Importa as bibliotecas necessárias
import socket  # Para conexão com o servidor
import os  # Para trabalhar com arquivos
import hashlib  # Para calcular hashes MD5

class FileClient:
    def __init__(self, host='localhost', port=5000):
        # Configurações de conexão
        self.host = host  # Endereço do servidor
        self.port = port  # Porta do servidor
        
        # Pasta para salvar os downloads
        self.download_dir = os.path.join(os.path.dirname(__file__), 'arquivos')
        os.makedirs(self.download_dir, exist_ok=True)

    def connect(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(10)  # 10 segundos
            self.socket.connect((self.host, self.port))
            return True
        except socket.timeout:
            print("Erro: Tempo de conexão excedido")
        except Exception as e:
            print(f"Erro ao conectar: {e}")
        return False

    def list_files(self):
        """Obtém a lista de arquivos do servidor"""
        if not self.connect():
            return
            
        try:
            # Envia o comando LIST
            self.socket.sendall(b"LIST")
            
            # Recebe a resposta
            data = self.socket.recv(4096).decode('utf-8')
            
            # Verifica se houve erro
            if data.startswith("ERRO"):
                print(f"Erro: {data[5:]}")
            else:
                # Mostra a lista de arquivos
                print("\nArquivos disponíveis:")
                for line in data.split('\n'):
                    if line:
                        name, size = line.rsplit(' ', 1)
                        print(f"- {name} ({size} bytes)")
                        
        except Exception as e:
            print(f"Erro ao listar arquivos: {e}")
        finally:
            self.socket.close()

    def download_file(self, filename):
        """Baixa um arquivo do servidor"""
        if not self.connect():
            return
            
        try:
            # Envia o comando DOW (download)
            self.socket.sendall(f"DOW {filename}".encode('utf-8'))
            
            # Recebe a resposta inicial
            response = self.socket.recv(1024).decode('utf-8')
            
            # Verifica erros
            if response.startswith("ERRO"):
                print(f"Erro: {response[5:]}")
                return
                
            if not response.startswith("OK"):
                print("Resposta inesperada do servidor")
                return
                
            # Obtém o tamanho do arquivo
            filesize = int(response.split()[1])
            filepath = os.path.join(self.download_dir, filename)
            
            # Recebe o arquivo em pedaços
            with open(filepath, 'wb') as f:
                received = 0
                while received < filesize:
                    data = self.socket.recv(4096)
                    if not data:
                        break
                    f.write(data)
                    received += len(data)
                    
            print(f"\nArquivo '{filename}' baixado com sucesso! ({received} bytes)")
            
        except Exception as e:
            print(f"\nErro ao baixar arquivo: {e}")
            # Remove o arquivo se o download falhou
            if 'filepath' in locals() and os.path.exists(filepath):
                os.remove(filepath)
        finally:
            self.socket.close()

    def resume_download(self, filename):
        """Continua um download interrompido"""
        filepath = os.path.join(self.download_dir, filename)
        
        # Se o arquivo não existe, faz download completo
        if not os.path.exists(filepath):
            print("\nArquivo não existe, iniciando download completo...")
            self.download_file(filename)
            return
            
        # Calcula o hash da parte já baixada
        local_size = os.path.getsize(filepath)
        md5_hash = hashlib.md5()
        
        with open(filepath, 'rb') as f:
            md5_hash.update(f.read())
            
        if not self.connect():
            return
            
        try:
            # Envia comando para continuar download (DRA)
            self.socket.sendall(
                f"DRA {filename} {local_size} {md5_hash.hexdigest()}".encode('utf-8')
            )
            
            # Recebe resposta
            response = self.socket.recv(1024).decode('utf-8')
            
            # Verifica erros
            if response.startswith("ERRO"):
                print(f"\nErro: {response[5:]}")
                return
                
            if not response.startswith("OK"):
                print("\nResposta inesperada do servidor")
                return
                
            # Obtém o tamanho restante
            remaining = int(response.split()[1])
            
            # Recebe o restante do arquivo
            with open(filepath, 'ab') as f:
                received = 0
                while received < remaining:
                    data = self.socket.recv(4096)
                    if not data:
                        break
                    f.write(data)
                    received += len(data)
                    
            print(f"\nDownload continuado! {received} bytes adicionados ao arquivo.")
            
        except Exception as e:
            print(f"\nErro ao continuar download: {e}")
        finally:
            self.socket.close()

    def download_multiple(self, mask):
        # ... código existente ...
        for filename in files:
            dest_path = os.path.join(self.download_dir, filename)
            if os.path.exists(dest_path):
                overwrite = input(f"Arquivo {filename} já existe. Sobrescrever? (s/n): ").strip().lower()
                if overwrite != 's':
                    print(f"Pulando {filename}...")
                    continue
            self.download_file(filename)


def show_menu():
    """Mostra o menu de opções"""
    print("\n" + "="*40)
    print("SERVIDOR DE ARQUIVOS - MENU PRINCIPAL")
    print("="*40)
    print("1. Listar arquivos no servidor")
    print("2. Baixar arquivo")
    print("3. Continuar download interrompido")
    print("4. Baixar múltiplos arquivos (usando padrão)")
    print("5. Sair")
    print("="*40)

if __name__ == "__main__":
    # Cria o cliente
    client = FileClient()
    
    # Loop principal
    while True:
        show_menu()
        choice = input("Escolha uma opção (1-5): ")
        
        if choice == "1":
            client.list_files()
        elif choice == "2":
            filename = input("Digite o nome do arquivo: ")
            client.download_file(filename)
        elif choice == "3":
            filename = input("Digite o nome do arquivo para continuar: ")
            client.resume_download(filename)
        elif choice == "4":
            pattern = input("Digite o padrão (ex: *.txt): ")
            client.download_multiple(pattern)
        elif choice == "5":
            print("\nSaindo... Até logo!")
            break
        else:
            print("\nOpção inválida! Tente novamente.")
        
        input("\nPressione Enter para continuar...")
