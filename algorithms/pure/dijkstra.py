import heapq


def dijkstra(graph, start):
    """
    Tìm đường đi ngắn nhất từ đỉnh start đến tất cả các đỉnh khác.
    graph: Adjacency list dạng {u: [(v, weight), ...]}
    Trả về: (dist, prev)
    """
    dist = {node: float("inf") for node in graph}
    prev = {node: None for node in graph}
    dist[start] = 0
    pq = [(0, start)]

    while pq:
        current_dist, u = heapq.heappop(pq)
        if current_dist > dist[u]:
            continue

        for v, weight in graph.get(u, []):
            if weight < 0:
                raise ValueError("Dijkstra does not support negative edge weights.")
            candidate = current_dist + weight
            if candidate < dist[v]:
                dist[v] = candidate
                prev[v] = u
                heapq.heappush(pq, (candidate, v))

    return dist, prev
