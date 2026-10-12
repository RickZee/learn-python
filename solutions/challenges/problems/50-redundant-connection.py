def find_redundant(edges: list[list[int]]) -> list[int]:
    """Return the edge that closes a cycle in an undirected graph.

    Approach: union-find; the first edge whose ends share a root is redundant.
    Time: O(E * α(V))
    Space: O(V)
    Alternative: DFS for a back edge (harder to match input order).
    Common bugs: union before the same-component check.
    """
    parent = {}

    def find(x):
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for a, b in edges:
        ra, rb = find(a), find(b)
        if ra == rb:
            return [a, b]
        parent[rb] = ra
    return []
