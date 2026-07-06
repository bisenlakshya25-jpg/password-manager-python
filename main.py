#================/@/==================
#.         import the modules 
#.         defining universal things
#================/@/==================

import os
import json
import re
import secrets
import string
import time

FILE_NAME = "credentials_database.json"
database = {}
credentials = {}
master_password = None
last_verified = 0
ACCESS_TIME = 300

#================/@/==================
# file handling
#================/@/==================

#To load data
def load_data():
    global credentials
    global database
    
    if os.path.exists(FILE_NAME):      
        
        try:
            with open(FILE_NAME, "r") as file:
                data = json.load(file)
                database = {k: v for k, v in data.items()}
                
                try:
                    raw_data = database["credentials"]
                    credentials = {int(k): v for k, v in raw_data.items()}
                
                except Exception as e:
                    print(f"❌ Error loading Data : {e}")
                    credentials = {}
        
        except Exception as e:
            print(f"❌ Error loading Data : {e}")
            database = {}
    
    else:
        database = {}
        credentials = {}
        
#to save data
def save_data():
    global credentials
    
    updated_credentials = {}
    new_id = 1
        
    for old_id, details in credentials.items():
        updated_credentials[new_id] = details
        new_id += 1
    
    credentials = updated_credentials
    database["credentials"] = credentials
    
    try:
        with open(FILE_NAME, "w") as file:
            json.dump(database, file, indent=4)
    
    except Exception as e:
        print(f"❌ Error Saving the data: {e}")


#================/@/==================
# convienient functions
#================/@/==================

def print_credential(key):
    (print(" ")
    print(int(key))
    print(f"    Website/App  :  {credentials[key]["Website"]}")
    print(f"    UserName     :    {credentials[key]["UserName"]}")
    print(f"    Password     :  ***************")

#____________________________________________

def print_credential_with_password(key):
    print(" ")
    print(int(key))
    print(f"    Website/App  :  {credentials[key]["Website"]}")
    print(f"    UserName     :  {credentials[key]["UserName"]}")
    print(f"    Password.    :  {credentials[key]["Password"]}")
    
#____________________________________________

def check_database():
    if credentials:
        return False

    else:
        print("No credentials found in the database")
        return 

#____________________________________________

def check_access():
    global last_verified
    
    if time.time() - last_verified < ACCESS_TIME:
        return 
    
    while True:
        print(" ")
        master = input("Enter the master password to proceed: ")
        
        if master != master_password:
            print("Password not matched! Try again")
        
        else:
            last_verified = time.time()
            return


#================/@/==================
# Input Validation
#================/@/==================

def check_input(prompt, max_val = 10, min_val = 1):
    print(" ")
    
    while True:
        value = input(prompt)
        value = value.strip()
        
        try:
            num = int(value)
            
            if min_val <= num <= max_val:
                return num
            
            else:
                print("Invalid input! Please enter a value between", min_val, "and", max_val)
        
        except ValueError:
          print("Invalid input! Please enter a valid integer.")

#____________________________________________

def password_input(prompt = "Enter the password: "):
    print(" ")
    password = None
    
    while True: 
        new_pass = input(prompt)
        choice, initial = check_strength(new_pass)
        
        if choice:
            
            if initial != None:
                password = initial
                break
            
            password = new_pass
            break
    
    return password

#____________________________________________

def get_credential(prompt, show_pass = False):
    print(" ")
    user_input = input(f"Enter the Username or Website/App Name that you want to {prompt}")
    user_input = user_input.strip().lower()
    
    credential = []
    found = False
    
    for key, value in credentials.items():
        list = credentials[key]
        search_list = [list["Website"], list["UserName"]]
        
        for category in search_list:
            if user_input in category.lower():
                
                if show_pass == True:
                    print_credential_with_password(key)
                
                else:
                    print_credential(key)
                
                print("__________________________________")
                found = True
                credential.append(key)
    
    return found, credential


#================/@/==================
# password related operations
#================/@/==================

def generate_password(length = 12):
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*()"
    
    while True:
        password = ''.join(secrets.choice(alphabet) for _ in range(length))
        
        if (len(password) >= 8 and re.search(r"[a-z]", password) and re.search(r"[A-Z]", password) and re.search(r"\d", password) and re.search(r"[!@#$%^&*()]", password)):
            return password

#____________________________________________

def check_strength(password):
    print(" ")
    score = 0
    feedback = []
    
    if len(password) >= 8: 
        score += 1
    
    else: 
        feedback.append("Make password lenght atleast upto 8 character")
    
    
    if re.search(r"[a-z]", password): 
        score += 1
    
    else: 
        feedback.append("Add atleast 1 lower case letter")
        
    
    
    if re.search(r"[A-Z]", password): 
        score += 1
    
    else: 
        feedback.append("Add atleast 1 upper case letter.")
        
    
    
    if re.search(r"\d", password): 
        score += 1
    
    else: 
        feedback.append("Add atleast 1 numeric digit.")
        
    
    
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password): 
        score += 1
    
    else: 
        feedback.append("Add atleast one special character (e.g. @, #, $).")
    
    
    if score == 5:
        category = "Strong"
    
    elif score >= 3:
        category = "Medium"
    
    
    else:
        category = "Weak"
    
    
    if category == "Strong":
        print("Strong")
        return True, None
    
    print(f"\n{category} strength. Select appropriate option:")
    print("1. Change the password ")
    print("2. Continue with the current password ")
    print("3. Generate a strong password")
    choice = check_input("Enter Choice: ", max_val = 3)

    if choice == 1:
        print("--- Tips for a Strong Password ---")
        
        for tip in feedback:
            print(f"- {tip}")
        
        print("_______________________________")
        return False, None

    elif choice == 2:
        return True, None

    else:
        new_password = generate_password()
        print(f"\nyour new password: {new_password}")
        return True, new_password


