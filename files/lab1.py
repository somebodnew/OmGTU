import numpy as np
import matplotlib
matplotlib.use('Agg')
import os
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable

# ─────────────────────────────────────────
#  1. ЦЕЛЕВАЯ ФУНКЦИЯ — Экли (2D)
# ─────────────────────────────────────────
def ackley(x: np.ndarray, a=20, b=0.2, c=2*np.pi) -> float:
    """Функция Экли. Глобальный минимум: f(0,0) = 0."""
    d = len(x)
    sum_sq   = np.sum(x**2)
    sum_cos  = np.sum(np.cos(c * x))
    return -a * np.exp(-b * np.sqrt(sum_sq / d)) \
           - np.exp(sum_cos / d) \
           + a + np.e


# ─────────────────────────────────────────
#  2. ИНИЦИАЛИЗАЦИЯ ПОПУЛЯЦИИ
# ─────────────────────────────────────────
def init_population(pop_size: int, dim: int, bounds: tuple) -> np.ndarray:
    """Случайная инициализация особей в пределах bounds."""
    low, high = bounds
    return np.random.uniform(low, high, (pop_size, dim))


# ─────────────────────────────────────────
#  3. ПРИСПОСОБЛЕННОСТЬ
# ─────────────────────────────────────────
def compute_fitness(population: np.ndarray) -> np.ndarray:
    """
    Приспособленность = обратное значение функции Экли.
    Чем меньше Экли → тем выше fitness.
    """
    scores = np.array([ackley(ind) for ind in population])
    # fitness: 1 / (1 + ackley) → [0, 1], больше — лучше
    return 1.0 / (1.0 + scores)


# ─────────────────────────────────────────
#  4. ОТБОР (турнирный)
# ─────────────────────────────────────────
def tournament_selection(population: np.ndarray, fitness: np.ndarray,
                         k: int = 3) -> np.ndarray:
    """Турнирный отбор: выбираем k случайных особей, побеждает лучшая."""
    selected = []
    pop_size = len(population)
    for _ in range(pop_size):
        contestants = np.random.choice(pop_size, k, replace=False)
        winner = contestants[np.argmax(fitness[contestants])]
        selected.append(population[winner])
    return np.array(selected)


# ─────────────────────────────────────────
#  5. СКРЕЩИВАНИЕ (SBX — симулированный двоичный)
# ─────────────────────────────────────────
def crossover(parents: np.ndarray, crossover_rate: float = 0.9,
              eta: float = 15.0) -> np.ndarray:
    """SBX-скрещивание (Simulated Binary Crossover)."""
    pop_size, dim = parents.shape
    offspring = parents.copy()
    for i in range(0, pop_size - 1, 2):
        if np.random.rand() < crossover_rate:
            p1, p2 = parents[i], parents[i+1]
            u = np.random.rand(dim)
            beta = np.where(u <= 0.5,
                            (2 * u) ** (1 / (eta + 1)),
                            (1 / (2 * (1 - u))) ** (1 / (eta + 1)))
            offspring[i]   = 0.5 * ((1 + beta) * p1 + (1 - beta) * p2)
            offspring[i+1] = 0.5 * ((1 - beta) * p1 + (1 + beta) * p2)
    return offspring


# ─────────────────────────────────────────
#  6. МУТАЦИЯ (гауссова)
# ─────────────────────────────────────────
def mutate(offspring: np.ndarray, mutation_rate: float = 0.1,
           sigma: float = 0.3, bounds: tuple = (-5, 5)) -> np.ndarray:
    """Гауссова мутация с ограничением по границам."""
    mutated = offspring.copy()
    mask = np.random.rand(*mutated.shape) < mutation_rate
    mutated[mask] += np.random.normal(0, sigma, mutated.shape)[mask]
    return np.clip(mutated, bounds[0], bounds[1])


# ─────────────────────────────────────────
#  7. ЗАМЕНА ПОПУЛЯЦИИ (элитизм)
# ─────────────────────────────────────────
def replace_population(population: np.ndarray, offspring: np.ndarray,
                       fitness: np.ndarray, elite_size: int = 5) -> np.ndarray:
    """Сохраняем elite_size лучших из родителей, остальные — потомки."""
    elite_idx  = np.argsort(fitness)[-elite_size:]
    elite      = population[elite_idx]
    new_pop    = np.vstack([elite, offspring[:len(population) - elite_size]])
    return new_pop


# ─────────────────────────────────────────
#  8. РАЗНООБРАЗИЕ ПОПУЛЯЦИИ
# ─────────────────────────────────────────
def population_diversity(population: np.ndarray) -> float:
    """Среднее стандартное отклонение по каждому измерению."""
    return float(np.mean(np.std(population, axis=0)))


