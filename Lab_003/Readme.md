# LEZIONE 003 (26/03/2024)
## SOCKET:
- Si tratta di un oggetto software che permette l'invio e la ricezione di dati, tra host remoti (attraverso la rete) o tra processi locali.
- Il concetto di Socket si basa sul modello di I/O su file di Unix, ovvero sulle operazioni `open`, `read`, `write` e `close` (l'utilizzo avviene secondo le stesse modalità, ma con l'aggiunta dei parametri utili alla comunicazione, quali gli indirizzi IP, i numeri di porta e i protocolli).
- Si viene a formare una coppia composta da Socket locale e Socket remota (composta da indirizzo e posta del client e del server).
- Il FUNZIONAMENTO DELLA SOCKET si compone di alcuni passaggi:
    1) Client e Server creano i loro rispettivi Socket e il Server, pone quest'ultima in ascolto su una porta (dato che il server può creare più connessioni con client diversi, ha bisogno di una coda per gestire le varie richieste).
    2) Il Client invia una richiesta di connessione al Server, il quale (nel caso in cui accetti la richiesta) crea una nuova connessione. 
        --> OSSERVAZIONE: potrebbero esserci più porte, dovute al fatto che una potrebbe essere dedicata solo al flusso in uscita e uno in entrata (dipende dalle configurazioni).
    3) Il Client e il Server comunicano attraverso un canale virtuale, caratterizzato dal Socket del Client e da un nuovo Socket (creato appositamente dal Server per quel flusso di dati), chiamato "DATA SOCKET".
        --> OSSERVAZIONE: il Server crea un nuovo Socket, poichè il primo viene utilizzato esclusivamente per la gestione delle richieste dei vari Client. 
    4) Dato che il TCP è un protocollo orientato alla connessione, quando non si ha più la necessità di comunicare, il Client lo comunica al Server, che deistanzia il Data Socket, chiudendo di fatto la connessione.
- I tipi di protocolli utilizzati dalla Socket appartengono a due famiglie principali:
    --> **AF_INET**: comunicazione tra host remoti (tramite Internet).
    --> **AF_UNIX**: Comunicazione tra processi locali (ad esempio il servizio di stampa).

## LOOPBACK:
- Si tratta di una scheda di rete virtuale gestita dal protocollo TCP/IP.
- I dati inviati all'indirizzo IP di Loopback (ovvero l'indirizzo `127.0.0.1`) non vengono instradati attraverso la scheda di rete, ma attraverso l'interfaccia di Loopback.
- Tramite il Loopback, i dati vengono gestiti localmente, senza l'ausilio della scheda di rete (da qui il termine `localhost`).
- Lo scopo è quello di testare il funzionamento di un sistema.

## PROGRAMAZIONE SOCKET TCP PYTHON
### Programmazione TCP_Socket_Server:
- Utilizzare la libreria `socket`, per utilizzare tutte le funzioni legate all'oggetto Socket.
- La Socket, viene creata mediante la funzione `socket()`, a cui vengono passati due argomenti:
    1) NOME DELLA FAMIGLIA DEL PROTOCOLLO: ad esempio `AF_INET`(comunicazione fra host remoti), oppure `AF_UNIX` (comunicazione fra host locali).
    2) TIPOLOGIA DI CONNESSIONE: si può inserire `SOCK_STREAM` (per connessioni di tipo TCP), oppure `SOCK_DGRAM` (per connessioni UDP).
- Il Server deve poi associare la propria Socket con l'indirizzo locale (`localhost`), tramite la funzione `socket.bind()`.
- La funzione `socket.listen()` prende come parametro la dimensione della CODA DI BACKLOG, ovvero il numero di tentativi di connessione, che non sono ancora state accettate dall'applicazione (inserendo 1 come parametro si sta dicendo che al massimo si avrà solamente 1 Client in attesa, non di più).
- La funzione `socket.accept()` serve per accettare una connessione. La Socket deve essere connessa ad un indirizzo ed essere in fase di "listening" verso tentativi di connessione. La funzione ritorna una coppia di valori:
    1) CONNECTION: si tratta di una nuova Socket su cui è possibile chiamare delle funzioni per inviare o ricevere informazioni sulla connessione creata.
    2) ADDRESS: si tratta dell'indirizzo associato alla Socket dall'altro lato della connessione.
- La funzione `socket.recv()` serve per leggere un quantitativo di byte specificato dall'argomento passato alla funzione durante la sua invocazione (ad esempio socket.recv(1024) leggerà al massimo 1024 byte).
- La funzione `socket.send()` serve per inviare dei dati alla Socket (nel nostro caso vengono inviati dei messaggi, codificati in sequenze di bytes, sia per il caso di file non trovato, che in caso di esito positivo).
- La funzione `socket.close()` serve per terminare la connessione, eliminando qualsiasi risorsa associata alla Socket utilizzata per la connessione.

