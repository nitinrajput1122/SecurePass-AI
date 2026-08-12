import customtkinter as ctk
import os

from config import APP_TITLE, WINDOW_SIZE
from ui import SecurePassUI


def main():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.title(APP_TITLE)
    app.geometry(WINDOW_SIZE)
    app.resizable(True, True)

    SecurePassUI(app)

    app.mainloop()


if __name__ == "__main__":
    main()