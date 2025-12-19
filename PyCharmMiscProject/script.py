# -*- coding: cp1251 -*-

import tkinter as tk
from tkinter import ttk
import random
import time

# COLOR CONSTANTS
COLOR_NORMAL = 'lightblue'
COLOR_COMPARE = 'red'
COLOR_SWAP = 'blue'
COLOR_PIVOT = 'yellow'
COLOR_DONE = 'green'
COLOR_SUBARRAY = 'orange'  # SUBARRAY COLOR CHARASTERISTICS


# ABSTRACT
class BaseAlgorithm:
    """Базовый класс для алгоритмов сортировки, генерирующих шаги."""

    def __init__(self, array_data):
        self.array = list(array_data)
        self.steps = []
        self.name = "Базовый Алгоритм"
        self.complexity = "O(N)"
        self.generate_steps()

    def generate_steps(self):
        """
        Генерирует последовательность состояний (шагов) сортировки.
        Каждый шаг - это кортеж: (текущее состояние массива, [индексы и цвета для подсветки])
        """
        raise NotImplementedError("Метод generate_steps должен быть переопределен.")

    def add_step(self, array, highlights):
        """Сохраняет текущее состояние массива и элементы для подсветки."""
        self.steps.append((list(array), list(highlights)))

    def get_step(self, index):
        """Возвращает состояние на заданном шаге."""
        if 0 <= index < len(self.steps):
            return self.steps[index]
        return None, []


# BUBBLE SORT
class BubbleSort(BaseAlgorithm):
    def __init__(self, array_data):
        self.name = "Сортировка Пузырьком"
        self.complexity = "O(N^2)"
        super().__init__(array_data)

    def generate_steps(self):
        n = len(self.array)
        arr = self.array
        self.add_step(arr, [])  # initial state

        for i in range(n - 1):
            swapped = False
            for j in range(0, n - i - 1):
                # step -> comparison
                self.add_step(arr, [(j, COLOR_COMPARE), (j + 1, COLOR_COMPARE)])

                if arr[j] > arr[j + 1]:
                    # step -> exchange
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    swapped = True
                    self.add_step(arr, [(j, COLOR_SWAP), (j + 1, COLOR_SWAP)])

                # adds the element that has taken its place
                if j == n - i - 2:
                    self.add_step(arr, [(n - i - 1, COLOR_DONE)])

            if not swapped:
                # rest of array is sorted if no swap
                for k in range(n - i - 1):
                    self.add_step(arr, [(k, COLOR_DONE)])
                break

        # final effect
        self.add_step(arr, [(k, COLOR_DONE) for k in range(n)])


#  INSERTTION SORT
class InsertionSort(BaseAlgorithm):
    def __init__(self, array_data):
        self.name = "Сортировка Вставками"
        self.complexity = "O(N^2)"
        super().__init__(array_data)

    def generate_steps(self):
        n = len(self.array)
        arr = self.array
        self.add_step(arr, [])  # Начальное состояние

        for i in range(1, n):
            key = arr[i]
            j = i - 1

            # Подсветка текущего элемента для вставки
            self.add_step(arr, [(i, COLOR_PIVOT)] + [(k, COLOR_DONE) for k in range(i)])

            while j >= 0 and key < arr[j]:
                # Шаг: Сравнение (key с arr[j])
                self.add_step(arr, [(i, COLOR_PIVOT), (j, COLOR_COMPARE)] + [(k, COLOR_DONE) for k in range(i - 1)])

                # Сдвиг
                arr[j + 1] = arr[j]

                # Шаг: Сдвиг
                self.add_step(arr, [(j + 1, COLOR_SWAP), (j, COLOR_COMPARE)] + [(k, COLOR_DONE) for k in range(i - 1)])

                j -= 1

            # Вставка key на правильное место
            arr[j + 1] = key

            # Шаг: Вставка завершена, элемент отсортирован
            self.add_step(arr, [(j + 1, COLOR_DONE)] + [(k, COLOR_DONE) for k in range(i)])

            # Финальный эффект: все зеленые
        self.add_step(arr, [(k, COLOR_DONE) for k in range(n)])


