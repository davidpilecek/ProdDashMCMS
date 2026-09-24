
import datetime

from utils import read_tag_value, read_tag_string, write_tag_value, write_tag_string
from metris import connect

from save_prod_mcms import save_batch
from save_segment_mcms import save_segment

# ----------------------------
# Metris connection
# ----------------------------

def check_change():

    hc, cc, dac = connect()

    event = None
    code = 0
    
    # 1. Day rollover check
    curr_day = float(datetime.datetime.now().strftime("%d"))
    last_day = read_tag_value(cc, hc, "MCMS-Last_Day")

    # 2. Check if the current recipe edit date is different from the last recipe edit date 
    current_update_date = read_tag_string(cc, hc, "MCMS-Current_Date")
    last_update_date = read_tag_string(cc, hc, "MCMS-Last_Date")

    if curr_day != last_day:
        event = "DAY_ROLLOVER"
        code = 2
        write_tag_value(cc, hc, "MCMS-Last_Day", curr_day, datetime.datetime.now().astimezone().isoformat())

    if current_update_date != "" and current_update_date != last_update_date:
        event = "RECIPE_CHANGED"
        code = 1

    return event, code

# ----------------------------
# Check for changes and run batch files accordingly
# ----------------------------

if __name__ == "__main__":
    
    event, code = check_change()

    if event == "RECIPE_CHANGED":
        save_batch()

    if code != 0:
        save_segment(event)