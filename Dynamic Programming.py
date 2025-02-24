import time
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
def fib_dynamic(n):
    if n <= 1:
        return n
    fib = [0, 1]
    for i in range(2, n + 1):
        fib.append(fib[i - 1] + fib[i - 2])
    return fib[n]

large_scope = [501, 631, 794, 1000, 1259, 1585, 1995, 2512, 3162, 3981, 5012, 6310, 7943, 10000, 12589, 15849]
times = []

for n in large_scope:
    start = time.perf_counter()
    result = fib_dynamic(n)
    end = time.perf_counter()
    elapsed_time = end - start
    times.append(elapsed_time)
    print(f"fib_dynamic({n}) , Time = {elapsed_time:.6f} seconds")

plt.plot(large_scope, times, marker='o', linestyle='-', color='g', label="Dynamic Programming")
plt.xlabel("n")
plt.ylabel("Time (s)")
plt.title("Fibonacci Dynamic Programming Performance")
plt.legend()
plt.show()
