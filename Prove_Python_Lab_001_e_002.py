# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 17:09:44 2024

@author: mpagg
"""

# OPERAZIONI CON LE STRINGHE
src_address = '210.000.000.001'
dst_address = '210.000.000.00'
indice = 0
dst_address = dst_address + src_address[0]      # Accesso al singolo carattere
header_simpl = src_address + dst_address        # Concatenazione di stringhe
while indice < len(src_address):                # Attraversamento della stringa
    carattere = src_address[indice]
    print(carattere)
    indice = indice + 1
print("Indirizzo parziale con valori n ed m: ", src_address[3:7]) # Slicing tot.
print("Indirizzo parziale con solo valore n: ", src_address[3:])  # Slicing parz.
print("Indirizzo parziale con solo valore m: ", src_address[:7])  # Slicing parz.
print("Indirizzo sorgente: ", src_address)
print("Indirizzo destinazione: ", dst_address)
print("Header semplificato:", header_simpl)


# IMPORTAZIONE DI UN MODULO
import math
potenza_segnale = int(input("Inserisci il valore del segnale:"))
potenza_rumore = int(input("Inserisci il valore del rumore:"))
SNR = potenza_segnale/potenza_rumore  ## SNR identifica il rapporto segnale-rumore
SNR_dB = 10*math.log10(SNR)           ## SNR in base decimale
print("Il valore di SNR in dB è", SNR_dB)


# GENERAZIONE DI GRAFICI
import numpy as np
import matplotlib.pyplot as plt
x = np.linspace(0, 2*np.pi)           ## Il dominio della funzione è (0,2pi)
y = np.sin(x)                         ## Definisco la funzione da rappresentare
plt.plot(x,y,marker = "o", color = "red")


# DEFINIZIONE DI UNA FUNZIONE
def area_rettangolo(x,y):
    area = x*y
    return area
print("L'area di un rettangolo con lati 4 e 5 è: ", area_rettangolo(5, 4))


# UTILIZZO DI ESPRESSIONI CONDIZIONALI
valore_input = int(input("Inserire valore intero:"))
if valore_input < 1024:
    print("Il numero di porta inserito è una well-known port!")
else:
    print("Il numero di porta inserito è una ephemeral port")
    
    
# UTILIZZO DELLA RICORSIONE
def stampa_n(n):
    if n <= 0:
        return
    print(n)
    stampa_n(n-1)
stampa_n(10)
    

# UTILIZZO DI ITERAZIONE CON BREAK
riga = "."
while True:
    if riga == "...":
        print(riga)
        print("Finito")
        break
    print(riga)
    riga = riga + "."
    
    
# OPERAZIONI SU FILE
import os                                       # Libreria per il file system
print(os.getcwd())                              # Identifica la cartella corrente
fin =  open("Prova_di_lettura_da_file.txt")     # Apertura del file in lettura
print(fin.readline())
print(fin.readline())
print(fin.readline())
fin.close()
fout = open("Prova_di_lettura_da_file.txt", 'w') # Apertura del file in scrittura
fout.write("Ciao anche a te, si ho letto il file (scritto da comando).")
fout.write("Ho finito di utilizzare il file quindi lo chiudo")
fout.close()

# OPERAZIONI SU LISTE
lista = ["ciao", 2.12, "io sono", ["Marco", "Paggetti"]]  # Creazione lista
print(lista)
for val in lista:                               # Esempio di attraversamento (for)
    print(val)

# UTILIZZO DI DIZIONARI
protocol_dictionary = {"SSH": "22", "FTP":"21", "DNS":"53", "HTTP":"80"}
print(protocol_dictionary)  
print(protocol_dictionary.get("SSH","null"))
print(protocol_dictionary.get("sh", "null"))  

# UTILIZZO DI TUPLE
tupla1 = "a","b","c","d"
print(type(tupla1))
print(tuple(tupla1))
a,b = "a","b"
print("Valore di a: ", a, "Valore di b:", b)

