import time
import matplotlib
matplotlib.use('TkAgg')  # Добавляем для использования TkAgg
import matplotlib.pyplot as plt

def fib_iterative(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

# Измерение времени для итеративного метода
large_scope = [501, 631, 794, 1000, 1259, 1585, 1995, 2512, 3162, 3981, 5012, 6310, 7943, 10000, 12589, 15849, 17869]
times = []

for n in large_scope:
    start = time.perf_counter()
    fib_iterative(n)
    end = time.perf_counter()
    times.append(end - start)
    print(f"fib_iterative({n}), Time = {end - start:.6f} seconds")

plt.plot(large_scope, times, marker='o', linestyle='-', color='orange', label="Iterative")
plt.xlabel("n")
plt.ylabel("Time (s)")
plt.title("Fibonacci Iterative Method Performance")
plt.legend()
plt.show()