### Programmazione TCP_Socket_Client in Python:
- Bisogna modificare le impostazioni del comando di run, in maniera tale che quando il codice viene fatto eseguire, venga passata come argomento la stringa `127.0.0.1 8080 index.html`.
- Crea subito la Socket Client mediante la funzione `socket.socket()`, passando gli stessi argomenti del Server.
- Distingue subito l'host, la porta e la richiesta da parte del Client al Server.
- Prova a connettersi mediante il comando `socket.connect()`, specificando come argomenti l'indirizzo IP e la porta dell'host da raggiungere con la richiesta di connessione.
- La Socket del Client manda a quella del Server, un messaggio in cui specifica l'informazione richiesta, mediante la funzione `socket,send()`.
- La Socket del Client utilizza poi la funzione `socket.recv()` per ricevere la risposta alla sua richiesta (nel nostro caso leggerà al massimo 1024 byte di risposta).

## PROGRAMAZIONE SOCKET UDP PYTHON
### Programmazione UDP_Socket_Server:
- Crea la Socket mediante la funzione `socket.socket()`, specificando come argomenti la famiglia `AF_INET` e come connessione quella UDP, mediante il parametro `SOCK_DGRAM`.
- Associa la Socket appena creata all'indirizzo IP locale, mediante la funzione `socket.bind()`, passando come parametri `localhost` (indirizzo IP locale) e `10000`, ovvero la porta su cui dovrà lavorare.
- La funzione `socket.recvfrom()` legge i dati in ingresso in socket connessi e non connessi e acquisisce l'indirizzo da cui sono stati inviati i dati, specificando come argomento il numero di byte da lggere dal pacchetto ricevuto (si tratta di una funzione bloccante, perchè se ci sono problemi, ad esempio quando non c'è nessun pacchetto da ricevere, il processo viene messo in stato sleeping, aspettando che arrivi un pacchetto che lo risvegli).

### Programmazione UDP_Socket_Client:
- Crea la propria Socket, mediante la funzione `socket.socket()`, specificando gli stessi argomenti del Server (`AF_INET` e `SHOCK_DGRAM`).
- Definisce la domanda del messaggio (in maniera da capire noi umani che richiesta sta facendo) e definisce l'indirizzo del Server a cui collegarsi, come coppia `localhost`-porta_utilizzata (in questo caso la 10000).
- La funzione `socket.sendto()`, server per inviare dei dati ad una destinazione specificata (prende come argomenti il messaggio da inviare e l'indirizzo del Server a cui inviare il messaggio).
- Utilizza la funzione `socket.recvfrom()` per aspettare di ricevere il pacchetto dal Server, contenente la risposta alla sua richiesta.
- Indica al Server di voler chiudere la connessione mediante la funzione `socket.close()`.


## CONFRONTO TCP - UDP
### Wireshark TCP:
- Pacchetto TCP con `RST` (reset) e `ACK` (acknowledge), vuol dire che c'è un problema fra il client e server e c'è una perdita di pacchetti (ad esempio quando il pacchetto è formattato in un modo che il server non riesce a capire).
- Dopo ognuno di questi pacchetti, c'è una nuova trasmissione del pacchetto (Pacchetto TCP con `RETRASMISSION`).

### Trasmissione TCP - Server Socket e Client Socket
1) Three-way handshake:
    1) Il Client manda una richiesta di sincronizzazione (`SYN`) al Server sulla porta che quest ultimo mette a disposizione.
    2) Il Server risponde, inviando un `ACK` (per confermare l'avvenuta ricezione della richiesta di connessione) e un altro `SYN` per chiedere al Client se si tratta di un vecchio tentativo di connessione, o se intende ancora connettersi.
    3) Il Client risponderà con un `ACK` per confermare la ricezione della richiesta di connessione da parte del Server (instaurando così a tutti gli effetti la connessione).
...
5) Chiusura della connessione (potrebbe essere utilizzato ancora il 3-way handshake, ma questa volta con il messaggio `FIN`, che indica la volontà di terminare la connessione).

### Trasmissione UDP - Server Socket e Client Socket
- Sono le trasmissioni non orientate alla comunicazione, dove non si hanno ritrasmissione di pacchetti (ad esempio le chiamate VoIP come quelle su Teams o Zoom).
- Il protocollo TCP viene definito **orientato alla connessione**, perchè prima di inviare messaggi, richieste, o altro, si accerta della corretta creazione della connessione e si accerta che tutti e due gli estremi della connessione siano in grado di comunicare.
- Il protocollo UDP non è orientato alla conessione, in quanto trasmette messaggi e pacchetti, senza preoccuparsi che ci sia qualcuno effettivamente in ascolto (anche nella programmazione in Python, non viene più messo l'assert, che controllava l'Handshaking della connessione, perchè l'UDP non lo fa).
- Con TCP, tutti i pacchetti devono arrivare a destinazione, mentre con UDP, anche se qualche pacchetto viene perso non succede nulla di grave (oltre la non ritrasmissione dei paccheti, il protocollo UDP non supporta il riordinamento dei pacchetti).
- All'interno delle connessioni UDP, non c'è nessun controllo, ma c'è una ricezione ed una risposta immediata delle informazioni.
- A livello di programmazione, nella parte relativa alle Socket UDP, non è più presente il comando `listen()`, perchè non c'è nessun tipo di Handshaking (viene inviato direttamente il pacchetto, oppure richiesto un pacchetto, senza accertarsi dell'ascolto o che ci sia effettivamente qualcuno dall'altro lato).
- La struttura della connessione è composta da:
1) Invio della richiesta al Server, da parte del Client.
2) Invio della risposta da parte del Server, verso il Client.