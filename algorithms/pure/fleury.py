def find_eulerian_path_or_circuit_fleury(graph, is_directed=False):
    """
    Tìm đường đi hoặc chu trình Euler bằng thuật toán Fleury.
    graph: Adjacency list dạng {u: [(v, weight), ...]}
    Trả về: (path, path_type, edges_visited)
    """
    # Xây dựng danh sách cạnh
    edge_list = []
    edge_id = 0
    adj_local = {u: [] for u in graph}
    for u in graph:
        for v, _ in graph[u]:
            if not is_directed:
                if u <= v:
                    edge_list.append((edge_id, u, v))
                    adj_local[u].append((v, edge_id))
                    adj_local[v].append((u, edge_id))
                    edge_id += 1
            else:
                edge_list.append((edge_id, u, v))
                adj_local[u].append((v, edge_id))
                edge_id += 1

    num_edges = len(edge_list)
    active_edges = set(range(num_edges))

    # Đếm số đỉnh bậc lẻ (với đồ thị vô hướng)
    odd_nodes = []
    if not is_directed:
        for u in graph:
            deg = len(adj_local[u])
            if deg % 2 != 0:
                odd_nodes.append(u)

    # Chọn đỉnh bắt đầu
    start_node = list(graph.keys())[0] if graph else 0
    path_type = "Chu trinh Euler (Fleury)"
    if not is_directed:
        if len(odd_nodes) == 2:
            start_node = odd_nodes[0]
            path_type = "Duong di Euler (Fleury)"
        elif len(odd_nodes) > 2 or len(odd_nodes) == 1:
            return [], "Khong co duong di Euler", []

    curr = start_node
    path = [curr]
    visited_edges = []

    # Helper function đếm số đỉnh có thể đi tới từ u dùng DFS
    full_adj = {}
    for eid, x, y in edge_list:
        full_adj.setdefault(x, []).append((y, eid))
        if not is_directed and x != y:
            full_adj.setdefault(y, []).append((x, eid))

    def dfs_count(u, active_edge_ids):
        visited_nodes = {u}
        stack = [u]
        while stack:
            curr_node = stack.pop()
            for neighbor, eid in full_adj.get(curr_node, []):
                if eid in active_edge_ids and neighbor not in visited_nodes:
                    visited_nodes.add(neighbor)
                    stack.append(neighbor)
        return len(visited_nodes)

    while active_edges:
        next_edge = None
        candidates = []
        for neighbor, eid in adj_local[curr]:
            if eid in active_edges:
                candidates.append((neighbor, eid))

        if not candidates:
            break

        if len(candidates) == 1:
            next_edge = candidates[0]
        else:
            # Ưu tiên chọn cạnh không phải cầu
            for neighbor, eid in candidates:
                # Đếm số đỉnh liên thông trước khi xóa
                count_before = dfs_count(curr, active_edges)

                # Thử xóa cạnh
                active_edges.remove(eid)
                count_after = dfs_count(curr, active_edges)

                # Hoàn trả
                active_edges.add(eid)

                if count_after == count_before:
                    next_edge = (neighbor, eid)
                    break

            # Nếu tất cả đều là cầu, chọn cạnh đầu tiên
            if not next_edge:
                next_edge = candidates[0]

        neighbor, eid = next_edge
        active_edges.remove(eid)
        visited_edges.append((curr, neighbor))
        curr = neighbor
        path.append(curr)

    if len(path) != num_edges + 1:
        return [], "Do thi khong lien thong", []

    return path, path_type, visited_edges
