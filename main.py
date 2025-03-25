import os
import time
import pandas as pd
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from supabase import create_client, Client
from dotenv import load_dotenv
import logging
from excel_updater import run_excel_updater

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize Supabase client
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

class CSVHandler(FileSystemEventHandler):
    def __init__(self):
        self.last_modified = 0
        self.last_hash = None

    def on_modified(self, event):
        if event.is_directory or not event.src_path.endswith('Real-time data for GUI.csv'):
            return

        try:
            # Read the CSV file
            df = pd.read_csv(event.src_path)
            
            # Get the latest row as a copy
            latest_row = df.iloc[-1:].copy()
            
            # Convert timestamp
            latest_row.loc[latest_row.index[0], 'Computer_TS'] = pd.to_datetime(latest_row['Computer_TS'].iloc[0])
            
            # Determine which table to use based on the file path
            is_input = 'Input Real Time Data' in event.src_path
            table_name = 'input_real_time_data' if is_input else 'output_real_time_data'
            
            # Convert to dict and clean NaN values
            data = {
                'computer_ts': latest_row['Computer_TS'].iloc[0].isoformat(),
                'A Phase Voltage': float(latest_row['A Phase Voltage'].iloc[0]),
                'A Phase Current': float(latest_row['A Phase Current'].iloc[0]),
                'A Phase Active Power': float(latest_row['A Phase Active Power'].iloc[0]),
                'A Phase Reactive Power': float(latest_row['A Phase Reactive Power'].iloc[0]),
                'A Phase Apparent Power': float(latest_row['A Phase Apparent Power'].iloc[0]),
                'A Power Factor': float(latest_row['A Power Factor'].iloc[0]),
                'B Phase Voltage': float(latest_row['B Phase Voltage'].iloc[0]),
                'B Phase Current': float(latest_row['B Phase Current'].iloc[0]),
                'B Phase Active Power': float(latest_row['B Phase Active Power'].iloc[0]),
                'B Phase Reactive Power': float(latest_row['B Phase Reactive Power'].iloc[0]),
                'B Phase Apparent Power': float(latest_row['B Phase Apparent Power'].iloc[0]),
                'B Power Factor': float(latest_row['B Power Factor'].iloc[0]),
                'C Phase Voltage': float(latest_row['C Phase Voltage'].iloc[0]),
                'C Phase Current': float(latest_row['C Phase Current'].iloc[0]),
                'C Phase Active Power': float(latest_row['C Phase Active Power'].iloc[0]),
                'C Phase Reactive Power': float(latest_row['C Phase Reactive Power'].iloc[0]),
                'C Phase Apparent Power': float(latest_row['C Phase Apparent Power'].iloc[0]),
                'C Power Factor': float(latest_row['C Power Factor'].iloc[0]),
                'Frequency': float(latest_row['Frequency'].iloc[0]),
                'DC Voltage': float(latest_row['DC Voltage'].iloc[0]),
                'DC Current': float(latest_row['DC Current'].iloc[0]),
                'Temperature': float(latest_row['Temperature'].iloc[0])
            }

            try:
                # First, get all existing rows
                result = supabase.table(table_name).select('id').execute()
                
                if result.data:
                    # If rows exist, update the first one
                    row_id = result.data[0]['id']
                    supabase.table(table_name).update(data).eq('id', row_id).execute()
                    logger.info(f"Updated existing row in {table_name} with timestamp: {data['computer_ts']}")
                else:
                    # If no rows exist, insert new row
                    result = supabase.table(table_name).insert(data).execute()
                    logger.info(f"Inserted new row in {table_name} with timestamp: {data['computer_ts']}")
                
            except Exception as e:
                logger.error(f"Error updating Supabase table {table_name}: {str(e)}")
            
        except Exception as e:
            logger.error(f"Error processing file {event.src_path}: {str(e)}")

def main():
    # Start Excel updater in a separate thread
    excel_thread = run_excel_updater()
    
    # Create event handler for CSV monitoring
    event_handler = CSVHandler()
    
    # Create observer
    observer = Observer()
    
    # Get absolute paths for both directories
    input_dir = os.path.abspath('Input Real Time Data')
    output_dir = os.path.abspath('Output Real Time Data')
    
    # Schedule monitoring for both directories
    observer.schedule(event_handler, input_dir, recursive=False)
    observer.schedule(event_handler, output_dir, recursive=False)
    
    # Start the observer
    observer.start()
    logger.info(f"Started monitoring directories:\n{input_dir}\n{output_dir}")
    
    try:
        while True:
            time.sleep(0.01)  # Check every 10ms
    except KeyboardInterrupt:
        observer.stop()
        logger.info("Stopping monitoring.")
    
    observer.join()

if __name__ == "__main__":
    main()
