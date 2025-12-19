# -*- coding: cp1251 -*-

import config
class BaseAlgorithm:
    def __init__(self, array_data):
        self.array = list(array_data)
        self.steps = []
        self.name = "Базовый Алгоритм"
        self.complexity = "O(N)"
        self.generate_steps()

    def generate_steps(self):
        raise NotImplementedError("Метод generate_steps должен быть переопределен.")

    def add_step(self, array, highlights):
        self.steps.append((list(array), list(highlights)))

    def get_step(self, index):
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
                self.add_step(arr, [(j, config.COLOR_COMPARE), (j + 1, config.COLOR_COMPARE)])

                if arr[j] > arr[j + 1]:
                    # step -> exchange
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    swapped = True
                    self.add_step(arr, [(j, config.COLOR_SWAP), (j + 1, config.COLOR_SWAP)])

                # adds the element that has taken its place
                if j == n - i - 2:
                    self.add_step(arr, [(n - i - 1, config.COLOR_DONE)])

            if not swapped:
                # rest of array is sorted if no swap
                for k in range(n - i - 1):
                    self.add_step(arr, [(k, config.COLOR_DONE)])
                break

        # final effect
        self.add_step(arr, [(k, config.COLOR_DONE) for k in range(n)])


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


            self.add_step(arr,
                          [(i, config.COLOR_PIVOT)] + [(k, config.COLOR_DONE) for k in range(i)])

            while j >= 0 and key < arr[j]:

                self.add_step(arr,
                              [(i, config.COLOR_PIVOT),
                               (j, config.COLOR_COMPARE)] + [(k, config.COLOR_DONE) for k in range(i - 1)])


                arr[j + 1] = arr[j]


                self.add_step(arr,
                              [(j + 1, config.COLOR_SWAP),
                               (j, config.COLOR_COMPARE)] + [(k, config.COLOR_DONE) for k in range(i - 1)])

                j -= 1


            arr[j + 1] = key


            self.add_step(arr, [(j + 1, config.COLOR_DONE)] + [(k, config.COLOR_DONE) for k in range(i)])


        self.add_step(arr, [(k, config.COLOR_DONE) for k in range(n)])



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


        self.add_step(arr, [(k, config.COLOR_DONE) for k in range(n)])

    def _partition(self, arr, low, high):

        pivot = arr[high]
        i = low - 1


        highlights = [(high, config.COLOR_PIVOT)] + [(k, config.COLOR_SUBARRAY) for k in range(low, high)]
        self.add_step(arr, highlights)

        for j in range(low, high):

            self.add_step(arr,
                          [(high, config.COLOR_PIVOT),
                           (j, config.COLOR_COMPARE)] + [(k, config.COLOR_SUBARRAY) for k in range(low, high)])

            if arr[j] <= pivot:
                i = i + 1

                arr[i], arr[j] = arr[j], arr[i]

                self.add_step(arr,
                              [(high, config.COLOR_PIVOT), (i, config.COLOR_SWAP),
                               (j, config.COLOR_SWAP)] + [(k, config.COLOR_SUBARRAY) for k in
                                                                                         range(low, high)])


        arr[i + 1], arr[high] = arr[high], arr[i + 1]


        self.add_step(arr,
                      [(i + 1, config.COLOR_DONE)] + [(k, config.COLOR_SUBARRAY) for k in range(low, high + 1) if k != i + 1])

        return i + 1

    def _quick_sort_recursive(self, arr, low, high):
        if low < high:
            pi = self._partition(arr, low, high)


            self._quick_sort_recursive(arr, low, pi - 1)
            self._quick_sort_recursive(arr, pi + 1, high)