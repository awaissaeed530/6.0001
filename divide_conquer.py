import random
import datetime
import sys

sys.setrecursionlimit(1_000_000_0)


def guess(min, max, current, goal, tries=0):
    if current != goal:
        current = int((min + max) / 2)
        if current > goal:
            max = current
            tries = guess(min, max, current, goal, tries + 1)
        elif current < goal:
            min = current
            tries = guess(min, max, current, goal, tries + 1)
        return tries


def benchmark(min_guess, max_guess, itertations):
    print(f"Running with min: {min_guess}, max: {max_guess}")
    num_tries = list()
    times = list()
    for i in range(1, itertations):
        random_number = random.randint(min_guess, max_guess)
        print(f"Iteration {i}: trying to guess {random_number}")

        start = datetime.datetime.now()
        tries = guess(min_guess, max_guess,
                      (min_guess / max_guess) / 2, random_number)
        end = datetime.datetime.now()
        duration = (end - start).microseconds
        print(f"Guessed in {tries} tries in {duration} ms")
        num_tries.append(tries)
        times.append(duration)

    print("")
    print(f"Average tries: {sum(num_tries)/len(num_tries)}")
    print(f"Min: {min(num_tries)}, Max: {max(num_tries)}")
    print("")
    print(f"Average duration: {sum(times)/len(times)}")
    print(f"Min: {min(times)}, Max: {max(times)}")
    return max(times)


max_times = dict()
for i in range(1, 10000, 1000):
    max_time = benchmark(1, i, 100)
    max_times[i] = max_time

print(max_times)
