def path_exists(n: int, edges: list[list[int]], source: int, destination: int) -> bool:
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for a, b in edges:
        parent[find(b)] = find(a)
    return find(source) == find(destination)


def always_ready() -> bool:
    return True
