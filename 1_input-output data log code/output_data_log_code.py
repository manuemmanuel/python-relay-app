import serial
import csv
from datetime import datetime
import time
import os

# Configuration
SERIAL_PORT = '/dev/ttyACM0'  # Changed to COM9
BAUD_RATE = 115200
BASE_DIR = "/home/rahul/Desktop/Project"

# Updated output folder names
MAIN_LOG_DIR = os.path.join(BASE_DIR, "Output Data Log")  # Changed to Output Data Log
REALTIME_DIR = os.path.join(BASE_DIR, "Output Real Time Data")  # Changed to Output Real Time Data

# Real-time files
REALTIME_FILES = {
    "GUI": os.path.join(REALTIME_DIR, "Real-time data for GUI.csv"),
    "RELAY": os.path.join(REALTIME_DIR, "Real-time data for relay.csv")
}

def create_csv_file():
    """Create main log file with timestamp in 'Output Data Log' folder"""
    os.makedirs(MAIN_LOG_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
    return os.path.join(MAIN_LOG_DIR, f"power_log_{timestamp}.csv")

def write_realtime_files(headers, data):
    """Write to real-time files in 'Output Real Time Data' folder"""
    os.makedirs(REALTIME_DIR, exist_ok=True)
    
    for file_path in REALTIME_FILES.values():
        with open(file_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerow(data)

def main():
    csv_file = create_csv_file()
    headers = [
        "Computer_TS",
        "A Phase Voltage", "A Phase Current", "A Phase Active Power", "A Phase Reactive Power", 
        "A Phase Apparent Power", "A Power Factor",
        "B Phase Voltage", "B Phase Current", "B Phase Active Power", "B Phase Reactive Power", 
        "B Phase Apparent Power", "B Power Factor",
        "C Phase Voltage", "C Phase Current", "C Phase Active Power", "C Phase Reactive Power", 
        "C Phase Apparent Power", "C Power Factor",
        "Frequency", "DC Voltage", "DC Current", "Temperature"
    ]
    
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0.001)
        time.sleep(2)
        print(f"Connected to {SERIAL_PORT} at {BAUD_RATE} baud")
    except serial.SerialException as e:
        print(f"Serial error: {e}")
        return

    with open(csv_file, 'w', newline='') as f:
        csv.writer(f).writerow(headers)
    print(f"Main log file: {csv_file}")
    print(f"Real-time files location: {REALTIME_DIR}")

    print("Logging started. Press CTRL+C to stop.")
    
    try:
        while True:
            if ser.in_waiting:
                line = ser.readline().decode(errors='ignore').strip()
                
                if line:
                    data = line.split(',')
                    
                    if len(data) == 22:
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                        full_data = [timestamp] + data

                        with open(csv_file, 'a', newline='') as f:
                            csv.writer(f).writerow(full_data)

                        write_realtime_files(headers, full_data)
                        print(f"Updated @ {timestamp}")
                    else:
                        print(f"Ignored partial data: {line}")

            time.sleep(0.001)
            
    except KeyboardInterrupt:
        print("\nLogging stopped")
    finally:
        ser.close()
        print("Serial port closed")

if __name__ == "__main__":
    main()
