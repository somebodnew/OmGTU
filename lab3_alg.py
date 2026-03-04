import itertools
import time
import matplotlib.pyplot as plt
import numpy as np

def narayana_permutations(n):
    arr = list(range(1, n + 1))
    perms = [arr.copy()]
    
    while True:
        i = n - 2
        while i >= 0 and arr[i] >= arr[i + 1]:
            i -= 1
        if i < 0:
            break
            
        j = n - 1
        while arr[j] <= arr[i]:
            j -= 1
            
        arr[i], arr[j] = arr[j], arr[i]
        
        arr[i + 1:] = reversed(arr[i + 1:])
        perms.append(arr.copy())
    
    return perms

def johnson_trotter_permutations(n):
    elements = list(range(1, n + 1))
    perms = [elements.copy()]
    
    def generate(k):
        if k <= 1:
            return
        generate(k - 1)
        for i in range(k - 1):
            if k % 2 == 0:
                elements[i], elements[k - 1] = elements[k - 1], elements[i]
            else:
                elements[0], elements[k - 1] = elements[k - 1], elements[0]
            perms.append(elements.copy())
        generate(k - 1)
    
    if n > 1:
        generate(n)
    return perms

def inversion_permutations(n):
    perms = []
    
    inv_vectors = []
    current = [0] * n
    
    while True:
        inv_vectors.append(current.copy())
    
        i = n - 1
        while i >= 0 and current[i] == n - 1 - i:
            i -= 1
        if i < 0:
            break
            
        current[i] += 1
        for j in range(i + 1, n):
            current[j] = 0
    
    for inv in inv_vectors:
        numbers = list(range(1, n + 1))
        perm = []
        for i in range(n - 1, -1, -1):
            perm.insert(inv[i], numbers.pop())
        perms.append(perm)
    
    return perms

def task1_demo():
    print("\n" + "="*60)
    print("ЗАДАНИЕ 1: Сравнение алгоритмов генерации перестановок")
    print("="*60)
    
    algorithms = [
        ("Нарайаны", narayana_permutations),
        ("Джонсона-Троттера", johnson_trotter_permutations),
        ("Вектор инверсий", inversion_permutations)
    ]

    n_values = [2, 3, 4, 5, 6, 7, 8, 9, 10]
    results = {name: [] for name, _ in algorithms}
    
    print("\nИзмерение времени выполнения (в секундах):")
    print("-" * 60)
    print(f"{'n':<5} | {'Нарайаны':<16} | {'Джонсона-Троттера':<10} | {'Вектор инверсий':<15}")
    print("-" * 60)
    
    for n in n_values:
        print(f"{n:<5} |", end=" ")
        
        for name, func in algorithms:
            start_time = time.time()
            perms = func(n)
            end_time = time.time()
            
            exec_time = end_time - start_time
            results[name].append(exec_time)
            
            print(f"{exec_time:.6f}         | ", end=" ")
        print()
    
    print("-" * 60)
    
    plt.figure(figsize=(12, 8))
    
    for name, _ in algorithms:
        plt.plot(n_values, results[name], marker='o', linewidth=2, markersize=8, label=name)
    
    plt.xlabel('n (длина перестановки)', fontsize=12)
    plt.ylabel('Время выполнения (секунды)', fontsize=12)
    plt.title('Сравнение алгоритмов генерации перестановок', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=11)
    plt.yscale('log')
    
    plt.tight_layout()
    plt.savefig('permutations_comparison.png', dpi=300, bbox_inches='tight')
    plt.show()


def permutations_with_repeats(elements):
    perms = set(itertools.permutations(elements))
    return sorted(perms)

def task2_demo():
    print("\n" + "="*60)
    print("ЗАДАНИЕ 2: Перестановки с повторениями")
    print("="*60)
    
    examples = [
        [1, 2, 1],
        [1, 2, 3],
        [1, 1, 1]
    ]
    
    for example in examples:
        print(f"\nИсходная последовательность: {example}")
        result = permutations_with_repeats(example)
        print(f"Уникальные перестановки ({len(result)}):")
        for p in result:
            print(f"  {p}")


def all_combinations(items):
    result = []
    n = len(items)
    
    for r in range(1, n + 1):
        for combo in itertools.combinations(items, r):
            result.append(combo)
    
    return result

def task3_demo():
    print("\n" + "="*60)
    print("ЗАДАНИЕ 3: Все возможные выборки")
    print("="*60)
    
    items = ["стол", "стул", "шкаф"]
    print(f"Исходные элементы: {items}")
    
    choices = all_combinations(items)
    print(f"\nВсе выборки (всего {len(choices)}):")
    for i, choice in enumerate(choices, 1):
        print(f"{i}. {choice}")


def find_best_purchase(needs, prices, budget):
    best_combo = []
    max_items = 0
    
    all_items = []
    for item, needed in needs.items():
        if item in prices:
            price = prices[item]
            max_possible = min(needed, budget // price if price > 0 else needed)
            all_items.extend([(item, price)] * max_possible)
    
    n = len(all_items)
    for r in range(1, n + 1):
        for combo in itertools.combinations(all_items, r):
            total = sum(price for _, price in combo)
            if total <= budget and len(combo) > max_items:
                max_items = len(combo)
                best_combo = combo
    
    result = {}
    for item, price in best_combo:
        result[item] = result.get(item, 0) + 1
    
    return result

def task4_demo():
    print("\n" + "="*60)
    print("ЗАДАНИЕ 4: Покупка канцелярских принадлежностей")
    print("="*60)
    
    needs = {
        "ручка": 5,
        "карандаш": 3,
        "тетрадь": 10,
        "линейка": 2,
        "ластик": 1
    }
    
    prices = {
        "ручка": 10,
        "карандаш": 5,
        "тетрадь": 15,
        "линейка": 20,
        "ластик": 8
    }
    
    budget = 100
    
    print(f"Нужно купить: {needs}")
    print(f"Цены: {prices}")
    print(f"Бюджет: {budget} руб.\n")
    
    purchase = find_best_purchase(needs, prices, budget)
    
    if purchase:
        print("Оптимальная покупка (максимум наименований):")
        total = 0
        for item, qty in purchase.items():
            cost = qty * prices[item]
            total += cost
            print(f"  {item}: {qty} шт. × {prices[item]} руб. = {cost} руб.")
        print(f"\nИтого: {total} руб.")
        print(f"Всего наименований: {len(purchase)}")
        print(f"Остаток: {budget - total} руб.")
    else:
        print("Ничего нельзя купить")



    
task1_demo()
task2_demo()
task3_demo()
task4_demo()
    
