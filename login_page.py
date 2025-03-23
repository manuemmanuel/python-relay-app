import customtkinter as ctk
import json
import os

class LoginPage(ctk.CTkFrame):
    def __init__(self, parent, show_signup_page, show_dashboard, font_family):
        super().__init__(parent)
        self.configure(fg_color="#0F172A")
        self.font_family = font_family
        
        # Store callbacks
        self.show_signup_page = show_signup_page
        self.show_dashboard = show_dashboard
        
        # Create content frame with enhanced glass morphism effect
        content_frame = ctk.CTkFrame(
            self,
            fg_color=("#1E293B", "#1E293B"),
            corner_radius=24,
            border_width=2,
            border_color="#334155"
        )
        content_frame.pack(expand=True, padx=40, pady=40, ipadx=50, ipady=50)

        # Logo
        logo_label = ctk.CTkLabel(
            content_frame,
            text="⚡",
            font=(self.font_family, 48),
            text_color="#60A5FA"
        )
        logo_label.pack(pady=(0, 15))

        # Title with enhanced styling
        title_label = ctk.CTkLabel(
            content_frame,
            text="Welcome Back",
            font=(self.font_family, 40, "bold"),
            text_color="#F1F5F9"
        )
        title_label.pack(pady=(0, 10))

        # Subtitle with enhanced styling
        subtitle_label = ctk.CTkLabel(
            content_frame,
            text="Enter your credentials to access your account",
            font=(self.font_family, 14),
            text_color="#94A3B8"
        )
        subtitle_label.pack(pady=(0, 40))

        # Username input with enhanced styling
        username_label = ctk.CTkLabel(
            content_frame,
            text="USERNAME",
            font=(self.font_family, 12, "bold"),
            text_color="#64748B"
        )
        username_label.pack(anchor="w", padx=30, pady=(0, 8))
        
        self.username_entry = ctk.CTkEntry(
            content_frame,
            font=(self.font_family, 15),
            fg_color="#1E293B",
            border_color="#475569",
            border_width=2,
            text_color="#F1F5F9",
            height=48,
            placeholder_text="Enter your username",
            placeholder_text_color="#475569",
            corner_radius=12
        )
        self.username_entry.pack(fill="x", padx=30, pady=(0, 20))

        # Password input with enhanced styling
        password_label = ctk.CTkLabel(
            content_frame,
            text="PASSWORD",
            font=(self.font_family, 12, "bold"),
            text_color="#64748B"
        )
        password_label.pack(anchor="w", padx=30, pady=(0, 8))
        
        self.password_entry = ctk.CTkEntry(
            content_frame,
            font=(self.font_family, 14),
            fg_color="#1E293B",
            border_color="#475569",
            border_width=2,
            text_color="#F1F5F9",
            height=45,
            show="●",
            placeholder_text="Enter your password",
            placeholder_text_color="#475569"
        )
        self.password_entry.pack(fill="x", padx=30, pady=(0, 30))

        # Error label with enhanced styling
        self.error_label = ctk.CTkLabel(
            content_frame,
            text="",
            font=(self.font_family, 13),
            text_color="#EF4444"
        )
        self.error_label.pack(pady=(0, 15))
        self.error_label.pack_forget()

        # Login button with enhanced styling
        login_button = ctk.CTkButton(
            content_frame,
            text="Sign In",
            font=(self.font_family, 16, "bold"),
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            corner_radius=14,
            height=52,
            command=self.handle_login
        )
        login_button.pack(fill="x", padx=30, pady=(0, 30))

        # Separator
        separator = ctk.CTkFrame(
            content_frame,
            height=2,
            fg_color="#334155"
        )
        separator.pack(fill="x", padx=30, pady=(0, 30))

        # Sign up link with enhanced styling
        signup_frame = ctk.CTkFrame(
            content_frame,
            fg_color="transparent"
        )
        signup_frame.pack(fill="x", padx=30)

        signup_text = ctk.CTkLabel(
            signup_frame,
            text="New to Protection Relay? ",
            font=(self.font_family, 13),
            text_color="#94A3B8"
        )
        signup_text.pack(side="left", padx=(0, 0))

        signup_link = ctk.CTkButton(
            signup_frame,
            text="Create an account",
            font=(self.font_family, 13, "bold"),
            fg_color="transparent",
            hover_color="#1E293B",
            text_color="#3B82F6",
            command=self.show_signup_page,
            width=20,
            height=20
        )
        signup_link.pack(side="left", padx=(0, 0))

    def handle_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            self.show_error("Please fill in all fields")
            return

        # Check if users.json exists
        if not os.path.exists("users.json"):
            with open("users.json", "w") as f:
                json.dump({}, f)

        # Get stored users from JSON file
        try:
            with open("users.json", "r") as f:
                users = json.load(f)
        except:
            users = {}

        # For testing purposes, allow admin/admin login
        if username == "admin" and password == "admin":
            self.show_dashboard()
            return

        # Verify credentials
        if username in users and users[username]["password"] == password:
            self.show_dashboard()
        else:
            self.show_error("Invalid username or password")

    def show_error(self, message):
        self.error_label.configure(text=message)
        self.error_label.pack(pady=(0, 10)) 