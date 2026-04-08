"""
Вариант 21:
  x: 0.248  0.663  1.238  2.092  2.939
  y: -3.642  0.802  0.841  0.513  0.328
"""


# Исходные данные
X = [0.248, 0.663, 1.238, 2.092, 2.939]
Y = [-3.642, 0.802, 0.841, 0.513, 0.328]
n = len(X)  # = 5 узлов, степень полинома = 4

# Точка вычисления: x1 + x2 = X[1] + X[2]
x_eval = X[1] + X[2]   # 0.663 + 1.238 = 1.901



# Вспомогательные функции

def fmt(v, width=10, prec=6):
    """Форматирование числа."""
    return f"{v:{width}.{prec}f}"


def separator(char="─", width=70):
    print(char * width)



# 1. Многочлен Лагранжа

def lagrange_basis(xi, x_nodes, y_nodes):
    basis = []
    for i in range(len(x_nodes)):
        num = 1.0
        den = 1.0
        for j in range(len(x_nodes)):
            if j != i:
                num *= (xi - x_nodes[j])
                den *= (x_nodes[i] - x_nodes[j])
        basis.append(num / den)
    return basis


def lagrange(xi, x_nodes, y_nodes):
    basis = lagrange_basis(xi, x_nodes, y_nodes)
    return sum(y_nodes[i] * basis[i] for i in range(len(y_nodes)))



# 2. Таблица конечных разностей

def finite_differences(y):
    cols = [list(y)]
    cur = list(y)
    for _ in range(len(y) - 1):
        nxt = [cur[j + 1] - cur[j] for j in range(len(cur) - 1)]
        cols.append(nxt)
        cur = nxt
    return cols



# 3. Таблица разделённых разностей

def divided_differences(x_nodes, y_nodes):
    n = len(x_nodes)
    table = [list(y_nodes)]
    for order in range(1, n):
        prev = table[order - 1]
        col = []
        for k in range(len(prev) - 1):
            col.append(
                (prev[k + 1] - prev[k]) /
                (x_nodes[k + order] - x_nodes[k])
            )
        table.append(col)
    return table



# 4. Полином Ньютона (через разделённые разности)

def newton(xi, x_nodes, dd_table):
    result = dd_table[0][0]
    product = 1.0
    for order in range(1, len(x_nodes)):
        product *= (xi - x_nodes[order - 1])
        result += dd_table[order][0] * product
    return result



# 5. Линейный сплайн

def linear_spline_coeffs(x_nodes, y_nodes):
    coeffs = []
    for k in range(len(x_nodes) - 1):
        x0, x1 = x_nodes[k], x_nodes[k + 1]
        y0, y1 = y_nodes[k], y_nodes[k + 1]
        a = (y1 - y0) / (x1 - x0)
        b = y0 - a * x0
        coeffs.append((a, b))
    return coeffs


def linear_spline_eval(xi, x_nodes, coeffs):
    for k in range(len(coeffs)):
        if x_nodes[k] <= xi <= x_nodes[k + 1]:
            a, b = coeffs[k]
            return a * xi + b
    return None



# 6. Квадратичный сплайн
#    n=5 точек => 2 звена по 3 точки:
#    звено 1: x[0], x[1], x[2]
#    звено 2: x[2], x[3], x[4]

def solve_3x3(A, b):
    import copy
    M = [A[i][:] + [b[i]] for i in range(3)]
    for col in range(3):
        pivot = max(range(col, 3), key=lambda r: abs(M[r][col]))
        M[col], M[pivot] = M[pivot], M[col]
        for row in range(col + 1, 3):
            if M[col][col] == 0:
                continue
            factor = M[row][col] / M[col][col]
            for j in range(col, 4):
                M[row][j] -= factor * M[col][j]
    sol = [0.0] * 3
    for i in range(2, -1, -1):
        sol[i] = M[i][3]
        for j in range(i + 1, 3):
            sol[i] -= M[i][j] * sol[j]
        sol[i] /= M[i][i]
    return sol


def quadratic_spline_coeffs(x_nodes, y_nodes):
    segments = [(0, 1, 2), (2, 3, 4)]
    coeffs = []
    for i0, i1, i2 in segments:
        xs = [x_nodes[i0], x_nodes[i1], x_nodes[i2]]
        ys = [y_nodes[i0], y_nodes[i1], y_nodes[i2]]
        A = [
            [xs[0]**2, xs[0], 1],
            [xs[1]**2, xs[1], 1],
            [xs[2]**2, xs[2], 1],
        ]
        sol = solve_3x3(A, ys)
        coeffs.append(tuple(sol))   # (a, b, c): ax²+bx+c
    boundaries = [(x_nodes[0], x_nodes[2]), (x_nodes[2], x_nodes[4])]
    return coeffs, boundaries


