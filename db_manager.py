import sqlite3

# A class that manages everything related to the SQLite database:
# creating tables, saving users, saving vault entries, etc.
class DatabaseManager:
  def __init__(self, db_name="vault.db"):
    # Store the database file name (default = "vault.db")
    self.db_name = db_name
    
    # Automatically create the required tables when the class is initialized
    self.setup_database()
    
  def _connect(self):
    # Opens a connection to the SQLite database file
    # Every function that interacts with the DB calls this
    return sqlite3.connect(self.db_name)
  
  def setup_database(self):
    # Create tables if they don’t exist (runs only once when program starts)
    conn = self._connect()
    cursor = conn.cursor()

    # Create the "users" table (stores master login data + salts)
    cursor.execute('''
                  CREATE TABLE IF NOT EXISTS users(
      username TEXT PRIMARY KEY,      -- Unique username for each user
      auth_hash TEXT NOT NULL,        -- PBKDF2-derived authentication hash
      salt_auth BLOB NOT NULL,        -- Salt used to create auth key
      salt_enc BLOB NOT NULL,         -- Salt used to create encryption key
      recovery_key BLOB               -- Optional password recovery data
    )
    ''')

    # Create the "vault" table (stores website passwords for each user)
    cursor.execute('''
                  CREATE TABLE IF NOT EXISTS vault(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Unique entry ID
                    user_id TEXT,                          -- Links entry to a user
                    website TEXT,                          -- Website name
                    site_username TEXT,                    -- Username used on website
                    site_password TEXT,                    -- Encrypted password
                    FOREIGN KEY(user_id) REFERENCES users(username)
                    -- Ensures vault entries belong to a valid user
                    )
    ''')

    conn.commit()  # Save changes to the DB
    conn.close()   # Close connection to avoid memory leaks
    pass
  
  def add_user(self, username, auth_hash, salt_auth, salt_enc):
    # Add a new user into the "users" table
    conn = self._connect()
    cursor = conn.cursor()
    
    # SQL query with ? placeholders → prevents SQL injection attacks
    query = '''INSERT INTO users(username, auth_hash, salt_auth, salt_enc) VALUES (?, ?, ?, ?)'''
    
    try:
      # Insert the user into the table
      cursor.execute(query, (username, auth_hash, salt_auth, salt_enc))
      conn.commit()  # Save the new user to the database
      print(f"User {username} registered successfully.\n")
    
    except sqlite3.IntegrityError:
      # Happens when username already exists (PRIMARY KEY violation)
      print("The username is already registered.")
      
    finally:
      # Always close connection, even if error happens
      conn.close() 
  
  def get_user(self, username):
    conn=self._connect()
    cursor=conn.cursor()
    
    query = "SELECT auth_hash,salt_auth,salt_enc FROM users WHERE username=?"
    cursor.execute(query,(username,))
    result = cursor.fetchone()
    conn.close
    return result

# This block only runs if the file is executed directly (not imported)
if __name__ == "__main__":
    db = DatabaseManager()   # Create database + tables automatically
    
    # Test add_user → You can comment after first run to avoid duplicates
    db.add_user("test_user", "fake_hash", b'salt1', b'salt2')
