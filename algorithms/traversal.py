from collections import deque


def bfs_generator(graph, start):
    """
    Generator version of BFS for GUI animation.
    Yields ("START"|"STEP"|"FINISHED", data)
    """
    if start not in graph:
        return None, "Dinh bat dau khong co trong do thi."
    visited = []
    visited_set = {start}
    queue = deque([start])
    edges = []

    yield "START", (list(visited), list(edges), list(queue))

    while queue:
        u = queue.popleft()
        visited.append(u)
        yield "STEP", (list(visited), list(edges), list(queue), u, None)

        # Sort neighbors by vertex index for a deterministic traversal order
        for v, w in sorted(graph.get(u, []), key=lambda x: x[0]):
            if v not in visited_set:
                visited_set.add(v)
                queue.append(v)
                edges.append((u, v, w))
                yield "STEP", (list(visited), list(edges), list(queue), u, (u, v, w))

    yield "FINISHED", (visited, edges)


def dfs_generator(graph, start):
    """
    Generator version of DFS for GUI animation.
    Yields ("START"|"STEP"|"FINISHED", data)
    """
    if start not in graph:
        return None, "Dinh bat dau khong co trong do thi."
    visited = []
    visited_set = {start}
    edges = []

    neighbors = {u: sorted(graph.get(u, []), key=lambda x: x[0]) for u in graph}
    stack = [[start, 0]]
    visited.append(start)

    yield "START", (list(visited), list(edges), [s[0] for s in stack])

    while stack:
        u, idx = stack[-1]
        u_neighbors = neighbors.get(u, [])
        if idx < len(u_neighbors):
            v, w = u_neighbors[idx]
            stack[-1][1] += 1
            if v not in visited_set:
                visited_set.add(v)
                visited.append(v)
                edges.append((u, v, w))
                yield "STEP", (list(visited), list(edges), [s[0] for s in stack], u, (u, v, w))
                stack.append([v, 0])
        else:
            stack.pop()
            yield "STEP", (list(visited), list(edges), [s[0] for s in stack], u, None)

    yield "FINISHED", (visited, edges)


def bfs(graph, start):
    """
    Wrapper version of BFS returning (visited_nodes, traversal_edges).
    """
    gen = bfs_generator(graph, start)
    last_val = ([], [])
    while True:
        try:
            step_type, data = next(gen)
            if step_type == "FINISHED":
                last_val = (data[0], data[1])
        except StopIteration as e:
            if e.value is not None:
                return e.value
            return last_val


def dfs(graph, start):
    """
    Wrapper version of DFS returning (visited_nodes, traversal_edges).
    """
    gen = dfs_generator(graph, start)
    last_val = ([], [])
    while True:
        try:
            step_type, data = next(gen)
            if step_type == "FINISHED":
                last_val = (data[0], data[1])
        except StopIteration as e:
            if e.value is not None:
                return e.value
            return last_val
