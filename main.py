"""Игра «Пятнашки»: точка входа.

Размер поля по умолчанию — 4x4, меняется в меню «Настройки».
"""

from app import run_app

DEFAULT_SIZE = 4


def main():
    run_app(DEFAULT_SIZE)


if __name__ == "__main__":
    main()
