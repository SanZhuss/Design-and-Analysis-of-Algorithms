import heapq

class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [1] * n
        self.components = n
        self.largest_component_size = 1 if n > 0 else 0

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        rootx, rooty = self.find(x), self.find(y)
        if rootx != rooty:
            if self.rank[rootx] > self.rank[rooty]:
                self.parent[rooty] = rootx
                self.rank[rootx] += self.rank[rooty]
                self.rank[rooty] = self.parent[rootx]
            elif self.rank[rootx] < self.rank[rooty]:
                self.parent[rootx] = rooty
                self.rank[rooty] += self.rank[rootx]
                self.rank[rootx] = 0
            else:
                self.parent[rooty] = rootx
                self.rank[rootx] += self.rank[rooty]
                self.rank[rooty] = 0
            self.largest_component_size = max(self.largest_component_size, max(self.rank[rootx], self.rank[rooty]))
            self.components -= 1

def topsort(v, edges):
    graph = [[] for _ in range(v)]
    for edge in edges:
        u, n = edge[:2]
        graph[u].append(n)

    visited = [False] * v
    path = [False] * v
    acyclic = True
    ordering = [0] * v
    i = v - 1

    def dfs(start, visitedNodes, graph):
        nonlocal acyclic

        stack = [(start, 0)]
        visited[start] = True
        path[start] = True

        while stack:
            n, edgeIndex = stack[-1]

            if edgeIndex < len(graph[n]):
                u = graph[n][edgeIndex]
                stack[-1] = (n, edgeIndex + 1)

                if not visited[u]:
                    visited[u] = True
                    path[u] = True
                    stack.append((u, 0))

                elif path[u]:
                    acyclic = False

            else:
                stack.pop()
                path[n] = False
                visitedNodes.append(n)

    for n in range(v):
        if not visited[n]:
            visitedNodes = []
            dfs(n, visitedNodes, graph)

            for nodeId in visitedNodes:
                ordering[i] = nodeId
                i -= 1

    return acyclic, ordering

"""Implement algorithm bodies. See CONTRACTS.md; inputs and outputs are dictionaries."""
def dsu(request):
    v = request["n"]
    operations = request["operations"]

    components = v
    largest_component_size = 1 if v > 0 else 0
    dsu = DSU(v)
    states = []

    if operations is not None:
        for operation in operations:
            a = operation[0]
            b = operation[1]
            dsu.union(a, b)
            states.append([dsu.components, dsu.largest_component_size])
    return {"states": states}


def kruskal(request):
    v = request["n"]
    edges = request["edges"]
    cost = 0
    edge_ids = []
    dsu = DSU(v)

    for i, edge in enumerate(edges):
        edge.append(i)

    edges.sort(key=lambda edge: [edge[2]])

    for x, y, weight, id in edges:
        rootx = dsu.find(x)
        rooty = dsu.find(y)

        if rootx != rooty:
            cost+=weight
            edge_ids.append(id)
            dsu.union(rootx, rooty)

    return {"cost":cost,"edge_ids":edge_ids,"components":dsu.components}

def prim(request):
    v = request["n"]
    edges = request["edges"]

    min_priority_queue = []
    g = [[] for _ in range(v)]

    for i, (x, y, weight) in enumerate(edges):
        g[y].append((x, weight, i))
        g[x].append((y, weight, i))

    visited = [False] * v

    def addEdges(indexAdd):
        visited[indexAdd] = True

        for y, weight, i in g[indexAdd]:
            if not visited[y]:
                heapq.heappush(
                    min_priority_queue,
                    (weight, y, i)
                )

    mstCost = 0
    edge_ids = []
    edgeCount = 0

    for start in range(v):
        if visited[start]:
            continue

        addEdges(start)

        while min_priority_queue:
            weight, nodeIndex, edgeId = heapq.heappop(
                min_priority_queue
            )

            if visited[nodeIndex]:
                continue

            edge_ids.append(edgeId)
            mstCost += weight

            addEdges(nodeIndex)
            edgeCount += 1


    return {
        "cost": mstCost,
        "edge_ids": edge_ids,
        "components": v - edgeCount
    }

def scc(request):
    def DFS(graph, n, priority, visited):
        stack = [(n, False)]
        while stack:
            vertex, finished = stack.pop()
            if finished:
                priority.append(vertex)
                continue
            if visited[vertex]:
                continue
            visited[vertex] = True
            stack.append((vertex, True))
            for u in reversed(graph[vertex]):
                if not visited[u]:
                    stack.append((u, False))

    def Transpose(graph):
        v = len(graph)
        transpose = [[] for _ in range(v)]
        for n in range(v):
            for neighbor in graph[n]:
                transpose[neighbor].append(n)
        return transpose

    v = request["n"]
    edges = request["edges"]

    graph = [[] for _ in range(v)]
    for u, n in edges:
        graph[u].append(n)
    visited = [False] * v
    priority = []
    for n in range(v):
        if not visited[n]:
            DFS(graph, n, priority, visited)
    transpose = Transpose(graph)
    visited = [False] * v
    component = [-1] * v
    condensation = []
    label = 0

    while priority:
        n = priority.pop()
        if not visited[n]:
            stack = [n]
            visited[n] = True
            while stack:
                vertex = stack.pop()
                component[vertex] = label
                for u in transpose[vertex]:
                    if not visited[u]:
                        visited[u] = True
                        stack.append(u)
            if edges != []:
                if label == 0:
                    condensation.append([label])
                else:
                    condensation[label - 1].append(label)
                    condensation.append([label])    
            label += 1

    return {"component": component, "condensation": condensation[:-1]}

def topo(request):
    v = request["n"]
    edges = request["edges"]

    acyclic, ordering = topsort(v, edges)

    return {"acyclic": acyclic, "order": ordering if acyclic else []}

def dag(request):
    v = request["n"]
    source = request["source"]
    edges = request["edges"]
    acyclic, ordering = topsort(v, edges)
    if not acyclic:
        return {
            "acyclic": False,
            "distance": [],
            "parent_edge": []
        }
    dist = [None] * v
    dist[source] = 0
    parent_edge = [-1] * v
    graph = [[] for _ in range(v)]
    for i, (u, n, weight) in enumerate(edges):
        graph[u].append([n, weight, i])
    for i in range(v):
        nodeIndex = ordering[i]
        if dist[nodeIndex] is not None:
            adjacentEdges = graph[nodeIndex]
            if adjacentEdges is not None:
                for edge in adjacentEdges:
                    neighbor = edge[0]
                    weight = edge[1]
                    edge_index = edge[2]

                    newDist = dist[nodeIndex] + weight

                    if dist[neighbor] is None or newDist < dist[neighbor]:
                        dist[neighbor] = newDist
                        parent_edge[neighbor] = edge_index


    return {"acyclic": acyclic, "distance": dist, "parent_edge": parent_edge}