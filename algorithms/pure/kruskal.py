def kruskal(num_nodes, edges):
    """
    Tìm cây khung nhỏ nhất (MST) bằng thuật toán Kruskal.
    edges: Danh sách cạnh dạng [(u, v, weight), ...]
    Trả về: (mst_edges, total_weight)
    """
    parent = list(range(num_nodes))

    def find(i):
        path = []
        while parent[i] != i:
            path.append(i)
            i = parent[i]
        for node in path:
            parent[node] = i
        return i

    def union(i, j):
        root_i = find(i)
        root_j = find(j)
        if root_i != root_j:
            parent[root_i] = root_j
            return True
        return False

    sorted_edges = sorted(edges, key=lambda item: item[2])
    mst = []
    total_weight = 0

    for u, v, w in sorted_edges:
        if union(u, v):
            mst.append((u, v, w))
            total_weight += w
            if len(mst) == num_nodes - 1:
                break

    return mst, total_weight
