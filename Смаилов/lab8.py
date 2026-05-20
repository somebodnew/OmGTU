# Лабораторная работа 8 — Вариант 21
# Задача Коши: y' = 3 + 2x + y,  y(0) = 2,  x in [0; 1],  h = 0.2
# Методы: Эйлера, модифицированный Эйлера, Рунге-Кутта 4-го порядка

def f(x, y):
    return 3 + 2*x + y

# Начальные условия
x0, y0 = 0.0, 2.0
h = 0.2
b = 1.0

def euler(f, x0, y0, h, b):
    xs, ys = [x0], [y0]
    x, y = x0, y0
    while round(x, 10) < b:
        y = y + h * f(x, y)
        x = round(x + h, 10)
        xs.append(x)
        ys.append(y)
    return xs, ys

def modified_euler(f, x0, y0, h, b):
    xs, ys = [x0], [y0]
    x, y = x0, y0
    while round(x, 10) < b:
        y_tilde = y + h * f(x, y)
        y = y + h / 2 * (f(x, y) + f(x + h, y_tilde))
        x = round(x + h, 10)
        xs.append(x)
        ys.append(y)
    return xs, ys

def runge_kutta(f, x0, y0, h, b):
    xs, ys = [x0], [y0]
    x, y = x0, y0
    while round(x, 10) < b:
        k0 = h * f(x, y)
        k1 = h * f(x + h/2, y + k0/2)
        k2 = h * f(x + h/2, y + k1/2)
        k3 = h * f(x + h,   y + k2)
        y = y + (k0 + 2*k1 + 2*k2 + k3) / 6
        x = round(x + h, 10)
        xs.append(x)
        ys.append(y)
    return xs, ys

# Точное решение: y = -5 - 2x + 7*e^x
import math
def exact(x):
    return -5 - 2*x + 7 * math.exp(x)

# Запуск
xs_e,  ys_e  = euler(f, x0, y0, h, b)
xs_me, ys_me = modified_euler(f, x0, y0, h, b)
xs_rk, ys_rk = runge_kutta(f, x0, y0, h, b)

# Вывод таблицы
header = f"{'x':>6} | {'Эйлер':>12} | {'Мод.Эйлер':>12} | {'Рунге-Кутта':>13} | {'Точное':>12} | {'|err E|':>10} | {'|err ME|':>10} | {'|err RK|':>10}"
print("=" * len(header))
print(f"  y' = 3 + 2x + y,  y(0) = 2,  x in [0; 1],  h = {h}")
print("=" * len(header))
print(header)
print("-" * len(header))

for i in range(len(xs_e)):
    x  = xs_e[i]
    ye = ys_e[i]
    yme = ys_me[i]
    yrk = ys_rk[i]
    yex = exact(x)
    print(f"{x:>6.1f} | {ye:>12.6f} | {yme:>12.6f} | {yrk:>13.6f} | {yex:>12.6f} | {abs(ye-yex):>10.6f} | {abs(yme-yex):>10.6f} | {abs(yrk-yex):>10.6f}")

print("=" * len(header))
print("\nПогрешности в конечной точке x = 1.0:")
yex1 = exact(1.0)
print(f"  Эйлер:           {abs(ys_e[-1]  - yex1):.6f}")
print(f"  Мод. Эйлер:      {abs(ys_me[-1] - yex1):.6f}")
print(f"  Рунге-Кутта 4:   {abs(ys_rk[-1] - yex1):.6f}")
