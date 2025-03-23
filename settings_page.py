import customtkinter as ctk
from datetime import datetime
import json
import pandas as pd
import os

class SettingsPage(ctk.CTkFrame):
    def __init__(self, parent, font_family, on_back):
        super().__init__(parent)
        self.parent = parent
        self.font_family = font_family
        self.font_family_bold = (font_family, "bold")
        self.on_back = on_back
        
        # Excel file path
        self.excel_file = "parameters.xlsx"
        
        # Create save indicator first
        self.save_indicator = ctk.CTkLabel(
            self,
            text="",
            font=(self.font_family, 13),
            text_color="#22C55E"
        )
        self.save_indicator.place(
            relx=0.98,  # Slightly offset from right edge
            rely=0.98,  # Slightly offset from bottom edge
            anchor="se"
        )
        
        # Load settings before creating UI
        self.load_settings()
        
        # Configure main frame
        self.configure(fg_color="#0F172A")
        
        # Create header bar
        self.create_header_bar()
        
        # Create main grid container
        self.grid_container = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        self.grid_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Configure grid layout - 3x2 grid
        self.grid_container.grid_columnconfigure((0, 1, 2), weight=1, uniform="column")
        self.grid_container.grid_rowconfigure((0, 1), weight=1, uniform="row")
        
        # Create all sections in grid layout
        self.create_grid_sections()

    def load_settings(self):
        try:
            # First try to load from Excel
            if os.path.exists(self.excel_file):
                df = pd.read_excel(self.excel_file)
                excel_settings = df.set_index('Parameter')['Value'].to_dict()
            else:
                excel_settings = {}

            # Merge with default settings
            self.settings = {
                # Excel parameters
                **excel_settings,
                
                # Additional UI settings
                "profile": {
                    "name": "",
                    "email": "",
                    "company": "",
                    "phone": ""
                },
                "csv_config": {
                    "file_path": "data/measurements.csv",
                    "update_interval": 1000
                }
            }
            
            # Ensure all required parameters exist
            default_settings = self.get_default_settings()
            for key, value in default_settings.items():
                if key not in self.settings:
                    self.settings[key] = value
            
            self.save_to_excel()
            
        except Exception as e:
            print(f"Error loading Excel: {e}")
            self.settings = self.get_default_settings()

    def save_settings(self):
        try:
            # Save to Excel file
            df = pd.DataFrame(list(self.settings.items()), columns=['Parameter', 'Value'])
            df.to_excel(self.excel_file, index=False)
            self.show_save_indicator(True)
        except Exception as e:
            print(f"Error saving to Excel: {e}")
            self.show_save_indicator(False)

    def create_header_bar(self):
        header_bar = ctk.CTkFrame(
            self,
            fg_color="#1E293B",
            height=60,
            corner_radius=0
        )
        header_bar.pack(fill="x")
        header_bar.pack_propagate(False)
        
        # Container for header content
        header_content = ctk.CTkFrame(header_bar, fg_color="transparent")
        header_content.pack(fill="both", expand=True, padx=20)
        
        # Left side container
        left_container = ctk.CTkFrame(header_content, fg_color="transparent")
        left_container.pack(side="left", fill="y")
        
        # Back button with improved styling
        back_button = ctk.CTkButton(
            left_container,
            text="← Back to Dashboard",
            font=(self.font_family, 14),
            fg_color="transparent",
            hover_color="#2563EB",
            command=self.handle_back,
            width=150,
            height=32
        )
        back_button.pack(side="left", padx=(0, 20))
        
        # Title
        title = ctk.CTkLabel(
            left_container,
            text="Settings",
            font=(self.font_family_bold, 20),
            text_color="#F1F5F9"
        )
        title.pack(side="left")
        
        # Right side container for save button
        right_container = ctk.CTkFrame(header_content, fg_color="transparent")
        right_container.pack(side="right", fill="y")
        
        # Save button
        self.save_button = ctk.CTkButton(
            right_container,
            text="Save Changes",
            font=(self.font_family, 14),
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            command=self.handle_save,
            width=120,
            height=32,
            corner_radius=6,
            border_width=1,
            border_color="#3B82F6"
        )
        self.save_button.pack(side="right")

    def create_grid_sections(self):
        # User Profile (Top Left)
        profile_section = self.create_compact_section(
            "👤 Profile",
            grid_pos=(0, 0)
        )
        self.create_profile_content(profile_section)
        
        # Protection Settings (Top Middle)
        protection_section = self.create_compact_section(
            "🛡️ Protection",
            grid_pos=(0, 1)
        )
        self.create_protection_content(protection_section)
        
        # Fault Settings (Top Right)
        fault_section = self.create_compact_section(
            "⚠️ Fault Detection",
            grid_pos=(0, 2)
        )
        self.create_fault_content(fault_section)
        
        # Trip Settings (Bottom Left)
        trip_section = self.create_compact_section(
            "⚡ Trip Settings",
            grid_pos=(1, 0)
        )
        self.create_trip_content(trip_section)
        
        # Data Settings (Bottom Middle)
        data_section = self.create_compact_section(
            "📊 Data Config",
            grid_pos=(1, 1)
        )
        self.create_data_content(data_section)
        
        # System Settings (Bottom Right)
        system_section = self.create_compact_section(
            "⚙️ System",
            grid_pos=(1, 2)
        )
        self.create_system_content(system_section)

    def create_compact_section(self, title, grid_pos):
        section = ctk.CTkFrame(
            self.grid_container,
            fg_color="#1E293B",
            corner_radius=12,
            border_width=1,
            border_color="#334155"
        )
        section.grid(row=grid_pos[0], column=grid_pos[1], padx=10, pady=10, sticky="nsew")
        
        # Title bar
        title_bar = ctk.CTkFrame(
            section,
            fg_color="#162234",
            height=40,
            corner_radius=8
        )
        title_bar.pack(fill="x", padx=8, pady=8)
        title_bar.pack_propagate(False)
        
        title_label = ctk.CTkLabel(
            title_bar,
            text=title,
            font=(self.font_family_bold, 15),
            text_color="#F1F5F9"
        )
        title_label.pack(side="left", padx=12)
        
        return section

    def create_profile_content(self, parent):
        content = ctk.CTkFrame(parent, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=8, pady=(0, 8))
        
        fields = [
            ("Name", "name"),
            ("Email", "email"),
            ("Company", "company"),
            ("Phone", "phone")
        ]
        
        for label, key in fields:
            self.create_compact_input(content, label, key)

    def create_protection_content(self, parent):
        content = ctk.CTkFrame(parent, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=8, pady=(0, 8))
        
        # Input protections
        input_protections = [
            ("Phase A Over-Current", "input_phase_a_over_current_status", "input_phase_a_over_current_set_value", 10),
            ("Phase B Over-Current", "input_phase_b_over_current_status", "input_phase_b_over_current_set_value", 20),
            ("Phase C Over-Current", "input_phase_c_over_current_status", "input_phase_c_over_current_set_value", 40),
            ("Phase A Over-Voltage", "input_phase_a_over_voltage_status", "input_phase_a_over_voltage_set_value", 10),
            ("Phase B Over-Voltage", "input_phase_b_over_voltage_status", "input_phase_b_over_voltage_set_value", 3),
            ("Phase C Over-Voltage", "input_phase_c_over_voltage_status", "input_phase_c_over_voltage_set_value", 0)
        ]
        
        # Create section label
        section_label = ctk.CTkLabel(
            content,
            text="Input Protection",
            font=(self.font_family_bold, 14),
            text_color="#94A3B8"
        )
        section_label.pack(anchor="w", pady=(0, 8))
        
        # Create toggles with value inputs
        for label, status_key, value_key, default_value in input_protections:
            self.create_protection_toggle(content, label, status_key, value_key, default_value)

    def create_protection_toggle(self, parent, label, status_key, value_key, default_value):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", pady=4)
        
        # Create horizontal container
        container = ctk.CTkFrame(frame, fg_color="transparent")
        container.pack(fill="x")
        
        # Initialize status value if not present
        if status_key not in self.settings:
            self.settings[status_key] = 0
            self.save_to_excel()  # Save immediately when adding new parameter
        if value_key not in self.settings:
            self.settings[value_key] = default_value
            self.save_to_excel()  # Save immediately when adding new parameter
        
        # Create switch
        switch_var = ctk.BooleanVar(value=bool(self.settings[status_key]))
        
        def on_toggle():
            # Update status value (0 or 1)
            self.settings[status_key] = 1 if switch_var.get() else 0
            # Show/hide value entry
            if switch_var.get():
                value_frame.pack(fill="x", pady=(4, 0))
            else:
                value_frame.pack_forget()
            self.save_to_excel()  # Save to Excel immediately
        
        switch = ctk.CTkSwitch(
            container,
            text=label,
            variable=switch_var,
            font=(self.font_family, 13),
            progress_color="#2563EB",
            button_color="#1E293B",
            button_hover_color="#2563EB",
            height=24,
            command=on_toggle
        )
        switch.pack(side="left")
        
        # Create value entry frame
        value_frame = ctk.CTkFrame(frame, fg_color="transparent")
        if switch_var.get():
            value_frame.pack(fill="x", pady=(4, 0))
        
        # Create value entry
        value_entry = ctk.CTkEntry(
            value_frame,
            font=(self.font_family, 13),
            fg_color="#1E293B",
            border_color="#334155",
            text_color="#F1F5F9",
            height=28,
            placeholder_text="Enter value"
        )
        value_entry.insert(0, str(self.settings[value_key]))
        value_entry.pack(fill="x", padx=(32, 0))
        
        def save_value(event=None):
            try:
                value = float(value_entry.get())
                self.settings[value_key] = value
                self.save_to_excel()  # Save to Excel immediately
            except ValueError:
                # Reset to previous value if invalid input
                value_entry.delete(0, 'end')
                value_entry.insert(0, str(self.settings[value_key]))
        
        value_entry.bind("<FocusOut>", save_value)
        value_entry.bind("<Return>", save_value)

    def create_fault_content(self, parent):
        content = ctk.CTkFrame(parent, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=8, pady=(0, 8))
        
        faults = [
            ("Over-voltage", "over_voltage"),
            ("Over-current", "over_current"),
            ("Short Circuit", "short_circuit"),
            ("Ground Fault", "ground_fault")
        ]
        
        for label, key in faults:
            self.create_compact_toggle(content, label, key)

    def create_trip_content(self, parent):
        content = ctk.CTkFrame(parent, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=8, pady=(0, 8))
        
        trips = [
            ("Instantaneous", "instantaneous"),
            ("Inverse Time", "inverse_time"),
            ("Definite Time", "definite_time"),
            ("Differential", "differential")
        ]
        
        for label, key in trips:
            self.create_compact_toggle(content, label, key)

    def create_data_content(self, parent):
        content = ctk.CTkFrame(parent, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=8, pady=(0, 8))
        
        self.create_compact_input(content, "CSV Path", "file_path", settings_key="csv_config")
        self.create_compact_input(content, "Interval (ms)", "update_interval", settings_key="csv_config")

    def create_system_content(self, parent):
        content = ctk.CTkFrame(parent, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=8, pady=(0, 8))
        
        settings = [
            ("Auto-update", "auto_update"),
            ("Notifications", "notifications"),
            ("Dark Mode", "dark_mode"),
            ("Analytics", "analytics")
        ]
        
        for label, key in settings:
            self.create_compact_toggle(content, label, key)

    def create_compact_input(self, parent, label, key, settings_key="profile"):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", pady=4)
        
        label = ctk.CTkLabel(
            frame,
            text=label,
            font=(self.font_family, 13),
            text_color="#94A3B8"
        )
        label.pack(anchor="w")
        
        # Safely get the value, with empty string as default
        value = ""
        try:
            if settings_key in self.settings and isinstance(self.settings[settings_key], dict):
                value = str(self.settings[settings_key].get(key, ""))
            else:
                self.settings[settings_key] = {}
                self.settings[settings_key][key] = value
        except Exception as e:
            print(f"Error accessing settings: {e}")
        
        entry = ctk.CTkEntry(
            frame,
            font=(self.font_family, 13),
            fg_color="#1E293B",
            border_color="#334155",
            text_color="#F1F5F9",
            height=28
        )
        entry.insert(0, value)
        entry.pack(fill="x", pady=(2, 0))
        
        def save_value(event=None):
            if settings_key not in self.settings:
                self.settings[settings_key] = {}
            self.settings[settings_key][key] = entry.get()
            self.save_to_excel()
        
        entry.bind("<FocusOut>", save_value)
        entry.bind("<Return>", save_value)

    def create_compact_toggle(self, parent, label, key):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", pady=4)
        
        switch_var = ctk.BooleanVar(value=self.settings.get(key, False))
        
        switch = ctk.CTkSwitch(
            frame,
            text=label,
            variable=switch_var,
            font=(self.font_family, 13),
            progress_color="#2563EB",
            button_color="#1E293B",
            button_hover_color="#2563EB",
            height=24
        )
        switch.pack(fill="x")

    def show_save_indicator(self, success=True):
        if success:
            self.save_indicator.configure(
                text="✓ Changes saved successfully",
                text_color="#22C55E"
            )
        else:
            self.save_indicator.configure(
                text="✕ Error saving changes",
                text_color="#EF4444"
            )
        
        # Clear the message after 2 seconds
        self.after(2000, lambda: self.save_indicator.configure(text=""))

    def handle_back(self):
        print("Back button clicked")
        # Save any pending changes
        self.save_settings()
        
        # Call the callback to return to dashboard
        if self.on_back:
            self.on_back()

    def handle_save(self):
        """Handle save button click"""
        try:
            # Save to Excel
            self.save_to_excel()
            
            # Show success message
            self.show_save_indicator(True)
            
            # Temporarily disable save button to prevent double-clicks
            self.save_button.configure(state="disabled")
            self.after(1000, lambda: self.save_button.configure(state="normal"))
            
        except Exception as e:
            print(f"Error saving settings: {e}")
            self.show_save_indicator(False)

    def get_default_settings(self):
        # Return default settings matching the Excel structure
        return {
            "input_phase_a_over_current_status": 1,
            "input_phase_a_over_current_set_value": 10,
            "input_phase_b_over_current_status": 0,
            "input_phase_b_over_current_set_value": 20,
            "input_phase_c_over_current_status": 0,
            "input_phase_c_over_current_set_value": 40,
            "input_phase_a_over_voltage_status": 0,
            "input_phase_a_over_voltage_set_value": 10,
            "input_phase_b_over_voltage_status": 0,
            "input_phase_b_over_voltage_set_value": 3,
            "input_phase_c_over_voltage_status": 0,
            "input_phase_c_over_voltage_set_value": 0,
            # Add all other parameters from your Excel file
            "Instantaneous_Trip_Characteristics_status": 0,
            "Inverse_Time_Characteristics_status": 0,
            "Definite_Time_Characteristics_status": 0,
            "Differential_Relay_Characteristics_status": 0,
            "Trip_button": 0,
            "Reset_button": 0
        }

    def save_to_excel(self):
        """Save settings to Excel file immediately"""
        try:
            # Convert settings to DataFrame format
            data = {'Parameter': [], 'Value': []}
            
            # Add Excel-specific parameters
            for key, value in self.settings.items():
                # Skip dictionary-type settings (profile, csv_config)
                if not isinstance(value, dict):
                    data['Parameter'].append(key)
                    data['Value'].append(value)
            
            df = pd.DataFrame(data)
            df.to_excel(self.excel_file, index=False)
            self.show_save_indicator(True)
        except Exception as e:
            print(f"Error saving to Excel: {e}")
            self.show_save_indicator(False)
            self.on_back() 