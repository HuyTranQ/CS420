def dfs(graph, start, end, limit, solution):
    if limit == 0 and start == end:
        return True, solution
    elif limit > 0:
        for child in graph.data.edge[start]:
            solution.append(child)
            found, result = dfs(graph, child, end, limit - 1, solution)
            if found:
                return True, result
            solution.pop(len(solution) - 1)
    return False, None


def ids_algorithm(graph, start, end):
    sol = [start]
    limit = 0
    while True:
        found, result = dfs(graph, start, end, limit, sol)
        if found:
            return result
        limit += 1
    return None
