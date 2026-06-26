# CLI File System Manager

Консольный менеджер файловой системы на Python. Позволяет выполнять базовые операции с файлами и папками через удобный CLI-интерфейс.

##  Установка и запуск

# 1. Клонируйте репозиторий
git clone <URL-РЕПО>
cd cli-file-manager

# 2. Установите зависимости (если есть)
pip install -r requirements.txt

# 3. Запустите приложение
python cli.py --help

# 4. Запустите тесты
python -m unittest discover tests/ -v

# Структура проекта
cli-file-manager/
├── cli.py              # Точка входа (argparse, subcommands)
├── filesystem/         # Бизнес-логика (модульная архитектура)
│   ├── __init__.py
│   ├── copy.py
│   ├── delete.py
│   ├── count.py
│   ├── search.py
│   ├── add_date.py
│   └── analyse.py
├── tests/              # Юнит-тесты
│   ├── __init__.py
│   ├── test_cli.py
│   └── test_ops.py
├── requirements.txt    # Зависимости
├── .gitignore          # Исключения для Git
└── README.md           # Документация
