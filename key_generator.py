import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# Function to generate a cryptographically secure random 16-byte salt
def generate_salt():
  salt = os.urandom(16)
  return salt

password = "Mysecretpass"
bpass = password.encode('utf-8')   # Convert password string to bytes (required for PBKDF2)

# Generate two different salts:
salt_auth = generate_salt()  # Salt for deriving the authentication key (e.g., login verification)
salt_enc = generate_salt()   # Salt for deriving the encryption key (e.g., encrypting stored data)

# PBKDF2 instance for deriving authentication key
authkey = PBKDF2HMAC(
  algorithm = hashes.SHA256(),  # Hash algorithm used in PBKDF2
  length = 32,                  # Output key size (32 bytes = 256-bit key)
  salt = salt_auth,             # Unique salt for authentication
  iterations = 600000,          # High iteration count for brute-force resistance
)

# PBKDF2 instance for deriving encryption key
enckey = PBKDF2HMAC(
  algorithm = hashes.SHA256(),  # Same hashing algorithm
  length = 32,                  # 256-bit encryption key
  salt = salt_enc,              # Different salt → produces a different key for encryption
  iterations = 600000,          # Same iteration count for security
)

# Derive keys using the password bytes
auth_hash = authkey.derive(bpass)          # Authentication key (used for verifying login password)
encryption_key = enckey.derive(bpass)      # Encryption key (used for encrypting vault data)

# Print keys in hex format for readability
print(f"Auth key is: {auth_hash.hex()} \nEncryption key is: {encryption_key.hex()}")
