import json
from pathlib import Path
from app.utils.benchmark import benchmark
from app.utils.plots import plot_results


if __name__ == "__main__":
    print("⏳ Uruchamiam benchmark kryptograficzny (RSA, AES, 3DES)...")
    results = benchmark()
    results_path = Path("results")

    with open(results_path/"benchmark_results_summary.json", "w") as f:
        json.dump(results, f, indent=2)

    plot_results(results)
    print("✅ Wyniki zapisano w: benchmark_results_summary.json")
    print("✅ Wykresy: keygen_time_vs_keys.png, throughput_vs_size.png")
