import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import FancyArrowPatch
import matplotlib.colors as mcolors
import time
import warnings
warnings.filterwarnings('ignore')

# Настройка стиля
plt.rcParams.update({
    'figure.facecolor': '#0d1117',
    'axes.facecolor': '#161b22',
    'axes.edgecolor': '#30363d',
    'axes.labelcolor': '#e6edf3',
    'xtick.color': '#8b949e',
    'ytick.color': '#8b949e',
    'text.color': '#e6edf3',
    'grid.color': '#21262d',
    'grid.alpha': 0.8,
    'font.family': 'DejaVu Sans',
    'axes.titlesize': 11,
    'axes.labelsize': 10,
})

COLORS = {
    'ackley':     '#58a6ff',
    'rastrigin':  '#3fb950',
    'holder':     '#f78166',
    'sphere':     '#d2a8ff',
    'rosenbrock': '#ffa657',
}
ACCENT = '#f0883e'
BG = '#0d1117'
PANEL = '#161b22'

# 1. ТЕСТОВЫЕ ФУНКЦИИ

def ackley(x):
    n = len(x)
    a, b, c = 20, 0.2, 2 * np.pi
    s1 = np.sum(x**2)
    s2 = np.sum(np.cos(c * x))
    return -a * np.exp(-b * np.sqrt(s1 / n)) - np.exp(s2 / n) + a + np.e

def rastrigin(x):
    n = len(x)
    return 10 * n + np.sum(x**2 - 10 * np.cos(2 * np.pi * x))

def holder_table(x):
    x1, x2 = x[0], x[1]
    return -np.abs(np.sin(x1) * np.cos(x2) * np.exp(np.abs(1 - np.sqrt(x1**2 + x2**2) / np.pi)))

def sphere(x):
    return np.sum(x**2)

def rosenbrock(x):
    return np.sum(100 * (x[1:] - x[:-1]**2)**2 + (1 - x[:-1])**2)

FUNCTIONS = {
    'Ackley':      {'fn': ackley,       'bounds': (-32.768, 32.768), 'optimum': 0.0,       'dim': 2, 'color': COLORS['ackley']},
    'Rastrigin':   {'fn': rastrigin,    'bounds': (-5.12,   5.12),   'optimum': 0.0,       'dim': 2, 'color': COLORS['rastrigin']},
    'Holder Table':{'fn': holder_table, 'bounds': (-10.0,   10.0),   'optimum': -19.2085,  'dim': 2, 'color': COLORS['holder']},
    'Sphere':      {'fn': sphere,       'bounds': (-5.12,   5.12),   'optimum': 0.0,       'dim': 2, 'color': COLORS['sphere']},
    'Rosenbrock':  {'fn': rosenbrock,   'bounds': (-2.048,  2.048),  'optimum': 0.0,       'dim': 2, 'color': COLORS['rosenbrock']},
}

# 2. АЛГОРИТМ РОЯ ЧАСТИЦ (PSO)

