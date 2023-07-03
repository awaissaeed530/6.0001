import random

MIN = 1
MAX = 1_000_000_000_000_000


def guess(min, max, current, tries=0):
    if current != random_number:
        current = int((min + max) / 2)
        if current > random_number:
            max = current
            tries = guess(min, max, current, tries + 1)
        elif current < random_number:
            min = current
            tries = guess(min, max, current, tries + 1)
        return tries


num_tries = list()
for i in range(1, 100001):
    random_number = random.randint(MIN, MAX)
    print(f"Iteration {i}: trying to guess {random_number}")

    tries = guess(MIN, MAX, (MIN / MAX) / 2)
    print(f"Guessed in {tries} tries")
    num_tries.append(tries)

print("")
print(f"Average tries: {sum(num_tries)/len(num_tries)}")
print(f"Min: {min(num_tries)}, Max: {max(num_tries)}")