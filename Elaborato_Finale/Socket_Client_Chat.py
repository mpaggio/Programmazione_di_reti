#!/usr/bin/env python3

from socket import *
from threading import *
import tkinter as tk
import time
import sys
import traceback

# Variabile di stop pingThread
ping_thread_stop = 0
# Variabile di stop receiveThread
receive_thread_stop = 0


# ---- FUNZIONE CONNECT TO SERVER ----
def connect_to_server(server_address):
     global clientSocket
     while True:
        try:
           # Connessione con il Server
           clientSocket.connect(server_address)
           # Terminazione del ciclo della funzione
           break

        # Gestione del rifiuto della connessione a causa della non accensione del Server
        except ConnectionRefusedError:
            print("Server non raggiungibile, si prega di riprovare a connettersi")
            sys.exit(0)

        # Gestione delle eccezioni
        except Exception as ex:
            # Stampa di debugging per il nuovo tentativo di riconnessione a causa di un errore
            print(f'Connessione fallita, tentativo di riconnessione in corso: {ex}')
            # Stampa del traceback per vedere da dove viene l'eccezione
            traceback.print_exc()
            # Aspetta 3 sec prima di farlo
            time.sleep(3)
        


# ---- FUNZIONE CHE INVIA IL PING AL SERVER ----
# Funzione che ogni 3 secondi manda un segnale (messaggio con scritto "[ping]") al Server:
def ping(client):
    global receive_thread_stop
    while ping_thread_stop == 0:
        try:
            # Aspetta 3 secondi prima di inviare il ping
            time.sleep(3)
            # Controlla che la socket sia ancora attiva
            if clientSocket.fileno() != -1:
                # Invia il messaggio ping al server
                client.send("[ping]".encode("utf-8"))
                # Stampa di debugging per visualizzare che il ping è stato inviato
                print("[System]: Sent ping")
            else:
                # Stampa di debugging per visualizzare la corretta chiusura del thread ping
                print("----- Terminato il PING THREAD -------")
                # Terminazione del ciclo while
                break
            
        # Cattura di eventuali eccezioni
        except Exception as ex:
            # Stampa dell'eccezione generata
            print(f'Problema rilevato: {ex}, chiusura in corso ...')
            # Stampa del traceback per vedere da dove viene l'eccezione
            traceback.print_exc()
            # Se c'è un errore (la connessione è interrota) allora viene terminato il ciclo
            break
     

# ---- FUNZIONE CHE GESTISCE L'INVIO DEI MESSAGGI ----
def send_message(event = None):
        global ping_thread_stop
        global receive_thread_stop
        # Prende il messaggio dalla casella di input in cui viene inserito
        messaggio = input_area_message.get()
        # Libera la variabile del messaggio della casella di inserimento dei messaggi
        input_area_message.set("")
        # Libera la casella di inserimento dei messaggi
        input_area.delete(0, tk.END)
        # Controlla che la socket sia ancora attiva
        if clientSocket.fileno() != -1:
            # Invia il messaggio al Server
            clientSocket.send(messaggio.encode("utf-8"))
        # Controlla se il messaggio inviato è un quit
        if messaggio == "[quit]":
            ping_thread_stop = 1
            receive_thread_stop = 1
            while pingThread.is_alive() or receiveThread.is_alive():
                ping_thread_stop = 1
                receive_thread_stop = 1
            # Chiude la socket
            clientSocket.close()
            # Chiude la finestra grafica della chat
            window.quit()


# ---- FUNZIONE CHE GESTISCE LA RICEZIONE DEI MESSAGGI ----
def receive(client):
    global ping_thread_stop
    global receive_thread_stop
    while receive_thread_stop == 0:
            try:
                # Controlla che la socket sia ancora attiva
                if client.fileno() != -1:
                    # Imposta un timeout di 10 secondi al Server 
                    # Se non riceve alcun ping in questo lasso di tempo lancia una timeout exception
                    client.settimeout(10)
                    # Salva il messaggio ricevuto dal Server
                    message = client.recv(1024).decode("utf-8")
                    # Controlla che non gli sia arrivato un messaggio di quit
                    if message == "[quit]":
                        # In caso di messaggio di quit dal Server, chiude la connessione
                        # Stampa la causa della disconnessione
                        print("Disconnessione in corso a causa della chiusura del Server ...")
                        ping_thread_stop = 1
                        send_button.config(state='disabled')
                        while pingThread.is_alive():
                            ping_thread_stop = 1
                        # Chiude la socket
                        clientSocket.close()
                        # Chiude la finestra grafica della chat
                        window.quit()
                        break
                    # Controlla che il messaggio non sia il ping
                    elif "[ping]" not in message:
                        # Se non è un ping, allora inserisce il messaggio nell'elenco dei messaggi della chat
                        message_list.insert(tk.END, message + '\n')
                        # Stampa di debugging del messaggio ricevuto
                        print(message)
                    else:
                        # Stampa di debugging per visualizzare che il Client ha ricevuto il ping dal Server
                        print("[System]: Server ping received")
                else:
                    # Stampa di debugging per visualizzare la corretta terminazione del thread di ricezione
                    print("------ Terminato il RECEIVE THREAD ------")
                    # Terminazione del ciclo della funzione
                    break

            # Controllo dell'eccezione generata dal timeout (dopo 10 sec in cui non riceve più niente)
            except timeout:
                # Chiude la socket
                clientSocket.close()
                # Stampa di debugging della chiusura a causa del timeout
                print('Il Server non è più attivo quindi sei stato disconnesso')
                # Chiusura della finestra grafica della chat
                window.quit()
                # Stampa di debugging per visualizzare la corretta terminazione del thread di ricezione
                print("------ Terminato il RECEIVE THREAD ------")
                # Terminazione del ciclo della funzione
                break

            # Gestione di un'eccezione generica al di fuori di quella legata al timeout
            except Exception as ex:
                # Stampa dell'eccezione generata
                print(f'Problema rilevato: {ex}, chiusura in corso ...')
                # Stampa del traceback per vedere da dove viene l'eccezione
                traceback.print_exc()
                # Chiusura della socket
                clientSocket.close()
                # Chiusura della finestra grafica della chat
                window.quit()
                # Terminazione del ciclo della funzione
                break 


