import anvil.server
from anvil.tables import app_tables
from curl_cffi import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd
import time
import random


error_count = 0

correct_count = 0

# -------------------------
# CONFIG
# -------------------------
MAX_WORKERS = 1
BATCH_SIZE = 500

distances_list = ["800 Meters","1600 Meters","3200 Meters"]


# -------------------------
# HELPERS
# -------------------------

def get_allowed():
  allowed = {}

  rows = list(app_tables.jrcbs_coach_list.search())
  for row in rows:
    schoolid = row["School ID"]
    year = row["Year"]
    if schoolid not in allowed:
      allowed[schoolid] = []

    allowed[schoolid].append(year)
  return allowed


def time_to_seconds(time_str):
  try:
    if float(time_str) < 60:
      return float(time_str)
  except:
    try:
      minutes, seconds = time_str.split(":")
      return int(minutes) * 60 + float(seconds)
    except:
      return None


# -------------------------
# FETCH FUNCTION
# -------------------------
def get_records(row,sport,allowed):
  global correct_count
  global error_count

  student_id = row["StudentID"]
  student = row["Runner"]
  years = int(row["Year"])

  if sport == "track":
    sport_id = "tf"
  else:
    sport_id = "xc"

  url = f"https://www.athletic.net/api/v1/AthleteBio/GetAthleteBioData?athleteId={student_id}&sport={sport_id}&level=0"

  time.sleep(random.uniform(0.2,0.5))
  for attempt in range(3):
    res = requests.get(url, impersonate="chrome110")

    if res.status_code == 200:
      break

    if res.status_code != 200:
      print(f"ERROR: CODE {res.status_code} |Attempt {attempt + 1 }| Time : {time.time()-start_time} |Completed {correct_count} Errors {error_count}  | URL : {url} ")
      time.sleep(random.uniform(5,6))
  else:
    error_count += 1
    return []


  data = res.json()
  correct_count += 1

  records = []
  event_dict = {}
  meet_dict = data.get("meets",[])
  school_dict = data.get("allTeams",[])
  grade_dict = data.get("grades",[])

  if sport == "track":
    for r in data.get("eventsTF",[]):
      event_dict[r["IDEvent"]] = r["Event"]

    for r in data.get("resultsTF", []):
      event = event_dict[r["EventID"]]
      #check data
      if r["SchoolID"] in allowed:
        print("a")
        if r["SeasonID"] in allowed[r["SchoolID"]]:     
          print(b)
          if event in distances_list and r['Result'] not in ["DNS","DNF","SCR","DQ","NT"]:
            records.append({
              "School":school_dict[str(r["SchoolID"])]["SchoolName"],
              "Runner": student,
              "Meet": meet_dict[str(r["MeetID"])]["MeetName"],
              "Date" : meet_dict[str(r["MeetID"])]["EndDate"].replace("T00:00:00", ""),        
              "Time": r["Result"].replace("a", ""),
              "Length": event,
              "Year":r["SeasonID"],
              "Grade":grade_dict[f"{str(r['SchoolID'])}_{str(r['SeasonID'])}"],
              "Gender":row["Gender"],
              "Sport":"Track"
            })
  else:
    for r in data.get("distancesXC",[]):
      event_dict[r["Meters"]] = r["Distance"]

    for r in data.get("resultsXC", []):
      if r["SchoolID"] in allowed:
        if r["SeasonID"] in allowed[r["SchoolID"]]:
          records.append({
            "School": school_dict[str(r["SchoolID"])]["SchoolName"] ,
            "Runner": student,
            "Meet": meet_dict[str(r["MeetID"])]["MeetName"],
            "Date" : meet_dict[str(r["MeetID"])]["EndDate"].replace("T00:00:00", ""),
            "Time": r["Result"],
            "Length": str(event_dict[r["Distance"]]),
            "Year":r["SeasonID"],
            "Grade":grade_dict[f"{str(r['SchoolID'])}_{str(r['SeasonID'])}"],
            "Gender":row["Gender"],
            "Sport":"XC"
          })


  return records


  # -------------------------
  # MAIN PIPELINE
  # -------------------------
@anvil.server.background_task
def import_all_records(sport):
    global start_time
    if sport == "track":
      rows = list(app_tables.track_id_table.search())
    else:
      rows = list(app_tables.xc_id_table.search())

    all_records = []

    # -------------------------
    # 1. PARALLEL SCRAPE
    # -------------------------
    start_time = time.time()
    allowed = get_allowed()
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
      futures = [executor.submit(get_records, row,sport,allowed) for row in rows]

      for future in as_completed(futures):
        result = future.result()
        if result:
          all_records.extend(result)

    # -------------------------
    # 2. CLEAN + TRANSFORM
    # -------------------------
    for r in all_records:
      r["time_seconds"] = time_to_seconds(r["Time"])




    # -------------------------
    # 3. BATCH INSERT INTO ANVIL
    # -------------------------
    def chunked(lst, size):
      for i in range(0, len(lst), size):
        yield lst[i:i+size]

    if error_count == 0:
      if sport == "track":
        app_tables.track_table.delete_all_rows()
        for chunk in chunked(all_records, BATCH_SIZE):
          print(chunk)
          app_tables.track_table.add_rows(chunk)
        print("DONE")
      else:
        app_tables.xc_table.delete_all_rows()
        for chunk in chunked(all_records, BATCH_SIZE):
          print(chunk)
          app_tables.xc_table.add_rows(chunk)
        print("DONE")
    return "Completed"


    # -------------------------
    # CALLABLE START FUNCTION
    # -------------------------
@anvil.server.callable
def start_import(sport):
  anvil.server.launch_background_task("import_all_records",sport)