# ─────────────────────────────────────────
#  9. ГЛАВНЫЙ ЦИКЛ ГА
# ─────────────────────────────────────────
def genetic_algorithm(pop_size=100, dim=2, bounds=(-5, 5),
                      n_generations=150, crossover_rate=0.9,
                      mutation_rate=0.15, sigma=0.3,
                      elite_size=5, tournament_k=3, seed=42):
    np.random.seed(seed)

    population = init_population(pop_size, dim, bounds)
    history = {
        'best_fitness':  [],
        'mean_fitness':  [],
        'best_ackley':   [],
        'diversity':     [],
        'best_solution': None,
        'snapshots':     [],   # (поколение, популяция) для визуализации
    }

    snap_gens = [0, 25, 50, 100, n_generations - 1]

    for gen in range(n_generations):
        fitness  = compute_fitness(population)

        best_idx  = np.argmax(fitness)
        best_ind  = population[best_idx]
        best_ack  = ackley(best_ind)

        history['best_fitness'].append(float(np.max(fitness)))
        history['mean_fitness'].append(float(np.mean(fitness)))
        history['best_ackley'].append(best_ack)
        history['diversity'].append(population_diversity(population))

        if gen in snap_gens:
            history['snapshots'].append((gen, population.copy(), fitness.copy()))

        # Лучшее решение за всё время
        if history['best_solution'] is None or best_ack < ackley(history['best_solution']):
            history['best_solution'] = best_ind.copy()

        # Операторы ГА
        parents  = tournament_selection(population, fitness, k=tournament_k)
        offspring = crossover(parents, crossover_rate)
        offspring = mutate(offspring, mutation_rate, sigma, bounds)
        population = replace_population(population, offspring, fitness, elite_size)

    return history


