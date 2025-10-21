import hashlib
import os

HASH_FILE = "mpwd.hash" 

def mdp_hash(master, tag, n): 

    combined = master + tag
    bite_combined = combined.encode('utf-8')
    hash_object = hashlib.sha256(bite_combined).hexdigest()
    final_password = hash_object[:n]
    return final_password

def get_hash(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def set_new_master_password():

    while True:
        new_master = input("Veuillez définir un nouveau mot de passe maître : ")
        new_master_confirm = input("Confirmez le mot de passe maître : ")

        if new_master != new_master_confirm:
            print("Erreur : Les mots de passe ne correspondent pas. Réessayez.")
            continue
            
        if " " in new_master or not new_master:
            print("Erreur : Le mot de passe maître ne doit pas contenir d'espaces et ne peut pas être vide.")
        else:
            try:
                hash_to_store = get_hash(new_master)
                with open(HASH_FILE, "w", encoding="utf-8") as f:
                    f.write(hash_to_store)
                print(f"Hachage du nouveau mot de passe maître enregistré dans {HASH_FILE}.")
                return new_master 
            except IOError as e:
                print(f"Erreur critique lors de l'écriture du fichier : {e}")
                return None

def get_master_password():
   
    if not os.path.exists(HASH_FILE):
        print(f"Aucun fichier {HASH_FILE} trouvé.")
        return set_new_master_password() 
    
    change_request = input("Voulez-vous changer le mot de passe maître ? (o/n) : ").lower().strip()
    if change_request == 'o':
        return set_new_master_password()
        
    print("Veuillez déverrouiller votre gestionnaire.")
    
    for attempt in range(3):
        unlock_pass = input("Mot de passe maître : ")
        
        current_hash = get_hash(unlock_pass)
        
 
        with open(HASH_FILE, "r", encoding="utf-8") as f:
            stored_hash = f.read().strip()

        if current_hash == stored_hash:
            print("Mot de passe correct. Programme déverrouillé.")
            return unlock_pass
        else:
            print(f"Mot de passe incorrect. (Essai {attempt + 1}/3)")
    
    print("Trop de tentatives échouées.")
    return None

def get_password_length():
    while True: 
        try:
            user_input = input("Entrez la longueur souhaitée pour le mot de passe (entre 1 et 12) : ")
            length = int(user_input)
            if 1 <= length <= 12: return length
            else: print("Erreur : Le nombre doit être compris entre 1 et 12.")
        except ValueError:
            print("Erreur : Veuillez entrer un nombre valide.")

if __name__ == "__main__":
    print("--- Générateur de mots de passe Sécurisé (Exercice 5 - Simple) ---")
    
    master = get_master_password()
    
    if master is None:
        print("Impossible de vérifier le mot de passe maître. Arrêt du programme.")
    else:
        tag = input("Entrez le tag (ex: 'Unilim', 'Facebook') : ")
        length = get_password_length()
        
        final_password = mdp_hash(master, tag, length)
        
        print("--------------------------------------------------")
        print(f"Mot de passe généré : {final_password}")
        print("--------------------------------------------------")
        
    print("Fin du programme.")