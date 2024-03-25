# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 21:48:32 2024

@author: mpagg
"""

# TEST DI RISOLUZIONE DEL NOME DI DOMINIO
print("\n-------------------------- PARTE 1 -----------------------------------\n")
import dns.resolver
def query_dns(domain_name):
    try:
        # Eseguire la query DNS per ottenere gli indirizzi IP legati al nome
        answers = dns.resolver.resolve(domain_name, 'A')
        
        # Stampare gli indirizzi IP ottenuti
        for answer in answers:
            print("Indirizzo IP per", domain_name, ":", answer.address)
    # Caso in cui il nome simbolico non esiste
    except dns.resolver.NXDOMAIN:
        print("Il dominio", domain_name,"non esiste")
    # Caso in cui non ci sono record associati a tale dominio
    except dns.resolver.NoAnswer:
        print("Non ci sono record associati al dominio", domain_name)
    # Caso in cui la query DNS è stata mandata avanti troppo a lungo
    except dns.resolver.Timeout:
        print("La query DNS per", domain_name,"è scaduta")
    # Caso in cui non ci sono server DNS disponibili per rispondere
    except dns.resolver.NoNameservers:
        print("Nessun server DNS disponibile per risolvere il dominio", domain_name)
        
# Utilizzo
domain_name = "google.com"
query_dns(domain_name)


# TEST DELLA QUERY INVERSA
print("\n-------------------------- PARTE 2 -----------------------------------\n")
from dns import reversename
from dns import resolver
# Indirizzo del dominio (controllare la presenza di in-addr.arpa)
domain_address = reversename.from_address('8.8.4.4')
print("Il domain address è:", domain_address)
# Indirizzo IPv4
ip_address = reversename.to_address(domain_address)
print("L'ip address è:", ip_address)
# Nome del dominio come risposta alla query inversa
## Viene preso il valore di indice 0, perchè per uno stesso indirizzo IP
## possono esserci più nomi di dominio collegati (a noi ne interessa 1 dei tanti)
domain_name = str(resolver.resolve(domain_address, 'PTR')[0])
print("Il nome di dominio è:", domain_name)


# TEST DEL FUNZIONAMENTO DELLA RICERCA LDAP
print("\n-------------------------- PARTE 3 -----------------------------------\n")
import ldap
def ldap_search():
    ldap_server = "ldap.forumsys.com"
    ldap_conn = ldap.initialize("ldap://" + ldap_server)
    
    # Bind con l'utente e password specificati
    ldap_conn.simple_bind_s("uid=tesla,dc=example,dc=com", "password")
    
    # Definizione della base di ricerca
    base_dn = "dc=example,dc=com"
    
    # Creazione della query di ricerca
    search_filter = "(objectclass=*)"
    
    # Esecuzione della ricerca
    result = ldap_conn.search_s(base_dn, ldap.SCOPE_SUBTREE, search_filter)
    
    # Chiusura connessione
    ldap_conn.unbind()
    
    return result

# Esempio di utilizzo
search_result = ldap_search()
for dn, entry in search_result:
    print("DN:", dn)
    print("Entry:", entry)