import hashlib

def mdp_hash(master,tag): 
    combined = master + tag
    bite_combined = combined.encode('utf-8')
    hash_object = hashlib.sha256(bite_combined).hexdigest()
    final_password = hash_object[:8]
    return final_password


if __name__ == "__main__":

    print("--- Exercice 1 ---")
    master = input("Enter the master password: ")
    tag = input("Enter the tag: ")
    print("Generated password:", mdp_hash(master, tag))