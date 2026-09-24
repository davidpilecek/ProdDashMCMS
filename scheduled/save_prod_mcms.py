from metris import connect
from utils import read_tag_value, read_tag_string, write_tag_value, write_tag_string

import datetime
import csv
from pathlib import Path
import os

# Directory containing this script
SCRIPT_DIR = Path(__file__).resolve().parent

DATA_DIR = (
    Path(os.environ.get("PROGRAMDATA", Path.home()))
    / "ANDRITZ"
    / "ProdDashMCMS"
    / "data"
)

hc, cc, dac = connect()

def save_batch():
    
    current_update_date = read_tag_string(cc, hc, "MCMS-Current_Date")
    current_dataset_name = read_tag_string(cc, hc, "MCMS-Current_Dataset_Name")

    filename = DATA_DIR / datetime.datetime.now().strftime("%m%Y_PROD_LIST.csv")

    prod_id = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
    
    batch_recipe = current_dataset_name

    prod_descr = f"N/A"

    file_exists = os.path.exists(filename)
    
    with open(filename, "a", newline="") as f:
        writer = csv.writer(f)
    
        if not file_exists:
            writer.writerow([
                "PROD_ID",
                "PROD_NUM",
                "PROD_DESC",
                "RECIPE_NAME"
            ])
    
        writer.writerow([
            prod_id,
            prod_id,
            prod_descr,
            batch_recipe
        ])

    timedate_now = datetime.datetime.now().astimezone().isoformat()
      
    write_tag_string(cc, hc, "MCMS-Last_Date", current_update_date, timedate_now)
    
    print("Batch Saved")
        
if __name__ == "__main__":
    save_batch()