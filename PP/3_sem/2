import numpy as np
from scipy.misc import derivative
import sympy as sp
from scipy.optimize import minimize


def y(x):
    return np.sin(np.log(x))


x0 = 4

f_prime = derivative(y, x0, dx=1e-6)
f_double_prime = derivative(y, x0, dx=1e-6, n=2)

print(f"Первая производная в x0 = {x0}: {f_prime}")
print(f"Вторая производная в x0 = {x0}: {f_double_prime}")  # 1

x = sp.symbols('x')

y_symbolic = sp.sin(sp.log(x))

y_derivative = sp.diff(y_symbolic, x)

print(f"Символьное представление первой производной: {y_derivative}")  # 2

a = 3
b = 8

def rectangle_integration(y,a,b,n):
    x = np.linspace(a,b,n)
    dx = (b-a) / n
    return np.sum(y(x)*dx)

integral_value = rectangle_integration(y,a,b,1000)

print(f"Определенный интеграл от {a} до {b}: {integral_value}")  # 3

y_integral_symbolic = sp.integrate(y_symbolic, x)

print(f"Неопределенный интеграл функции: {y_integral_symbolic}")  # 4

def L(x):
    x1, x2 = x
    return (x1 - 3) ** 2 + x2

x0_opt = np.array([0, 0])

# Решаем задачу
result = minimize(L, x0_opt, constraints = {'type': 'ineq', 'fun': lambda x: -2 * x[0] + 3 * x[1] - 4}, bounds=((0, None), (0, None)))

if result.success:
    print(f"Оптимальное значение: {result.fun}")
    print(f"Решение: x1 = {result.x[0]}, x2 = {result.x[1]}")
else:
    print("Оптимизация не удалась")
