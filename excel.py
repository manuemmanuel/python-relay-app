import os
import time
import pandas as pd
from supabase import create_client, Client
from dotenv import load_dotenv
import logging
from openpyxl import load_workbook

# Configure logging with more detailed format
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

def update_parameters(xlsx_path):
    try:
        # Get data from Supabase parameters_table
        result = supabase.table('parameters_table').select('*').execute()
        
        if not result.data:
            logger.warning("No data found in parameters_table")
            return
        
        # Create dictionary of parameters and values from Supabase
        supabase_params = {item['parameter'].strip(): item['value'] for item in result.data}
        
        # Load Excel workbook
        wb = load_workbook(xlsx_path)
        ws = wb.active
        
        # Track updated parameters with their old and new values
        updates = []
        
        # Skip the header row (row 1) and start from row 2
        for row in range(2, ws.max_row + 1):
            # Get parameter name from column A
            param = ws[f'A{row}'].value
            if param:
                param = param.strip()  # Remove any whitespace
                
                if param in supabase_params:
                    # Get current Excel value and Supabase value
                    excel_value = ws[f'B{row}'].value
                    supabase_value = supabase_params[param]
                    
                    # Convert values to integers for comparison
                    try:
                        excel_value = int(float(excel_value)) if excel_value is not None else 0
                        supabase_value = int(float(supabase_value)) if supabase_value is not None else 0
                        
                        # Update if values are different
                        if excel_value != supabase_value:
                            ws[f'B{row}'].value = supabase_value
                            updates.append({
                                'parameter': param,
                                'old_value': excel_value,
                                'new_value': supabase_value,
                                'row': row
                            })
                    except (ValueError, TypeError) as e:
                        logger.error(f"Error converting values for parameter {param}: {str(e)}")
                        continue
        
        # Save if there were any updates
        if updates:
            wb.save(xlsx_path)
            logger.info("\nUpdated parameters:")
            for update in updates:
                logger.info(f"  Row {update['row']}: {update['parameter']}")
                logger.info(f"    Old value: {update['old_value']}")
                logger.info(f"    New value: {update['new_value']}")
        else:
            logger.info("No updates needed - all parameters are current")
            
    except Exception as e:
        logger.error(f"Error updating parameters: {str(e)}")
        logger.error("Full error details:", exc_info=True)

def main():
    xlsx_path = "User Data Input.xlsx"
    logger.info(f"Starting parameter update service for {xlsx_path}")
    logger.info("Monitoring for parameter changes...")
    
    try:
        while True:
            update_parameters(xlsx_path)
            time.sleep(1)  # Check every second
    except KeyboardInterrupt:
        logger.info("Stopping parameter update service")

if __name__ == "__main__":
    main()