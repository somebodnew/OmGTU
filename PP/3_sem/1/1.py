import numpy as np
from random import randint

def printt(Q):
    print('\n'.join(' '.join(str(int(x)).lstrip('0') or '0' for x in row)for row in Q))

my_array = np.arange(10,70,2)
print('Задание 1')
print(my_array,sep = '\n') # 1
print()

A = my_array.reshape(6,5).T
print('Задание 2')
printt(A) # 2
print()

A *= 2.5
A[0] -= 5
print('Задание 3')
printt(A) # 3
print()

B = np.random.uniform(0,10,(6,3))
print('Задание 4')
printt(B) # 4
print()

razmA=0
aver = np.sum(A,1)
bver = np.sum(B,0)
print('Задание 5')
print(len(aver))
print(len(bver)) # 5
print()

C = np.dot(A,B)
print('Задание 6')
printt(C) # 6
print()

A = np.delete(A,2,axis = 1)
B = np.hstack((B,np.random.uniform(10,20,(6,3))))
print('Задание 7')
printt(A) # 7
printt(B)
print()


print('Задание 8')
detA = np.linalg.det(A)
detB = np.linalg.det(B)
print(detA,detB)
print(printt(np.linalg.inv(A)) if detA!=0 else 'det is equal zero')
print(printt(np.linalg.inv(B)) if detB!=0 else 'det is equal zero')
print() # 8

bA = np.linalg.matrix_power(A, 6)
bB = np.linalg.matrix_power(B, 14)
print('Задание 9')
print(A)
printt(bA) # 9
printt(bB) 
print() 

_A = np.array([
[4,-3.4,1,1.8],
[-2,8,0,-9],
[2,-2.5,-7,4],
[1,-1,5,1]
])
_b = np.array([6,-4.8,10,3])

_x = np.linalg.solve(_A,_b)

print('Задание 10')
print(_x) # 10
