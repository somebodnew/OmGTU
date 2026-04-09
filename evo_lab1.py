import math
import random
import matplotlib.pyplot as plt
import numpy as np

# 1. ЦЕЛЕВАЯ ФУНКЦИЯ И ПРИСПОСОБЛЕННОСТЬ

def ackley_function(x, y):
    term1 = -20.0 * math.exp(-0.2 * math.sqrt(0.5 * (x**2 + y**2)))
    term2 = -math.exp(0.5 * (math.cos(2 * math.pi * x) + math.cos(2 * math.pi * y)))
    return term1 + term2 + math.e + 20.0

def calculate_fitness(x, y):
    return -ackley_function(x, y)



# 2. МОДУЛИ ГЕНЕТИЧЕСКОГО АЛГОРИТМА

def create_individual(bounds):
    return [random.uniform(bounds[0], bounds[1]), random.uniform(bounds[0], bounds[1])]

def init_population(pop_size, bounds):
    return [create_individual(bounds) for _ in range(pop_size)]

def tournament_selection(population, fitnesses, k=3):
    selected_indices = random.sample(range(len(population)), k)
    best_idx = max(selected_indices, key=lambda idx: fitnesses[idx])
    return population[best_idx]

def crossover(parent1, parent2, crossover_rate=0.8):
    if random.random() < crossover_rate:
        alpha = random.random()
        child1 = [alpha * parent1[0] + (1 - alpha) * parent2[0], 
                  alpha * parent1[1] + (1 - alpha) * parent2[1]]
        return child1
    return parent1.copy()

def mutate(individual, bounds, mutation_rate=0.1, step=0.5):
    if random.random() < mutation_rate:
        individual[0] += random.uniform(-step, step)
        individual[1] += random.uniform(-step, step)
        
        individual[0] = max(bounds[0], min(bounds[1], individual[0]))
        individual[1] = max(bounds[0], min(bounds[1], individual[1]))
    return individual

def measure_diversity(population):
    unique_individuals = set((round(ind[0], 2), round(ind[1], 2)) for ind in population)
    return len(unique_individuals)



# 3. ОСНОВНОЙ ЦИКЛ АЛГОРИТМА

def run_genetic_algorithm(pop_size=50, generations=100, bounds=[-5.0, 5.0]):
    population = init_population(pop_size, bounds)
    
    history_max_fit = []
    history_avg_fit = []
    history_diversity = []
    history_populations = []
    
    best_overall_individual = None
    best_overall_fitness = -float('inf')
    
    for gen in range(generations):
        fitnesses = [calculate_fitness(ind[0], ind[1]) for ind in population]
        
        max_fit = max(fitnesses)
        avg_fit = sum(fitnesses) / pop_size
        
        history_max_fit.append(max_fit)
        history_avg_fit.append(avg_fit)
        history_diversity.append(measure_diversity(population))
        history_populations.append([ind.copy() for ind in population])
        
        best_idx = fitnesses.index(max_fit)
        if max_fit > best_overall_fitness:
            best_overall_fitness = max_fit
            best_overall_individual = population[best_idx].copy()
            
        new_population = [population[best_idx].copy()]
        
        while len(new_population) < pop_size:
            p1 = tournament_selection(population, fitnesses)
            p2 = tournament_selection(population, fitnesses)
            
            child = crossover(p1, p2)
            child = mutate(child, bounds)
            
            new_population.append(child)
            
        population = new_population

    return best_overall_individual, ackley_function(*best_overall_individual), \
           history_max_fit, history_avg_fit, history_diversity, history_populations

# 4. ВИЗУАЛИЗАЦИЯ И АНАЛИЗ

def visualize_results(history_max_fit, history_avg_fit, history_diversity, history_pops, bounds):
    generations = range(len(history_max_fit))
    
    fig = plt.figure(figsize=(15, 10))
    
    # 1. График изменения приспособленности
    ax1 = fig.add_subplot(2, 2, 1)
    ax1.plot(generations, history_max_fit, label='Макс. приспособленность (Лучшая)', color='red')
    ax1.plot(generations, history_avg_fit, label='Ср. приспособленность', color='blue')
    ax1.set_title('Изменение приспособленности по поколениям')
    ax1.set_xlabel('Номер поколения')
    ax1.set_ylabel('Приспособленность (-Ackley)')
    ax1.legend()
    ax1.grid(True)

    # 2. График разнообразия
    ax2 = fig.add_subplot(2, 2, 2)
    ax2.plot(generations, history_diversity, color='purple')
    ax2.set_title('Разнообразие популяции')
    ax2.set_xlabel('Номер поколения')
    ax2.set_ylabel('Кол-во уникальных особей')
    ax2.grid(True)

    # 3. Распределение особей в пространстве (Начало, Середина, Конец)
    ax3 = fig.add_subplot(2, 1, 2)
    

    x = np.linspace(bounds[0], bounds[1], 100)
    y = np.linspace(bounds[0], bounds[1], 100)
    X, Y = np.meshgrid(x, y)
    Z = np.zeros_like(X)
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            Z[i, j] = ackley_function(X[i, j], Y[i, j])
            
    contour = ax3.contourf(X, Y, Z, levels=20, cmap='viridis', alpha=0.6)
    plt.colorbar(contour, ax=ax3, label='Значение функции Экли')
    
    pop_first = np.array(history_pops[0])
    pop_mid = np.array(history_pops[len(history_pops)//2])
    pop_last = np.array(history_pops[-1])
    
    ax3.scatter(pop_first[:, 0], pop_first[:, 1], c='black', marker='x', label='Поколение 0', alpha=0.6)
    ax3.scatter(pop_mid[:, 0], pop_mid[:, 1], c='blue', marker='s', label=f'Поколение {len(history_pops)//2}', alpha=0.6)
    ax3.scatter(pop_last[:, 0], pop_last[:, 1], c='red', marker='o', label=f'Поколение {len(history_pops)-1} (Финал)')
    
    ax3.set_title('Распределение особей в пространстве решений (Функция Экли)')
    ax3.set_xlabel('Ось X')
    ax3.set_ylabel('Ось Y')
    ax3.legend()

    plt.tight_layout()
    plt.show()

POPULATION_SIZE = 50
NUM_GENERATIONS = 60
BOUNDS = [-5.0, 5.0]

print("Запуск Генетического Алгоритма...")
best_ind, best_val, max_fit_hist, avg_fit_hist, div_hist, pops_hist = run_genetic_algorithm(
    pop_size=POPULATION_SIZE, 
    generations=NUM_GENERATIONS, 
    bounds=BOUNDS
)

print("-" * 40)
print("АНАЛИЗ РЕЗУЛЬТАТОВ:")
print(f"Теоретический минимум Экли: x = 0.0, y = 0.0, f(x,y) = 0.0")
print(f"Найденный минимум ГА:       x = {best_ind[0]:.6f}, y = {best_ind[1]:.6f}, f(x,y) = {best_val:.6f}")
print(f"Абсолютная ошибка по f(x,y): {abs(0.0 - best_val):.6f}")
print("-" * 40)

visualize_results(max_fit_hist, avg_fit_hist, div_hist, pops_hist, BOUNDS)