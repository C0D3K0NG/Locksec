import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class CryptoManager:
  def __init__(self):
    self.ITERATIONS=600_000
    self.LENGTH=32
    
  def generate_salt(self):
    return os.urandom(16)
  
  def derive_keys(self,password,salt_auth,salt_enc):
    password=password.encode('utf-8')
    # Salt for Authentication
    auth = PBKDF2HMAC(
      algorithm=hashes.SHA256(),
      length=self.LENGTH,
      iterations=self.ITERATIONS,
      salt=salt_auth
    )
  
    # Salt for Encryption key
    enc = PBKDF2HMAC(
      algorithm=hashes.SHA256(),
      length=self.LENGTH,
      iterations=self.ITERATIONS,
      salt=salt_enc
    )
    authkey=auth.derive(password)
    enckey=enc.derive(password)
    return(authkey.hex(),enckey)
    
    
if __name__ == "__main__":
    cm = CryptoManager()
    s1 = cm.generate_salt()
    s2 = cm.generate_salt()
    a_hash, e_key = cm.derive_keys("testpass", s1, s2)
    print(f"Auth: {a_hash}")
    print(f"Key: {e_key.hex()}")