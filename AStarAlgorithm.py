import sys


def a_star_algorithm(agent , start , goal, iterate):
    if start == goal:
        return {'cost' : 0 , 'path' : [], 'checked' : 1}
    opened = {start}
    closed = set()
    previous = {}
    cost = {}
    total = {}
    nodes_checked = 0
    for node in agent.graph.nodes_iter():
        cost[node] = sys.maxsize
        total[node] = sys.maxsize
    cost[start] = 0
    if agent.default_heuristic:
        total[start] = agent.heuristic(start , goal)
    else:
        total[start] = agent.lone_heuristic(start)

    while opened:
        nodes_checked += 1
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
            return {'cost' : cost[goal] , 'path' : path, 'checked' : nodes_checked}
        opened.remove(current)
        closed.add(current)
        if iterate:
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
            if agent.default_heuristic:
                total[neighbor] = new_cost + agent.heuristic(neighbor , goal)
            else:
                total[neighbor] = new_cost + agent.lone_heuristic(neighbor)
    return None
