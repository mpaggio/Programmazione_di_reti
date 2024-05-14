#!/usr/bin/env python3

from socket import *
from threading import *
import tkinter as tk
import time
import sys
import traceback

ping_thread_stop = 0
receive_thread_stop = 0


def connect_to_server(server_address):
     global clientSocket
     while True:
        try:
           clientSocket.connect(server_address)
           clientSocket.send(nickname.encode("utf-8"))
           break

        except ConnectionRefusedError:
            print("Server non raggiungibile, si prega di riprovare a connettersi")
            sys.exit(0)

        except Exception as ex:
            print(f'Connessione fallita, tentativo di riconnessione in corso: {ex}')
            traceback.print_exc()
            time.sleep(3)
        


def ping(client):
    global receive_thread_stop
    while ping_thread_stop == 0:
        try:
            time.sleep(3)
            if clientSocket.fileno() != -1:
                client.send("[ping]".encode("utf-8"))
                print("[System]: Sent ping")
            else:
                print("----- Terminato il PING THREAD -------")
                break
            
        except Exception as ex:
            print(f'Problema rilevato: {ex}, chiusura in corso ...')
            traceback.print_exc()
            break
     

def send_message(event = None):
        global ping_thread_stop
        global receive_thread_stop
        messaggio = input_area_message.get()
        input_area_message.set("")
        input_area.delete(0, tk.END)
        if clientSocket.fileno() != -1:
            clientSocket.send(messaggio.encode("utf-8"))
        if messaggio == "[quit]":
            ping_thread_stop = 1
            receive_thread_stop = 1
            while pingThread.is_alive() or receiveThread.is_alive():
                ping_thread_stop = 1
                receive_thread_stop = 1
            clientSocket.close()
            window.quit()


def receive(client):
    global ping_thread_stop
    global receive_thread_stop
    while receive_thread_stop == 0:
            try:
                if client.fileno() != -1:
                    client.settimeout(10)
                    message = client.recv(1024).decode("utf-8")
                    if message == "[quit]":
                        print("Disconnessione in corso a causa della chiusura del Server ...")
                        ping_thread_stop = 1
                        send_button.config(state='disabled')
                        while pingThread.is_alive():
                            ping_thread_stop = 1
                        clientSocket.close()
                        window.quit()
                        break
                    elif "[ping]" not in message:
                        message_list.insert(tk.END, message + '\n')
                        print(message)
                    else:
                        print("[System]: Server ping received")
                else:
                    print("------ Terminato il RECEIVE THREAD ------")
                    break

            except timeout:
                clientSocket.close()
                print('Il Server non è più attivo quindi sei stato disconnesso')
                window.quit()
                print("------ Terminato il RECEIVE THREAD ------")
                break

            except Exception as ex:
                print(f'Problema rilevato: {ex}, chiusura in corso ...')
                traceback.print_exc()
                clientSocket.close()
                window.quit()
                break 


def on_closing(event = None):
      input_area_message.set("[quit]")
      send_message()


serverHost = input("Inserire server host:")
serverPort = int(input("Inserire server port:"))
nickname = input("Inserire nickname:")
serverAddress = (serverHost, serverPort)
clientSocket = socket(AF_INET, SOCK_STREAM)
connect_to_server(serverAddress)


window = tk.Tk()
window.title("Chat_Elaborato_Programmazione_di_Reti")
window.configure(background="green")
messages_frame = tk.Frame(window)
scrollbar = tk.Scrollbar(messages_frame)
message_list = tk.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
message_list.pack(side=tk.LEFT, fill=tk.BOTH)
message_list.pack()
messages_frame.pack()
input_area_message = tk.StringVar()
input_area_message.set("Scrivi qui il tuo messaggio.")
input_area = tk.Entry(window, textvariable=input_area_message)
input_area.bind("<Return>", send_message)
input_area.pack()
send_button = tk.Button(window, text="Invio", command=send_message)
send_button.pack()

window.protocol("WM_DELETE_WINDOW", on_closing)

pingThread = Thread(target=ping, args=(clientSocket,))
pingThread.start()
receiveThread = Thread(target=receive, args=(clientSocket,))
receiveThread.start()

window.mainloop()

sys.exit(0)