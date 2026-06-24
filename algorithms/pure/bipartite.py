def check_bipartite(graph):
    """
    Kiểm tra đồ thị hai phía (2-Coloring).
    graph: Adjacency list dạng {u: [(v, weight), ...]}
    Trả về: (is_bipartite, color_dict_or_odd_cycle)
    """
    color = {}
    parent = {}

    def dfs(u, c):
        color[u] = c
        for v, _ in graph.get(u, []):
            if v not in color:
                parent[v] = u
                cycle = dfs(v, 1 - c)
                if cycle:
                    return cycle
            elif color[v] == color[u]:
                # Tìm thấy chu trình lẻ
                cycle = [v, u]
                curr = u
                while curr in parent and curr != v:
                    curr = parent[curr]
                    cycle.append(curr)
                return cycle[::-1]
        return None

    for node in graph:
        if node not in color:
            cycle = dfs(node, 0)
            if cycle:
                return False, cycle
    return True, color
