# Security Assessment Report – Devvortex

**Author:** Franco Salvucci  
**Date:** 08/04/2024  
**Environment:** HackTheBox Lab  
**Target:** devvortex.htb  

---

## 1. Executive Summary

Durante l’attività di security assessment sono state identificate vulnerabilità critiche che consentono la compromissione completa del sistema.

La catena di attacco include:
- Information Disclosure non autenticata su Joomla CMS
- Accesso amministrativo e Remote Code Execution tramite template injection
- Recupero credenziali dal database e accesso SSH
- Privilege escalation tramite vulnerabilità in apport-cli (CVE-2023-1326)

**Impatto:** compromissione completa del sistema  
**Livello di rischio:** Critico  

---

## 2. Scope

- Target: devvortex.htb  
- Servizi esposti:
  - SSH (22)
  - HTTP (80)  
- Applicazione web: Joomla CMS  

---

## 3. Methodology

L’attività è stata condotta seguendo un approccio strutturato:

1. Reconnaissance  
2. Enumeration  
3. Exploitation  
4. Lateral Movement  
5. Privilege Escalation  

Strumenti utilizzati:
- Nmap
- ffuf  
- curl  
- bash
- netcat  

---

## 4. Findings

### 4.1 Unauthenticated Information Disclosure – Joomla

**Severity:** Critical  
**CVE:** CVE-2023-23752  

#### Descrizione
Una vulnerabilità di information disclosure permette a un utente non autenticato di ottenere informazioni sensibili di configurazione, incluse credenziali del database.

#### Evidenza
Endpoint vulnerabile: `/api/index.php/v1/config/application?public=true`


#### Exploitation
È stata effettuata una richiesta HTTP che ha restituito credenziali in chiaro:

- Username: lewis  
- Password: [REDACTED]

#### Impatto
- Accesso amministrativo all’applicazione Joomla  
- Esposizione completa della configurazione  

#### Mitigazione
- Aggiornare Joomla a una versione non vulnerabile  
- Limitare accesso agli endpoint API  
- Proteggere configurazioni sensibili  

---

### 4.2 Remote Code Execution – Template Injection

**Severity:** Critical  

#### Descrizione
Con accesso amministrativo, è possibile modificare i template Joomla per eseguire codice PHP arbitrario.

#### Evidenza
- Modifica file `error.php` nel template Cassiopeia  
- Inserimento payload PHP  

#### Exploitation
È stato iniettato codice PHP per ottenere una reverse shell tramite esecuzione remota.

#### Impatto
- Accesso remoto come utente web server (`www-data`)  
- Controllo del sistema  

#### Mitigazione
- Limitare accesso amministrativo  
- Monitorare modifiche ai template  
- Disabilitare esecuzione codice non necessario  

---

### 4.3 Credential Exposure via Database

**Severity:** High  

#### Descrizione
Le credenziali utente sono memorizzate nel database e accessibili dopo compromissione iniziale.

#### Evidenza
- Accesso al database MySQL tramite credenziali recuperate  
- Dump tabella utenti  

#### Exploitation
È stato ottenuto un hash bcrypt per l’utente `logan`, successivamente crackato offline.

#### Impatto
- Accesso SSH al sistema  
- Movimento laterale  

#### Mitigazione
- Applicare politiche di password robuste  
- Limitare accesso al database  
- Monitorare accessi sospetti  

---

### 4.4 Privilege Escalation – apport-cli

**Severity:** Critical  
**CVE:** CVE-2023-1326  

#### Descrizione
L’utente può eseguire `apport-cli` con privilegi elevati tramite sudo. Il tool invoca un pager che consente esecuzione di comandi arbitrari.

#### Evidenza
Comando: `sudo -l`

Permesso: `/usr/bin/apport-cli`


#### Exploitation
È stato possibile sfruttare il pager (`less`) per eseguire `/bin/bash` e ottenere una shell root.

#### Impatto
- Escalation completa a root  

#### Mitigazione
- Limitare uso di sudo  
- Aggiornare apport-cli  
- Disabilitare accesso a pager interattivi  

---

## 5. Attack Chain

1. Enumerazione servizi web  
2. Identificazione Joomla CMS  
3. Exploit Information Disclosure  
4. Accesso amministrativo  
5. Template injection → RCE  
6. Accesso sistema (www-data)  
7. Accesso database → hash utenti  
8. Crack password → accesso SSH  
9. Exploit apport-cli → root  

---

## 6. Conclusion

Il sistema presenta vulnerabilità critiche su più livelli:

- vulnerabilità applicative (Joomla)  
- gestione insicura delle credenziali  
- configurazioni errate di privilegi  

Queste vulnerabilità, combinate, permettono una compromissione completa con bassa complessità.

Si raccomanda:
- aggiornamento software  
- hardening dei privilegi  
- monitoraggio accessi  

---

## 7. Appendix

### Tecniche utilizzate
- Web exploitation  
- Credential harvesting  
- Password cracking  
- Privilege escalation  

### Note
Dettagli tecnici completi disponibili nella directory [labs-devvortex](/labs/HTB/Devvortex/).