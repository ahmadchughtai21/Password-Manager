from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.urls import reverse
import random
import string
import os
import pyperclip

encryption_strength = 12
log_out = True

websites = []
usernames = []
passwords = []
master_password = ""
g_generated_password = ""


def export_passwords():
    with open("static/database/websites.txt", 'w') as f:
        for i in range(len(websites)):
            f.write(f"{websites[i]}\n")
    with open("static/database/usernames.txt", 'w') as f:
        for i in range(len(usernames)):
            f.write(f"{usernames[i]}\n")
    with open("static/database/passwords.txt", 'w') as f:
        for i in range(len(passwords)):
            f.write(f"{passwords[i]}\n")
    with open("static/database/key.txt", 'w') as p:
        p.write(master_password)
        

def import_passwords():
    if not os.path.exists("static/database/websites.txt"):
        open("static/database/websites.txt", 'w').close()
    if not os.path.exists("static/database/usernames.txt"):
        open("static/database/usernames.txt", 'w').close()
    if not os.path.exists("static/database/passwords.txt"):
        open("static/database/passwords.txt", 'w').close()
    with open("static/database/websites.txt", 'r') as f:
        global websites
        websites = f.read().splitlines()
    with open("static/database/usernames.txt", 'r') as f:
        global usernames
        usernames = f.read().splitlines()
    with open("static/database/passwords.txt", 'r') as f:
        global passwords
        passwords = f.read().splitlines()
            
    if not os.path.exists("static/database/key.txt"):
        open("static/database/key.txt", 'w').close()
    with open("static/database/key.txt", 'r') as p:
        global master_password
        master_password = p.read()  

def encrypt_password(password):
    hash = ("" + string.ascii_letters + string.digits + string.punctuation)
    reversed_password = password[::-1]
    encrypted_password = ""
    list_rev = list(reversed_password)
    for letter in list_rev:
        encrypted_password += letter + ''.join(random.choices(hash, k=encryption_strength))
    return encrypted_password

def decrypt_password(encrypted_password):
    decrypted_password = ""
    for i in range(0, len(encrypted_password), encryption_strength+1):
        decrypted_password += encrypted_password[i]
    return decrypted_password[::-1]
                          
def authentication(request):
    import_passwords()
    if master_password == "":
        return redirect('sign_up')
    elif log_out==True:
        return redirect('log_in')
    elif log_out==False:
        return redirect('home')
    else:
        return redirect('log_in')


def sign_up(request):
    import_passwords()
    data = {
        'error': '',
    }
    global master_password, log_out
    if master_password != "":
        return redirect('home')
    if request.method == 'POST':
        if request.POST['password'] == request.POST['confirm_password']:
            master_password = encrypt_password(request.POST['password'])
            export_passwords()
            log_out = False
            return redirect('home')
        else:
            data['error'] = 'Passwords do not match'
            return render(request, 'sign_up.html', data)
    return render(request, 'sign_up.html', data)

    
def log_in(request):
    import_passwords()
    data={
        'error': '',
    }
    global master_password, log_out
    if request.method == 'POST':
        if request.POST['password'] == decrypt_password(master_password):
            log_out = False
            return redirect('home')
        else:
            data['error'] = 'Invalid Password! Try Again'
            return render(request,'log_in.html', data)
    return render(request, 'log_in.html', data)

def log_out(request):
    global log_out
    log_out = True
    return redirect('log_in')

def save_password(request):
    import_passwords()
    if master_password == "":
        return redirect('sign_up')
    elif log_out==True:
        return redirect('log_in')
    else:
        global websites, usernames, passwords, g_generated_password
        data = {
            'error': '',
            "password": g_generated_password,
        }
            
        if request.method == 'POST':
            website = request.POST.get('website')
            username = request.POST.get('username')
            password = request.POST.get('password')
            websites.append(website)
            usernames.append(username)
            if g_generated_password == "":
                passwords.append(encrypt_password(password))
            else:
                passwords.append(encrypt_password(g_generated_password))
            export_passwords()

            error = "Password Saved Successfully!"
            return redirect(f'/home?error={error}')

        return render(request, 'save_password.html', data)


