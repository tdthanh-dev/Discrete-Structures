from collections import deque


def bfs(graph, start):
    """
    Duyệt đồ thị theo chiều rộng (BFS).
    graph: Adjacency list dạng {u: [(v, weight), ...]}
    Trả về: (visited_nodes, traversal_edges)
    """
    if start not in graph:
        return [], []
    visited = []
    visited_set = {start}
    queue = deque([start])
    edges = []

    while queue:
        u = queue.popleft()
        visited.append(u)
        for v, w in sorted(graph.get(u, []), key=lambda x: x[0]):
            if v not in visited_set:
                visited_set.add(v)
                queue.append(v)
                edges.append((u, v, w))
    return visited, edges


def dfs(graph, start):
    """
    Duyệt đồ thị theo chiều sâu (DFS) - phiên bản khử đệ quy bằng Stack.
    graph: Adjacency list dạng {u: [(v, weight), ...]}
    Trả về: (visited_nodes, traversal_edges)
    """
    if start not in graph:
        return [], []
    visited = []
    visited_set = {start}
    edges = []

    neighbors = {u: sorted(graph.get(u, []), key=lambda x: x[0]) for u in graph}
    stack = [[start, 0]]
    visited.append(start)

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
                stack.append([v, 0])
        else:
            stack.pop()

    return visited, edges
