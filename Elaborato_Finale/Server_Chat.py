#!/usr/bin/env python3

from socket import *
from threading import *
import sys
import time
import traceback

# Inizializza la lista dei flag di stop dei thread
ping_thread_stop = []
# Inizializza la lista dei thread attivati
threads = []

# FUNZIONE DI PING
def ping(client, indice):
    global ping_thread_stop
    while ping_thread_stop[indice] == 0:
        try:
            # Aspetta 3 secondi
            time.sleep(3)
            # Invia il messaggio di ping al Client
            client.send("[ping]".encode("utf-8"))
            # Stampa di debugging per visualizzare il corretto invio del ping
            print("[System]: Sent ping")
            
        # Gestione della ricezione in un socket che è già stato chiuso
        except ConnectionResetError:
            # Stampa di errore
            print("La connessione è stata interrotta in modo inaspettato, terminazione del thread ping in corso ...")
            # Terminazione del ciclo
            break

        # Gestione del tentativo di invio di un messaggio su un socket chiuso
        except ConnectionAbortedError:
            # Stampa di errore
            print("Tentativo di invio del ping su socket precedentemente chiusa, terminazione del thread ping in corso ... ")
            # Terminazione del ciclo
            break

        # Gestione generale delle eccezioni rimanenti
        except Exception as ex:
            # Stampa dell'eccezione
            print(f'Problema rilevato: {ex}, chiusura in corso ...')
            # Stampa della traccia dello stack
            traceback.print_exc()
            # Terminazione del ciclo
            break


# FUNZIONE DI MESSAGGIO BROADCAST
def broadcast(message, clients):
    # Scorre la lista di tutti i Client connessi alla Chat
    for client in clients:
        # Manda il messaggio ad ogni Client connesso
        client.send(message)


# FUNZIONE DI DISCONNESSIONE DEL CLIENT
def delete_client(client):
    try:
        # Invio del messaggio di quit al Client (per dirgli di abbandonare la chat)
        client.send("[quit]".encode("utf-8"))
        # Recupera l'indice del Client da disconnettere
        index = clients.index(client)
        # Rimuove il Client dalla lista di quelli connessi
        clients.remove(client)
        # Recupera il nickname del Client da disconnettere
        nickname = nicknames[index]
        # Rimuove il nickname da quelli dei Client connessi
        nicknames.remove(nickname)
        # Stampa di debugging per visualizzare la corretta rimozione del Client
        print(f"Rimosso {nickname} dalla chat")
        # Messaggio a tutti i Client ancora connessi, che il Client specifico è stato disconnesso
        broadcast(f'{nickname} ha lasciato la chat!'.encode("utf-8"), clients)
    
    # Gestione del tentativo di invio di un messaggio su un socket chiuso
    except ConnectionResetError:
        # Stampa di avviso
        print("Azione non andata a buon fine perchè la socket è gia stata chiusa")


# FUNZIONE DI GESTIONE DELLA CONNESSIONE COL CLIENT
def handle(client, pingThread, indice, nick):
    global ping_thread_stop
    # Attiva il thread di ping
    pingThread.start()
    while True:
        try:
            # Imposta un timeout di 10 secondi per il Client
            client.settimeout(10)
            # Riceve un messaggio dal Client
            message = client.recv(1024).decode("utf-8")
            # Controlla che il messaggio sia vuoto
            if not message:
                # Disconnette il client
                delete_client(client)
                # Interruzione del ciclo
                break
            # Controlla che non sia un messaggio di ping
            if "[ping]" not in message:
                # Controlla che non sia un messaggio di quit
                if message != "[quit]":
                    # Completa il messaggio da stampare mettendo il nickname all'inizio
                    total_message = nick + ": " + message
                    # Invia il messaggio completo a tutti i Client connessi
                    broadcast(total_message.encode("utf-8"), clients)
                else:
                    # Imposta il flag di chiusura del thread specifico a 1
                    ping_thread_stop[indice] = 1
                    # Attende che il thread di ping non sia più attivo
                    while pingThread.is_alive():
                        ping_thread_stop[indice] = 1
                    # Rimuove il client dalla lista di quelli connessi
                    clients.remove(client)
                    # Rimuove il nickname dalla lista dei Client connessi
                    nicknames.remove(nick)
                    # Stampa di debugging per accertarsi della corretta rimozione del Client
                    print(f"Rimosso {nick} dalla chat")
                    # Messaggio a tutti i Client connessi della disconnessione di quest'ultimo
                    broadcast(f'{nick} ha lasciato la chat!'.encode("utf-8"), clients)
                    # Stampa dei nickname dei Client ancora connessi
                    print("Nickname dei Client rimanenti nella chat:\n ")
                    # Scorre la lista di tutti i nickname dei Client connessi
                    for nick in nicknames:
                        # Stampa il nickname
                        print(nick) 
                    # Interruzione del ciclo
                    break
            else:
                # Stampa di debugging per confermare la ricezione del ping del Client
                print("[System]: Client ping arrived")

        # Gestione dello scadere del timeout
        except TimeoutError:
            # Stampa di debugging per visualizzare la disconnessione del Client
            print(f'{nick} non è più connesso.')
            # Disconnessione del client
            delete_client(client)
            # Interruzione del ciclo
            break

        # Gestione del tentativo di ricezione su socket chiuso
        except ConnectionResetError:
            # Stampa di errore
            print("Tentativo di ricezione su socket precedentemente chiusa, terminazione dell'handle thread in corso ...")
            # Interruzione del ciclo
            break
            
        # Gestione generale delle eccezioni rimanenti
        except Exception as ex:
            # Stampa dell'eccezione
            print(f"Problema rilevato: {ex}, chiusura dell'handel thread in corso ...")
            # Stampa della traccia dello stack
            traceback.print_exc()
            # Interruzione del ciclo
            break
            

