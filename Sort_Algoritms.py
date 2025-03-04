import tkinter as tk
from tkinter import ttk
import time
import random
import pygame
import sys

def quick_sort_visual(arr):
    states = []

    def partition(low, high):
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            if arr[j] < pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                states.append((arr.copy(), [i, j]))
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        states.append((arr.copy(), [i + 1, high]))
        return i + 1

    def quick_sort_recursive(low, high):
        if low < high:
            pi = partition(low, high)
            quick_sort_recursive(low, pi - 1)
            quick_sort_recursive(pi + 1, high)

    quick_sort_recursive(0, len(arr) - 1)
    return states

def merge_sort_visual(arr):
    states = []

    def merge(start, mid, end):
        left = arr[start:mid]
        right = arr[mid:end]
        i = j = 0
        k = start
        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                arr[k] = left[i]
                i += 1
            else:
                arr[k] = right[j]
                j += 1
            k += 1
            states.append((arr.copy(), [k - 1]))
        while i < len(left):
            arr[k] = left[i]
            i += 1
            k += 1
            states.append((arr.copy(), [k - 1]))
        while j < len(right):
            arr[k] = right[j]
            j += 1
            k += 1
            states.append((arr.copy(), [k - 1]))

    def merge_sort(start, end):
        if end - start > 1:
            mid = (start + end) // 2
            merge_sort(start, mid)
            merge_sort(mid, end)
            merge(start, mid, end)

    merge_sort(0, len(arr))
    return states

def heap_sort_visual(arr):
    states = []

    def heapify(n, i):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2
        if left < n and arr[left] > arr[largest]:
            largest = left
        if right < n and arr[right] > arr[largest]:
            largest = right
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            states.append((arr.copy(), [i, largest]))
            heapify(n, largest)

    def heap_sort():
        n = len(arr)
        for i in range(n // 2 - 1, -1, -1):
            heapify(n, i)
        for i in range(n - 1, 0, -1):
            arr[i], arr[0] = arr[0], arr[i]
            states.append((arr.copy(), [i, 0]))
            heapify(i, 0)

    heap_sort()
    return states

def shell_sort_visual(arr):
    states = []
    gap = len(arr) // 2
    while gap > 0:
        for i in range(gap, len(arr)):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                states.append((arr.copy(), [j, j - gap]))
                j -= gap
            arr[j] = temp
            states.append((arr.copy(), [j]))
        gap //= 2
    return states

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

WIDTH, HEIGHT = 800, 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sorting Visualization")

def draw_array(arr, highlighted_indices=[]):
    screen.fill(WHITE)
    BAR_WIDTH = max(1, WIDTH // len(arr))
    for i, value in enumerate(arr):
        x = i * BAR_WIDTH
        height = value * (HEIGHT // max(arr))
        color = RED if i in highlighted_indices else BLUE
        pygame.draw.rect(screen, color, (x, HEIGHT - height, BAR_WIDTH, height))
    pygame.display.flip()

def animate_sorting(states):
    clock = pygame.time.Clock()
    for state in states:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        new_arr, active_indices = state
        draw_array(new_arr, active_indices)
        clock.tick(500)

def start_sorting():
    size = int(size_entry.get())
    min_val = int(min_entry.get())
    max_val = int(max_entry.get())
    sort_algorithm = algo_var.get()
    arr = [random.randint(min_val, max_val) for _ in range(size)]

    sorting_algorithms = {
        "Quick Sort": quick_sort_visual,
        "Merge Sort": merge_sort_visual,
        "Heap Sort": heap_sort_visual,
        "Shell Sort": shell_sort_visual
    }

    if sort_algorithm in sorting_algorithms:
        start_time = time.time()
        states = sorting_algorithms[sort_algorithm](arr.copy())
        execution_time = time.time() - start_time
        print(f"Execution Time of {sort_algorithm}: {execution_time:.8f} seconds")
        animate_sorting(states)

root = tk.Tk()
root.title("Sorting Algorithm Visualization")

tk.Label(root, text="Choose Sorting Algorithm:").pack()
algo_var = tk.StringVar(value="Quick Sort")
algorithms = ["Quick Sort", "Merge Sort", "Heap Sort", "Shell Sort"]
algo_menu = ttk.Combobox(root, textvariable=algo_var, values=algorithms)
algo_menu.pack()

tk.Label(root, text="Array Size:").pack()
size_entry = tk.Entry(root)
size_entry.pack()
size_entry.insert(0, "500")

tk.Label(root, text="Min Value:").pack()
min_entry = tk.Entry(root)
min_entry.pack()
min_entry.insert(0, "1")

tk.Label(root, text="Max Value:").pack()
max_entry = tk.Entry(root)
max_entry.pack()
max_entry.insert(0, "100")

tk.Button(root, text="Start Sorting", command=start_sorting).pack()
root.mainloop()