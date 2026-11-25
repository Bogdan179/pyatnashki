"""Сохранение лучшего времени в JSON-файл."""

import json
import os

SAVE_FILE = "best_time.json"


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
