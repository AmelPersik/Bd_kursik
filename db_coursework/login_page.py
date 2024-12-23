import tkinter as tk
from tkinter import messagebox
from db_handler import DatabaseHandler
from user_page import UserPage

from hashlib import sha256

class LoginPage:
    def __init__(self, root):
        self.root = root
        self.db = DatabaseHandler()

        self.frame = tk.Frame(root)
        self.frame.pack(fill="both", expand=True)

        tk.Label(self.frame, text="Jewelry Store", font=("Arial", 24, "bold")).pack(pady=20)

        tk.Label(self.frame, text="Логин").pack(pady=5)
        self.login_entry = tk.Entry(self.frame)
        self.login_entry.pack(pady=5)

        tk.Label(self.frame, text="Пароль").pack(pady=5)
        self.password_entry = tk.Entry(self.frame, show="*")
        self.password_entry.pack(pady=5)

        tk.Button(self.frame, text="Войти", command=self.login).pack(pady=10)
        tk.Button(self.frame, text="Зарегистрироваться", command=self.show_register_page).pack()

    def login(self):
        login = self.login_entry.get()
        password = self.password_entry.get()

        if not login or not password:
            messagebox.showwarning("Ошибка", "Заполните все поля!")
            return

        user = self.db.authenticate_user(login, password)

        if user:
            self.frame.destroy()
            if user["role_id"] == 1:  # Admin
                AdminPage(self.root, user)
            elif user["role_id"] == 2:  # Master
                MasterPage(self.root, user)
            elif user["role_id"] == 3:  # User
                UserPage(self.root, user, self.db)
        else:
            messagebox.showerror("Ошибка", "Неверный логин или пароль!")

    def show_register_page(self):
        self.frame.destroy()
        RegisterPage(self.root)


class RegisterPage:
    def __init__(self, root):
        self.root = root
        self.db = DatabaseHandler()

        self.frame = tk.Frame(root)
        self.frame.pack(fill="both", expand=True)

        tk.Label(self.frame, text="Регистрация", font=("Arial", 24, "bold")).pack(pady=20)

        tk.Label(self.frame, text="Логин").pack(pady=5)
        self.login_entry = tk.Entry(self.frame)
        self.login_entry.pack(pady=5)

        tk.Label(self.frame, text="Пароль").pack(pady=5)
        self.password_entry = tk.Entry(self.frame, show="*")
        self.password_entry.pack(pady=5)

        tk.Label(self.frame, text="Повторите пароль").pack(pady=5)
        self.confirm_password_entry = tk.Entry(self.frame, show="*")
        self.confirm_password_entry.pack(pady=5)

        tk.Label(self.frame, text="Email").pack(pady=5)
        self.email_entry = tk.Entry(self.frame)
        self.email_entry.pack(pady=5)

        tk.Button(self.frame, text="Зарегистрироваться", command=self.register).pack(pady=10)
        tk.Button(self.frame, text="Назад", command=self.show_login_page).pack()

    def register(self):
        login = self.login_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        email = self.email_entry.get()

        if not login or not password or not confirm_password or not email:
            messagebox.showwarning("Ошибка", "Заполните все поля!")
            return

        if password != confirm_password:
            messagebox.showwarning("Ошибка", "Пароли не совпадают!")
            return

        hashed_password = sha256(password.encode()).hexdigest()

        if self.db.register_user(login, hashed_password, email):
            messagebox.showinfo("Успех", "Регистрация прошла успешно!")
            self.show_login_page()
        else:
            messagebox.showerror("Ошибка", "Не удалось зарегистрироваться!")

    def show_login_page(self):
        self.frame.destroy()
        LoginPage(self.root)