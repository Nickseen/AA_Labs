import time
import random
import matplotlib.pyplot as plt

# Реализация алгоритмов сортировки
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def heap_sort(arr):
    def heapify(arr, n, i):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2
        if left < n and arr[left] > arr[largest]:
            largest = left
        if right < n and arr[right] > arr[largest]:
            largest = right
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            heapify(arr, n, largest)

    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)
    return arr

def shell_sort(arr):
    gap = len(arr) // 2
    while gap > 0:
        for i in range(gap, len(arr)):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
        gap //= 2
    return arr

# Функция для измерения времени выполнения
def measure_time(sort_func, arr):
    start_time = time.time()
    sort_func(arr.copy())
    return time.time() - start_time

# Основная функция для построения графика
def plot_sorting_times():
    sizes = [10, 50, 100, 500, 1000, 2000, 3000, 4000, 5000, 10000, 15000, 20000]
    algorithms = {
        "Quick Sort": quick_sort,
        "Merge Sort": merge_sort,
        "Heap Sort": heap_sort,
        "Shell Sort": shell_sort
    }

    results = {algo: [] for algo in algorithms}

    for size in sizes:
        arr = [random.randint(1, 1000) for _ in range(size)]
        for algo_name, algo_func in algorithms.items():
            time_taken = measure_time(algo_func, arr)
            results[algo_name].append(time_taken)
            print(f"{algo_name} with {size} elements: {time_taken:.6f} seconds")

    # Построение графика
    plt.figure(figsize=(10, 6))
    for algo_name, times in results.items():
        plt.plot(sizes, times, label=algo_name, marker='o')

    plt.xlabel("Number of Elements")
    plt.ylabel("Time (seconds)")
    plt.title("Sorting Algorithm Performance")
    plt.legend()
    plt.grid(True)
    plt.show()

# Запуск программы
plot_sorting_times()