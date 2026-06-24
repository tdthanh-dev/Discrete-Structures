import heapq


def prim_generator(node_count, graph, start=0):
    """
    Generator version of Prim's algorithm for GUI animation.
    Yields ("START"|"EXAMINE"|"STEP"|"SKIP"|"FINISHED", data)
    """
    if start not in graph:
        return None, "Dinh bat dau khong co trong do thi."

    visited = {start}
    mst = []
    total = 0
    pq = []

    # Yield initial state
    yield "START", (list(visited), list(mst), total)

    # Push all edges from the start node
    for v, w in graph.get(start, []):
        heapq.heappush(pq, (w, start, v))

    while pq and len(visited) < node_count:
        w, u, v = heapq.heappop(pq)
        # Yield that we are examining this edge
        yield "EXAMINE", (list(visited), list(mst), (u, v, w))

        if v not in visited:
            visited.add(v)
            mst.append((u, v, w))
            total += w
            # Yield that we accepted this edge and visited v
            yield "STEP", (list(visited), list(mst), (u, v, w))

            for next_v, next_w in graph.get(v, []):
                if next_v not in visited:
                    heapq.heappush(pq, (next_w, v, next_v))
        else:
            # Yield that we skipped this edge because it would form a cycle
            yield "SKIP", (list(visited), list(mst), (u, v, w))

    yield "FINISHED", (list(visited), list(mst), total)


def prim(node_count, graph, start=0):
    """
    Wrapper version of Prim's algorithm returning (mst, total).
    """
    gen = prim_generator(node_count, graph, start)
    last_val = ([], 0)
    while True:
        try:
            step_type, data = next(gen)
            if step_type == "FINISHED":
                last_val = (data[1], data[2])
        except StopIteration as e:
            if e.value is not None:
                return e.value
            return last_val
