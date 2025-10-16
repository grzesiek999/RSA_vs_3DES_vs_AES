from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding as asympad
from cryptography.hazmat.backends import default_backend


def generate_rsa_key(bits: int):
    return rsa.generate_private_key(public_exponent=65537, key_size=bits, backend=default_backend())

def encrypt_decrypt_rsa(data: bytes, private_key):
    public_key = private_key.public_key()
    ciphertext = public_key.encrypt(
        data,
        asympad.OAEP(
            mgf=asympad.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    plaintext = private_key.decrypt(
        ciphertext,
        asympad.OAEP(
            mgf=asympad.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    assert plaintext == data