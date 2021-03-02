
SERVER_ADDRESS = '127.0.0.1'

SERVER_PORT = 22224



def riceviComandi(socket):
    while True:
        sock_service, addr_client = socket.accept()
        print("\nConnessione ricevuta da " + str(addr_client))
        print("\nAspetto di ricevere i dati ")
        contConn = 0
        while True:
            dati = sock_service.recv(2048)
            contConn += 1
            if not dati:
                print("Fine dati dal client. Reset")
                break
         
            dati = dati.decode()
            print("Ricevuto: '%s'" % dati)
            if dati == '0':
                print("Chiudo la connessione con " + str(addr_client))
                break

            dati = dati.split(";")  
            risposta = str()

            if dati[0] == "+" or dati[0] == "-" or dati[0] == "*" or dati[0] == "/":
                try:
                    dati[1] = int(dati[1])
                    dati[2] = int(dati[2])
                except ValueError:
                    print("ValueError")
                    risposta = "Non hai inserito i numeri correttamente."

                if risposta == "": 
                    risultato = int()

                    if dati[0] == "+":
                        risultato = dati[1] + dati[2]
                    elif dati[0] == "-":
                        risultato = dati[1] - dati[2]
                    elif dati[0] == "*":
                        risultato = dati[1] * dati[2]
                    else:
                        risultato = dati[1] / dati[2]

                    risposta = "Il risultato dell'operazione " + \
                        str(dati[0]) + " tra " + str(dati[1]) + " e " + \
                        str(dati[2]) + " è uguale a " + str(risultato) + "."
            else:
                risposta = "Operazione non valida."

            risposta = risposta.encode()

            sock_service.send(risposta)
        sock_service.close()
        
def ricevi_connessioni(socket_listen):
    while True:
        socket_service, addr_client = sock_listen.accept()
        print("\nConnessione ricevuta da %s" % str(addr_client))
        print("Creo un thread per servire le richieste")
        try:
            Thread(target=riceviComandi, args=(sock_service, addr_client)).start()
        except:
            print("Il thread non si avvia")
            sock_listen.close()
            
def avviaServer(address, port):
    
    sock_listen = socket.socket()
   
    sock_listen.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
   
    sock_listen.bind((address, port))
  
    sock_listen.listen(5)
    print("Server in ascolto su %s." % str((address, port)))

    riceviComandi(sock_listen)


if __name__ == "__main__":
    avviaServer(SERVER_ADDRESS, SERVER_PORT)