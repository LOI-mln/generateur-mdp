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
    n = int(input("Enter the length of the generated password: "))
    while n <= 0 or n > 12:
        n = int(input("Please enter a valid length (1-12): "))
    print("Generated password:", mdp_hash(master, tag, n))