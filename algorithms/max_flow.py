from collections import deque


def bfs_augmenting_path(graph, capacity, flow, s, t, parent):
    visited = {s}
    queue = deque([s])
    while queue:
        u = queue.popleft()
        for v in graph[u]:
            residual = capacity[(u, v)] - flow.get((u, v), 0)
            if v not in visited and residual > 0:
                visited.add(v)
                parent[v] = u
                if v == t:
                    return True
                queue.append(v)
    return False


def max_flow_generator(node_count, edges, s, t, is_directed=False):
    """
    Generator version of Edmonds-Karp Max Flow algorithm for GUI animation.
    Yields ("START"|"STEP"|"FINISHED", data)
    """
    graph = {i: set() for i in range(node_count)}
    capacity = {}

    for u, v, w in edges:
        graph[u].add(v)
        capacity[(u, v)] = capacity.get((u, v), 0) + w
        if not is_directed:
            graph[v].add(u)
            capacity[(v, u)] = capacity.get((v, u), 0) + w
        else:
            if (v, u) not in capacity:
                graph[v].add(u)
                capacity[(v, u)] = 0

    flow = {}
    max_flow_val = 0
    augmenting_paths = []

    yield "START", (0, {}, [], None)

    parent = {}
    while bfs_augmenting_path(graph, capacity, flow, s, t, parent):
        path_flow = float("inf")
        curr = t
        path = []
        while curr != s:
            p = parent[curr]
            path.append(curr)
            residual = capacity[(p, curr)] - flow.get((p, curr), 0)
            path_flow = min(path_flow, residual)
            curr = p
        path.append(s)
        path = path[::-1]

        curr = t
        while curr != s:
            p = parent[curr]
            flow[(p, curr)] = flow.get((p, curr), 0) + path_flow
            flow[(curr, p)] = flow.get((curr, p), 0) - path_flow
            curr = p

        max_flow_val += path_flow
        augmenting_paths.append((path, path_flow))

        # Reconstruct current flow dictionary for edges
        curr_flow = {}
        for u_edge, v_edge, w_edge in edges:
            f_val = flow.get((u_edge, v_edge), 0)
            if not is_directed:
                if f_val < 0:
                    curr_flow[(v_edge, u_edge)] = -f_val
                elif f_val > 0:
                    curr_flow[(u_edge, v_edge)] = f_val
            else:
                if f_val > 0:
                    curr_flow[(u_edge, v_edge)] = f_val

        # Yield each augmenting path and the updated flow
        yield "STEP", (max_flow_val, curr_flow, list(path), path_flow)
        parent = {}

    orig_flow = {}
    for u, v, w in edges:
        f_val = flow.get((u, v), 0)
        if not is_directed:
            if f_val < 0:
                orig_flow[(v, u)] = -f_val
            elif f_val > 0:
                orig_flow[(u, v)] = f_val
        else:
            if f_val > 0:
                orig_flow[(u, v)] = f_val

    yield "FINISHED", (max_flow_val, orig_flow, augmenting_paths)


def max_flow(node_count, edges, s, t, is_directed=False):
    """
    Wrapper version of max_flow returning (max_flow_val, orig_flow, augmenting_paths).
    """
    gen = max_flow_generator(node_count, edges, s, t, is_directed)
    last_val = (0, {}, [])
    while True:
        try:
            step_type, data = next(gen)
            if step_type == "FINISHED":
                last_val = (data[0], data[1], data[2])
        except StopIteration as e:
            if e.value is not None:
                return e.value
            return last_val
