# Programmazione_di_reti
## Struttura dell'esame:
Il progetto non è obbligatorio (ma serve per avere un voto maggiore di 28) --> 4 punti
Esame teorico --> 28 punti

## LEZIONE_001

## ----------------------------------------------------------------------------------------------------------------------------------------------------------- ##
## Introduzione Whireshark
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

E' possibile filtrare i pacchetti che si vogliono vedere, scrivendo nella barra di ricerca in alto l'indirizzo IP che ci interessa, il protocollo dei pacchetti che ci interessa analizzare e anche altro.
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

## Introduzione Python con Spyder

#### Variabili:
Le variabili sono dei nomi che fanno riferimento ad un valore. L'istruzione di assegnazione ci permette di affidare ad un nome un certo valore (stringe, valori numerici, ...).

#### Espressione:
Un espressione è una combinazione di valori, variabili ed operatori.

#### Stringhe
- Una stringa è una sequenza di caratteri, ognuno dei quali è contrassegnato da un "indice", ovvero un numero intero che indica il carattere della sequenza che si desidera estrarre (sono i valori che si inseriscono all'interno delle parentesi quadre nelle stringhe). Gli indici vengono contati a partire dal valore 0. Gli indici negativi vengono utilizzati per contare a ritroso, ovvero dalla fine della stringa (ad esempio -1 fa riferimento all'ultimo carattere della stringa).
- La stringa è per definizione "IMMUTABILE", cioè, una volta creata non posso modificare i suoi caratteri (se voglio modificare un valore, devo per forza crearne un'altra). 
- Per concatenare due o più stringhe, si utilizza semplicemente il '+' in mezzo alle variabili che contengono i valori che si vogliono concatenare. 
- Per calcolare la dimensione di una stringa di caratteri (ovvero da quanti caratteri è formata) è possibile utilizzare la funzione `len(nome_var)`, che restituisce un intero, il quale indica la dimensione della stringa.
- Per "Attraversamento" si intende il tipo di calcolo che comporta l'elaborazione di una stringa, un carattere per volta.

#### Slicing (stringhe):
Un segmento/porzione di stringa è chiamato "SLICE", mentre lo "SLICING" è l'operazione di selezione di una porzione di stringa (paragonabile alla selezione di un carattere della stringa mediante l'uso di indici):
    - `[n:m]`: restituisce la porzione di stringa nell'intervallo compreso fra n (incluso) ed m (escluso).
    - `[:m]`: come nel caso precedente, ma invece di partire da n, parte dal primo elemento della stringa.
    - `[n:]`: come nel caso iniziale, ma invece di arrivare fino ad m escluso, arriva fino in fondo alla stringa.

#### Funzioni:
- Una funzione è una serie di istruzioni che esegue un calcolo.
- Un "modulo" è un file che contiene una raccolta di funzioni correlate (ad esempio Math è un modulo che contiene delle funzioni matematiche standard, Matplotlib per la generazione di grafici e Numpy per lavorare sugli array).
- Per utilizzare un modulo bisogna importarlo nel progetto, mediante il comando `import`, specificando poi il nome del modulo.
- Per definire noi una funzione con i relativi parametri, usare il comando `def nome_fun()` (specificando anche eventuali parametri da passargli).

#### Istruzioni condizionali:
Consentono di controllare se si verificano determinate condizioni e consentono quindi di variare conseguentemente il comportamento del programma, tramite strutture del flusso delle operazioni (ad esempio if, for, while, ...).

#### Ricorsione:
La ricorsione si verifica ogni volta che una funzione richiama sè stessa (l'istruzione `return` serve per provocare l'uscita dalla funzione, provocando il ritorno del flusso di esecuzione al chiamante, senza eseguire le righe di codice rimanenti).

#### Iterazione:
La ripetizione di operazioni identiche o simili, viene chiamata "iterazione" e può essere realizzata con vari costrutti, come il `while`, oppure il `for`. A volte capita di dover uscire dal flusso dell'iterazione, quando il ciclo stesso è in esecuzione. Questo può essere realizzato mediante il comando `break`, che serve per uscire da un ciclo, mentre il suo flusso di esecuzione, è in esecuzione.

