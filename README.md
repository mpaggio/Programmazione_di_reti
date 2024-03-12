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




