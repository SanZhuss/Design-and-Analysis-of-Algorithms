"""Reproducible Kruskal/Prim benchmark. Run from this folder or any directory.
Graph construction is outside the timed region; each algorithm call includes
its own adjacency/sort/heap setup. A warm-up call is excluded from timings.
"""
import platform
import random
import statistics
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "Python" / "source"))
from algorithms import kruskal, prim


def make_graph(n, seed):
    rng = random.Random(seed)
    edges = []
    # A chain guarantees connectivity; random additional edges make the graph sparse.
    for u in range(n - 1):
        edges.append([u, u + 1, rng.randint(-1000, 1000)])
    target_m = 3 * n
    while len(edges) < target_m:
        u = rng.randrange(n)
        v = rng.randrange(n)
        if u != v:
            edges.append([u, v, rng.randint(-1000, 1000)])
    return edges


def measure(function, request, repeats=5):
    function(request)  # warm-up; excluded
    samples = []
    for _ in range(repeats):
        start = time.perf_counter()
        answer = function(request)
        samples.append((time.perf_counter() - start) * 1000)
        assert answer["components"] == 1
    return samples, statistics.median(samples)


def main():
    print(f"Python: {platform.python_version()}")
    print(f"Platform: {platform.platform()}")
    print("Timing: perf_counter; graph generation excluded; algorithm setup included; 1 warm-up + 5 measured calls")
    for label, n, seed in [("Small", 200, 20261025), ("Medium", 2000, 20261026), ("Large", 10000, 20261027)]:
        edges = make_graph(n, seed)
        request = {"n": n, "edges": edges}
        k = kruskal(request)
        p = prim(request)
        assert k["cost"] == p["cost"] and k["components"] == p["components"]
        k_samples, k_median = measure(kruskal, request)
        p_samples, p_median = measure(prim, request)
        print(f"{label}: n={n}, m={len(edges)}, seed={seed}")
        print("  Kruskal ms:", ", ".join(f"{x:.3f}" for x in k_samples), f"median={k_median:.3f}")
        print("  Prim ms:   ", ", ".join(f"{x:.3f}" for x in p_samples), f"median={p_median:.3f}")
        print(f"  Correctness: both connected spanning trees; equal cost={k['cost']}")


if __name__ == "__main__":
    main()
