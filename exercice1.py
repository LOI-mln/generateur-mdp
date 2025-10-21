import hashlib
import sys

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

def mdp_hash(master, tag):
    combined = master + tag
    bite_combined = combined.encode('utf-8')
    hash_object = hashlib.sha256(bite_combined).hexdigest()
    final_password = hash_object[:8]
    return final_password

def display_header():
    print(f"{Colors.HEADER}{Colors.BOLD}")
    print("╔" + "═" * 50 + "╗")
    print("║" + " " * 8 + "GÉNÉRATEUR DE MOTS DE PASSE BASIQUE" + " " * 7 + "║")
    print("╚" + "═" * 50 + "╝")
    print(f"{Colors.ENDC}")

def display_result(master, tag, password):
    master_hidden = '*' * len(master)
    print(f"\n{Colors.GREEN}{Colors.BOLD}Voici le résultat de la génération :{Colors.ENDC}")
    print(f"{Colors.BLUE}╔" + "═" * 50 + "╗")
    print(f"║ {Colors.ENDC}Mot de passe maître (caché) : {master_hidden:<18}{Colors.BLUE} ║")
    print(f"║ {Colors.ENDC}Tag utilisé                 : {tag:<18}{Colors.BLUE} ║")
    print(f"║{Colors.ENDC}" + "─" * 50 + f"{Colors.BLUE}║")
    print(f"║ {Colors.BOLD}{Colors.CYAN}Mot de passe généré (8 chars) : {password:<16}{Colors.BLUE}{Colors.BOLD} ║")
    print(f"╚" + "═" * 50 + f"╝{Colors.ENDC}\n")

# --- Main Execution ---
if __name__ == "__main__":
    
    display_header()
    
    master = input(f"{Colors.CYAN}Entrez le mot de passe maître : {Colors.ENDC}")
    tag = input(f"{Colors.CYAN}Entrez le tag (ex: 'Unilim', 'Facebook') : {Colors.ENDC}")
    
    final_password = mdp_hash(master, tag)
    
    display_result(master, tag, final_password)
