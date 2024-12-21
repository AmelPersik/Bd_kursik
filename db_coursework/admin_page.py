import tkinter as tk
from tkinter import ttk

class AdminPage:
    def __init__(self, root, user):
        self.root = root
        self.user = user

        self.frame = tk.Frame(root)
        self.frame.pack(fill="both", expand=True)

        tk.Label(self.frame, text="Jewelry Store - Пользователь", font=("Arial", 24, "bold")).pack(pady=20)

        # Блок информации
        info_frame = tk.LabelFrame(self.frame, text="Информация", padx=10, pady=10)
        info_frame.pack(fill="x", padx=10, pady=10)

        tk.Label(info_frame, text=f"Логин: {self.user['login']}").pack(anchor="w")
        tk.Label(info_frame, text=f"Роль: Пользователь").pack(anchor="w")
        tk.Label(info_frame, text="ФИО: Иван Иванович").pack(anchor="w")  # Пример ФИО

        # Блок меню
        menu_frame = tk.LabelFrame(self.frame, text="Меню", padx=10, pady=10)
        menu_frame.pack(fill="x", padx=10, pady=10)

        tk.Button(menu_frame, text="Изменить почту", command=self.change_email).pack(side="left", padx=5)
        tk.Button(menu_frame, text="Оформить заказ", command=self.create_order).pack(side="left", padx=5)
        tk.Button(menu_frame, text="Магазин", command=self.open_shop).pack(side="left", padx=5)
        tk.Button(menu_frame, text="Оформленные заказы", command=self.view_orders).pack(side="left", padx=5)

        # Таблица заказов
        self.table_frame = tk.LabelFrame(self.frame, text="Оформленные заказы", padx=5, pady=5)
        self.table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.table = ttk.Treeview(self.table_frame, columns=("OrderID", "ProductID", "Type", "Master", "Status", "Total"),
                                  show="headings")
        self.table.heading("OrderID", text="№ заказа")
        self.table.heading("ProductID", text="№ изделия")
        self.table.heading("Type", text="Тип украшения")
        self.table.heading("Master", text="Мастер")
        self.table.heading("Status", text="Статус")
        self.table.heading("Total", text="Сумма")
        self.table.pack(fill="both", expand=True)

        # Пример заполнения таблицы (данные должны приходить из базы данных)
        self.table.insert("", "end", values=(1, 101, "Кольцо", "Мастер Иван", "В процессе", "5000"))

    def change_email(self):
        tk.messagebox.showinfo("Инфо", "Изменение почты еще не реализовано.")

    def create_order(self):
        tk.messagebox.showinfo("Инфо", "Оформление заказа еще не реализовано.")

    def open_shop(self):
        tk.messagebox.showinfo("Инфо", "Просмотр магазина еще не реализован.")

    def view_orders(self):
        tk.messagebox.showinfo("Инфо", "Список заказов еще не реализован.")