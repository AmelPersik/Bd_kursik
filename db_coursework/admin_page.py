import math
import tkinter as tk
import re
from tkinter import ttk, messagebox, simpledialog

from unicodedata import decimal

class AdminPage:
    def __init__(self, root, user, db_handler):
        self.root = root
        self.user = user
        self.db_handler = db_handler
        self.difficulty_window = None
        self.status_window = None
        self.add_user_window = None
        self.logs_window = None
        self.users_window = None
        self.frame = tk.Frame(root)
        self.frame.pack(fill="both", expand=True)

        tk.Label(self.frame, text="Jewelry Store - Администратор", font=("Arial", 24, "bold")).pack(pady=20)

        # Блок информации
        self.info_frame = tk.LabelFrame(self.frame, text="Информация", padx=10, pady=10)
        self.info_frame.pack(fill="x", padx=10, pady=10)

        tk.Label(self.info_frame, text=f"Логин: {self.user['login']}").pack(anchor="w")
        role = "Администратор"
        tk.Label(self.info_frame, text=f"Роль: {role}").pack(anchor="w")
        self.email_label = tk.Label(self.info_frame, text=f"Почта: {self.user['email']} ")
        self.email_label.pack(anchor="w")

        # Блок меню
        menu_frame = tk.LabelFrame(self.frame, text="Меню", padx=10, pady=10)
        menu_frame.pack(fill="x", padx=10, pady=10)

        tk.Button(menu_frame, text="Изменить почту", command=self.change_email).pack(side="left", padx=5)
        self.change_order_difficulty_button = tk.Button(menu_frame, text="Изменить изменить сложность заказа", command=self.change_order_difficulty, state=tk.DISABLED)
        self.change_order_difficulty_button.pack(side="left", padx=5)
        self.change_order_state_button = tk.Button(menu_frame, text="Изменить статус заказа", command=self.change_order_state, state=tk.DISABLED)
        self.change_order_state_button.pack(side="left", padx=5)
        self.delete_order_button = tk.Button(menu_frame, text="Удалить заказ", command=self.delete_order, state=tk.DISABLED)
        self.delete_order_button.pack(side="left", padx=5)
        self.add_user_button = tk.Button(menu_frame, text="Добавить нового пользователя", command=self.add_user, state=tk.NORMAL)
        self.add_user_button.pack(side="left", padx=5)
        self.view_users_button = tk.Button(menu_frame, text="Просмотреть всех пользователей", command=self.view_users, state=tk.NORMAL)
        self.view_users_button.pack(side="left", padx=5)
        self.view_logs_button = tk.Button(menu_frame, text="Просмотреть логи", command=self.view_logs,state=tk.NORMAL)
        self.view_logs_button.pack(side="left", padx=5)
        self.logout = tk.Button(menu_frame, text="Выйти из аккаунта", command=self.logout,state=tk.NORMAL)
        self.logout.pack(side="left", padx=5)

        # Таблица заказов
        self.table_frame = tk.LabelFrame(self.frame, text="Оформленные заказы", padx=5, pady=5)
        self.table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.table = ttk.Treeview(self.table_frame,
                                   columns=("OrderID", "Type of jewerly", "Metal", "Metal Gram", "Gem", "Gem Carat", "Client", "Master", "Status", "Type", "Difficulty", "Total"),
                                   show="headings")
        self.table.heading("OrderID", text="№ заказа")
        self.table.heading("Type of jewerly", text="Тип украшения")
        self.table.heading("Metal", text="Метал")
        self.table.heading("Metal Gram", text="Грамм метала")
        self.table.heading("Gem", text="Камень")
        self.table.heading("Gem Carat", text="Карат камня")
        self.table.heading("Client", text="Клиент")
        self.table.heading("Master", text="Мастер")
        self.table.heading("Status", text="Статус")
        self.table.heading("Type", text="Тип")
        self.table.heading("Difficulty", text="Сложность")
        self.table.heading("Total", text="Сумма")
        self.table.pack(fill="both", expand=True)

        # Set column widths
        column_width = 100  # Set a default width for all columns
        for col in self.table["columns"]:
            self.table.column(col, width=column_width)

        self.table.pack(fill="both", expand=True)

        # Bind the selection event to enable/disable the refuse button
        self.table.bind("<<TreeviewSelect>>", self.on_select)

        # Populate the table with orders
        self.view_orders()

    def view_orders(self):
        try:
            # Clear the table before loading new orders
            self.table.delete(*self.table.get_children())

            # Fetch orders for the user
            orders = self.db_handler.get_all_orders()

            # Sort orders based on the fourth attribute (index 8)
            sorted_orders = sorted(orders, key=lambda order: order[8])  # Change the index if needed

            # Insert sorted orders into the table
            for order in sorted_orders:
                self.table.insert("", "end", values=order)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить заказы: {e}")

    def on_select(self, event):
        # Get selected item
        selected_item = self.table.selection()
        if selected_item:
            self.change_order_difficulty_button.config(state=tk.NORMAL)
            self.change_order_state_button.config(state=tk.NORMAL)
            self.delete_order_button.config(state=tk.NORMAL)
        else:
            self.change_order_state_button.config(state=tk.DISABLED)
            self.change_order_difficulty_button.config(state=tk.DISABLED)
            self.delete_order_button.config(state=tk.DISABLED)

    def view_logs(self):
        # Create a new window for the shop
        self.logs_window = tk.Toplevel(self.root)
        self.logs_window.title("Логи")
        self.logs_window.geometry("820x1200")

        # Create a Treeview to display products
        columns = ("log_id","user_id", "action", "created_at")  # Adjust based on your product attributes
        product_table = ttk.Treeview(self.logs_window, columns=columns, show="headings")

        # Define headings
        product_table.heading("log_id", text="Id лога")
        product_table.heading("user_id", text="Id юзера, который взаимодействовал")
        product_table.heading("action", text="Действие")
        product_table.heading("created_at", text="Лог создан в")


        # Set column widths
        product_table.column("log_id", width=100)
        product_table.column("user_id", width=120)
        product_table.column("action", width=120)
        product_table.column("created_at", width=120)

        product_table.pack(fill="both", expand=True)

        try:
            logs = self.db_handler.get_all_logs()

            for log in logs:
                product_table.insert("", "end", values=log)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить логи: {e}")


    def view_users(self):
        # Create a new window for the shop
        self.users_window = tk.Toplevel(self.root)
        self.users_window.title("Пользователи")
        self.users_window.geometry("820x1200")

        # Create a Treeview to display products
        columns = ("user_id", "role", "login", "email")  # Adjust based on your product attributes
        product_table = ttk.Treeview(self.users_window, columns=columns, show="headings")

        # Define headings
        product_table.heading("user_id", text="Id пользователя")
        product_table.heading("role", text="Роль пользователя")
        product_table.heading("login", text="Логин пользователя")
        product_table.heading("email", text="Почта пользователя")


        # Set column widths
        product_table.column("user_id", width=100)
        product_table.column("role", width=120)
        product_table.column("login", width=120)
        product_table.column("email", width=120)

        product_table.pack(fill="both", expand=True)

        try:
            users = self.db_handler.get_all_users()

            for user in users:
                product_table.insert("", "end", values=user)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить пользователей: {e}")

    def change_email(self):
        new_email = simpledialog.askstring("Изменить почту", "Введите новый адрес электронной почты:",
                                           initialvalue=self.user['email'])

        if new_email is not None:  # User pressed OK
            if new_email != self.user['email']:  # Check if the new email is different
                if self.is_valid_email(new_email):  # Validate the new email
                    self.user['email'] = new_email  # Update the current email
                    self.db_handler.update_user_email(self.user['user_id'], new_email)
                    messagebox.showinfo("Успех", "Почта успешно изменена.")
                    self.email_label.config(text=f"Почта: {self.user['email']} ")
                else:
                    messagebox.showerror("Ошибка", "Некорректный адрес электронной почты.")
            else:
                messagebox.showinfo("Инфо", "Новый адрес электронной почты не может быть таким же, как старый.")

    def is_valid_email(self, email):
        # Simple regex for validating an email
        regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(regex, email) is not None

    def change_order_difficulty(self):
        # Create a new Toplevel window for the order dialog
        self.difficulty_window = tk.Toplevel(self.root)
        self.difficulty_window.title("Изменить сложность заказа")

        selected_item = self.table.selection()

        # Get the current difficulty of the selected item
        current_difficulty = self.table.item(selected_item, 'values')[10]  # Assuming difficulty is at index 8
        current_status = self.table.item(selected_item, 'values')[9]
        current_order_id = self.table.item(selected_item, 'values')[0]
        if current_status == "Готов к выдаче" or current_status == "Выдан" or current_status == "Отменен":
            messagebox.showwarning("Предупреждение", "Вы не можете изменить сложность заказа с текущим статусом.")
            self.difficulty_window.destroy()
        else:
            difficulties = self.db_handler.get_order_difficulties()

            # Drop-down menu for difficulty type
            tk.Label(self.difficulty_window, text="Выберите новую сложность:").pack(pady=5)
            difficulty_var = tk.StringVar(value=current_difficulty)  # Set the initial value to the current difficulty

            # Set the width of the dropdown (e.g., 50 characters wide)
            difficulty_dropdown = ttk.Combobox(self.difficulty_window, textvariable=difficulty_var, state='readonly',
                                               width=100)
            difficulty_dropdown['values'] = [f"{difficulty[1]} : {difficulty[2]} балла из 3.7" for difficulty in
                                             difficulties]  # Show name and price
            difficulty_dropdown.pack(pady=5)

        def submit_difficulty():
            difficulty = difficulty_var.get()
            difficulty_id = None
            new_difficulty = None
            for diff in difficulties:
                buf = f"{diff[1]} : {diff[2]} балла из 3.7"
                if buf == difficulty:
                    difficulty_id = diff[0]
                    new_difficulty = diff[2]

            self.db_handler.update_order_difficulty(float(current_difficulty), float(new_difficulty), current_order_id, difficulty_id)
            self.difficulty_window.destroy()
            self.view_orders()

        # Add a button to confirm the change
        tk.Button(self.difficulty_window, text="Изменить сложность", command=submit_difficulty).pack(pady=10)

    def change_order_state(self):
        # Create a new Toplevel window for the order dialog
        self.status_window = tk.Toplevel(self.root)
        self.status_window.title("Изменить статус заказа")

        selected_item = self.table.selection()

        # Get the current difficulty of the selected item
        current_status = self.table.item(selected_item, 'values')[8]
        current_order_id = self.table.item(selected_item, 'values')[0]
        statuses = self.db_handler.get_order_statuses()
        # Drop-down menu for difficulty type
        tk.Label(self.status_window, text="Выберите новую сложность:").pack(pady=5)
        status_var = tk.StringVar(value=current_status)  # Set the initial value to the current difficulty
        # Set the width of the dropdown (e.g., 50 characters wide)
        status_dropdown = ttk.Combobox(self.status_window, textvariable=status_var, state='readonly',
                                           width=100)
        status_dropdown['values'] = [f"{status[1]}" for status in
                                         statuses]  # Show name and price
        status_dropdown.pack(pady=5)

        def submit_status():
            status = status_var.get()
            status_id = None
            for stat in statuses:
                if stat[1] == status:
                    status_id = stat[0]

            self.db_handler.update_order_status(current_order_id, status_id)
            self.status_window.destroy()
            self.view_orders()

        # Add a button to confirm the change
        tk.Button(self.status_window, text="Изменить статус", command=submit_status).pack(pady=10)

    def delete_order(self):
        selected_item = self.table.selection()
        current_order_id = self.table.item(selected_item, 'values')[0]
        self.db_handler.delete_order(current_order_id)
        messagebox.showinfo("Информация", "Заказ удален.")
        self.view_orders()

    def add_user(self):
        self.add_user_window = tk.Toplevel(self.root)

        tk.Label(self.add_user_window, text="Добавление юзера", font=("Arial", 24, "bold")).pack(pady=20)

        tk.Label(self.add_user_window, text="Логин").pack(pady=5)
        self.login_entry = tk.Entry(self.add_user_window)  # Изменено на self.add_user_window
        self.login_entry.pack(pady=5)

        tk.Label(self.add_user_window, text="Пароль").pack(pady=5)
        self.password_entry = tk.Entry(self.add_user_window, show="*")  # Изменено на self.add_user_window
        self.password_entry.pack(pady=5)

        tk.Label(self.add_user_window, text="Email").pack(pady=5)
        self.email_entry = tk.Entry(self.add_user_window)  # Изменено на self.add_user_window
        self.email_entry.pack(pady=5)

        role_var = tk.StringVar(value="Пользователь")  # Установлено значение по умолчанию
        self.dropdown = ttk.Combobox(self.add_user_window, textvariable=role_var, state='readonly',
                                     width=100)  # Изменено на self.add_user_window
        self.dropdown['values'] = ["Пользователь", "Мастер", "Админ"]
        self.dropdown.pack(pady=5)

        def register():
            login = self.login_entry.get()
            password = self.password_entry.get()
            email = self.email_entry.get()

            role_name = role_var.get()
            if role_name == 'Пользователь':
                role = 3
            elif role_name == 'Мастер':
                role = 2
            else:
                role = 1

            if not login or not password or not email or not self.is_valid_email(email):
                messagebox.showwarning("Ошибка", "Заполните все поля!")
                return

            if len(password) < 8:  # Example: minimum length of 8 characters
                messagebox.showwarning("Ошибка", "Пароль должен содержать не менее 8 символов!")
                return

            hashed_password = password  # Здесь можно добавить хеширование пароля

            if self.db_handler.register_user(login, hashed_password, email, role):
                messagebox.showinfo("Успех", "Регистрация прошла успешно!")
            else:
                messagebox.showerror("Ошибка", "Не удалось зарегистрироваться!")

        tk.Button(self.add_user_window, text="Добавить пользователя", command=register).pack(pady=10)

    def logout(self):
        from login_page import LoginPage  # Local import
        self.frame.destroy()
        LoginPage(self.root)

