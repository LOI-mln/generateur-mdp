import hashlib
import os 

MASTER_FILE = "mpwd.txt" 

def mdp_hash(master, tag, n): 
    combined = master + tag
    bite_combined = combined.encode('utf-8')
    hash_object = hashlib.sha256(bite_combined).hexdigest()
    final_password = hash_object[:n]
    return final_password

def set_new_master_password():
    while True:
        new_master = input("Veuillez définir un nouveau mot de passe maître : ")
        
        if " " in new_master:
            print("Erreur : Le mot de passe maître ne doit pas contenir d'espaces.")
        elif not new_master:
             print("Erreur : Le mot de passe maître ne peut pas être vide.")
        else:
            try:
                with open(MASTER_FILE, "w", encoding="utf-8") as f:
                    f.write(new_master)
                print(f"Nouveau mot de passe maître enregistré dans {MASTER_FILE}.")
                return new_master
            except IOError as e:
                print(f"Erreur critique lors de l'écriture du fichier : {e}")
                return None 

def get_master_password():

    master_password = None
    
    # on vérifie d'abord si le fichier existe
    file_exists = os.path.exists(MASTER_FILE)

    if file_exists:
        change_request = input("Voulez-vous changer le mot de passe maître ? (o/n) : ").lower().strip()
        if change_request == 'o':
            master_password = set_new_master_password()
            return master_password 
    
    if master_password is None: 
        try:
            with open(MASTER_FILE, "r", encoding="utf-8") as f:
                master_password = f.read().strip()
            
            if not master_password:
                print(f"Le fichier {MASTER_FILE} est vide.")
                master_password = set_new_master_password()
            else:
                print("Mot de passe maître chargé depuis le fichier.")
        except FileNotFoundError:
            print(f"Aucun fichier {MASTER_FILE} trouvé.")
            master_password = set_new_master_password()
        except IOError as e:
            print(f"Erreur lors de la lecture du fichier : {e}")
            return None
    
    return master_password

def get_password_length():
    while True: 
        try:
            user_input = input("Entrez la longueur souhaitée pour le mot de passe (entre 1 et 12) : ")
            length = int(user_input)

            if 1 <= length <= 12:
                return length
            else:
                print("Erreur : Le nombre doit être compris entre 1 et 12.")
                
        except ValueError:
            print("Erreur : Veuillez entrer un nombre valide.")


if __name__ == "__main__":
    
    print("--- Exercice 3 ---")
    
    master = get_master_password()

    tag = input("Entrez le tag (ex: 'Unilim', 'Facebook') : ")
    length = get_password_length()

    final_password = mdp_hash(master, tag, length)
    
    print("--------------------------------------------------")
    print(f"Mot de passe maître (caché): {'*' * len(master)}")
    print(f"Tag: {tag}")
    print(f"Longueur: {length}")
    print(f"Mot de passe généré : {final_password}")
    print("--------------------------------------------------")