#### Metodi:
Sono simili a delle funzioni, ovvero ricevono argomenti e restituiscono un valore con una diversa sintassi. La chiamata di un metodo prende il nome di "INVOCAZIONE".
    - `upper()`: prende una stringa e ne crea una copia, con tutte le lettere maiuscole.
    - `find()`: restituisce l'indice della posizione del carattere passatogli come argomento all'interno della stringa (se non è presente restituisce -1). Questo metodo è in grado di ricercare anche sottostringhe, non solo e unicamente dei caratteri (nel caso indica l'indice di partenza della sottostringa nella stringa originale). Il metodo è anche in grado di ricevere come secondo argomento l'indice da cui partire a verificare.

#### Lettura di un file:
- Prima di poter visualizzare il file, è necessario poter vedere in quale directory di lavoro ci troviamo, utilizzando il modulo "OS" (`import os`), tramite il comando `os.getcwd()`.
- E' possibile leggere un file presente nel nostro dispositivo, mediante il comando `open(file_name)`, che restituisce un oggetto di tipo "file".
- L'oggetto FILE comprende dei metodi di lettura, ad esempio `.readline()`, che legge i caratteri del file, fino a quando non giunge ad una andata a capo (\n).
- Prima di poter scrivere sul file, bisonga aprirlo in modalità scrittura, tramite il comando `open(nome_file, "w")` e poi utilizzando il comando `.write()` è possibile specificare il testo che si vuole scrivere sul file.
- Una volta che si ha finito di usare il file, è opportuno chiuderlo, tramite il comando `close()`.

#### Liste:
- Sono delle sequenze di valori, che non necessariamente devono essere solamente dei caratteri (come invece è per le stringhe), ma possono essere di tipi diversi.
- I valori che appartengono ad una lista vengono chiamati "ELEMENTI" della lista.
- Il metodo classico per creare una nuova lista è racchiudendo i suoi elementi tra parentesi quadre (`lista = ["...", 1.3, "asfwe"]`).
- Una lista all'interno di un'altra lista viene detta "NIDIFICATA".
- Le liste sono MUTABILI, perciò i loro elementi possono essere cambiati (la modalità di accesso ad un elemento della lista rimane la stessa delle stringhe).
    - Il metodo `len()` restituisce la dimensione della lista (il numero degli elementi che la compongono).
    - Il metodo `range()` restituisce una lista di indici da 1 ad n-1 (dove n è la lunghezza passata come argomento).
    - Il metodo `append()` aggiunge un nuovo elemento in coda alla lista (passatogli come argomento).
    - Il metodo `extend()` prende una lista come argomento e accoda i suoi elementi.
    - Il metodo `sum(list_name)` somma tutti i valori numerici presenti all'interno di una lista.
- Le liste possono essere concatenate mediante l'operatore `+` (proprio come per le stringhe).
- L'operatore `*` ripete una lista per un dato numero di volte.
- Anche sulle liste è possibile eseguire operazioni di SLICING (tramite il costrutto `[n:m]`, dove uno dei due può essere omesso).
- Per cancellare gli elementi di una lista sono disponibili i metodi `pop(index)`, `del(index)` e `remove(character/substring)`

#### Operazioni particolari:
- MAPPA: Si tratta di un'operazione che applica una funzione su ciascun elemento di una sequenza di valori (che sia esso una stringa, una lista o altro).
- FILTRO: Si tratta di un'operazione di selezione di alcuni elementi di una lista, per formare una sottolista.

#### Dizionari:
Rappresenta una mappatura simile alle liste, dove però gli indici possono essere quasi di ogni tipo (non esclusivamente degli interi come per le liste). Contengono una raccolta di indici (CHIAVI) ed una raccolta di dati, associati fra di loro: ogni chiave è associata ad un solo valore. Ogni associazione viene chiamata "COPPIA CHIAVE-VALORE".
- `get(key, standard_value)`: se la chiave è presente nel dizionario, viene restituito il valore che identifica, mentre se non è presente, viene restituito il valore predefinito passato come secondo argomento del metodo.

#### Tuple:
- Sono una sequenza di valori (di qualsiasi tipo) separati da una virgola, indicizzati da valori interi (sono IMMUTABILI, cioè non modificabili una volta che sono state create).
- Rappresentano il risultato di un'operazione di connessione verso un server (sono presenti 2 oggetti che caratterizzano la tupla, 2 informazioni per la connessione, ovvero INDIRIZZO e PORTA, sorgente e destinazione).
- E' possibile creare una tupla o specificando i valori durante l'assegnazione, separati da virgola, oppure mediante il metodo `tuple()`, dove se viene specificata una sequenza di valori (lista, tupla, ...), viene creata una tupla contenente quei valori.

#### Operatori di formato:
Permettono di inserire dei valori numerici all'interno del testo stampato:
    - `%d`: utilizzato per formattare un intero.
    - `%g`: utilizzato per formattare un decimale in virgola mobile (floating-point).
    - `%s`: utilizzato per formattare una stringa.
## ----------------------------------------------------------------------------------------------------------------------------------------------------------- ##

## LEZIONE_002

## ----------------------------------------------------------------------------------------------------------------------------------------------------------- ##
## LEZIONE DI LABORATORIO 002:
#### DNS
- Il DNS (Domain Name System) è uno degli elementi costitutivi e fondamentali di Internet, che costituisce il database di informazioni, globale e distribuito, che è responsabile della traduzione dei nomi simbolici in indirizzi (e viceversa), dell'instradamento della posta alla destinazione corretta e di molti altri servizi.
- E' lo schema mediante il quale milioni di Host Internet collaborano per rispondere alla domanda su come il nome Host si risolva in indirizzi IPv4 oppure IPv6 (nel caso sia utilizzata).

#### Resolver
- Il Resolver è la parte client del sistema client/server DNS, che pone le domande sugli "hostnames".
- Di solito si tratta di una piccola libreria compilata in qualsiasi linguaggio, che richiede i servizi DNS e conosce quello che basta per inviare una query a un nameserver vicino. 
- Solitamente sono delle strutture molto semplici, che si appoggiano ai server per svolgere il lavoro più pesante.

#### Nameserver (generico) 
- Si tratta di un server software, che risponde alle query DNS.
- Potrebbe conoscere già la risposta (in questo caso si dice che è "AUTORITATIVO"), oppure potrebbe dover andare su Internet e chiedere in giro per trovare la risposta (in questo caso, si dice che è "RICORSIVO").

#### Nameserver Ricorsivo
- Un "Resolver Ricorsivo" è la prima fermata in una query DNS.
- Si tratta di un server software, che funge da intermediario tra un client e un Nameserver DNS.
- Dopo aver ricevuto una query DNS, risponde con i dati memorizzati nella cache, oppure invierà una richiesta ad un "ROOT NAMESERVER", seguita da una richiesta ad un "TLD NAMESERVER" e da un'ultima richiesta al "NAMESERVER AUTORITATIVO", il quale fornirà l'indirizzo IP richiesto. Il Recursive Nameserver invierà poi questa risposta al client. 

#### Nameserver Autoritativo
- Per ogni zona, qualcuno deve mantenere un file contenente le associazioni Hostname e indirizzi IP.
- Questa funzione amministrativa viene eseguita da un umano e il file è contenuto su una macchina, chiamata "ZONE MASTER".

#### Registro delle risorse
- Si potrebbe pensare che il DNS fornisca solamente la mappatura Hostname-IP, ma in realtà ci sono altri tipi di query che possono essere poste ad un DNS.
- Il DNS è in realtà un Database ricco di risorse.
- Il tipo più comune di registro è il tipo `A`, ovvero quello degli indirizzi IP (viene utilizzato un Hostname per ricevere un indirizzo IPv4), ma esistono anche altri tipi di record, ad esempio quelli di tipo `AAAA` (che invece di fornire un IPv4, fornisce un indirizzo IPv6), quelli di tipo `MX` (che maneggiano e gestiscono le email per il dominio specificato) e altri ancora. 

#### Query flow
1) Il sistema operativo tenta di risolvere localmente l'indirizzo, cercando nella chache locale. Se la risposta non è disponibile, allora effettua una richiesta al RECURSIVE SERVER, che controlla la sua cache.
2) Se il Recursive Server non trova il record, effettua una richiesta per nostro conto ad uno qualsiasi dei 13 ROOT SERVER.
3) Se il Root Server non conosce la risposta alla nostra richiesta, invia un record al nostro RECURSIVE SERVER, con un elenco dei "Global Top Level Domain" (GTLD), ovvero i server responsabili di un dominio (ad esempio `.com`, `.net`, `.org`, ...).
4) Il Recursive Server, utilizzando la risposta del Root Server, sceglie a caso uno dei SERVER AUTORITATIVI GLTD e invia la stessa query. Se il server non conosce la risposta specifica alla nostra domanda, restituisce un `referral` (un set di record) ad un altro server, che con buona probabilità conosce la risposta.
5) Il Recursive Server, seguendo una catena di risposte per conto del client, sceglie a caso uno dei nameserver e invia una terza query, uguale alle altre due.
6) Ora che ha la risposta, il Recursive Nameserver dell'ISP, consegna la risposta al client e soddisfa la query. Il Recursive Nameserver archivia questa risposta nella propria cache (nel caso in cui questo o qualche altro client effettui la stessa query in un altro momento).

