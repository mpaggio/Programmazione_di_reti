#!/usr/bin/env python3

from socket import *
from threading import *
import tkinter as tk
import time
import sys
import traceback

# Inizializza la variabile per controllare il thread ping
ping_thread_stop = 0
# Inizializza la variabile per controllare il thread di ricezione
receive_thread_stop = 0


# FUNZIONE DI CONNESSIONE AL SERVER
def connect_to_server(server_address):
    global clientSocket
    while True:
        try:
            # Connessione con il Server
            clientSocket.connect(server_address)
            # Invio del nickname al Server
            clientSocket.send(nickname.encode("utf-8"))
            # Terminazione del ciclo della funzione
            break

        # Gestione del rifiuto della connessione a causa della non accensione del Server
        except ConnectionRefusedError:
            # Stampa un messaggio di errore
            print("Server non raggiungibile, si prega di riprovare a connettersi")
            # Esce dal programma
            sys.exit(0)

        # Gestione delle altre eccezioni
        except Exception as ex:
            # Stampa un messaggio di errore
            print(f'Connessione fallita, tentativo di riconnessione in corso: {ex}')
            # Stampa la traccia dello stack
            traceback.print_exc()
            # Aspetta 3 secondi
            time.sleep(3)



# FUNZIONE DI INVIO DEL PING AL SERVER
def ping(client):
    global receive_thread_stop
    while ping_thread_stop == 0:
        try:
            # Aspetta 3 secondi
            time.sleep(3)
            # Controlla che il socket sia ancora aperto
            if clientSocket.fileno() != -1:
                # Invia un messaggio di ping al server
                client.send("[ping]".encode("utf-8"))
                # Stampa di debugging per visualizzare che il ping è stato inviato
                print("[System]: Sent ping")
            else:
                # Stampa di debugging per visualizzare la corretta terminazione del thread di ping
                print("----- Terminato il PING THREAD -------")
                # Terminazione del ciclo
                break
            
        # Gestione generale delle eccezioni
        except Exception as ex:
            # Stampa dell'errore
            print(f'Problema rilevato: {ex}, chiusura in corso ...')
            # Stampa della traccia dello stack
            traceback.print_exc()
            # Terminazione del ciclo
            break


# FUNZIONE CHE GESTISCE L'INVIO DEI MESSAGGI
def send_message(event = None):
    global ping_thread_stop
    global receive_thread_stop
    # Ottiene il messaggio dall'area di input
    messaggio = input_area_message.get()
    # Resetta la variabile di inserimento dei messaggi
    input_area_message.set("")
    # Resetta l'area di input
    input_area.delete(0, tk.END)
    # Controlla che il socket è ancora valido
    if clientSocket.fileno() != -1:
        # Manda il messaggio al Server
        clientSocket.send(messaggio.encode("utf-8"))
    # Controlla che il messaggio sia un messaggio di quit
    if messaggio == "[quit]":
        # Imposta ad 1 il flag di chiusura del thread ping
        ping_thread_stop = 1
        # Imposta ad 1 il flag di chiusura del thread receive
        receive_thread_stop = 1
        # Attende che i thread di ping e di receive non siano più attivi
        while pingThread.is_alive() or receiveThread.is_alive():
            ping_thread_stop = 1
            receive_thread_stop = 1
        # Chiusura del socket
        clientSocket.close()
        # Chiusura della finestra grafica
        window.quit()


