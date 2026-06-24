import re


def to_adjacency_matrix(nodes_count, edges, is_directed):
    matrix = [[0] * nodes_count for _ in range(nodes_count)]
    for u, v, w in edges:
        if u < nodes_count and v < nodes_count:
            matrix[u][v] = w
            if not is_directed:
                matrix[v][u] = w
    return "\n".join(" ".join(map(str, row)) for row in matrix)


def to_adjacency_list(nodes_count, edges, is_directed):
    adj = {i: [] for i in range(nodes_count)}
    for u, v, w in edges:
        if u < nodes_count and v < nodes_count:
            adj[u].append((v, w))
            if not is_directed:
                adj[v].append((u, w))
    lines = []
    for i in range(nodes_count):
        neighbors = sorted(adj[i], key=lambda x: x[0])
        neighbors_str = ", ".join(f"{v}({w})" for v, w in neighbors)
        lines.append(f"{i}: {neighbors_str}")
    return "\n".join(lines)


def to_edge_list(edges, is_directed):
    seen = set()
    result = []
    for u, v, w in sorted(edges):
        key = (u, v) if is_directed else tuple(sorted((u, v)))
        if key not in seen:
            seen.add(key)
            result.append(f"{u} {v} {w}")
    return "\n".join(result)


def parse_adjacency_matrix(text):
    lines = [line.strip() for line in text.strip().split("\n") if line.strip()]
    matrix = [[int(x) for x in line.split()] for line in lines]
    n = len(matrix)
    edges = []
    for i in range(n):
        for j in range(len(matrix[i])):
            w = matrix[i][j]
            if w != 0:
                edges.append((i, j, w))
    return n, edges


def parse_adjacency_list(text):
    lines = [line.strip() for line in text.strip().split("\n") if line.strip()]
    edges = []
    n = 0
    for line in lines:
        match = re.match(r"^(\d+)\s*:\s*(.*)$", line)
        if match:
            u = int(match.group(1))
            n = max(n, u + 1)
            neighbors_part = match.group(2).strip()
            if neighbors_part:
                items = re.findall(r"(\d+)\s*\(\s*(\-?\d+)\s*\)", neighbors_part)
                for v_str, w_str in items:
                    v = int(v_str)
                    w = int(w_str)
                    n = max(n, v + 1)
                    edges.append((u, v, w))
    return n, edges


def parse_edge_list(text):
    lines = [line.strip() for line in text.strip().split("\n") if line.strip()]
    edges = []
    n = 0
    for line in lines:
        parts = [int(x) for x in line.split()]
        if len(parts) >= 2:
            u, v = parts[0], parts[1]
            w = parts[2] if len(parts) > 2 else 1
            n = max(n, u + 1, v + 1)
            edges.append((u, v, w))
    return n, edges
