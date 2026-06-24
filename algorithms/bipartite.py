def check_bipartite_generator(graph):
    """
    Generator version of Bipartite graph check for GUI animation.
    Yields ("START"|"COLOR"|"CONFLICT"|"FINISHED", data)
    """
    color = {}
    parent = {}

    yield "START", (dict(color), None)

    for start_node in graph:
        if start_node not in color:
            # Iterative DFS for coloring and odd cycle detection
            stack = [(start_node, 0)]
            color[start_node] = 0
            yield "COLOR", (dict(color), start_node, 0, None)

            while stack:
                u, c = stack[-1]
                unvisited_found = False
                for v, _ in graph[u]:
                    if v not in color:
                        color[v] = 1 - c
                        parent[v] = u
                        stack.append((v, 1 - c))
                        unvisited_found = True
                        yield "COLOR", (dict(color), v, 1 - c, (u, v))
                        break
                    elif color[v] == color[u]:
                        # Found an odd cycle (conflict)
                        cycle = [v, u]
                        curr = u
                        while curr in parent and curr != v:
                            curr = parent[curr]
                            cycle.append(curr)
                        cycle = cycle[::-1]
                        yield "CONFLICT", (dict(color), cycle, (u, v))
                        yield "FINISHED", (False, cycle)
                        return

                if not unvisited_found:
                    stack.pop()

    yield "FINISHED", (True, color)


def check_bipartite(graph):
    """
    Wrapper version of check_bipartite returning (is_bipartite, color_dict_or_odd_cycle).
    """
    gen = check_bipartite_generator(graph)
    last_val = (True, {})
    while True:
        try:
            step_type, data = next(gen)
            if step_type == "FINISHED":
                last_val = (data[0], data[1])
        except StopIteration as e:
            if e.value is not None:
                return e.value
            return last_val
