from cryptography.fernet import Fernet
import hashlib
import base64
import time
import os

# Function to generate and save the secret key========
def gen_key(manually=False):

    if not manually:    # generating a random key
        key = Fernet.generate_key()
    
    else:   # Generating manual key
        key = input("Type the key: ")
        hash_bytes = hashlib.sha256(key.encode()).digest()
        key = base64.urlsafe_b64encode(hash_bytes[:32])
    
    # writing key
    with open("key.key", "wb") as key_file:
        key_file.write(key)
    print("Key generated and saved in the 'key.key' file. Keep it safe!")



# Function to load the secret key=====================
def load_key():
    if not os.path.exists("key.key"):
        raise FileNotFoundError("\nNo key was provided! Type or generate a new one.")
    with open("key.key", "rb") as key_file:
        return key_file.read()



# Function to encrypt and save a password=============
def save_password(name, password, key_str): 

    if not key_str:
        try:
            key = load_key()    # Loads a key file
            print("Loading .key file...")
        except Exception as e:
            print(f"{e}")
            return
        
    else:   # Processing the manual key   
        hash_bytes = hashlib.sha256(key_str.encode()).digest()
        key = base64.urlsafe_b64encode(hash_bytes[:32])

    fernet = Fernet(key)

    if not os.path.exists("passwd.enc"):
        with open("passwd.enc", "wb") as file:
            file.write(b"")


    if os.path.exists("passwd.enc"):
        with open("passwd.enc", "ab") as file:
            encrypted_password = fernet.encrypt(f"{name}:{password}".encode())
            file.write(encrypted_password + b"\n")
        print(f"Password for {name} saved successfully!")
        time.sleep(2)
        return


# Function to view decrypted passwords================
def view_passwords(key_str):

    if not key_str:
        try:
            key = load_key()
            print("Loading .key file...")
        except Exception as e:
            print(f"{e}")
            return

    else:
        hash_bytes = hashlib.sha256(key_str.encode()).digest()
        key = base64.urlsafe_b64encode(hash_bytes[:32])

    fernet = Fernet(key)

    # If passwd file does not exists
    if not os.path.exists("passwd.enc"):
        print("No passwords saved yet.")
        return

    # Reading passwd file
    with open("passwd.enc", "rb") as file:
        lines = file.readlines()

    # Displaying passwords
    print("\nStored passwords:")
    for line in lines:
        decrypted_password = fernet.decrypt(line.strip()).decode()
        print(decrypted_password)


# Program menu=========================================
def menu():
    while True:
        print("\n=== PASSWORD MANAGER ===")
        print("1. Generate key (optional)")
        print("2. Save password")
        print("3. View passwords")
        print("4. Exit")

        choice = input("\nChoose an option: ")

        # Generate a new key
        if choice == "1":
            os.system("clear")
            while True:
                print("\n=== PASSWORD MANAGER ===")
                print("1. Generate a random key")
                print("2. Insert manually")
                print("0. <- Back to menu")
                choice = input("\nChoose an option: ")
                if choice == "1":
                    gen_key()
                    break
                elif choice == "2":
                    gen_key(manually=True)
                    break
                elif choice == "0":
                    break
                else:
                    print("\n#INVALID OPTION!")
            os.system("clear")


        # Save a new password
        elif choice == "2":
            os.system("clear")
            name = input("Enter name/service: ")
            password = input("Enter password: ")    
            key = input("\nKEY: ")
            save_password(name, password, key)
            time.sleep(3)
            os.system("clear")


        # View passwords
        elif choice == "3":
            key = input("\nKEY: ")
            view_passwords(key)
            input("\nType ENTER to back to menu <-")
            os.system("clear")


        # Exit
        elif choice == "4":
            print("Exiting...")
            time.sleep(2)
            os.system("clear")
            break
        
        # Invalid
        else:
            print("Invalid option! Please try again.")

if __name__ == "__main__":
    menu()
