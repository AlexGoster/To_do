import importlib.util
from pathlib import Path
import sqlite3
import tkinter as tk

spec = importlib.util.spec_from_file_location("todo_gui", Path(__file__).parents[1] / "todo.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_task_lifecycle_and_persistence(tmp_path, monkeypatch):
    monkeypatch.setattr(module, "DB_FILE", str(tmp_path / "todo.db"))
    monkeypatch.setattr(module.messagebox, "askyesno", lambda *args: True)
    monkeypatch.setattr(module.messagebox, "showwarning", lambda *args: None)
    module.init_db()
    root = tk.Tk()
    root.withdraw()
    try:
        app = module.TodoApp(root)
        app.entry.insert(0, "Test task")
        app.add_task()
        assert app.listbox.size() == 1
        app.listbox.selection_set(0)
        app.mark_done()
        with sqlite3.connect(module.DB_FILE) as db:
            assert db.execute("SELECT done FROM tasks").fetchone() == (1,)
        app.refresh()
        app.listbox.selection_set(0)
        app.delete_task()
        assert app.listbox.size() == 0
        app.entry.insert(0, "Delete only test data")
        app.add_task()
        app.clear_all()
        assert app.listbox.size() == 0
    finally:
        root.destroy()
