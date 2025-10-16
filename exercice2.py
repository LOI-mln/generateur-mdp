import hashlib
import base64

def mdp_hash(master,tag,n): 
    combined = master + tag
    bite_combined = combined.encode('utf-8')
    hash_object = hashlib.sha256(bite_combined).hexdigest()
    final_password = hash_object[:n]
    return final_password


if __name__ == "__main__":
    master = input("Enter the master password: ")
    tag = input("Enter the tag: ")
    is_correct = False
    while not is_correct: 
        try:
            user_input = input("Entrez la longueur souhaitée pour le mot de passe (entre 1 et 12) : ")
            length = int(user_input)

            if 1 <= length <= 12:
                print(f"OK, la longueur sera de {length} caractères.")
                is_correct = True
            else:
                print("Erreur : Le nombre doit être compris entre 1 et 12.")
                
        except ValueError:
            print("Erreur : Veuillez entrer un nombre valide.")
    print("Generated password:", mdp_hash(master, tag, length))