# FUNZIONE DI RICEZIONE DEI MESSAGGI
def receive(client):
    global ping_thread_stop
    global receive_thread_stop
    while receive_thread_stop == 0:
        try:
            # Controlla che il socket sia ancora valido
            if client.fileno() != -1:
                # Imposta un timeout di 10 secondi per il Server
                client.settimeout(10)
                # Riceve un messaggio dal Server
                message = client.recv(1024).decode("utf-8")
                # Controlla che sia un messaggio di quit
                if message == "[quit]":
                    # Stampa un messaggio di conferma chiusura per avvenuta chiusura del Server
                    print("Disconnessione in corso a causa della chiusura del Server ...")
                    # Imposta il flag di chiusura del thread di ping a 1
                    ping_thread_stop = 1
                    # Disabilita il bottone per inviare i dati
                    send_button.config(state='disabled')
                    # Attende che il thread di ping non sia più attivo
                    while pingThread.is_alive():
                        ping_thread_stop = 1
                    # Chiusura del socket
                    clientSocket.close()
                    # Chiusura della finestra grafica
                    window.quit()
                    # Interruzione del ciclo
                    break
                # Controlla che il messaggio non sia di ping
                elif "[ping]" not in message:
                    # Inserisce il messaggio nella lista dei messaggi
                    message_list.insert(tk.END, message + '\n')
                    # Stampa il messaggio sul terminale
                    print(message)
                else:
                    # Stampa di debugging per confermare la ricezione del ping del Server
                    print("[System]: Server ping received")
            else:
                # Stampa di debugging per confermare la terminazione del thread receive
                print("------ Terminato il RECEIVE THREAD ------")
                # Terminazione del ciclo
                break

        # Gestione dell'eccezione generata dallo scadere del timeout
        except timeout:
            # Chiusura del socket
            clientSocket.close()
            # Stampa di debugging per la chiusura a causa del timeout
            print('Il Server non è più attivo quindi sei stato disconnesso')
            # Chiusura della finestra grafica
            window.quit()
            # Stampa di debugging per la chiusura del thread receive
            print("------ Terminato il RECEIVE THREAD ------")
            # Interruzione del ciclo
            break

        # Gestione di tutte le altre eccezioni
        except Exception as ex:
            # Stampa di errore con l'eccezione generata
            print(f'Problema rilevato: {ex}, chiusura in corso ...')
            # Stampa della traccia dello stack
            traceback.print_exc()
            # Chisura del socket
            clientSocket.close()
            # Chiusura della finestra grafica
            window.quit()
            # Interruzione del ciclo
            break 


# FUNZIONE DI CHIUSURA DELLA FINESTRA GRAFICA
def on_closing(event = None):
    # Imposta come messaggio scritto il quit
    input_area_message.set("[quit]")
    # Richiama la funzione di invio del messaggio per inviare il quit
    send_message()


# CONFIGURAZIONI GENERALI
# Richiesta del server host
serverHost = input("Inserire server host:")
# Richiesta della server port
serverPort = int(input("Inserire server port:"))
# Richiesta del nickname dell'utente
nickname = input("Inserire nickname:")
# Creazione del Server address
serverAddress = (serverHost, serverPort)
# Creazione del socket del Server
clientSocket = socket(AF_INET, SOCK_STREAM)
# Connessione con il Server
connect_to_server(serverAddress)


# INTERFACCIA GRAFICA
# Creazione della finestra principale
window = tk.Tk()
# Impostazione del titolo
window.title(f"Chat di {nickname}")
# Impostazione del colore di backgroung della finestra
window.configure(background="green")
# Configurazione dell'area di testo in cui verranno visualizzati i messaggi
messages_frame = tk.Frame(window)
# Creazione di una scrollbar per navigare fra i messaggi
scrollbar = tk.Scrollbar(messages_frame)
# Creazione della listbox che conterrà i messaggi
message_list = tk.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
# Integrazione della scrollbar all'interno della finestra
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
# Integrazione della listbox all'interno della finestra
message_list.pack(side=tk.LEFT, fill=tk.BOTH)
# Integrazione della listbox all'interno della finestra
message_list.pack()
# Integrazione dell'area di testo dei messaggi all'interno della finestra
messages_frame.pack()
# Configurazione della variabile che conterrà i messaggi all'interno dell'area di inserimento
input_area_message = tk.StringVar()
# Creazione del messaggio visibile nell'area di inserimento all'inizio
input_area_message.set("Scrivi qui il tuo messaggio.")
# Creazione dell'area di inserimento dei messaggi
input_area = tk.Entry(window, textvariable=input_area_message)
# Lega l'invio del messaggio scritto alla pressione del tasto invio della tastiera
input_area.bind("<Return>", send_message)
# Integrazione dell'area di inserimento all'interno della finestra
input_area.pack()
# Creazione del tasto invio, legato alla funzione di invio del messaggio
send_button = tk.Button(window, text="Invio", command=send_message)
# Integrazione del bottone di invio all'interno della finestra
send_button.pack()

# Configurazione del procotollo di chiusura della finestra grafica della chat (quando viene premuto il pulsante di chiusura)
# Personalizza l'azione di chiusura della finestra, facendo eseguire on_closing al posto dell'azione predefinita
window.protocol("WM_DELETE_WINDOW", on_closing)

# CONFIGURAZIONE DEI THREAD
# Creazione del thread che si occupa di mandare il ping al Server
pingThread = Thread(target=ping, args=(clientSocket,))
# Avvio del thread di ping
pingThread.start()
# Creazione del thread che si occupa di ricevere i messaggi della Chat
receiveThread = Thread(target=receive, args=(clientSocket,))
# Avvio del thread di ricezione
receiveThread.start()

# Avvio dell'interfaccia grafica
window.mainloop()

# Terminazione del programma
sys.exit(0)
