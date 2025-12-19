
# -*- coding: cp1251 -*-

import tkinter as tk
from tkinter import ttk
import random

import time

import config
import algorithms


class SortVisualizer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Визуализатор Алгоритмов Сортировки")


        self.array_size = 50
        self.array_data = self.generate_array('random')
        self.current_algorithm = None
        self.current_step = 0
        self.is_running = False
        self.animation_delay = 100  # ms
        self.animation_job = None


        self.setup_ui()
        self.draw_array()

    def setup_ui(self):

        control_frame = ttk.Frame(self)
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)


        self.canvas_width = 800
        self.canvas_height = 400
        self.canvas = tk.Canvas(self, width=self.canvas_width, height=self.canvas_height, bg='white')
        self.canvas.pack(side=tk.TOP, padx=10, pady=5)


        ttk.Label(control_frame, text="Алгоритм:").pack(side=tk.LEFT, padx=5)
        self.algorithm_var = tk.StringVar(value="BubbleSort")
        algorithms = ["BubbleSort", "InsertionSort", "QuickSort", "MergeSort (TODO)"]
        self.algo_dropdown = ttk.Combobox(control_frame, textvariable=self.algorithm_var, values=algorithms,
                                          state='readonly')
        self.algo_dropdown.bind("<<ComboboxSelected>>", self.on_algo_changed)
        self.algo_dropdown.pack(side=tk.LEFT, padx=5)


        self.start_btn = ttk.Button(control_frame, text="Start/Resume", command=self.start_animation)
        self.start_btn.pack(side=tk.LEFT, padx=5)

        self.pause_btn = ttk.Button(control_frame, text="Pause", command=self.pause_animation, state=tk.DISABLED)
        self.pause_btn.pack(side=tk.LEFT, padx=5)

        self.step_btn = ttk.Button(control_frame, text="Step >", command=self.step_forward, state=tk.DISABLED)
        self.step_btn.pack(side=tk.LEFT, padx=5)


        ttk.Label(control_frame, text="Скорость:").pack(side=tk.LEFT, padx=15)
        self.speed_scale = ttk.Scale(control_frame, from_=5, to=500, orient=tk.HORIZONTAL, command=self.update_delay)
        self.speed_scale.set(self.animation_delay)
        self.speed_scale.pack(side=tk.LEFT, padx=5)


        ttk.Label(control_frame, text="Размер (N):").pack(side=tk.LEFT, padx=15)
        self.size_scale = ttk.Scale(control_frame, from_=10, to=100, orient=tk.HORIZONTAL,
                                    command=self.update_array_size)  # Ограничил до 100 для QuickSort
        self.size_scale.set(self.array_size)
        self.size_scale.pack(side=tk.LEFT, padx=5)


        self.generate_btn = ttk.Button(control_frame, text="New Random Array",
                                       command=lambda: self.reset(array_type='random'))
        self.generate_btn.pack(side=tk.LEFT, padx=5)

        # 6. Инфо-панель
        self.info_label = ttk.Label(self, text="Готов к работе. N=50. BubbleSort. O(N^2)")
        self.info_label.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)

    def update_delay(self, value):
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
            height_ratio = val / max_val
            bar_height = height_ratio * self.canvas_height * 0.9

            # coords
            x1 = i * bar_width
            y1 = self.canvas_height - bar_height
            x2 = (i + 1) * bar_width - padding
            y2 = self.canvas_height

            # coloring
            color = config.COLOR_NORMAL
            highlight_color = next((c for idx, c in highlights if idx == i), None) if highlights else None

            if highlight_color:
                color = highlight_color

            # draws the rectangle
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='black')

    def on_algo_changed(self, event):
        # Если анимация шла, она остановится внутри prepare_algorithm
        self.prepare_algorithm()
        # Также можно сразу разблокировать кнопку Start, если она была заблокирована
        if not self.is_running:
            self.start_btn.config(state=tk.NORMAL)

    def prepare_algorithm(self):
        # cancels current animation
        if self.animation_job:
            self.after_cancel(self.animation_job)
            self.animation_job = None

        self.current_step = 0
        self.is_running = False

        algo_name = self.algorithm_var.get()

        if algo_name == "BubbleSort":
            self.current_algorithm = algorithms.BubbleSort(self.array_data)
        elif algo_name == "InsertionSort":
            self.current_algorithm = algorithms.InsertionSort(self.array_data)
        elif algo_name == "QuickSort":
            self.current_algorithm = algorithms.QuickSort(self.array_data)
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

        # if running and not last -> plan the next step
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

        # unlocks settings
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
        self.pause_animation()

        self.array_data = self.generate_array(array_type)
        self.prepare_algorithm()


        self.draw_array(self.array_data)

        self.start_btn.config(state=tk.NORMAL)


if __name__ == "__main__":
    app = SortVisualizer()
    app.prepare_algorithm()
    app.mainloop()
