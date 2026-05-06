# Security Assessment Report – Bizness

**Author:** Franco Salvucci  
**Date:** 19/10/2024  
**Environment:** HackTheBox Lab  
**Target:** bizness.htb  

---

## 1. Executive Summary

Durante l’attività di security assessment sono state identificate vulnerabilità critiche che consentono l’esecuzione di codice remoto e la compromissione completa del sistema.

La catena di attacco include:
- Remote Code Execution non autenticata su Apache OFBiz tramite vulnerabilità di deserializzazione Java
- Accesso iniziale al sistema tramite reverse shell
- Estrazione e cracking di credenziali dal database Apache Derby
- Accesso diretto come root tramite credenziali recuperate

**Impatto:** compromissione completa del sistema  
**Livello di rischio:** Critico  

---

## 2. Scope

- Target: bizness.htb  
- Servizi esposti:
  - SSH (22)
  - HTTP (80)
  - HTTPS (443)
- Applicazione: Apache OFBiz  

---

## 3. Methodology

L’attività è stata condotta seguendo un approccio strutturato:

1. Reconnaissance  
2. Enumeration  
3. Exploitation  
4. Post-Exploitation  
5. Privilege Escalation  

Strumenti utilizzati:
- Nmap
- ffuf
- exploit Java deserialization  
- netcat  

---

## 4. Findings

### 4.1 Unauthenticated Remote Code Execution – Apache OFBiz

**Severity:** Critical  
**CVE:** CVE-2023-49070 / CVE-2023-51467  

#### Descrizione
L’applicazione Apache OFBiz è vulnerabile a una deserializzazione Java non sicura tramite endpoint XML-RPC, che consente a un attaccante non autenticato di eseguire codice remoto.

#### Evidenza
- Endpoint vulnerabile:
  `/webtools/control/xmlrpc`
- Versione OFBiz vulnerabile (18.12)

#### Exploitation
È stato utilizzato un exploit pubblico che invia payload serializzati malevoli per ottenere esecuzione di codice remoto. 
`python3 exploit.py --url https://bizness.htb --cmd 'CMD'` 

#### Impatto
- Remote Code Execution senza autenticazione  
- Accesso iniziale al sistema  

#### Mitigazione
- Aggiornare Apache OFBiz  
- Disabilitare XML-RPC non necessario  
- Validare input serializzati  

---

### 4.2 Initial Foothold – Reverse Shell

**Severity:** Critical  

#### Descrizione
Dopo l’exploit RCE, è stato possibile ottenere una reverse shell sul sistema target.

#### Evidenza
- Esecuzione comandi arbitrari tramite payload  
- Connessione reverse shell stabilita  

#### Impatto
- Accesso al sistema come utente applicativo (ofbiz)  
- Possibilità di enumerazione interna  

#### Mitigazione
- Monitorare attività anomale  
- Limitare esecuzione comandi lato server  

---

### 4.3 Credential Exposure – Apache Derby Database

**Severity:** High  

#### Descrizione
Le credenziali utente sono memorizzate nel database Apache Derby e accessibili dopo compromissione iniziale.

#### Evidenza
- Accesso ai file/configurazioni OFBiz  
- Estrazione hash password dal database  

#### Exploitation
Gli hash sono stati convertiti e crackati utilizzando strumenti standard, ottenendo credenziali valide. 

#### Impatto
- Accesso completo al sistema  
- Possibile riutilizzo credenziali  

#### Mitigazione
- Proteggere accesso al database  
- Utilizzare hashing robusto e salt adeguati  
- Implementare access control  

---

### 4.4 Privilege Escalation – Root Credential Reuse

**Severity:** Critical  

#### Descrizione
Le credenziali ottenute dal database consentono accesso diretto come utente root.

#### Evidenza
- Password crackata associata all’utente root  
- Accesso SSH riuscito  

#### Impatto
- Compromissione completa del sistema  

#### Mitigazione
- Separare credenziali tra servizi  
- Evitare riutilizzo password  
- Implementare least privilege  

---

## 5. Attack Chain

1. Scansione porte (22, 80, 443)  
2. Identificazione Apache OFBiz  
3. Ricerca vulnerabilità note (CVE)  
4. Exploit deserializzazione → RCE  
5. Reverse shell → accesso iniziale  
6. Enumerazione sistema e database  
7. Estrazione hash credenziali  
8. Cracking password  
9. Accesso root  

---

## 6. Conclusion

Il sistema presenta vulnerabilità critiche a livello applicativo e di gestione delle credenziali:

- software vulnerabile (Apache OFBiz)  
- esposizione di servizi non sicuri  
- gestione inadeguata delle password  

La combinazione di queste vulnerabilità consente una compromissione completa con basso sforzo.

Si raccomanda:
- aggiornamento continuo del software  
- revisione delle configurazioni  
- adozione di politiche di sicurezza per le credenziali  

---

## 7. Appendix

### Tecniche utilizzate
- Java deserialization exploitation  
- Remote Code Execution  
- Database enumeration  
- Password cracking  

### Note
Dettagli tecnici completi disponibili nella directory [labs-bizness](/labs/HTB/Bizness/).