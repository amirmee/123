"""Небольшой консольный менеджер задач без внешних зависимостей."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable


DATA_FILE = Path("tasks.json")


@dataclass
class Task:
    id: int
    title: str
    completed: bool = False
    created_at: str = ""

    def __post_init__(self) -> None:
        if not self.created_at:
            self.created_at = datetime.now().isoformat(timespec="seconds")


def load_tasks(path: Path = DATA_FILE) -> list[Task]:
    """Загружает задачи из JSON или возвращает пустой список."""
    if not path.exists():
        return []

    try:
        rows = json.loads(path.read_text(encoding="utf-8"))
        return [Task(**row) for row in rows]
    except (json.JSONDecodeError, TypeError, KeyError):
        print("Не удалось прочитать tasks.json. Начинаю с пустого списка.")
        return []


def save_tasks(tasks: Iterable[Task], path: Path = DATA_FILE) -> None:
    """Сохраняет текущий список задач."""
    payload = [asdict(task) for task in tasks]
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def next_id(tasks: list[Task]) -> int:
    return max((task.id for task in tasks), default=0) + 1


def show_tasks(tasks: list[Task]) -> None:
    if not tasks:
        print("Список задач пуст.")
        return

    print("\nВаши задачи:")
    for task in tasks:
        mark = "x" if task.completed else " "
        print(f"  {task.id:>2}. [{mark}] {task.title} ({task.created_at})")


def add_task(tasks: list[Task]) -> None:
    title = input("Текст задачи: ").strip()
    if not title:
        print("Задача не добавлена: текст пустой.")
        return

    tasks.append(Task(id=next_id(tasks), title=title))
    print("Задача добавлена.")


def complete_task(tasks: list[Task]) -> None:
    try:
        task_id = int(input("Номер выполненной задачи: "))
    except ValueError:
        print("Введите число.")
        return

    for task in tasks:
        if task.id == task_id:
            task.completed = True
            print("Задача отмечена выполненной.")
            return
    print("Задача с таким номером не найдена.")


def delete_task(tasks: list[Task]) -> None:
    try:
        task_id = int(input("Номер задачи для удаления: "))
    except ValueError:
        print("Введите число.")
        return

    for index, task in enumerate(tasks):
        if task.id == task_id:
            tasks.pop(index)
            print(f"Задача «{task.title}» удалена.")
            return
    print("Задача с таким номером не найдена.")


def main() -> None:
    tasks = load_tasks()
    actions = {
        "1": lambda: show_tasks(tasks),
        "2": lambda: add_task(tasks),
        "3": lambda: complete_task(tasks),
        "4": lambda: delete_task(tasks),
    }

    while True:
        print("\n1 — показать, 2 — добавить, 3 — выполнить, 4 — удалить, 0 — выход")
        choice = input("Выберите действие: ").strip()

        if choice == "0":
            save_tasks(tasks)
            print("Данные сохранены. До встречи!")
            break

        action = actions.get(choice)
        if action:
            action()
        else:
            print("Неизвестная команда.")


if __name__ == "__main__":
    main()