def quadratic_spline_eval(xi, coeffs, boundaries):
    for k, (lo, hi) in enumerate(boundaries):
        if lo <= xi <= hi:
            a, b, c = coeffs[k]
            return a * xi**2 + b * xi + c
    return None


# ГЛАВНАЯ ПРОГРАММА
print()
separator("═")
print("  ЛАБОРАТОРНАЯ РАБОТА №5 — ИНТЕРПОЛЯЦИЯ ТАБЛИЧНЫХ ФУНКЦИЙ")
print("  Вариант 21")
separator("═")

print("\nИсходные данные:")
print("  x: " + "  ".join(f"{v:7.3f}" for v in X))
print("  y: " + "  ".join(f"{v:7.3f}" for v in Y))
print(f"\nТочка вычисления: x1+x2 = {X[1]:.3f}+{X[2]:.3f} = {x_eval:.3f}")



# Задание 1: Многочлен Лагранжа

separator()
print("1. МНОГОЧЛЕН ЛАГРАНЖА")
separator()

print("\nБазисные полиномы p_i(x) определяются произведением:")
print("  p_i(x) = ∏_{j≠i} (x - x_j) / (x_i - x_j)\n")

print("Коэффициенты 1/∏(x_i - x_j):")
for i in range(n):
    den = 1.0
    for j in range(n):
        if j != i:
            den *= (X[i] - X[j])
    print(f"  1/den_{i} = 1/{den:.4f} = {1/den:.4f}")

L4_val = lagrange(x_eval, X, Y)
print(f"\nL4({x_eval:.3f}) = {L4_val:.6f}")

print("\nПроверка в узловых точках (должно совпадать с y_i):")
print(f"  {'xi':>8}  {'yi':>10}  {'L4(xi)':>10}  {'погрешн.':>12}")
for i in range(n):
    lv = lagrange(X[i], X, Y)
    print(f"  {X[i]:8.3f}  {Y[i]:10.4f}  {lv:10.6f}  {abs(lv-Y[i]):12.2e}")



# Задание 2: Таблицы разностей

separator()
print("2. ТАБЛИЦЫ РАЗНОСТЕЙ")
separator()

# --- Конечные разности ---
fd = finite_differences(Y)
print("\nТаблица конечных разностей:")
header = f"  {'k':>3}  {'xk':>7}  {'yk':>9}"
for order in range(1, n):
    header += f"  {'Δ^'+str(order)+'yk':>10}"
print(header)
separator("-", 70)
for k in range(n):
    row = f"  {k:3d}  {X[k]:7.3f}  {Y[k]:9.4f}"
    for order in range(1, n):
        if k < len(fd[order]):
            row += f"  {fd[order][k]:10.4f}"
        else:
            row += f"  {'':10}"
    print(row)

# --- Разделённые разности ---
dd = divided_differences(X, Y)
print("\nТаблица разделённых разностей:")
header = f"  {'k':>3}  {'xk':>7}  {'yk':>9}"
for order in range(1, n):
    header += f"  {f'f[{order}]':>12}"
print(header)
separator("-", 70)
for k in range(n):
    row = f"  {k:3d}  {X[k]:7.3f}  {Y[k]:9.4f}"
    for order in range(1, n):
        if k < len(dd[order]):
            row += f"  {dd[order][k]:12.6f}"
        else:
            row += f"  {'':12}"
    print(row)

print("\nКоэффициенты полинома Ньютона (первая строка каждого порядка):")
for order in range(n):
    print(f"  f[{order}] = {dd[order][0]:12.6f}")



# Задание 3: Полином Ньютона

separator()
print("3. ПОЛИНОМ НЬЮТОНА")
separator()

print("\nN4(x) = f[0]")
print("      + f[1]·(x-x0)")
print("      + f[2]·(x-x0)(x-x1)")
print("      + f[3]·(x-x0)(x-x1)(x-x2)")
print("      + f[4]·(x-x0)(x-x1)(x-x2)(x-x3)")

N4_val = newton(x_eval, X, dd)
print(f"\nN4({x_eval:.3f}) = {N4_val:.6f}")

