from db_manager import DatabaseManager
from crypto_manager import CryptoManager
import getpass # Built-in python tool to hide password input

if __name__ == "__main__":
    db = DatabaseManager()
    crypto = CryptoManager()
    username = input("Enter Your Username: ")
    master_password = getpass.getpass("\nEnter the Master Password: ")
    salt1 = crypto.generate_salt()
    salt2 = crypto.generate_salt()
    a_hash, e_key = crypto.derive_keys(master_password, salt1, salt2)
    db.add_user(username,a_hash,salt1,salt2)
    