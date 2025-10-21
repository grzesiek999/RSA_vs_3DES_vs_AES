import secrets
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


def generate_aes_key(bits: int):
    return secrets.token_bytes(bits // 8)

def encrypt_decrypt_aes(data: bytes, key: bytes):
    iv = secrets.token_bytes(12)
    encryptor = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend()).encryptor()
    ct = encryptor.update(data) + encryptor.finalize()
    tag = encryptor.tag

    decryptor = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=default_backend()).decryptor()
    pt = decryptor.update(ct) + decryptor.finalize()
    assert pt == data