#!/usr/bin/env python3

from socket import *
from threading import *
import sys
import time
import traceback

# Vettore di variabili di stop pingThread
ping_thread_stop = []


# ---- FUNZIONE PING ----
# Funzione che ogni 3 secondi manda un messaggio ping al Client:
def ping(client, indice):
    global ping_thread_stop
    while ping_thread_stop[indice] == 0:
        try:
            # Aspetta per 3 secondi
            time.sleep(3)
            # Controlla se il socket è valido e aperto (oppure no) tramite il suo file descriptor
            if client.fileno() != -1:
                # Invia il messaggio ping al server
                client.send("[ping]".encode("utf-8"))
                # Stampa di debugging per visualizzare l'invio del ping
                print("[System]: Sent ping")
            else:
                # Terminazione del ciclo della funzione
                break
            
        # Gestione della ricezione in una socket che è già stata chiusa
        except ConnectionResetError:
            # Stampa di debug
            print("Tentativo di ricezione su socket precedentemente chiusa, terminazione in corso ...")
            # Terminazione del ciclo della funzione
            break

        # Gestione delle eccezioni (generale)
        except Exception as ex:
            # Stampa dell'eccezione generata
            print(f'Problema rilevato: {ex}, chiusura in corso ...')
            # Stampa del traceback per vedere da dove viene l'eccezione
            traceback.print_exc()
            # Se c'è un errore (la connessione è interrota) allora si interrompe
            break


# ---- FUNZIONE BROADCAST ----
# Funzione che invia un messaggio in broadcast a tutti i Client:
def broadcast(message, clients):
    # Scorre tutti i Client connessi
    for client in clients:
        # Invia il messaggio ad ogni Client connesso
        client.send(message)


# ---- FUNZIONE DI UTILITY ----
# Funzione che viene chiamata per eliminare un client dal Server
def delete_client(client):
    # Scrive al Client che ha abbandonato la chat
    client.send("[quit]".encode("utf-8"))
    # Recupera l'indice del client da eliminare
    index = clients.index(client)
    # Rimuove il client dalla lista dei Client connessi
    clients.remove(client)
    # Ricava il nome del Client da eliminare
    nickname = nicknames[index]
    # Rimuove il nickname del Client dalla lista salvata
    nicknames.remove(nickname)
    # Stampa di debugging per visualizzare il Client eliminato dalla chat
    print(f"Rimosso {nickname} dalla chat")
    # Scrive un messaggio a tutti i Client rimanenti, che il Client ha abbandonato la chat
    broadcast(f'{nickname} ha lasciato la chat!'.encode("utf-8"), clients)
    # Stampa che indica che si stanno per visualizzare i nickname di tutti i Client rimanenti
    print("Nickname dei Client rimanenti nella chat:\n ")
    # Stampa tutti i nickname
    for nick in nicknames:
        print(nick)


# ---- FUNZIONE HANDLE ----
# Funzione che gestisce la connessione di un singolo Client (il cui socket viene passato come argomento):
def handle(client, pingThread, indice):
    global ping_thread_stop
    # Avvio del trhead ping
    pingThread.start()
    while True:
        # Salva il nome del client che gli viene passato come primo messaggio
        nickname = client.recv(1024).decode("utf-8")
        # Controlla che il messaggio non sia vuoto (ovvero che il Client si è disconnesso inaspettatamente)
        if not nickname:
            # Disconnetto il client
            delete_client(client)
            # Termino il ciclo della funzione
            break
        # Controlla che il messaggio ricevuto non sia ping 
        if "[ping]" not in nickname:
            # Salva il nickname del Client nella lista apposita
            nicknames.append(nickname)
            # Salva le informazioni del Client nella lista apposita
            clients.append(client)
            # Messaggio di debugging che tiene traccia della registrazione del nome del Client
            print(f'Nickname: {nickname}')
            # Breve messaggio di benvenuto e indicazioni sull'uscita dalla chat
            client.send(f'Benvenuto {nickname}! \nSe vuoi lasciare la chat scrivi \"[quit]\".'.encode("utf-8"))
            # Messaggio brodcast con cui tutti i Client connessi alla chat vengono avvisati che l'utente è entrato
            broadcast(f'{nickname} si è unito alla chat!'.encode("utf-8"), clients)
            # Terminazione del ciclo della funzione
            break

    # Si mette in ascolto del thread del singolo Client e gestisce l'invio dei messaggi e l'uscita dalla chat
    while True:
        try:
            # Imposta un timeout di 10 secondi al Client
            client.settimeout(10)
            # Attende di ricevere il messaggio
            message = client.recv(1024).decode("utf-8")
            # Controlla che il Client non si sia disconnesso inaspettatamente
            if not message:
                # Disconnetto il client
                delete_client(client)
                # Termina il ciclo della funzione
                break
            # Controlla che non sia il messaggio di ping
            if "[ping]" not in message:
                # Verifico che il messaggio non sia quello di uscita
                if message != "[quit]":
                    # Imposta il messaggio totale come nickname: messaggio
                    total_message = nickname + ": " + message
                    # Invio in broadcast del messaggio
                    broadcast(total_message.encode("utf-8"), clients)
                else:
                    # Imposto la variabile di stop del pingThread per evitare che continui
                    ping_thread_stop[indice] = 1
                    while pingThread.is_alive():
                        ping_thread_stop[indice] = 1
                    # Rimuove il client dalla lista dei Client connessi
                    clients.remove(client)
                    # Ricava il nome del Client da eliminare
                    nickname = nicknames[indice]
                    # Rimuove il nickname del Client dalla lista salvata
                    nicknames.remove(nickname)
                    # Stampa di debugging per visualizzare il Client eliminato dalla chat
                    print(f"Rimosso {nickname} dalla chat")
                    # Scrive un messaggio a tutti i Client rimanenti, che il Client ha abbandonato la chat
                    broadcast(f'{nickname} ha lasciato la chat!'.encode("utf-8"), clients)
                    # Stampa che indica che si stanno per visualizzare i nickname di tutti i Client rimanenti
                    print("Nickname dei Client rimanenti nella chat:\n ")
                    # Stampa tutti i nickname
                    for nick in nicknames:
                        print(nick) 
                    # Terminazione del ciclo della funzione
                    break
            else:
                # Stampa di debugging per segnalare l'arrivo del ping del Client
                print("[System]: Client ping arrived")

        # Gestione dell'eccezione legata al timeout del Client
        except timeout:
            # Stampa di debugging per dire che il Client si è disconnesso
            print(f'{nickname} non è più connesso.')
            # Disconnetto il client
            delete_client(client)
            # Terminazione del ciclo della funzione
            break

        # Gestione della ricezione in una socket che è già stata chiusa
        except ConnectionResetError:
            # Stampa di debug
            print("Tentativo di ricezione su socket precedentemente chiusa, terminazione in corso ...")
            # Terminazione del ciclo della funzione
            break
            

        # Gestione delle eccezioni al di fuori di quella legata al timeout
        except Exception as ex:
            # Stampa dell'eccezione generata
            print(f'Problema rilevato: {ex}, chiusura in corso ...')
            # Stampa del traceback per vedere da dove viene l'eccezione
            traceback.print_exc()
            # Terminazione del ciclo della funzione
            break
            
            
