"""
Лабораторная работа 7 — Жадные алгоритмы
Задача 1: Планирование заказов (максимальная суммарная стоимость)
Задача 2: Детский утренник (минимальное количество групп)
"""

import time


# ─────────────────────────────────────────────
# Задача 1: Планирование заказов
# ─────────────────────────────────────────────

def schedule_orders(orders: list[dict]) -> tuple[list, int]:
    """
    Жадный алгоритм: сортируем заказы по убыванию стоимости,
    затем жадно ставим каждый заказ на максимально поздний
    свободный слот до его дедлайна.

    orders — список словарей {'name', 'deadline', 'cost'}
    Возвращает (выбранные заказы, суммарную стоимость).

    Сложность: O(n log n) — сортировка + O(n*m) назначение слотов
    (m — максимальный дедлайн), на практике почти O(n log n).
    """
    # Сортировка по убыванию стоимости
    sorted_orders = sorted(orders, key=lambda o: o['cost'], reverse=True)

    max_deadline = max(o['deadline'] for o in orders)
    # slots[i] = None означает, что день i свободен (дни 1..max_deadline)
    slots = [None] * (max_deadline + 1)

    selected = []
    total_cost = 0

    for order in sorted_orders:
        # Ищем последний свободный слот <= deadline
        for day in range(order['deadline'], 0, -1):
            if slots[day] is None:
                slots[day] = order['name']
                selected.append(order)
                total_cost += order['cost']
                break

    # Расписание по дням
    schedule = {day: slots[day] for day in range(1, max_deadline + 1) if slots[day]}
    return selected, total_cost, schedule


# ─────────────────────────────────────────────
# Задача 2: Детский утренник — минимум групп
# ─────────────────────────────────────────────

def min_groups(children: list[dict]) -> list[list]:
    """
    Жадный алгоритм: сортируем детей по возрасту,
    затем проходим и добавляем ребёнка в текущую группу,
    если его возраст не больше чем на 2 года отличается
    от возраста первого ребёнка группы; иначе — новая группа.

    Сложность: O(n log n) — сортировка, O(n) — один проход.
    """
    sorted_children = sorted(children, key=lambda c: c['age'])
    groups = []
    current_group = []
    group_start_age = None

    for child in sorted_children:
        if group_start_age is None or child['age'] - group_start_age > 2:
            current_group = [child]
            group_start_age = child['age']
            groups.append(current_group)
        else:
            current_group.append(child)

    return groups


# ─────────────────────────────────────────────
# Демонстрация
# ─────────────────────────────────────────────


print("=" * 55)
print("ЗАДАЧА 1: Планирование заказов")
print("=" * 55)

orders = [
    {'name': 'A', 'deadline': 2, 'cost': 40},
    {'name': 'B', 'deadline': 1, 'cost': 25},
    {'name': 'C', 'deadline': 2, 'cost': 30},
    {'name': 'D', 'deadline': 1, 'cost': 15},
    {'name': 'E', 'deadline': 3, 'cost': 20},
]

print("Заказы:")
print(f"{'Заказ':<8} {'Дедлайн':<10} {'Стоимость'}")
for o in orders:
    print(f"{o['name']:<8} {o['deadline']:<10} {o['cost']}")

t0 = time.perf_counter()
selected, total, schedule = schedule_orders(orders)
elapsed = time.perf_counter() - t0

print(f"\nВыбранные заказы: {[o['name'] for o in selected]}")
print(f"Суммарная стоимость: {total}")
print("Расписание:")
for day, name in sorted(schedule.items()):
    print(f"  День {day}: заказ {name}")
print(f"\nВремя выполнения: {elapsed:.6f} с")

# ───────────────────────────────────────────
print("\n" + "=" * 55)
print("ЗАДАЧА 2: Детский утренник")
print("=" * 55)

children = [
    {'id': 1, 'age': 5},
    {'id': 2, 'age': 7},
    {'id': 3, 'age': 6},
    {'id': 4, 'age': 10},
    {'id': 5, 'age': 8},
    {'id': 6, 'age': 3},
    {'id': 7, 'age': 11},
    {'id': 8, 'age': 4},
    {'id': 9, 'age': 9},
]

print("Дети (id, возраст):", [(c['id'], c['age']) for c in children])

t0 = time.perf_counter()
groups = min_groups(children)
elapsed = time.perf_counter() - t0

print(f"\nМинимальное количество групп: {len(groups)}")
for i, g in enumerate(groups, 1):
    ages = [c['age'] for c in g]
    ids  = [c['id']  for c in g]
    print(f"  Группа {i}: дети {ids}, возраст {ages} (диапазон {min(ages)}–{max(ages)})")
print(f"\nВремя выполнения: {elapsed:.6f} с")
