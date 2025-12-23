import math

# ==============================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ==============================

def gcd(a, b):
    """Нахождение НОД алгоритмом Евклида."""
    while b:
        a, b = b, a % b
    return a

def is_perfect_square(n):
    """Проверка, является ли число полным квадратом."""
    return math.isqrt(n) ** 2 == n

def sieve_of_modulus(mod, start):
    """
    Создание решета для квадратичного метода.
    Возвращает список булевых значений длиной mod,
    где True означает, что число является квадратичным вычетом.
    """
    sieve = [False] * mod
    for x in range(mod):
        if ((x + start) ** 2) % mod in {0, 1, 4, 9, 16}:
            sieve[x] = True
    return sieve

# ==============================
# МЕТОД КВАДРАТИЧНОГО РЕШЕТА
# ==============================

def quadratic_sieve(m, mods):
    """
    Метод квадратичного решета для факторизации числа m.
    mods — список модулей (например, [3, 5, 7]).
    """
    start = math.isqrt(m) + 1
    end = (m + 1) // 2
    print(f"Ищем x в интервале от {start} до {end}")
    
    # Строим решета для каждого модуля
    sieves = []
    for mod in mods:
        sieve = sieve_of_modulus(mod, start)
        sieves.append(sieve)
        print(f"Решето по модулю {mod}: {sieve}")
    
    # Проходим по всем x
    for x in range(start, end + 1):
        # Проверяем, проходит ли x через все решета
        passed_all = True
        for idx, mod in enumerate(mods):
            if not sieves[idx][(x - start) % mod]:
                passed_all = False
                break
        if passed_all:
            z = x * x - m
            if is_perfect_square(z):
                y = math.isqrt(z)
                p = x + y
                q = x - y
                if p * q == m:
                    return p, q, x, y
    return None

# ==============================
# ρ-МЕТОД ПОЛЛАРДА
# ==============================

def rho_method(m, x0=2, f=None):
    """
    ρ-метод Полларда для факторизации числа m.
    x0 — начальное значение.
    f — циклическая функция (по умолчанию x² + 1 mod m).
    """
    if f is None:
        f = lambda x: (x * x + 1) % m
    
    x1 = x0
    x2 = x0
    d = 1
    step = 0
    
    while d == 1:
        x1 = f(x1)
        x2 = f(f(x2))
        d = gcd(abs(x1 - x2), m)
        step += 1
        print(f"Шаг {step}: x1={x1}, x2={x2}, d={d}")
        if d != 1 and d != m:
            p = d
            q = m // d
            return p, q, step
    return None

# ==============================
# ГЛАВНАЯ ПРОГРАММА
# ==============================

def main():
    print("=" * 50)
    print("ЛАБОРАТОРНАЯ РАБОТА №6: МЕТОДЫ ФАКТОРИЗАЦИИ ЧИСЛА")
    print("=" * 50)
    
    # Ввод числа для факторизации
    m = int(input("Введите число m для факторизации: "))
    print(f"\nЧисло m = {m}")
    
    # ==============================
    # 1. МЕТОД КВАДРАТИЧНОГО РЕШЕТА
    # ==============================
    print("\n" + "="*30)
    print("1. МЕТОД КВАДРАТИЧНОГО РЕШЕТА")
    print("="*30)
    
    mods = list(map(int, input("Введите три модуля для решет (через пробел): ").split()))
    if len(mods) != 3:
        print("Нужно ровно три модуля!")
        return
    
    result = quadratic_sieve(m, mods)
    if result:
        p, q, x, y = result
        print(f"\nНайдены делители методом квадратичного решета:")
        print(f"x = {x}, y = {y}")
        print(f"p = x + y = {p}")
        print(f"q = x - y = {q}")
        print(f"Проверка: {p} * {q} = {p * q} (ожидалось {m})")
    else:
        print("Делители не найдены методом квадратичного решета.")
    
    # ==============================
    # 2. ρ-МЕТОД ПОЛЛАРДА
    # ==============================
    print("\n" + "="*30)
    print("2. ρ-МЕТОД ПОЛЛАРДА")
    print("="*30)
    
    x0 = int(input("Введите начальное значение x0 (по умолчанию 2): ") or "2")
    result = rho_method(m, x0)
    if result:
        p, q, steps = result
        print(f"\nНайдены делители ρ-методом на шаге {steps}:")
        print(f"p = {p}")
        print(f"q = {q}")
        print(f"Проверка: {p} * {q} = {p * q} (ожидалось {m})")
    else:
        print("Делители не найдены ρ-методом.")
    
    print("\n" + "="*50)
    print("РАБОТА ЗАВЕРШЕНА")
    print("="*50)

if __name__ == "__main__":
    main()
