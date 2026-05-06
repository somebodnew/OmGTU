import math


# Подынтегральная функция и её первообразная (для Ньютона-Лейбница)

def f(x: float) -> float:
    return (x**2 + 4*x + math.sqrt(x))


def antiderivative(x: float) -> float:
    
    return ((x**3 / 3) + (2 * x**2) + (2 * x * math.sqrt(x) / 3))


def left_rectangles(func, a: float, b: float, n: int) -> float:
    h = (b - a) / n
    return h * sum(func(a + i * h) for i in range(n))


def right_rectangles(func, a: float, b: float, n: int) -> float:
    h = (b - a) / n
    return h * sum(func(a + i * h) for i in range(1, n + 1))


def trapezoid(func, a: float, b: float, n: int) -> float:
    h = (b - a) / n
    total = 0.5 * (func(a) + func(b))
    total += sum(func(a + i * h) for i in range(1, n))
    return h * total


def simpson(func, a: float, b: float, n: int) -> float:
    if n % 2 != 0:
        n += 1
    h = (b - a) / n
    total = func(a) + func(b)
    for i in range(1, n):
        coeff = 4 if i % 2 == 1 else 2
        total += coeff * func(a + i * h)
    return (h / 3) * total


def newton_leibniz(F, a: float, b: float) -> float:
    return F(b) - F(a)


def runge_error(I_n: float, I_2n: float, p: int) -> float:
    return abs(I_2n - I_n) / (2**p - 1)



def print_node_table(func, a, b, n):
    h = (b - a) / n
    print(f"\n{'Таблица значений функции в узлах (n=' + str(n) + ')'}")
    print(f"{'i':>4}  {'Xi':>10}  {'f(Xi)':>12}")
    for i in range(n + 1):
        xi = a + i * h
        print(f"{i:>4}  {xi:>10.4f}  {func(xi):>12.6f}")


def print_results(a, b, n, exact, methods):
    col = 22
    print(f"\n{'═'*70}")
    print(f"  СВОДНАЯ ТАБЛИЦА РЕЗУЛЬТАТОВ   a={a}, b={b}, n={n}")
    print(f"{'═'*70}")
    hdr = f"{'Метод':<{col}} {'Результат':>12}  {'Погр. (Рунге)':>14}  {'Откл. от NL':>12}"
    print(hdr)
    print("─" * 70)

    for name, value, runge, p_label in methods:
        dev = abs(value - exact)
        runge_str = f"{runge:.8f}" if runge is not None else "    —"
        print(f"{name:<{col}} {value:>12.6f}  {runge_str:>14}  {dev:>12.8f}")

    print("─" * 70)
    print(f"{'Ньютон-Лейбниц':<{col}} {exact:>12.6f}")
    print(f"{'═'*70}\n")



def main():
    # Параметры задачи 
    a = 3.0
    b = 6.0
    n = 6 
    
    print_node_table(f, a, b, n)

    # Вычисление методами
    I_left   = left_rectangles(f, a, b, n)
    I_right  = right_rectangles(f, a, b, n)
    I_trap   = trapezoid(f, a, b, n)
    I_simp   = simpson(f, a, b, n)
    I_exact  = newton_leibniz(antiderivative, a, b)

    # Погрешности Рунге
    I_left_2n  = left_rectangles(f, a, b, 2 * n)
    I_right_2n = right_rectangles(f, a, b, 2 * n)
    I_trap_2n  = trapezoid(f, a, b, 2 * n)
    I_simp_2n  = simpson(f, a, b, 2 * n)

    runge_left  = runge_error(I_left,  I_left_2n,  p=1)
    runge_right = runge_error(I_right, I_right_2n, p=1)
    runge_trap  = runge_error(I_trap,  I_trap_2n,  p=2)
    runge_simp  = runge_error(I_simp,  I_simp_2n,  p=4)

    # Сводная таблица
    methods = [
        ("Лев. прямоугольники", I_left,  runge_left,  "p=1"),
        ("Прав. прямоугольники", I_right, runge_right, "p=1"),
        ("Трапеции",             I_trap,  runge_trap,  "p=2"),
        ("Симпсон (параболы)",   I_simp,  runge_simp,  "p=4"),
    ]
    print_results(a, b, n, I_exact, methods)


    print("ВЫВОД ПО МЕТОДАМ")
    

    items = [
        ("Левых прямоугольников", I_left,  I_left_2n,  runge_left,  1),
        ("Правых прямоугольников",I_right, I_right_2n, runge_right, 1),
        ("Трапеций",              I_trap,  I_trap_2n,  runge_trap,  2),
        ("Симпсона (парабол)",    I_simp,  I_simp_2n,  runge_simp,  4),
    ]
    for name, Iv, I2v, runge, p in items:
        print(f"\n  Метод {name}:")
        print(f"    I (n={n:>2})   = {Iv:.8f}")
        print(f"    I (n={2*n:>2})  = {I2v:.8f}")
        print(f"    d Рунге       = {runge:.8f}  (порядок точности p={p})")
        print(f"    |I - точное|  = {abs(Iv - I_exact):.8f}")

    print(f"\n  Формула Ньютона-Лейбница:")
    print(f"    F(b) - F(a) = F({b}) - F({a}) = {I_exact:.8f}")

    # Общий вывод
    best_name, best_err = min(
        [(name, abs(Iv - I_exact)) for name, Iv, _, _, _ in items],
        key=lambda t: t[1]
    )

    print(f"""
    {'═'*70}
    ОБЩИЙ ВЫВОД
    {'═'*70}
    Вычислен определённый интеграл I
    четырьмя численными методами при n = {n} и точное значение
    по формуле Ньютона-Лейбница.

    Точное значение (Ньютон-Лейбниц): I = {I_exact:.8f}

    Сравнение методов (отклонение от точного значения):
        • Лев. прямоугольники  : {abs(I_left  - I_exact):.8f}  (наибольшая погрешность)
        • Прав. прямоугольники : {abs(I_right - I_exact):.8f}  (симметрично левым)
        • Трапеций             : {abs(I_trap  - I_exact):.8f}  (средняя точность, p=2)
        • Симпсона             : {abs(I_simp  - I_exact):.8f}  (наивысшая точность, p=4)
    {'═'*70}
    """)


main()