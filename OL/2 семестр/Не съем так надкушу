def read_input(file_path):
    with open(file_path, 'r') as f:
        data = f.read().split()

    index = 0

    N = int(data[index])
    M = int(data[index + 1])
    index += 2

    splitters = []
    for i in range(0, N):
        splitters.append([int(data[index]), int(data[index + 1])])
        index += 2

    apples = []
    for i in range(0, M):
        apples.append([int(data[index]), int(data[index + 1])])
        index += 2

    X = int(data[index])
    Z = int(data[index + 1])

    return N, M, splitters, apples, X, Z


def filter_sticks(N, sticks, apples, X, Z):
    set = {}
    for i in range(N):
        if X - 1 == i:
            set[i + 1] = sticks[i]
        for a in apples:
            if a[0] - 1 == i and a[1] >= Z:
                set[i + 1] = sticks[i]
        for j in range(N):
            if sticks[j][0] - 1 == i:
                set[i + 1] = sticks[i]
    return set


def find_apples_routes(branches, apples):
    routes = []
    for a in apples:
        route = []
        p = a[0] - 1
        while p != -1 and p + 1 in branches:
            route.append({p + 1: branches[p + 1]})
            p = branches[p + 1][0] - 1
        routes.append(route)
    return routes


def find_worm_way(branches, X):
    way = []
    p = X - 1
    while p != -1 and p + 1 in branches:
        way.append({p + 1: branches[p + 1]})
        p = branches[p + 1][0] - 1
    return way


def find_max_way(branches, apples, X):
    worm_way = find_worm_way(branches, X)
    apple_routes = find_apples_routes(branches, apples)
    routes = []

    for e in apple_routes:
        route = []
        for r in worm_way:
            route.append(r)
        for ee in e:
            if ee not in route:
                route.append(ee)
            else:
                route.remove(ee)
        routes.append(route)

    used_branches = [0, []]
    max_route_length = 0

    for route in routes:
        route_sum = 0
        for e in route:
            for key, value in e.items():
                if e not in used_branches[1]:
                    used_branches[1].append(e)
                    used_branches[0] += value[1]
                route_sum += value[1]
        max_route_length = max(max_route_length, route_sum)

    return max_route_length, used_branches


def Program(input_path):
    N, M, branches, apples, X, Z = read_input(input_path)
    branches = filter_sticks(N, branches, apples, X, Z)
    max_route_length, used_branches = find_max_way(branches, apples, X)

    if max_route_length == 0:
        out_str = "0"
    else:
        out_str = str(used_branches[0] * 2 - max_route_length)

    print(out_str)
    return out_str


for i in range(1, 26):
    input_file_path = rf"C:\Users\Admin\Downloads\Не съем, так надкушу\input_s1_{i:02}.txt"
    file2 = open(fr"C:\Users\Admin\Downloads\Не съем, так надкушу\output_s1_{i:02}.txt")
    print(f"Тест {i}")
    print(file2.readline() + "\n")
