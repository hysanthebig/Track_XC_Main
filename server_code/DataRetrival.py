import anvil.server
from anvil.tables import app_tables
from curl_cffi import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd

# -------------------------
# CONFIG
# -------------------------
MAX_WORKERS = 10
BATCH_SIZE = 500

distances_list = ["800 Meters","1600 Meters","3200 Meters"]


# -------------------------
# HELPERS
# -------------------------


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
def get_records(row,sport):
  student_id = row["StudentID"]
  student = row["Runner"]
  if sport == "track":
    sport_id = "tf"
  else:
    sport_id = "xc"

  url = f"https://www.athletic.net/api/v1/AthleteBio/GetAthleteBioData?athleteId={student_id}&sport={sport_id}&level=0"

  res = requests.get(url, impersonate="chrome110")

  if res.status_code != 200:
    print("Error")
    print(res.status_code)
    print(url)
    return []

  data = res.json()

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
      if event in distances_list and r['Result'] not in ["DNS","DNF","SCR","DQ"]:
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
      records.append({
        "School": school_dict[str(r["SchoolID"])]["SchoolName"],
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
      
  print(records)
  return records


# -------------------------
# MAIN PIPELINE
# -------------------------
@anvil.server.background_task
def import_all_records(sport):
  if sport == "track":
    rows = list(app_tables.track_id_table.search())
  else:
    rows = list(app_tables.xc_id_table.search())

  all_records = []

  # -------------------------
  # 1. PARALLEL SCRAPE
  # -------------------------
  with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    futures = [executor.submit(get_records, row,sport) for row in rows]

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

  if sport == "track":
    app_tables.track_table.delete_all_rows()
    for chunk in chunked(all_records, BATCH_SIZE):
      print(chunk)
      app_tables.track_table.add_rows(chunk)
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