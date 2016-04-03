import heapq




def UCS(graph, start, goal):
    frontier = [(0, start, [])]
    explored = []
    while frontier:
        cost, node, path = heapq.heappop(frontier)
        path = path + [start]
        if node == goal:
            return path
        explored.append(node)
        for childnode,childcost in graph.data.edge[start].items():
            a = False
            b = False
            for f in frontier:
                if childnode == f[0]:
                    a = True
            for e in explored:
                if childnode == e:
                    b = True
            if a == True and b == True:
                heapq.heappush(frontier, (cost + childcost, childnode, path))
            elif a == True:
                for idx, f in frontier:
                    if childnode == f[0]:
                        if childcost < cost:
                            frontier[idx] = (childcost, childnode, path)
                            heapq.heapify(frontier)
    return None
