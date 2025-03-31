import serial
import csv
from datetime import datetime
import time
import os

# Configuration
SERIAL_PORT = '/dev/ttyUSB0' #  /dev/ttyACM0
BAUD_RATE = 115200
BASE_DIR =  "/home/rahul/Desktop/Project" # Base project directory

# Updated folder names
MAIN_LOG_DIR = os.path.join(BASE_DIR, "Output Data Log")  # For main log files
REALTIME_DIR = os.path.join(BASE_DIR, "Output Real Time Data")  # For real-time files

# Real-time files
REALTIME_FILES = {
    "GUI": os.path.join(REALTIME_DIR, "Real-time data for GUI.csv"),
    "RELAY": os.path.join(REALTIME_DIR, "Real-time data for relay.csv")
}

def create_csv_file():
    """Create main log file with timestamp in 'Input Data Log' folder"""
    os.makedirs(MAIN_LOG_DIR, exist_ok=True)  # Ensure directory exists
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
    return os.path.join(MAIN_LOG_DIR, f"power_log_{timestamp}.csv")

def write_realtime_files(headers, data):
    """Write to both real-time files in 'Input Real Time Data' folder"""
    os.makedirs(REALTIME_DIR, exist_ok=True)  # Ensure directory exists
    
    for file_path in REALTIME_FILES.values():
        with open(file_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerow(data)

def main():
    # Create main log file in 'Input Data Log'
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
    
    # Initialize serial connection
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0.001)
        time.sleep(2)
        print(f"Connected to {SERIAL_PORT} at {BAUD_RATE} baud")
    except serial.SerialException as e:
        print(f"Serial error: {e}")
        return

    # Initialize main log file
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

                        # Write to main log
                        with open(csv_file, 'a', newline='') as f:
                            csv.writer(f).writerow(full_data)

                        # Update real-time files
                        write_realtime_files(headers, full_data)
                        
                        print(f"Updated @ {timestamp}")
                    else:
                        print(f"Ignored partial data: {line}")

            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nLogging stopped")
    finally:
        ser.close()
        print("Serial port closed")

if __name__ == "__main__":
    main()
