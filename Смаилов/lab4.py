
import math

EPS = 0.001
MAX_ITER = 10000


def F(x, y):
    return math.cos(y - 1) + x - 0.5

def G(x, y):
    return y - math.cos(x) - 3

def Fx(x, y): return 1.0
def Fy(x, y): return -math.sin(y - 1)
def Gx(x, y): return math.sin(x)
def Gy(x, y): return 1.0

def dPhi_dx(x, y):
    return 2 * F(x, y) * Fx(x, y) + 2 * G(x, y) * Gx(x, y)

def dPhi_dy(x, y):
    return 2 * F(x, y) * Fy(x, y) + 2 * G(x, y) * Gy(x, y)

def Phi(x, y):
    return F(x, y)**2 + G(x, y)**2


# Метод Ньютона

def newton(x0, y0, eps=EPS, max_iter=MAX_ITER):
    x, y = x0, y0
    print("\n=== Метод Ньютона ===")
    print(f"{'Iter':>5}  {'x':>12}  {'y':>12}  {'|dx|':>12}  {'|dy|':>12}")

    for k in range(max_iter):
        fx = Fx(x, y); fy = Fy(x, y)
        gx = Gx(x, y); gy = Gy(x, y)
        det = fx * gy - gx * fy
        if abs(det) < 1e-14:
            print("Якобиан вырожден, метод не применим.")
            return None, None

        f_val = F(x, y)
        g_val = G(x, y)

        dx = (-f_val * gy + g_val * fy) / det
        dy = (-g_val * fx + f_val * gx) / det

        xk = x + dx
        yk = y + dy

        print(f"{k+1:>5}  {xk:>12.7f}  {yk:>12.7f}  {abs(dx):>12.7f}  {abs(dy):>12.7f}")

        if abs(dx) < eps and abs(dy) < eps:
            print(f"\nРешение найдено за {k+1} итераций.")
            print(f"x* = {xk:.6f},  y* = {yk:.6f}")
            return xk, yk

        x, y = xk, yk

    print("Решение не найдено за максимальное число итераций.")
    return None, None


# Метод простых итераций (Якоби) 

def jacobi(x0, y0, eps=EPS, max_iter=MAX_ITER):
    x, y = x0, y0
    print("\n=== Метод простых итераций (Якоби) ===")
    print(f"{'Iter':>5}  {'x':>12}  {'y':>12}  {'погрешность':>14}")

    for k in range(max_iter):
        xk = 0.5 - math.cos(y - 1)
        yk = 3.0 + math.cos(x)

        err = max(abs(xk - x), abs(yk - y))
        print(f"{k+1:>5}  {xk:>12.7f}  {yk:>12.7f}  {err:>14.7f}")

        if err < eps:
            print(f"\nРешение найдено за {k+1} итераций.")
            print(f"x* = {xk:.6f},  y* = {yk:.6f}")
            return xk, yk

        x, y = xk, yk

    print("Решение не найдено за максимальное число итераций.")
    return None, None


# Метод Зейделя 

def seidel(x0, y0, eps=EPS, max_iter=MAX_ITER):
    x, y = x0, y0
    print("\n=== Метод Зейделя ===")
    print(f"{'Iter':>5}  {'x':>12}  {'y':>12}  {'погрешность':>14}")

    for k in range(max_iter):
        xk = 0.5 - math.cos(y - 1)
        yk = 3.0 + math.cos(xk)          

        err = max(abs(xk - x), abs(yk - y))
        print(f"{k+1:>5}  {xk:>12.7f}  {yk:>12.7f}  {err:>14.7f}")

        if err < eps:
            print(f"\nРешение найдено за {k+1} итераций.")
            print(f"x* = {xk:.6f},  y* = {yk:.6f}")
            return xk, yk

        x, y = xk, yk

    print("Решение не найдено за максимальное число итераций.")
    return None, None


# Метод наискорейшего спуска

def golden_section(func, a, b, tol=1e-8):
    phi = (math.sqrt(5) - 1) / 2
    c = b - phi * (b - a)
    d = a + phi * (b - a)
    while abs(b - a) > tol:
        if func(c) < func(d):
            b = d
        else:
            a = c
        c = b - phi * (b - a)
        d = a + phi * (b - a)
    return (a + b) / 2


def steepest_descent(x0, y0, eps=EPS, max_iter=MAX_ITER):
    x, y = x0, y0
    print("\n=== Метод наискорейшего спуска ===")
    print(f"{'Iter':>5}  {'x':>12}  {'y':>12}  {'Phi':>14}  {'погрешность':>14}")

    for k in range(max_iter):
        px = -dPhi_dx(x, y)
        py = -dPhi_dy(x, y)

        norm_p = math.sqrt(px**2 + py**2)
        if norm_p < 1e-14:
            print("Градиент нулевой — найдена стационарная точка.")
            break

        def phi_line(alpha):
            return Phi(x + alpha * px, y + alpha * py)

        alpha_star = golden_section(phi_line, 0.0, 10.0)

        xk = x + alpha_star * px
        yk = y + alpha_star * py

        err = max(abs(xk - x), abs(yk - y))
        phi_val = Phi(xk, yk)

        print(f"{k+1:>5}  {xk:>12.7f}  {yk:>12.7f}  {phi_val:>14.2e}  {err:>14.7f}")

        if err < eps:
            print(f"\nРешение найдено за {k+1} итераций.")
            print(f"x* = {xk:.6f},  y* = {yk:.6f}")
            return xk, yk

        x, y = xk, yk

    print("Решение не найдено за максимальное число итераций.")
    return x, y



print("=" * 60)
print("Вариант 21. Система нелинейных уравнений:")
print("  F(x, y) = cos(y - 1) + x - 0.5 = 0")
print("  G(x, y) = y - cos(x) - 3       = 0")
print(f"Точность: eps = {EPS}")
print("=" * 60)

    # Начальное приближение:
    # из G: y ≈ 3 + cos(x), при x≈0 => y≈4
    # из F: x ≈ 0.5 - cos(y-1), при y≈4 => x ≈ 0.5 - cos(3) ≈ 0.5+0.99 ≈ 1.49
x0, y0 = 0.5, 4.0
print(f"\nНачальное приближение: x0 = {x0},  y0 = {y0}\n")

newton(x0, y0)
jacobi(x0, y0)
seidel(x0, y0)
steepest_descent(x0, y0)
