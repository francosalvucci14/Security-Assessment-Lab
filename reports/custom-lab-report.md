# Security Assessment Report – Custom Internal Lab

**Author:** Franco Salvucci  
**Date:** 10/08/2024  
**Environment:** Academic Lab (Custom Machine) a.k.a Robot 
**Target:** 10.0.2.5  

---

## 1. Executive Summary

Durante l’attività di security assessment sono state identificate vulnerabilità critiche che consentono la compromissione completa del sistema.

La catena di attacco include:
- Reverse engineering di un binario per ottenere credenziali
- Code injection tramite uso insicuro di eval() in applicazione web
- Privilege escalation tramite wildcard injection in rsync eseguito via cron

**Impatto:** compromissione completa del sistema  
**Livello di rischio:** Critico  

---

## 2. Scope

- Target: 10.0.2.5  
- Servizi esposti:
  - SSH (22)
  - HTTP (80)
  - HTTPS (443)
  - Web services (8080, 8081, 8082)

---

## 3. Methodology

L’attività è stata condotta secondo un approccio strutturato:

1. Reconnaissance
2. Enumeration
3. Reverse Engineering
4. Exploitation
5. Privilege Escalation

Strumenti utilizzati:
- Nmap
- rsync
- gobuster  
- netcat  

---

## 4. Findings

### 4.1 Credential Disclosure via Reverse Engineering

**Severity:** High  

#### Descrizione
Un file binario accessibile pubblicamente (`/connector`) contiene logica di cifratura delle credenziali. Analizzando il binario è possibile recuperare i dati necessari per decifrare username e password.

#### Evidenza
- Analisi del binario con Ghidra
- Identificazione funzione `cryptHelper`
- Estrazione di variabili globali contenenti dati cifrati

#### Exploitation
I valori XOR sono stati estratti e utilizzati in uno script Python per ottenere credenziali in chiaro:

- Username: developer  
- Password: [REDACTED]

#### Impatto
- Accesso autenticato ai servizi interni

#### Mitigazione
- Non esporre binari contenenti logica sensibile
- Utilizzare cifratura robusta
- Evitare hardcoding di credenziali

---

### 4.2 Code Injection via Unsafe eval()

**Severity:** Critical  

#### Descrizione
L’applicazione web utilizza la funzione `eval()` su input utente non sanitizzato, rendendola vulnerabile a code injection.

#### Evidenza
- Analisi del codice lato client
- Identificazione uso di eval()

#### Exploitation
È stato possibile eseguire codice arbitrario: `import('os').system(...)`

ottenendo una reverse shell sul sistema.

#### Impatto
- Remote Code Execution
- Accesso come utente applicativo

#### Mitigazione
- Non utilizzare eval() su input utente
- Implementare validazione input
- Usare parsing sicuro

---

### 4.3 Privilege Escalation via rsync Wildcard Injection

**Severity:** Critical  

#### Descrizione
Uno script eseguito tramite cron utilizza il comando `rsync -a *`, permettendo wildcard injection.

#### Evidenza
- Presenza script `/backup.sh`
- Uso wildcard non sanitizzata

#### Exploitation
È stato possibile iniettare parametri malevoli e ottenere esecuzione di codice come root.

#### Impatto
- Escalation a privilegi root

#### Mitigazione
- Evitare uso di wildcard non controllate
- Validare input
- Usare percorsi espliciti

---

## 5. Attack Chain

1. Scansione rete e individuazione target  
2. Enumerazione servizi web  
3. Download e reverse engineering del binario  
4. Recupero credenziali  
5. Accesso a virtual host protetto  
6. Code injection tramite eval()  
7. Reverse shell → utente locale  
8. Exploit wildcard rsync → root  

---

## 6. Conclusion

Il sistema presenta vulnerabilità critiche in più livelli:

- esposizione di logica applicativa sensibile  
- uso insicuro di funzioni dinamiche  
- configurazioni di sistema errate  

La combinazione di queste vulnerabilità consente una compromissione completa con sforzo moderato.

---

## 7. Appendix

### Tecniche utilizzate
- Reverse engineering (XOR decoding)
- Code injection
- Wildcard exploitation

### Note
Dettagli tecnici completi disponibili nella directory [labs-custom1](/labs/Custom/custom-1/).