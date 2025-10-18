from typing import Dict
import matplotlib.pyplot as plt
from pathlib import Path

RESULTS_DIR = Path("results")


def create_chart(
        names: list,
        data,
        type: str,
        title: str,
        ylabel: str,
        xlabel: str,
        target_path: str,
        lim: tuple = None,
        xscale: str = None,
        yscale: str = None,
        legend: bool = False) -> bool:

    plt.figure()
    if type == "bar":
        plt.bar(names, data)
    elif type == "plot":
        if isinstance(data, dict):
            for label, value in data.items():
                plt.plot(names, value, marker="o", label=label)
        else:
            plt.plot(names, data, marker="o")
    else:
        raise TypeError(f"Unknown type: {type}")

    # --- Base chart settings ---
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)

    # --- Optional chart settings ---
    if yscale:
        plt.yscale(yscale)
    if xscale:
        plt.xscale(xscale)
    if lim:
        plt.ylim(lim[0], lim[1])
    if legend:
        plt.legend()

    plt.tight_layout()
    plt.savefig(RESULTS_DIR / f"{target_path}")
    plt.close()
    return True


def plot_results(results: Dict):
    keygen = results["keygen"]
    names = list(keygen.keys())
    asym_names = [name for name in names if "RSA" in name]
    sym_names = [name for name in names if "AES" in name or "3DES" in name]

    # --- keysgen ---
    keys_count = [1, 10, 100, 1000]
    for count in keys_count:
        asym_means = []
        for name in asym_names:
            try:
                asym_means.append(keygen[name][f"{count}_key"]["mean"])
            except KeyError:
                print(f"No data found for {name} ({count} keys)")
        if asym_means:
            create_chart(
                names=asym_names,
                data=asym_means,
                type="bar",
                title="Average time keys generation",
                ylabel="Time (s)",
                xlabel="Algorithm",
                target_path=f"keysgen/asym/{count}_keys_generation.png"
            )

    asym_total_time = []
    for name in asym_names:
        try:
            asym_total_time.append(keygen[name]["1000_key"]["times_sum"])
        except KeyError:
            print(f"No data found for {name} (1000 keys)")
    if asym_total_time:
        create_chart(
            names=asym_names,
            data=asym_total_time,
            type="bar",
            title="Total time 1000 keys generation",
            ylabel="Time (s)",
            xlabel="Algorithm",
            target_path="keysgen/asym/total_time.png"
        )

    for count in keys_count:
        sym_means = []
        for name in sym_names:
            try:
                sym_means.append(keygen[name][f"{count}_key"]["mean"])
            except KeyError:
                print(f"No data found for {name} ({count} keys)")
        if sym_means:
            create_chart(
                names=sym_names,
                data=sym_means,
                type="bar",
                title="Average time keys generation",
                ylabel="Time (s)",
                xlabel="Algorithm",
                target_path=f"keysgen/sym/{count}_keys_generation.png",
            )

    sym_total_time = []
    for name in sym_names:
        try:
            sym_total_time.append(keygen[name]["1000_key"]["times_sum"])
        except KeyError:
            print(f"No data found for {name} (1000 keys)")
    if sym_total_time:
        create_chart(
            names=sym_names,
            data=sym_total_time,
            type="bar",
            title="Total time 1000 keys generation",
            ylabel="Time (s)",
            xlabel="Algorithm",
            target_path="keysgen/sym/total_time.png"
        )


    # --- encdec ---
    # TO DO


    # --- throughput ---
    '''
    asym_throughputs = {
        alg: [
            (size / 1_048_576) / results["encryption"][alg]["mean"]
            for size in sizes
        ] for alg in ["RSA-2048-1B", "RSA-3072-1B", "RSA-2048-64B", "RSA-3072-64B", "RSA-2048-128B", "RSA-3072-128B", "RSA-2048-190B", "RSA-3072-190B"]
    }
    '''
    sizes = []
    for k in results["encryption"].keys():
        if isinstance(k, int):
            sizes.append(k)
    sizes.sort()

    sym_throughputs = {
        alg: [
            (size / 1_048_576) / results["encryption"][size][alg]["mean"]
            for size in sizes
        ] for alg in ["AES-128", "AES-256", "3DES"]
    }

    create_chart(
        names=sizes,
        data=sym_throughputs,
        type="plot",
        title="Throughput",
        ylabel="Throughput (MB/s)",
        xlabel="Data size (Bytes)",
        target_path="throughput/sym/throughput.png",
        xscale="log",
        legend=True
    )