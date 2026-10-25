# Your own tests

- `your_cases.jsonl`: ten independent JSON requests covering DSU updates, Kruskal and Prim with negative/parallel/self-loop edges, SCC condensation, valid and cyclic topological inputs, negative DAG edges, unreachable vertices, and an unreachable cycle.
- `EXPECTED_RESULTS.jsonl`: one reference answer per request in the same order. Different valid MST edge orderings and topological orders are acceptable.
- `ACTUAL_RESULTS.jsonl`: output captured by running `python tools/run.py --input tests/student/your_cases.jsonl` after implementing the algorithms. Regenerate it after any code change; do not type expected output into this file.
- `test_routes.py`: executable checks for a reachable target, the source itself, an unreachable target, selected parent-edge IDs, total route weight, and parallel edges.

Run from the `Assignment3_Sanzhar_Zhussip` directory:

```bash
python tools/run.py --input tests/student/your_cases.jsonl
python tests/student/test_routes.py
python tools/benchmark_mst.py
```

The public suite in `tests/public.json` adds empty graphs, deep chains, 64-bit totals and request-state reset checks.