def generate_password(request):
    import_passwords()
    if master_password == "":
        return redirect('sign_up')
    elif log_out==True:
        return redirect('log_in')
    else:
        
        global g_generated_password
        data = {
            'generated_password': '',
            'length_error': '',
            'strength': '',
            'error': '',
            'message': '',
        }
        
        if request.method == 'POST':
            try:
                length = int(request.POST.get('length', 0))
            except ValueError:
                length = 0

            include_upper = 'upper' in request.POST
            include_special = 'special' in request.POST
            include_numbers = 'numbers' in request.POST
            
            if length < 1 or length > 25:
                data['length_error'] = "Password length cannot be less than 1 or greater than 25"
                return render(request, 'generate_password.html', data)
            
            characters = string.ascii_lowercase
            if include_upper:
                characters += string.ascii_uppercase
            if include_special:
                characters += string.punctuation
            if include_numbers:
                characters += string.digits
            
            generated_password = ''.join(random.choice(characters) for _ in range(length))
            data['generated_password'] = generated_password
            
            strength = "Weak"
            if len(generated_password) >= 8 and include_upper and include_special and include_numbers:
                strength = "Strong"
            elif len(generated_password) >= 8:
                strength = "Medium"
            
            data['strength'] = strength
            g_generated_password = generated_password
            
            
        return render(request, 'generate_password.html', data)
    
def copy_password(request):
    generated_password = g_generated_password
    pyperclip.copy(generated_password)
    base_url = reverse('home')
    return redirect(f'{base_url}?error=Password Copied to Clipboard!')




def view_passwords(request):
    import_passwords()
    if master_password == "":
        return redirect('sign_up')
    elif log_out==True:
        return redirect('log_in')
    else:
        global websites, usernames, passwords
        data = {
            'websites': websites,
            'usernames': usernames,
            'passwords': [decrypt_password(password) for password in passwords],
        }
        return render(request, 'view_passwords.html', data)
    

def delete_password(request):
    if master_password == "":
        return redirect('sign_up')
    elif log_out==True:
        return redirect('log_in')
    else:
        global websites, usernames, passwords
        data = {
            'websites': websites,
            'usernames': usernames,
            'passwords': passwords,
            'error': '',
        }
        data['passwords'] = [decrypt_password(password) for password in passwords]
        
        if request.method == 'POST':
            try:
                index = int(request.POST.get('index'))
            except ValueError:
                data['error'] = "Invalid Entry"
                return render(request, 'delete_password.html', data)

            if index < 1 or index > len(websites):
                data['error'] = "Website does not exist"
                return render(request, 'delete_password.html', data)
            else:
                websites.pop(index-1)
                usernames.pop(index-1)
                passwords.pop(index-1)
                export_passwords()
                data['error'] = "Password Deleted Successfully!"
                data['passwords'] = [decrypt_password(password) for password in passwords]
                return render(request, 'delete_password.html', data)

        return render(request, 'delete_password.html', data)


def change_master_password(request):
    global master_password
    if master_password == "":
        return redirect('sign_up')
    elif log_out==True:
        return redirect('log_in')
    else:
        data = {
            'error': '',
        }
        if request.method == 'POST':
            if request.POST['new_password'] == request.POST['confirm_new_password']:
                master_password = encrypt_password(request.POST['new_password'])
                export_passwords()
                data['error'] = "Password Changed Successfully!"
                return redirect(f'/home?error={data["error"]}')
            else:
                data['error'] = "Passwords do not match!"
                return render(request, 'change_master_password.html', data)    
        return render(request, 'change_master_password.html')

      

def home(request):
    import_passwords()
    global master_password, log_out, g_generated_password
    if master_password == "":
        return redirect('sign_up')
    elif log_out==True:
        return redirect('log_in')
    else:
        g_generated_password = ""
        data={
            'password': master_password,
            'error': '',
        }
        data['error']=request.GET.get('error')
        if master_password == "":
            return redirect('sign_up')
        elif log_out==True:
            return redirect('log_in')
        else:
            return render(request, 'home.html', data)