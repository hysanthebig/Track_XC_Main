import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import pandas as pd
from ServerMain import filter_df

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

pd.set_option('display.max_columns',None)
pd.set_option('display.max_rows',None)
pd.set_option('display.width',None)

distance_list = ["800 Meters","1600 Meters","3200 Meters"]
xc_distance_list = ["2.0","3.0"]

@anvil.server.callable
def refresh_pr():
  df = pd.DataFrame(app_tables.race_data_table.search())

  all_df = []
  
  for (year,length,gender), dfs in df.groupby(["Year","Length","Gender"]):
    dfs = dfs.sort_values(by = "time_seconds").drop_duplicates("StudentID",keep = "first").reset_index(drop = True)
    print(dfs)
    dfs["Team Position"] = dfs.index + 1
    all_df.append(dfs)
      
  pr_df = pd.concat(all_df, ignore_index = True)

  app_tables.pr_table.delete_all_rows()
  app_tables.pr_table.add_rows(pr_df.to_dict(orient = "records"))
  print("PR_table Updated")


@anvil.server.callable
def load_all_time():
  df = pd.DataFrame(app_tables.race_data_table.search())

  all_df = []

  for (length,gender), dfs in df.groupby(["Length","Gender"]):
    dfs = dfs.sort_values(by = "time_seconds").drop_duplicates("StudentID",keep = "first").reset_index(drop = True)
    print(dfs)
    dfs["Coaching Year"] = [
      f"Year {year - 2022}" for year in dfs["Year"]
    ]
    dfs["Team Position"] = dfs.index + 1
    if length in distance_list:
       dfs = dfs.head(10)
    elif length in xc_distance_list:
      dfs = dfs.head(20)
      
    all_df.append(dfs)

  pr_df = pd.concat(all_df, ignore_index = True)

  app_tables.all_time_table.delete_all_rows()
  app_tables.all_time_table.add_rows(pr_df.to_dict(orient = "records"))
  print("All_time_table Updated")



  