def copy_mat(A):
    return [row[:] for row in A]

def norm_inf(v):
    return max(abs(x) for x in v) if v else 0.0

def mat_vec(A, x):
    return [sum(a * xi for a, xi in zip(row, x)) for row in A]

def vec_sub(a, b):
    return [x - y for x, y in zip(a, b)]

def swap_rows(M, i, j):
    M[i], M[j] = M[j], M[i]

def inverse(A, eps=1e-12):
    A = copy_mat(A)
    n = len(A)
    I = [[0.0] * n for _ in range(n)]
    for i in range(n):
        I[i][i] = 1.0

    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(A[r][col]))
        if abs(A[pivot][col]) < eps:
            raise ValueError("Матрица необратима (нулевой pivot).")
        if pivot != col:
            swap_rows(A, pivot, col)
            swap_rows(I, pivot, col)

        div = A[col][col]
        for k in range(n):
            A[col][k] /= div
            I[col][k] /= div

        for row in range(n):
            if row == col:
                continue
            factor = A[row][col]
            if factor == 0:
                continue
            for k in range(n):
                A[row][k] -= factor * A[col][k]
                I[row][k] -= factor * I[col][k]

    return I

def gauss(A, b, eps=1e-12):
    A = copy_mat(A)
    b = b[:]
    n = len(A)

    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(A[r][col]))
        if abs(A[pivot][col]) < eps:
            raise ValueError("Система вырожденная или имеет бесконечно много решений (нулевой pivot).")
        if pivot != col:
            swap_rows(A, pivot, col)
            b[pivot], b[col] = b[col], b[pivot]

        for row in range(col + 1, n):
            factor = A[row][col] / A[col][col]
            if factor == 0:
                continue
            for k in range(col, n):
                A[row][k] -= factor * A[col][k]
            b[row] -= factor * b[col]

    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        s = sum(A[i][j] * x[j] for j in range(i + 1, n))
        x[i] = (b[i] - s) / A[i][i]
    return x

def by_inverse(A, b):
    Inv = inverse(A)
    return [sum(Inv[i][j] * b[j] for j in range(len(b))) for i in range(len(b))]


def jacobi(A, b, x0=None, eps=1e-9, max_iter=10000):
    n = len(A)
    x = [0.0] * n if x0 is None else x0[:]
    x_new = x[:]

    for _ in range(max_iter):
        for i in range(n):
            s = sum(A[i][j] * x[j] for j in range(n) if j != i)
            x_new[i] = (b[i] - s) / A[i][i]

        if norm_inf(vec_sub(x_new, x)) < eps:
            return x_new
        x, x_new = x_new, x 

    return x

def seidel(A, b, x0=None, eps=1e-9, max_iter=10000):
    n = len(A)
    x = [0.0] * n if x0 is None else x0[:]

    for _ in range(max_iter):
        old = x[:]
        for i in range(n):
            s1 = sum(A[i][j] * x[j] for j in range(i))
            s2 = sum(A[i][j] * old[j] for j in range(i + 1, n))
            x[i] = (b[i] - s1 - s2) / A[i][i]

        if norm_inf(vec_sub(x, old)) < eps:
            return x

    return x

def progonka(A, b):
    n = len(A)
    a = [0.0] * n
    b = [0.0] * n
    c = [0.0] * n
    d = [0.0] * n
    for i in range(n):
        b[i] = A[i][i]
        if i > 0:
            a[i] = A[i][i - 1]
        if i < n - 1:
            c[i] = A[i][i + 1]
        d[i] = b[i]
    
    n = len(b)
    
    alpha = [0.0] * n
    beta = [0.0] * n 
    
    alpha[0] = -c[0] / b[0]
    beta[0] = d[0] / b[0]
    
    for i in range(1, n):
        denom = a[i] * alpha[i - 1] + b[i]
        if i < n - 1:
            alpha[i] = -c[i] / denom
        else:
            alpha[i] = 0.0  
        beta[i] = (d[i] - a[i] * beta[i - 1]) / denom
        
    x = [0.0] * n
    x[n - 1] = beta[n - 1] 
    for i in range(n - 2, -1, -1):
        x[i] = alpha[i] * x[i + 1] + beta[i]
        
    return x

    

def dvaznaka(x):
    for i in range(len(x)):
        x[i] = round(x[i],2)
    return x

# ----------------------------------------------------------------

A = [
    [1.42,  3.17,   0.85,  2.63],
    [2.51,  -1.39, 1.74, -3.26],
    [0.93, 2.88, -1.57, 4.02],
    [-1.64, 0.75, 3.41, -2.18],
]
b = [5.28, -4.15, 6.37, 1.92]

print("   Gauss:", dvaznaka(gauss(A, b)))
print(" Inverse:", dvaznaka(by_inverse(A, b)))

A = [
    [3, 1, -1, 1],
    [1, -4, 1, -1],
    [-1, 1, 4, 1],
    [1, 2, 1, -5],
]
b = [62, 15, -6, 23]

x0 = [14.7, 1, 2, 0.5]

print("  Jacobi:", dvaznaka(jacobi(A, b, x0)))
print("  Seidel:", dvaznaka(seidel(A, b, x0)))

A = [
    [3, 2.2, 0, 0, 0],
    [1, -4, 1, 0, 0],
    [0, 2, -7, 2.5, 0],
    [0, 0, -1.2, 6, 1],
    [0, 0, 0, 2, 3.5],
]
b = [4.8, -1, 0.5, 6.1, 3]

print("  Progon:", dvaznaka(progonka(A,b)))

    

