from networkx import nx


def ids_algorithm(graph, start, end):
    max_limit = 0

    nodes_checked = 0

    # assume maximum depth must be the number of nodes n in the graph (branching factor = 1)
    # then return failure if the depth limit surpass n
    while max_limit <= len(nx.nodes(graph.graph)):
        depth_changed = True
        limit = 0
        solution = []
        cost = [0]
        opened = [(start, 0, 0)]

        # search until limit reaches 0
        while len(opened) > 0:
            cur = opened.pop(0)
            nodes_checked += 1
            while len(solution) != cur[1]:
                solution.pop(len(solution) - 1)
                cost.pop(len(cost) - 1)
            solution.append(cur[0])
            cost.append(cost[len(cost) - 1] + cur[2])

            if len(solution) == max_limit:
                yield {'depth changed' : depth_changed, 'current path' : solution,
                       'opened' : opened, 'cost' : cost[1:len(cost)]}

            if limit > cur[1]:
                limit = cur[1]

            if limit == max_limit and cur[0] == end:    # a solution is found
                return {'path' : solution, 'cost' : cost[len(cost) - 1], 'checked' : nodes_checked}
            elif limit < max_limit:
                if limit == cur[1]:
                    limit += 1
                elif limit > cur[1]:
                    limit = cur[1]

                # get all child nodes
                tmp = []
                for child in graph.graph.edges_iter(cur[0], data=True):
                    tmp.append((child[1], limit, child[2]['cost']))

                opened = tmp + opened
                
                depth_changed = False

        # increase depth limit
        max_limit += 1

    return None
