import secrets
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, modes
from cryptography.hazmat.decrepit.ciphers import algorithms
from cryptography.hazmat.backends import default_backend


def generate_3des_key():
    return secrets.token_bytes(24)

def encrypt_decrypt_3des(data: bytes, key: bytes):
    iv = secrets.token_bytes(8)
    cipher = Cipher(algorithms.TripleDES(key), modes.CBC(iv), backend=default_backend())
    padder = padding.PKCS7(64).padder()
    padded = padder.update(data) + padder.finalize()

    enc = cipher.encryptor().update(padded) + cipher.encryptor().finalize()

    dec = cipher.decryptor().update(enc) + cipher.decryptor().finalize()
    unpadder = padding.PKCS7(64).unpadder()
    unpadded = unpadder.update(dec) + unpadder.finalize()
    assert unpadded == data