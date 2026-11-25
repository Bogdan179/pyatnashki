"""Логика игрового поля пятнашек."""

import random


class Board:
    """Поле NxN: список костяшек, 0 — пустая клетка."""

    def __init__(self, size):
        self.size = size
        self.tiles = list(range(1, size * size)) + [0]
        self.empty = size * size - 1

    def shuffle(self):
        """Перемешивает поле до решаемой несобранной раскладки."""
        while True:
            random.shuffle(self.tiles)
            self.empty = self.tiles.index(0)
            if self.is_solvable() and not self.is_solved():
                return

    def is_solvable(self):
        """Проверка решаемости методом подсчёта инверсий."""
        seq = [t for t in self.tiles if t != 0]
        inversions = sum(
            1
            for i in range(len(seq))
            for j in range(i + 1, len(seq))
            if seq[i] > seq[j]
        )
        if self.size % 2 == 1:
            return inversions % 2 == 0
        row_from_bottom = self.size - self.empty // self.size
        return (inversions + row_from_bottom) % 2 == 1

    def is_solved(self):
        """Поле собрано, если костяшки идут по порядку."""
        return self.tiles == list(range(1, self.size * self.size)) + [0]

    def move_tile(self, direction):
        """Сдвигает костяшку в указанную сторону на пустое место.

        Возвращает True, если ход выполнен.
        """
        shifts = {
            "left": (0, 1),
            "right": (0, -1),
            "up": (1, 0),
            "down": (-1, 0),
        }
        dr, dc = shifts[direction]
        row, col = divmod(self.empty, self.size)
        nr, nc = row + dr, col + dc
        if not (0 <= nr < self.size and 0 <= nc < self.size):
            return False
        idx = nr * self.size + nc
        self.tiles[self.empty], self.tiles[idx] = (
            self.tiles[idx],
            self.tiles[self.empty],
        )
        self.empty = idx
        return True

    def move_index(self, idx):
        """Сдвигает костяшку с позиции idx, если она соседняя с пустой.

        Возвращает True, если ход выполнен.
        """
        row, col = divmod(self.empty, self.size)
        tr, tc = divmod(idx, self.size)
        if abs(row - tr) + abs(col - tc) != 1:
            return False
        self.tiles[self.empty], self.tiles[idx] = (
            self.tiles[idx],
            self.tiles[self.empty],
        )
        self.empty = idx
        return True
