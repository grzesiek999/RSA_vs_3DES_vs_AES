import json
from pathlib import Path
from app.utils.benchmark import benchmark
from app.utils.plots import plot_results


if __name__ == "__main__":
    print("⏳ Running benchmark cryptographic (RSA, AES, 3DES)...")
    results = benchmark()
    results_path = Path("results/benchmark/results.json")

    with open(results_path, "w") as f:
        json.dump(results, f, indent=2)

    plot_results(results)
    print("✅ Results saved completed.")
    print("✅ Charts saved completed.")
