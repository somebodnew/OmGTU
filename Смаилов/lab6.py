import math
import matplotlib.pyplot as plt

# ---------------------------
# Данные варианта 21
# ---------------------------
X = [0.351, 0.664, 0.978, 1.291, 1.605, 1.918, 2.232, 2.546, 2.859]
Y = [0.605, 0.265, 0.064, 0.116, 0.415, 0.728, 1.673, 3.138, 5.092]



def solve_linear_system(A, b):
    n = len(A)
    M = [row[:] + [b[i]] for i, row in enumerate(A)]

    for col in range(n):
        pivot = col
        for r in range(col + 1, n):
            if abs(M[r][col]) > abs(M[pivot][col]):
                pivot = r
        if abs(M[pivot][col]) < 1e-15:
            return None

        M[col], M[pivot] = M[pivot], M[col]

        div = M[col][col]
        for j in range(col, n + 1):
            M[col][j] /= div

        for r in range(n):
            if r == col:
                continue
            factor = M[r][col]
            if factor == 0:
                continue
            for j in range(col, n + 1):
                M[r][j] -= factor * M[col][j]

    return [M[i][n] for i in range(n)]

def least_squares_3(phi1, phi2, phi3, xdata, ydata):
    S11 = S12 = S13 = S22 = S23 = S33 = 0.0
    T1 = T2 = T3 = 0.0

    for x, y in zip(xdata, ydata):
        p1 = phi1(x)
        p2 = phi2(x)
        p3 = phi3(x)

        S11 += p1 * p1
        S12 += p1 * p2
        S13 += p1 * p3
        S22 += p2 * p2
        S23 += p2 * p3
        S33 += p3 * p3

        T1 += p1 * y
        T2 += p2 * y
        T3 += p3 * y

    A = [
        [S11, S12, S13],
        [S12, S22, S23],
        [S13, S23, S33],
    ]
    b = [T1, T2, T3]
    return solve_linear_system(A, b)


def residual_delta(yhat, ydata):
    s = 0.0
    for yh, y in zip(yhat, ydata):
        d = y - yh
        s += d * d
    return math.sqrt(s)


# ---------------------------
# 10 законов 
# ---------------------------

def fit_law_1(x, y):
    # (1) y = a*x + b*x^2 + c
    coeff = least_squares_3(lambda t: t, lambda t: t*t, lambda t: 1.0, x, y)
    if coeff is None:
        return None
    a, b, c = coeff
    yhat = [a*xi + b*xi*xi + c for xi in x]
    return ("(1) y = a*x + b*x^2 + c", (a, b, c), yhat)

def fit_law_2(x, y):
    # (2) y = a/(x + b) + c
    best = None
    for b in [ -2.0 + 0.01*i for i in range(0, 801) ]:
        ok = True
        for xi in x:
            if abs(xi + b) < 1e-6:
                ok = False
                break
        if not ok:
            continue
        coeff = least_squares_3(lambda t: 1.0/(t + b), lambda t: 0.0, lambda t: 1.0, x, y)
        if coeff is None:
            continue
        a, junk, c = coeff
        yhat = [a/(xi + b) + c for xi in x]
        d = residual_delta(yhat, y)
        if (best is None) or (d < best[0]):
            best = (d, b, a, c, yhat)
    if best is None:
        return None
    d, b, a, c, yhat = best
    return ("(2) y = a/(x + b) + c", (a, b, c), yhat)

def fit_law_3(x, y):
    # (3) y = a*ln x + b*x + c
    if any(xi <= 0 for xi in x):
        return None
    coeff = least_squares_3(lambda t: math.log(t), lambda t: t, lambda t: 1.0, x, y)
    if coeff is None:
        return None
    a, b, c = coeff
    yhat = [a*math.log(xi) + b*xi + c for xi in x]
    return ("(3) y = a*ln(x) + b*x + c", (a, b, c), yhat)

def fit_law_4(x, y):
    # (4) y = a/x + b + c*x
    if any(abs(xi) < 1e-12 for xi in x):
        return None
    coeff = least_squares_3(lambda t: 1.0/t, lambda t: t, lambda t: 1.0, x, y)
    if coeff is None:
        return None
    a, b, c = coeff
    yhat = [a/xi + c*xi + b for xi in x]
    return ("(4) y = a/x + b + c*x", (a, b, c), yhat)

def fit_law_5(x, y):
    # (5) y = a*sin(x) + b*x + c
    coeff = least_squares_3(lambda t: math.sin(t), lambda t: t, lambda t: 1.0, x, y)
    if coeff is None:
        return None
    a, b, c = coeff
    yhat = [a*math.sin(xi) + b*xi + c for xi in x]
    return ("(5) y = a*sin(x) + b*x + c", (a, b, c), yhat)

