import os
import platform
import time
import statistics
from app.utils.rsa import generate_rsa_key, encrypt_decrypt_rsa
from app.utils.aes import generate_aes_key, encrypt_decrypt_aes
from app.utils.des import generate_3des_key, encrypt_decrypt_3des


def measure_time(func, *args, repeats=10, warmup=2, **kwargs):
    times = []
    for i in range(repeats + warmup):
        start = time.perf_counter()
        func(*args, **kwargs)
        end = time.perf_counter()
        if i >= warmup:
            times.append(end - start)
    return {
        "mean": statistics.mean(times),
        "median": statistics.median(times),
        "p95": statistics.quantiles(times, n=100)[94],
        "raw": times
    }

def benchmark():
    results = {
        "env": {
            "platform": platform.platform(),
            "python_version": platform.python_version(),
        },
        "keygen": {},
        "encryption": {}
    }

    rsa_key_sizes = [2048, 3072]
    for bits in rsa_key_sizes:
        t = measure_time(lambda: generate_rsa_key(bits), repeats=5)
        results["keygen"][f"RSA-{bits}"] = t

    for bits in [128, 256]:
        t = measure_time(lambda: generate_aes_key(bits), repeats=1000)
        results["keygen"][f"AES-{bits}"] = t

    t = measure_time(generate_3des_key, repeats=1000)
    results["keygen"]["3DES"] = t

    # --- Encryption/Decryption ---
    data_sizes = [128, 512, 2048, 8192, 32768, 1048576]  # 1 MB max
    algs = ["AES-128", "AES-256", "3DES"]
    for size in data_sizes:
        data = os.urandom(size)
        results["encryption"][size] = {}

        key_aes128 = generate_aes_key(128)
        key_aes256 = generate_aes_key(256)
        key_3des = generate_3des_key()

        results["encryption"][size]["AES-128"] = measure_time(encrypt_decrypt_aes, data, key_aes128, repeats=10)
        results["encryption"][size]["AES-256"] = measure_time(encrypt_decrypt_aes, data, key_aes256, repeats=10)
        results["encryption"][size]["3DES"] = measure_time(encrypt_decrypt_3des, data, key_3des, repeats=10)

    # RSA small messages
    def rsa_max_message_size(bits: int, hash_len: int = 32) -> int:
        return bits // 8 - 2 * hash_len - 2

    rsa_private_2048 = generate_rsa_key(2048)
    rsa_private_3072 = generate_rsa_key(3072)

    small_sizes = [1, 64, 128, 190, 256, 300]
    for size in small_sizes:
        max_2048 = rsa_max_message_size(2048)
        max_3072 = rsa_max_message_size(3072)

        if size > max_2048:
            continue
        data = os.urandom(size)
        results["encryption"][f"RSA-2048-{size}B"] = measure_time(encrypt_decrypt_rsa, data, rsa_private_2048, repeats=10)

        if size <= max_3072:
            results["encryption"][f"RSA-3072-{size}B"] = measure_time(encrypt_decrypt_rsa, data, rsa_private_3072, repeats=10)

    return results