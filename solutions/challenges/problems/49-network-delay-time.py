def network_delay(times: list[list[int]], n: int, k: int) -> int:
    """Time for a signal from k to reach every node, or -1.

    Approach: Dijkstra on the directed weighted graph; answer is max dist.
    Time: O((V + E) log V)
    Space: O(V + E)
    Alternative: Bellman-Ford in O(V * E).
    Common bugs: returning the sum of distances; forgetting unreachable → -1.
    """
    import heapq
    from collections import defaultdict

    graph = defaultdict(list)
    for u, v, w in times:
        graph[u].append((v, w))
    dist = {k: 0}
    heap = [(0, k)]
    while heap:
        d, node = heapq.heappop(heap)
        if d > dist.get(node, 10**9):
            continue
        for nxt, w in graph[node]:
            nd = d + w
            if nd < dist.get(nxt, 10**9):
                dist[nxt] = nd
                heapq.heappush(heap, (nd, nxt))
    return max(dist.values()) if len(dist) == n else -1
