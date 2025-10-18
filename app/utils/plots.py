from typing import Dict
import matplotlib.pyplot as plt
from pathlib import Path

RESULTS_DIR = Path("results")


def create_plot(
        names: list,
        data: list,
        title: str,
        y_label: str,
        target_path: str,
        lim: tuple = None) -> bool:

    # --- func ---
    plt.figure()
    plt.bar(names, data)
    plt.ylabel(y_label)
    plt.title(title)
    plt.xticks(rotation=30)

    if lim:
        plt.ylim(lim[0], lim[1])

    plt.tight_layout()
    plt.savefig(RESULTS_DIR / f"{target_path}")
    plt.close()
    return True


def plot_results(results: Dict):
    keygen = results["keygen"]
    names = list(keygen.keys())
    asym_names = [name for name in names if "RSA" in name]
    sym_names = [name for name in names if "AES" in name or "3DES" in name]

    # --- Generated keys time ---
    keys_count = [1, 10, 100, 1000]
    for count in keys_count:
        asym_means = []
        for name in asym_names:
            try:
                asym_means.append(keygen[name][f"{count}_key"]["mean"])
            except KeyError:
                print(f"No data found for {name} ({count} keys)")
        if asym_means:
            create_plot(
                asym_names,
                asym_means,
                "Average time keys generation",
                "Time (s)",
                f"keysgen/asym/{count}_keys_generation.png"
            )

    asym_total_time = []
    for name in asym_names:
        try:
            asym_total_time.append(keygen[name]["1000_key"]["times_sum"])
        except KeyError:
            print(f"No data found for {name} (1000 keys)")
    if asym_total_time:
        create_plot(
            asym_names,
            asym_total_time,
            "Total time 1000 keys generation",
            "Time (s)",
            "keysgen/asym/total_time.png"
        )

    for count in keys_count:
        sym_means = []
        for name in sym_names:
            try:
                sym_means.append(keygen[name][f"{count}_key"]["mean"])
            except KeyError:
                print(f"No data found for {name} ({count} keys)")
        if sym_means:
            create_plot(
                sym_names,
                sym_means,
                "Average time keys generation",
                "Time (s)",
                f"keysgen/sym/{count}_keys_generation.png",
                (7.75e-7, 8.5e-7)
            )

    sym_total_time = []
    for name in sym_names:
        try:
            sym_total_time.append(keygen[name]["1000_key"]["times_sum"])
        except KeyError:
            print(f"No data found for {name} (1000 keys)")
    if sym_total_time:
        create_plot(
            sym_names,
            sym_total_time,
            "Total time 1000 keys generation",
            "Time (s)",
            "keysgen/sym/total_time.png"
        )


    # --- Encryption & decryption ---
    sizes = []
    for k in results["encryption"].keys():
        if isinstance(k, int):
            sizes.append(k)
    sizes.sort()

    for alg in ["AES-128", "AES-256", "3DES"]:
        throughputs = [
            (size / 1_000_000) / results["encryption"][size][alg]["mean"]
            for size in sizes
        ]
        plt.plot(sizes, throughputs, marker="o", label=alg)
'''
    plt.xscale("log")
    plt.xlabel("Rozmiar danych (B)")
    plt.ylabel("Przepustowość (MB/s)")
    plt.title("Przepustowość szyfrowania+deszyfrowania")
    plt.legend()
    plt.tight_layout()'''
    plt.savefig(RESULTS_DIR/"throughput/throughput_vs_size.png")