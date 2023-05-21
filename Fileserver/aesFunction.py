import base64
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2

BLOCK_SIZE = 16
pad = lambda cip: cip + (BLOCK_SIZE - len(cip) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(cip) % BLOCK_SIZE)
unpad = lambda cip: cip[:-ord(cip[len(cip) - 1:])]
AES_PASSPHRASE = "asdasdasd"

def get_private_key(passphrase):
    salt = b"qweqweqwe"
    kdf = PBKDF2(passphrase, salt , 64, 1000)
    key = kdf[:32]
    return key

AES_PASSWORD = get_private_key(AES_PASSPHRASE)

def encrypt(raw):
    raw = pad(raw)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(AES_PASSWORD, AES.MODE_CBC, iv)
    return base64.b64encode(iv + cipher.encrypt(raw.encode("utf-8")))

def decrypt(enc):
    enc = base64.b64decode(enc)
    iv = enc[:16]
    cipher = AES.new(AES_PASSWORD, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(enc[16:]))
