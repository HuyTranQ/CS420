import heapq


def UCS(graph, start, goal, iterate):
    frontier = [(0, start, [])]
    explored = []
    nodes_checked = 0
    while frontier:
        nodes_checked += 1
        cost, node, path = heapq.heappop(frontier)
        path = path + [node]
        if node == goal:
            return {'path': path, 'cost': cost, 'checked' : nodes_checked}
        #yield {'frontier': frontier, 'explored': explored}
        if iterate:
            yield{'cost': cost, 'node': node, 'path': path, 'start':start, 'goal': goal}
        explored.append(node)
        for childnode,childcost in graph.data.edge[node].items():
            a = False
            b = False
            for f in frontier:
                if childnode == f[1]:
                    a = True
                    break
            for e in explored:
                if childnode == e:
                    b = True
                    break
            if a is not True and b is not True:
                heapq.heappush(frontier, (cost + childcost['cost'], childnode, path))
            elif a is True:
                for idx, f in enumerate(frontier):
                    if childnode == f[1]:
                        if f[0] > childcost['cost'] + cost:
                            frontier[idx] = (cost + childcost['cost'], childnode, path)
                            heapq.heapify(frontier)
                            break
    return None
