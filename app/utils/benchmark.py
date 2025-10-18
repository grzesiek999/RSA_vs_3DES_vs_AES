import os
import platform
import time
import statistics
from app.utils.rsa import generate_rsa_key, encrypt_decrypt_rsa
from app.utils.aes import generate_aes_key, encrypt_decrypt_aes
from app.utils.des import generate_3des_key, encrypt_decrypt_3des


def measure_time(func, *args, repeats=10, warmup=5, **kwargs):
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
        "times_sum": sum(times),
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

    # --- Keys generated times ---
    key_count = [1, 10, 100, 1000]
    rsa_key_sizes = [2048, 3072]
    for bits in rsa_key_sizes:
        results["keygen"][f"RSA-{bits}"] = {}
        for count in key_count:
            t = measure_time(lambda: generate_rsa_key(bits), repeats=count)
            results["keygen"][f"RSA-{bits}"][f"{count}_key"] = t

    for bits in [128, 256]:
        results["keygen"][f"AES-{bits}"] = {}
        for count in key_count:
            t = measure_time(lambda: generate_aes_key(bits), repeats=count)
            results["keygen"][f"AES-{bits}"][f"{count}_key"] = t

    results["keygen"]["3DES"] = {}
    for count in key_count:
        t = measure_time(generate_3des_key, repeats=count)
        results["keygen"]["3DES"][f"{count}_key"] = t


    # --- Encryption & Decryption ---
    # AES & 3DES
    data_sizes = [128, 512, 2048, 8192, 32_768, 1_048_576, 4_194_304, 16_777_216]  # [128 B, 512 B, 2 KB, 8 KB, 32 KB, 1 Mb, 4 MB, 16 MB]
    for size in data_sizes:
        data = os.urandom(size)
        results["encryption"][size] = {}

        key_aes128 = generate_aes_key(128)
        key_aes256 = generate_aes_key(256)
        key_3des = generate_3des_key()

        results["encryption"][size]["AES-128"] = measure_time(encrypt_decrypt_aes, data, key_aes128, repeats=3)
        results["encryption"][size]["AES-256"] = measure_time(encrypt_decrypt_aes, data, key_aes256, repeats=3)
        results["encryption"][size]["3DES"] = measure_time(encrypt_decrypt_3des, data, key_3des, repeats=3)

    # RSA
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
        results["encryption"][f"RSA-2048-{size}B"] = measure_time(encrypt_decrypt_rsa, data, rsa_private_2048, repeats=3)

        if size <= max_3072:
            results["encryption"][f"RSA-3072-{size}B"] = measure_time(encrypt_decrypt_rsa, data, rsa_private_3072, repeats=3)

    return results