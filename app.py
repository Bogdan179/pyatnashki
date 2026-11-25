"""Графический интерфейс игры «Пятнашки» (tkinter)."""

import tkinter as tk

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480


class PyatnashkiApp:
    """Главное окно приложения."""

    def __init__(self, root, size):
        self.root = root
        self.size = size
        root.title("Пятнашки")
        root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        root.configure(bg="white")
        self._build_menu()
        self._build_layout()

    def _build_menu(self):
        menu = tk.Menu(self.root)
        game_menu = tk.Menu(menu, tearoff=0)
        game_menu.add_command(label="Новая игра", command=self.new_game)
        game_menu.add_separator()
        game_menu.add_command(label="Выход", command=self.root.destroy)
        menu.add_cascade(label="Игра", menu=game_menu)
        self.root.config(menu=menu)

    def _build_layout(self):
        self.board_frame = tk.Frame(self.root, bg="white")
        self.board_frame.pack(side="left", padx=10, pady=10)
        self.panel = tk.Frame(self.root, bg="white")
        self.panel.pack(side="right", anchor="n", padx=10, pady=10)
        tk.Label(
            self.panel,
            text=f"Поле {self.size}x{self.size}",
            bg="white",
            font=("Arial", 12),
        ).pack(anchor="w")

    def new_game(self):
        """Заглушка: генерация поля появится на следующем этапе."""


def run_app(size):
    root = tk.Tk()
    PyatnashkiApp(root, size)
    root.mainloop()
