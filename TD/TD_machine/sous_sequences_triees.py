def partition(n, k):
    
    part = k*[1]
    if k < n:
        for i in range(k):
            total = sum(part)
            if i == k - 1:
                p = n-total+1
            else:
                p = rd(1, n-total)
            part[i] = p
    return part
    
def fabriquerSousSequenceTrie(n, p, inf, sup):
    
    T = []
    une_partition = partition(n, p)
    for taille in une_partition:
        T += sorted([rd(inf, sup) for i in range(taille)])
    return T