# --- Реализация Быстрой Сортировки ---
class QuickSort(BaseAlgorithm):
    def __init__(self, array_data):
        self.name = "Быстрая Сортировка"
        self.complexity = "O(N log N) (средн.)"
        super().__init__(array_data)

    def generate_steps(self):
        arr = self.array
        n = len(arr)
        self.add_step(arr, [])  # Начальное состояние
        self._quick_sort_recursive(arr, 0, n - 1)

        # Финальный эффект: все зеленые
        self.add_step(arr, [(k, COLOR_DONE) for k in range(n)])

    def _partition(self, arr, low, high):
        """Вспомогательная функция для разделения (Partition)"""
        pivot = arr[high]
        i = low - 1

        # Шаг: Выделение текущего подмассива и опорного элемента
        highlights = [(high, COLOR_PIVOT)] + [(k, COLOR_SUBARRAY) for k in range(low, high)]
        self.add_step(arr, highlights)

        for j in range(low, high):
            # Шаг: Сравнение
            self.add_step(arr,
                          [(high, COLOR_PIVOT), (j, COLOR_COMPARE)] + [(k, COLOR_SUBARRAY) for k in range(low, high)])

            if arr[j] <= pivot:
                i = i + 1
                # Обмен
                arr[i], arr[j] = arr[j], arr[i]
                # Шаг: Обмен
                self.add_step(arr,
                              [(high, COLOR_PIVOT), (i, COLOR_SWAP), (j, COLOR_SWAP)] + [(k, COLOR_SUBARRAY) for k in
                                                                                         range(low, high)])

        # Перемещение опорного элемента на правильное место
        arr[i + 1], arr[high] = arr[high], arr[i + 1]

        # Шаг: Окончательное размещение опорного элемента
        self.add_step(arr, [(i + 1, COLOR_DONE)] + [(k, COLOR_SUBARRAY) for k in range(low, high + 1) if k != i + 1])

        return i + 1

    def _quick_sort_recursive(self, arr, low, high):
        if low < high:
            pi = self._partition(arr, low, high)

            # Рекурсивные вызовы для двух подмассивов
            self._quick_sort_recursive(arr, low, pi - 1)
            self._quick_sort_recursive(arr, pi + 1, high)


