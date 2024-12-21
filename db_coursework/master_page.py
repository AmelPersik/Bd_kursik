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
                              columns=("OrderID", "Type", "Metal", "Gem", "Master", "Status", "Total"),
                              show="headings")
    self.table.heading("OrderID", text="№ заказа")
    self.table.heading("Type", text="Тип украшения")
    self.table.heading("Metal", text="Метал")
    self.table.heading("Gem", text="Камень")
    self.table.heading("Master", text="Мастер")
    self.table.heading("Status", text="Статус")
    self.table.heading("Total", text="Сумма")
    self.table.pack(fill="both", expand=True)

    # Bind the selection event to enable/disable the refuse button
    self.table.bind("<<TreeviewSelect>>", self.on_select)

    # Populate the table with orders
    self.view_orders()

def view_orders(self):
    user_id = self.user['user_id']  # Assuming user dictionary has a 'user_id' key
    try:
        # Clear the table before loading new orders
        self.table.delete(*self.table.get_children())

        # Fetch orders for the user
        orders = self.db_handler.get_orders_by_user_id(user_id)

        # Sort orders based on the fourth attribute (index 3)
        sorted_orders = sorted(orders, key=lambda order: order[5])  # Change the index if needed

        # Insert sorted orders into the table
        for order in sorted_orders:
            self.table.insert("", "end", values=order)
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось загрузить заказы: {e}")