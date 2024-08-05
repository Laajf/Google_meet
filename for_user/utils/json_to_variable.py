import json
from pathlib import Path


def get_project_root() -> Path:
    """Возвращает корневую директорию проекта."""
    return Path(__file__).resolve().parent.parent


def get_config_value(key, file_name='config.json', default=None):
    """Чтение значения из JSON файла по ключу, используя путь относительно корневой директории проекта."""
    try:
        # Определение корневой директории проекта
        root_dir = get_project_root()

        # Построение полного пути к файлу
        file_path = root_dir / file_name

        # Открытие и чтение файла
        with open(file_path, 'r') as file:
            config = json.load(file)
            return config.get(key, default)
    except FileNotFoundError:

        # Определение корневой директории проекта
        root_dir = get_project_root()

        # Построение полного пути к файлу
        file_path = root_dir / file_name

        print(f"Файл {file_path} не найден.")
        return default
    except json.JSONDecodeError as e:

        # Определение корневой директории проекта
        root_dir = get_project_root()

        # Построение полного пути к файлу
        file_path = root_dir / file_name

        print(f"Ошибка при разборе JSON из файла {file_path}: {e}")
        return default