def find_eulerian_path_or_circuit_fleury_generator(graph, is_directed=False):
    """
    Hàm Fleury phiên bản Generator phục vụ cho việc tạo Hoạt họa (Animation) trên GUI.
    Mỗi bước lặp trả về (loại_bước, dữ_liệu)
    """
    if is_directed:
        return None, "Giai thuat Fleury chi ho tro do thi vo huong."

    degree = {u: len(graph.get(u, [])) for u in graph}
    start_vertex = next((u for u in degree if degree[u] > 0), None)
    if start_vertex is None:
        return [], "Do thi khong co canh."

    # Kiểm tra tính liên thông
    visited = set()
    stack = [start_vertex]
    while stack:
        u = stack.pop()
        if u not in visited:
            visited.add(u)
            for v, _ in graph.get(u, []):
                if v not in visited:
                    stack.append(v)
    if any(degree[u] > 0 and u not in visited for u in degree):
        return None, "Do thi khong lien thong."

    # Kiểm tra bậc lẻ
    odd_vertices = [u for u in degree if degree[u] % 2 != 0]
    if len(odd_vertices) == 0:
        start_node = start_vertex
        path_type = "Chu trinh Euler (Fleury)"
    elif len(odd_vertices) == 2:
        start_node = odd_vertices[0]
        path_type = "Duong di Euler (Fleury)"
    else:
        return None, f"Do thi co {len(odd_vertices)} dinh bac le (Fleury yeu cau 0 hoac 2)."

    # Khởi tạo danh sách cạnh với ID duy nhất
    edge_list = []
    edge_id = 0
    for u in graph:
        for v, _ in graph[u]:
            if u < v:
                edge_list.append((edge_id, u, v))
                edge_id += 1
            elif u == v:
                edge_list.append((edge_id, u, u))
                edge_id += 1

    # Dựng sẵn danh sách kề cố định
    full_adj = {}
    for eid, x, y in edge_list:
        full_adj.setdefault(x, []).append((y, eid))
        if x != y:
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

    def is_bridge(u, v, eid, active_edge_ids):
        count1 = dfs_count(u, active_edge_ids)
        count2 = dfs_count(u, active_edge_ids - {eid})
        return count2 < count1

    remaining_ids = set(eid for eid, _, _ in edge_list)
    curr = start_node
    path = [curr]

    # Trả về siêu dữ liệu trước khi chạy vòng lặp chính
    yield "START", (path, path_type, None)

    while remaining_ids:
        # Lấy trực tiếp từ full_adj, tối ưu O(1) bước tìm kiếm
        candidates = [(neighbor, eid) for neighbor, eid in full_adj.get(curr, []) if eid in remaining_ids]
                    
        if not candidates:
            break

        if len(candidates) == 1:
            next_node, eid = candidates[0]
        else:
            non_bridges = [(neighbor, eid) for neighbor, eid in candidates if not is_bridge(curr, neighbor, eid, remaining_ids)]
            if non_bridges:
                next_node, eid = non_bridges[0]
            else:
                next_node, eid = candidates[0]

        remaining_ids.remove(eid)
        path.append(next_node)
        
        # Bắn trạng thái ra cho giao diện cập nhật (Tô màu cạnh vừa đi, highlight đỉnh hiện tại)
        yield "STEP", (list(path), curr, next_node, eid)
        curr = next_node

    yield "FINISHED", (path, path_type, None)


def find_eulerian_path_or_circuit_fleury(graph, is_directed=False):
    """
    Hàm bao tương thích ngược để trả về trực tiếp kết quả chạy cuối cùng.
    """
    gen = find_eulerian_path_or_circuit_fleury_generator(graph, is_directed)
    last_finished = None
    while True:
        try:
            step_type, data = next(gen)
            if step_type == "FINISHED":
                last_finished = (data[0], data[1])
        except StopIteration as e:
            if e.value is not None:
                return e.value
            return last_finished