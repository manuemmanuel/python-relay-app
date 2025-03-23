import customtkinter as ctk
from tkinter import font
import os
import requests
import tempfile

def load_manrope_font():
    # URLs for Manrope font files
    font_urls = {
        "regular": "https://fonts.gstatic.com/s/manrope/v15/xn7gYHE41ni1AdIRggexSg.ttf",
        "bold": "https://fonts.gstatic.com/s/manrope/v15/xn7gYHE41ni1AdIRggexSg.ttf"
    }
    
    font_files = {}
    temp_dir = tempfile.gettempdir()
    
    # Download and load fonts
    for style, url in font_urls.items():
        try:
            # Create font file path
            font_path = os.path.join(temp_dir, f"Manrope-{style}.ttf")
            
            # Download font if not exists
            if not os.path.exists(font_path):
                response = requests.get(url)
                with open(font_path, "wb") as f:
                    f.write(response.content)
            
            # Load font
            font_files[style] = font.Font(file=font_path, family="Manrope")
            
        except Exception as e:
            print(f"Error loading font: {e}")
            return "Helvetica"  # Fallback font
    
    return "Manrope"

# Load Manrope font when module is imported
FONT_FAMILY = load_manrope_font() 