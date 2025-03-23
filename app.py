import customtkinter as ctk
import webbrowser
from PIL import Image, ImageTk
from login_page import LoginPage
from signup_page import SignupPage
from tkinter import font
import os
import requests
import tempfile
from dashboard_page import DashboardPage

# Create a simple localStorage-like class for storing session data
class LocalStorage:
    def __init__(self):
        self._storage = {}

    def setItem(self, key, value):
        self._storage[key] = value

    def getItem(self, key):
        return self._storage.get(key)

    def removeItem(self, key):
        if key in self._storage:
            del self._storage[key]

# Initialize localStorage
localStorage = LocalStorage()

class ProtectionRelayApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("Protection Relay")
        self.geometry("1200x800")
        self.configure(fg_color="#111827")
        
        # Try different methods to remove icon based on platform
        try:
            # For Windows
            self.iconbitmap(default="")
        except:
            try:
                # For Linux/Unix
                self.wm_iconbitmap("")
            except:
                pass  # If both methods fail, just continue
        
        # Set up Consolas font
        self.font_family = "Consolas"
        self.font_family_bold = ("Consolas", "bold")
        
        # Create the main page first
        self.main_page = self.create_main_page()
        
        # Initialize first page
        self.current_page = None
        self.check_auth()

    def check_auth(self):
        # Check if user is already logged in
        is_authenticated = localStorage.getItem("isAuthenticated")
        if is_authenticated == "true":
            self.show_dashboard()
        else:
            self.show_main_page()  # Show main page instead of login page directly

    def load_custom_font(self):
        # Get the absolute path to the fonts directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        fonts_dir = os.path.join(current_dir, "fonts")
        
        # Register the font files
        font_paths = {
            "regular": os.path.join(fonts_dir, "Manrope-Regular.ttf"),
            "bold": os.path.join(fonts_dir, "Manrope-Bold.ttf"),
        }
        
        for style, path in font_paths.items():
            try:
                font.families()  # Initialize font system
                font.Font(file=path, family="Manrope")
            except Exception as e:
                print(f"Error loading font: {e}")
                self.font_family = "Arial"  # Fallback to Arial if font loading fails

    def create_main_page(self):
        page = ctk.CTkFrame(self, fg_color="#0F172A")
        
        # Create content frame with increased size
        content_frame = ctk.CTkFrame(
            page,
            fg_color=("#1E293B", "#1E293B"),
            corner_radius=16,
            border_width=2,
            border_color="#334155"
        )
        content_frame.pack(expand=True, padx=100, pady=80, ipadx=100, ipady=80)  # Increased padding and internal padding

        # Logo with larger size
        logo_label = ctk.CTkLabel(
            content_frame,
            text="⚡",
            font=(self.font_family, 64),  # Increased font size
            text_color="#60A5FA"
        )
        logo_label.pack(pady=(20, 30))  # Increased padding

        # Title with larger size
        title_label = ctk.CTkLabel(
            content_frame,
            text="Protection Relay",
            font=(self.font_family_bold, 48),  # Increased font size
            text_color="#F1F5F9"
        )
        title_label.pack(pady=(0, 20))

        # Subtitle with larger size
        subtitle_label = ctk.CTkLabel(
            content_frame,
            text="Welcome to the Solid State Transformer\nProtection Relay System",
            font=(self.font_family, 16),  # Increased font size
            text_color="#94A3B8"
        )
        subtitle_label.pack(pady=(0, 60))  # Increased padding

        # Login button with increased size
        login_button = ctk.CTkButton(
            content_frame,
            text="Login",
            font=(self.font_family_bold, 18),  # Increased font size
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            corner_radius=12,
            height=50,  # Increased height
            command=self.show_login_page
        )
        login_button.pack(fill="x", padx=60, pady=(0, 20))  # Increased padding

        # Sign Up button with increased size
        signup_button = ctk.CTkButton(
            content_frame,
            text="Sign Up",
            font=(self.font_family_bold, 18),  # Increased font size
            fg_color="#1E293B",
            hover_color="#334155",
            border_width=2,
            border_color="#3B82F6",
            corner_radius=12,
            height=50,  # Increased height
            command=self.show_signup_page
        )
        signup_button.pack(fill="x", padx=60, pady=(0, 40))  # Increased padding

        return page

    def show_main_page(self):
        if self.current_page:
            self.current_page.pack_forget()
        self.main_page.pack(fill="both", expand=True)
        self.current_page = self.main_page

    def show_login_page(self):
        if hasattr(self, 'current_page') and self.current_page:
            self.current_page.pack_forget()
        self.current_page = LoginPage(
            self,
            self.show_signup_page,
            self.show_dashboard,
            self.font_family
        )
        self.current_page.pack(fill="both", expand=True)

    def show_signup_page(self):
        if hasattr(self, 'current_page') and self.current_page:
            self.current_page.pack_forget()
        self.current_page = SignupPage(
            self,
            self.show_login_page,
            self.font_family
        )
        self.current_page.pack(fill="both", expand=True)

    def show_dashboard(self):
        if hasattr(self, 'current_page') and self.current_page:
            self.current_page.pack_forget()
        self.current_page = DashboardPage(
            self,
            self.font_family
        )
        self.current_page.pack(fill="both", expand=True)

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = ProtectionRelayApp()
    
    # Center window on screen
    window_width = 1200
    window_height = 800
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    app.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    app.mainloop()
