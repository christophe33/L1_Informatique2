## Exo 2 ##
def insert (t, n, e, k): # O(n - k)
    
    if k > n:
        k = n
    for i in range(n,k,-1):
        t[i] = t[i-1]
    t[k] = e
    return n+1
    
## Exo 3 ##
def delete(t, n, k):
    
    for i in range(k+1, n):
        t[i-1] = t[i]
    return n-1
    
## Exo 4 ##
def amplitude(t, n):
    
    maxi = t[0]
    mini = t[0]
    for i in range(1, n):
        if t[i] > maxi:
            maxi = t[i]
        elif t[i] < mini:
            mini = t[i]
    return maxi - mini
    
## Exo 5 ##
def max2(t,n):
    
    max1 = t[0]
    max2 = t[1]
    for i in range(1, n):
        if t[i] >= max1:
            max2 = max1
            max1 = t[i]
        elif t[i] > max2:
            max2 = t[i]
    return max2
    
## Exo 6 ##
def deleteFirstInstance(t, n, x):
    for i in range(n):
        if t[i]==x:
            return delete(t, n, i)
    return n

## Exo 7 ##
def unduplicated(t, n):
    for i in range(n-1):
        for j in range(i+1, n):
            if t[i] == t[j]:
                return False
    return True
    

## Exo 9 ##
def deleteInstancesV1(t,n,x): # O(n)
    j=0 # j=indice d'écriture
    for i in range(n): # i=indice de lecture
        if t[i] != x:
            t[j] = t[i]
            j += 1
    return j

def deleteInstancesV2(t,n,x): # O(n)
    suppr=0 #nombre d´eléments supprimés
    for i in range(n):
        if t[i] != x:
            t[i-suppr] = t[i]
        else:
            suppr +=1
    return n-suppr
    

