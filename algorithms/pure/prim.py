import heapq


def prim(num_nodes, graph, start=0):
    """
    Tìm cây khung nhỏ nhất (MST) bằng thuật toán Prim.
    graph: Adjacency list dạng {u: [(v, weight), ...]}
    Trả về: (mst_edges, total_weight)
    """
    visited = {start}
    mst = []
    total_weight = 0

    pq = []
    for v, w in graph.get(start, []):
        heapq.heappush(pq, (w, start, v))

    while pq and len(visited) < num_nodes:
        w, u, v = heapq.heappop(pq)
        if v not in visited:
            visited.add(v)
            mst.append((u, v, w))
            total_weight += w
            for to_node, weight in graph.get(v, []):
                if to_node not in visited:
                    heapq.heappush(pq, (weight, v, to_node))

    return mst, total_weight
