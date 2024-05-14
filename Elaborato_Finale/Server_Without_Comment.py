#!/usr/bin/env python3

from socket import *
from threading import *
import sys
import time
import traceback

ping_thread_stop = []

def ping(client, indice):
    global ping_thread_stop
    while ping_thread_stop[indice] == 0:
        try:
            time.sleep(3)
            if client.fileno() != -1:
                client.send("[ping]".encode("utf-8"))
                print("[System]: Sent ping")
            else:
                break
            
        except ConnectionResetError:
            print("Tentativo di ricezione su socket precedentemente chiusa, terminazione in corso ...")
            break

        except Exception as ex:
            print(f'Problema rilevato: {ex}, chiusura in corso ...')
            traceback.print_exc()
            break


def broadcast(message, clients):
    for client in clients:
        client.send(message)


def delete_client(client):
    client.send("[quit]".encode("utf-8"))
    index = clients.index(client)
    clients.remove(client)
    nickname = nicknames[index]
    nicknames.remove(nickname)
    print(f"Rimosso {nickname} dalla chat")
    broadcast(f'{nickname} ha lasciato la chat!'.encode("utf-8"), clients)


def handle(client, pingThread, indice):
    global ping_thread_stop
    pingThread.start()
    while True:
        try:
            client.settimeout(10)
            message = client.recv(1024).decode("utf-8")
            if not message:
                delete_client(client)
                break
            if "[ping]" not in message:
                if message != "[quit]":
                    total_message = nicknames[indice] + ": " + message
                    broadcast(total_message.encode("utf-8"), clients)
                else:
                    ping_thread_stop[indice] = 1
                    while pingThread.is_alive():
                        ping_thread_stop[indice] = 1
                    clients.remove(client)
                    nickname = nicknames[indice]
                    nicknames.remove(nickname)
                    print(f"Rimosso {nickname} dalla chat")
                    broadcast(f'{nickname} ha lasciato la chat!'.encode("utf-8"), clients)
                    print("Nickname dei Client rimanenti nella chat:\n ")
                    for nick in nicknames:
                        print(nick) 
                    break
            else:
                print("[System]: Client ping arrived")

        except timeout:
            print(f'{nickname} non è più connesso.')
            delete_client(client)
            break

        except ConnectionResetError:
            print("Tentativo di ricezione su socket precedentemente chiusa, terminazione in corso ...")
            break
            

        except Exception as ex:
            print(f'Problema rilevato: {ex}, chiusura in corso ...')
            traceback.print_exc()
            break
            
            
def receive(server, clients, nicknames):
    while True:
        try:
            client, clientAddress = serverSocket.accept()
            print(f'Connesso con {str(clientAddress)}')
            nickname = client.recv(1024).decode("utf-8")
            nicknames.append(nickname)
            clients.append(client)
            print(f"Nickname: {nickname}")
            client.send(f'Benvenuto {nickname}! \nSe vuoi lasciare la chat scrivi \"[quit]\".'.encode("utf-8"))
            broadcast(f'{nickname} si è unito alla chat!'.encode("utf-8"), clients)
            ping_thread_stop.append(0)
            indice_ping = len(ping_thread_stop) - 1
            pingThread = Thread(target=ping, args=(client,indice_ping,))
            handleThread = Thread(target=handle, args=(client, pingThread, indice_ping,))
            handleThread.start()
           
        except OSError:
            print("Tentativo di accept su Socket chiusa, chiusura in corso ...")
            break

        except Exception as ex: 
            print(f'Problema rilevato: {ex}, chiusura in corso ...')
            traceback.print_exc()
            break


serverHost = input("Inserisci server host:")
serverPort = int(input("Inserisci server port:"))
serverAddress = (serverHost, serverPort)
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(serverAddress)
serverSocket.listen(5)
clients = []
nicknames = []


if __name__ == "__main__":    
    receiveThread = Thread(target=receive, args=(serverSocket, clients, nicknames))
    receiveThread.start()
    print("In attesa di connessioni ...")

    while True:
        try: 
            time.sleep(5)
            print("Server in esecuzione")

        except KeyboardInterrupt:
            print("Avviata procedura di chiusura del Server ... (CTRL+C)")
            for client in clients:
                delete_client(client)
            print("Tutti i client sono stati disconnessi")
            clients = []
            nicknames = []
            serverSocket.close()
            print("Server disconnesso")

            sys.exit(0)