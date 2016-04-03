import heapq




def UCS(graph, start, goal):
    frontier = [(0, start, [])]
    explored = []
    while frontier:
        cost, node, path = heapq.heappop(frontier)
        path = path + [node]
        if node == goal:
            return path
        explored.append(node)
        for childnode,childcost in graph.data.edge[node].items():
            a = False
            b = False
            for f in frontier:
                if childnode == f[1]:
                    a = True
            for e in explored:
                if childnode == e:
                    b = True
            if a != True and b != True:
                heapq.heappush(frontier, (cost + childcost['cost'], childnode, path))
            elif a == True:
                for idx, f in enumerate(frontier):
                    if childnode == f[1]:
                        if childcost['cost'] < cost:
                            frontier[idx] = (cost + childcost['cost'], childnode, path)
                            heapq.heapify(frontier)
                            break
    return None
