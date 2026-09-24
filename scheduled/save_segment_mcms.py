# TODO:
# 
# Change calculate tag arguments, change and test check_update.py function
# Change and test paths on deployment pc

from metris import connect
from utils import read_tag_value, read_tag_string, write_tag_value

import datetime
from datetime import timedelta
import csv
from pathlib import Path
import os
import sys

# Directory containing this script
SCRIPT_DIR = Path(__file__).resolve().parent

DATA_DIR = (
    Path(os.environ.get("PROGRAMDATA", Path.home()))
    / "ANDRITZ"
    / "ProdDashMCMS"
    / "data"
)

hc, cc, dac = connect()

prod_filename = DATA_DIR / datetime.datetime.now().strftime("%m%Y_PROD_LIST.csv")
segment_filename = DATA_DIR / datetime.datetime.now().strftime("%m%Y_PROD_SEGMENT.csv")

mass_prod_total = read_tag_value(cc, hc, "MCMS_PROD_TOTAL")
add1_total = read_tag_value(cc, hc, "MCMS_ADDITIVE1_TOTAL")
add2_total = read_tag_value(cc, hc, "MCMS_ADDITIVE2_TOTAL")
add3_total = read_tag_value(cc, hc, "MCMS_ADDITIVE3_TOTAL")
add4_total = read_tag_value(cc, hc, "MCMS_ADDITIVE4_TOTAL")
add5_total = read_tag_value(cc, hc, "MCMS_ADDITIVE5_TOTAL")
total_incl_additives = read_tag_value(cc, hc, "MCMS_TOTAL_PROD_INCL_ADDITIVES")
add1_percent = read_tag_value(cc, hc, "MCMS_TOTAL_ADDITIVE1_PERCENT")
add2_percent = read_tag_value(cc, hc, "MCMS_TOTAL_ADDITIVE2_PERCENT")
add3_percent = read_tag_value(cc, hc, "MCMS_TOTAL_ADDITIVE3_PERCENT")
add4_percent = read_tag_value(cc, hc, "MCMS_TOTAL_ADDITIVE4_PERCENT")
add5_percent = read_tag_value(cc, hc, "MCMS_TOTAL_ADDITIVE5_PERCENT")
segment_runtime = read_tag_value(cc, hc, "MCMS_SEGMENT_RUNTIME")

header = [
    "SEGMENT_ID",
    "PROD_ID",
    "USR_ID",
    "START_TIME",
    "STOP_TIME",
    "RUN_TIME",
    "MASS_TOTAL",
    "ADD1_TOTAL",
    "ADD2_TOTAL",
    "ADD3_TOTAL",
    "ADD4_TOTAL",
    "ADD5_TOTAL",
    "TOTAL_INCL_ADDITIVES",
    "ADD1_PERCENT",
    "ADD2_PERCENT",
    "ADD3_PERCENT",
    "ADD4_PERCENT",
    "ADD5_PERCENT"
                ]

