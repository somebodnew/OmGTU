import time
import random

# =========================================================
# РЕШЕНИЕ ЗАДАЧ 1 и 2
# Выбор максимального подмножества непересекающихся отрезков
# =========================================================
def solve_max_activities(intervals):
    if not intervals:
        return []

    # 1. Жадный выбор: сортируем по времени ОКОНЧАНИЯ (возрастание)
    # Если окончания совпадают, порядок не важен (сорт стабильный)
    sorted_intervals = sorted(intervals, key=lambda x: x[1])

    selected = []
    
    if sorted_intervals:
        last_end_time = sorted_intervals[0][1]
        selected.append(sorted_intervals[0])

    # 2. Проходим по остальным и берем те, что не пересекаются
    for i in range(1, len(sorted_intervals)):
        start, end = sorted_intervals[i]
        # Если начало текущего >= концу последнего выбранного
        if start >= last_end_time:
            selected.append((start, end))
            last_end_time = end
            
    return selected

# =========================================================
# РЕШЕНИЕ ЗАДАЧИ 3
# Покрытие интервала [L, R] минимальным числом отрезков
# =========================================================
def solve_min_segments_cover(segments, L, R):
    # 1. Сортируем по времени НАЧАЛА
    segments.sort(key=lambda x: x[0])
    
    result = []
    current_reach = L
    i = 0
    n = len(segments)
    
    while current_reach < R:
        best_segment = None
        max_end = -1
        
        # 2. Ищем все отрезки, которые начинаются ДО или В текущей границе
        # Из них выбираем тот, который тянется максимально ВПРАВО
        while i < n and segments[i][0] <= current_reach:
            if segments[i][1] > max_end:
                max_end = segments[i][1]
                best_segment = segments[i]
            i += 1
            
        if best_segment is None:
            return None 
            
        result.append(best_segment)
        current_reach = max_end
        
        if current_reach <= L and not result: 
             return None 

    return result

# =========================================================
# БЛОК ТЕСТИРОВАНИЯ И ЗАМЕРА ВРЕМЕНИ
# =========================================================
def run_lab_6():
    print("Лабораторная работа 6: Жадные алгоритмы\n")

    # --- ТЕСТ ДЛЯ ЗАДАЧ 1 и 2 ---
    print(" Задачи 1 и 2: Максимальное число непересекающихся заявок")
    
    # Генерация данных (например, 100 000 заявок)
    N = 100000
    tasks = []
    for _ in range(N):
        start = random.randint(0, 10000)
        duration = random.randint(1, 100)
        tasks.append((start, start + duration))
    
    print(f"Входные данные: {N} случайных отрезков.")
    
    start_time = time.perf_counter()
    res_tasks = solve_max_activities(tasks)
    end_time = time.perf_counter()
    
    print(f"Выбрано заявок: {len(res_tasks)}")
    print(f"Время выполнения: {(end_time - start_time)*1000:.4f} мс")
    print("-" * 30)

    # --- ТЕСТ ДЛЯ ЗАДАЧИ 3 ---
    print("\n Задача 3: Минимальное покрытие интервала")
    
    # Целевой интервал
    Target_L, Target_R = 0, 5000
    
    # Генерация данных (гарантируем перекрытие для теста)
    M = 10000
    segments = []
    for k in range(M):
        l = random.randint(0, 4900)
        r = l + random.randint(50, 200)
        segments.append((l, r))
    
    # Добавим пару гарантирующих отрезков для краев
    segments.append((0, 100))
    segments.append((4900, 5100))

    print(f"Входные данные: {len(segments)} отрезков. Цель: покрыть [{Target_L}, {Target_R}]")
    
    start_time = time.perf_counter()
    res_cover = solve_min_segments_cover(segments, Target_L, Target_R)
    end_time = time.perf_counter()
    
    if res_cover:
        print(f"Покрытие найдено. Количество отрезков: {len(res_cover)}")
        # Проверка (для наглядности выведем первые 3 и последние 3)
        if len(res_cover) > 6:
            print(f"Пример решения: {res_cover[:3]} ... {res_cover[-3:]}")
        else:
            print(f"Решение: {res_cover}")
    else:
        print("Невозможно покрыть интервал заданными отрезками.")
        
    print(f"Время выполнения: {(end_time - start_time)*1000:.4f} мс")


run_lab_6()

