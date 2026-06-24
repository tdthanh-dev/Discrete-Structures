def kruskal_generator(node_count, edges):
    """
    Generator version of Kruskal's algorithm for GUI animation.
    Yields ("START"|"STEP"|"FINISHED", data)
    """
    parent = list(range(node_count))

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    sorted_edges = sorted(edges, key=lambda edge: edge[2])
    mst = []
    total = 0

    yield "START", (list(mst), total, None)

    for u, v, w in sorted_edges:
        root_u, root_v = find(u), find(v)
        if root_u != root_v:
            parent[root_u] = root_v
            mst.append((u, v, w))
            total += w
            # Yield step with edge, showing it was accepted
            yield "STEP", (list(mst), total, (u, v, w), True)
        else:
            # Yield step with edge, showing it was rejected (forms cycle)
            yield "STEP", (list(mst), total, (u, v, w), False)

    yield "FINISHED", (list(mst), total, None)


def kruskal(node_count, edges):
    """
    Wrapper version of Kruskal's algorithm returning (mst, total).
    """
    gen = kruskal_generator(node_count, edges)
    last_val = ([], 0)
    while True:
        try:
            step_type, data = next(gen)
            if step_type == "FINISHED":
                last_val = (data[0], data[1])
        except StopIteration as e:
            if e.value is not None:
                return e.value
            return last_val
