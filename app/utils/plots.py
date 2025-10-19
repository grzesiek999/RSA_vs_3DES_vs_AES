from typing import Dict
import matplotlib.pyplot as plt
from pathlib import Path

RESULTS_DIR = Path("results")


def get_sizes(results: dict, alg_type: str) -> list:
    sizes = []
    for k in results["encryption"][f"{alg_type}"].keys():
        if isinstance(k, int):
            sizes.append(k)
    sizes.sort()
    return sizes

def calculate_throughputs(results: dict, names: list, sizes: list, alg_type: str) -> dict:
    throughputs = {
        alg: [
            (size / 1_048_576) / results["encryption"][f"{alg_type}"][size][alg]["mean"]
            for size in sizes
        ] for alg in names
    }
    return throughputs

def get_total_times(keygen: dict, names:list, count: int) -> list:
    total_times = []
    for name in names:
        try:
            total_times.append(keygen[name][f"{count}_key"]["times_sum"])
        except KeyError:
            print(f"No data found for {name} ({count} keys)")
    return total_times

def get_means(keygen: dict, names:list, count: int) -> list:
    means = []
    for name in names:
        try:
            means.append(keygen[name][f"{count}_key"]["mean"])
        except KeyError:
            print(f"No data found for {name} ({count} keys)")
    return means

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
    # --- keysgen ---
    keygen = results["keygen"]
    names = list(keygen.keys())
    asym_names = [name for name in names if "RSA" in name]
    sym_names = [name for name in names if "AES" in name or "3DES" in name]
    keys_count = [1, 10, 100, 1000]

    for count in keys_count:
        asym_means = get_means(keygen, asym_names, count)
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
        else: raise Exception("Asymmetric keys generation means data not found !")

    asym_total_times = get_total_times(keygen, asym_names, 1000)
    if asym_total_times:
        create_chart(
            names=asym_names,
            data=asym_total_times,
            type="bar",
            title="Total time 1000 keys generation",
            ylabel="Time (s)",
            xlabel="Algorithm",
            target_path="keysgen/asym/total_time.png"
        )
    else: raise Exception("Asymmetric keys generation total time data not found !")

    for count in keys_count:
        sym_means = get_means(keygen, sym_names, count)
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
        else: raise Exception("Symmetric keys generation means data not found !")

    sym_total_times = get_total_times(keygen, sym_names, 1000)
    if sym_total_times:
        create_chart(
            names=sym_names,
            data=sym_total_times,
            type="bar",
            title="Total time 1000 keys generation",
            ylabel="Time (s)",
            xlabel="Algorithm",
            target_path="keysgen/sym/total_time.png"
        )
    else: raise Exception("Symmetric keys generation total time data not found !")

    # --- encdec ---


    # --- throughput ---
    asym_sizes = get_sizes(results,"asym")
    if asym_sizes:
        asym_throughputs = calculate_throughputs(results, asym_names, asym_sizes, "asym")
        if asym_throughputs:
            create_chart(
                names=asym_sizes,
                data=asym_throughputs,
                type="plot",
                title="Throughput",
                ylabel="Throughput (MB/s)",
                xlabel="Data size (Bytes)",
                target_path="throughput/asym/throughput.png",
                xscale="log",
                legend=True
            )
        else: raise Exception("Asymetric algorithm throughputs data not found !")
    else: raise Exception("Asymetric algorithm sizes data not found !")

    sym_sizes = get_sizes(results,"sym")
    if sym_sizes:
        sym_throughputs = calculate_throughputs(results, sym_names, sym_sizes, "sym")
        if sym_throughputs:
            create_chart(
                names=sym_sizes,
                data=sym_throughputs,
                type="plot",
                title="Throughput",
                ylabel="Throughput (MB/s)",
                xlabel="Data size (Bytes)",
                target_path="throughput/sym/throughput.png",
                xscale="log",
                legend=True
            )
        else: raise Exception("Symetric algorithm throughputs data not found !")
    else: raise Exception("Symetric algorithm sizes data not found !")