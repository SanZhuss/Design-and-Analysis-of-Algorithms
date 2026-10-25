
- **DSU (path compression + union by size, component size/largest):** Each vertex starts as its own parent and has size 1. `find` follows parent links and applies path compression; `union` finds both roots and attaches the smaller tree to the larger one, updating the root size, component count and largest component size only when two different components are joined. Repeated unions and self-unions leave the state unchanged, and the empty graph starts with zero components and largest size 0. Each request creates a new `DSU`, so state does not leak across input lines; the amortized time is O(n + q α(n)) and memory is O(n + q) including the returned states.

- **Kruskal (sorted original edges + DSU, forest of all components):** The method sorts a decorated copy of the input edges by weight and edge ID, so the caller's input list is not modified. It accepts an edge only when its endpoints currently have different DSU roots; this avoids cycles and the cut property makes each accepted lightest crossing edge safe for a minimum spanning forest. Negative weights are valid, self-loops are naturally rejected, and disconnected or isolated vertices remain separate components. Time is O(n + m log(m + 1)) and memory is O(n + m), including the sorted copy and result.

- **Prim (adjacency lists + heap, restart for each component):** The method builds an undirected adjacency list carrying the original edge ID, then grows a tree by repeatedly taking the cheapest edge that reaches an unvisited vertex. Stale heap entries and self-loops are skipped when their destination is already visited; the outer loop restarts at every remaining vertex, so disconnected graphs produce a forest and isolated vertices count as components. It is independent of Kruskal and may choose different edge IDs for equal-cost optima. With a lazy heap its time is O(n + m log(m + 1)) and memory is O(n + m).

- **Kosaraju SCC and exact condensation:** The first DFS pass records vertices in finish order, and the second pass visits the transposed graph in decreasing finish order to assign one label per strongly connected component. Both DFS passes use explicit stacks, avoiding Python's recursion-depth limit on long chains. After labels are assigned, the algorithm scans the original edges and adds only pairs whose endpoints have different labels to a set; this removes duplicate condensation edges and excludes internal edges. Every request builds fresh graphs and arrays. Time and memory are O(n + m) expected, including the set of unique condensation edges.

- **DFS topological order (three states, reverse postorder, cycles anywhere):** Each vertex is white (unvisited), gray (currently active) or black (finished). The iterative DFS stores the next outgoing-edge index on the stack; an edge to a gray vertex proves a directed cycle, while an edge to a black vertex does not. When a vertex finishes it is appended to postorder, and reversing this list gives a valid topological order if no cycle was found. The outer loop starts DFS from every vertex, so cycles in disconnected parts are detected too; explicit stacks avoid call-stack failure. Time and memory are O(n + m).

- **DAG shortest paths and route helper:** The algorithm first checks the whole directed graph for cycles; any cycle causes `acyclic=false` with empty distance and parent arrays, even if the cycle is unreachable from the source. Otherwise it relaxes outgoing edges in topological order, allowing negative weights and never relaxing from an unreachable (`None`) distance. `parent_edge[v]` stores the input edge ID that reaches `v`, not the predecessor vertex; source and unreachable vertices use -1. `reconstruct_route` follows these edge IDs backward, returns `[source]` for the source, a source-to-target vertex list for a reachable target, and `None` for an unreachable target. Time and memory are O(n + m) for the DAG computation; route reconstruction takes O(route length) time and output space. Every request allocates fresh local state.

## Kruskal versus Prim

Both methods were first checked on the same connected generated graph at each size. Graph generation is outside the timed region; each algorithm call includes its own internal sorting/adjacency/heap setup, but excludes JSON parsing, I/O and graph generation. One warm-up call per algorithm and graph was excluded. Each row contains five measured calls, and the reported median is in milliseconds. The same generated edge list was passed to both methods. Runtime environment: Python 3.13.5, Linux 6.18.55 x86_64, AMD EPYC 9V74 80-Core Processor (5 logical CPUs visible to the process). Reproduce from the Assignment 3 directory with `python tools/benchmark_mst.py`; the script records the exact random seed for each graph.

| Size | n | m | Kruskal measurements (ms) | Median (ms) | Prim measurements (ms) | Median (ms) |
|---|---:|---:|---|---:|---|---:|
| Small | 200 | 600 | 0.301, 0.305, 0.299, 0.312, 0.297 | 0.301 | 0.320, 0.299, 0.396, 0.348, 0.295 | 0.320 |
| Medium | 2,000 | 6,000 | 4.735, 4.529, 4.500, 4.805, 4.506 | 4.529 | 4.950, 5.160, 5.160, 5.101, 4.892 | 5.101 |
| Large | 10,000 | 30,000 | 33.492, 35.926, 34.361, 32.859, 34.478 | 34.361 | 58.902, 79.202, 58.000, 111.919, 46.022 | 58.902 |

For each size, both algorithms returned a connected spanning tree with the same total cost: -118186 (small), -1238996 (medium) and -6275141 (large). In this run Kruskal was slightly faster on the small graph and faster on the medium and large graphs. Prim's large-graph timings varied more, illustrating that short benchmarks are affected by runtime noise and environment load. These measurements support a comparison of these implementations on these sparse inputs; they do not prove asymptotic complexity or mean Kruskal is always faster. Different graph densities and runtimes may change the result.

## My tests and route reconstruction

The custom JSONL inputs are in `tests/student/your_cases.jsonl`, expected reference answers are in `tests/student/EXPECTED_RESULTS.jsonl`, and actual program output is recorded in `tests/student/ACTUAL_RESULTS.jsonl`. Run them from this directory using `python tools/run.py --input tests/student/your_cases.jsonl`. Expected answers are semantic: a valid minimum spanning forest or topological order can differ in edge/order sequence when multiple optimal answers exist.

The cases cover repeated/self unions and component-size updates; negative, parallel and self-loop edges for both MST methods; several SCCs with duplicate cross-component edges; a DAG with multiple valid orders; a disconnected graph with a cycle; negative DAG weights; unreachable vertices; and a cycle unreachable from the DAG source. The public test suite additionally covers empty inputs, deep chains, 64-bit sums and repeated request batches in one process. The route helper has separate executable assertions in `tests/student/test_routes.py`.

Route helper evidence from `python tests/student/test_routes.py`:

- Reachable target 3: `reconstruct_route(0, 3, edges, parent_edge, distance)` returns `[0, 2, 1, 3]`. Selected parent edge IDs are `[1, 2, 3]`, corresponding to weights 2, -4 and 3; their sum is 1, equal to `distance[3]`.
- Source target 0: `reconstruct_route(0, 0, edges, parent_edge, distance)` returns `[0]`.
- Unreachable target 5: its distance is `None`, and `reconstruct_route(0, 5, edges, parent_edge, distance)` returns `None` (the no-route representation).
- Parallel-edge case: between 0 and 1, edge ID 1 with weight 4 is selected instead of edge ID 0 with weight 10; the route is `[0, 1]` and the distance is 4.

## Assistance and sources

I used ChatGPT for debugging suggestions, test-case planning and some explanations. I reviewed and ran the code and tests in this submission, and I am responsible for understanding the implementation and verifying the final result. The assignment repository's `CONTRACTS.md`, `TESTING.md` and `RUBRIC.md` were used as the specification for required input/output behavior and edge cases. Benchmark numbers above are measured results from the included benchmark script in the stated runtime environment, not theoretical estimates.