# ---- FUNZIONE DI CHIUSURA DELLA FINESTRA GRAFICA ----
# Funzione che viene invocata quando viene chiusa la finestra della chat:
def on_closing(event = None):
      # Imposta come messaggio scritto il quit
      input_area_message.set("[quit]")
      # Richiama la funzione di invio del messaggio (che invierà il quit)
      send_message()


# ---- IMPOSTAZIONI GENERALI ----
# Richiesta del Server host
serverHost = input("Inserire server host:")
# Richiesta della Server port
serverPort = int(input("Inserire server port:"))
# Creazione del Server address
serverAddress = (serverHost, serverPort)
# Creazione della socket
clientSocket = socket(AF_INET, SOCK_STREAM)
# Connessione con il Server
connect_to_server(serverAddress)


# ---- INTERFACCIA GRAFICA ----
# Creazione della finestra principale dell'interfaccia grafica
window = tk.Tk()
# Impostazione del titolo della finestra
window.title("Chat_Elaborato_Programmazione_di_Reti")
# Impostazione del colore di background della finestra
window.configure(background="green")
# Configurazione dell'area di testo in cui verranno visualizzati i messaggi
messages_frame = tk.Frame(window)
# Creazione di una scrollbar per navigare fra i messaggi precedenti
scrollbar = tk.Scrollbar(messages_frame)
# Creazione della list box che conterrà i messaggi
message_list = tk.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
# Integrazione all'interno della finestra della scrollbar
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
# Integrazione all'interno della finestra della list box dei messaggi
message_list.pack(side=tk.LEFT, fill=tk.BOTH)
message_list.pack()
# Integrazione all'interno della finestra del frame per i messaggi
messages_frame.pack()
# Configurazione della variabile che conterrà i messaggi all'interno dell'area di inserimento
input_area_message = tk.StringVar()
# Creazione del messaggio visibile fin dall'inizio nell'area di inserimento dei messaggi
input_area_message.set("Scrivi qui il tuo messaggio.")
# Configurazione dell'area di inserimento dei messaggi (composta dalla variabile creata in precendenza)
input_area = tk.Entry(window, textvariable=input_area_message)
# Lega l'invio del messaggio scritto all'invio digitato da tastiera
input_area.bind("<Return>", send_message)
# Integrazione dell'area di inserimento all'interno della finestra
input_area.pack()
# Creazione del tasto invio, legato alla funzione di invio del messaggio
send_button = tk.Button(window, text="Invio", command=send_message)
# Integrazione del bottone di invio all'interno della finestra
send_button.pack()

# Configurazione del protocollo di chiusura della finestra grafica della chat (quando viene premuto il pulsante di chiusura)
# Personalizza l'azione di chiusura della finestra facendo eseguire on_closing al posto dell'azione predefinita
window.protocol("WM_DELETE_WINDOW", on_closing)


# ---- CONFIGURAZIONE DEI THREAD ----
# Creazione del Thread che si occupa di mandare il ping al Server
pingThread = Thread(target=ping, args=(clientSocket,))
# Avvio del thread
pingThread.start()
# Creazione del Thread che si occupa di ricevere i messaggi del Client
receiveThread = Thread(target=receive, args=(clientSocket,))
# Avvio del thread
receiveThread.start()



# ---- AVVIO DELL'INTERFACCIA GRAFICA ----
# Avvia l'esecuzione della finestra grafica della Chat
window.mainloop()


# ---- TERMINAZIONE DEL PROGRAMMA ----
# Terminazione del programma
sys.exit(0)