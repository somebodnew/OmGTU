N = int(input())

Part = []

for i in range(N):
    a = input()
    pofig = []
    
    for j in range(0,16,5):
        pofig.append(a[j:j+5])
        
    Part.append(pofig)
        

Halve = []

for i in range(2*N):
    a = input()
    pofig = []
    
    for j in range(0,11,5):
        pofig.append(a[j:j+5])
        
    Halve.append(pofig)

    
#print(Part)