#### --- Osservazione (1)
Se la risposta non viene trovata entro un certo periodo, allora per evitare di essere continuamente sbalzati in giro fra i server, ci viene detto che è finito il tempo massimo disponibile per la ricerca e ci viene detto che quell'indirizzo non esiste.

#### DNS in Python
- Bisogna scaricare e utilizzare la libreria `dns.resolver`.
- La funzione realizzata a laboratorio della query DNS, accetta il nome di dominio come parametro, eseguendo la query DNS mediante il comando `.resolve()`, per ottenere gli indirizzi IP associati al dominio (stampando quelli ottenuti).
- Bisogna gestire le eccezioni attraverso gli Except Blocks, tramite il comando `except`, per gestire tutti i casi in cui si possono verificare delle risposte di errore o non contenenti la risposta desiderata (il tutto, successivo al comando `try`, che esprime il comando di provare a fare quella serie di istruzioni, vedendo se si incappa in delle eccezioni).

#### --- Osservazione (2)
La nostra macchina non ha in cache l'indirizzo di www.google.com, chiede quindi al server locale, poi lo chiede al root server, poi manda un IP che indirizza ad un altro server, altrimenti se questo non ha la risposta risponde con il nome del server autoritativo (ovvero .com), che se non ha l'indirizzo, allora non esiste, lo restituisce al nostro Nameserver ISP e ce lo fornisce.

