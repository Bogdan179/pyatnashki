"""Графический интерфейс игры «Пятнашки» (tkinter)."""

import tkinter as tk

from board import Board

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
TILE_COLOR = "#4a90d9"
TEXT_COLOR = "white"


class PyatnashkiApp:
    """Главное окно приложения."""

    def __init__(self, root, size):
        self.root = root
        self.size = size
        self.board = Board(size)
        root.title("Пятнашки")
        root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        root.configure(bg="white")
        self._build_menu()
        self._build_layout()
        self.new_game()

    def _build_menu(self):
        menu = tk.Menu(self.root)
        game_menu = tk.Menu(menu, tearoff=0)
        game_menu.add_command(label="Новая игра", command=self.new_game)
        game_menu.add_separator()
        game_menu.add_command(label="Выход", command=self.root.destroy)
        menu.add_cascade(label="Игра", menu=game_menu)
        self.root.config(menu=menu)

    def _build_layout(self):
        self.canvas = tk.Canvas(self.root, bg="white", highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True,
                         padx=10, pady=10)
        self.canvas.bind("<Configure>", lambda event: self.draw_board())
        self.panel = tk.Frame(self.root, bg="white")
        self.panel.pack(side="right", anchor="n", padx=10, pady=10)
        tk.Label(
            self.panel,
            text=f"Поле {self.size}x{self.size}",
            bg="white",
            font=("Arial", 12),
        ).pack(anchor="w")

    def new_game(self):
        """Начинает новую партию: перемешивание и отрисовка."""
        self.board.shuffle()
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
                fill=TILE_COLOR, outline="white",
            )
            self.canvas.create_text(
                x0 + cell / 2, y0 + cell / 2,
                text=str(value), fill=TEXT_COLOR,
                font=("Arial", max(8, int(cell / 3)), "bold"),
            )


def run_app(size):
    root = tk.Tk()
    PyatnashkiApp(root, size)
    root.mainloop()
