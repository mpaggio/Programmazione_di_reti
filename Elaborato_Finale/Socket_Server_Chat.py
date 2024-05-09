#!/usr/bin/env python3

from socket import *
from threading import *

# Funzione che invia un messaggio in broadcast a tutti i Client:
def broadcast(message, clients):
    for client in clients:
        client.send(message)

# Funzione che gestisce la connessione di un singolo Client (il cui socket viene passato come argomento):
def handle(client):
    # Salva il nome del client che gli viene passato come primo messaggio
    nickname = client.recv(1024).decode("utf-8")
    # Salviamo le informazioni del Client nelle liste create in precedenza 
    nicknames.append(nickname)
    clients.append(client)
    # Messaggio interno al Server che tiene traccia della registrazione del nome del Client
    print(f'Nickname: {nickname}')
    # Breve messaggio di benvenuto e indicazioni sull'uscita dalla chat
    client.send(f'Benvenuto {nickname}! Se vuoi lasciare la chat, scrivi \"quit\" per uscire.'.encode("utf-8"))
    # Messaggio brodcast con cui tutti i Client connessi alla chat vengono avvisati che l'utente è entrato
    broadcast(f'{nickname} si è unito alla chat!'.encode("utf-8"), clients)

    # Si mette in ascolto del thread del singolo Client e gestisce l'invio dei messaggi e l'uscita dalla chat
    while True:
        try:
            message = client.recv(1024)
            # Verifico che il messaggio non sia quello di uscita
            if message != "quit".encode("utf-8"):
                message = message.decode("utf-8")
                message = nickname + ": " + message
                broadcast(message.encode("utf-8"), clients)
            else:
                # Scrive al Client che ha abbandonato la chat
                client.send("quit".encode("utf-8"))
                # Chiude la connessione con il Client
                client.close()
                # Aggiorna le liste dei Client e dei rispettivi nickname
                index = clients.index(client)
                clients.remove(client)
                nickname = nicknames[index]
                nicknames.remove(nickname)
                # Scrive un messaggio a tutti i Client rimanenti, che il Client ha abbandonato la chat
                broadcast(f'{nickname} ha lasciato la chat!'.encode("utf-8"), clients)
                break

        except Exception as exception:
            break
            
            

# Funzione che accetta le connessioni dei client in entrata:
def receive(server, clients, nicknames):
    while True:
        client, clientAddress = serverSocket.accept()
        print(f'Connesso con {str(clientAddress)}')
        # Al client appena connesso specifichiamo una prima indicazione su cosa fare (scrivere il nickname e dare invio)
        client.send('Digita il tuo nickname e premi invio'.encode("utf-8"))
        # Diamo inizio all'attività di gestione dei Client mediante un Thread (uno per ogni Client)
        thread = Thread(target=handle, args=(client,))
        thread.start()

# Creazione dell'indirizzo del Server:
serverHost = input("Inserisci server host:")
serverPort = int(input("Inserisci server port:"))
serverAddress = (serverHost, serverPort)

# Creazione della Socket Server:
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(serverAddress)
serverSocket.listen(5)

# Creazione delle liste per la gestione dei client in ingresso e dei loro nickname:
clients = []
nicknames = []

if __name__ == "__main__":
    acceptThread = Thread(target=receive, args=(serverSocket, clients, nicknames))
    acceptThread.start()
    acceptThread.join()
    serverSocket.close()