import time
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
def fib_matrix(n):
    def multiply_matrices(A, B):
        return [[A[0][0] * B[0][0] + A[0][1] * B[1][0], A[0][0] * B[0][1] + A[0][1] * B[1][1]],
                [A[1][0] * B[0][0] + A[1][1] * B[1][0], A[1][0] * B[0][1] + A[1][1] * B[1][1]]]

    def matrix_power(F, n):
        result = [[1, 0], [0, 1]]
        base = F
        while n > 0:
            if n % 2 == 1:
                result = multiply_matrices(result, base)
            base = multiply_matrices(base, base)
            n //= 2
        return result

    if n == 0:
        return 0
    F = [[1, 1], [1, 0]]
    result = matrix_power(F, n - 1)
    return result[0][0]

large_scope = [501, 631, 794, 1000, 1259, 1585, 1995, 2512, 3162, 3981, 5012, 6310, 7943, 10000, 12589, 15849]
times = []

for n in large_scope:
    start = time.perf_counter()  # Используем более точный метод
    result = fib_matrix(n)
    end = time.perf_counter()
    elapsed_time = end - start
    times.append(elapsed_time)
    print(f"fib_matrix({n}), Time = {elapsed_time:.6f} seconds")

plt.plot(large_scope, times, marker='o', linestyle='-', color='b', label="Matrix Power")
plt.xlabel("n")
plt.ylabel("Time (s)")
plt.title("Fibonacci Matrix Power Performance")
plt.legend()
plt.show()
