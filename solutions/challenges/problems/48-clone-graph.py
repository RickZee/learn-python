def clone_graph_values(adj: list[list[int]]) -> list[list[int]]:
    """Deep-copy an adjacency-list graph (new neighbor lists).

    Approach: copy each row so the clone does not share list objects.
    For a Node API, map each original node to a new node and walk neighbors.
    Time: O(V + E)
    Space: O(V + E)
    Alternative: serialize then rebuild; BFS with an old→new map.
    Common bugs: shallow copy that aliases inner lists; infinite recursion on cycles without a map.
    """
    return [list(row) for row in adj]
