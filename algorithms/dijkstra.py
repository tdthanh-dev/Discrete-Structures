import heapq


def dijkstra_generator(graph, start):
    """
    Generator version of Dijkstra's algorithm for GUI animation.
    Yields ("START"|"EXAMINE"|"RELAX"|"SKIP"|"FINISHED", data)
    """
    dist = {node: float("inf") for node in graph}
    prev = {node: None for node in graph}
    dist[start] = 0
    pq = [(0, start)]

    yield "START", (dict(dist), dict(prev), start)

    while pq:
        current_dist, u = heapq.heappop(pq)
        yield "EXAMINE", (dict(dist), dict(prev), u)

        if current_dist > dist[u]:
            continue

        for v, weight in graph[u]:
            if weight < 0:
                raise ValueError("Dijkstra does not support negative edge weights.")
            candidate = current_dist + weight
            if candidate < dist[v]:
                dist[v] = candidate
                prev[v] = u
                heapq.heappush(pq, (candidate, v))
                yield "RELAX", (dict(dist), dict(prev), (u, v, weight, candidate))
            else:
                yield "SKIP", (dict(dist), dict(prev), (u, v, weight))

    yield "FINISHED", (dist, prev)


def dijkstra(graph, start):
    """
    Wrapper version of Dijkstra's algorithm returning (dist, prev).
    """
    gen = dijkstra_generator(graph, start)
    last_val = ({}, {})
    while True:
        try:
            step_type, data = next(gen)
            if step_type == "FINISHED":
                last_val = (data[0], data[1])
        except StopIteration as e:
            if e.value is not None:
                return e.value
            return last_val
