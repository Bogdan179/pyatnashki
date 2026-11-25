"""Сохранение лучшего времени и настроек в JSON-файлы."""

import json
import os

SAVE_FILE = "best_time.json"
SETTINGS_FILE = "settings.json"
DEFAULT_COLORS = {"bg_color": "white", "tile_color": "#4a90d9"}


def load_colors():
    """Читает сохранённые цвета; при ошибке возвращает умолчания."""
    colors = dict(DEFAULT_COLORS)
    if not os.path.exists(SETTINGS_FILE):
        return colors
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (ValueError, OSError):
        return colors
    if isinstance(data, dict):
        for key in colors:
            if isinstance(data.get(key), str):
                colors[key] = data[key]
    return colors


def save_colors(bg_color, tile_color):
    """Сохраняет выбранные цвета в файл настроек."""
    try:
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump({"bg_color": bg_color, "tile_color": tile_color},
                      f, ensure_ascii=False, indent=2)
    except OSError:
        pass


def load_records():
    """Читает рекорды из файла; при ошибке возвращает пустой словарь."""
    if not os.path.exists(SAVE_FILE):
        return {}
    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (ValueError, OSError):
        return {}
    return data if isinstance(data, dict) else {}


def get_best(size):
    """Возвращает рекорд для заданного размера поля или None."""
    return load_records().get(str(size))


def save_best(size, seconds, moves, initial_board):
    """Сохраняет результат, если он лучше прежнего рекорда.

    Возвращает True, если установлен новый рекорд.
    """
    records = load_records()
    key = str(size)
    old = records.get(key)
    if old is not None and seconds >= old.get("seconds", float("inf")):
        return False
    records[key] = {
        "seconds": round(seconds, 1),
        "moves": moves,
        "initial_board": initial_board,
    }
    try:
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(records, f, ensure_ascii=False, indent=2)
    except OSError:
        return False
    return True