# ─────────────────────────────────────────
#  10. ВИЗУАЛИЗАЦИЯ
# ─────────────────────────────────────────
def visualize(history: dict, bounds=(-5, 5), save_path=None):
    if save_path is None:
        save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ga_results.png')

    gens   = np.arange(len(history['best_fitness']))
    colors = plt.cm.viridis(np.linspace(0.2, 0.95, len(history['snapshots'])))

    # Поверхность Экли
    N = 300
    x1 = np.linspace(bounds[0], bounds[1], N)
    x2 = np.linspace(bounds[0], bounds[1], N)
    X1, X2 = np.meshgrid(x1, x2)
    Z = np.array([[ackley(np.array([x1v, x2v])) for x1v in x1] for x2v in x2])

    fig = plt.figure(figsize=(18, 14))
    fig.patch.set_facecolor('#0f1117')
    gs  = gridspec.GridSpec(2, 3, figure=fig, hspace=0.45, wspace=0.35)

    ax_title = fig.add_axes([0, 0.94, 1, 0.06])
    ax_title.axis('off')
    ax_title.text(0.5, 0.5,
                  'Генетический алгоритм — минимизация функции Экли',
                  ha='center', va='center', fontsize=18, fontweight='bold',
                  color='white', transform=ax_title.transAxes)

    style = dict(facecolor='#1a1d27', edgecolor='#3a3d4d')

    # ── График 1: приспособленность ──────────────────────────
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.set_facecolor('#1a1d27')
    ax1.plot(gens, history['best_fitness'], color='#4fc3f7', lw=2, label='Макс. fitness')
    ax1.plot(gens, history['mean_fitness'], color='#ffb74d', lw=2, label='Ср. fitness')
    ax1.set_title('Приспособленность по поколениям', color='white', pad=8)
    ax1.set_xlabel('Поколение', color='#aaa')
    ax1.set_ylabel('Fitness', color='#aaa')
    ax1.legend(facecolor='#2a2d3a', edgecolor='none', labelcolor='white')
    ax1.tick_params(colors='#aaa')
    for sp in ax1.spines.values(): sp.set_color('#3a3d4d')

    # ── График 2: значение Экли ──────────────────────────────
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.set_facecolor('#1a1d27')
    ax2.plot(gens, history['best_ackley'], color='#ef5350', lw=2)
    ax2.axhline(0, ls='--', color='#66bb6a', lw=1.5, label='Теор. минимум (0)')
    ax2.set_title('Лучшее значение f(x) — Экли', color='white', pad=8)
    ax2.set_xlabel('Поколение', color='#aaa')
    ax2.set_ylabel('f(x)', color='#aaa')
    ax2.legend(facecolor='#2a2d3a', edgecolor='none', labelcolor='white')
    ax2.tick_params(colors='#aaa')
    for sp in ax2.spines.values(): sp.set_color('#3a3d4d')

    # ── График 3: разнообразие ───────────────────────────────
    ax3 = fig.add_subplot(gs[0, 2])
    ax3.set_facecolor('#1a1d27')
    ax3.fill_between(gens, history['diversity'], color='#ab47bc', alpha=0.4)
    ax3.plot(gens, history['diversity'], color='#ce93d8', lw=2)
    ax3.set_title('Разнообразие популяции', color='white', pad=8)
    ax3.set_xlabel('Поколение', color='#aaa')
    ax3.set_ylabel('σ (std)', color='#aaa')
    ax3.tick_params(colors='#aaa')
    for sp in ax3.spines.values(): sp.set_color('#3a3d4d')

    # ── График 4: контур Экли + снимки популяций ─────────────
    ax4 = fig.add_subplot(gs[1, :2])
    ax4.set_facecolor('#1a1d27')
    cf = ax4.contourf(X1, X2, Z, levels=40, cmap='inferno', alpha=0.85)
    cbar = fig.colorbar(cf, ax=ax4, pad=0.02)
    cbar.ax.tick_params(colors='#aaa')
    cbar.set_label('f(x)', color='#aaa')

    for i, (gen, pop, fit) in enumerate(history['snapshots']):
        sc = ax4.scatter(pop[:, 0], pop[:, 1],
                         c=[colors[i]] * len(pop),
                         s=22, alpha=0.75, edgecolors='none',
                         label=f'Поколение {gen}')

    best = history['best_solution']
    ax4.scatter(best[0], best[1], marker='*', s=350,
                color='#76ff03', zorder=10, label=f'Лучшее: ({best[0]:.3f}, {best[1]:.3f})')
    ax4.scatter(0, 0, marker='+', s=200, color='white', lw=2, zorder=10, label='Глоб. минимум (0,0)')

    ax4.set_title('Пространство решений — эволюция популяции', color='white', pad=8)
    ax4.set_xlabel('x₁', color='#aaa')
    ax4.set_ylabel('x₂', color='#aaa')
    ax4.tick_params(colors='#aaa')
    for sp in ax4.spines.values(): sp.set_color('#3a3d4d')
    leg = ax4.legend(facecolor='#2a2d3a', edgecolor='none', labelcolor='white', fontsize=8)

    # ── График 5: итоговая сводка ─────────────────────────────
    ax5 = fig.add_subplot(gs[1, 2])
    ax5.set_facecolor('#1a1d27')
    ax5.axis('off')

    found = ackley(history['best_solution'])
    theoretical = 0.0
    error = abs(found - theoretical)

    lines = [
        ('Параметры ГА', None, '#4fc3f7'),
        ('Размер популяции', '100',     '#ddd'),
        ('Число поколений', '150',      '#ddd'),
        ('Вероятность скрещ.', '0.90',  '#ddd'),
        ('Вероятность мутац.', '0.15',  '#ddd'),
        ('Элитизм', '5 особей',         '#ddd'),
        ('Отбор', 'Турнирный (k=3)',    '#ddd'),
        ('', None, None),
        ('Результаты', None, '#4fc3f7'),
        ('Найденный минимум', f'{found:.6f}', '#66bb6a' if found < 0.01 else '#ffb74d'),
        ('Теор. минимум', f'{theoretical:.6f}', '#ddd'),
        ('Абс. погрешность', f'{error:.6f}',  '#ef5350' if error > 0.01 else '#66bb6a'),
        ('Координата x₁', f'{history["best_solution"][0]:.6f}', '#ddd'),
        ('Координата x₂', f'{history["best_solution"][1]:.6f}', '#ddd'),
    ]

    y = 0.97
    for label, value, color in lines:
        if color is None:
            y -= 0.05
            continue
        if value is None:
            ax5.text(0.05, y, label, color=color, fontsize=10,
                     fontweight='bold', transform=ax5.transAxes)
        else:
            ax5.text(0.05, y, label + ':', color='#aaa', fontsize=9,
                     transform=ax5.transAxes)
            ax5.text(0.65, y, value, color=color, fontsize=9,
                     fontweight='bold', transform=ax5.transAxes)
        y -= 0.066

    ax5.set_title('Сводка', color='white', pad=8)
    for sp in ax5.spines.values(): sp.set_color('#3a3d4d')

    plt.savefig(save_path, dpi=150, bbox_inches='tight', facecolor='#0f1117')
    plt.close()
    print(f"Сохранено: {save_path}")
    return found, theoretical, error


# ─────────────────────────────────────────
#  ЗАПУСК
# ─────────────────────────────────────────
if __name__ == '__main__':
    print("Запуск генетического алгоритма...")
    history = genetic_algorithm(
        pop_size=100, dim=2, bounds=(-5, 5),
        n_generations=150, crossover_rate=0.9,
        mutation_rate=0.15, sigma=0.3,
        elite_size=5, tournament_k=3, seed=42
    )

    found, theoretical, error = visualize(history)

    print("\n=== РЕЗУЛЬТАТЫ ===")
    print(f"Найденный минимум:    {found:.8f}")
    print(f"Теоретический минимум:{theoretical:.8f}")
    print(f"Абс. погрешность:     {error:.8f}")
    print(f"Координаты:           {history['best_solution']}")
