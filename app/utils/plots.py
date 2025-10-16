from typing import Dict
import matplotlib.pyplot as plt
from pathlib import Path

RESULTS_DIR = Path("results")

def plot_results(results: Dict):
    keygen = results["keygen"]
    names = list(keygen.keys())
    means = [keygen[k]["mean"] for k in names]
    plt.figure()
    plt.bar(names, means)
    plt.ylabel("Średni czas (s)")
    plt.title("Czas generowania kluczy")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig(RESULTS_DIR/"keygen_time_vs_keys.png")

    # Encryption throughput
    sizes = []
    for k in results["encryption"].keys():
        if isinstance(k, int):  # tylko dla AES/3DES
            sizes.append(k)
    sizes.sort()

    for alg in ["AES-128", "AES-256", "3DES"]:
        throughputs = [
            (size / 1_000_000) / results["encryption"][size][alg]["mean"]
            for size in sizes
        ]
        plt.plot(sizes, throughputs, marker="o", label=alg)

    plt.xscale("log")
    plt.xlabel("Rozmiar danych (B)")
    plt.ylabel("Przepustowość (MB/s)")
    plt.title("Przepustowość szyfrowania+deszyfrowania")
    plt.legend()
    plt.tight_layout()
    plt.savefig(RESULTS_DIR/"throughput_vs_size.png")