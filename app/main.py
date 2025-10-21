import json
import threading
from app.utils.benchmark import benchmark
from app.utils.plots import plot_results
from app.utils.animation import blinking_dots


if __name__ == "__main__":
    stop_event = threading.Event()
    t = threading.Thread(target=blinking_dots, args=("⏳ Running benchmark cryptographic (RSA, AES, 3DES)", "✅ Benchmark completed.           ", stop_event))
    t.start()
    results = benchmark()
    stop_event.set()
    t.join()

    with open("results/benchmark/results.json", "w") as f:
        json.dump(results, f, indent=2)
    print("✅ Results saved completed.")

    plot_results(results)
    print("✅ Charts saved completed.")
