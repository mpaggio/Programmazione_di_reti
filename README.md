# Programmazione_di_reti
## Struttura dell'esame:
Il progetto non è obbligatorio (ma serve per avere un voto maggiore di 28) --> 4 punti
Esame teorico --> 28 punti

## Strumenti di laboratorio:
### Whireshark
E' un analizzatore di protocollo (c'era una perdita di pacchetti nell'Università). Creò un protocollo che trasformava la scheda di rete con cui si collegava in rete, in una SCHEDA DI SNIFFING con cui poteva leggere i pacchetti che passavano per questa scheda.
La pila ISO-OSI è una rapprensentazione dei livelli di rete che ci permettono di trasmettere delle informazioni via rete:
    - DATA LINK(livello 2): instaura un collegamento tra due punti contigui della rete, libero da errori di trasmissione non segnalati.
    - NETWORK(livello 3): inserisce pacchetti nella rete, in modo tale che questi viaggino verso una destinazione (utilizza il protocollo TCP).
    - TRASPORTO(livello 4): permette a due entità di pari livello di conversare (utilizza 2 protocolli, ovvero TCP, orientato alla connessione e affidabile, e UDP, inaffidabile e non orientato alla connessione).
    - APPLICAZIONE(livello 5): applicazioni degli utenti della rete.
Quando attiviamo Whireshark, utilizza la modalità promiscua per catturare i pacchetti, che permette di leggere tutto il traffico che transita in quel punto della rete.

Aprire il Prompt dei Comandi e digitare:
    - `ipconfig`: mostra tutte le informazioni legate alle schede di rete disponibili.
    - `ping 8.8.8.8` oppure `ping www.google.com`: mostra l'indirizzo corrispondente all'indirizzo sintattico del server che risponde alle nostre richieste DNS.

