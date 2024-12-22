import numpy as np
from scipy.linalg import det, lu
from scipy import stats
from AMatrix import A

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
normal_sample = np.random.normal(loc=0, scale=10, size=100).astype(int)
print(normal_sample)

def calculate_statistics(sample):
    return {
        'mean': np.mean(sample),
        'mode': stats.mode(sample),
        'median': np.median(sample),
        'min': np.min(sample),
        'max': np.max(sample),
        'std_dev': np.std(sample)
    }
uniform_stats = calculate_statistics(uniform_sample)
normal_stats = calculate_statistics(normal_sample)
print(uniform_sample,normal_sample,sep='\n')

_, p_value_uniform = stats.chisquare(uniform_sample)
_, p_value_normal = stats.chisquare(normal_sample)
print(p_value_uniform,p_value_normal,sep='\n')