class PSO:
    """
    Стандартный PSO с инерционным весом.
    Параметры:
      w  - инерционный вес (снижается линейно)
      c1 - когнитивный коэффициент
      c2 - социальный коэффициент
    """
    def __init__(self, func, bounds, dim=2,
                 n_particles=40, max_iter=200,
                 w_start=0.9, w_end=0.4, c1=2.0, c2=2.0,
                 seed=None):
        self.func = func
        self.lb, self.ub = bounds
        self.dim = dim
        self.n = n_particles
        self.max_iter = max_iter
        self.w_start = w_start
        self.w_end = w_end
        self.c1 = c1
        self.c2 = c2
        rng = np.random.default_rng(seed)

        self.pos = rng.uniform(self.lb, self.ub, (self.n, self.dim))
        self.vel = rng.uniform(-(self.ub - self.lb), self.ub - self.lb, (self.n, self.dim))
        self.rng = rng
        self.pbest_pos = self.pos.copy()
        self.pbest_val = np.array([func(p) for p in self.pos])
        idx = np.argmin(self.pbest_val)
        self.gbest_pos = self.pbest_pos[idx].copy()
        self.gbest_val = self.pbest_val[idx]

    def run(self, store_history=False):
        history_best = []
        history_mean = []
        history_diversity = []
        history_positions = []
        conv_iter = self.max_iter

        for t in range(self.max_iter):
            w = self.w_start - (self.w_start - self.w_end) * t / self.max_iter
            r1 = self.rng.random((self.n, self.dim))
            r2 = self.rng.random((self.n, self.dim))
            self.vel = (w * self.vel
                        + self.c1 * r1 * (self.pbest_pos - self.pos)
                        + self.c2 * r2 * (self.gbest_pos - self.pos))
            
            vmax = (self.ub - self.lb) * 0.2
            self.vel = np.clip(self.vel, -vmax, vmax)
            self.pos = self.pos + self.vel
            self.pos = np.clip(self.pos, self.lb, self.ub)

            vals = np.array([self.func(p) for p in self.pos])
            improved = vals < self.pbest_val
            self.pbest_val = np.where(improved, vals, self.pbest_val)
            self.pbest_pos = np.where(improved[:, None], self.pos, self.pbest_pos)

            idx = np.argmin(self.pbest_val)
            if self.pbest_val[idx] < self.gbest_val:
                self.gbest_val = self.pbest_val[idx]
                self.gbest_pos = self.pbest_pos[idx].copy()
                if conv_iter == self.max_iter:
                    conv_iter = t

            history_best.append(self.gbest_val)
            history_mean.append(np.mean(vals))
            diversity = np.mean(np.std(self.pos, axis=0))
            history_diversity.append(diversity)
            if store_history and t % 10 == 0:
                history_positions.append(self.pos.copy())

        return {
            'best_val': self.gbest_val,
            'best_pos': self.gbest_pos,
            'history_best': history_best,
            'history_mean': history_mean,
            'history_diversity': history_diversity,
            'history_positions': history_positions,
            'conv_iter': conv_iter,
        }


# 3. ЭКСПЕРИМЕНТЫ

def run_experiments(n_runs=20, max_iter=200, n_particles=40):
    results = {}
    print("=" * 60)
    print("  PSO — Эксперименты на 5 тестовых функциях")
    print("=" * 60)

    for name, cfg in FUNCTIONS.items():
        print(f"\n* {name}  ({n_runs} запусков)...")
        best_vals = []
        times = []
        conv_iters = []
        first_history = None

        for run in range(n_runs):
            t0 = time.time()
            pso = PSO(cfg['fn'], cfg['bounds'], dim=cfg['dim'],
                      n_particles=n_particles, max_iter=max_iter,
                      seed=run * 42)
            r = pso.run(store_history=(run == 0))
            elapsed = time.time() - t0
            best_vals.append(r['best_val'])
            times.append(elapsed)
            conv_iters.append(r['conv_iter'])
            if run == 0:
                first_history = r

        best_vals = np.array(best_vals)
        optimum = cfg['optimum']
        rel_err = np.abs(best_vals - optimum) / (np.abs(optimum) + 1e-12) * 100

        results[name] = {
            'best_vals': best_vals,
            'times': times,
            'conv_iters': conv_iters,
            'first_history': first_history,
            'optimum': optimum,
            'rel_err': rel_err,
            'color': cfg['color'],
        }

        print(f"   min={best_vals.min():.6f}  mean={best_vals.mean():.6f}  "
              f"max={best_vals.max():.6f}  time={np.mean(times):.3f}s")

    return results


# 4. ВИЗУАЛИЗАЦИЯ

def plot_convergence(results):
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    fig.patch.set_facecolor(BG)
    fig.suptitle('PSO — Кривые сходимости (лучшее и среднее значение)',
                 color='#e6edf3', fontsize=14, fontweight='bold', y=0.98)

    axes_flat = axes.flatten()
    for ax in axes_flat[5:]:
        ax.set_visible(False)

    for i, (name, data) in enumerate(results.items()):
        ax = axes_flat[i]
        h = data['first_history']
        iters = range(len(h['history_best']))
        c = data['color']
        ax.plot(iters, h['history_best'], color=c, lw=2, label='Лучшее')
        ax.plot(iters, h['history_mean'], color=c, lw=1, alpha=0.5, linestyle='--', label='Среднее')
        ax.fill_between(iters, h['history_best'], h['history_mean'], alpha=0.07, color=c)
        ax.set_title(name, color='#e6edf3', fontweight='bold')
        ax.set_xlabel('Итерация')
        ax.set_ylabel('Значение функции')
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)
        ax.set_facecolor(PANEL)
        for spine in ax.spines.values():
            spine.set_edgecolor('#30363d')

    plt.tight_layout()
    plt.savefig('/mnt/user-data/outputs/01_convergence.png', dpi=150, bbox_inches='tight',
                facecolor=BG)
    plt.close()


