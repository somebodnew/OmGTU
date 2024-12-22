import numpy as np
import matplotlib.pyplot as plt
x = np.linspace(3, 8, 100)
y = np.sin(np.log(x))

np.random.seed(0)
uniform_data = np.random.randint(0, 100, size=100)
normal_data = np.random.normal(loc=0, scale=10, size=100).astype(int)

def L(x1, x2):
    return (x1 - 3) ** 2 + x2
