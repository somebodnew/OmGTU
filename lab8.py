import time
import itertools


def knapsack_brute(items: list[dict], W: int) -> tuple[list, int, int]:
    n = len(items)
    best_cost = 0
    best_subset = []

    for r in range(n + 1):
        for combo in itertools.combinations(range(n), r):
            w = sum(items[i]['weight'] for i in combo)
            c = sum(items[i]['cost']   for i in combo)
            if w <= W and c > best_cost:
                best_cost = c
                best_subset = list(combo)

    selected = [items[i] for i in best_subset]
    total_w  = sum(it['weight'] for it in selected)
    return selected, total_w, best_cost


def knapsack_greedy(items: list[dict], W: int) -> tuple[list, int, int]:
    sorted_items = sorted(items, key=lambda x: x['cost'] / x['weight'], reverse=True)
    selected = []
    total_w = 0
    total_c = 0

    for item in sorted_items:
        if total_w + item['weight'] <= W:
            selected.append(item)
            total_w += item['weight']
            total_c += item['cost']

    return selected, total_w, total_c


# Демонстрация

def print_result(label, selected, w, c, elapsed):
    print(f"\n  [{label}]")
    names = [it['name'] for it in selected]
    print(f"  Предметы  : {names}")
    print(f"  Вес       : {w}")
    print(f"  Стоимость : {c}")
    print(f"  Время     : {elapsed:.6f} с")


def main():
    items = [
        {'name': 'A', 'weight': 2,  'cost': 6},
        {'name': 'B', 'weight': 2,  'cost': 10},
        {'name': 'C', 'weight': 3,  'cost': 12},
        {'name': 'D', 'weight': 5,  'cost': 15},
        {'name': 'E', 'weight': 7,  'cost': 20},
        {'name': 'F', 'weight': 1,  'cost': 4},
        {'name': 'G', 'weight': 4,  'cost': 9},
    ]
    W = 10

    print("=" * 55)
    print("ЗАДАЧА О РЮКЗАКЕ (0/1 Knapsack)")
    print("=" * 55)
    print(f"Грузоподъёмность W = {W}")
    print(f"\n{'Предмет':<10} {'Вес':<8} {'Стоимость':<10} {'Стоим/Вес'}")
    for it in items:
        print(f"{it['name']:<10} {it['weight']:<8} {it['cost']:<10} {it['cost']/it['weight']:.2f}")

    t0 = time.perf_counter()
    sel_b, w_b, c_b = knapsack_brute(items, W)
    elapsed_b = time.perf_counter() - t0

    t0 = time.perf_counter()
    sel_g, w_g, c_g = knapsack_greedy(items, W)
    elapsed_g = time.perf_counter() - t0

    print("\nРезультаты:")
    print_result("Полный перебор O(2^n)", sel_b, w_b, c_b, elapsed_b)
    print_result("Жадный алгоритм O(n log n)", sel_g, w_g, c_g, elapsed_g)

    print("\nАнализ сложности:")
    print("  Полный перебор : O(2^n) — экспоненциальный рост, точный результат")
    print("  Жадный         : O(n log n) — быстро, но не всегда оптимально")
    if c_b != c_g:
        diff = c_b - c_g
        print(f"  Разница в стоимости: {diff} (жадный нашёл не оптимум)")
    else:
        print("  В данном примере жадный совпал с оптимумом")


if __name__ == '__main__':
    main()