def create_new_segment(fieldnames, segment_filename, segment_id, usr_id, prod_id, start_time, segment_file_exists):

    with open(segment_filename, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not segment_file_exists:
            writer.writeheader()
        elif segment_filename.stat().st_size == 0:
            writer.writeheader()

        writer.writerow({
            "SEGMENT_ID": segment_id,
            "USR_ID": usr_id,
            "PROD_ID": prod_id,
            "START_TIME": start_time
        })

def get_segment_file_to_close(current_file: Path) -> Path:
    """
    Returns the file containing the currently open segment.
    Normally this is the current month's file.
    During a month rollover, it may be the previous month's file.
    """

    # Check current month's file first
    if current_file.exists():
        with open(current_file, newline="") as f:
            rows = list(csv.DictReader(f))

        if rows and rows[-1]["STOP_TIME"] == "":
            return current_file

    # If today isn't the first day of the month,
    # there's no reason to check another file.
    today = datetime.datetime.now()

    if today.day != 1:
        return current_file

    # Previous month's filename
    if today.month == 1:
        prev_month = 12
        prev_year = today.year - 1
    else:
        prev_month = today.month - 1
        prev_year = today.year

    previous_file = (
        current_file.parent /
        f"{prev_month:02d}{prev_year}_PROD_SEGMENT.csv"
    )

    if previous_file.exists():
        with open(previous_file, newline="") as f:
            rows = list(csv.DictReader(f))

        if rows and rows[-1]["STOP_TIME"] == "":
            return previous_file

    return current_file

def get_current_prod_id(prod_filename: Path) -> str:
    """
    Returns the latest PROD_ID from the current month's PROD_LIST.
    If the file doesn't exist or is empty, searches previous months.
    """

    current_file = prod_filename

    while True:

        if current_file.exists():
            with open(current_file, newline="") as f:
                rows = list(csv.DictReader(f))

            if rows:
                return rows[-1]["PROD_ID"]

        # Parse filename: MMYYYY_PROD_LIST.csv
        month = int(current_file.stem[:2])
        year = int(current_file.stem[2:6])

        # Go to previous month
        if month == 1:
            month = 12
            year -= 1
        else:
            month -= 1

        current_file = (
            current_file.parent /
            f"{month:02d}{year}_PROD_LIST.csv"
        )

        # Stop after an arbitrary lower limit
        if year < 2000:
            break

    return "PROD_ID_NOT_FOUND"

def save_segment(event: str, segment_filename = segment_filename):
    
    current_update_date = read_tag_string(cc, hc, "MCMS-Current_Date") # Date when current PROD_ID was created
    #last_update_date = read_tag_string(cc, hc, "MCMS-Last_Date")
    '''

    RECIPE CHANGE:
     Check if unclosed segment exists, if so:
     Close it with current totalizer values, current timestamp, running time

     Create a new segment under the current PROD_ID, add start time
     Reset totalizers
    '''

    # Convert PLC time strings to Unix timestamps
    current_update_dt = datetime.datetime.strptime(
        current_update_date,
        "%m/%d/%Y - %I:%M:%S %p"
    )

    prod_id = get_current_prod_id(prod_filename)
    segment_id = (f"SEG_{prod_id}_{current_update_dt:%H%M%S}")
    usr_id = f"N/A"
    segment_file_exists = os.path.exists(segment_filename)

    updated = False
    rows = []
    fieldnames = header

    if event=="RECIPE_CHANGED":

        if segment_file_exists:
            with open(segment_filename, newline="") as f:
                rows = list(csv.DictReader(f))

            if rows and rows[-1]["STOP_TIME"] == "":                          # Check if unclosed segment exists
                prev_start_time = datetime.datetime.fromisoformat(            # Calculate running time of previous segment
                rows[-1]["START_TIME"]
                )    

                rows[-1]["STOP_TIME"] = current_update_dt.isoformat()                     # Update the last row
                rows[-1]["RUN_TIME"] = segment_runtime
                rows[-1]["MASS_TOTAL"] = mass_prod_total
                rows[-1]["ADD1_TOTAL"] = add1_total
                rows[-1]["ADD2_TOTAL"] = add2_total
                rows[-1]["ADD3_TOTAL"] = add3_total
                rows[-1]["ADD4_TOTAL"] = add4_total
                rows[-1]["ADD5_TOTAL"] = add5_total
                rows[-1]["TOTAL_INCL_ADDITIVES"] = total_incl_additives
                rows[-1]["ADD1_PERCENT"] = add1_percent
                rows[-1]["ADD2_PERCENT"] = add2_percent
                rows[-1]["ADD3_PERCENT"] = add3_percent
                rows[-1]["ADD4_PERCENT"] = add4_percent
                rows[-1]["ADD5_PERCENT"] = add5_percent
                updated = True

            if updated:
                # Rewrite the file
                with open(segment_filename, "w", newline="") as f:
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(rows)

        # Append the new segment
        create_new_segment(fieldnames, segment_filename, segment_id, usr_id, prod_id, current_update_dt.isoformat(), segment_file_exists)

    elif event=="DAY_ROLLOVER":

        now = datetime.datetime.now()

        midnight_today = now.replace(hour=0, minute=0, second=0, microsecond=0)
        last_second_yesterday = midnight_today - timedelta(seconds=1)

        midnight_today = midnight_today.isoformat(timespec="seconds")
        last_second_yesterday = last_second_yesterday.isoformat(timespec="seconds")

        midnight_today_dt = now.replace(hour=0, minute=0, second=0, microsecond=0)
        last_second_yesterday_dt = midnight_today_dt - timedelta(seconds=1)

        segment_filename = get_segment_file_to_close(segment_filename)
        segment_file_exists = segment_filename.exists()

        if segment_file_exists:
            with open(segment_filename, newline="") as f:
                rows = list(csv.DictReader(f))

            if rows and rows[-1]["STOP_TIME"] == "":                                        # Check if unclosed segment exists
                prev_start_time = datetime.datetime.fromisoformat(                          # Calculate running time of previous segment
                rows[-1]["START_TIME"]
                )    
                
                rows[-1]["STOP_TIME"] = last_second_yesterday                # Update the last row
                rows[-1]["RUN_TIME"] = segment_runtime
                rows[-1]["MASS_TOTAL"] = mass_prod_total
                rows[-1]["ADD1_TOTAL"] = add1_total
                rows[-1]["ADD2_TOTAL"] = add2_total
                rows[-1]["ADD3_TOTAL"] = add3_total
                rows[-1]["ADD4_TOTAL"] = add4_total
                rows[-1]["ADD5_TOTAL"] = add5_total
                rows[-1]["TOTAL_INCL_ADDITIVES"] = total_incl_additives
                rows[-1]["ADD1_PERCENT"] = add1_percent
                rows[-1]["ADD2_PERCENT"] = add2_percent
                rows[-1]["ADD3_PERCENT"] = add3_percent
                rows[-1]["ADD4_PERCENT"] = add4_percent
                rows[-1]["ADD5_PERCENT"] = add5_percent
                updated = True

            if updated:
                # Rewrite the file
                with open(segment_filename, "w", newline="") as f:
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(rows)

                # Append the new segment 
                create_new_segment(fieldnames, segment_filename, segment_id, usr_id, prod_id, midnight_today, segment_file_exists)   

    else:
        raise ValueError(f"Unknown event: {event}")

    write_tag_value(cc, hc, "MCMS-Prod_Saved", 1, datetime.datetime.now().astimezone().isoformat()) # Update MCMS-Prod_Saved tag to signal that segment has been saved

    print("Segment Saved")



if __name__ == "__main__":

    if len(sys.argv) != 2:
        raise ValueError(
            "Usage: python save_segment.py <event>"
        )

    event = sys.argv[1]

    save_segment(event)