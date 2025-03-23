import customtkinter as ctk
from storage import LocalStorage

class SignupPage(ctk.CTkFrame):
    def __init__(self, parent, show_login_page, font_family):
        super().__init__(parent)
        self.configure(fg_color="#0F172A")
        
        # Set up Consolas font
        self.font_family = "Consolas"
        self.font_family_bold = ("Consolas", "bold")
        
        self.storage = LocalStorage()
        self.show_login_page = show_login_page
        
        # Create content frame with enhanced glass morphism effect
        content_frame = ctk.CTkFrame(
            self,
            fg_color=("#1E293B", "#1E293B"),
            corner_radius=24,
            border_width=2,
            border_color="#334155"
        )
        content_frame.pack(expand=True, padx=40, pady=40, ipadx=80, ipady=50)

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
            text="Create Account",
            font=(self.font_family_bold, 40),
            text_color="#F1F5F9"
        )
        title_label.pack(pady=(0, 10))

        # Subtitle with enhanced styling
        subtitle_label = ctk.CTkLabel(
            content_frame,
            text="Join us to monitor and control your system",
            font=(self.font_family, 14),
            text_color="#94A3B8"
        )
        subtitle_label.pack(pady=(0, 40))

        # Username input with enhanced styling
        username_label = ctk.CTkLabel(
            content_frame,
            text="USERNAME",
            font=(self.font_family_bold, 12),
            text_color="#64748B"
        )
        username_label.pack(anchor="w", padx=50, pady=(0, 8))
        
        self.username_entry = ctk.CTkEntry(
            content_frame,
            font=(self.font_family, 14),
            fg_color="#1E293B",
            border_color="#475569",
            border_width=2,
            text_color="#F1F5F9",
            height=45,
            placeholder_text="Choose a username",
            placeholder_text_color="#475569"
        )
        self.username_entry.pack(fill="x", padx=50, pady=(0, 20))

        # Password input with enhanced styling
        password_label = ctk.CTkLabel(
            content_frame,
            text="PASSWORD",
            font=(self.font_family_bold, 12),
            text_color="#64748B"
        )
        password_label.pack(anchor="w", padx=50, pady=(0, 8))
        
        self.password_entry = ctk.CTkEntry(
            content_frame,
            font=(self.font_family, 14),
            fg_color="#1E293B",
            border_color="#475569",
            border_width=2,
            text_color="#F1F5F9",
            height=45,
            show="●",
            placeholder_text="Create a password",
            placeholder_text_color="#475569"
        )
        self.password_entry.pack(fill="x", padx=50, pady=(0, 20))

        # Confirm Password input with enhanced styling
        confirm_password_label = ctk.CTkLabel(
            content_frame,
            text="CONFIRM PASSWORD",
            font=(self.font_family_bold, 12),
            text_color="#64748B"
        )
        confirm_password_label.pack(anchor="w", padx=50, pady=(0, 8))
        
        self.confirm_password_entry = ctk.CTkEntry(
            content_frame,
            font=(self.font_family, 14),
            fg_color="#1E293B",
            border_color="#475569",
            border_width=2,
            text_color="#F1F5F9",
            height=45,
            show="●",
            placeholder_text="Confirm your password",
            placeholder_text_color="#475569"
        )
        self.confirm_password_entry.pack(fill="x", padx=50, pady=(0, 30))

        # Error label with enhanced styling
        self.error_label = ctk.CTkLabel(
            content_frame,
            text="",
            font=(self.font_family, 13),
            text_color="#EF4444"
        )
        self.error_label.pack(pady=(0, 15))
        self.error_label.pack_forget()

        # Sign Up button with enhanced styling
        signup_button = ctk.CTkButton(
            content_frame,
            text="Create Account",
            font=(self.font_family_bold, 15),
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            corner_radius=12,
            height=50,
            command=self.handle_signup
        )
        signup_button.pack(fill="x", padx=50, pady=(0, 30))

        # Separator
        separator = ctk.CTkFrame(
            content_frame,
            height=2,
            fg_color="#334155"
        )
        separator.pack(fill="x", padx=50, pady=(0, 30))

        # Login link with enhanced styling
        login_frame = ctk.CTkFrame(
            content_frame,
            fg_color="transparent"
        )
        login_frame.pack(fill="x", padx=50)

        login_text = ctk.CTkLabel(
            login_frame,
            text="Already have an account? ",
            font=(self.font_family, 13),
            text_color="#94A3B8"
        )
        login_text.pack(side="left", padx=(0, 0))

        login_link = ctk.CTkButton(
            login_frame,
            text="Sign in here",
            font=(self.font_family_bold, 13),
            fg_color="transparent",
            hover_color="#1E293B",
            text_color="#3B82F6",
            command=self.show_login_page,
            width=20,
            height=20
        )
        login_link.pack(side="left", padx=(0, 0))

    def handle_signup(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if not username or not password or not confirm_password:
            self.show_error("Please fill in all fields")
            return

        if password != confirm_password:
            self.show_error("Passwords do not match")
            return

        if len(password) < 6:
            self.show_error("Password must be at least 6 characters")
            return

        # Add the new user
        success, message = self.storage.create_user(username, password)
        if success:
            self.show_login_page()  # Redirect to login page after successful signup
        else:
            self.show_error(message)

    def show_error(self, message):
        self.error_label.configure(text=message)
        self.error_label.pack(pady=(0, 10)) 