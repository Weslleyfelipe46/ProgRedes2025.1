import socket, threading, random

PORT = 50000
SERVER = 'localhost'

def trataUsuario():
    totMsgs = random.randint(1, 5)
    nMsg = 1
    while nMsg <= totMsgs:
        msg = input (f"Digite msg ({nMsg}): ")
        sockClient.send((f"msg {nMsg} -> "+msg).encode())
        nMsg += 1
    sockClient.close()

def trataServidor():
    try:
        while True:
            msg = sockClient.recv(4096)
            print (msg.decode())
    except:
        print ("Fechando conexão porque:")
        print ("   1. limite de msgs suportado alcancado; ou ...")
        print ("   2. o servidor caiu abruptamente.")
    
sockClient = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
sockClient.connect((SERVER, PORT))

tUsuario  = threading.Thread(target=trataUsuario)
tServidor = threading.Thread(target=trataServidor)

tServidor.start()
tUsuario.start()

tServidor.join()
tUsuario.join()

sockClient.close()
