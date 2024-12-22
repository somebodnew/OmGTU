import numpy as np
from scipy.linalg import det, lu
from scipy import stats

A = np.array([[4, -3.4, 1, 1.8],
              [-2, 8, 0, -9],
              [2, -2.5, -7, 4],
              [1, -1, 5, 1]])
print(A)

P, L, U = lu(A)
print(P,L,U,sep = '\n')

det_L = np.prod(np.diag(L))
det_U = np.prod(np.diag(U))
det_P_inv = det(P)  
det_total = det_L * det_U * det_P_inv
print(det_P_inv,det_L,det_U,det_total,sep = '\n')

# Генерация выборки с равномерным распределением
uniform_sample = np.random.randint(0, 100, size=100)
print(uniform_sample)

# Генерация выборки с нормальным распределением
normal_sample = np.random.normal(loc=50, scale=15, size=100).astype(int)
print(normal_sample)

def calculate_statistics(sample):
    return {
        'mean': np.mean(sample),
        'mode': np.argmax(np.bincount(sample.astype(int))),
        'median': np.median(sample),
        'min': np.min(sample),
        'max': np.max(sample),
        'std_dev': np.std(sample)
    }
uniform_stats = calculate_statistics(uniform_sample)
normal_stats = calculate_statistics(normal_sample)
print(uniform_sample,normal_sample,sep='/n')


expected_frequencies = np.full(100, 1/100) 

chi2_uniform, p_value_uniform = stats.chisquare(uniform_sample, expected_frequencies)
chi2_normal, p_value_normal = stats.chisquare(normal_sample, expected_frequencies)
print(p_value_uniform,p_value_normal,sep='/n')
