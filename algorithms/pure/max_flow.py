from collections import deque


def max_flow(num_nodes, edges, source, sink, is_directed=True):
    """
    Tìm luồng cực đại bằng thuật toán Edmonds-Karp.
    edges: Danh sách cạnh [(u, v, capacity), ...]
    Trả về: (max_flow_value, flow_dict, augmenting_paths)
    """
    adj = {i: {} for i in range(num_nodes)}
    for u, v, cap in edges:
        adj[u][v] = adj[u].get(v, 0) + cap
        if not is_directed:
            adj[v][u] = adj[v].get(u, 0) + cap
        else:
            # Tạo cạnh ngược với dung lượng ban đầu là 0
            if v not in adj[u]:
                adj[u][v] = 0
            if u not in adj[v]:
                adj[v][u] = 0

    flow = {u: {v: 0 for v in adj[u]} for u in adj}
    max_flow_val = 0
    paths = []

    def bfs_find_path():
        parent = {source: None}
        queue = deque([source])
        while queue:
            curr = queue.popleft()
            if curr == sink:
                break
            for neighbor in adj[curr]:
                residual = adj[curr][neighbor] - flow[curr][neighbor]
                if residual > 0 and neighbor not in parent:
                    parent[neighbor] = curr
                    queue.append(neighbor)

        if sink not in parent:
            return None

        path = []
        curr = sink
        while curr is not None:
            path.append(curr)
            curr = parent[curr]
        path.reverse()
        return path

    while True:
        path = bfs_find_path()
        if not path:
            break

        # Tìm bottleneck capacity
        path_flow = float("inf")
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            residual = adj[u][v] - flow[u][v]
            path_flow = min(path_flow, residual)

        # Cập nhật luồng trên các cạnh dọc theo đường đi
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            flow[u][v] += path_flow
            flow[v][u] -= path_flow

        max_flow_val += path_flow
        paths.append((path, path_flow))

    # Lọc luồng thực tế (loại bỏ luồng âm trên các cạnh ngược ảo)
    orig_flow = {}
    for u, v, cap in edges:
        f_val = flow[u].get(v, 0)
        orig_flow[(u, v)] = max(0, f_val)
        if not is_directed:
            f_val_rev = flow[v].get(u, 0)
            orig_flow[(v, u)] = max(0, f_val_rev)

    return max_flow_val, orig_flow, paths
