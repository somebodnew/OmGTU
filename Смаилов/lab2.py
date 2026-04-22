

def f(x):
    return x**3 + 7*x - 7

def f1(x):
    return 3 *(x**2) + 7

def f2(x):
    return 6*x

# x^3 = 7 - 7x
# x = 0 => a = 0, b = 1

def section(a, b, e = 0.01):
    i = 0
    while abs(b - a) >= e:
        i += 1
        x = (b + a) / 2

        print(f"{i} итерация {a:.2f} {b:.2f} {x:.2f}")
        
        fa = f(a)
        fb = f(b)
        fx = f(x)
        
        if fa*fx < 0:
            b = x
        if fx*fb < 0:
            a = x
    return x

print(f"{section(0,1):.2f}")
print()

#МЕтод Ньютона
# для а f(x)f''(x) = -7, не > 0
# для b f(x)f''(x) = 7, > 0  =>  x0 = b

def newton(x0, e = 0.01):
    i = 1
    x = x0 - (f(x0)/f1(x0))
    print(f"{i} итерация {x0:.2f} {x:.2f}")
    while abs(x - x0) >= e:
        i += 1
        x0 = x
        x = x0 - (f(x0)/f1(x0))
        print(f"{i} итерация {x0:.2f} {x:.2f}")
        
    return x

print(f"{newton(1):.2f}")
print()


# M = 1.01 * f1(1) = 10.1
# phi(x) = x - F(x)/m

def phi(x):
    return x - f(x)/10.1


def simple_iteration(x0, e = 0.01):
    i = 1
    x = phi(x0)
    print(f"{i} итерация {x0:.2f} {x:.2f}")
    while abs(x - x0) >= e:
        i += 1
        x0 = x
        x = phi(x0)
        print(f"{i} итерация {x0:.2f} {x:.2f}")
        
    return x 



print(f"{simple_iteration(1):.2f}")
print()


#Разностный Ньютон с пост. шагом
def newton_constant_step(x0, h = 1e-5, eps = 1e-6, max_iter = 1000):
    x = x0
    iterations = []
    
    for n in range(max_iter):
        fx = f(x)
        denom = f(x+h) - fx
        
        if abs(denom) < 1e-14:
            raise ZeroDivisionError("Denom_small")
        
        x_next = x - fx * h / denom
        iterations.append((n,x,fx,x_next))
        
        if abs(x_next - x) < eps:
            return x_next
        
        x = x_next
    
    raise ValueError("Max_iter")


print(f"{newton_constant_step(1):.2f}")
print()

#метод Стеффенсона
def steffensen(x0, eps = 1e-6, max_iter = 1000):
    x = x0
    iterations = []
    
    for n in range(max_iter):
        fx = f(x)
        denom = f(x+fx) - fx
        
        if abs(denom) < 1e-14:
            raise ZeroDivisionError("Denom_small")
        
        x_next = x - (fx ** 2 ) / denom
        iterations.append((n,x,fx,x_next))
        
        if abs(x_next - x) < eps:
            return x_next
        
        x = x_next
    
    raise ValueError("Max_iter")

print(f"{steffensen(1):.2f}")
print()