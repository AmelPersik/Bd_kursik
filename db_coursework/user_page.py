import math
import tkinter as tk
import re
from tkinter import ttk, messagebox, simpledialog



class UserPage:
    def __init__(self, root, user, db_handler):
        self.root = root
        self.user = user
        self.db_handler = db_handler
        self.shop_window = None
        self.order_window = None
        self.frame = tk.Frame(root)
        self.frame.pack(fill="both", expand=True)

        tk.Label(self.frame, text="Jewelry Store - Пользователь", font=("Arial", 24, "bold")).pack(pady=20)

        # Блок информации
        self.info_frame = tk.LabelFrame(self.frame, text="Информация", padx=10, pady=10)
        self.info_frame.pack(fill="x", padx=10, pady=10)

        tk.Label(self.info_frame, text=f"Логин: {self.user['login']}").pack(anchor="w")
        role = "Пользователь"
        if self.user['role_id'] == 2:
            role = "Мастер"
        elif self.user['role_id'] == 1:
            role = "Администратор"

        tk.Label(self.info_frame, text=f"Роль: {role}").pack(anchor="w")
        self.email_label = tk.Label(self.info_frame, text=f"Почта: {self.user['email']} ")
        self.email_label.pack(anchor="w")

        # Блок меню
        menu_frame = tk.LabelFrame(self.frame, text="Меню", padx=10, pady=10)
        menu_frame.pack(fill="x", padx=10, pady=10)

        tk.Button(menu_frame, text="Изменить почту", command=self.change_email).pack(side="left", padx=5)
        tk.Button(menu_frame, text="Оформить заказ", command=self.create_order).pack(side="left", padx=5)
        tk.Button(menu_frame, text="Магазин", command=self.open_shop).pack(side="left", padx=5)

        # Create the "Отменить заказ" button and set it to be initially disabled
        self.refuse_button = tk.Button(menu_frame, text="Отменить заказ", command=self.refuse_order, state=tk.DISABLED)
        self.refuse_button.pack(side="left", padx=5)

        # Таблица заказов
        self.table_frame = tk.LabelFrame(self.frame, text="Оформленные заказы", padx=5, pady=5)
        self.table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.table = ttk.Treeview(self.table_frame,
                                   columns=("OrderID", "Type", "Master", "Status", "Total"),
                                   show="headings")
        self.table.heading("OrderID", text="№ заказа")
        self.table.heading("Type", text="Тип украшения")
        self.table.heading("Master", text="Мастер")
        self.table.heading("Status", text="Статус")
        self.table.heading("Total", text="Сумма")
        self.table.pack(fill="both", expand=True)

        # Bind the selection event to enable/disable the refuse button
        self.table.bind("<<TreeviewSelect>>", self.on_select)

        # Populate the table with orders
        self.view_orders()

    def open_shop(self):
        # Create a new window for the shop
        self.shop_window = tk.Toplevel(self.root)
        self.shop_window.title("Магазин")
        self.shop_window.geometry("820x820")

        # Create a Treeview to display products
        columns = ("product_id","product_name", "metal", "metal_gramm", "gem", "gem_carat",
                   "total_cost")  # Adjust based on your product attributes
        product_table = ttk.Treeview(self.shop_window, columns=columns, show="headings")

        # Define headings
        product_table.heading("product_id", text="Id продукта")
        product_table.heading("product_name", text="Название изделия")
        product_table.heading("metal", text="Название металла")
        product_table.heading("metal_gramm", text="Цена металла за грамм")
        product_table.heading("gem", text="Название камня")
        product_table.heading("gem_carat", text="Цена камня за карат")
        product_table.heading("total_cost", text="Цена изделия")

        # Set column widths
        product_table.column("product_id", width=100)
        product_table.column("product_name", width=120)
        product_table.column("metal", width=120)
        product_table.column("metal_gramm", width=120)
        product_table.column("gem", width=120)
        product_table.column("gem_carat", width=120)
        product_table.column("total_cost", width=120)

        product_table.pack(fill="both", expand=True)

        # Fetch products from the database
        try:
            products = self.db_handler.get_all_products()  # Предполагается, что у вас есть этот метод в db_handler
            for product in products:
                # Округляем цену вверх и приводим к int
                product = list(product)  # Преобразуем к списку, чтобы изменить значение
                product[6] = int(math.ceil(product[6]))  # Округляем вверх и приводим к int
                product = tuple(product)  # Преобразуем обратно в кортеж, если это необходимо

                product_table.insert("", "end", values=product)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить продукты: {e}")

        # Bind double-click event
        product_table.bind("<Double-1>", lambda event: self.on_product_double_click(event, product_table))

    def on_product_double_click(self, event, product_table):
        # Get selected item

        selected_item = product_table.selection()
        if selected_item:
            product_details = product_table.item(selected_item, 'values')

            # Create a dialog for order confirmation
            response = messagebox.askquestion("Оформить заказ", f"Вы хотите оформить заказ на {product_details[1]}?",
                                              icon='warning')

            if response == 'yes':
                # Create an order for the selected product
                self.db_handler.create_order(product_details[0], self.user["user_id"], 1)
                self.view_orders()
                # Close the shop window
                self.shop_window.destroy()  # Close the window after processing
            else:
                # If the user selects "No", bring the shop window to the front
                self.shop_window.lift()


    def view_orders(self):
        user_id = self.user['user_id']  # Assuming user dictionary has a 'user_id' key
        try:
            # Clear the table before loading new orders
            self.table.delete(*self.table.get_children())

            # Fetch orders for the user
            orders = self.db_handler.get_orders_by_user_id(user_id)

            # Sort orders based on the fourth attribute (index 3)
            sorted_orders = sorted(orders, key=lambda order: order[3])  # Change the index if needed

            # Insert sorted orders into the table
            for order in sorted_orders:
                self.table.insert("", "end", values=order)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить заказы: {e}")

    def on_select(self, event):
        # Get selected item
        selected_item = self.table.selection()
        if selected_item:
            self.refuse_button.config(state=tk.NORMAL)  # Enable the button if an item is selected
        else:
            self.refuse_button.config(state=tk.DISABLED)  # Disable the button if no item is selected

    def refuse_order(self):
        # Get the selected order ID
        selected_item = self.table.selection()
        if selected_item:
            order_id = self.table.item(selected_item, 'values')[0]  # Assuming OrderID is the first column
            order_status = self.table.item(selected_item, 'values')[3]  # Assuming Status is the fifth column

            # Check if the order status is "Оформлен" (or whatever the status is for cancellable orders)
            if order_status == "Оформлен":  # Replace "Оформлен" with the actual status name
                # Call the method to change the order status in the database
                try:
                    self.db_handler.update_order_status(order_id, 4)  # Implement this method in your DatabaseHandler
                    messagebox.showinfo("Успех", f"Заказ №{order_id} был успешно отменен.")
                    self.view_orders()  # Refresh the orders table
                except Exception as e:
                    messagebox.showerror("Ошибка", f"Не удалось отменить заказ: {e}")
            else:
                messagebox.showwarning("Предупреждение", "Вы не можете отменить заказ с текущим статусом.")
        else:
            messagebox.showwarning("Предупреждение", "Пожалуйста, выберите заказ для отмены.")

    def change_email(self):
        # Open a dialog to get the new email
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

    def create_order(self):
        # Create a new Toplevel window for the order dialog
        self.order_window = tk.Toplevel(self.root)
        self.order_window.title("Создать заказ")

        # Drop-down menu 1
        tk.Label(self.order_window, text="Выберите тип украшения:").pack(pady=5)
        type_var = tk.StringVar()
        type_dropdown = ttk.Combobox(self.order_window, textvariable=type_var)
        type_dropdown['values'] = ("Тип 1", "Тип 2", "Тип 3")  # Replace with actual types
        type_dropdown.pack(pady=5)

        # Drop-down menu 2
        tk.Label(self.order_window, text="Выберите мастера:").pack(pady=5)
        master_var = tk.StringVar()
        master_dropdown = ttk.Combobox(self.order_window, textvariable=master_var)
        master_dropdown['values'] = ("Мастер 1", "Мастер 2", "Мастер 3")  # Replace with actual masters
        master_dropdown.pack(pady=5)

        # Text field 1
        tk.Label(self.order_window, text="Введите описание:").pack(pady=5)
        description_entry = tk.Entry(self.order_window)
        description_entry.pack(pady=5)

        # Drop-down menu 3
        tk.Label(self.order_window, text="Выберите статус:").pack(pady=5)
        status_var = tk.StringVar()
        status_dropdown = ttk.Combobox(self.order_window, textvariable=status_var)
        status_dropdown['values'] = ("Статус 1", "Статус 2", "Статус 3")  # Replace with actual statuses
        status_dropdown.pack(pady=5)

        # Text field 2
        tk.Label(self.order_window, text="Введите сумму:").pack(pady=5)
        total_entry = tk.Entry(self.order_window)
        total_entry.pack(pady=5)

        # Submit button
        def submit_order():
            order_type = type_var.get()
            master = master_var.get()
            description = description_entry.get()
            status = status_var.get()
            total = total_entry.get()

            # Here you can add logic to handle the order submission
            # For example, validate the inputs and save to the database
            if order_type and master and description and status and total:
                # Assuming you have a method to handle order creation
                self.db_handler.create_order(order_type, master, description, status, total)
                messagebox.showinfo("Успех", "Заказ успешно создан.")
                self.order_window.destroy()  # Close the dialog
            else:
                messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля.")

        tk.Button(self.order_window, text="Создать заказ", command=submit_order).pack(pady=10)
