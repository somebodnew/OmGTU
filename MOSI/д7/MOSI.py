import math

def mod_pow(base: int, exponent: int, modulus: int) -> int:
    """Быстрое возведение в степень по модулю"""
    result = 1
    base = base % modulus
    
    while exponent > 0:
        if exponent & 1:
            result = (result * base) % modulus
        exponent = exponent >> 1
        base = (base * base) % modulus
    
    return result

def baby_step_giant_step(a: int, b: int, p: int):
    """Алгоритм 'шаг младенца - шаг великана'"""
    # Вычисляем k = floor(sqrt(p)) + 1
    k = math.isqrt(p) + 1
    
    # Шаг "младенца" (Baby-step)
    baby_steps = {}
    current = b % p
    
    for j in range(k):
        baby_steps[current] = j
        current = (current * a) % p
    
    # Шаг "великана" (Giant-step)
    a_k = mod_pow(a, k, p)
    current = 1
    
    for i in range(1, k + 1):
        current = (current * a_k) % p
        
        if current in baby_steps:
            j = baby_steps[current]
            x = i * k - j
            
            if x >= 0:
                return x, i, j, k
    
    return None

def main():
    """Решение для варианта 19"""
    # Вариант 19: a = 8, b = 16190, p = 30803
    a = 8
    b = 16190
    p = 30803
    
    print("=" * 60)
    print("ЛАБОРАТОРНАЯ РАБОТА №7: ВЫЧИСЛЕНИЕ ДИСКРЕТНОГО ЛОГАРИФМА")
    print(f"Вариант 19: a = {a}, b = {b}, p = {p}")
    print(f"Найти x такой, что: {a}^x ≡ {b} (mod {p})")
    print("=" * 60)
    
    result = baby_step_giant_step(a, b, p)
    
    if result is None:
        print("Решение не найдено в пределах алгоритма")
        return
    
    x, i, j, k = result
    
    print("\nРЕЗУЛЬТАТЫ ВЫЧИСЛЕНИЙ:")
    print("-" * 40)
    print(f"1. Вычисляем k = ⌊√{p}⌋ + 1")
    print(f"   √{p} ≈ {math.sqrt(p):.2f}")
    print(f"   ⌊√{p}⌋ = {math.isqrt(p)}")
    print(f"   k = {math.isqrt(p)} + 1 = {k}")
    
    print(f"\n2. Шаг 'младенца' (Baby-step)")
    print(f"   Вычисляем z_j = b·a^j mod p для j = 0..{k-1}")
    print(f"   Сохраняем {k} значений в хеш-таблице")
    
    print(f"\n3. Шаг 'великана' (Giant-step)")
    print(f"   Вычисляем y_i = a^(i·k) mod p для i = 1..{k}")
    print(f"   a^k mod p = {a}^{k} mod {p} = {mod_pow(a, k, p)}")
    
    print(f"\n4. Найдено совпадение:")
    print(f"   При i = {i} (шаг 'великана')")
    print(f"   При j = {j} (шаг 'младенца')")
    print(f"   y_{i} = z_{j}")
    
    print(f"\n5. Вычисляем x:")
    print(f"   x = i·k - j = {i}·{k} - {j} = {x}")
    
    print("\n" + "=" * 60)
    print("ОТВЕТ:")
    print(f"x = {x}")
    print("=" * 60)
    
    # Проверка
    print("\nПРОВЕРКА:")
    print("-" * 40)
    left_side = mod_pow(a, x, p)
    print(f"{a}^{x} mod {p} = {left_side}")
    print(f"b mod {p} = {b % p}")
    
    if left_side == b % p:
        print(f"✓ ВЕРНО: {left_side} ≡ {b % p} (mod {p})")
    else:
        print(f"✗ ОШИБКА: {left_side} ≠ {b % p}")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
