# Corso di Programmazione di Reti - Laboratorio - Universit�  di Bologna
# Socket_Programming_Assignment - WebServer - F. Callegati - G.Pau - A. Piroddi

import sys
from socket import * 

# Specifichiamo la porta su cui il server lavorerà:
serverPort=8080

# COMANDO SOCKET(socket_family, socket_type):
#
#   --> "SOCKET_FAMILY corrisponde alla tipologia di indirizzo con cui si vuole lavorare:"
#           1) AF_INET: "Indica la famiglia di indirizzi IPv4".
#           2) AF_INET6: "Indica la famiglia di indirizzi IPv6".
#   --> "SOCKET_TYPE corrisponde alla tipologia di socket che vogliamo creare:"
#           1) SOCK_STREAM: "Indica un socket orientato alla connessione (TCP)".
#           2) SOCK_DGRAM: "Indica un socket non orientato alla connessione (UDP)".
serverSocket = socket(AF_INET, SOCK_STREAM)

# Costruiamo la coppia formata dal nome simbolico del server e dalla porta in cui lavora:
server_address=('localhost',serverPort)

# Il metodo BIND(address) assegna ad un'istanza di un socket, un certo indirizzo IP e una certa porta:
serverSocket.bind(server_address)

# COMANDO LISTEN(n):
#
#   --> "Definisce la lunghezza della CODA DI BACKLOG, ovvero il numero
#       di connessioni in entrata che sono state completate dallo stack TCP / IP
#       ma non ancora accettate dall'applicazione".
#   --> "Il numero massimo di connessioni incomplete è pari ad 1 più il valore n".

serverSocket.listen(1)
print ('the web server is up on port:',serverPort)

while True:

    print ('Ready to serve...')

    # Un socket in azione, rimane in attesa di eventuali richieste da parte di client.
    # Il metodo accept() permette di accettare una richiesta di connessione.
    # Restituisce una tupla (conn, address) contente:
    #   --> CONN: "Oggetto socket da utilizzare per la comunicazione con il client".
    #   --> ADDRESS: "L'indirizzo del client".
    connectionSocket, addr = serverSocket.accept()
    print(connectionSocket,addr)

    try:
        # Ricevo il pacchetto
        # Il metodo recv(bufsize) necessita come parametro BUFSIZE, la dimensione del buffer di ricezione.
        # Il metodo restituisce i dati che ha ricevuto.
        message = connectionSocket.recv(1024)

        # Crea una lista di elementi che compongono il messaggio ricevuto (separando le parole in base agli spazi).
        # Se è maggiore di 0, allora stampo "::" + elemento con indice 0 + ":" + elemento con indice 1
        if len(message.split())>0:              
            print (message,'::',message.split()[0],':',message.split()[1]) 
            filename = message.split()[1] 
            print (filename,'||',filename[1:]) 
            f = open(filename[1:],'r+') 
            outputdata = f.read()
            print (outputdata) 
                
            # Invia la riga di intestazione HTTP nel socket con il messaggio OK
            # L'encode � dato dal fatto che in python2 c'erano dei problemi legati alla codifica
            # In python3 si � deciso di codificare in byte, in maniera che tutti i caratteri possano
            # essere trasmessi senza problemi
            connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())
            connectionSocket.send(outputdata.encode())        # Invio il contenuto del file (codificato)
            connectionSocket.send("\r\n".encode())
            connectionSocket.close()
            

    except IOError:
        # Invia messaggio di risposta per file non trovato
        connectionSocket.send(bytes("HTTP/1.1 404 Not Found\r\n\r\n","UTF-8"))
        connectionSocket.send(bytes("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n","UTF-8"))
        connectionSocket.close()


