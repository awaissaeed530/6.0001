def bubble_sort_recur(L):
    '''O(n**c) maybe or O(n**2), got to figure it out'''
    count = 0
    for i in range(len(L) - 1):
        if L[i] > L[i + 1]:
            count += 1
            L[i], L[i+1] = L[i+1], L[i]
    if (count != 0):
        return bubble_sort_recur(L)
    else:
        return L


def bubble_sort_loop(L):
    '''O(n**2)'''
    swap = False
    while not swap:
        swap = True
        for i in range(1, len(L)):
            if L[i - 1] > L[i]:
                swap = False
                L[i], L[i-1] = L[i-1], L[i]
    return L


def selection_sort_recur(L):
    smaller = min(L)
    index = L.index(smaller)
    L[0], L[index] = L[index], L[0]
    if (index == len(L) - 1):
        return selection_sort_recur(L)
    else:
        return L


def selection_sort_loop(L):
    '''O(n**2)'''
    suffixSt = 0
    while suffixSt != len(L):
        for i in range(suffixSt, len(L)):
            if L[i] < L[suffixSt]:
                L[suffixSt], L[i] = L[i], L[suffixSt]
        suffixSt += 1
    return L


def merge(left, right):
    result = []
    i, j = 0, 0

    while i < len(left) and j < len(right):
        if (left[i]) < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right(j))
            j += 1
    while i < len(left):
        result.append(left[i])
        i += 1
    while j < len(right):
        result.append(right[j])
        j += 1
    return result


def merge_sort(L):
    '''O(n log n)'''
    if len(L) < 2:
        return L[:]
    else:
        middle = len(L) // 2
        left = merge_sort(L[:middle])
        right = merge_sort(L[middle:])
        return merge(left, right)


test_list = [1, 5, 10, 7, 4, 8, 3, 2, 17, 11, 19, 13, 6, 9]
print(bubble_sort_recur(test_list))
print(bubble_sort_loop(test_list))
print(selection_sort_recur(test_list))
print(selection_sort_loop(test_list))
print(merge_sort(test_list))
