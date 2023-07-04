import matplotlib.pyplot as plt
import datetime


def int_to_str(i):
    '''O(log n)'''
    digits = '0123456789'
    if i == 0:
        return '0'

    res = ''
    while i > 0:
        res = digits[i % 10] + res
        i = i // 10
    return res


def mul_range(min, max, step):
    while min < max:
        yield min
        min *= step


def bisection_search(L, e):
    '''O(n log n)'''
    if L == []:
        return False
    elif len(L) == 1:
        return L[0] == e
    else:
        half = len(L) // 2
        if L[half] > e:
            return bisection_search(L[:half], e)
        else:
            return bisection_search(L[half:], e)


def bisection_search_benchmark():
    times = dict()
    for i in mul_range(10, 1_000, 2):
        start = datetime.datetime.now()
        bisection_search(list(range(1, i)), int(i * 0.16))
        difference = (datetime.datetime.now() - start).microseconds
        times[i] = difference
    return times


def bisection_search_2(L, e):
    '''O(log n)'''
    def bisection_search_helper(L, e, low, high):
        if high == low:
            return L[low] == e
        mid = (low + high) // 2
        if L[mid] == e:
            return True
        elif L[mid] > e:
            if low == mid:
                return False
            else:
                return bisection_search_helper(L, e, low, mid - 1)
        else:
            return bisection_search_helper(L, e, mid + 1, high)
    if len(L) == 0:
        return False
    else:
        return bisection_search_helper(L, e, 0, len(L) - 1)


def bisection_search_2_benchmark():
    times = dict()
    for i in mul_range(10, 1_000, 2):
        start = datetime.datetime.now()
        bisection_search_2(list(range(1, i)), int(i * 0.16))
        difference = (datetime.datetime.now() - start).microseconds
        times[i] = difference
    return times


print("Bisection Search by Copy")
times = bisection_search_benchmark()
print(times)

print("Bisection Search without Copy")
times_2 = bisection_search_2_benchmark()
print(times_2)

# Very strange behaviours because of memory and stuff, I don't know i'm not a nerd
fig, ax = plt.subplots()
ax.plot(times.keys(), times.values())
plt.show()

fig_2, ax_2 = plt.subplots()
ax_2.plot(times_2.keys(), times_2.values())
plt.show()