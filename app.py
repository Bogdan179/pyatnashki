"""Графический интерфейс игры «Пятнашки» (tkinter)."""

import time
import tkinter as tk
from tkinter import colorchooser, messagebox

from board import Board
from storage import (
    DEFAULT_COLORS, get_best, load_colors, save_best, save_colors,
)

WINDOW_SIZES = [(640, 480), (720, 480), (900, 600), (1100, 700)]
PANEL_WIDTH = 200
MIN_SIZE = 2
MAX_SIZE = 10

CONTROL_SCHEMES = {
    "WASD": {"a": "left", "w": "up", "s": "down", "d": "right",
             "ф": "left", "ц": "up", "ы": "down", "в": "right"},
    "DFJK": {"d": "left", "f": "up", "j": "down", "k": "right",
             "в": "left", "а": "up", "о": "down", "л": "right"},
}
OPPOSITE = {"left": "right", "right": "left", "up": "down", "down": "up"}


class PyatnashkiApp:
    """Главное окно приложения."""

    def __init__(self, root, size):
        self.root = root
        self.size = size
        self.board = Board(size)
        self.scheme = "WASD"
        colors = load_colors()
        self.bg_color = colors["bg_color"]
        self.tile_color = colors["tile_color"]
        self.moves = 0
        self.start_time = None
        self.timer_job = None
        root.title("Пятнашки")
        root.geometry(f"{WINDOW_SIZES[1][0]}x{WINDOW_SIZES[1][1]}")
        root.configure(bg=self.bg_color)
        root.bind("<Key>", self._safe(self.on_key))
        self._build_menu()
        self._build_layout()
        self.new_game()

    def _build_menu(self):
        menu = tk.Menu(self.root)
        game_menu = tk.Menu(menu, tearoff=0)
        game_menu.add_command(label="Новая игра",
                              command=self._safe(self.new_game))
        game_menu.add_separator()
        game_menu.add_command(label="Выход", command=self.root.destroy)
        menu.add_cascade(label="Игра", menu=game_menu)

        settings = tk.Menu(menu, tearoff=0)

        size_menu = tk.Menu(settings, tearoff=0)
        self.size_var = tk.IntVar(value=self.size)
        for n in range(MIN_SIZE, MAX_SIZE + 1):
            size_menu.add_radiobutton(
                label=f"{n}x{n}", variable=self.size_var, value=n,
                command=self._safe(self.change_size))
        settings.add_cascade(label="Размер поля", menu=size_menu)

        window_menu = tk.Menu(settings, tearoff=0)
        self.window_var = tk.StringVar(
            value=f"{WINDOW_SIZES[1][0]}x{WINDOW_SIZES[1][1]}")
        for w, h in WINDOW_SIZES:
            window_menu.add_radiobutton(
                label=f"{w}x{h}", variable=self.window_var,
                value=f"{w}x{h}", command=self._safe(self.change_window))
        settings.add_cascade(label="Размер окна", menu=window_menu)

        scheme_menu = tk.Menu(settings, tearoff=0)
        self.scheme_var = tk.StringVar(value="WASD")
        for name in CONTROL_SCHEMES:
            scheme_menu.add_radiobutton(
                label=name, variable=self.scheme_var, value=name,
                command=self._safe(self.change_scheme))
        settings.add_cascade(label="Управление", menu=scheme_menu)

        self.invert_var = tk.BooleanVar(value=False)
        settings.add_checkbutton(label="Инвертировать управление",
                                 variable=self.invert_var)

        colors_menu = tk.Menu(settings, tearoff=0)
        colors_menu.add_command(label="Цвет фона...",
                                command=self._safe(self.pick_bg_color))
        colors_menu.add_command(label="Цвет плиток...",
                                command=self._safe(self.pick_tile_color))
        colors_menu.add_separator()
        colors_menu.add_command(label="По умолчанию",
                                command=self._safe(self.reset_colors))
        settings.add_cascade(label="Цвета", menu=colors_menu)

        menu.add_cascade(label="Настройки", menu=settings)
        self.root.config(menu=menu)

    def _build_layout(self):
        self.canvas = tk.Canvas(self.root, bg=self.bg_color,
                                highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True,
                         padx=10, pady=10)
        self.canvas.bind("<Configure>",
                         lambda event: self._safe(self.draw_board)())
        self.canvas.bind("<Button-1>", self._safe(self.on_click))
        self.panel = tk.Frame(self.root, bg=self.bg_color,
                              width=PANEL_WIDTH)
        self.panel.pack(side="right", fill="y", padx=10, pady=10)
        self.panel.pack_propagate(False)
        self.size_label = tk.Label(
            self.panel,
            text=f"Поле {self.size}x{self.size}",
            bg=self.bg_color,
            font=("Arial", 12),
        )
        self.size_label.pack(anchor="w")
        self.best_label = tk.Label(self.panel, bg=self.bg_color,
                                   font=("Arial", 11), justify="left",
                                   wraplength=PANEL_WIDTH - 20)
        self.best_label.pack(anchor="w", pady=(10, 0))
        self.timer_label = tk.Label(self.panel, text="Время: 0.0 с",
                                    bg=self.bg_color, font=("Arial", 11))
        self.timer_label.pack(anchor="w")
        self.moves_label = tk.Label(self.panel, text="Ходы: 0",
                                    bg=self.bg_color, font=("Arial", 11))
        self.moves_label.pack(anchor="w")
        self.status = tk.Label(
            self.panel, text="", bg=self.bg_color,
            font=("Arial", 12, "bold"), fg="green",
        )
        self.status.pack(anchor="w", pady=5)

    def _safe(self, func):
        """Обёртка: исключение в callback показывает окно ошибки."""
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as exc:
                messagebox.showerror("Ошибка", f"Произошла ошибка: {exc}")
        return wrapper

    def change_size(self):
        """Меняет размер поля и начинает новую партию."""
        self.size = self.size_var.get()
        self.board = Board(self.size)
        self.size_label.config(text=f"Поле {self.size}x{self.size}")
        self.new_game()

    def change_window(self):
        """Применяет выбранный в меню размер окна."""
        self.root.geometry(self.window_var.get())

    def change_scheme(self):
        """Переключает схему управления (WASD / DFJK)."""
        self.scheme = self.scheme_var.get()

    def pick_bg_color(self):
        """Выбор цвета фона окна."""
        color = colorchooser.askcolor(color=self.bg_color,
                                      title="Цвет фона")[1]
        if color is None:
            return
        self.bg_color = color
        self._apply_bg()
        save_colors(self.bg_color, self.tile_color)

    def pick_tile_color(self):
        """Выбор цвета плиток."""
        color = colorchooser.askcolor(color=self.tile_color,
                                      title="Цвет плиток")[1]
        if color is None:
            return
        self.tile_color = color
        self.draw_board()
        save_colors(self.bg_color, self.tile_color)

    def reset_colors(self):
        """Возвращает цвета фона и плиток к значениям по умолчанию."""
        self.bg_color = DEFAULT_COLORS["bg_color"]
        self.tile_color = DEFAULT_COLORS["tile_color"]
        self._apply_bg()
        self.draw_board()
        save_colors(self.bg_color, self.tile_color)

    def _apply_bg(self):
        """Красит фон окна и всех элементов панели."""
        widgets = (self.root, self.canvas, self.panel, self.size_label,
                   self.best_label, self.timer_label, self.moves_label,
                   self.status)
        for widget in widgets:
            widget.configure(bg=self.bg_color)

    def _text_color(self):
        """Цвет цифр на плитке: чёрный на светлом, белый на тёмном."""
        r, g, b = self.root.winfo_rgb(self.tile_color)
        lum = (0.299 * r + 0.587 * g + 0.114 * b) / 65535
        return "black" if lum > 0.6 else "white"

    def on_key(self, event):
        """Обрабатывает нажатие клавиш управления."""
        key = event.char.lower()
        direction = CONTROL_SCHEMES[self.scheme].get(key)
        if direction is None or self.board.is_solved():
            return
        if self.invert_var.get():
            direction = OPPOSITE[direction]
        if self.board.move_tile(direction):
            self._after_move()

    def on_click(self, event):
        """Обрабатывает клик мышью по костяшке."""
        if self.board.is_solved():
            return
        cell = min(self.canvas.winfo_width(),
                   self.canvas.winfo_height()) / self.size
        col = int(event.x // cell)
        row = int(event.y // cell)
        if not (0 <= row < self.size and 0 <= col < self.size):
            return
        if self.board.move_index(row * self.size + col):
            self._after_move()

    def _after_move(self):
        """Общие действия после хода: таймер, ходы, победа."""
        if self.start_time is None:
            self.start_time = time.monotonic()
            self._update_timer()
        self.moves += 1
        self.moves_label.config(text=f"Ходы: {self.moves}")
        self.draw_board()
        if self.board.is_solved():
            self._on_win()

    def _on_win(self):
        """Фиксирует победу: стоп таймера, рекорд, надпись."""
        elapsed = time.monotonic() - self.start_time
        if self.timer_job is not None:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None
        self.timer_label.config(text=f"Время: {elapsed:.1f} с")
        is_record = save_best(self.size, elapsed, self.moves,
                              self.initial_board)
        self._show_best()
        text = f"Вы победили! Время: {elapsed:.1f} с, ходов: {self.moves}"
        if is_record:
            text += ". Новый рекорд!"
        self.status.config(text="Вы победили!")
        messagebox.showinfo("Победа", text)

    def _show_best(self):
        """Показывает лучшее время для текущего размера поля."""
        best = get_best(self.size)
        if best is None:
            text = "Лучшее время:\n—"
        else:
            text = (f"Лучшее время:\n{best['seconds']:.1f} с "
                    f"({best['moves']} ходов)")
        self.best_label.config(text=text)

    def _update_timer(self):
        """Обновляет таймер каждые 100 мс."""
        if self.start_time is None:
            return
        elapsed = time.monotonic() - self.start_time
        self.timer_label.config(text=f"Время: {elapsed:.1f} с")
        self.timer_job = self.root.after(100, self._update_timer)

    def new_game(self):
        """Начинает новую партию: перемешивание, сброс таймера и ходов."""
        if self.timer_job is not None:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None
        self.board.shuffle()
        self.initial_board = list(self.board.tiles)
        self.moves = 0
        self.start_time = None
        self.moves_label.config(text="Ходы: 0")
        self.timer_label.config(text="Время: 0.0 с")
        self.status.config(text="")
        self._show_best()
        self.draw_board()

    def draw_board(self):
        """Рисует текущее состояние поля на холсте."""
        self.canvas.delete("all")
        self.canvas.update_idletasks()
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        side = min(width, height)
        cell = side / self.size
        for idx, value in enumerate(self.board.tiles):
            if value == 0:
                continue
            row, col = divmod(idx, self.size)
            x0, y0 = col * cell, row * cell
            self.canvas.create_rectangle(
                x0 + 2, y0 + 2, x0 + cell - 2, y0 + cell - 2,
                fill=self.tile_color, outline=self.bg_color,
            )
            self.canvas.create_text(
                x0 + cell / 2, y0 + cell / 2,
                text=str(value), fill=self._text_color(),
                font=("Arial", max(8, int(cell / 3)), "bold"),
            )


def run_app(size):
    root = tk.Tk()
    PyatnashkiApp(root, size)
    root.mainloop()
