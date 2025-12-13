import os
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

class CryptoManager:
  def __init__(self):
    self.ITERATIONS=600_000
    self.LENGTH=32
    
  def generate_salt(self):
    return os.urandom(16)
  
  def generate_mek(self):
    os.urandom(32)
    
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
  
  def encrypt(self, data, key):
    data_bytes = data.encode('utf-8')
    nonce=os.urandom(12)
    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(nonce,data_bytes,None)
    return base64.b64encode(nonce+ciphertext).decode('utf-8')
  
  def decrypt(self,encrypted_string,key,return_bytes=False):
    nonce = base64.b64decode(encrypted_string)[:12]
    ciphertext = base64.b64decode(encrypted_string)[12:]
    aesgcm = AESGCM(key)
    plaintext = aesgcm.decrypt(nonce,ciphertext,None)
    if return_bytes:
      return plaintext # Returns b'\xfa...'
    else:
      return plaintext.decode('utf-8')
  
  def encrypt(self, data, key):
    if isinstance(data,bytes):
      data_bytes = data
    else:
      data_bytes = data.encode('utf-8')
    nonce=os.urandom(12)
    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(nonce,data_bytes,None)
    return base64.b64encode(nonce+ciphertext).decode('utf-8')



if __name__ == "__main__":
    cm = CryptoManager()
    # Fake a key for testing (32 bytes)
    fake_key = os.urandom(32) 

    secret = "My Super Secret Password"
    encrypted = cm.encrypt(secret, fake_key)
    print(f"Encrypted: {encrypted}")

    decrypted = cm.decrypt(encrypted, fake_key)
    print(f"Decrypted: {decrypted}")