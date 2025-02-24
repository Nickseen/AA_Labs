import time
import matplotlib
matplotlib.use('TkAgg')  # Добавляем для использования TkAgg
import matplotlib.pyplot as plt

def fib_tail_recursive(n, a=0, b=1):
    if n == 0:
        return a
    if n == 1:
        return b
    return fib_tail_recursive(n - 1, b, a + b)

# Измерение времени для хвостовой рекурсии
large_scope = [5, 7, 10, 12, 15, 17, 20, 22, 25, 27, 30, 32, 35, 37, 40, 42, 45]
times = []

for n in large_scope:
    start = time.perf_counter()
    fib_tail_recursive(n)
    end = time.perf_counter()
    times.append(end - start)
    print(f"fib_tail_recursive({n}), Time = {end - start:.6f} seconds")

plt.plot(large_scope, times, marker='o', linestyle='-', color='cyan', label="Tail Recursion")
plt.xlabel("n")
plt.ylabel("Time (s)")
plt.title("Fibonacci Tail Recursion Performance")
plt.legend()
plt.show()
