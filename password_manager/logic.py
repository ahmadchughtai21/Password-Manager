import random
import string
import os
from pwinput import pwinput

encryption_strength = 12

websites = []
usernames = []
passwords = []
master_password = ""

def generate_password():
    print("Generate Password")
    try:
        length = int(input("Enter Password Length: "))
    except ValueError:
        print("Invalid Length!")
        generate_password()
    upper = input("Include Uppercase Characters? (y/n): ")
    special = input("Include Special Characters? (y/n): ")
    numbers = input("Include Numbers? (y/n): ")
    
    characters = string.ascii_lowercase
    if upper == "y":
        characters += string.ascii_uppercase
    if special == "y":
        characters += string.punctuation
    if numbers == "y":
        characters += string.digits
        
    password = ''.join(random.choices(characters, k=length))
    
    print(f"Generated Password: {password}")
    if upper == "y" and special == "y" and numbers == "y" and length >= 8:
        print("Password Strength is Strong!")
    elif upper == "y" and special == "y" or upper == "y" and numbers == "y" or special == "y" and numbers == "y" and length >= 8:
        print("Password Strength is Medium!")
        choice= input("Do you want to save this password? (y/n): ")
        if choice == "y":
            website = input("Enter Website: ")
            username = input("Enter Username: ")
            encrypted_password = encrypt_password(password)
            websites.append(website)
            usernames.append(username)
            passwords.append(encrypted_password)
            export_passwords()
            print("Password Saved!")
            export_passwords()
            main()
        else:
            print("Password Not Saved!")
            main()
    else:
        print("Password Strength is Weak!")
        choice= input("Do you want to save this password? (y/n): ")
        if choice == "y":
            website = input("Enter Website: ")
            username = input("Enter Username: ")
            encrypted_password = encrypt_password(password)
            websites.append(website)
            usernames.append(username)
            passwords.append(encrypted_password)
            export_passwords()
            print("Password Saved!")
            export_passwords()
            main()
        else:
            print("Password Not Saved!")
            main()
    
    website = input("Enter Website: ")
    username = input("Enter Username: ")
    encrypted_password = encrypt_password(password)
    
    websites.append(website)
    usernames.append(username)
    passwords.append(encrypted_password)
    export_passwords()
    print("Password Saved!")

def save_password():
    print("Save Password")
    website = input("Enter Website: ")
    username = input("Enter Username: ")
    password = pwinput("Enter Password: ", '*')
    encrypted_password = encrypt_password(password)
    
    websites.append(website)
    usernames.append(username)
    passwords.append(encrypted_password)
    print("Password Saved!")
    export_passwords()
    
    
def encrypt_password(password):
    hash = "" + string.ascii_letters + string.digits + string.punctuation
    reversed_password = password[::-1]
    encrypted_password = ""
    list_rev = list(reversed_password)
    for letter in list_rev:
        encrypted_password += letter + ''.join(random.choices(hash, k=encryption_strength))
    return encrypted_password
    
def delete_password():
    print("Delete Password")
    for i in range(len(websites)):
        print(f"{i+1}. {websites[i]}")
    
    choice = int(input("Enter Choice: "))
    websites.pop(choice-1)
    usernames.pop(choice-1)
    passwords.pop(choice-1)
    export_passwords()
    print("Password Deleted!")
    
def retrieve_password():
    print("Retrieve Passwords")
    for i in range(len(websites)):
        print(f"{i+1}. {websites[i]}")
    
    choice = int(input("Enter Choice: "))
    print (f"Username: {usernames[choice-1]}")
    
    # Decryption
    reversed_password = passwords[choice-1]
    decrypted_password = ""
    for i in range(0, len(reversed_password), encryption_strength+1):
        decrypted_password += reversed_password[i]
    print(f"Password: {decrypted_password[::-1]}")

def export_passwords():
    with open("database.txt", 'w') as f:
        for i in range(len(websites)):
            f.write(f"{websites[i]} {usernames[i]} {passwords[i]}\n")
    with open("key.txt", 'w') as p:
        p.write(master_password)
        
    # print("Passwords Exported!")

def import_passwords():
    if not os.path.exists("database.txt"):
        open("database.txt", 'w').close()
    with open("database.txt", 'r') as f:
        lines = f.readlines()
        for line in lines:
            data = line.split()
            websites.append(data[0])
            usernames.append(data[1])
            passwords.append(data[2])
            
    if not os.path.exists("key.txt"):
        open("key.txt", 'w').close()
    with open("key.txt", 'r') as p:
        global master_password
        master_password = p.read()  
        
    # print("Passwords Imported!")

def main():
    while True:
        print("Main Menu")
        print(" [1]. Save Password")
        print(" [2]. Generate Password")
        print(" [3]. Retrieve Password")
        print(" [4]. Delete Password")
        print(" [5]. Change Master Password")
        print(" [6]. Save and Exit")
        
        choice = int(input("Enter Choice: "))
        
        match(choice):
            case 1:
                save_password()
            case 2:
                generate_password()
            case 3:
                retrieve_password()
            case 4:
                delete_password()
            case 5:
                change_master_password()
            case 6:
                export_passwords()
                exit()
            case _:
                print("Invalid!")       

def authentication():
    import_passwords()
    global master_password
    if master_password == "":
        temp_master_password = pwinput("Setup Master Password: ","*")
        confirm_master_password = pwinput("Confirm Master Password: ","*")
        if temp_master_password == confirm_master_password:
            master_password = encrypt_password(temp_master_password)
            print("Master Password Set!")
            export_passwords()
            import_passwords()
            authentication()
        else:
            print("Passwords Do Not Match!")
            authentication()
            
            
    else:
        m_password = pwinput("Enter Master Password: ", "*")
        nPass = ""
        for i in range(0, len(master_password), encryption_strength+1):
            nPass += master_password[i]
        oldPass = nPass[::-1]
        
        if oldPass == m_password:
            print("Authentication Successful!")
            export_passwords()
            main()
        else:
            print("Authentication Failed!")
            authentication()
            
def change_master_password():
    global master_password
    print("Change Master Password")
    new_password = pwinput("Enter New Master Password: ", "*")
    confirm_password = pwinput("Confirm New Master Password: " , "*")
    if new_password != confirm_password:
        print("Passwords Do Not Match!")
        change_master_password()
    else:
        master_password = encrypt_password(new_password)
        export_passwords()
        print("Master Password Changed!")
        
if __name__ == "__main__":
    authentication()