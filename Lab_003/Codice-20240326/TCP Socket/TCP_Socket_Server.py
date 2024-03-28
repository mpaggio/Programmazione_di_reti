# Corso di Programmazione di Reti - Laboratorio - UniversitÃ  di Bologna
# Socket_Programming_Assignment - WebServer - F. Callegati - G.Pau - A. Piroddi

import sys
from socket import * 
serverPort=8080
serverSocket = socket(AF_INET, SOCK_STREAM)
server_address=('localhost',serverPort)
serverSocket.bind(server_address)

#listen(1) Definisce la lunghezza della coda di backlog, ovvero il numero
#di connessioni in entrata che sono state completate dallo stack TCP / IP
#ma non ancora accettate dall'applicazione.
serverSocket.listen(1)
print ('the web server is up on port:',serverPort)

while True:

    print ('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()
    print(connectionSocket,addr)

    try:
        # Ricevo il pacchetto
        message = connectionSocket.recv(1024)                              
        # Crea una lista di elementi che compongono il messaggio ricevuto
        # Se è maggiore di 0, allora stampo "::" + elemento con indice 0 + ":" + elemento con indice 1
        if len(message.split())>0:              
            print (message,'::',message.split()[0],':',message.split()[1]) 
            filename = message.split()[1] 
            print (filename,'||',filename[1:]) 
            f = open(filename[1:],'r+') 
            outputdata = f.read()
            print (outputdata) 
                
            # Invia la riga di intestazione HTTP nel socket con il messaggio OK
            # L'encode è dato dal fatto che in python2 c'erano dei problemi legati alla codifica
            # In python3 si è deciso di codificare in byte, in maniera che tutti i caratteri possano
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


