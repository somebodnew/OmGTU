from collections import defaultdict

def find_eul_cycle(pairs):
    graph = defaultdict(list)
    for pair in pairs:
        graph[pair[0]].append(pair[1])

    cycle = []
    stack = [pairs[0][0]]

    while stack:
        vertex = stack[-1]
        if graph[vertex]:
            stack.append(graph[vertex].pop())
        else:
            cycle.append(stack.pop())
    return cycle[::-1]


for j in range(1, 9):
    f = open(fr"C:\Users\Admin\Downloads\Игра ~Города~\Игра ~Города~\input_s1_{j:02}.txt")
    f2 = open(fr"C:\Users\Admin\Downloads\Игра ~Города~\Игра ~Города~\output_s1_{j:02}.txt")
    right_ans = f2.readlines()
    right_ans = list(map(lambda x: x[:-1], right_ans[:-1])) + [right_ans[-1]]

    pairs = []
    answer = []
    inp = f.readlines()
    inp = list(map(lambda x: x[:-1], inp[:-1])) + [inp[-1]]

    for city in inp:
        pairs.append(city[0] + city[-1])

    while len(pairs) > 0:
        a = find_eul_cycle(pairs)
        answer.append(len(a)-1)
        for i in range(len(a)-1):
            pairs.remove(a[i] + a[i+1])
    answer.sort(reverse=True)
    answer.insert(0, len(answer))
    flag = True
    for i in range(len(answer)):
        if str(answer[i]) != right_ans[i]:
            flag = False
            break
    print(f"Тест {j}: {flag}")
