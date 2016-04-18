import sys


def a_star_algorithm(agent , start , goal):
    if start == goal:
        return {'cost' : 0 , 'path' : []}
    opened = {start}
    closed = set()
    previous = {}
    cost = {}
    total = {}
    for node in agent.graph.nodes_iter():
        cost[node] = sys.maxsize
        total[node] = sys.maxsize
    cost[start] = 0
    total[start] = agent.heuristic(start , goal)
    while opened:
        current = start
        max_total = sys.maxsize
        for node in opened:
            if total[node] < max_total:
                max_total = total[node]
                current = node
        if current == goal:
            path = []
            while current in previous:
                path.append(current)
                current = previous[current]
            path.append(start)
            path.reverse()
            return {'cost' : cost[goal] , 'path' : path}
        opened.remove(current)
        closed.add(current)
        yield {'opened' : opened , 'closed' : closed , 'cost' : cost , 'total' : total , 'previous' : previous}
        for neighbor in agent.graph.neighbors(current):
            new_cost = cost[current] + agent.graph[current][neighbor]['cost']
            if new_cost >= cost[neighbor]:
                continue
            elif neighbor in closed:
                opened.add(neighbor)
                closed.remove(neighbor)
            elif neighbor not in opened:
                opened.add(neighbor)
            previous[neighbor] = current
            cost[neighbor] = new_cost
            total[neighbor] = new_cost + agent.heuristic(neighbor , goal)
    return None
