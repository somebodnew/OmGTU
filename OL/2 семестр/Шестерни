from collections import defaultdict

def read_input(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    n, m = map(int, lines[0].strip().split())

    gears = {}
    for i in range(1, n + 1):
        k, rk = map(int, lines[i].strip().split())
        gears[k] = rk

    connections = []
    for i in range(n + 1, n + 1 + m):
        s1, s2 = map(int, lines[i].strip().split())
        connections.append((s1, s2))

    z1, z2 = map(int, lines[n + 1 + m].strip().split())
    v = int(lines[n + 2 + m].strip())

    return n, m, gears, connections, z1, z2, v


def build_graph(connections):
    graph = defaultdict(list)
    for s1, s2 in connections:
        graph[s1].append(s2)
        graph[s2].append(s1)
    return graph


def dfs(node, parent, graph, gears, directions, z1_direction, speed_ratios):
    for neighbor in graph[node]:
        if neighbor == parent:
            continue
        if directions[neighbor] is None:
            directions[neighbor] = -directions[node]
            speed_ratios[neighbor] = speed_ratios[node] * gears[node] / gears[neighbor]
            if not dfs(neighbor, node, graph, gears, directions, z1_direction, speed_ratios):
                return False
        elif directions[neighbor] != -directions[node]:
            return False
    return True


def work(filename):
    n, m, gears, connections, z1, z2, v = read_input(filename)

    graph = build_graph(connections)

    directions = {i: None for i in gears}
    speed_ratios = {i: None for i in gears}

    directions[z1] = v
    speed_ratios[z1] = 1.0

    if not dfs(z1, None, graph, gears, directions, v, speed_ratios):
        return -1, None, None

    if directions[z2] is None:
        return -1, None, None

    w = directions[z2]
    o = speed_ratios[z2]

    return 1, w, o


def press(result):
    if result[0] == -1:
        return f"{result[0]}"
    else:
        return f"{result[0]}\n{result[1]}\n{result[2]:.3f}"


for i in range(1, 14):
    file1 = rf"C:\Users\Admin\Downloads\Шестренки\input_s1_{i:02}.txt"
    file2 = open(rf"C:\Users\Admin\Downloads\Шестренки\output_s1_{i:02}.txt")
    result = work(file1)

    ans = []
    b = file2.readlines()
    for j in range(len(b)-1):
        ans.append(b[j][:-1])
    ans.append(b[-1])

    print(f"Test {i}: {press(result).split() == ans}")
    print(ans)
