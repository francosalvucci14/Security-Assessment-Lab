# Security Assessment Report – PermX

**Author:** Franco Salvucci  
**Date:** [inserisci data]  
**Environment:** HackTheBox Lab  
**Target:** 10.10.11.23  

---

## 1. Executive Summary

Durante l’attività di security assessment sono state identificate vulnerabilità critiche che consentono a un attaccante non autenticato di ottenere accesso completo al sistema.

In particolare:
- Una vulnerabilità Remote Code Execution (CVE-2023-4220) su Chamilo LMS ha permesso accesso iniziale
- Credenziali in chiaro hanno facilitato il movimento laterale
- Una configurazione errata dei permessi ha consentito privilege escalation a root

**Impatto:** compromissione completa del sistema  
**Livello di rischio:** Critico  

---

## 2. Scope

- Target: 10.10.11.23  
- Servizi esposti:
  - SSH (22)
  - HTTP (80)  
- Applicazione web: Chamilo LMS  

---

## 3. Methodology

L’attività è stata condotta seguendo le seguenti fasi:

1. Reconnaissance
2. Enumeration
3. Exploitation
4. Privilege Escalation
5. Post-Exploitation

Strumenti utilizzati:
- Nmap
- ffuf
- gobuster
- linPEAS

---

## 4. Findings

### 4.1 Remote Code Execution – Chamilo LMS

**Severity:** Critical  
**CVE:** CVE-2023-4220  

#### Descrizione
È stata identificata una vulnerabilità RCE nella piattaforma Chamilo LMS che consente l’upload di file arbitrari e l’esecuzione di codice remoto.

#### Evidenza
- Versione vulnerabile identificata tramite directory `/documentation`
- Endpoint vulnerabile:
  `/main/inc/lib/javascript/bigupload/`

#### Exploitation
È stato utilizzato un exploit pubblico per caricare una webshell e ottenere accesso come utente `www-data`.

#### Impatto
- Accesso remoto non autenticato
- Esecuzione di codice sul server

#### Mitigazione
- Aggiornare Chamilo a versione sicura (> 1.11.24)
- Limitare upload non autenticati

---

### 4.2 Hardcoded Credentials

**Severity:** High  

#### Descrizione
Credenziali del database sono state trovate in chiaro nei file di configurazione.

#### Evidenza
File:
- `/var/www/chamilo/app/config/configuration.php`

Credenziali:
- user: chamilo
- password: [REDACTED]

#### Impatto
- Accesso al database
- Possibile riutilizzo credenziali

#### Mitigazione
- Rimuovere credenziali hardcoded
- Utilizzare secret management

---

### 4.3 Privilege Escalation – Misconfigured ACL Script

**Severity:** Critical  

#### Descrizione
Un utente locale può eseguire uno script con privilegi elevati che consente la modifica degli ACL su file sensibili.

#### Evidenza
Comando: `sudo -l`

Script: `/opt/acl.sh`


#### Exploitation
È stato possibile modificare i permessi dei file `/etc/passwd` e `/etc/shadow`, creando un utente con privilegi root.

#### Impatto
- Compromissione completa del sistema

#### Mitigazione
- Limitare l’uso di sudo
- Validare input negli script
- Evitare operazioni su file critici

---

## 5. Attack Chain

1. Scansione porte (22, 80)
2. Enumerazione web e vhost
3. Identificazione Chamilo LMS
4. Exploit RCE → accesso www-data
5. Recupero credenziali
6. Accesso SSH
7. Privilege escalation → root

---

## 6. Conclusion

Il sistema presenta vulnerabilità critiche che permettono la compromissione completa tramite una catena di attacco relativamente semplice.

Le principali criticità includono:
- Software non aggiornato
- Credenziali esposte
- Configurazioni insicure

Si raccomanda l’adozione di pratiche di sicurezza più rigorose, tra cui patch management e hardening dei sistemi.

---

## 7. Appendix

### Comandi principali
- nmap -sC -sV
- gobuster dir
- ffuf vhost fuzzing

### Note
Dettagli tecnici completi disponibili nella directory labs.