import matplotlib.pyplot as plt
import time
import numpy as np

def recursion(n):
    if n <= 1:
        return n
    return recursion(n - 1) + recursion(n - 2)


    
def iteration(n):
    if n <= 1:
        return n
    arr = [0] * (n + 1)
    arr[1] = 1
    for i in range(2, n + 1):
        arr[i] = arr[i - 1] + arr[i - 2]
    return arr[n]

n_values = list(range(41))
time_rec = [0] * 41
time_ite = [0] * 41

for test in range(41):
    
    rec_times = []
    for _ in range(5):
        start = time.perf_counter()
        recursion(test)
        end = time.perf_counter()
        rec_times.append(end - start)
    
    time_rec[test] = np.mean(rec_times)  

    ite_times = []
    for _ in range(5):
        start = time.perf_counter()
        iteration(test)
        end = time.perf_counter()
        ite_times.append(end - start)
    time_ite[test] = np.mean(ite_times)

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

axes[0].plot(n_values, time_ite, 'b-o', linewidth=2, markersize=4, label='Итерация')
axes[0].set_title('Время выполнения итерационного метода', fontsize=14, fontweight='bold')
axes[0].set_xlabel('n (номер числа Фибоначчи)', fontsize=12)
axes[0].set_ylabel('Время (секунды)', fontsize=12)
axes[0].grid(True, alpha=0.3)
axes[0].legend(fontsize=11)
axes[0].set_xlim(0, 40)

axes[1].plot(n_values, time_rec, 'r-o', linewidth=2, markersize=4, label='Рекурсия')
axes[1].set_title('Время выполнения рекурсивного метода', fontsize=14, fontweight='bold')
axes[1].set_xlabel('n (номер числа Фибоначчи)', fontsize=12)
axes[1].set_ylabel('Время (секунды)', fontsize=12)
axes[1].grid(True, alpha=0.3)
axes[1].legend(fontsize=11)
axes[1].set_xlim(0, 40)

axes[1].set_yscale('log')
axes[1].set_ylabel('Время (секунды, логарифмическая шкала)', fontsize=12)

for ax in axes:
    ax.tick_params(axis='both', which='major', labelsize=10)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.show()
