def gen_sets(L):
    '''O(2**n)'''
    if len(L) == 0:
        return [[]]
    smaller = gen_sets(L[:-1])
    extra = L[-1:]
    new = []
    for small in smaller:
        new.append(small + extra)
    return smaller + new


print(gen_sets([1, 2, 3, 4]))
