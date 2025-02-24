import time
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
def fib_recursive(n):
    if n <= 1:
        return n
    return fib_recursive(n - 1) + fib_recursive(n - 2)

# Измерение времени выполнения
small_scope = [5, 7, 10, 12, 15, 17, 20, 22, 25, 27, 30, 32, 35, 37, 40]
times = []

for n in small_scope:
    start = time.perf_counter()
    result = fib_recursive(n)
    end = time.perf_counter()
    elapsed_time = end - start
    times.append(elapsed_time)
    print(f"fib_recursive({n}) = {result}, Time = {elapsed_time:.6f} seconds")

# Построение графика
plt.plot(small_scope, times, marker='o', linestyle='-', color='r', label="Recursive")
plt.xlabel("n")
plt.ylabel("Time (s)")
plt.title("Fibonacci Recursive Method Performance")
plt.legend()
plt.show()