# --- Класс Визуализатора / Главное Приложение ---
class SortVisualizer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Визуализатор Алгоритмов Сортировки")

        # --- Параметры ---
        self.array_size = 50
        self.array_data = self.generate_array('random')
        self.current_algorithm = None
        self.current_step = 0
        self.is_running = False
        self.animation_delay = 100  # ms
        self.animation_job = None

        # --- Настройка Интерфейса ---
        self.setup_ui()
        self.draw_array()

    def setup_ui(self):
        # Фрейм для управления (Controls)
        control_frame = ttk.Frame(self)
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        # Фрейм для рисования (Canvas)
        self.canvas_width = 800
        self.canvas_height = 400
        self.canvas = tk.Canvas(self, width=self.canvas_width, height=self.canvas_height, bg='white')
        self.canvas.pack(side=tk.TOP, padx=10, pady=5)

        # --- Элементы управления ---

        # 1. Выбор алгоритма
        ttk.Label(control_frame, text="Алгоритм:").pack(side=tk.LEFT, padx=5)
        self.algorithm_var = tk.StringVar(value="BubbleSort")
        algorithms = ["BubbleSort", "InsertionSort", "QuickSort", "MergeSort (TODO)"]
        self.algo_dropdown = ttk.Combobox(control_frame, textvariable=self.algorithm_var, values=algorithms,
                                          state='readonly')
        self.algo_dropdown.pack(side=tk.LEFT, padx=5)

        # 2. Кнопки управления
        self.start_btn = ttk.Button(control_frame, text="Start/Resume", command=self.start_animation)
        self.start_btn.pack(side=tk.LEFT, padx=5)

        self.pause_btn = ttk.Button(control_frame, text="Pause", command=self.pause_animation, state=tk.DISABLED)
        self.pause_btn.pack(side=tk.LEFT, padx=5)

        self.step_btn = ttk.Button(control_frame, text="Step >", command=self.step_forward, state=tk.DISABLED)
        self.step_btn.pack(side=tk.LEFT, padx=5)

        # 3. Ползунок скорости
        ttk.Label(control_frame, text="Скорость:").pack(side=tk.LEFT, padx=15)
        self.speed_scale = ttk.Scale(control_frame, from_=5, to=500, orient=tk.HORIZONTAL, command=self.update_delay)
        self.speed_scale.set(self.animation_delay)
        self.speed_scale.pack(side=tk.LEFT, padx=5)

        # 4. Ползунок размера массива
        ttk.Label(control_frame, text="Размер (N):").pack(side=tk.LEFT, padx=15)
        self.size_scale = ttk.Scale(control_frame, from_=10, to=100, orient=tk.HORIZONTAL,
                                    command=self.update_array_size)  # Ограничил до 100 для QuickSort
        self.size_scale.set(self.array_size)
        self.size_scale.pack(side=tk.LEFT, padx=5)

        # 5. Генерация массива
        self.generate_btn = ttk.Button(control_frame, text="New Random Array",
                                       command=lambda: self.reset(array_type='random'))
        self.generate_btn.pack(side=tk.LEFT, padx=5)

        # 6. Инфо-панель
        self.info_label = ttk.Label(self, text="Готов к работе. N=50. BubbleSort. O(N^2)")
        self.info_label.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)

    def update_delay(self, value):
        """Обновляет задержку анимации."""
        # the more the faster (scroll thingy)
        self.animation_delay = int(550 - float(value))

    def update_array_size(self, value):
        new_size = int(float(value))
        if new_size != self.array_size:
            self.array_size = new_size
            self.reset(array_type='random')

    def generate_array(self, array_type='random'):
        arr = list(range(1, self.array_size + 1))

        if array_type == 'random':
            random.shuffle(arr)
        elif array_type == 'reversed':
            arr.reverse()

        return arr

    def draw_array(self, current_array=None, highlights=None):
        """Отрисовывает массив на Canvas."""
        self.canvas.delete("all")

        if current_array is None:
            current_array = self.array_data

        if not current_array:
            return

        n = len(current_array)
        max_val = max(current_array) if current_array else 1

        # bar sizes
        bar_width = self.canvas_width / n
        padding = 2  # between bars

        for i, val in enumerate(current_array):
            # normalizes the height in order to achieve a balanced picture
            height_ratio = val / max_val
            bar_height = height_ratio * self.canvas_height * 0.9

            # coords
            x1 = i * bar_width
            y1 = self.canvas_height - bar_height
            x2 = (i + 1) * bar_width - padding
            y2 = self.canvas_height

            # coloring
            color = COLOR_NORMAL
            highlight_color = next((c for idx, c in highlights if idx == i), None) if highlights else None

            if highlight_color:
                color = highlight_color

            # draws the rectangle
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='black')

    def prepare_algorithm(self):

        # cancel current animation
        if self.animation_job:
            self.after_cancel(self.animation_job)
            self.animation_job = None

        self.current_step = 0
        self.is_running = False

        algo_name = self.algorithm_var.get()

        if algo_name == "BubbleSort":
            self.current_algorithm = BubbleSort(self.array_data)
        elif algo_name == "InsertionSort":
            self.current_algorithm = InsertionSort(self.array_data)
        elif algo_name == "QuickSort":
            self.current_algorithm = QuickSort(self.array_data)
        # elif algo_name == "MergeSort":
        #      self.current_algorithm = MergeSort(self.array_data) # TODO
        else:
            self.current_algorithm = None

        if self.current_algorithm:
            # updated info panel
            self.info_label.config(
                text=f"Готов. N={self.array_size}. {self.current_algorithm.name}. Сложность: {self.current_algorithm.complexity}. Шагов: {len(self.current_algorithm.steps) - 1}")
            # draw initial state
            self.draw_array(self.array_data)
            self.step_btn.config(state=tk.NORMAL)
        else:
            self.info_label.config(text="Выберите или реализуйте алгоритм.")
            self.step_btn.config(state=tk.DISABLED)

    def animate_step(self):
        if not self.current_algorithm or self.current_step >= len(self.current_algorithm.steps):
            self.pause_animation()
            return

        current_array, highlights = self.current_algorithm.get_step(self.current_step)
        self.draw_array(current_array, highlights)
        self.current_step += 1

        # if running nor last -> plan the next step
        if self.is_running and self.current_step < len(self.current_algorithm.steps):
            self.animation_job = self.after(self.animation_delay, self.animate_step)
        else:
            self.pause_animation()  # halt when finished

    # CONTROLLING THE ANIMATION

    def start_animation(self):
        if not self.current_algorithm:
            self.prepare_algorithm()
            if not self.current_algorithm:
                return

        if self.current_step >= len(self.current_algorithm.steps):
            self.reset()  # reset when reached the end

        self.is_running = True
        self.start_btn.config(state=tk.DISABLED)
        self.pause_btn.config(state=tk.NORMAL)
        self.step_btn.config(state=tk.DISABLED)

        # block settings while working
        self.algo_dropdown.config(state=tk.DISABLED)
        self.generate_btn.config(state=tk.DISABLED)
        self.size_scale.config(state=tk.DISABLED)

        self.animate_step()

    def pause_animation(self):
        self.is_running = False
        self.start_btn.config(state=tk.NORMAL)
        self.pause_btn.config(state=tk.DISABLED)
        if self.current_algorithm and self.current_step < len(self.current_algorithm.steps):
            self.step_btn.config(state=tk.NORMAL)

        # unlock настроек
        self.algo_dropdown.config(state='readonly')
        self.generate_btn.config(state=tk.NORMAL)
        self.size_scale.config(state=tk.NORMAL)

        if self.animation_job:
            self.after_cancel(self.animation_job)
            self.animation_job = None

    def step_forward(self):
        if self.current_algorithm and not self.is_running:
            if self.current_step < len(self.current_algorithm.steps):
                self.animate_step()
            else:
                # иф конец
                self.step_btn.config(state=tk.DISABLED)

    def reset(self, array_type='random'):
        """Сброс состояния и генерация нового массива."""
        self.pause_animation()  # останавливаем текущий процесс

        self.array_data = self.generate_array(array_type)
        self.prepare_algorithm()

        # перерисовка начального состояния
        self.draw_array(self.array_data)

        self.start_btn.config(state=tk.NORMAL)


if __name__ == "__main__":
    app = SortVisualizer()
    app.prepare_algorithm()
    app.mainloop()