print("\nПроверка в узловых точках:")
print(f"  {'xi':>8}  {'yi':>10}  {'N4(xi)':>10}  {'погрешн.':>12}")
for i in range(n):
    nv = newton(X[i], X, dd)
    print(f"  {X[i]:8.3f}  {Y[i]:10.4f}  {nv:10.6f}  {abs(nv-Y[i]):12.2e}")

print(f"\nL4 vs N4 в точке {x_eval:.3f}:")
print(f"  L4 = {L4_val:.6f}")
print(f"  N4 = {N4_val:.6f}")
print(f"  |L4 - N4| = {abs(L4_val - N4_val):.2e}  (должно быть ~0)")



# Задание 4: Сплайны

separator()
print("4. ИНТЕРПОЛЯЦИОННЫЕ СПЛАЙНЫ")
separator()

# --- Линейный сплайн ---
lin_c = linear_spline_coeffs(X, Y)
print("\nЛинейный сплайн φ(x) = a_k·x + b_k на каждом отрезке:\n")
print(f"  {'Отрезок':>18}  {'a_k':>10}  {'b_k':>10}")
separator("-", 50)
for k in range(len(lin_c)):
    a, b = lin_c[k]
    print(f"  [{X[k]:.3f}, {X[k+1]:.3f}]  {a:10.4f}  {b:10.4f}")

print("\nПроверка линейного сплайна в узловых точках:")
print(f"  {'xi':>8}  {'yi':>10}  {'φ(xi)':>10}  {'погрешн.':>12}")
for i in range(n):
    sv = linear_spline_eval(X[i], X, lin_c)
    print(f"  {X[i]:8.3f}  {Y[i]:10.4f}  {sv:10.6f}  {abs(sv-Y[i]):12.2e}")

# --- Квадратичный сплайн ---
q_coeffs, q_bounds = quadratic_spline_coeffs(X, Y)
print("\nКвадратичный сплайн φ(x) = a_k·x² + b_k·x + c_k:\n")
print(f"  {'Отрезок':>18}  {'a_k':>10}  {'b_k':>10}  {'c_k':>10}")
separator("-", 60)
for k, ((lo, hi), (a, b, c)) in enumerate(zip(q_bounds, q_coeffs)):
    print(f"  [{lo:.3f}, {hi:.3f}]  {a:10.4f}  {b:10.4f}  {c:10.4f}")

print("\nПроверка квадратичного сплайна в узловых точках:")
print(f"  {'xi':>8}  {'yi':>10}  {'φ(xi)':>10}  {'погрешн.':>12}")
for i in range(n):
    sv = quadratic_spline_eval(X[i], q_coeffs, q_bounds)
    print(f"  {X[i]:8.3f}  {Y[i]:10.4f}  {sv:10.6f}  {abs(sv-Y[i]):12.2e}")



# Задание 5: Сводная таблица значений (текстовый «график»)

separator()
print("5. СРАВНИТЕЛЬНАЯ ТАБЛИЦА ЗНАЧЕНИЙ")
separator()

step = (X[-1] - X[0]) / 20
xs_plot = [X[0] + step * i for i in range(21)]

print(f"\n  {'x':>7}  {'Лагранж':>10}  {'Ньютон':>10}  {'Лин.спл':>10}  {'Кв.спл':>10}")
separator("-", 60)
for xi in xs_plot:
    lv = lagrange(xi, X, Y)
    nv = newton(xi, X, dd)
    sv_lin = linear_spline_eval(xi, X, lin_c)
    sv_q   = quadratic_spline_eval(xi, q_coeffs, q_bounds)
    sv_lin_s = f"{sv_lin:10.4f}" if sv_lin is not None else f"{'—':>10}"
    sv_q_s   = f"{sv_q:10.4f}" if sv_q is not None else f"{'—':>10}"
    print(f"  {xi:7.3f}  {lv:10.4f}  {nv:10.4f}  {sv_lin_s}  {sv_q_s}")

separator("═")
print("  ИТОГ")
separator("═")
print(f"  Точка вычисления: x1+x2 = {x_eval:.4f}")
print(f"  L4({x_eval:.4f}) = {L4_val:.6f}")
print(f"  N4({x_eval:.4f}) = {N4_val:.6f}")
sv_lin_final = linear_spline_eval(x_eval, X, lin_c)
sv_q_final   = quadratic_spline_eval(x_eval, q_coeffs, q_bounds)
print(f"  Линейный сплайн({x_eval:.4f}) = {sv_lin_final:.6f}")
print(f"  Квадратичный сплайн({x_eval:.4f}) = {sv_q_final:.6f}")
separator("═")
