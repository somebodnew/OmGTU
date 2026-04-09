import math
import random
import time
import matplotlib.pyplot as plt
import numpy as np


# 1. ТЕСТОВЫЕ ФУНКЦИИ И ПАРАМЕТРЫ

class BenchmarkFunction:
    def __init__(self, name, func, bounds, true_min):
        self.name = name
        self.func = func
        self.bounds = bounds
        self.true_min = true_min

def sphere(x, y):
    return x**2 + y**2

def rastrigin(x, y):
    A = 10
    return A * 2 + (x**2 - A * math.cos(2 * math.pi * x)) + (y**2 - A * math.cos(2 * math.pi * y))

def ackley(x, y):
    term1 = -20.0 * math.exp(-0.2 * math.sqrt(0.5 * (x**2 + y**2)))
    term2 = -math.exp(0.5 * (math.cos(2 * math.pi * x) + math.cos(2 * math.pi * y)))
    return term1 + term2 + math.e + 20.0

def holder_table(x, y):
    term = math.sqrt(x**2 + y**2)
    val = -abs(math.sin(x) * math.cos(y) * math.exp(abs(1 - term / math.pi)))
    return val

def rosenbrock(x, y):
    return (1 - x)**2 + 100 * (y - x**2)**2

FUNCTIONS = [
    BenchmarkFunction("Sphere", sphere, [-5.12, 5.12], 0.0),
    BenchmarkFunction("Rastrigin", rastrigin, [-5.12, 5.12], 0.0),
    BenchmarkFunction("Ackley", ackley, [-32.0, 32.0], 0.0),
    BenchmarkFunction("Holder Table", holder_table, [-10.0, 10.0], -19.2085),
    BenchmarkFunction("Rosenbrock", rosenbrock, [-2.048, 2.048], 0.0) # Минимум в (1,1)
]



# 2. АЛГОРИТМ ДИФФЕРЕНЦИАЛЬНОЙ ЭВОЛЮЦИИ (DE)

def init_population(pop_size, bounds):
    return [[random.uniform(bounds[0], bounds[1]), random.uniform(bounds[0], bounds[1])] 
            for _ in range(pop_size)]

def mutate(population, F, bounds):
    mutated_pop = []
    pop_size = len(population)
    for i in range(pop_size):
        candidates = [idx for idx in range(pop_size) if idx != i]
        r1, r2, r3 = random.sample(candidates, 3)
        
        v = [
            population[r1][0] + F * (population[r2][0] - population[r3][0]),
            population[r1][1] + F * (population[r2][1] - population[r3][1])
        ]
        
        v[0] = max(bounds[0], min(bounds[1], v[0]))
        v[1] = max(bounds[0], min(bounds[1], v[1]))
        mutated_pop.append(v)
    return mutated_pop

def crossover(target, mutant, CR):
    trial = []
    j_rand = random.randint(0, 1)
    for j in range(2):
        if random.random() < CR or j == j_rand:
            trial.append(mutant[j])
        else:
            trial.append(target[j])
    return trial

def select(target, trial, func):
    if func(*trial) <= func(*target):
        return trial
    return target

def measure_diversity(population):
    if len(population) < 2: return 0
    total_dist = 0
    count = 0
    sample = random.sample(population, min(10, len(population)))
    for i in range(len(sample)):
        for j in range(i + 1, len(sample)):
            dist = math.sqrt((sample[i][0]-sample[j][0])**2 + (sample[i][1]-sample[j][1])**2)
            total_dist += dist
            count += 1
    return total_dist / count if count > 0 else 0



# 3. ЗАПУСК ЭКСПЕРИМЕНТА

def run_experiment(func_obj, pop_size=50, generations=100, runs=20):
    results = []
    best_run_history = None
    best_run_fitness = float('inf')
    
    print(f"Запуск серии экспериментов для {func_obj.name}...")
    
    for run_idx in range(runs):
        population = init_population(pop_size, func_obj.bounds)
        history_best = []
        history_avg = []
        history_div = []
        
        start_time = time.time()
        
        F = 0.5
        CR = 0.9
        
        for gen in range(generations):
            fitnesses = [func_obj.func(ind[0], ind[1]) for ind in population]
            current_best = min(fitnesses)
            current_avg = sum(fitnesses) / pop_size
            
            history_best.append(current_best)
            history_avg.append(current_avg)
            history_div.append(measure_diversity(population))
            
            mutated_pop = mutate(population, F, func_obj.bounds)
            new_population = []
            
            for i in range(pop_size):
                trial = crossover(population[i], mutated_pop[i], CR)
                winner = select(population[i], trial, func_obj.func)
                new_population.append(winner)
            
            population = new_population
            
        end_time = time.time()
        
        final_fitness = min([func_obj.func(ind[0], ind[1]) for ind in population])
        best_ind = min(population, key=lambda ind: func_obj.func(ind[0], ind[1]))
        
        results.append({
            'fitness': final_fitness,
            'time': end_time - start_time,
            'best_individual': best_ind
        })
        
        if final_fitness < best_run_fitness:
            best_run_fitness = final_fitness
            best_run_history = {
                'best': history_best,
                'avg': history_avg,
                'div': history_div,
                'populations': [p.copy() for p in population]
            }

    return results, best_run_history



