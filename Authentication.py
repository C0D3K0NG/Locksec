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
    return key_ram
  else:
    print("\nPassword is wrong")
    return None

def register_user(username):
  if username == "new user":
    username = input("\nEnter Your Username to make a new account: ")
    password = getpass.getpass("\nEnter the Master Password: ")
  else:
    password = getpass.getpass(f"Create a new account for {username}.\nEnter Your Mater Password:")
  salt1 = crypto.generate_salt()
  salt2 = crypto.generate_salt()
  a_hash, e_key = crypto.derive_keys(password, salt1, salt2)
  db.add_user(username,a_hash,salt1,salt2)
  
  
if __name__ == "__main__":
    db = DatabaseManager()
    crypto = CryptoManager()
    choice = input("\n----------------------\n1.Register Account\n2.Login to Account\n3.Close\n----------------------\nChoice: ")
    if choice == "1":
      register_user("new user")
    elif choice == "2":
      login_user()
    else:
      sys.exit(0)
    