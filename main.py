import time
import random
import psutil
import matplotlib.pyplot as plt

def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result


def quick_sort(arr):
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]

    return quick_sort(left) + middle + quick_sort(right)

def measure(func, data):
    try:
        import pyRAPL
        return measure_with_pyrapl(func, data)
    except Exception:
        pass

    try:
        from pyJoules.energy_meter import EnergyContext
        return measure_with_pyjoules(func, data)
    except Exception:
        pass

    return measure_with_model(func, data)


def measure_with_pyrapl(func, data):
    import pyRAPL
    pyRAPL.setup()
    meter = pyRAPL.Measurement("energy")

    start = time.perf_counter()
    meter.begin()
    func(data)
    meter.end()
    end = time.perf_counter()

    energy = meter.result.pkg + meter.result.dram

    return {"time": end - start, "energy": energy, "method": "pyRAPL"}


def measure_with_pyjoules(func, data):
    from pyJoules.energy_meter import EnergyContext
    from pyJoules.handler.pandas_handler import PandasHandler

    handler = PandasHandler()

    start = time.perf_counter()
    with EnergyContext(handler=handler):
        func(data)
    end = time.perf_counter()

    energy = handler.get_dataframe().sum().sum()

    return {"time": end - start, "energy": energy, "method": "pyJoules"}


P_IDLE = 20   # Watt
P_MAX = 65    # Watt

def measure_with_model(func, data):
    psutil.cpu_percent(interval=None)

    start = time.perf_counter()
    func(data)
    end = time.perf_counter()

    cpu_usage = psutil.cpu_percent(interval=None) / 100
    duration = end - start

    power = P_IDLE + (P_MAX - P_IDLE) * cpu_usage
    energy = power * duration

    return {"time": duration, "energy": energy, "method": "model-based"}


def benchmark(func, data, runs=5):
    times, energies = [], []
    method = None

    for _ in range(runs):
        r = measure(func, data.copy())
        times.append(r["time"])
        energies.append(r["energy"])
        method = r["method"]

    return {
        "avg_time": sum(times) / runs,
        "avg_energy": sum(energies) / runs,
        "method": method
    }


if __name__ == "__main__":
    import random
    import matplotlib.pyplot as plt

    # Kullanıcıdan input al
    user_input = input(
        "Girdi boyutlarını virgülle ayırarak gir (örn: 1000,5000,20000): "
    )
    sizes = [int(x.strip()) for x in user_input.split(",")]

    algorithms = {
        "MergeSort": merge_sort,
        "QuickSort": quick_sort
    }

    results = {
        "MergeSort": {"n": [], "time": [], "energy": []},
        "QuickSort": {"n": [], "time": [], "energy": []}
    }

    # Benchmark
    for n in sizes:
        print(f"\n📌 Input Size: n = {n}")
        data = [random.randint(0, 100000) for _ in range(n)]

        for name, algo in algorithms.items():
            r = benchmark(algo, data, runs=5)

            print(f"🔹 {name}")
            print(f"   Avg Time   : {r['avg_time']:.6f} s")
            print(f"   Avg Energy : {r['avg_energy']:.6f} J")
            print(f"   Method     : {r['method']}")

            results[name]["n"].append(n)
            results[name]["time"].append(r["avg_time"])
            results[name]["energy"].append(r["avg_energy"])

    # ----------------------------
    # Energy Graph
    # ----------------------------
    plt.figure(figsize=(8,5))
    for name in algorithms:
        plt.plot(
            results[name]["n"],
            results[name]["energy"],
            marker="o",
            label=name
        )

    plt.xlabel("Input Size (n)")
    plt.ylabel("Energy (Joule)")
    plt.title("Energy Complexity Comparison")
    plt.legend()
    plt.grid(True)
    plt.xlim(0, max(sizes)*1.05)        # X ekseni sıfırdan başlasın
    plt.ylim(0, max(max(results[a]["energy"]) for a in algorithms)*1.05)  # Y ekseni sıfırdan başlasın
    plt.show()

    # ----------------------------
    # Time Graph
    # ----------------------------
    plt.figure(figsize=(8,5))
    for name in algorithms:
        plt.plot(
            results[name]["n"],
            results[name]["time"],
            marker="o",
            label=name
        )

    plt.xlabel("Input Size (n)")
    plt.ylabel("Time (seconds)")
    plt.title("Time Complexity Comparison")
    plt.legend()
    plt.grid(True)
    plt.xlim(0, max(sizes)*1.05)
    plt.ylim(0, max(max(results[a]["time"]) for a in algorithms)*1.05)
    plt.show()