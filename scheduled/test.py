from metrisapi.historian import HistorianClient
from metrisapi.configuration import ConfigurationClient
from metrisapi.dataanalysis import DataAnalysisClient
from metrisapi.account import AccountClient

import subprocess

import datetime


def run_bat(path, args=None, timeout=180, cwd=None, debug=False):
    if args is None:
        args = []

    command = [path] + args
    try:
        p = subprocess.Popen(
            command,
            shell=True,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace"
        )
 
        try:
            stdout, stderr = p.communicate(timeout=timeout)
            if debug:
                print("Finished!")
                print("Return code:", p.returncode)
                print("OUTPUT:")
                print(stdout)
                print("ERRORS:")
                print(stderr)

            if p.returncode == 0:
                return 1, stdout, stderr   # success
            else:
                return -1, stdout, stderr  # error in script
 
        except subprocess.TimeoutExpired:

            subprocess.run(f"taskkill /F /T /PID {p.pid}", shell=True)
            stdout, stderr = p.communicate()
            if debug:
                print("Timeout expired! Process killed.")
                print("OUTPUT (partial):")
                print(stdout)
                print("ERRORS (partial):")
                print(stderr)
 
            return -1, stdout, stderr      # timeout = fail
 
    except Exception as e:
        if debug:
            print("Exception occurred:", e)
        return -1, "", str(e)              # crash

# ----------------------------
# Metris connection
# ----------------------------

def read_tag_value(cc, hc, tag_name):
    tag_id = cc.get_tags_by_name([tag_name])[0]["id"]
    return hc.get_tag_values(tag_id)[0]["value"]

def read_tag_string(cc, hc, tag_name):
    tag_id = cc.get_tags_by_name([tag_name])[0]["id"]
    return hc.get_tag_values(tag_id)[0]["valueString"]

def write_tag_value(cc, hc, tag_name, value, timestamp):
    tag_id = cc.get_tags_by_name([tag_name])[0]["id"]
    payload = [
        {
          "tagID": tag_id,
          "timestamp": timestamp,
          "value": value,
        "quality":192
        }]
    hc.post_tag_values(payload)

def write_tag_string(cc, hc, tag_name, value, timestamp):
    tag_id = cc.get_tags_by_name([tag_name])[0]["id"]
    payload = [
        {
          "tagID": tag_id,
          "timestamp": timestamp,
          "valueString": value,
        "quality":192
        }]
    hc.post_tag_values(payload)

def check_change():
    base_uri = 'https://localhost:9000'
    ac = AccountClient(base_uri)
    token = ac.authenticate(username='metris.user', password='Metris123!')['id']

    hc = HistorianClient(base_uri, lambda: token)
    cc = ConfigurationClient(base_uri, token=lambda: token)
    dac = DataAnalysisClient(base_uri, lambda: token)

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

event, code = check_change()

if event == "RECIPE_CHANGED":
    code1, out, err = run_bat(
        path=r"C:\Metris\Metris.Python\notebooks\user-notebooks\Dashboards\MCMS\run_save_prod.bat",
        timeout=15,
        cwd=r"C:\Metris\Metris.Python\notebooks\user-notebooks\Dashboards\MCMS",
        debug=False,
    )

if code != 0:
    code2, out, err = run_bat(
        path=r"C:\Metris\Metris.Python\notebooks\user-notebooks\Dashboards\MCMS\run_save_segment.bat",
        args=[event],
        timeout=15,
        cwd=r"C:\Metris\Metris.Python\notebooks\user-notebooks\Dashboards\MCMS",
        debug=False,
    )