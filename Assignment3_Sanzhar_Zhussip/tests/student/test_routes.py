"""Own route-helper checks required by Assignment 3.
Run from Assignment3_Sanzhar_Zhussip with: python tests/student/test_routes.py
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "Python" / "source"))
from algorithms import dag, reconstruct_route

# Reachable target, negative edge, and a parallel edge with a worse weight.
request = {
    "n": 6,
    "source": 0,
    "edges": [
        [0, 1, 5], [0, 2, 2], [2, 1, -4], [1, 3, 3],
        [2, 3, 8], [4, 5, -2], [0, 2, 9]
    ],
}
result = dag(request)
assert result["acyclic"] is True
assert result["distance"][3] == 1
assert result["parent_edge"][3] == 3
assert reconstruct_route(0, 3, request["edges"], result["parent_edge"], result["distance"]) == [0, 2, 1, 3]
assert [result["parent_edge"][v] for v in [2, 1, 3]] == [1, 2, 3]
assert sum(request["edges"][i][2] for i in [1, 2, 3]) == result["distance"][3]

# Source target must reconstruct to a one-vertex route.
assert reconstruct_route(0, 0, request["edges"], result["parent_edge"], result["distance"]) == [0]

# Vertex 5 is not reachable from source 0, despite its own incoming edge.
assert result["distance"][5] is None
assert reconstruct_route(0, 5, request["edges"], result["parent_edge"], result["distance"]) is None

# Parallel edges: shortest route must use the lower-weight edge ID 1.
parallel = {"n": 2, "source": 0, "edges": [[0, 1, 10], [0, 1, 4]]}
p_result = dag(parallel)
assert p_result["distance"] == [0, 4]
assert p_result["parent_edge"] == [-1, 1]
assert reconstruct_route(0, 1, parallel["edges"], p_result["parent_edge"], p_result["distance"]) == [0, 1]

print("PASS route helper: reachable target -> [0, 2, 1, 3], edge IDs [1, 2, 3], total weight 1")
print("PASS route helper: source target -> [0]")
print("PASS route helper: unreachable target -> None")
print("PASS route helper: parallel edges select edge ID 1 with weight 4")
