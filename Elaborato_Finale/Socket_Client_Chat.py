#!/usr/bin/env python3

from socket import *
from threading import *
import tkinter as tk
import time

# Funzione che manda costantemente (ogni 3 secondi) un segnale al server:
def ping(client):
    while True:
        try:
            # Aspetta per 3 secondi
            time.sleep(3)
            # Invia il messaggio ping al server
            client.send("ping".encode("utf-8"))
            print(f"Sent ping to {client}")
        except:
             # Se c'è un errore (la connessione è interrota) allora si interrompe
             break
     

# Funzione che gestisce l'invio dei messaggi:
def send_message(event = None):
        # Creiamo il messaggio prendendolo dalla casella in cui viene inserito (attaccandoci il nickname del Client)
        messaggio = input_area_message.get()
        input_area_message.set("")
        # Libera la casella di inserimento del messaggio
        input_area.delete(0, tk.END)
        # Invia il messaggio sul socket
        clientSocket.send(messaggio.encode("utf-8"))
        if messaggio == "quit":
            clientSocket.close()
            window.quit()

# Funzione che gestisce la ricezione dei messaggi:
def receive(client):
    while True:
            try:
                message = client.recv(1024).decode("utf-8")
                message_list.insert(tk.END, message + '\n')
                print(message)
                if message == "":
                    print("Il server ha terminato la connessione a causa di un errore")
                    clientSocket.close()
                    window.quit()
                    break

            # Controllo degli errori
            except OSError:
                print("Il server ha terminato la connessione a causa di un errore")
                clientSocket.close()
                window.quit()
                break 

# Funzione che viene invocata quando viene chiusa la finestra della chat:
def on_closing(event = None):
      input_area_message.set("quit")
      send_message()


# Connessione al server:
serverHost = input("Inserire server host:")
serverPort = int(input("Inserire server port:"))
serverAddress = (serverHost, serverPort)
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(serverAddress)

# Creazione della finestra principale dell'interfaccia grafica
window = tk.Tk()
window.title("Chat_Elaborato_Programmazione_di_Reti")
window.configure(background="green")

# Configurazione dell'area di testo in cui verranno visualizzati i messaggi
messages_frame = tk.Frame(window)
# Creazione di una scrollbar per navigare fra i messaggi precedenti
scrollbar = tk.Scrollbar(messages_frame)

# Creazione della parte contenente i messaggi
message_list = tk.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
message_list.pack(side=tk.LEFT, fill=tk.BOTH)
message_list.pack()
messages_frame.pack()

# Configurazione dell'area in cui si potranno scrivere i messaggi da inviare
input_area_message = tk.StringVar()
input_area_message.set("Scrivi qui il tuo messaggio.")
input_area = tk.Entry(window, textvariable=input_area_message)
# leghiamo la funzione send al tasto Return
input_area.bind("<Return>", send_message)
input_area.pack()


# Creazione del tasto invio, legato alla funzione send_message
send_button = tk.Button(window, text="Invio", command=send_message)
send_button.pack()

window.protocol("WM_DELETE_WINDOW", on_closing)

# Creazione del Thread che si occupa di mandare il ping al Server
pingThread = Thread(target=ping, args=(clientSocket,))
pingThread.start()

# Creazione del Thread che si occupa di ricevere i messaggi del Client
receiveThread = Thread(target=receive, args=(clientSocket,))
receiveThread.start()

# Avvio l'esecuzione della finestra grafica della Chat
window.mainloop()