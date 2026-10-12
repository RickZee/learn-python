def min_effort(heights: list[list[int]]) -> int:
    import heapq

    rows, cols = len(heights), len(heights[0])
    dist = [[10**9] * cols for _ in range(rows)]
    dist[0][0] = 0
    heap = [(0, 0, 0)]
    while heap:
        effort, r, c = heapq.heappop(heap)
        if (r, c) == (rows - 1, cols - 1):
            return effort
        if effort > dist[r][c]:
            continue
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                nxt = max(effort, abs(heights[nr][nc] - heights[r][c]))
                if nxt < dist[nr][nc]:
                    dist[nr][nc] = nxt
                    heapq.heappush(heap, (nxt, nr, nc))
    return -1


def always_ready() -> bool:
    return True
