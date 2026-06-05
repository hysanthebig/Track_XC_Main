import anvil.server
from anvil.tables import app_tables
from curl_cffi import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd
from ServerMain import add_unique_rows
# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#

###Retrieve student ids from athletic net
MAX_WORKERS = 5

def retrieve_id(row):
  sport = row["Sport"]
  team_id = row["School ID"]
  year = row["Year"]

  
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
          "Runner": name,
          "Gender": gender,
          "Grade": r["GradeID"],
          "StudentID": r["IDAthlete"],
          "Year":year,
          "Sport":"Track",
          "School":row["School"]
        })

  else:
    for r in data.get("results", []):
      name = f"{r['FirstName']} {r['LastName']}"
      gender = "Female" if r["GenderID"] == "F" else "Male"

      records.append({
        "Runner": name,
        "Gender": gender,
        "Grade": int(r["ShortDesc"]),
        "StudentID": r["IDAthlete"],
        "Year": year,
        "Sport":"XC",
        "School":row["School"]
      })
  
  return records

    

@anvil.server.callable
def get_id_launcher():
  
  rows = list(app_tables.jrcbs_coach_list.search())

  all_records = []

  with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    futures = [executor.submit(retrieve_id, row) for row in rows]

    for future in as_completed(futures):
      result = future.result()
      if result:
        all_records.extend(result)

  
  df = pd.DataFrame(all_records)
  df = df.drop_duplicates(subset = ["StudentID","Sport"]).reset_index(drop = True)
  to_add = df.to_dict(orient = "records")
  add_unique_rows(to_add,"athlete_table")


  print("IDs Updated")