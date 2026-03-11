import time

# ---------------------------------------------------------
# 1. Наивный метод (Brute Force)
# ---------------------------------------------------------
def naive_search(text, pattern):
    n = len(text)
    m = len(pattern)
    
    if m == 0 or n < m: return -1
        
    for i in range(n - m + 1):
        j = 0
        while j < m and text[i + j] == pattern[j]:
            j += 1
        if j == m:
            return i # Найдено
    return -1

# ---------------------------------------------------------
# 2. Алгоритм Рабина-Карпа
# ---------------------------------------------------------
def rabin_karp_search(text, pattern, d=256, q=101):
    n = len(text)
    m = len(pattern)
    
    if m == 0 or n < m: return -1
    
    h = pow(d, m-1) % q
    p = 0
    t = 0 
    
    for i in range(m):
        p = (d * p + ord(pattern[i])) % q
        t = (d * t + ord(text[i])) % q
        
    # Поиск
    for i in range(n - m + 1):
        if p == t:
            match = True
            for j in range(m):
                if text[i + j] != pattern[j]:
                    match = False
                    break
            if match:
                return i
                
        if i < n - m:
            t = (d * (t - ord(text[i]) * h) + ord(text[i + m])) % q
            if t < 0:
                t = t + q
    return -1

# ---------------------------------------------------------
# 3. Алгоритм Кнута-Морриса-Пратта (KMP)
# ---------------------------------------------------------
def compute_lps(pattern, m):
    lps = [0] * m
    length = 0
    i = 1
    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps

def kmp_search(text, pattern):
    n = len(text)
    m = len(pattern)
    
    if m == 0 or n < m: return -1
    
    lps = compute_lps(pattern, m)
    i = 0 # индекс для text
    j = 0 # индекс для pattern
    
    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1
            
        if j == m:
            return i - j # Найдено
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return -1

# ---------------------------------------------------------
# 4. Алгоритм Бойера-Мура (эвристика плохого символа)
# ---------------------------------------------------------
def bad_char_heuristic(pattern, m):
    bad_char = [-1] * 256 
    for i in range(m):
        bad_char[ord(pattern[i])] = i
    return bad_char

def boyer_moore_search(text, pattern):
    n = len(text)
    m = len(pattern)
    
    if m == 0 or n < m: return -1
    
    bad_char = bad_char_heuristic(pattern, m)
    s = 0 
    
    while s <= n - m:
        j = m - 1
        
        # Сравниваем с конца шаблона
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1
            
        if j < 0:
            return s
        else:
            s += max(1, j - bad_char[ord(text[s + j])])
            
    return -1

# =========================================================
# СРАВНИТЕЛЬНЫЙ АНАЛИЗ (ЗАМЕР ВРЕМЕНИ)
# =========================================================
def run_benchmark():
    # Создаем тестовые данные
    # 1. Обычный текст (Случайный)
    text_normal = "В этой лабораторной работе мы изучаем алгоритмы поиска подстроки. Это очень важная тема в информатике." * 500
    pattern_normal = "важная тема"
    
    # 2. Худший случай (много повторяющихся символов)
    text_worst = "A" * 100000 + "B"
    pattern_worst = "A" * 1000 + "B"
    
    tests = [
        ("Обычный текст", text_normal, pattern_normal),
        ("Худший случай", text_worst, pattern_worst)
    ]
    
    algorithms = [
        ("Наивный метод", naive_search),
        ("Рабин-Карп", rabin_karp_search),
        ("Кнут-Моррис-Пратт", kmp_search),
        ("Бойер-Мур", boyer_moore_search)
    ]
    
    for test_name, text, pattern in tests:
        print(f"\n--- Тест: {test_name} ---")
        print(f"Длина текста: {len(text)} | Длина шаблона: {len(pattern)}")
        
        for algo_name, algo_func in algorithms:
            # Прогрев и замер
            start_time = time.perf_counter()
            result = algo_func(text, pattern)
            end_time = time.perf_counter()
            
            exec_time = (end_time - start_time) * 1000 # в миллисекундах
            print(f"{algo_name:<20}: {exec_time:8.4f} мс | Индекс: {result}")

if __name__ == "__main__":
    run_benchmark()
