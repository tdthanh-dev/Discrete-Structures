def find_eulerian_path_or_circuit_hierholzer_generator(graph, is_directed=False):
    """
    Generator version of Hierholzer's algorithm for GUI animation.
    Yields ("START"|"PUSH"|"POP"|"FINISHED", data)
    """
    if is_directed:
        return None, "Giai thuat Hierholzer chi ho tro do thi vo huong."

    # 1. Calculate degrees
    degree = {u: len(graph.get(u, [])) for u in graph}

    # 2. Check connectivity for vertices with edges
    start_vertex = next((u for u in degree if degree[u] > 0), None)
    if start_vertex is None:
        return [], "Do thi khong co canh."

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
        return None, "Do thi khong lien thong (xet cac dinh co canh)."

    # 3. Find odd degree vertices
    odd_vertices = [u for u in degree if degree[u] % 2 != 0]

    if len(odd_vertices) == 0:
        start_node = start_vertex
        path_type = "Chu trinh Euler (Hierholzer)"
    elif len(odd_vertices) == 2:
        start_node = odd_vertices[0]
        path_type = "Duong di Euler (Hierholzer)"
    else:
        return None, f"Do thi co {len(odd_vertices)} dinh bac le (yeu cau phai la 0 hoac 2)."

    # 4. Hierholzer's Algorithm
    adj = {u: {} for u in graph}
    for u in graph:
        for v, w in graph[u]:
            adj[u][v] = adj[u].get(v, 0) + 1

    stack = [start_node]
    path = []

    yield "START", (list(stack), list(path), path_type)

    while stack:
        u = stack[-1]
        neighbors = [v for v in adj[u] if adj[u][v] > 0]
        if neighbors:
            v = neighbors[0]
            adj[u][v] -= 1
            adj[v][u] -= 1
            stack.append(v)
            yield "PUSH", (list(stack), list(path), (u, v))
        else:
            popped = stack.pop()
            path.append(popped)
            yield "POP", (list(stack), list(path), popped)

    final_path = path[::-1]
    yield "FINISHED", (final_path, path_type)


def find_eulerian_path_or_circuit_hierholzer(graph, is_directed=False):
    """
    Wrapper version of find_eulerian_path_or_circuit_hierholzer returning (path, path_type).
    """
    gen = find_eulerian_path_or_circuit_hierholzer_generator(graph, is_directed)
    last_val = ([], "")
    while True:
        try:
            step_type, data = next(gen)
            if step_type == "FINISHED":
                last_val = (data[0], data[1])
        except StopIteration as e:
            if e.value is not None:
                return e.value
            return last_val