def plot_search_space(results):
    fig, axes = plt.subplots(2, 3, figsize=(18, 11))
    fig.patch.set_facecolor(BG)
    fig.suptitle('PSO — Пространство поиска и финальные позиции частиц',
                 color='#e6edf3', fontsize=14, fontweight='bold', y=0.98)

    axes_flat = axes.flatten()
    for ax in axes_flat[5:]:
        ax.set_visible(False)

    for i, (name, cfg) in enumerate(FUNCTIONS.items()):
        ax = axes_flat[i]
        lb, ub = cfg['bounds']
        xs = np.linspace(lb, ub, 300)
        ys = np.linspace(lb, ub, 300)
        X, Y = np.meshgrid(xs, ys)
        Z = np.array([[cfg['fn'](np.array([x, y])) for x in xs] for y in ys])

        c_map = ax.contourf(X, Y, Z, levels=40, cmap='inferno', alpha=0.85)
        ax.contour(X, Y, Z, levels=15, colors='white', alpha=0.15, linewidths=0.5)

        # Позиции частиц из первого запуска (финальные)
        data = results[name]
        h = data['first_history']
        if h['history_positions']:
            last_pos = h['history_positions'][-1]
            ax.scatter(last_pos[:, 0], last_pos[:, 1],
                       c=data['color'], s=20, alpha=0.8, zorder=5, edgecolors='white', linewidths=0.3)

        # Глобальный минимум
        best_pos = h['best_pos']
        ax.scatter(best_pos[0], best_pos[1], c='#f0f6fc', s=120,
                   marker='*', zorder=10, edgecolors=data['color'], linewidths=1.5)

        ax.set_title(name, color='#e6edf3', fontweight='bold')
        ax.set_xlabel('x1')
        ax.set_ylabel('x2')
        ax.set_facecolor(PANEL)
        for spine in ax.spines.values():
            spine.set_edgecolor('#30363d')
        plt.colorbar(c_map, ax=ax, pad=0.01)

    plt.tight_layout()
    plt.savefig('/mnt/user-data/outputs/02_search_space.png', dpi=150, bbox_inches='tight',
                facecolor=BG)
    plt.close()


def plot_diversity(results):
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    fig.patch.set_facecolor(BG)
    fig.suptitle('PSO — Разнообразие популяции по итерациям',
                 color='#e6edf3', fontsize=14, fontweight='bold', y=0.98)

    axes_flat = axes.flatten()
    for ax in axes_flat[5:]:
        ax.set_visible(False)

    for i, (name, data) in enumerate(results.items()):
        ax = axes_flat[i]
        div = data['first_history']['history_diversity']
        iters = range(len(div))
        c = data['color']
        ax.fill_between(iters, div, alpha=0.25, color=c)
        ax.plot(iters, div, color=c, lw=2)
        ax.set_title(name, color='#e6edf3', fontweight='bold')
        ax.set_xlabel('Итерация')
        ax.set_ylabel('Разнообразие (σ)')
        ax.grid(True, alpha=0.3)
        ax.set_facecolor(PANEL)
        for spine in ax.spines.values():
            spine.set_edgecolor('#30363d')

    plt.tight_layout()
    plt.savefig('/mnt/user-data/outputs/03_diversity.png', dpi=150, bbox_inches='tight',
                facecolor=BG)
    plt.close()


def plot_boxplots(results):
    fig, ax = plt.subplots(figsize=(14, 6))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(PANEL)
    ax.set_title('PSO — Сводное сравнение: боксплоты результатов (20 запусков)',
                 color='#e6edf3', fontsize=13, fontweight='bold')

    names = list(results.keys())
    data_list = [results[n]['best_vals'] for n in names]
    colors_list = [results[n]['color'] for n in names]

    bp = ax.boxplot(data_list, patch_artist=True, notch=False,
                    medianprops=dict(color='white', linewidth=2),
                    whiskerprops=dict(color='#8b949e'),
                    capprops=dict(color='#8b949e'),
                    flierprops=dict(marker='o', color='#8b949e', alpha=0.5, markersize=4))

    for patch, color in zip(bp['boxes'], colors_list):
        patch.set_facecolor(color)
        patch.set_alpha(0.6)
        patch.set_edgecolor(color)

    ax.set_xticks(range(1, len(names) + 1))
    ax.set_xticklabels(names, fontsize=10)
    ax.set_ylabel('Найденное минимальное значение')
    ax.grid(True, alpha=0.3, axis='y')
    for spine in ax.spines.values():
        spine.set_edgecolor('#30363d')

    plt.tight_layout()
    plt.savefig('/mnt/user-data/outputs/04_boxplots.png', dpi=150, bbox_inches='tight',
                facecolor=BG)
    plt.close()


