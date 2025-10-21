import hashlib
import os
import sys

MASTER_FILE = "mpwd.txt"

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def mdp_hash(master, tag, n):
    combined = master + tag
    bite_combined = combined.encode('utf-8')
    hash_object = hashlib.sha256(bite_combined).hexdigest()
    final_password = hash_object[:n]
    return final_password

def print_error(message):
    print(f"{Colors.FAIL}Erreur : {message}{Colors.ENDC}")

def set_new_master_password():
    while True:
        try:
            new_master = input(f"{Colors.CYAN}Veuillez définir un nouveau mot de passe maître : {Colors.ENDC}")
        except (EOFError, KeyboardInterrupt):
            print(f"\n{Colors.WARNING}Opération annulée. Au revoir !{Colors.ENDC}")
            sys.exit(0)

        if " " in new_master:
            print_error("Le mot de passe maître ne doit pas contenir d'espaces.")
        elif not new_master:
            print_error("Le mot de passe maître ne peut pas être vide.")
        else:
            try:
                with open(MASTER_FILE, "w", encoding="utf-8") as f:
                    f.write(new_master)
                print(f"{Colors.GREEN}Nouveau mot de passe maître enregistré dans {MASTER_FILE}.{Colors.ENDC}")
                return new_master
            except IOError as e:
                print_error(f"Erreur critique lors de l'écriture du fichier : {e}")
                return None

def get_master_password():
    master_password = None
    
    # on vérifie d'abord si le fichier existe
    file_exists = os.path.exists(MASTER_FILE)

    if file_exists:
        try:
            change_request = input(f"{Colors.WARNING}Voulez-vous changer le mot de passe maître ? (o/n) : {Colors.ENDC}").lower().strip()
            if change_request == 'o':
                master_password = set_new_master_password()
                return master_password
        except (EOFError, KeyboardInterrupt):
            print(f"\n{Colors.WARNING}Opération annulée. Au revoir !{Colors.ENDC}")
            sys.exit(0)

    if master_password is None:
        try:
            with open(MASTER_FILE, "r", encoding="utf-8") as f:
                master_password = f.read().strip()

            if not master_password:
                print(f"{Colors.WARNING}Le fichier {MASTER_FILE} est vide.{Colors.ENDC}")
                master_password = set_new_master_password()
            else:
                print(f"{Colors.GREEN}Mot de passe maître chargé depuis le fichier.{Colors.ENDC}")
        except FileNotFoundError:
            print(f"{Colors.WARNING}Aucun fichier {MASTER_FILE} trouvé.{Colors.ENDC}")
            master_password = set_new_master_password()
        except IOError as e:
            print_error(f"Erreur lors de la lecture du fichier : {e}")
            return None

    return master_password

def get_password_length():
    while True:
        try:
            user_input = input(f"{Colors.CYAN}Entrez la longueur souhaitée pour le mot de passe (entre 1 et 12) : {Colors.ENDC}")
            length = int(user_input)

            if 1 <= length <= 12:
                return length
            else:
                print_error("Le nombre doit être compris entre 1 et 12.")

        except ValueError:
            print_error("Veuillez entrer un nombre entier valide.")
        
            
def display_header():
    print(f"{Colors.HEADER}{Colors.BOLD}")
    print("╔" + "═" * 50 + "╗")
    print("║" + " " * 11 + "GÉNÉRATEUR DE MOTS DE PASSE" + " " * 12 + "║")
    print("╚" + "═" * 50 + "╝")
    print(f"{Colors.ENDC}")

def display_result(master, tag, length, password):
    master_hidden = '*' * len(master)
    print(f"\n{Colors.GREEN}{Colors.BOLD}Voici le résultat de la génération :{Colors.ENDC}")
    print(f"{Colors.BLUE}╔" + "═" * 50 + "╗")
    print(f"║ {Colors.ENDC}Mot de passe maître (caché) : {master_hidden:<18}{Colors.BLUE} ║")
    print(f"║ {Colors.ENDC}Tag utilisé                 : {tag:<18}{Colors.BLUE} ║")
    print(f"║ {Colors.ENDC}Longueur demandée           : {length:<18}{Colors.BLUE} ║")
    print(f"║{Colors.ENDC}" + "─" * 50 + f"{Colors.BLUE}║")
    print(f"║ {Colors.BOLD}{Colors.CYAN}Mot de passe généré : {password:<26}{Colors.BLUE}{Colors.BOLD} ║")
    print(f"╚" + "═" * 50 + f"╝{Colors.ENDC}\n")

# --- Main Execution ---
if __name__ == "__main__":
    
    print("--- Exercice 3 ---")
    
    master = get_master_password()

    print()
    
    tag = input(f"{Colors.CYAN}Entrez le tag (ex: 'Unilim', 'Facebook') : {Colors.ENDC}")
    length = get_password_length()
    
    final_password = mdp_hash(master, tag, length)
    
    display_result(master, tag, length, final_password)

