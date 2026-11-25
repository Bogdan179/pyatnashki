"""Игра «Пятнашки»: точка входа.

Размер поля запрашивается в консоли до запуска
графического интерфейса.
"""

from app import run_app

MIN_SIZE = 2
MAX_SIZE = 10


def ask_size():
    """Запрашивает размер поля в консоли до корректного ввода."""
    while True:
        raw = input(f"Введите размер поля ({MIN_SIZE}-{MAX_SIZE}): ").strip()
        try:
            size = int(raw)
        except ValueError:
            print("Ошибка: нужно ввести целое число.")
            continue
        if not MIN_SIZE <= size <= MAX_SIZE:
            print(f"Ошибка: число должно быть от {MIN_SIZE} до {MAX_SIZE}.")
            continue
        return size


def main():
    size = ask_size()
    run_app(size)


if __name__ == "__main__":
    main()
