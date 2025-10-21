import hashlib
import os
import itertools 
import time     

CHARSET_ATTAQUE = "abcdefghijklmnopqrstuvwxyz" 

LONGUEUR_ATTAQUE = 10 


def mdp_hash(master, tag, n): 
    combined = master + tag
    bite_combined = combined.encode('utf-8')
    hash_object = hashlib.sha256(bite_combined).hexdigest()
    final_password = hash_object[:n]
    return final_password

def load_real_master_password(filename="mpwd.txt"):
 
    if not os.path.exists(filename):
        print(f"Erreur : Le fichier '{filename}' est introuvable.")
        print("Veuillez le créer avec votre mot de passe maître de 10 caractères.")
        return None
        
    try:
        with open(filename, "r", encoding="utf-8") as f:
            master_password = f.read().strip()
            
        if len(master_password) != 10:
            print(f"Erreur : Le mot de passe maître dans '{filename}' doit faire 10 caractères.")
            return None
            
        return master_password
        
    except IOError as e:
        print(f"Erreur lors de la lecture du fichier : {e}")
        return None

def run_bruteforce_attack(real_master, target_tags, N):

    print(f"\n--- Lancement Force Brute (N={N}) sur {target_tags} ---")
    print(f"  Charset: '{CHARSET_ATTAQUE[0]}...{CHARSET_ATTAQUE[-1]}' ({len(CHARSET_ATTAQUE)} caractères)")
    print(f"  Longueur d'entrée: {LONGUEUR_ATTAQUE}")
    
    targets = {}
    for tag in target_tags:
        targets[tag] = mdp_hash(real_master, tag, N)
    print(f"  Cible(s) à trouver (Sortie N={N}): {targets}")

    generator = itertools.product(CHARSET_ATTAQUE, repeat=LONGUEUR_ATTAQUE)

    attempts = 0
    found_collision = False
    start_time = time.time() 

    try:
        for guess_tuple in generator:
            attempts += 1
            guess = "".join(guess_tuple)
            
            if attempts % 250000 == 0:
                print(f"  ... {attempts} essais ({guess})")

            match = True
            for tag in target_tags:
                guess_pass = mdp_hash(guess, tag, N)
                if guess_pass != targets[tag]:
                    match = False
                    break
            
            if match:
                if guess == real_master:
                    print(f"  ... {attempts} essais : Le mot de passe maître réel a été trouvé. On continue...")
                    continue 
                    
                found_collision = True
                end_time = time.time()
                print(f"\n!!! COLLISION TROUVÉE après {attempts} essais !!!")
                print(f"  Temps écoulé : {end_time - start_time:.4f} secondes")
                print(f"  Un 'faux' mot de passe maître : '{guess}'")
                print(f"  Produit les mêmes résultats que le vrai mot de passe :")
                for tag in target_tags:
                    print(f"    - {tag} (N={N}) : {mdp_hash(guess, tag, N)}")
                break 
    except KeyboardInterrupt:
        print("\n--- Attaque arrêtée manuellement. ---")           
            
    if not found_collision:
        end_time = time.time()
        print(f"\n--- Aucune collision trouvée après {attempts} essais. ---")
        print(f"  Temps écoulé : {end_time - start_time:.2f} secondes")

if __name__ == "__main__":
    MASTER_FILE = "mpwd.txt"
    real_master = load_real_master_password(MASTER_FILE)
    
    if real_master:

        print(f"Mot de passe maître (10 car.) chargé avec succès : {'*' * 10}")

        run_bruteforce_attack(real_master, ["Unilim"], 1)
        run_bruteforce_attack(real_master, ["Unilim"], 2)
        run_bruteforce_attack(real_master, ["Unilim"], 3)
        run_bruteforce_attack(real_master, ["Unilim", "Amazon", "Netflix"], 1)
        run_bruteforce_attack(real_master, ["Unilim", "Amazon", "Netflix"], 2)
        run_bruteforce_attack(real_master, ["Unilim", "Amazon", "Netflix"], 3) 