import random
import time
import random
import itertools

def generate_permutations(n):
    perm = list(range(1, n+1))
    dir = [-1]*n
    print(perm)

    while True:
        mobile = -1
        mobile_index = -1

        for i in range(n):
            j = i + dir[i]
            if 0 <= j < n and perm[i] > perm[j]:
                if perm[i] > mobile:
                    mobile = perm[i]
                    mobile_index = i

        if mobile == -1:
            break

        j = mobile_index + dir[mobile_index]
        perm[mobile_index], perm[j] = perm[j], perm[mobile_index]
        dir[mobile_index], dir[j] = dir[j], dir[mobile_index]
        mobile_index = j

        for i in range(n):
            if perm[i] > mobile:
                dir[i] *= -1

        print(perm)

def fisher_yates(n):
    a = list(range(1, n+1))
    for i in range(n-1, 0, -1):
        j = random.randint(0, i)
        a[i], a[j] = a[j], a[i]
    return a

def random_sort_shuffle(arr):
    return sorted(arr, key=lambda x: random.random())



def test_algorithm(algo_func, n, repeats=1000):
    times = []
    for i in range(repeats):
        start = time.time()
        fisher_yates(n)
        end = time.time()
        times.append(end-start)
    return sum(times) / repeats


avg_time_fy = test_algorithm(fisher_yates, 1000)
print(f"Фишер-Йейтс (среднее время): {avg_time_fy:.6f} сек")
avg_time_sort = test_algorithm(random_sort_shuffle, 1000)
print(f"Сортировка по случайным ключам: {avg_time_sort:.6f} сек")
avg_time_builtin = test_algorithm(lambda a: random.shuffle(a) or a, 1000)
print(f"Встроенный random.shuffle: {avg_time_builtin:.6f} сек")


