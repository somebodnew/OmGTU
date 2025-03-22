import math

def f(x):
    return math.pow(x+5,4)

def dh_method(a, b, eps):    
    if f(a) * f(b) >= 0:
        print("Метод дихотомии не может быть применен на данном отрезке.")
        return None

    while abs(b - a) > 2 * eps:
        x = (a + b) / 2
        x1 = x - eps / 2
        x2 = x + eps / 2

        if f(x1) > f(x2):
            a = x1 
        else: 
            b = x2

    return (a + b) / 2  # Возвращаем приближенное значение точки

# Ввод данных
a, b, eps = 0, math.pi, 0.001

# Решение
result = dh_method(a, b, eps)
print(f"Минимум в точке: {result:.5f}")
print(f"Значение функции в точке минимума: {f(result):.5f}")

def fibonacci(n):
    fib_sequence = [0, 1]
    for i in range(2, n):
        fib_sequence.append(fib_sequence[i-1] + fib_sequence[i-2])
    return fib_sequence

def fib_method(a, b, n):
    fib_numbers = fibonacci(n + 1)
    L = abs(b - a)
    
    for i in range(n, 2, -1):
        x1 = a + (fib_numbers[i-1] / fib_numbers[i]) * L
        x2 = b - (fib_numbers[i-1] / fib_numbers[i]) * L
        f1 = f(x1)
        f2 = f(x2)
        
        if f1 > f2: 
          b = x1
          f1 = f2
          x1 = x2
          L = b - a
          x2 = b - (fib_numbers[i-2] / fib_numbers[i-1]) * L
          
        else: 
          a = x2
          f2 = f1
          x2 = x1
          L = b - a
          x1 = a + (fib_numbers[i-2] / fib_numbers[i-1]) * L
        
    return (a + b) / 2

# Ввод данных
a, b, n = 0, math.pi, 100

# Решение
result = fib_method(a, b, n)
print(f"Минимум в точке: {result:.5f}")
print(f"Значение функции в точке минимума: {f(result):.5f}")


def gold_method(a, b, eps):
    tau = 0.618  # Золотое сечение
    L = abs(b - a)
    
    while L > eps:
        x1 = a + tau * L
        x2 = b - tau * L
        f1, f2 = f(x1), f(x2)
        if f1 > f2:
            b = x1
            f1 = f2
            x1 = x2
            L = abs(b - a)
            x2 = b - tau * L 
            f2 - f(x2)
        else:
            a = x2
            f2 = f1
            x2 = x1
            L = abs(b - a)
            x1 = a + tau * L 
            f1 = f(x1)
    
    return (a + b) / 2  # Возвращаем приближенную точку минимума

# Ввод данных
a, b, eps = 0, math.pi, 0.001

# Решение
result = gold_method(a, b, eps)
print(f"Минимум в точке: {result:.5f}")
print(f"Значение функции в точке минимума: {f(result):.5f}")