def fit_law_6(x, y):
    # (6) y = a*e^(b*x) + c 
    best = None
    for b in [ -5.0 + 0.02*i for i in range(0, 501) ]:
        coeff = least_squares_3(lambda t: math.exp(b*t), lambda t: 0.0, lambda t: 1.0, x, y)
        if coeff is None:
            continue
        a, junk, c = coeff
        yhat = [a*math.exp(b*xi) + c for xi in x]
        d = residual_delta(yhat, y)
        if (best is None) or (d < best[0]):
            best = (d, b, a, c, yhat)
    if best is None:
        return None
    d, b, a, c, yhat = best
    return ("(6) y = a*exp(b*x) + c", (a, b, c), yhat)

def fit_law_7(x, y):
    # (7) y = a*x + b*e^(-x) + c
    coeff = least_squares_3(lambda t: t, lambda t: math.exp(-t), lambda t: 1.0, x, y)
    if coeff is None:
        return None
    a, b, c = coeff
    yhat = [a*xi + b*math.exp(-xi) + c for xi in x]
    return ("(7) y = a*x + b*exp(-x) + c", (a, b, c), yhat)

def fit_law_8(x, y):
    # (8) y = a*ln(x) + b*exp(x) + c
    if any(xi <= 0 for xi in x):
        return None
    coeff = least_squares_3(lambda t: math.log(t), lambda t: math.exp(t), lambda t: 1.0, x, y)
    if coeff is None:
        return None
    a, b, c = coeff
    yhat = [a*math.log(xi) + b*math.exp(xi) + c for xi in x]
    return ("(8) y = a*ln(x) + b*exp(x) + c", (a, b, c), yhat)

def fit_law_9(x, y):
    # (9) y = a*x^2 + b*exp(x) + c
    coeff = least_squares_3(lambda t: t*t, lambda t: math.exp(t), lambda t: 1.0, x, y)
    if coeff is None:
        return None
    a, b, c = coeff
    yhat = [a*xi*xi + b*math.exp(xi) + c for xi in x]
    return ("(9) y = a*x^2 + b*exp(x) + c", (a, b, c), yhat)

def fit_law_10(x, y):
    # (10) y = a/(x^2 + b) + c
    best = None
    for b in [ -1.0 + 0.01*i for i in range(0, 1201) ]:
        ok = True
        for xi in x:
            if abs(xi*xi + b) < 1e-8:
                ok = False
                break
        if not ok:
            continue
        coeff = least_squares_3(lambda t: 1.0/(t*t + b), lambda t: 0.0, lambda t: 1.0, x, y)
        if coeff is None:
            continue
        a, junk, c = coeff
        yhat = [a/(xi*xi + b) + c for xi in x]
        d = residual_delta(yhat, y)
        if (best is None) or (d < best[0]):
            best = (d, b, a, c, yhat)
    if best is None:
        return None
    d, b, a, c, yhat = best
    return ("(10) y = a/(x^2 + b) + c", (a, b, c), yhat)


FITTERS = [
    fit_law_1, fit_law_2, fit_law_3, fit_law_4, fit_law_5,
    fit_law_6, fit_law_7, fit_law_8, fit_law_9, fit_law_10
]


results = []
for f in FITTERS:
    r = f(X, Y)
    if r is None:
        continue
    name, params, yhat = r
    d = residual_delta(yhat, Y)
    results.append((d, name, params))

results.sort(key=lambda t: t[0])

print("Вариант 21. Результаты (от лучшей невязки к худшей):\n")
for d, name, (a, b, c) in results:
    print(f"{name}")
    print(f"    a = {a:.6g}, b = {b:.6g}, c = {c:.6g}")
    print(f"    delta = {d:.6g}\n")

print("Два лучших закона:")
for i in range(min(2, len(results))):
    d, name, (a, b, c) = results[i]
    print(f"{i+1}) {name} | delta = {d:.6g}")
    
# 8 и 1
x_min, x_max = min(X), max(X)
x_plot = [x_min + (x_max - x_min)*t/500 for t in range(501)]

(d1, name1, (a1, b1, c1)), (d2, name2, (a2, b2, c2)) = results[:2]

y1 = [a1*math.log(xi) + b1*math.exp(xi) + c1 for xi in x_plot]
y2 = [a2*xi + b2*xi*xi + c2 for xi in x_plot]

plt.figure(figsize=(9, 6))
plt.scatter(X, Y, label="Начальыне данные", color="black", zorder=3)

plt.plot(x_plot, y1, label=f"{name1} (delta={d1:.3g})", linestyle="-")
plt.plot(x_plot, y2, label=f"{name2} (delta={d2:.3g})", linestyle="--")

plt.xlabel("x")
plt.ylabel("y")
plt.title("Сравнение двух лучших аппроксимаций (вариант 21)")
plt.legend()
plt.grid(True)
plt.show()
