import time
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
from mpmath import mp

mp.dps = 1000
def fib_binet(n):
    phi = mp.mpf((1 + 5 ** 0.5) / 2)
    psi = mp.mpf((1 - 5 ** 0.5) / 2)
    return (phi**n - psi**n) / mp.mpf(5**0.5)

# Список значений для расчета
large_scope = [501, 631, 794, 1000, 1259, 1585, 1995, 2512, 3162, 3981, 5012, 6310, 7943, 10000, 12589, 15849, 17869]
times = []

# Измеряем время выполнения для каждого числа
for n in large_scope:
    start = time.perf_counter()
    result = fib_binet(n)
    end = time.perf_counter()
    elapsed_time = end - start
    times.append(elapsed_time)
    print(f"fib_binet({n}) , Time = {elapsed_time:.6f} seconds")

# Строим график времени выполнения
plt.plot(large_scope, times, marker='o', linestyle='-', color='purple', label="Binet Formula")
plt.xlabel("n")
plt.ylabel("Time (s)")
plt.title("Fibonacci Binet Formula Performance")
plt.legend()
plt.show()
