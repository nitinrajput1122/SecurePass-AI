import customtkinter as ctk
from tkinter import filedialog, messagebox
from checker import check_password as password_checker
from generator import generate_password


class SecurePassUI:

    def __init__(self, app):
        self.app = app
        self.password_history = []
        self.build_ui()

    def build_ui(self):

        # ===========================
        # Main Container
        # ===========================

        self.container = ctk.CTkFrame(self.app)
        self.container.pack(fill="both", expand=True)

        # ===========================
        # Sidebar
        # ===========================

        self.sidebar = ctk.CTkFrame(
            self.container,
            width=220,
            corner_radius=0
        )
        self.sidebar.pack(side="left", fill="y")

        ctk.CTkLabel(
            self.sidebar,
            text="🔐 SecurePass AI",
            font=("Segoe UI", 22, "bold")
        ).pack(pady=30)

        menu = [
            "🏠 Home",
            "🔍 Password Checker",
            "🔑 Password Generator",
            "📊 Reports",
            "⚙ Settings"
        ]

        for item in menu:
            ctk.CTkButton(
                self.sidebar,
text=item,
command=lambda x=item: self.sidebar_action(x)
            ).pack(
                pady=10,
                padx=20,
                fill="x"
            )

        # ===========================
        # Main Area
        # ===========================

        self.main_area = ctk.CTkScrollableFrame(
            self.container,
            corner_radius=0
        )

        self.main_area.pack(
            side="right",
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # ===========================
        # Heading
        # ===========================

        ctk.CTkLabel(
            self.main_area,
            text="Password Strength Checker",
            font=("Segoe UI", 30, "bold")
        ).pack(pady=(20, 10))

        ctk.CTkLabel(
            self.main_area,
            text="Check how secure your password is.",
            font=("Segoe UI", 16)
        ).pack(pady=(0, 20))

        # ===========================
        # Password Entry
        # ===========================

        self.password_entry = ctk.CTkEntry(
    self.main_area,
    width=560,
    height=50,
    placeholder_text="Enter your password",
    font=("Segoe UI", 16),
    show="*"
)
        self.password_entry.pack(pady=(10, 20))
        self.password_entry.bind(
            "<KeyRelease>",
            lambda event: self.check_password()
        )

        # ===========================
        # Password Requirements
        # ===========================

        self.requirements_label = ctk.CTkLabel(
            self.main_area,
            text=(
                "❌ 8+ Characters\n"
                "❌ Uppercase\n"
                "❌ Lowercase\n"
                "❌ Number\n"
                "❌ Special Character"
            ),
            justify="left",
            font=("Segoe UI", 13)
        )
        self.requirements_label.pack(pady=(0, 20))
        # ===========================
        # Show / Hide Button
        # ===========================

        self.show_button = ctk.CTkButton(
    self.main_area,
    text="👁 Show",
    width=220,
    height=40,
    font=("Segoe UI", 15),
    command=self.toggle_password
)
        self.show_button.pack(pady=10)
                # ===========================
        # Password Length
        # ===========================

        ctk.CTkLabel(
            self.main_area,
            text="Password Length",
            font=("Segoe UI", 16)
        ).pack(pady=(10, 5))

        self.length_slider = ctk.CTkSlider(
            self.main_area,
            from_=8,
            to=32,
            number_of_steps=24,
            command=self.update_length_label
        )

        self.length_slider.set(12)
        self.length_slider.pack(pady=5)

        self.length_label = ctk.CTkLabel(
            self.main_area,
            text="12 Characters",
            font=("Segoe UI", 14)
        )
        self.length_label.pack(pady=(0, 15))

        # ===========================
        # Character Options
        # ===========================

        self.uppercase_var = ctk.BooleanVar(value=True)
        self.lowercase_var = ctk.BooleanVar(value=True)
        self.numbers_var = ctk.BooleanVar(value=True)
        self.symbols_var = ctk.BooleanVar(value=True)

        ctk.CTkCheckBox(
            self.main_area,
            text="Uppercase (A-Z)",
            variable=self.uppercase_var
        ).pack(anchor="center")

        ctk.CTkCheckBox(
            self.main_area,
            text="Lowercase (a-z)",
            variable=self.lowercase_var
        ).pack(anchor="center")

        ctk.CTkCheckBox(
            self.main_area,
            text="Numbers (0-9)",
            variable=self.numbers_var
        ).pack(anchor="center")

        ctk.CTkCheckBox(
            self.main_area,
            text="Symbols (!@#$)",
            variable=self.symbols_var
        ).pack(anchor="center", pady=(0, 15))

        # ===========================
        # Buttons
        # ===========================

        self.generate_button = ctk.CTkButton(
        self.main_area,
        text="🔑 Generate Password",
        command=self.generate_password,
        width=220,
        height=40,
        font=("Segoe UI", 15)
)
        self.generate_button.pack(pady=5)

        self.copy_button = ctk.CTkButton(
        self.main_area,
    text="📋 Copy Password",
    command=self.copy_password,
    width=220,
    height=40,
    font=("Segoe UI", 15)
)
        self.copy_button.pack(pady=5)

        self.check_button = ctk.CTkButton(
       self.main_area,
    text="🔍 Check Password",
    command=self.check_password,
    width=220,
    height=40,
    font=("Segoe UI", 15)
)
        self.check_button.pack(pady=(5, 20))

        # ===========================
        # Result Section
        # ===========================

        self.crack_time_label = ctk.CTkLabel(
            self.main_area,
            text="Estimated Crack Time : -",
            font=("Segoe UI", 15)
        )
        self.crack_time_label.pack(pady=5)

        self.ai_label = ctk.CTkLabel(
        self.main_area,
         text="🤖 AI Suggestions:\n-",
         justify="left",
         font=("Segoe UI", 14)
)
        self.ai_label.pack(pady=10)

        self.result_label = ctk.CTkLabel(
            self.main_area,
            text="Strength : -",
            font=("Segoe UI", 20, "bold")
        )
        self.result_label.pack(pady=10)

        self.progress = ctk.CTkProgressBar(
            self.main_area,
            width=400
        )
        self.progress.pack(pady=10)
        self.progress.set(0)

        # ===========================
        # Password History
        # ===========================

        self.history_label = ctk.CTkLabel(
            self.main_area,
            text="Generated Password History",
            font=("Segoe UI", 18, "bold")
        )
        self.history_label.pack(pady=(25, 10))

        self.history_box = ctk.CTkTextbox(
            self.main_area,
            width=420,
            height=150
        )
        self.history_box.pack()

        self.history_box.configure(state="disabled")

        self.clear_history_button = ctk.CTkButton(
            self.main_area,
            text="🗑 Clear History",
            command=self.clear_history
        )
        self.clear_history_button.pack(pady=10)

        self.export_button = ctk.CTkButton(
            self.main_area,
            text="💾 Export History",
            command=self.export_history
        )
        self.export_button.pack(pady=(0, 20))
            # ===========================
    # Methods
    # ===========================

    def toggle_password(self):
        if self.password_entry.cget("show") == "*":
            self.password_entry.configure(show="")
            self.show_button.configure(text="🙈 Hide")
        else:
            self.password_entry.configure(show="*")
            self.show_button.configure(text="👁 Show")

    def update_length_label(self, value):
        self.length_label.configure(
            text=f"{int(value)} Characters"
        )

    def generate_password(self):
        length = int(self.length_slider.get())

        password = generate_password(
            length=length,
            uppercase=self.uppercase_var.get(),
            lowercase=self.lowercase_var.get(),
            numbers=self.numbers_var.get(),
            symbols=self.symbols_var.get()
        )

        self.password_entry.delete(0, "end")
        self.password_entry.insert(0, password)

        self.password_history.append(password)

        self.history_box.configure(state="normal")
        self.history_box.insert("end", password + "\n")
        self.history_box.configure(state="disabled")

        self.check_password()

    def copy_password(self):
        password = self.password_entry.get()

        if not password:
            return

        self.app.clipboard_clear()
        self.app.clipboard_append(password)

        self.copy_button.configure(text="✅ Copied!")

        self.app.after(
            2000,
            lambda: self.copy_button.configure(
                text="📋 Copy Password"
            )
        )

    def clear_history(self):
        self.password_history.clear()

        self.history_box.configure(state="normal")
        self.history_box.delete("1.0", "end")
        self.history_box.configure(state="disabled")

    def export_history(self):
        if not self.password_history:
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt")],
            title="Save Password History"
        )

        if not file_path:
            return

        with open(file_path, "w", encoding="utf-8") as file:
            file.write("SecurePass AI - Password History\n")
            file.write("=" * 40 + "\n\n")

            for password in self.password_history:
                file.write(password + "\n")

    def check_password(self):
        password = self.password_entry.get()

        result = password_checker(password)

        requirements = (
            f"{'✅' if result['length'] else '❌'} 8+ Characters\n"
            f"{'✅' if result['uppercase'] else '❌'} Uppercase\n"
            f"{'✅' if result['lowercase'] else '❌'} Lowercase\n"
            f"{'✅' if result['number'] else '❌'} Number\n"
            f"{'✅' if result['special'] else '❌'} Special Character"
        )

        self.requirements_label.configure(text=requirements)

        self.progress.set(result["score"] / 5)

        if result["strength"] == "Weak":
            color = "red"
        elif result["strength"] == "Medium":
            color = "orange"
        else:
            color = "green"

        self.result_label.configure(
            text=f"🔥 Strength : {result['strength']}",
            text_color=color
        )

        self.crack_time_label.configure(
            text=f"Estimated Crack Time : {result.get('crack_time', '-')}"

        )

        # Show AI Suggestions
        if result["suggestions"]:
         suggestions = "\n".join(result["suggestions"])
        else:
         suggestions = "✅ No security issues detected."

        self.ai_label.configure(
        text=f"🤖 AI Suggestions:\n{suggestions}"
)

        
    def sidebar_action(self, item):
         messagebox.showinfo(
        "Menu",
        f"You clicked:\n\n{item}"
    )