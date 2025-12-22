"""
Лабораторная работа №5: Криптоанализ шифра RSA (Вариант 19)
"""

import math

# Данные для варианта 19
e = 251
n = 66043
C = 23262

# Таблица кодировки русского алфавита
encoding_table = {
    'А': 10, 'Б': 11, 'В': 12, 'Г': 13, 'Д': 14,
    'Е': 15, 'Ж': 16, 'З': 17, 'И': 18, 'Й': 19,
    'К': 20, 'Л': 21, 'М': 22, 'Н': 23, 'О': 24,
    'П': 25, 'Р': 26, 'С': 27, 'Т': 28, 'У': 29,
    'Ф': 30, 'Х': 31, 'Ц': 32, 'Ч': 33, 'Ш': 34,
    'Щ': 35, 'Ъ': 36, 'Ы': 37, 'Ь': 38, 'Э': 39,
    'Ю': 40, 'Я': 41
}

# Обратная таблица для декодирования
reverse_encoding = {v: k for k, v in encoding_table.items()}
reverse_encoding[99] = ' '  # Пробел

def extended_gcd(a, b):
    """Расширенный алгоритм Евклида"""
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def mod_inverse(e, phi):
    """Вычисление обратного элемента по модулю"""
    gcd, x, _ = extended_gcd(e, phi)
    if gcd != 1:
        return None
    return x % phi

def trial_division_factorization(n):
    """Факторизация методом пробного деления"""
    if n % 2 == 0:
        return 2, n // 2
    
    limit = int(math.isqrt(n))
    
    for i in range(3, limit + 1, 2):
        if n % i == 0:
            return i, n // i
    
    raise ValueError(f"Не удалось факторизовать число {n}")

def fast_pow_mod(base, exp, mod):
    """Быстрое возведение в степень по модулю"""
    result = 1
    base = base % mod
    
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        exp = exp // 2
        base = (base * base) % mod
    
    return result

def number_to_text(number):
    """Преобразование числового блока в текст"""
    result = ""
    num_str = str(number)
    i = 0
    
    while i < len(num_str):
        # Проверяем на пробел (99)
        if i + 2 <= len(num_str) and num_str[i:i+2] == "99":
            result += " "
            i += 2
        else:
            # Берем двузначное число
            if i + 2 <= len(num_str):
                code = int(num_str[i:i+2])
                if code in reverse_encoding:
                    result += reverse_encoding[code]
                i += 2
            else:
                i += 1
    
    return result

def main():
    print("=" * 60)
    print("Лабораторная работа №5: Криптоанализ шифра RSA")
    print("Вариант 19")
    print("=" * 60)
    
    print(f"Исходные данные:")
    print(f"  Открытый ключ: e = {e}, n = {n}")
    print(f"  Шифротекст: C = {C}")
    print()
    
    # 1. Факторизация числа n
    print("1. Факторизация числа n:")
    p, q = trial_division_factorization(n)
    print(f"   p = {p}")
    print(f"   q = {q}")
    print(f"   Проверка: {p} * {q} = {p*q} = {n}")
    print()
    
    # 2. Вычисление функции Эйлера
    phi_n = (p - 1) * (q - 1)
    print("2. Вычисление функции Эйлера:")
    print(f"   φ(n) = (p-1)*(q-1) = ({p}-1)*({q}-1) = {phi_n}")
    print()
    
    # 3. Нахождение закрытого ключа d
    print("3. Нахождение закрытого ключа d:")
    d = mod_inverse(e, phi_n)
    print(f"   Решаем: e * d ≡ 1 mod φ(n)")
    print(f"           {e} * d ≡ 1 mod {phi_n}")
    print(f"   Найден d = {d}")
    print(f"   Проверка: {e} * {d} mod {phi_n} = {(e * d) % phi_n}")
    print()
    
    # 4. Расшифрование сообщения
    print("4. Расшифрование сообщения:")
    print(f"   Формула: M = C^d mod n")
    print(f"           M = {C}^{d} mod {n}")
    
    M = fast_pow_mod(C, d, n)
    print(f"   Числовой блок: M = {M}")
    print()
    
    # 5. Преобразование в текст
    print("5. Преобразование в текст:")
    text = number_to_text(M)
    print(f"   Текст: '{text}'")
    print()
    
    # Вывод всех результатов для отчета
    print("=" * 60)
    print("Результаты для отчета:")
    print("=" * 60)
    print(f"Параметр n = {n}")
    print(f"Открытый ключ шифрования e = {e}")
    print(f"Факторизация числа n: p = {p}, q = {q}")
    print(f"Функция Эйлера φ(n) = {phi_n}")
    print(f"Закрытый ключ шифрования d = {d}")
    print(f"Шифротекст: C = {C}")
    print(f"Открытый текст (числовой блок): M = {M}")
    print(f"Текстовое представление: '{text}'")
    print("=" * 60)

if __name__ == "__main__":
    main()
