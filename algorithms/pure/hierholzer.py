def find_eulerian_path_or_circuit_hierholzer(graph, is_directed=False):
    """
    Tìm đường đi hoặc chu trình Euler bằng thuật toán Hierholzer.
    graph: Adjacency list dạng {u: [(v, weight), ...]}
    Trả về: (path, path_type)
    """
    # Tạo bản sao cục bộ của danh sách kề để xóa cạnh khi duyệt
    adj = {}
    for u in graph:
        adj[u] = []
        for v, _ in graph[u]:
            adj[u].append(v)

    # Tính toán bậc vào/bậc ra (với có hướng) và bậc (với vô hướng)
    in_degree = {u: 0 for u in graph}
    out_degree = {u: 0 for u in graph}
    if is_directed:
        for u in graph:
            out_degree[u] = len(adj[u])
            for v in adj[u]:
                in_degree[v] = in_degree.get(v, 0) + 1

    # Kiểm tra điều kiện tồn tại và chọn đỉnh bắt đầu
    start_node = list(graph.keys())[0] if graph else 0
    path_type = "Chu trinh Euler (Hierholzer)"

    if is_directed:
        start_nodes = []
        end_nodes = []
        for u in graph:
            out_d = out_degree[u]
            in_d = in_degree.get(u, 0)
            if out_d - in_d == 1:
                start_nodes.append(u)
            elif in_d - out_d == 1:
                end_nodes.append(u)
            elif out_d != in_d:
                return [], "Khong co duong di Euler"

        if len(start_nodes) == 1 and len(end_nodes) == 1:
            start_node = start_nodes[0]
            path_type = "Duong di Euler (Hierholzer)"
        elif len(start_nodes) > 1 or len(end_nodes) > 1:
            return [], "Khong co duong di Euler"
    else:
        odd_nodes = []
        for u in graph:
            if len(adj[u]) % 2 != 0:
                odd_nodes.append(u)

        if len(odd_nodes) == 2:
            start_node = odd_nodes[0]
            path_type = "Duong di Euler (Hierholzer)"
        elif len(odd_nodes) > 2 or len(odd_nodes) == 1:
            return [], "Khong co duong di Euler"

    stack = [start_node]
    path = []

    # Duyệt theo thuật toán Hierholzer
    while stack:
        curr = stack[-1]
        if adj.get(curr):
            next_node = adj[curr].pop(0)
            if not is_directed:
                # Xóa cạnh ngược đối với đồ thị vô hướng
                if curr in adj.get(next_node, []):
                    adj[next_node].remove(curr)
            stack.append(next_node)
        else:
            path.append(stack.pop())

    path.reverse()
    return path, path_type
