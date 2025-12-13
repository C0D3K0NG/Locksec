from db_manager import DatabaseManager
from crypto_manager import CryptoManager
import getpass # Built-in python tool to hide password input
import sys

def login_user():
  username = input("Enter Your Username: ")
  
  user_data = db.get_user(username) 
  
  if not user_data:
    print("Users not Found.Register Now")
    register_user(username)
    return
  master_password = getpass.getpass("\nEnter the Master Password: ")
  
  stored_auth_hash,salt_auth,salt_enc = user_data
  
  new_auth_hash,key_ram = crypto.derive_keys(master_password,salt_auth,salt_enc)
  
  if new_auth_hash == stored_auth_hash:
    print(f"\n{username} is successfully logged in")
    return key_ram,username
  else:
    print("\nPassword is wrong")
    return None

def register_user(username):
  if username == "new user":
    username = input("\nEnter Your Username to make a new account: ")
    password = getpass.getpass("\nEnter the Master Password: ")
  else:
    password = getpass.getpass(f"Create a new account for {username}.\nEnter Your Master Password:")
  salt1 = crypto.generate_salt()
  salt2 = crypto.generate_salt()
  a_hash, e_key = crypto.derive_keys(password, salt1, salt2)
  db.add_user(username,a_hash,salt1,salt2)
  

def add_new_password(user, key_ram):
    print("\n--- 📝 Add New Password ---")
    website = input("Website Name (e.g. Netflix): ")
    username = input("Username/Email for site: ")
    password = input("Password for site: ")
    
    # ENCRYPT: We use the key_ram we got from login!
    enc_user = crypto.encrypt(username, key_ram)
    enc_pass = crypto.encrypt(password, key_ram)
    
    # SAVE: We send the encrypted blobs to the DB
    db.add_password(user, website, enc_user, enc_pass)
  
def view_passwords(user,key_ram):
  print('-'*25)
  print(f"WELCOME {user}😇!")
  print('-'*25)
  results=db.get_passwords(user)
  
  if results == None:
    print("No passwords are saved.")
    return

  for row in results:
    print(f"{row[0]:<5} | {row[1]:<20}")
  
  try:
    choice = int(input("\nEnter The ID of the website you want to know the pass(click 0 to cancel): "))
    if choice == 0: return
    
    target_row=None
    for row in results:
      if row[0] == choice:
        target_row = row
        break
      
    if target_row:
      username=crypto.decrypt(target_row[2],key_ram)
      password=crypto.decrypt(target_row[3],key_ram)
      
      print(f"\n--- 🕵️ Credentials for {target_row[1]} ---")
      print(f"Username: {username}")
      print(f"Password: {password}")
      input("\nPress Enter to hide...") # Wait before clearing
    else:
      print("Invalid ID.")
            
  except ValueError:
        print("Please enter a valid number.")
      
    
    
if __name__ == "__main__":
    db = DatabaseManager()
    crypto = CryptoManager()
    choice = input("\n----------------------\n1.Register Account\n2.Login to Account\n3.Close\n----------------------\nChoice: ")
    if choice == "1":
      register_user("new user")
    elif choice == "2":
      data = login_user()
      if not data:
        sys.exit(0)
      key,user = data
      
      while True:
        choice=int(input('''\n1.Add New Password\n2.View Passwords\n3.Close\n'''))
        
        if choice == 1:
          add_new_password(user,key)
        
        elif choice == 2:
          view_passwords(user,key)
          
        elif choice == 3:
          key = None
          print("Logged Out")
          break
        
    else:
      sys.exit(0)
    