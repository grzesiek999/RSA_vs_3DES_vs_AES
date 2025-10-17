from typing import Dict
import matplotlib.pyplot as plt
from pathlib import Path

RESULTS_DIR = Path("results")


def create_plot(names: list, data: list, title: str, y_label: str, target_path: str, lim: tuple = None) -> bool:
    plt.figure()
    plt.bar(names, data)
    plt.ylabel(y_label)
    plt.title(title)
    plt.xticks(rotation=30)
    if lim is not None:
        bot_lim = lim[0]
        top_lim = lim[1]
    else:
        bot_lim = None
        top_lim = None
    plt.ylim(bot_lim, top_lim)
    plt.tight_layout()
    if not plt.savefig(RESULTS_DIR / f"{target_path}"):
        return False
    return True

def plot_results(results: Dict):
    keygen = results["keygen"]
    names = list(keygen.keys())
    asym_names = [name for name in names if "RSA" in name]
    sym_names = [name for name in names if "AES" in name or "3DES" in name]
    keys_count = [1, 10, 100, 1000]

    asym_means = []
    sym_means = []

    for count in keys_count:
        for name in asym_names:
            asym_means.append(keygen[name][f"{count}_key"]["mean"])
            create_plot(
                asym_names,
                asym_means,
                "Average time keys generation",
                "Time (s)",
                f"keysgen/asym/{count}_keys_generation.png")
        asym_means.clear()

    for count in keys_count:
        for name in sym_names:
            sym_means.append(keygen[name][f"{count}_key"]["mean"])
            create_plot(
                sym_names,
                sym_means,
                "Average time keys generation",
                "Time (s)",
                f"keysgen/sym/{count}_keys_generation.png",
                (7.8e-7, 8.35e-7))
        sym_means.clear()



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
    plt.savefig(RESULTS_DIR/"throughput/throughput_vs_size.png")