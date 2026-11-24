# To-Do

Tkinter-приложение с SQLite: добавление, выполнение, удаление и очистка задач. Локальная БД todo.db создаётся рядом с todo.py. В проверке использована отдельная временная БД, пользовательские задачи не изменялись.

Требуется Python с Tkinter для GUI-проектов.

```bash
python todo.py
```

Проверка:

```bash
python -m pip install -r requirements-dev.txt
python -m pytest
```

GUI-тесты создают настоящие виджеты в скрытых окнах.