E' possibile filtrare i pacchetti che si vogliono vedere, scrivendo nella barra di ricerca in alto, l'indirizzo IP che ci interessa, digitando `ip.addr = ...` (inserendo l'indirizzo IP di interesse).
Se clicchiamo su di un pacchetto vediamo la Pila TCP al contrario.

Oggi Google utilizza il protocollo https, che nel momento in cui stiamo facendo una transazione di informazioni e di dati, quei dati vengono criptati e garantiscono la tutela e la riservatezza (vedremo a laboratorio una funzione di "Encription", cioè atto al decriptaggio  -->  Tecnica TLS).

Quando si tenta di uscire dalla applicazione chiede se si vuole salvare (in un certo formato, per poter riprendere lo sniffing successivamente anche dopo aver chiuso e riaperto l'applicazione).

Il lavoro dell'analizzatore di protocollo si divide in 3 parti:
    - RACCOLTA: selezione e corretto posizionamento sulla rete dell'interfaccia di cattura in modalità promiscua (è possibile qui, per l'interfaccia, ascoltare tutto il traffico di quel segmento di rete).
    - CONVERSIONE: i dati grezzi vengono convertiti in formato comprensibile.
    - ANALISI: prende i dati catturati, verifica i protocolli basandosi sulle informazioni estratte e in base alle loro caratteristiche le analizza.

Man mano che si sale nella pila TCP-IP, le informazioni che vengono aggiunte al pacchetto sono sempre di più, arrivando ad avere 3 sezioni generali:
    - HEADER: frame start, addressing, types e quality control.
    - DATA: il contenuto del pacchetto, in termini legati a quello che l'utente vuole inviare.
    - TRAILER: error detection e frame stop.
(Ad ogni passaggio da uno strato all'altro, vengono aggiunte delle parti).

### Python (Spyder)

#### Variabili:
Le variabili sono dei nomi che fanno riferimento ad un valore. L'istruzione di assegnazione ci permette di affidare ad un nome un certo valore (stringe, valori numerici, ...).

#### Espressione:
Un espressione è una combinazione di valori, variabili ed operatori.

#### Concatenamento di stringhe:
Si utilizza semplicemente il + in mezzo alle variabili che contengono i valori che si vogliono concatenare.

#### Funzioni:
Una funzione è una serie di istruzioni che esegue un calcolo.
Un "modulo" è un file che contiene una raccolta di funzioni correlate (ad esempio Math è un modulo che contiene delle funzioni matematiche standard, Matplotlib e Numpy).
Per utilizzare un modulo bisogna importarlo nel progetto, mediante il comando `import`, specificando poi il nome del modulo.
Per definire noi una funzione con i relativi parametri, usare il comando `def nome_fun()`.

#### Istruzione di Break:
Il comando `break` serve per uscire da un ciclo, mentre il suo flusso di esecuzione, è in esecuzione.

#### Stringhe:
Una stringa è una sequenza di caratteri, ognuno dei quali è contrassegnato da un indice (a cui posso accedere proprio mediante l'indice). Gli indici vengono contati a partire dal valore 0.
La stringa è per definizione immutabile (una volta creata non posso modificare i suoi caratteri). Se voglio modificare un valore, devo per forza crearne un'altra.

#### Metodi:
Si tratta di un meccanismo che mi permette di utilizzare un oggetto, utilizzando delle operazioni utili (funzioni), messe a disposizione dall'oggetto stesso.

#### Lettura di un file:
Prima di poter visualizzare il file, è necessario poter vedere in quale directory di lavoro ci troviamo, utilizzando il modulo Os (`import os`), tramite il comando `os.getcwd()`.
E' possibile leggere un file presente nel nostro dispositivo, mediante il comando `open()`, che restituisce un oggetto di tipo "file".
E' possibile usare altri metodi di lettura, ad esempio `.readline()`, che legge i caratteri di un file fino a quando non giunge ad una andata a capo (\n).

#### Scrittura su file:
Prima bisonga aprirlo in modalità scrittura, tramite il comando `open(nome_file, "w")` e poi utilizzando il comando `.write()` è possibile specificare il testo che si vuole scrivere sul file.

#### Liste:

#### Dizionari:
Consentono di associare un valore ad una chiave.

#### Tuple:
Rappresentano il risultato di un'operazione di connessione verso un server (sono presenti 2 oggetti che caratterizzano la tupla, 2 informazioni per la connessione, ovvero INDIRIZZO DI DESTINAZIONE e PORTA)
Le tuple sono immutabili (per modificarne i valori è necessario crearne una nuova).

#### Operatori di formato:


## LEZIONE DI LABORATORIO 002:
### DNS
Il DNS è uno degli elementi costitutivi di Internet, che costituisce il database di informazioni, globale, che è responsabile della traduzione dei nomi simbolici in indirizzi e viceversa e dell'instradamento della posta alla destinazione corretta.

### Resolver
Il Resolver è la parte client del sistema, che pone le domande sui nomi degli host (di solito è una piccola libreria compilata in qualsiasi linguaggio, che richiede i servizi DNS e conosce quello che basta per inviare una query a un nameserver.

### Nameserver
Si tratta di un server software, che risponde alle query DNS (a volte conosce direttamente la risposta, se è "Autoritativo", mentre altre volte deve andare su Internet e chiedere in giro per trovare la risposta, se è "Ricorsivo").

### Query flow
1) Il sistema operativo tenta di risolvere localmente l'indirizzo (cercando nella chache locale), ma se la risposta non è disponibile, effettua una richiesta al RECURSIVE SERVER.
2) Il RECURSIVE SERVER controlla la sua cache, se non trova il record, effettua una richiesta per nostro conto ad uno qualsiasi dei 13 ROOT SERVER.
3) Se il ROOT SERVER non conosce la risposta alla nostra richiesta, invia un record al RECURSIVE SERVER, con un elenco dei Global Top Level Domain, ovvero i server responsabili di un dominio (sotto forma di record).
4) Il RECURSIVE SERVER, utilizzando la risposta del ROOT SERVER, sceglie a caso uno dei server autoritativi GLTD e invia la stessa query. Se il server non conosce la risposta specifica alla domanda, restituisce un "REFERRAL" (un set di record) ad un server che con buona probabilità conosce la risposta.
5) Il RECURSIVE NAMESERVER, sceglie a caso uno dei nameserver e invia una terqua query, uguale alle altre due già inviate.
6) Ora che ha la risposta, il RECURSIVE NAMESERVER dell'ISP, consegna la risposta al client e soddisfa la query. Il RECURSIVE NAMESERVER archivia questa risposta nella propria cache, nel caso in cui questo o qualche altro client effettui la stessa query in un altro momento.
7) Se la risposta non viene trovata entro un certo periodo, allora per evitare di essere continuamente sbalzati in giro fra i server, ci viene detto che è finito il tempo massimo disponibile per la ricerca e ci viene detto che quell'indirizzo non esiste.

