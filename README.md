# file-manager-cli

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

реализовано
    copy — копирование файлов с проверками
    delete — удаление файлов и папок (рекурсивно)
    count — рекурсивный подсчёт файлов
    search — поиск по регулярным выражениям
    add-date — добавление даты создания в имя файла (с флагом --recursive)
    analyse — анализ размеров с форматированием вывода
Тесты
    Полное покрытие unittest для всех команд
    Изолированные тесты через tempfile
    Запуск: python -m unittest discover tests/ -v
Структура
    cli.py — точка входа (argparse, subcommands)
    filesystem/ — бизнес-логика (модульная архитектура)
    tests/ — юнит-тесты
    README.md, .gitignore, requirements.txt — оформлены
Требования ТЗ
    Запуск без падений на корректных данных
    Help-сообщения для всех команд
    Базовое логирование в stdout/stderr
    Ввод только через аргументы CLI (без input())
    Чистая Git-история: main → dev → feature-ветки