#### Query DNS Inversa
- `Ip look up` ci fornisce i nomi simbolici relativi ad un indirizzo IP specificato, ovvero fa la così detta "Query inversa".
- La risoluzione DNS inversa (rDNS) è la determinazione di un nome di dominio associato ad un indirizzo IP, tramite l'interrogazione del DNS.
- Le ricerche inverse per gli indirizzi IPv4, utilizzano il dominio speciale `in-addr.arpa`, in cui un indirizzo è rappresentato come una sequenza concatenata di quattro numeri decimali, separati da punti, a cui è aggiunto il suffisso di dominio di secondo livello `.in-addr.arpa` (i numeri decimali si ottengono dividendo l'indirizzo a 32 bit, in quattro porzioni da 8 bit e convertendo ciascuna porzione in un valore decimale).  
- Immaginiamoci di avere un indirizzo IP (143.50.23.2), l'elemento MENO SIGNIFICATIVO è quello più a sinistra, mentre quello PIU' SIGNIFICATIVO sta a destra. 
- Per fare la query inversa faccio il processo inverso, capovolgendo l'indirizzo (2.23.50.143) e vado a prendere il valore "[0]", perchè il risultato della operazione è una lista di di tutti i nomi simbolici associati ad uno stesso indirizzo IP (pensiamo a quanti siti si possono visitare utilizzando svariati nomi per lo stesso indirizzo, ad esempio TIM.it, oppure TelecomItalia.it).
- Si utilizza il metodo `reversename.from_address('IP_ADDRESS')`, dovendo importare `dns.reversename`.

#### LDAP
- Acronimo di Lightweight Directory Access Protocol, è un protoccollo di rete utilizzato per accedere e gestire le informazioni memorizzate in un servizio directory (ovvero una struttura di archiviazione che memorizza dati come: nomi, indirizzi, ...). 
- LDAP è leggero, perchè è progettato per essere efficiente in termini di risorse e semplice da implementare. 
- Viene spesso utilizzato per autenticazione, ricerca e recupero di informazioni di utenti e risorse in una rete.
- Descrizione di un'interazione classica tra client e server LDAP:
    1) CONNESSIONE: Il client LDAP stabilisce una connessione TCP/IP con il server LDAP (il protocollo LDAP utilizza la porta 389 per le connessioni non crittografate e la porta 636, per crittografia tramite SSL/TLS)
    2) AUTENTICAZIONE: Se richiesta, il client si autentica presso il server LDAP (può essere fatto tramite diversi meccanismi di autenticazione, come le credenziali di base, certificati client, ...).
    3) OPERAZIONI DI RICERCA/MODIFICA: Dopo aver stabilito la connessione e l'autenticazione, il client può inviare varie operazioni al server LDAP (le operazioni più comuni sono quelle di `RICERCA`, dove il client invia una query di ricerca, specificando la base di ricerca, il filtro e gli attributi da recuperare, di `AGGIUNTA`, dove il client invia una richiesta per aggiungere un nuovo oggetto alla directory LDAP, oppure di `ELIMINAZIONE`, dove il client invia una richiesta per eliminare un oggetto dalla directory).
    4) RISPOSTA DEL SERVER: Il server LDAP elabora le richieste ricevute dal client e invia le risposte appropriate (le risposte contengono i risultati delle operazioni richieste dal client).
    5) CHIUSURA DELLA CONNESSIONE: Alla fine dell'interazione, il client e il server LDAP, possono decidere di chiudere la connessione (solitamente dopo che tutte le operazioni richieste sono state completate con successo o in caso di errore).