# 4. ВИЗУАЛИЗАЦИЯ И АНАЛИЗ

def plot_function_landscape(func_obj, population, title_suffix=""):
    x = np.linspace(func_obj.bounds[0], func_obj.bounds[1], 100)
    y = np.linspace(func_obj.bounds[1], func_obj.bounds[1], 100)
    # Исправление для корректных границ Y (берем те же, что и X для простоты, если квадратные, или свои)
    # В нашем случае bounds - это [min, max], одинаковые для X и Y
    y = np.linspace(func_obj.bounds[0], func_obj.bounds[1], 100)
    
    X, Y = np.meshgrid(x, y)
    Z = np.zeros_like(X)
    
    func_vec = np.vectorize(func_obj.func)
    Z = func_vec(X, Y)
    
    plt.figure(figsize=(8, 6))
    contour = plt.contourf(X, Y, Z, levels=30, cmap='viridis', alpha=0.7)
    plt.colorbar(contour, label='Значение функции')
    
    pop_arr = np.array(population)
    plt.scatter(pop_arr[:, 0], pop_arr[:, 1], c='red', s=15, edgecolors='white', label='Популяция')
    
    plt.title(f"Ландшафт: {func_obj.name} {title_suffix}")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.legend()
    plt.grid(True)

def plot_comparison_boxplots(all_results):
    fig, ax = plt.subplots(figsize=(10, 6))
    
    data = []
    labels = []
    
    for func_name, res_list in all_results.items():
        fitnesses = [r['fitness'] for r in res_list]
        data.append(fitnesses)
        labels.append(func_name)
        
    bp = ax.boxplot(data, labels=labels, patch_artist=True)
    
    colors = ['lightblue', 'lightgreen', 'salmon', 'plum', 'orange']
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        
    ax.set_title("Сравнение качества решения (20 запусков)")
    ax.set_ylabel("Найденное значение функции (чем меньше, тем лучше)")
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    plt.xticks(rotation=15)
    plt.tight_layout()
    plt.show()

def print_summary_table(all_results):
    print("\n" + "="*80)
    print(f"{'Функция':<15} | {'Мин. знач.':<12} | {'Сред. знач.':<12} | {'Макс. знач.':<12} | {'Ср. время (с)':<12}")
    print("="*80)
    
    for func_name, res_list in all_results.items():
        fitnesses = [r['fitness'] for r in res_list]
        times = [r['time'] for r in res_list]
        
        min_val = min(fitnesses)
        avg_val = sum(fitnesses) / len(fitnesses)
        max_val = max(fitnesses)
        avg_time = sum(times) / len(times)
        
        print(f"{func_name:<15} | {min_val:<12.6f} | {avg_val:<12.6f} | {max_val:<12.6f} | {avg_time:<12.4f}")
    print("="*80)



# 5. ГЛАВНЫЙ БЛОК

POP_SIZE = 40
GENERATIONS = 150
NUM_RUNS = 40

all_experiment_results = {}
best_histories = {}

# 1. Проведение экспериментов
for func_obj in FUNCTIONS:
    results, best_hist = run_experiment(func_obj, POP_SIZE, GENERATIONS, NUM_RUNS)
    all_experiment_results[func_obj.name] = results
    best_histories[func_obj.name] = best_hist

# 2. Сводный анализ и таблица
print_summary_table(all_experiment_results)

# 3. Визуализация сравнения (Боксплоты)
plot_comparison_boxplots(all_experiment_results)

# 4. Детальная визуализация для каждой функции
for func_obj in FUNCTIONS:
    hist = best_histories[func_obj.name]
    if hist:
        fig, axs = plt.subplots(1, 2, figsize=(14, 5))
        
        axs[0].plot(hist['best'], label='Лучшая приспособленность', color='red')
        axs[0].plot(hist['avg'], label='Средняя приспособленность', color='blue', linestyle='--')
        axs[0].set_title(f"Сходимость: {func_obj.name}")
        axs[0].set_xlabel("Поколение")
        axs[0].set_ylabel("Значение функции")
        axs[0].legend()
        axs[0].grid(True)
        
        axs[1].plot(hist['div'], color='purple')
        axs[1].set_title(f"Разнообразие популяции: {func_obj.name}")
        axs[1].set_xlabel("Поколение")
        axs[1].set_ylabel("Среднее расстояние между особями")
        axs[1].grid(True)
        
        plt.tight_layout()
        plt.show()
        
        plot_function_landscape(func_obj, hist['populations'], "(Финал лучшего запуска)")
        plt.show()