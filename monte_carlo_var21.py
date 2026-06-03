"""
Семестровое задание — Метод Монте-Карло, Вариант 21

Задание 1: Вычисление тройного интеграла
Задание 2: Решение системы линейных уравнений
Задание 3: Площадь фигуры (вариант 9 из таблицы фигур)
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy import integrate

np.random.seed(42)
N = 100000



# Вычислить тройной интеграл 
# методом Монте-Карло:
print("=" * 60)
print("ЗАДАНИЕ 1: Тройной интеграл")
print("=" * 60)

a1, b1 = 0, 1   # по x
a2, b2 = 0, 1   # по y
a3, b3 = 0, 3   # по z

x = np.random.uniform(a1, b1, N)
y = np.random.uniform(a2, b2, N)
z = np.random.uniform(a3, b3, N)

f_vals = x + y**3 + z**4
I_mc = (b1 - a1) * (b2 - a2) * (b3 - a3) / N * np.sum(f_vals)

# Точное значение (аналитически):
# интеграл dx = 1/2   = 0.5
# интеграл dy = 1/4   = 0.25
# интеграл dz = 243/5 = 48.6
# I_exact = (1/2 + 1/4) * 3 + 1 * 1 * 243/5
I_exact = (1/2) * 1 * 3 + 1 * (1/4) * 3 + 1 * 1 * (3**5 / 5)

abs_err = abs(I_mc - I_exact)
rel_err = abs_err / abs(I_exact) * 100

print(f"Число испытаний N = {N}")
print(f"Метод Монте-Карло:  I ≈ {I_mc:.6f}")
print(f"Точное значение:    I  = {I_exact:.6f}")
print(f"Абсолютная погрешность: {abs_err:.6f}")
print(f"Относительная погрешность: {rel_err:.4f}%")



# Решить систему методом Монте-Карло (случайные блуждания)
#   x1 = 0.1*x1 + 0.5*x2 + 0.3
#   x2 = 0.8*x1 + 0.4*x2 + 0.3

print()
print("=" * 60)
print("ЗАДАНИЕ 2: Система линейных уравнений")
print("x1 = 0.1·x1 + 0.5·x2 + 0.3")
print("x2 = 0.8·x1 + 0.4·x2 + 0.3")
print("=" * 60)

alpha = np.array([[0.1, 0.5],
                  [0.8, 0.4]])
beta = np.array([0.3, 0.3])
n = 2


def solve_mc(eq_idx, N_traj=N):
    S = 0.0
    row_sums = np.sum(np.abs(alpha), axis=1)
    p = np.abs(alpha) / row_sums[:, np.newaxis]
    with np.errstate(divide='ignore', invalid='ignore'):
        v = np.where(p > 0, alpha / p, 0.0)

    for _ in range(N_traj):
        i = eq_idx
        w = 1.0
        x_traj = beta[i]
        for _step in range(50):
            j = np.random.choice(n, p=p[i])
            w *= v[i, j]
            x_traj += w * beta[j]
            i = j
            if abs(w) < 1e-6:
                break
        S += x_traj
    return S / N_traj

x1_mc = solve_mc(0)
x2_mc = solve_mc(1)

A_exact = np.eye(n) - alpha
x_exact = np.linalg.solve(A_exact, beta)

print(f"Число траекторий N = {N}")
print(f"Метод Монте-Карло:  x1 ≈ {x1_mc:.4f},  x2 ≈ {x2_mc:.4f}")
print(f"Точное решение:     x1 = {x_exact[0]:.4f},  x2 = {x_exact[1]:.4f}")
print(f"Погрешность x1: {abs(x1_mc - x_exact[0]):.4f}")
print(f"Погрешность x2: {abs(x2_mc - x_exact[1]):.4f}")



# Площадь фигуры:

print()
print("=" * 60)
print("ЗАДАНИЕ 3: Площадь фигуры (вар. 9 из таблицы фигур)")
print("=" * 60)

xmin, xmax = -2, 2
ymin, ymax = -2, 2
S_rect = (xmax - xmin) * (ymax - ymin)

x_r = np.random.uniform(xmin, xmax, N)
y_r = np.random.uniform(ymin, ymax, N)

inside = (-x_r**3 - 5*y_r**3 < 2) & (-x_r + y_r < 2)
K = np.sum(inside)
S_mc = S_rect * K / N

print(f"Ограничивающий прямоугольник: {S_rect}")
print(f"Число испытаний N = {N}")
print(f"Точек внутри K = {K}")
print(f"Площадь фигуры S ≈ {S_mc:.4f}")


def integrand_row(x_val):
    y_up = min(x_val + 2, ymax)

    threshold = (2 + x_val**3) / 5
    if threshold >= 0:
        y_lo = max(-(threshold**(1/3)), ymin)
    else:
        y_lo = max(((-threshold)**(1/3)), ymin)
    return max(y_up - y_lo, 0)

try:
    S_exact, _ = integrate.quad(integrand_row, xmin, xmax)
    abs_err3 = abs(S_mc - S_exact)
    rel_err3 = abs_err3 / S_exact * 100
    print(f"Точная площадь (scipy): {S_exact:.4f}")
    print(f"Абсолютная погрешность: {abs_err3:.4f}")
    print(f"Относительная погрешность: {rel_err3:.2f}%")
except Exception:
    print("(Точное значение не вычислено)")