#================/@/==================
# CRUD AND SEARCH OPERATIONS
#================/@/==================

def add_credential():
    print(" ")
    while True:
        
        website = input("Enter Website/App name: ")
        website = website.strip().title()
        
        user_name = input("Enter Username: ")
        password = password_input()      
        
        pass_id = None
        if credentials:
            pass_id = int(list(credentials.keys())[-1])
            pass_id += 1
        
        else:
            pass_id = 1
        
        credentials[pass_id] = {"Website" : website, "UserName" : user_name, "Password" : password}
        save_data()
        print("Credential added succesfully")
        print("________________________________________")
        
        next_choice = check_input("1. Add Another credential\n2. View all credentials\n3. Return to main menu\n4. Exit", max_val = 4)
        if next_choice == 2:
            return view_credentials()
        
        elif next_choice == 3: 
            return True
        
        elif next_choice == 4:
            return False

#____________________________________________

def view_credentials():
    print(" ")
    if check_database():
        return True
    
    check_access()
    
    for key, value in credentials.items():
        print("___________________________________________")
        print_credential_with_password(key)
    
    print("___________________________________________")
    user_choice = check_input("Select appropriate option:-\n1. Add new credential.  \n2. Update any credential\n3. Delete any credential\n4. Return to main menu\n5. Exit\nEnter choice: ", max_val = 5)  
    
    if user_choice == 1:
        return add_credential()   
    
    elif user_choice == 2:
        return update_credential()     
    
    elif user_choice == 3:
        return delete_credential()  
    
    elif user_choice == 4:
        return True 
    
    else:
        return False

#____________________________________________

def update_credential():
    print(" ")
    while True:      
        if check_database():
            return True        
        
        print("_______________________________")
        check_access()
        found, credential = get_credential("Update: ")
        
        if not found:
            print("No match found for your search")
            print("_______________________________")
        
        else:
            if len(credential) != 1:
                while True:
                    user_preference = check_input("Please enter the the code above the credential you want to update: ", max_val = max(credential))
                
                    if user_preference in credential:
                        credential = [user_preference]
                        break
                    
                    else:
                        print("Please enter the value that are listed above your credential")
        
            while True:
                print("What do you want to update for this credential")
                user_choice = check_input("1. UserName\n2. Password\n3. Return to previous menu \nEnter Choice: ", max_val = 3)     
                
                if user_choice == 1:
                    update_value = input("Enter new username: ")
                    credentials[credential[0]]["UserName"] = update_value.strip()           
                
                elif user_choice == 2:
                    check_access()
                    
                    while True:
                        password = password_input()
                        choices = check_input("Are you sure you want to update password: \n1. Yes \n2. No\nEnter choice: ", max_val = 2)
                        
                        if choices == 1:
                            credentials[credential[0]]["Password"] = password
                            break
                
                break
                
                print("_____________________________________")
                user_next = check_input("Do you want to update any other information for this credential\n1. Yes\n2. No\nEnter Choice: ", max_val = 2)
                print("_____________________________________")
                
                if user_next == 2:
                    break

        next_choice = check_input("1. Update Another credential\n2. View all credential\n3. Return to main menu \n4. Exit\nEnter your choice: ", max_val = 4)
        if next_choice == 2:
            return view_credentials()
            
        elif next_choice == 3:
            return True
            
        elif next_choice == 4:
            return False

#____________________________________________

