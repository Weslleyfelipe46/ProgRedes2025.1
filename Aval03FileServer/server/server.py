import socket, threading

SERVER = ''
PORT = 50000
allClients = []

def trataCliente(sockCon, origem):
    print (f"Tratando conexão com {origem}")
    allClients.append(sockCon)
    try:
        while True:
            msg = sockCon.recv(4096)
            if msg != b'':
                print (f"Recebi de {origem} -> {msg.decode()}")
                for sock in allClients:
                    if sock != sockCon:
                        sock.send(msg)
            else:
                allClients.remove(sockCon)
                sockCon.close()
                print ("Fechando conexão porque o cliente fechou.")
    except:
        allClients.remove(sockCon)
        sockCon.close()
        print ("Fechando conexão porque o servidor caiu abruptamente.")

                
sockServer = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
sockServer.bind((SERVER, PORT))
sockServer.listen(5)

while True:
    print ("Aguardando conexão ...")
    sockCon, origem = sockServer.accept()
    threading.Thread(target=trataCliente, args=(sockCon, origem)).start()
