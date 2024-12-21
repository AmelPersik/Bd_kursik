from tkinter import Tk
from login_page import LoginPage

if __name__ == "__main__":
    root = Tk()
    root.title("Jewelry Store Application")
    root.geometry("1024x768")
    app = LoginPage(root)
    root.mainloop()