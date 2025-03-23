import customtkinter as ctk
from datetime import datetime
import json
import random
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading
from settings_page import SettingsPage

class CSVFileHandler(FileSystemEventHandler):
    def __init__(self, dashboard):
        self.dashboard = dashboard

    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith('.csv'):
            # Run the update on the main thread to avoid tkinter threading issues
            self.dashboard.after(0, self.dashboard.update_from_files)

class DashboardPage(ctk.CTkFrame):
    def __init__(self, parent, font_family):
        super().__init__(parent)
        self.parent = parent  # Store parent reference
        
        # Add at the beginning of __init__ after super().__init__
        self.last_input_modified = 0
        self.last_output_modified = 0
        
        # Set Consolas font with fallbacks
        try:
            import tkinter as tk
            test_label = tk.Label(font="Consolas")
            test_label.destroy()
            self.font_family = "Consolas"
            self.font_family_bold = ("Consolas", "bold")
        except:
            # Fallback to other monospace fonts
            self.font_family = "Courier"
            self.font_family_bold = ("Courier", "bold")
        
        self.configure(fg_color="#0F172A")  # Darker background for better contrast
        
        # Create gradient effect background
        gradient_frame = ctk.CTkFrame(
            self,
            fg_color="#0F172A",
            corner_radius=0
        )
        gradient_frame.place(relx=0.5, rely=0.5, relwidth=1, relheight=1)
        
        # Create the main container first - MUST BE CREATED BEFORE OTHER COMPONENTS
        self.main_container = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            corner_radius=0,
            scrollbar_button_color="#1E293B",
            scrollbar_button_hover_color="#2563EB",
            border_width=0,
            border_color="#1E293B"
        )
        self.main_container.pack(fill="both", expand=True, padx=30, pady=30)

        # Add version number
        version_label = ctk.CTkLabel(
            self,
            text="v1.0.0",
            font=(self.font_family, 12),
            text_color="#475569"
        )
        version_label.place(relx=0.98, rely=0.98, anchor="se")

        # Create components in the correct order
        self.create_header()
        self.create_monitoring_panels()
        self.create_config_selector()
        self.create_measurement_panels()
        self.create_options_panel()
        
        # Initialize file observers
        self.setup_file_watchers()
        
        # Start real-time updates
        self.start_updates()

    def create_header(self):
        # Enhanced header frame with glass morphism effect
        header_frame = ctk.CTkFrame(
            self.main_container,
            fg_color="#1E293B",
            corner_radius=20,
            border_width=2,
            border_color="#334155"
        )
        header_frame.pack(fill="x", pady=(0, 25))

        # Inner header content with increased padding
        inner_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        inner_frame.pack(fill="x", padx=25, pady=20)

        # Logo and Title container
        title_container = ctk.CTkFrame(inner_frame, fg_color="transparent")
        title_container.pack(side="left")

        # Enhanced logo with glow effect
        logo_frame = ctk.CTkFrame(
            title_container,
            fg_color="#2563EB",
            corner_radius=15,
            width=45,
            height=45
        )
        logo_frame.pack(side="left", padx=(0, 15))
        logo_frame.pack_propagate(False)

        logo_label = ctk.CTkLabel(
            logo_frame,
            text="⚡",
            font=(self.font_family, 24),
            text_color="#FFFFFF"
        )
        logo_label.place(relx=0.5, rely=0.5, anchor="center")

        # Title with enhanced typography
        title = ctk.CTkLabel(
            title_container,
            text="Solid State Transformer",
            font=(self.font_family_bold, 28),
            text_color="#F1F5F9"
        )
        title.pack(side="left")

        # Subtitle
        subtitle = ctk.CTkLabel(
            title_container,
            text="Protection Relay System",
            font=(self.font_family, 14),
            text_color="#94A3B8"
        )
        subtitle.pack(side="left", padx=(10, 0))

        # DateTime with enhanced styling
        time_container = ctk.CTkFrame(
            inner_frame,
            fg_color="#0F172A",
            corner_radius=12
        )
        time_container.pack(side="right")

        self.time_label = ctk.CTkLabel(
            time_container,
            text="",
            font=(self.font_family, 14),
            text_color="#94A3B8"
        )
        self.time_label.pack(padx=15, pady=8)
        self.update_time()

    def create_monitoring_panels(self):
        panels_frame = ctk.CTkFrame(
            self.main_container,
            fg_color="transparent"
        )
        panels_frame.pack(fill="x", pady=(0, 25))

        # Create grid layout with improved spacing
        panels_frame.grid_columnconfigure(0, weight=1)
        panels_frame.grid_columnconfigure(1, weight=1)
        panels_frame.grid_rowconfigure(0, weight=1)

        # Relay Indication Panel
        self.create_relay_panel(panels_frame)
        
        # Energy Monitoring Panel
        self.create_energy_panel(panels_frame)

    def create_relay_panel(self, parent):
        relay_frame = ctk.CTkFrame(
            parent,
            fg_color="#1E293B",
            corner_radius=15,
            border_width=1,
            border_color="#334155"
        )
        relay_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        # Enhanced title frame with gradient-like effect
        title_frame = ctk.CTkFrame(
            relay_frame,
            fg_color="#1E293B",
            corner_radius=12,
            height=50
        )
        title_frame.pack(fill="x", padx=15, pady=(15, 20))

        # Animated pulse indicator
        self.animate_pulse(title_frame, "#3B82F6")

        title = ctk.CTkLabel(
            title_frame,
            text="Relay Indication Panel",
            font=(self.font_family_bold, 18),
            text_color="#F1F5F9"
        )
        title.pack(side="left", padx=(10, 0))

        # Status indicators
        self.relay_status = self.create_status_item(relay_frame, "Relay Status:", "HEALTHY", "green")
        self.config_status = self.create_status_item(relay_frame, "Configuration:", "Three phase AC to Three phase AC", "blue")
        self.input_status = self.create_status_item(relay_frame, "Input Status:", "HEALTHY", "green")
        self.output_status = self.create_status_item(relay_frame, "Output Status:", "HEALTHY", "green")
        self.breaker_status = self.create_status_item(relay_frame, "Circuit Breaker:", "CLOSED", "green")
        self.fault_status = self.create_status_item(relay_frame, "Fault Status:", "NO FAULTS", "green")

        # Control buttons
        button_frame = ctk.CTkFrame(relay_frame, fg_color="transparent")
        button_frame.pack(fill="x", padx=15, pady=15)

        self.trip_button = ctk.CTkButton(
            button_frame,
            text="Trip",
            font=(self.font_family, 14),
            fg_color="#EF4444",
            hover_color="#DC2626",
            command=self.handle_trip
        )
        self.trip_button.pack(side="left", expand=True, padx=(0, 5))

        self.reset_button = ctk.CTkButton(
            button_frame,
            text="Reset",
            font=(self.font_family, 14),
            fg_color="#3B82F6",
            hover_color="#2563EB",
            command=self.handle_reset
        )
        self.reset_button.pack(side="left", expand=True, padx=(5, 0))

    def create_energy_panel(self, parent):
        energy_frame = ctk.CTkFrame(
            parent,
            fg_color="#1E293B",
            corner_radius=15,
            border_width=1,
            border_color="#334155"
        )
        energy_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        # Title and Phase Selector Container
        header_frame = ctk.CTkFrame(energy_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=15, pady=(15, 25))  # Increased bottom padding

        # Title container
        title_container = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_container.pack(side="left")

        pulse_indicator = ctk.CTkLabel(
            title_container,
            text="●",
            font=(self.font_family, 16),
            text_color="#22C55E"
        )
        pulse_indicator.pack(side="left", padx=(0, 5))

        title = ctk.CTkLabel(
            title_container,
            text="Energy Monitoring Panel",
            font=(self.font_family_bold, 18),
            text_color="#F1F5F9"
        )
        title.pack(side="left", padx=(10, 0))

        # Phase Selector
        phase_container = ctk.CTkFrame(header_frame, fg_color="transparent")
        phase_container.pack(side="right")

        phase_label = ctk.CTkLabel(
            phase_container,
            text="Phase:",
            font=(self.font_family, 14),
            text_color="#94A3B8"
        )
        phase_label.pack(side="left", padx=(0, 10))

        self.phase_selector = ctk.CTkOptionMenu(
            phase_container,
            values=["Phase A", "Phase B", "Phase C"],
            font=(self.font_family, 14),
            dropdown_font=(self.font_family, 14),
            fg_color="#272727",
            button_color="#2563EB",
            button_hover_color="#1D4ED8",
            dropdown_fg_color="#1E293B",
            dropdown_hover_color="#2563EB",
            dropdown_text_color="#F1F5F9",
            width=100,
            command=self.update_energy_values
        )
        self.phase_selector.pack(side="right")
        self.phase_selector.set("Phase A")

        # Container for metrics
        metrics_container = ctk.CTkFrame(energy_frame, fg_color="transparent")
        metrics_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Energy metrics with increased spacing
        self.active_energy = self.create_metric_item(metrics_container, "Active Power:", "0.00 kW")
        self.add_spacing(metrics_container, 8)  # Add spacing between metrics
        
        self.reactive_energy = self.create_metric_item(metrics_container, "Reactive Power:", "0.00 kVAR")
        self.add_spacing(metrics_container, 8)
        
        self.apparent_power = self.create_metric_item(metrics_container, "Apparent Power:", "0.00 kVA")
        self.add_spacing(metrics_container, 8)
        
        self.power_factor = self.create_metric_item(metrics_container, "Power Factor:", "0.00")
        self.add_spacing(metrics_container, 8)
        
        self.frequency = self.create_metric_item(metrics_container, "Frequency:", "0.00 Hz")
        self.add_spacing(metrics_container, 8)
        
        self.temperature = self.create_metric_item(metrics_container, "Temperature:", "0.00 °C")

    def add_spacing(self, parent, height):
        """Add vertical spacing between elements"""
        spacing = ctk.CTkFrame(parent, fg_color="transparent", height=height)
        spacing.pack(fill="x")

    def create_status_item(self, parent, label, initial_value, color):
        frame = ctk.CTkFrame(
            parent,
            fg_color="#162234",  # Slightly darker for depth
            corner_radius=12
        )
        frame.pack(fill="x", padx=20, pady=6)

        label = ctk.CTkLabel(
            frame,
            text=label,
            font=(self.font_family, 14),
            text_color="#94A3B8"
        )
        label.pack(side="left", padx=15, pady=12)

        value_colors = {
            "green": ("#22C55E", "#064E3B"),
            "red": ("#EF4444", "#7F1D1D"),
            "blue": ("#3B82F6", "#1E3A8A")
        }

        value_label = ctk.CTkLabel(
            frame,
            text=initial_value,
            font=(self.font_family_bold, 13),
            text_color=value_colors[color][0],
            fg_color=value_colors[color][1],
            corner_radius=8,
            padx=12,
            pady=6
        )
        value_label.pack(side="right", padx=15)
        return value_label

    def create_metric_item(self, parent, label, initial_value):
        frame = ctk.CTkFrame(
            parent,
            fg_color="#162234",
            corner_radius=12
        )
        frame.pack(fill="x", padx=20, pady=6)

        label = ctk.CTkLabel(
            frame,
            text=label,
            font=(self.font_family, 14),
            text_color="#94A3B8"
        )
        label.pack(side="left", padx=15, pady=12)

        value_container = ctk.CTkFrame(
            frame,
            fg_color="#1E293B",
            corner_radius=8
        )
        value_container.pack(side="right", padx=15, pady=6)

        value_label = ctk.CTkLabel(
            value_container,
            text=initial_value,
            font=(self.font_family_bold, 14),
            text_color="#F1F5F9"
        )
        value_label.pack(padx=12, pady=4)
        return value_label

    def create_config_selector(self):
        configs = [
            "Three phase AC to Three phase AC",
            "DC to Three phase AC",
            "Three phase AC to DC",
            "DC to DC",
            "Single Phase AC to DC",
            "DC to Single Phase AC",
            "Single Phase AC to Single Phase AC"
        ]
        
        selector_frame = ctk.CTkFrame(
            self.main_container,
            fg_color="#1E293B",
            corner_radius=15,
            border_width=1,
            border_color="#334155"
        )
        selector_frame.pack(fill="x", pady=(0, 20))

        # Add a label above the selector
        label = ctk.CTkLabel(
            selector_frame,
            text="System Configuration",
            font=(self.font_family_bold, 14),
            text_color="#94A3B8"
        )
        label.pack(padx=15, pady=(15, 5))

        self.config_menu = ctk.CTkOptionMenu(
            selector_frame,
            values=configs,
            font=(self.font_family, 14),
            dropdown_font=(self.font_family, 14),
            fg_color="#272727",
            button_color="#2563EB",
            button_hover_color="#1D4ED8",
            dropdown_fg_color="#1E293B",
            dropdown_hover_color="#2563EB",
            dropdown_text_color="#F1F5F9",
            corner_radius=8
        )
        self.config_menu.pack(fill="x", padx=15, pady=(5, 15))
        self.config_menu.set(configs[0])

    def update_time(self):
        current_time = datetime.now().strftime("%B %d, %Y %H:%M:%S")
        self.time_label.configure(text=current_time)
        self.after(1000, self.update_time)

    def handle_trip(self):
        self.relay_status.configure(text="TRIPPED", text_color="#EF4444", fg_color="#7F1D1D")
        self.breaker_status.configure(text="OPEN", text_color="#EF4444", fg_color="#7F1D1D")
        self.fault_status.configure(text="FAULT DETECTED", text_color="#EF4444", fg_color="#7F1D1D")

    def handle_reset(self):
        self.relay_status.configure(text="HEALTHY", text_color="#22C55E", fg_color="#064E3B")
        self.breaker_status.configure(text="CLOSED", text_color="#22C55E", fg_color="#064E3B")
        self.fault_status.configure(text="NO FAULTS", text_color="#22C55E", fg_color="#064E3B")

    def setup_file_watchers(self):
        # Create an event handler and observer
        event_handler = CSVFileHandler(self)
        self.observer = Observer()
        
        # Watch Input folder
        input_path = 'Input Real Time Data'
        self.observer.schedule(event_handler, input_path, recursive=False)
        
        # Watch Output folder
        output_path = 'Output Real Time Data'
        self.observer.schedule(event_handler, output_path, recursive=False)
        
        # Start the observer in a separate thread
        self.observer.start()

    def update_from_files(self):
        try:
            input_file_path = os.path.join('Input Real Time Data', 'Real-time data for GUI.csv')
            output_file_path = os.path.join('Output Real Time Data', 'Real-time data for GUI.csv')
            
            # Read input data
            with open(input_file_path, 'r') as file:
                input_lines = file.readlines()
                if len(input_lines) > 1:
                    input_data = input_lines[-1].strip().split(',')
            
            # Read output data
            with open(output_file_path, 'r') as file:
                output_lines = file.readlines()
                if len(output_lines) > 1:
                    output_data = output_lines[-1].strip().split(',')
            
            config = self.config_menu.get()
            
            # Update measurements based on configuration
            if config == "Three phase AC to Three phase AC":
                self.update_three_phase_values(input_data, output_data)
            elif config == "DC to Three phase AC":
                self.update_dc_to_three_phase_values(input_data, output_data)
            elif config == "Three phase AC to DC":
                self.update_three_phase_to_dc_values(input_data, output_data)
            elif config == "DC to DC":
                self.update_dc_values(input_data, output_data)
            elif config == "Single Phase AC to DC":
                self.update_single_phase_to_dc_values(input_data, output_data)
            elif config == "DC to Single Phase AC":
                self.update_dc_to_single_phase_values(input_data, output_data)
            elif config == "Single Phase AC to Single Phase AC":
                self.update_single_phase_values(input_data, output_data)
            
            # Update common metrics using input data
            self.frequency.configure(text=f"{float(input_data[19]):.2f} Hz")
            self.temperature.configure(text=f"{float(input_data[21]):.2f} °C")
                    
            # Update energy panel with current phase
            self.update_energy_values()
        
        except Exception as e:
            print(f"Error updating values: {e}")

    def start_updates(self):
        # Initial update
        self.update_from_files()

    def __del__(self):
        # Stop the observer when the dashboard is destroyed
        if hasattr(self, 'observer'):
            self.observer.stop()
            self.observer.join()

    def create_measurement_panels(self):
        # Create frame for measurement panels
        measurements_frame = ctk.CTkFrame(
            self.main_container,
            fg_color="transparent",
            border_width=0
        )
        measurements_frame.pack(fill="x", pady=(0, 25), padx=0)
        
        # Configure grid
        measurements_frame.grid_columnconfigure(0, weight=1)
        measurements_frame.grid_columnconfigure(1, weight=1)
        measurements_frame.grid_rowconfigure(0, weight=1)
        
        # Store frames as instance variables
        self.input_frame = self.create_measurement_frame(measurements_frame, "Input Measurements", 0)
        self.output_frame = self.create_measurement_frame(measurements_frame, "Output Measurements", 1)
        
        # Initialize measurement labels dictionary
        self.measurement_labels = {}
        
        # Set up configuration change callback
        self.config_menu.configure(command=self.update_measurements_for_config)
        
        # Initial setup based on default configuration
        self.update_measurements_for_config(self.config_menu.get())

    def create_measurement_frame(self, parent, title, column):
        frame = ctk.CTkFrame(
            parent,
            fg_color="#1E293B",
            corner_radius=15,
            border_width=1,
            border_color="#334155"
        )
        frame.grid(row=0, column=column, sticky="nsew", padx=(0 if column == 0 else 10, 10 if column == 0 else 0), ipadx=20, ipady=10)
        
        # Title and button container
        header_frame = ctk.CTkFrame(frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=25, pady=(20, 15))
        
        # Title
        title_label = ctk.CTkLabel(
            header_frame,
            text=title,
            font=(self.font_family_bold, 18),
            text_color="#F1F5F9"
        )
        title_label.pack(side="left")
        
        # View Details button
        view_button = ctk.CTkButton(
            header_frame,
            text="View Details",
            font=(self.font_family, 14),
            fg_color="#3B82F6",
            hover_color="#2563EB",
            height=32,
            width=100,
            corner_radius=8,
            command=lambda: self.show_details_window(title)
        )
        view_button.pack(side="right")
        
        return frame

    def show_details_window(self, panel_type):
        # Create a new window
        details_window = ctk.CTkToplevel(self)
        details_window.title(f"{panel_type} Details")
        details_window.geometry("800x600")
        details_window.configure(fg_color="#0F172A")
        
        # Make window modal
        details_window.transient(self)
        details_window.grab_set()
        
        # Create scrollable frame for content
        content_frame = ctk.CTkScrollableFrame(
            details_window,
            fg_color="transparent",
            corner_radius=0
        )
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title = ctk.CTkLabel(
            content_frame,
            text=f"{panel_type} Details",
            font=(self.font_family_bold, 24),
            text_color="#F1F5F9"
        )
        title.pack(pady=(0, 20))
        
        # Create sections based on panel type
        if "Input" in panel_type:
            self.create_details_section(content_frame, "Voltage Measurements", [
                "RMS Voltage",
                "Peak Voltage",
                "Average Voltage",
                "THD Voltage",
                "Fundamental Voltage",
                "Phase Angle"
            ])
            
            self.create_details_section(content_frame, "Current Measurements", [
                "RMS Current",
                "Peak Current",
                "Average Current",
                "THD Current",
                "Fundamental Current",
                "Phase Angle"
            ])
            
            self.create_details_section(content_frame, "Power Quality", [
                "Power Factor",
                "Displacement Power Factor",
                "True Power Factor",
                "Voltage Unbalance",
                "Current Unbalance",
                "Frequency"
            ])
        else:  # Output measurements
            self.create_details_section(content_frame, "Output Parameters", [
                "Output Voltage",
                "Output Current",
                "Output Power",
                "Efficiency",
                "Power Loss",
                "Temperature"
            ])
            
            self.create_details_section(content_frame, "Protection Status", [
                "Overcurrent Protection",
                "Overvoltage Protection",
                "Temperature Protection",
                "Short Circuit Protection",
                "Ground Fault Protection",
                "System Status"
            ])
        
        # Close button
        close_button = ctk.CTkButton(
            details_window,
            text="Close",
            font=(self.font_family, 14),
            fg_color="#EF4444",
            hover_color="#DC2626",
            height=36,
            command=details_window.destroy
        )
        close_button.pack(pady=20, padx=20)

    def create_details_section(self, parent, title, parameters):
        # Section frame
        section_frame = ctk.CTkFrame(
            parent,
            fg_color="#1E293B",
            corner_radius=15,
            border_width=1,
            border_color="#334155"
        )
        section_frame.pack(fill="x", pady=10, padx=5)
        
        # Section title
        title_label = ctk.CTkLabel(
            section_frame,
            text=title,
            font=(self.font_family_bold, 18),
            text_color="#F1F5F9"
        )
        title_label.pack(padx=20, pady=(15, 10))
        
        # Parameters
        for param in parameters:
            param_frame = ctk.CTkFrame(
                section_frame,
                fg_color="#162234",
                corner_radius=12
            )
            param_frame.pack(fill="x", padx=20, pady=5)
            
            param_label = ctk.CTkLabel(
                param_frame,
                text=param,
                font=(self.font_family, 14),
                text_color="#94A3B8"
            )
            param_label.pack(side="left", padx=15, pady=12)
            
            value_container = ctk.CTkFrame(
                param_frame,
                fg_color="#1E293B",
                corner_radius=8
            )
            value_container.pack(side="right", padx=15, pady=8)
            
            value_label = ctk.CTkLabel(
                value_container,
                text="0.00",
                font=(self.font_family_bold, 14),
                text_color="#F1F5F9"
            )
            value_label.pack(padx=12, pady=4)

    def update_measurements_for_config(self, config):
        # Clear existing measurements
        for widget in self.input_frame.winfo_children()[1:]:  # Skip title
            widget.destroy()
        for widget in self.output_frame.winfo_children()[1:]:  # Skip title
            widget.destroy()
        
        self.measurement_labels = {}
        
        # Update configuration status in relay indication panel
        self.config_status.configure(text=config, text_color="#3B82F6", fg_color="#1E3A8A")
        
        # Configure measurements based on selected configuration
        if config == "Three phase AC to Three phase AC":
            self.create_three_phase_measurements(self.input_frame, "Input")
            self.create_three_phase_measurements(self.output_frame, "Output")
        
        elif config == "DC to Three phase AC":
            self.create_dc_measurements(self.input_frame, "Input")
            self.create_three_phase_measurements(self.output_frame, "Output")
        
        elif config == "Three phase AC to DC":
            self.create_three_phase_measurements(self.input_frame, "Input")
            self.create_dc_measurements(self.output_frame, "Output")
        
        elif config == "DC to DC":
            self.create_dc_measurements(self.input_frame, "Input")
            self.create_dc_measurements(self.output_frame, "Output")
        
        elif config == "Single Phase AC to DC":
            self.create_single_phase_measurements(self.input_frame, "Input")
            self.create_dc_measurements(self.output_frame, "Output")
        
        elif config == "DC to Single Phase AC":
            self.create_dc_measurements(self.input_frame, "Input")
            self.create_single_phase_measurements(self.output_frame, "Output")
        
        elif config == "Single Phase AC to Single Phase AC":
            self.create_single_phase_measurements(self.input_frame, "Input")
            self.create_single_phase_measurements(self.output_frame, "Output")

    def create_three_phase_measurements(self, parent, prefix):
        voltage_labels = self.create_measurement_values(parent, "Voltage", ["Phase A", "Phase B", "Phase C"])
        current_labels = self.create_measurement_values(parent, "Current", ["Phase A", "Phase B", "Phase C"])
        
        # Update labels dictionary with prefix
        for key, label in voltage_labels.items():
            self.measurement_labels[f"{prefix}_{key}"] = label
        for key, label in current_labels.items():
            self.measurement_labels[f"{prefix}_{key}"] = label

    def create_dc_measurements(self, parent, prefix):
        voltage_label = self.create_measurement_values(parent, "Voltage", ["DC"])
        current_label = self.create_measurement_values(parent, "Current", ["DC"])
        
        self.measurement_labels[f"{prefix}_Voltage_DC"] = voltage_label["Voltage_DC"]
        self.measurement_labels[f"{prefix}_Current_DC"] = current_label["Current_DC"]

    def create_single_phase_measurements(self, parent, prefix):
        voltage_label = self.create_measurement_values(parent, "Voltage", ["AC"])
        current_label = self.create_measurement_values(parent, "Current", ["AC"])
        
        self.measurement_labels[f"{prefix}_Voltage_AC"] = voltage_label["Voltage_AC"]
        self.measurement_labels[f"{prefix}_Current_AC"] = current_label["Current_AC"]

    def create_measurement_values(self, parent, title, phases):
        # Create frame for measurement type with increased width
        measure_frame = ctk.CTkFrame(parent, fg_color="transparent")
        measure_frame.pack(fill="x", padx=25, pady=5)  # Increased padding

        # Add title with more space
        measure_title = ctk.CTkLabel(
            measure_frame,
            text=title,
            font=(self.font_family, 14),
            text_color="#94A3B8"
        )
        measure_title.pack(anchor="w", pady=(10, 5))

        # Dictionary to store value labels
        value_labels = {}

        # Add phase measurements with increased spacing
        for phase in phases:
            phase_frame = ctk.CTkFrame(
                measure_frame,
                fg_color="#162234",  # Changed to match status items
                corner_radius=12
            )
            phase_frame.pack(fill="x", pady=3)

            phase_label = ctk.CTkLabel(
                phase_frame,
                text=phase,
                font=(self.font_family, 13),
                text_color="#94A3B8"
            )
            phase_label.pack(side="left", padx=15, pady=8)  # Increased padding

            value_label = ctk.CTkLabel(
                phase_frame,
                text="0.00",
                font=(self.font_family_bold, 13),
                text_color="#F1F5F9"
            )
            value_label.pack(side="right", padx=15, pady=8)  # Increased padding
            
            value_labels[f"{title}_{phase}"] = value_label

        return value_labels

    def animate_pulse(self, parent, color):
        # Create pulse indicator directly without frame
        pulse_indicator = ctk.CTkLabel(
            parent,
            text="●",
            font=(self.font_family, 16),
            text_color=color,
            width=24,
            height=24
        )
        pulse_indicator.pack(side="left", padx=(15, 10))

        def pulse():
            pulse_indicator.configure(text_color=color)
            self.after(1000, lambda: pulse_indicator.configure(text_color="#1E293B"))
            self.after(2000, pulse)

        pulse()

    # Add these helper methods for updating values
    def update_three_phase_values(self, input_data, output_data):
        # Input values
        for phase, idx in [('A', 1), ('B', 7), ('C', 13)]:
            self.measurement_labels[f'Input_Voltage_Phase {phase}'].configure(text=f"{float(input_data[idx]):.2f} V")
            self.measurement_labels[f'Input_Current_Phase {phase}'].configure(text=f"{float(input_data[idx+1]):.2f} A")
        
        # Output values from output data file
        for phase, idx in [('A', 1), ('B', 7), ('C', 13)]:
            self.measurement_labels[f'Output_Voltage_Phase {phase}'].configure(text=f"{float(output_data[idx]):.2f} V")
            self.measurement_labels[f'Output_Current_Phase {phase}'].configure(text=f"{float(output_data[idx+1]):.2f} A")

    def update_dc_values(self, input_data, output_data):
        # Update DC input from input data
        self.measurement_labels['Input_Voltage_DC'].configure(text=f"{float(input_data[20]):.2f} V")
        self.measurement_labels['Input_Current_DC'].configure(text=f"{float(input_data[21]):.2f} A")
        
        # Update DC output from output data
        self.measurement_labels['Output_Voltage_DC'].configure(text=f"{float(output_data[20]):.2f} V")
        self.measurement_labels['Output_Current_DC'].configure(text=f"{float(output_data[21]):.2f} A")

    def update_dc_to_three_phase_values(self, input_data, output_data):
        # Input DC values
        self.measurement_labels['Input_Voltage_DC'].configure(text=f"{float(input_data[20]):.2f} V")
        self.measurement_labels['Input_Current_DC'].configure(text=f"{float(input_data[21]):.2f} A")
        
        # Output three-phase values
        for phase, idx in [('A', 1), ('B', 7), ('C', 13)]:
            self.measurement_labels[f'Output_Voltage_Phase {phase}'].configure(text=f"{float(output_data[idx]):.2f} V")
            self.measurement_labels[f'Output_Current_Phase {phase}'].configure(text=f"{float(output_data[idx+1]):.2f} A")

    def update_three_phase_to_dc_values(self, input_data, output_data):
        # Input three-phase values
        for phase, idx in [('A', 1), ('B', 7), ('C', 13)]:
            self.measurement_labels[f'Input_Voltage_Phase {phase}'].configure(text=f"{float(input_data[idx]):.2f} V")
            self.measurement_labels[f'Input_Current_Phase {phase}'].configure(text=f"{float(input_data[idx+1]):.2f} A")
        
        # Output DC values
        self.measurement_labels['Output_Voltage_DC'].configure(text=f"{float(output_data[20]):.2f} V")
        self.measurement_labels['Output_Current_DC'].configure(text=f"{float(output_data[21]):.2f} A")

    def update_single_phase_values(self, input_data, output_data):
        # Input single-phase values (using phase A values)
        self.measurement_labels['Input_Voltage_AC'].configure(text=f"{float(input_data[1]):.2f} V")
        self.measurement_labels['Input_Current_AC'].configure(text=f"{float(input_data[2]):.2f} A")
        
        # Output single-phase values
        self.measurement_labels['Output_Voltage_AC'].configure(text=f"{float(output_data[1]):.2f} V")
        self.measurement_labels['Output_Current_AC'].configure(text=f"{float(output_data[2]):.2f} A")

    def update_single_phase_to_dc_values(self, input_data, output_data):
        # Input single-phase values
        self.measurement_labels['Input_Voltage_AC'].configure(text=f"{float(input_data[1]):.2f} V")
        self.measurement_labels['Input_Current_AC'].configure(text=f"{float(input_data[2]):.2f} A")
        
        # Output DC values
        self.measurement_labels['Output_Voltage_DC'].configure(text=f"{float(output_data[20]):.2f} V")
        self.measurement_labels['Output_Current_DC'].configure(text=f"{float(output_data[21]):.2f} A")

    def update_dc_to_single_phase_values(self, input_data, output_data):
        # Input DC values
        self.measurement_labels['Input_Voltage_DC'].configure(text=f"{float(input_data[20]):.2f} V")
        self.measurement_labels['Input_Current_DC'].configure(text=f"{float(input_data[21]):.2f} A")
        
        # Output single-phase values
        self.measurement_labels['Output_Voltage_AC'].configure(text=f"{float(output_data[1]):.2f} V")
        self.measurement_labels['Output_Current_AC'].configure(text=f"{float(output_data[2]):.2f} A")

    def update_energy_values(self, selected_phase=None):
        try:
            input_file_path = os.path.join('Input Real Time Data', 'Real-time data for GUI.csv')
            
            with open(input_file_path, 'r') as file:
                lines = file.readlines()
                if len(lines) > 1:
                    data = lines[-1].strip().split(',')
                    
                    # Get indices based on selected phase
                    phase_indices = {
                        "Phase A": (3, 4, 5, 6),    # Active, Reactive, Apparent, PF for Phase A
                        "Phase B": (9, 10, 11, 12),  # Active, Reactive, Apparent, PF for Phase B
                        "Phase C": (15, 16, 17, 18)  # Active, Reactive, Apparent, PF for Phase C
                    }
                    
                    selected = self.phase_selector.get()
                    indices = phase_indices[selected]
                    
                    # Update energy metrics for selected phase
                    self.active_energy.configure(text=f"{float(data[indices[0]]):.2f} kW")
                    self.reactive_energy.configure(text=f"{float(data[indices[1]]):.2f} kVAR")
                    self.apparent_power.configure(text=f"{float(data[indices[2]]):.2f} kVA")
                    self.power_factor.configure(text=f"{float(data[indices[3]]):.2f}")
                    
                    # These values are common for all phases
                    self.frequency.configure(text=f"{float(data[19]):.2f} Hz")
                    self.temperature.configure(text=f"{float(data[21]):.2f} °C")
                    
        except Exception as e:
            print(f"Error updating energy values: {e}")

    def create_options_panel(self):
        # Create options panel frame
        options_frame = ctk.CTkFrame(
            self.main_container,
            fg_color="#1E293B",
            corner_radius=15,
            border_width=1,
            border_color="#334155"
        )
        options_frame.pack(fill="x", pady=(0, 20))

        # Header
        header_frame = ctk.CTkFrame(options_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=15, pady=(15, 10))

        header_label = ctk.CTkLabel(
            header_frame,
            text="Options",
            font=(self.font_family_bold, 18),
            text_color="#F1F5F9"
        )
        header_label.pack(side="left")

        # Buttons container with grid layout
        buttons_frame = ctk.CTkFrame(options_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=15, pady=(0, 15))

        # Configure grid columns with equal weight
        buttons_frame.grid_columnconfigure(0, weight=1)
        buttons_frame.grid_columnconfigure(1, weight=1)
        buttons_frame.grid_columnconfigure(2, weight=1)

        # Options buttons with icons
        options = [
            ("⚙️", "Settings", self.show_settings),
            ("📊", "Self Diagnosis Test", lambda: print("Diagnosis")),
            ("📖", "Instruction Manual", lambda: print("Manual")),
            ("ℹ️", "About Us", lambda: print("About"))
        ]

        # Create buttons in grid layout
        for idx, (icon, label, command) in enumerate(options):
            row = idx // 3
            col = idx % 3
            
            button = ctk.CTkButton(
                buttons_frame,
                text=f"{icon}  {label}",
                font=(self.font_family, 14),
                fg_color="#2563EB",
                hover_color="#1D4ED8",
                height=36,
                corner_radius=8,
                command=command
            )
            button.grid(row=row, column=col, padx=5, pady=5, sticky="ew")

    def show_settings(self):
        # Hide current dashboard
        self.pack_forget()
        
        # Create and show settings page
        self.settings_page = SettingsPage(
            self.parent, 
            self.font_family, 
            self.return_to_dashboard  # Changed to use the new method name
        )
        self.settings_page.pack(fill="both", expand=True)

    def return_to_dashboard(self):  # Renamed for clarity
        # Hide settings page
        if hasattr(self, 'settings_page'):
            self.settings_page.pack_forget()
            self.settings_page.destroy()
        
        # Show dashboard again
        self.pack(fill="both", expand=True)
