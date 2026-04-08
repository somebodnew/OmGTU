"""
Лабораторная работа 9 — Жадные алгоритмы (раскраска графа)
Задача 1: Распределение работ между механизмами (минимальное время)
Задача 2: Размещение грузов по контейнерам (раскраска графа)
"""

import time


# ─────────────────────────────────────────────
# Задача 1: Распределение работ между механизмами
# ─────────────────────────────────────────────
#
# Представление: граф конфликтов механизмов.
# Два механизма «конфликтуют» (не могут работать одновременно),
# если они нужны хотя бы в одной общей работе.
# Жадный алгоритм: на каждом шаге берём работу, которая требует
# наибольшее число ещё незанятых механизмов, назначаем её в
# параллельный «слот», пока все механизмы в слоте совместимы.
# Сложность: O(n * m)  (n работ, m механизмов).

def distribute_works(works: dict[str, list]) -> list[list]:
    """
    works: {'a1': ['b1','b5','b8'], ...}  — механизмы для каждой работы.
    Возвращает список «шагов» (параллельных слотов), каждый — список работ,
    выполняемых одновременно (их механизмы не пересекаются).
    """
    remaining = dict(works)
    steps = []

    while remaining:
        slot = []
        used_mechanisms = set()

        # сортируем по убыванию кол-ва механизмов (жадный выбор)
        candidates = sorted(remaining.keys(),
                            key=lambda w: len(remaining[w]), reverse=True)
        for work in candidates:
            mechs = set(remaining[work])
            if mechs.isdisjoint(used_mechanisms):
                slot.append(work)
                used_mechanisms |= mechs

        for w in slot:
            del remaining[w]

        steps.append(slot)

    return steps


# ─────────────────────────────────────────────
# Задача 2: Размещение грузов по контейнерам
# Раскраска графа жадным алгоритмом
# ─────────────────────────────────────────────
#
# Граф: вершины = грузы, рёбра = несовместимые пары.
# Раскраска = распределение по контейнерам.
# Жадный алгоритм Уэлша–Пауэлла:
#   1. Сортируем вершины по убыванию степени.
#   2. Назначаем каждой вершине минимальный цвет (контейнер),
#      не используемый соседями.
# Сложность: O(n^2) в худшем случае.

def greedy_coloring(n: int, incompatible: list[tuple]) -> dict[int, int]:
    """
    n            — количество грузов (вершины 0..n-1)
    incompatible — список пар (i, j) несовместимых грузов
    Возвращает словарь {груз: контейнер}.
    """
    # Список смежности
    adj = {i: set() for i in range(n)}
    for u, v in incompatible:
        adj[u].add(v)
        adj[v].add(u)

    # Сортировка по убыванию степени (Уэлш–Пауэлл)
    order = sorted(range(n), key=lambda v: len(adj[v]), reverse=True)

    color = {}  # вершина -> цвет (контейнер)

    for v in order:
        neighbor_colors = {color[u] for u in adj[v] if u in color}
        c = 0
        while c in neighbor_colors:
            c += 1
        color[v] = c

    return color


# ─────────────────────────────────────────────
# Данные из условия (Задача 1)
# ─────────────────────────────────────────────

WORKS = {
    'a1':  ['b1', 'b5', 'b8'],
    'a2':  ['b2', 'b3'],
    'a3':  ['b2', 'b7', 'b9'],
    'a4':  ['b1', 'b6', 'b7', 'b9'],
    'a5':  ['b3', 'b5'],
    'a6':  ['b1', 'b4', 'b7', 'b9'],
    'a7':  ['b2', 'b6', 'b9'],
    'a8':  ['b3', 'b6', 'b8'],
    'a9':  ['b2', 'b4', 'b5'],
    'a10': ['b1', 'b6'],
}


def main():
    # ── Задача 1 ──────────────────────────────
    print("=" * 55)
    print("ЗАДАЧА 1: Распределение работ между механизмами")
    print("=" * 55)

    t0 = time.perf_counter()
    steps = distribute_works(WORKS)
    elapsed = time.perf_counter() - t0

    print(f"Минимальное время (количество шагов): {len(steps)}")
    for i, slot in enumerate(steps, 1):
        mechs = sorted(set(m for w in slot for m in WORKS[w]))
        print(f"  Шаг {i}: работы {slot}  |  механизмы {mechs}")
    print(f"\nВремя выполнения алгоритма: {elapsed:.6f} с")
    print("Сложность: O(n * m), n=кол-во работ, m=кол-во механизмов")

    # ── Задача 2 ──────────────────────────────
    print("\n" + "=" * 55)
    print("ЗАДАЧА 2: Размещение грузов по контейнерам")
    print("=" * 55)

    # 8 грузов, несовместимые пары
    n_cargo = 8
    incompatible = [(0,1),(0,3),(1,2),(1,4),(2,5),(3,4),(3,6),(4,5),(4,7),(5,6),(6,7)]

    print(f"Грузов: {n_cargo}")
    print(f"Несовместимые пары: {[(u+1, v+1) for u,v in incompatible]}")

    t0 = time.perf_counter()
    coloring = greedy_coloring(n_cargo, incompatible)
    elapsed = time.perf_counter() - t0

    # Группировка по контейнерам
    containers: dict[int, list] = {}
    for cargo, cont in coloring.items():
        containers.setdefault(cont, []).append(cargo + 1)  # нумерация с 1

    num_containers = len(containers)
    print(f"\nМинимальное количество контейнеров: {num_containers}")
    for cont in sorted(containers):
        print(f"  Контейнер {cont + 1}: грузы {sorted(containers[cont])}")
    print(f"\nВремя выполнения алгоритма: {elapsed:.6f} с")
    print("Сложность: O(n^2) в худшем случае (алгоритм Уэлша–Пауэлла)")


if __name__ == '__main__':
    main()
