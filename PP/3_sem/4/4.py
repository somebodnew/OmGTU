import numpy as np
import matplotlib.pyplot as plt
from for4ex import x,y,uniform_data,normal_data,L

# 1. значения функции y = sin(ln(x)) на отрезке [3, 8]

print(x,y,sep='\n')

# 2. график функции с названием и подписями осей
plt.figure(figsize=(10, 5))
plt.plot(x, y, label='y = sin(ln(x))')
plt.title('График функции y = sin(ln(x))', fontsize=14)
plt.xlabel('x', fontsize=14)
plt.ylabel('y', fontsize=14)
plt.legend()
plt.grid()
plt.show()

# 3. точечный график функции
plt.figure(figsize=(10, 5))
plt.scatter(x, y, color=(0.1, 0.2, 0.8), marker='h')
plt.title('Точечный график функции y = sin(ln(x))', fontsize=14)
plt.xlabel('x', fontsize=12)
plt.ylabel('y', fontsize=12)
plt.grid(color='gray', alpha=0.5)
plt.show()


# 4. выборки и гистограммы
plt.figure(figsize=(10, 5))
plt.hist(uniform_data, bins=10, color='blue', alpha=0.7, label='Равномерное распределение')
plt.hist(normal_data, bins=15, color='orange', alpha=0.7, label='Нормальное распределение')
plt.title('Гистограммы выборок', fontsize=14)
plt.xlabel('Значения', fontsize=12)
plt.ylabel('Частота', fontsize=12)
plt.legend()
plt.show()

# 5. Генерируем выборку из равномерного распределения
sample = np.random.randint(1, 5, size=50)
unique, counts = np.unique(sample, return_counts=True)

# Строим круговую диаграмму
plt.figure(figsize=(10, 5))
plt.pie(counts, labels=unique, colors=['gold', 'lightblue', 'lightgreen', 'gray'], autopct='%1.1f%%')
plt.title('Круговая диаграмма частоты значений', fontsize=14)
plt.show()

# Строим столбчатую диаграмму
plt.figure(figsize=(10, 5))
plt.bar(unique, counts, color=['magenta', 'blue', 'yellow','cyan'])
plt.title('Столбчатая диаграмма частоты значений', fontsize=14)
plt.xlabel('Значения', fontsize=12)
plt.ylabel('Частота', fontsize=12)
plt.xticks(unique)
plt.show()

# 6. Строим трехмерный график функции
x1 = np.linspace(3, 8, 100)
x2 = np.linspace(0, 6, 100)
X1, X2 = np.meshgrid(x1, x2)
Z = L(X1, X2)

fig = plt.figure(figsize=(10, 5))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X1, X2, Z, cmap='viridis')
ax.set_title('3D график функции', fontsize=12)
plt.show()

# 7. Строим сетку 2x2
fig, axs = plt.subplots(2, 2, figsize=(12, 8))
fig.suptitle('Сетка графиков', fontsize=16)

# График из пункта 2
axs[0, 0].plot(x, y, label='y = sin(ln(x))')
axs[0, 0].set_title('График функции', fontsize=12)
axs[0, 0].set_xlabel('x')
axs[0, 0].set_ylabel('y')
axs[0, 0].legend()

# График из пункта 3
axs[0, 1].scatter(x, y, color=(0.1, 0.2, 0.8), marker='o')
axs[0, 1].set_title('Точечный график функции', fontsize=12)
axs[0, 1].set_xlabel('x')
axs[0, 1].set_ylabel('y')
axs[0, 1].set_facecolor('#eafff5')

# Круговая диаграмма из пункта 5
axs[1, 0].pie(counts, labels=unique, colors=['gold', 'lightblue', 'lightgreen', 'gray'], autopct='%1.1f%%')
axs[1, 0].set_title('Круговая диаграмма частоты', fontsize=12)

# 3D график из пункта 6
ax = fig.add_subplot(2, 2, 4, projection='3d')
ax.plot_surface(X1, X2, Z)
ax.set_title('3D график', fontsize=12)

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()

# 8. Попробуем разные стили оформления
styles = ['fivethirtyeight', 'ggplot', 'dark_background','classic']
for style in styles:
    plt.style.use(style)
    plt.figure(figsize=(12, 8))
    plt.subplot(2, 2, 1)
    plt.plot(x, y)
    plt.title('График функции')
    
    plt.subplot(2, 2, 2)
    plt.scatter(x, y, marker='o')
    plt.title('Точечный график функции')

    plt.subplot(2, 2, 3)
    plt.pie(counts, labels=unique, autopct='%1.1f%%')
    plt.title('Круговая диаграмма частоты')

    ax = plt.subplot(2, 2, 4, projection='3d')
    ax.plot_surface(X1, X2, Z)
    ax.set_title('3D график')

    plt.suptitle(f'Стили оформления: {style}', fontsize=16)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()
