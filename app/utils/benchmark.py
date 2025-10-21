import os
import platform
import time
import statistics
from typing import Callable, Any
from app.utils.rsa import generate_rsa_key, encrypt_decrypt_rsa
from app.utils.aes import generate_aes_key, encrypt_decrypt_aes
from app.utils.des import generate_3des_key, encrypt_decrypt_3des


def rsa_max_message_size(bits: int, hash_len: int = 32) -> int:
    return bits // 8 - 2 * hash_len - 2

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

def calc_statistic(results: dict, key_count: list, alg: str, keygen: Callable, bits: int | None = None):
    for count in key_count:
        if bits:
            t = measure_time(lambda: keygen(bits), repeats=count)
            results["keygen"][f"{alg}-{bits}"][f"{count}_key"] = t
        else:
            t = measure_time(generate_3des_key, repeats=count)
            results["keygen"]["3DES"][f"{count}_key"] = t

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
    rsa_key_sizes = [2048, 3072, 4096]
    for bits in rsa_key_sizes:
        results["keygen"][f"RSA-{bits}"] = {}
        calc_statistic(results, key_count, "RSA", generate_rsa_key, bits)

    aes_key_sizes = [128, 256]
    for bits in aes_key_sizes:
        results["keygen"][f"AES-{bits}"] = {}
        calc_statistic(results, key_count, "AES", generate_aes_key, bits)

    results["keygen"]["3DES"] = {}
    calc_statistic(results, key_count, "3DES", generate_3des_key)

    # --- Encryption & Decryption ---
    # AES & 3DES
    data_sizes = [128, 512, 2048, 8192, 32_768, 1_048_576, 4_194_304, 16_777_216]  # [128 B, 512 B, 2 KB, 8 KB, 32 KB, 1 Mb, 4 MB, 16 MB]
    results["encryption"]["sym"] = {}
    for size in data_sizes:
        data = os.urandom(size)
        results["encryption"]["sym"][size] = {}
        key_aes128 = generate_aes_key(128)
        key_aes256 = generate_aes_key(256)
        key_3des = generate_3des_key()

        results["encryption"]["sym"][size]["AES-128"] = measure_time(encrypt_decrypt_aes, data, key_aes128, repeats=1000)
        results["encryption"]["sym"][size]["AES-256"] = measure_time(encrypt_decrypt_aes, data, key_aes256, repeats=1000)
        results["encryption"]["sym"][size]["3DES"] = measure_time(encrypt_decrypt_3des, data, key_3des, repeats=1000)

    # RSA
    rsa_private_2048 = generate_rsa_key(2048)
    rsa_private_3072 = generate_rsa_key(3072)
    rsa_private_4096 = generate_rsa_key(4096)
    small_sizes = [1, 64, 128, 190, 256, 300]
    results["encryption"]["asym"] = {}
    for size in small_sizes:
        max_2048 = rsa_max_message_size(2048)
        max_3072 = rsa_max_message_size(3072)
        max_4096 = rsa_max_message_size(4096)
        if size > max_2048:
            continue
        data = os.urandom(size)
        results["encryption"]["asym"][size] = {}

        results["encryption"]["asym"][size]["RSA-2048"] = measure_time(encrypt_decrypt_rsa, data, rsa_private_2048, repeats=1000)
        if size <= max_3072:
            results["encryption"]["asym"][size]["RSA-3072"] = measure_time(encrypt_decrypt_rsa, data, rsa_private_3072, repeats=1000)
        if size <= max_4096:
            results["encryption"]["asym"][size]["RSA-4096"] = measure_time(encrypt_decrypt_rsa, data, rsa_private_4096, repeats=1000)

    return results