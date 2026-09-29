#!/usr/bin/env python3
"""To-Do список с GUI"""

import tkinter as tk
from tkinter import messagebox, font
import sqlite3
import os

DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "todo.db")

COLORS = {
    "bg": "#1e1e2e",
    "surface": "#313244",
    "text": "#cdd6f4",
    "accent": "#89b4fa",
    "green": "#a6e3a1",
    "red": "#f38ba8",
    "yellow": "#f9e2af",
    "done_fg": "#6c7086",
}


def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            done INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()


class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do Список")
        self.root.geometry("500x550")
        self.root.configure(bg=COLORS["bg"])
        self.root.resizable(False, False)

        title_font = font.Font(family="Segoe UI", size=16, weight="bold")
        entry_font = font.Font(family="Segoe UI", size=12)
        btn_font = font.Font(family="Segoe UI", size=10, weight="bold")
        list_font = font.Font(family="Consolas", size=11)

        tk.Label(root, text="TO-DO LIST", font=title_font,
                 bg=COLORS["bg"], fg=COLORS["accent"]).pack(pady=(15, 10))

        input_frame = tk.Frame(root, bg=COLORS["bg"])
        input_frame.pack(pady=5)

        self.entry = tk.Entry(input_frame, width=30, font=entry_font,
                              bg=COLORS["surface"], fg=COLORS["text"],
                              insertbackground=COLORS["text"],
                              relief="flat", bd=0)
        self.entry.pack(side="left", padx=(0, 10), ipady=8)
        self.entry.bind("<Return>", lambda e: self.add_task())

        tk.Button(input_frame, text="＋ Добавить", command=self.add_task,
                  font=btn_font, bg=COLORS["accent"], fg=COLORS["bg"],
                  activebackground=COLORS["green"], relief="flat",
                  cursor="hand2", width=12, bd=0).pack(side="left", ipady=4)

        list_frame = tk.Frame(root, bg=COLORS["surface"], bd=0, highlightthickness=0)
        list_frame.pack(padx=15, pady=10, fill="both", expand=True)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")

        self.listbox = tk.Listbox(list_frame, width=50, height=16, font=list_font,
                                  bg=COLORS["surface"], fg=COLORS["text"],
                                  selectbackground=COLORS["accent"],
                                  selectforeground=COLORS["bg"],
                                  relief="flat", bd=0,
                                  yscrollcommand=scrollbar.set,
                                  highlightthickness=0)
        self.listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.listbox.yview)

        btn_frame = tk.Frame(root, bg=COLORS["bg"])
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="✓ Выполнено", command=self.mark_done,
                  font=btn_font, bg=COLORS["green"], fg=COLORS["bg"],
                  activebackground=COLORS["accent"], relief="flat",
                  cursor="hand2", width=14, bd=0).pack(side="left", padx=5, ipady=6)

        tk.Button(btn_frame, text="✕ Удалить", command=self.delete_task,
                  font=btn_font, bg=COLORS["red"], fg=COLORS["bg"],
                  activebackground=COLORS["accent"], relief="flat",
                  cursor="hand2", width=14, bd=0).pack(side="left", padx=5, ipady=6)

        tk.Button(btn_frame, text="Очистить всё", command=self.clear_all,
                  font=btn_font, bg=COLORS["yellow"], fg=COLORS["bg"],
                  activebackground=COLORS["red"], relief="flat",
                  cursor="hand2", width=14, bd=0).pack(side="left", padx=5, ipady=6)

        self.counter_label = tk.Label(root, text="", font=("Segoe UI", 9),
                                      bg=COLORS["bg"], fg=COLORS["done_fg"])
        self.counter_label.pack(pady=(0, 10))

        self.refresh()

    def refresh(self):
        self.listbox.delete(0, tk.END)
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT id, description, done FROM tasks ORDER BY done, id")
        tasks = cursor.fetchall()
        conn.close()

        done_count = 0
        total = len(tasks)

        for task in tasks:
            if task[2]:
                done_count += 1
                self.listbox.insert(tk.END, f"  ✓  {task[1]}")
                self.listbox.itemconfig(tk.END, fg=COLORS["done_fg"])
            else:
                self.listbox.insert(tk.END, f"  ○  {task[1]}")
                self.listbox.itemconfig(tk.END, fg=COLORS["text"])

        self.counter_label.config(text=f"Задач: {total} | Выполнено: {done_count} | Осталось: {total - done_count}")

    def add_task(self):
        text = self.entry.get().strip()
        if not text:
            messagebox.showwarning("Внимание", "Введите текст задачи.")
            return
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (description) VALUES (?)", (text,))
        conn.commit()
        conn.close()
        self.entry.delete(0, tk.END)
        self.refresh()

    def get_selected_id(self):
        sel = self.listbox.curselection()
        if not sel:
            return None
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT id, description, done FROM tasks ORDER BY done, id")
        tasks = cursor.fetchall()
        conn.close()
        idx = sel[0]
        if idx < len(tasks):
            return tasks[idx][0]
        return None

    def delete_task(self):
        task_id = self.get_selected_id()
        if task_id is None:
            messagebox.showwarning("Внимание", "Выберите задачу.")
            return
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        conn.close()
        self.refresh()

    def mark_done(self):
        task_id = self.get_selected_id()
        if task_id is None:
            messagebox.showwarning("Внимание", "Выберите задачу.")
            return
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("UPDATE tasks SET done = 1 WHERE id = ?", (task_id,))
        conn.commit()
        conn.close()
        self.refresh()

    def clear_all(self):
        if messagebox.askyesno("Подтверждение", "Удалить все задачи?"):
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tasks")
            conn.commit()
            conn.close()
            self.refresh()


if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()