# FUNZIONE DI GESTIONE DELL'ACCETTAZIONE DELLE CONNESSIONI IN ENTRATA            
def receive(server, clients, nicknames):
    while True:
        try:
            # Accetta una connessione dal Client
            client, clientAddress = serverSocket.accept()
            # Stampa di debugging per visualizzare la connessione con il Client
            print(f'Connesso con {str(clientAddress)}')
            # Ricezione del nickname del Client
            nickname = client.recv(1024).decode("utf-8")
            # Aggiunge il nickname alla lista corrispondente
            nicknames.append(nickname)
            # Aggiunge il Client alla lista corrispondente
            clients.append(client)
            # Stampa del nickname ricevuto
            print(f"Nickname: {nickname}")
            # Invio di un messaggio di benvenuto al Client
            client.send(f'Benvenuto {nickname}! \nSe vuoi lasciare la chat scrivi \"[quit]\".'.encode("utf-8"))
            # Invio di un messaggio di avviso ai Client connessi alla chat
            broadcast(f'{nickname} si è unito alla chat!'.encode("utf-8"), clients)
            # Aggiunge un flag, per il thread ping che verrà creato per il Client, con valore 0
            ping_thread_stop.append(0)
            # Ricava l'indice della posizione del flag nel vettore corrispondente
            indice_ping = len(ping_thread_stop) - 1
            # Creazione del thread di ping
            pingThread = Thread(target=ping, args=(client,indice_ping,))
            # Creazione del thread di gestione delle connessioni
            handleThread = Thread(target=handle, args=(client, pingThread, indice_ping, nickname,))
            # Salvataggio del thread di gestione delle connessioni nella lista corrispondente
            threads.append(handleThread)
            # Attivazione del thread di gestione delle connessioni
            handleThread.start()
           
        # Gestione dei tentativi di accpet su socket chiuso
        except OSError:
            # Stampa di errore
            print("Tentativo di accept su Socket chiusa, chiusura del thread receive in corso ...")
            # Interruzione del ciclo
            break

        # Gestione generica delle eccezioni rimanenti
        except Exception as ex: 
            # Stampa dell'eccezione
            print(f'Problema rilevato: {ex}, chiusura del thread receive in corso ...')
            # Stampa della traccia dello stack
            traceback.print_exc()
            # Interruzione del ciclo
            break


# CONFIGURAZIONI INIZIALI
# Richiesta del Server host
serverHost = input("Inserisci server host:")
# Richiesta della Server port
serverPort = int(input("Inserisci server port:"))
# Creazione del Server address
serverAddress = (serverHost, serverPort)
# Creazione del socket del Server
serverSocket = socket(AF_INET, SOCK_STREAM)
# Legame del socket del Server con il suo address
serverSocket.bind(serverAddress)
# Inizio dell'ascolto del Server, in attesa di connessioni
# Fino a 5 Client possono attendere in coda, mentre il Server gestisce una connessione
serverSocket.listen(5)
# Inizializzazione della lista dei Client
clients = []
# Inizializzazione della lista dei nickname
nicknames = []


# AVVIO DEL PROGRAMMA
if __name__ == "__main__":   
    # Creazione del thread di ricezione delle connessioni in entrata 
    receiveThread = Thread(target=receive, args=(serverSocket, clients, nicknames))
    # Avvvio del thread di ricezione
    receiveThread.start()
    # Stampa di debugging 
    print("In attesa di connessioni ...")

    while True:
        try: 
            # Aspetta 5 secondi
            time.sleep(5)
            # Stampa di debugging per visualizzare il funzionamento del Server
            print("Server in esecuzione")

        # Gestione dell'eccezione legata alla chiusura del programma Server mediante CTRL+C
        except KeyboardInterrupt:
            # Stampa di debugging di avvenuta digitazione di CTRL+C
            print("Avviata procedura di chiusura del Server ... (CTRL+C)")
            # Scorre una copia della lista dei Client connessi 
            # (per evitare di utilizzare la lista vera e propria che viene nel mentre modificata)
            for client in list(clients):
                # Disconnessione dei Client connessi
                delete_client(client)
            # Stampa di debugging per la disconnessione di tutti i Client
            print("Tutti i client sono stati disconnessi")
            # Chiusura del socket
            serverSocket.close()
            # Azzera la lista dei Client
            clients = []
            # Azzera la lista dei nickname
            nicknames = []
            # Stampa di debugging per la disconnessione del Server
            print("Server disconnesso")

            # Scorre la lista dei thread di gestione delle connessioni
            for thread in threads:
                # Attende la loro terminazione
                thread.join()

            # Terminazione del programma Server
            sys.exit(0)
