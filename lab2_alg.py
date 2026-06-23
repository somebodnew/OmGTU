import random
import time
import matplotlib.pyplot as plt

def bubble_sort(arr):
    n = len(arr)
    count = 0
    for i in range(n-1):
        for j in range(0, n-i-1):
            count+=1
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return count

def gnome_sort(arr):
    i = 0
    count = 0
    while i < len(arr):
        count+=1
        if i == 0 or arr[i] >= arr[i-1]:
            i += 1
        else:
            arr[i], arr[i-1] = arr[i-1], arr[i]
            i -= 1
    return count

def insertion_sort(arr):
    count = 0
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            count+=1
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return count

def test_algorithms():
    
    sizes = [10, 100, 500, 1000, 2000]
    
    bubble_times = []
    gnome_times = []
    insertion_times = []

    bubble_count = []
    gnome_count = []
    insertion_count = []
    
    for size in sizes:
        arr = [random.randint(1, 10000) for _ in range(size)]
        
        
        # Пузырьковая
        arr_copy = arr.copy()
        start = time.time()
        temp = 0
        temp = bubble_sort(arr_copy)
        bubble_times.append(time.time() - start)
        bubble_count.append(temp)
        
        # Гномья
        arr_copy = arr.copy()
        start = time.time()
        temp = 0
        temp = gnome_sort(arr_copy)
        gnome_times.append(time.time() - start)
        gnome_count.append(temp)
        
        # Вставками
        arr_copy = arr.copy()
        start = time.time()
        temp = 0
        temp = insertion_sort(arr_copy)
        insertion_times.append(time.time() - start)
        insertion_count.append(temp)
        
        print(f"Размер: {size:4d} | Пузырьком: {bubble_times[-1]:.5f}с | "
              f"Гномья: {gnome_times[-1]:.5f}с | Вставками: {insertion_times[-1]:.5f}с")

    
    # график 1: Время выполнения
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    plt.plot(sizes, bubble_times, 'ro-', label='Пузырьковая', linewidth=2)
    plt.plot(sizes, gnome_times, 'go-', label='Гномья', linewidth=2)
    plt.plot(sizes, insertion_times, 'bo-', label='Вставками', linewidth=2)
    plt.xlabel('Размер массива')
    plt.ylabel('Время (секунды)')
    plt.title('Время выполнения алгоритмов')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # график 2: Количество перестановок
    plt.subplot(1, 2, 2)
    
    plt.plot(sizes, bubble_count, 'ro-', label='Пузырьковая', linewidth=2)
    plt.plot(sizes, gnome_count, 'go-', label='Гномья', linewidth=2)
    plt.plot(sizes, insertion_count, 'bo-', label='Вставками', linewidth=2)
    plt.xlabel('Размер массива')
    plt.ylabel('Количество сравнений')
    plt.title('Эффективность алгоритмов')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    plt.tight_layout()
    plt.show()
    
   
test_algorithms()
