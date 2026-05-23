import anvil.server
from anvil.tables import app_tables
from curl_cffi import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd
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
@anvil.server.callable
def retrieve_id(team_id,year,sport):
  print("entered")
  
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
          "Sport":"Track"
        })

  else:
    for r in data.get("results", []):
      name = f"{r['FirstName']} {r['LastName']}"
      gender = "Female" if r["GenderID"] == "F" else "Male"

      records.append({
        "Runner": name,
        "Gender": gender,
        "Grade": r["ShortDesc"],
        "StudentID": r["IDAthlete"],
        "Year": year,
        "Sport":"XC"
      })
  df = pd.DataFrame(records)
  df = df.drop_duplicates().reset_index(drop = True)
  to_add = df.to_dict(orient = "records")
  if sport == "track":
    for row in to_add:
      app_tables.track_id_table.add_row(**row)
  else:
    for row in to_add:
      app_tables.xc_id_table.add_row(**row)
    



