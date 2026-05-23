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

field_events_list = [
  'Shot Put', 'Discus', 'High Jump',
  'Pole Vault', 'Long Jump', 'Triple Jump'
]


# -------------------------
# HELPERS
# -------------------------
def field_event(length):
  if "m" in length:
    return length
  elif "'" in length:
    try:
      feet, inches = length.split("'")
      total_inches = float(feet) * 12 + float(inches.replace('"', ""))
      meters = round(total_inches * 0.0254, 2)
      return f"{meters}m"
    except:
      print(length)
  elif "-" in length:
    feet, inches = length.split("-")
    total_inches = float(feet) * 12 + float(inches)
    meters = round(total_inches * 0.0254, 2)
    return f"{meters}m"
  return length


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
def get_records(row,sport,team_id,year):
  
  if sport == "track":
    url = f"https://www.athletic.net/api/v1/TeamHome/GetTeamEventRecords?teamId={team_id}&seasonId={year}"
  else:
    url = f"https://www.athletic.net/api/v1/TeamHome/GetSeasonBest?teamId={team_id}&seasonId={year}"

  res = requests.get(url, impersonate="chrome110")

  if res.status_code != 200:
    print("Error")
    return []

  data = res.json()

  records = []
  if sport == "track":
    for r in data.get("eventRecords", []):
      if r["Event"] in ["800 Meters","1600 Meters","3200 Meters"]:
        name = f"{r['FirstName']} {r['LastName']}"
        gender = "Female" if r["Gender"] == "F" else "Male"
  
        records.append({
          "School": school,
          "Runner": name,
          "Gender": gender,
          "Grade": r["GradeID"],
          "Race": r["MeetName"],
          "Time": r["Result"].replace("a", ""),
          "Length": r["Event"],
          "Date": r["EndDate"].replace("T00:00:00", ""),
        })
  else:
    for r in data.get("results", []):
      name = f"{r['FirstName']} {r['LastName']}"
      gender = "Female" if r["GenderID"] == "F" else "Male"

      records.append({
          "School": school,
          "Runner": name,
          "Gender": gender,
          "Grade": r["ShortDesc"],
          "Race": r["MeetName"],
          "Time": r["Result"].replace("a", ""),
          "Length": str(r["Distance"]),
          "Date": r["MeetDate"].replace("T00:00:00", ""),
        })
  print(records)
  return records


# -------------------------
# MAIN PIPELINE
# -------------------------
@anvil.server.background_task
def import_all_recordsa(sport):

  rows = list(app_tables.school_ids.search())

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

    if r["Length"] in field_events_list:
      r["Time"] = field_event(r["Time"])

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
def pr_retrival(sport):
  anvil.server.launch_background_task("import_all_recordsa",sport)