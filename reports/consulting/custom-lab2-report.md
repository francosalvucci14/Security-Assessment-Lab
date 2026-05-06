# Security Assessment Report – VDSI Lab

**Author:** Franco Salvucci  
**Date:** 26/06/2024  
**Environment:** Academic Lab (Custom Machine)  
**Target:** 10.0.2.4 - vdsi.com  

---

## 1. Executive Summary

Durante l’attività di security assessment sono state identificate vulnerabilità critiche che consentono a un attaccante di ottenere accesso completo al sistema.

La catena di attacco include:
- Remote Code Execution tramite vulnerabilità in plugin WordPress
- Lettura di dati sensibili tramite format string vulnerability
- Privilege escalation tramite Python library hijacking

**Impatto:** compromissione completa del sistema  
**Livello di rischio:** Critico  

---

## 2. Scope

- Target: vdsi.com  
- Servizi esposti:
  - SSH (22)
  - HTTP (80)  
- Applicazione web: WordPress  

---

## 3. Methodology

L’attività è stata condotta seguendo un approccio strutturato:

1. Reconnaissance  
2. Enumeration  
3. Exploitation  
4. Privilege Escalation  
5. Post-Exploitation  

Strumenti utilizzati:
- Nmap
- gobuster  
- exploit pubblico (wpDiscuz)  
- pspy64 

---

## 4. Findings

### 4.1 Remote Code Execution – WordPress Plugin (wpDiscuz)

**Severity:** Critical  
**CVE:** CVE-2020-24186  

#### Descrizione
È stata identificata una vulnerabilità RCE nel plugin WordPress wpDiscuz che consente l’upload di file malevoli e l’esecuzione di codice remoto.

#### Evidenza
- Plugin identificato tramite robots.txt  
- Presenza endpoint WordPress esposti  
- Versione vulnerabile individuata  

#### Exploitation
È stato utilizzato un exploit pubblico per ottenere una webshell sfruttando un post esistente.

#### Impatto
- Esecuzione di codice remoto  
- Accesso al sistema come utente web server  

#### Mitigazione
- Aggiornare plugin WordPress  
- Limitare upload file  
- Applicare controlli lato server  

---

### 4.2 Sensitive Information Disclosure via Format String Vulnerability

**Severity:** High  

#### Descrizione
Un binario con SUID attivo contiene una vulnerabilità di format string che permette la lettura di dati sensibili dalla memoria.

#### Evidenza
- Uso di `printf` con input utente non sanitizzato  
- Accesso a file contenente password (`/home/damian/password.txt`)  

#### Exploitation
È stato possibile leggere la memoria dello stack utilizzando specificatori di formato (`%lx`) per estrarre la password dell’utente damian.

#### Impatto
- Accesso a credenziali sensibili  
- Movimento laterale nel sistema  

#### Mitigazione
- Validare input utente  
- Evitare uso diretto di printf con input non controllato  
- Rimuovere SUID da binari non necessari  

---

### 4.3 Privilege Escalation – Python Library Hijacking

**Severity:** Critical  

#### Descrizione
Uno script Python eseguito con privilegi elevati importa librerie senza specificare percorsi assoluti, rendendolo vulnerabile a library hijacking.

#### Evidenza
- Script `/home/damian/scripts/backup.py`  
- Esecuzione automatica tramite cronjob  

#### Exploitation
È stato possibile creare una libreria malevola con lo stesso nome di quella importata e ottenere esecuzione di codice con privilegi root.

#### Impatto
- Escalation completa a root  

#### Mitigazione
- Utilizzare percorsi assoluti per import Python  
- Limitare esecuzione di script privilegiati  
- Controllare PATH e environment  

---

## 5. Attack Chain

1. Scansione porte (22, 80)  
2. Enumerazione WordPress  
3. Identificazione plugin vulnerabile  
4. Exploit RCE → accesso web shell  
5. Analisi binario SUID  
6. Exploit format string → recupero password  
7. Accesso SSH come damian  
8. Analisi cronjob  
9. Library hijacking → root  

---

## 6. Conclusion

Il sistema presenta vulnerabilità critiche su più livelli:

- vulnerabilità applicative (WordPress)  
- vulnerabilità a livello binario (format string)  
- configurazioni insicure del sistema (cronjob + Python imports)  

Queste vulnerabilità, combinate, permettono una compromissione completa del sistema.

Si raccomanda:
- aggiornamento continuo dei software  
- revisione del codice applicativo  
- hardening dei sistemi  

---

## 7. Appendix

### Tecniche utilizzate
- Web exploitation  
- Format string exploitation  
- Reverse engineering  
- Library hijacking  

### Note
Dettagli tecnici completi disponibili nella directory [labs-custom2](/labs/Custom/custom-2/).