# ---- FUNZIONE DI ACCETTAZIONE DELLE CONNESSIONI ----
# Funzione che accetta le connessioni dei client in entrata:
def receive(server, clients, nicknames):
    while True:
        try:
            # Accettazione della richiesta di connessione
            client, clientAddress = serverSocket.accept()
            # Stampa di debugging per visualizzare la connessione riuscita con il Client
            print(f'Connesso con {str(clientAddress)}')
            # Al client appena connesso specifichiamo una prima indicazione su cosa fare (scrivere il nickname e dare invio)
            client.send('Digita il tuo nickname e premi invio'.encode("utf-8"))
            # Imposto la variabile del handleTrhead
            ping_thread_stop.append(0)
            indice_ping = len(ping_thread_stop) - 1
            # Diamo inizio all'attività di invio del ping al Client tramite un Thread
            pingThread = Thread(target=ping, args=(client,indice_ping,))
            # Diamo inizio all'attività di gestione dei Client mediante un Thread di gestione
            handleThread = Thread(target=handle, args=(client, pingThread, indice_ping,))
            # Avvio del thread di gestione
            handleThread.start()
           
        # Gestione del tentativo di accept quando la Socket è chiusa:
        except OSError:
            print("Tentativo di accept su Socket chiusa, chiusura in corso ...")
            break

        # Gestione delle eccezioni
        except Exception as ex: 
            # Stampa dell'eccezione generata
            print(f'Problema rilevato: {ex}, chiusura in corso ...')
            # Stampa del traceback per vedere da dove viene l'eccezione
            traceback.print_exc()
            # Terminazione del ciclo della funzione
            break


# ---- IMPOSTAZIONI GENERALI ----
# Richiesta del Server host
serverHost = input("Inserisci server host:")
# Richiesta della Server port
serverPort = int(input("Inserisci server port:"))
# Creazione dell'indirizzo del Server
serverAddress = (serverHost, serverPort)
# Creazione della socket del Server
serverSocket = socket(AF_INET, SOCK_STREAM)
# Legame della socket con l'indirizzo (Server)
serverSocket.bind(serverAddress)
# Inizio dell'ascolto del Server, in attesa di altre connessioni
# (fino a 5 Client possono attendere in coda mentre il Server gestisce una connessione)
serverSocket.listen(5)
# Creazione delle liste per la gestione dei client in ingresso e dei loro nickname:
clients = []
nicknames = []


if __name__ == "__main__":
    
    # Creazione del thread che si occupa della receive
    receiveThread = Thread(target=receive, args=(serverSocket, clients, nicknames))
    # Avvio del thread
    receiveThread.start()
    # Stampa di debugging per visualizzare il corretto avvio del Server
    print("In attesa di connessioni ...")

    while True:
        try: 
            # Aspetta 5 secondi prima di stampare che il Server sta funzionando
            time.sleep(5)
            # Stampa di debugging per visualizzare che il Server sta ancora andando
            print("Server in esecuzione")

        # Gestione dell'eccezione legata alla chiusura del Server mediante digitazione di CTRL+C
        except KeyboardInterrupt:
            # Stampa di debugging per visualizzare la cattura dell'interrupt da tastiera
            print("Avviata procedura di chiusura del Server ... (CTRL+C)")
            # Scorre tutti i client connessi al Server
            for client in clients:
                # Stampa di debugging per visualizzare che si sta disconnettendo un Client
                print("Disconnettendo: ", client)
                # Invio del messaggio di quit per dire al Client di chiudere la connessione
                client.send("[quit]".encode("utf-8"))
            # Stampa di debugging per visualizzare che tutti i client sono stati disconnessi
            print("Tutti i client sono stati disconnessi")
            # Pulizia delle liste contenenti i Client connessi e dei relativi nickname
            clients = []
            nicknames = []
            # Chiusura della Socket del server
            serverSocket.close()
            # Stampa di appoggio per visualizzare che il Server ha chiuso la Socket
            print("Server disconnesso")

            # ---- TERMINAZIONE DEL PROGRAMMA ----
            sys.exit(0)