### DNS in Python
- Bisogna scaricare e utilizzare la libreria `dns.resolver`.
- Bisogna gestire le eccezioni tramite il comando `except` successivo al comando `try`.

### Appunti vari
La nostra macchina non ha in cache l'indirizzo di www.google.com, chiede quindi al server locale, poi lo chiede al root server, poi manda un IP che indirizza ad un altro server, altrimenti se questo non ha la risposta risponde con il nome del server autoritativo (ovvero .com), che se non ha l'indirizzo, allora non esiste, lo restituisce al nostro Nameserver ISP e ce lo fornisce.

`Ip look up` ci fornisce il nome simbolico dell'indirizzo IP, fa la cosi detta "Query inversa".

### Query inversa
Immaginiamoci di avere un indirizzo IP (143.50.23.2), l'elemento più significativo è quello più a sinistra, mentre quello meno significativo sta a destra. Per fare la query inversa faccio il processo inverso, capovolgendo l'indirizzo (2.23.50.143) e vado a prendere il valore "[0]", perchè il risultato della operazione è una lista di elementi (pensiamo a quanti siti si possono visitare utilizzando svariati nomi per lo stesso indirizzo, ad esempio TIM.it, oppure TelecomItalia.it).
- Si tratta di una lista di tutti i nomi simbolici associati ad uno stesso indirizzo IP.
- Si utilizza il metodo `reversename.from_address('IP_ADDRESS')`.

### LDAP
Acronimo di Lightwight Directory Access Protocol, è un protoccollo di rete utilizzato per accedere e gestire le informazioni memorizzate in un servizio directory (ovvero una struttura di archiviazione che memorizza dati come nomi, indirizzi e altre informazioni). Quello che ci serve avere sono: permessi e identificativo di cosa stiamo cercando.
1) LDAP Bind Request: tramite password chiedo di accedere a quella directory e mi viene detto Ok o Not Ok.
2) LDAP Bind Responde:
3) LDAP Search Request:
4) LDAP Search Response:
5) LDAP Unbind Request:
In Python viene utilizzata la libreria `ldap`, per eseguire la ricerca LDAP.

### Traceroute (Tracert)
Si tratta di un Programma diagnostico, tramite il quale, scegliendo un server, inserito l'indirizzo IP dell'host di destinazione e dando invio, il server invia un certo numero di pacchetti speciali verso tale destinazione. Questi pacchetti attraversano vari router, quando un router ne riceve uno, invia un breve messaggio che torna all'origine (messaggio contenente il nome e l'IP adress del router che l'ha inviato). Ripete l'operazione per 3 volte consecutive.

### TTL (Time To Live)
Il TTL indica il numero massimo di Hop (ovvero di Step) che può compiere per riuscire a giungere all'indirizzo destinatario specificato. Indica il numero di router che può passare per arrivare all'indirizzo di destinazione. Il TTL limita la durata della "vita" dei dati in una rete IP. Ad ogni pacchetto di dati viene assegnato un valore TTL. Ogni volta che un pacchetto di dati raggiunge un salto, il valore TTL viene diminuito di uno.




