def neighbors(n: int, edges: list[list[int]]) -> list[list[int]]:
    graph = [[] for _ in range(n)]
    for left, right in edges:
        graph[left].append(right)
        graph[right].append(left)
    return graph


def path_exists(n: int, edges: list[list[int]], source: int, target: int) -> bool:
    """True when source can reach target along undirected edges.

    Approach: walk a queue and skip nodes already seen.
    Time: O(n + edges)
    Space: O(n)
    Alternative: the same walk with recursion.
    Common bugs: forgetting that the source is already at the target.
    """
    graph = neighbors(n, edges)
    seen = {source}
    queue = [source]
    while queue:
        node = queue.pop()
        if node == target:
            return True
        for nxt in graph[node]:
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    return False


def component_size(n: int, edges: list[list[int]], source: int) -> int:
    graph = neighbors(n, edges)
    seen = {source}
    queue = [source]
    while queue:
        node = queue.pop()
        for nxt in graph[node]:
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    return len(seen)
