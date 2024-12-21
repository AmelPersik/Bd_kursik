import tkinter as tk
from tkinter import ttk, messagebox
from db import Database


class App:
    def __init__(self, master):
        """Инициализация главного окна приложения."""
        self.master = master
        self.db = Database()

        # Создание вкладок
        self.notebook = ttk.Notebook(master)
        self.notebook.pack(fill="both", expand=True)

        # Вкладки
        self.create_metal_tab()
        self.create_gem_tab()

    def populate_user_table(self, user_id):
        orders = self.db_handler.get_orders_by_user_id(user_id)
        for order in orders:
            self.table.insert("", "end", values=order)

    def create_metal_tab(self):
        """Создание вкладки для работы с таблицей 'Metal'."""
        self.metal_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.metal_frame, text="Металлы")

        # Таблица для отображения данных
        self.metal_table = ttk.Treeview(self.metal_frame, columns=("ID", "Название", "Цена за грамм"), show="headings")
        self.metal_table.heading("ID", text="ID")
        self.metal_table.heading("Название", text="Название")
        self.metal_table.heading("Цена за грамм", text="Цена за грамм")
        self.metal_table.pack(fill="both", expand=True)

        # Кнопка загрузки данных
        self.load_metal_button = ttk.Button(self.metal_frame, text="Загрузить данные", command=self.load_metals)
        self.load_metal_button.pack()

        # Форма для добавления записи
        self.metal_name_label = ttk.Label(self.metal_frame, text="Название:")
        self.metal_name_label.pack()
        self.metal_name_entry = ttk.Entry(self.metal_frame)
        self.metal_name_entry.pack()

        self.metal_cost_label = ttk.Label(self.metal_frame, text="Цена за грамм:")
        self.metal_cost_label.pack()
        self.metal_cost_entry = ttk.Entry(self.metal_frame)
        self.metal_cost_entry.pack()

        self.add_metal_button = ttk.Button(self.metal_frame, text="Добавить металл", command=self.add_metal)
        self.add_metal_button.pack()

    def load_metals(self):
        """Загрузка данных из таблицы 'Metal'."""
        query = "SELECT metal_id, name, cost_gramm FROM Metal"
        metals = self.db.fetch_all(query)

        # Очистка таблицы
        for row in self.metal_table.get_children():
            self.metal_table.delete(row)

        # Добавление данных в таблицу
        for metal in metals:
            self.metal_table.insert("", "end", values=(metal["metal_id"], metal["name"], metal["cost_gramm"]))

    def add_metal(self):
        """Добавление нового металла в таблицу 'Metal'."""
        name = self.metal_name_entry.get()
        cost_gramm = self.metal_cost_entry.get()

        if not name or not cost_gramm:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены.")
            return

        try:
            cost_gramm = float(cost_gramm)
            if cost_gramm <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Цена за грамм должна быть положительным числом.")
            return

        query = "INSERT INTO Metal (name, cost_gramm) VALUES (%s, %s)"
        self.db.execute(query, (name, cost_gramm))
        messagebox.showinfo("Успех", "Металл успешно добавлен.")
        self.load_metals()

    def create_gem_tab(self):
        """Создание вкладки для работы с таблицей 'Gem'."""
        self.gem_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.gem_frame, text="Драгоценные камни")

        # Функционал аналогичен вкладке 'Metal'
        # Реализация оставлена для самостоятельного дополнения

    def __del__(self):
        """Закрытие соединения с базой данных при завершении работы приложения."""
        self.db.close()