def plot_metrics_table(results):
    fig, ax = plt.subplots(figsize=(16, 5))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.axis('off')

    col_labels = ['Функция', 'Оптимум', 'Min', 'Mean', 'Max',
                  'Std', 'Ср. итераций', 'Ср. время (с)', 'Отн. ошибка (%)']
    rows = []
    for name, data in results.items():
        bv = data['best_vals']
        rows.append([
            name,
            f"{data['optimum']:.4f}",
            f"{bv.min():.6f}",
            f"{bv.mean():.6f}",
            f"{bv.max():.6f}",
            f"{bv.std():.6f}",
            f"{np.mean(data['conv_iters']):.1f}",
            f"{np.mean(data['times']):.3f}",
            f"{data['rel_err'].mean():.2f}",
        ])

    table = ax.table(cellText=rows, colLabels=col_labels,
                     loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1.0, 2.0)

    for (r, c), cell in table.get_celld().items():
        cell.set_facecolor('#161b22' if r > 0 else '#21262d')
        cell.set_edgecolor('#30363d')
        cell.set_text_props(color='#e6edf3' if r > 0 else '#f0883e',
                            fontweight='bold' if r == 0 else 'normal')

    ax.set_title('Сводная таблица метрик эффективности PSO',
                 color='#e6edf3', fontsize=13, fontweight='bold', pad=20)

    plt.tight_layout()
    plt.savefig('/mnt/user-data/outputs/05_metrics_table.png', dpi=150, bbox_inches='tight',
                facecolor=BG)
    plt.close()


def plot_convergence_speed(results):
    fig, ax = plt.subplots(figsize=(12, 6))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(PANEL)
    ax.set_title('PSO — Сравнение скорости сходимости (нормированное)',
                 color='#e6edf3', fontsize=13, fontweight='bold')

    for name, data in results.items():
        h = data['first_history']['history_best']
        arr = np.array(h)
        mn, mx = arr.min(), arr[0]
        if mx - mn > 1e-12:
            norm = (arr - mn) / (mx - mn)
        else:
            norm = np.zeros_like(arr)
        ax.plot(norm, color=data['color'], lw=2, label=name)

    ax.set_xlabel('Итерация')
    ax.set_ylabel('Нормированное значение (0=лучшее)')
    ax.legend()
    ax.grid(True, alpha=0.3)
    for spine in ax.spines.values():
        spine.set_edgecolor('#30363d')

    plt.tight_layout()
    plt.savefig('/mnt/user-data/outputs/06_speed_comparison.png', dpi=150, bbox_inches='tight',
                facecolor=BG)
    plt.close()


# 5. АНАЛИЗ И ВЫВОД

def print_analysis(results):
    print("\n" + "=" * 60)
    print("  АНАЛИЗ ЭФФЕКТИВНОСТИ PSO")
    print("=" * 60)

    for name, data in results.items():
        bv = data['best_vals']
        ci = data['conv_iters']
        times = data['times']
        print(f"\n{name}")
        print(f"   Оптимум теор.:   {data['optimum']:.6f}")
        print(f"   Найдено  min:    {bv.min():.6f}")
        print(f"   Найдено  mean:   {bv.mean():.6f}  ± {bv.std():.6f}")
        print(f"   Найдено  max:    {bv.max():.6f}")
        print(f"   Отн. ошибка:     {data['rel_err'].mean():.3f}%")
        print(f"   Итераций (mean): {np.mean(ci):.1f}")
        print(f"   Время (mean):    {np.mean(times):.3f} с")



# 6. MAIN

import os
os.makedirs('/mnt/user-data/outputs', exist_ok=True)

print("\nЗапуск экспериментов PSO...")
results = run_experiments(n_runs=20, max_iter=200, n_particles=40)

print("\nГенерация графиков...")
plot_convergence(results)
plot_search_space(results)
plot_diversity(results)
plot_boxplots(results)
plot_metrics_table(results)
plot_convergence_speed(results)

print_analysis(results)