def delete_credential():
    print(" ")
    while True:
        found, credential = get_credential("Delete: ")
        
        if not found:
            print("No match found for your search")
            print("_______________________________")
        
        else:
            if len(credential) != 1:
                
                while True:
                    user_preference = check_input("Please enter the the code above the credential you want to delete: ", max_val = max(credential))       
                    
                    if user_preference in credential:
                        credential = [user_preference]
                        break 
                    
                    else:
                        print("Please enter the value that are listed above your credential")
            
            print("Are you sure you want to delete the credential")
            user_choice = check_input("1. Yes\n2. No \nEnter Choice: ", max_val = 2)     
            
            if user_choice == 1:
                del credentials[credential[0]]
                save_data()
                
                print("Credential deletion completed ")
                print("____________________________")
        
        print("Select appropriate option")
        user_preference = check_input("1. Delete another credential\n2. View all credentials \n3. Return to main menu\n4. Exit", max_val = 4)   
        
        if user_preference == 2:
            return view_credentials()
        
        elif user_preference == 3:
            return True
        
        elif user_preference == 4:
            return False

#____________________________________________

def search_credential():
    print(" ")
    if check_database():
        return True
    
    check_access()
    while True:
        
        print("_______________________________")
        found, credential = get_credential("Search: ", show_pass = True)
        
        if not found:
            print("No credential found for your search")
            print("_______________________________")
        
        user_choice = check_input("1. Search for different credential\n2. View all credential\n3. Return to main menu\n4. Exit\nEnter your choice: ", max_val = 4)
        
        if user_choice == 2:
            return view_credentials()
        
        elif user_choice == 3:
            return True
        
        elif user_choice == 4:
            return False


#================/@/==================
# Additional features
#================/@/==================

def password_generator():
    print(" ")
    while True:
        length = check_input("\nEnter the length of password to generate: ", max_val = 50)
        password = generate_password(length = length)
        
        print(f"Your password is : {password}")
        print("__________________________________")
        print("1. Generate another password\n2. Return to previous menu\n3. Exit")
        
        choice = check_input("Enter choice: ", max_val = 3)
        if choice == 2:
            return True
        
        elif choice == 3:
            return False

#____________________________________________

def master_password_changer():
    print(" ")
    check_access()
    master_password_initialisation()
    return True

#================/@/==================
# Starting screens functions
#================/@/==================

def master_password_initialisation():
    global master_password
    print(" ")
    
    print("________________________________________")
    print("Welcome to Password manager\nBefore proceeding! Set a master password for your password manager\n(this password is for your security purpose)\n(Remeber the password if you forget it all data will be cleared)")
    print("________________________________________")
    
    initial_password = password_input(prompt = "Set Master password")
    
    while True:
        confirm_password = input("Confirm password: ")
        
        if confirm_password == initial_password:
            break
        
        else:
            print("Password doesn't match")
    
    database["master_password"] = initial_password
    master_password = initial_password 
    
    print("Master password created Succesfully")
    print("_______________________________________")
    print("Do you want to use this password when you login")
    
    choice = check_input("1. Yes\n2. No\nEnter choice: ", max_val = 2)
    
    if choice == 1:
        print("You will require this password whenever you want to login the password manager")
        database["Settings"] = {"require_login" : "true"}
        
    else:
        database["Settings"] = {"require_login" : "false"}
    
    save_data()
    return

#____________________________________________

def password_manager_authentication():
    global last_verified
    print(" ")
    
    print("=================================")
    print("Password Manager")
    print("=================================")
    
    print(" ")
    print("Password required to enter the app")
    print("(only 3 attempts)")
    
    attempts = 0
    while True:
        
        print("_____________________________________")
        password = input("Master password: ")
        attempts += 1
        
        if password == master_password:
            last_verified = time.time()
            return True
        
        elif attempts == 1:
            print("Two attempts left")
        
        elif attempts == 2:
            print("Warning⚠️ Last attempt left")
        
        elif attempts == 3:
            print("Wrong password can't give permission to proceed further\n Thanks have a nice day")
            return False

#____________________________________________

def main_screen():
    print(" ")
    print("=================================")
    print("Password Manager")
    print("=================================")
    
    user_preference = check_input("1. Add new credential\n2. View Credential list\n3. Search credential\n4. Delete Credential\n5. Update credential\n6. Generate Random Password \n7. Change Master password\n8.Exit\nEnter choice: ", max_val = 8)
    if user_preference == 1:
        return add_credential()
    
    elif user_preference == 2:
        return view_credentials()
    
    elif user_preference == 3:
        return search_credential()
    
    elif user_preference == 4:
        return delete_credential()
    
    elif user_preference == 5:
        return update_credential()
    
    elif user_preference == 6:
        return password_generator()
    
    elif user_preference == 7:
        return master_password_changer()
    
    else:
        return False

#================/@/==================
# Program startup 
#================/@/==================

load_data()

while True:
    
    if "master_password" not in database:
        master_password_initialisation()
    
    settings_required = database["Settings"].get("require_login")
    
    if settings_required == "true":
        if password_manager_authentication():
            
            while main_screen():
                pass
            
            print("Thanks for choosing us. See you later")
            break
        
        else:
            break
    
    else:
        while main_screen():
            pass
        
        print("Thanks for choosing us. See you later")
        break