- In Python viene utilizzata la libreria `ldap`, per eseguire la ricerca LDAP.

#### Traceroute (Tracert)
- Si tratta di un Programma diagnostico, tramite il quale, scegliendo un server, inserito l'indirizzo IP dell'host di destinazione e dando invio, il server invia un certo numero di pacchetti speciali verso tale destinazione. Questi pacchetti attraversano vari router, quando un router ne riceve uno, invia un breve messaggio che torna all'origine (messaggio contenente il nome e l'IP adress del router che l'ha inviato). Ripete l'operazione per 3 volte consecutive.
- Garantisce che ad ogni salto nel percorso verso un dispositivo destinazione, venga rilasciato un pacchetto e venga restituito un messaggio di errore ICMP (in questo modo è in grado di misurare quando tempo passa tra il momento in cui i dati vengono inviati e il momento in cui il messaggio ICMP viene ricevuto di nuovo, per ogni hop, fornendo il valore RTT per ogni hop).

#### TTL (Time To Live)
- Il TTL limita la durata massima della vita dei dati in una rete IP.
- Ad ogni pacchetto dati, viene assegnato un valore TTL, dove ogni volta che il pacchetto raggiunge un salto, il valore TTL viene diminuito di uno (quando arriva a 0, vuol dire che il suo tempo di vita è terminato, nel caso in cui non sia arrivato a destinazione in tempo).
- indica il numero massimo di Hop (ovvero di Step) che può compiere per riuscire a giungere all'indirizzo destinatario specificato. 
- Indica il numero di Router che può passare per arrivare all'indirizzo di destinazione. 

#### RTT (Round Trip Time)
- Rappresenta il tempo di andata e di ritorno di un pacchetto di una rete IP.




