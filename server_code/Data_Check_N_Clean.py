import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import pandas as pd
import ServerMain

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

pd.set_option('display.max_columns',None)
pd.set_option('display.max_rows',None)
pd.set_option('display.width',None)

#
distance_list = ["800 Meters","1600 Meters","3200 Meters"]
xc_distance_list = ["2.0","3.0"]
allowed_distances = ["800 Meters","1600 Meters","3200 Meters","2.0","3.0"]



def normalize_df(df):
  df = df.sort_index(axis = 1)
  df = df.sort_values(by = ["StudentID","Length","Year","time_seconds","Meet"])
  df = df.reset_index(drop = True)
  return df

@anvil.server.callable
def verify_pr(df = None):
  print("Verification Started")
  if df is None:
    df = (pd.DataFrame(app_tables.pr_table.search()).drop(columns = "Team Position"))
  df = normalize_df(df)
  truth_df = normalize_df(pd.DataFrame(app_tables.pr_from_an.search()))


  df_equals_boolean = df.equals(truth_df)

  if df_equals_boolean:
    print(f"DF Confirmed {df_equals_boolean}")
  else:
    print(f"DF Denied {df_equals_boolean}")
    print("="*20)
    print(f"SELF Null Values : {df.isna().sum()}")
    print(f"TRUTH Null Values : {truth_df.isna().sum()}")
    print("="*20)
    print(f"SELF_DF Index : {max(df.index)}")
    print(f"TRUTH_DF Index : {max(truth_df.index)}")
    print(f"Columns of SELF : {list(df.columns)}")
    print(f"Columns of TRUTH : {list(truth_df.columns)}")
    print(f"ColumnTypes of SELF : {list(df.dtypes)}")
    print(f"ColumnTypes of TRUTH : {list(truth_df.dtypes)}")
    print("="*20)
    print(df.compare(truth_df))

def convert_df_to_pr(df):
  all_df = []
  for (year,length,gender), dfs in df.groupby(["Year","Length","Gender"]):
    dfs = dfs.sort_values(by = "time_seconds").drop_duplicates("StudentID",keep = "first").reset_index(drop = True)

    all_df.append(dfs)

  pr_df = pd.concat(all_df, ignore_index = True)
  return pr_df


def clean_data(df):
  df = normalize_df(df)

  if df.isna().any().any():
    print(df[df.isna().any(axis = 1)])
    print("Check NAN rows")

  df = ServerMain.filter_df(df,lengthlist = allowed_distances)
  df.drop_duplicates(inplace = True)
  return df

@anvil.server.callable
def table_cleaner(table=None,auto_df = None):
  if table is not None:
    df = pd.DataFrame(app_tables[table].search())
  else:
    df = auto_df
  df = clean_data(df)
  df_pr = convert_df_to_pr(df)
  verify_pr(df_pr)
  app_tables.snapshot_table.delete_all_rows()
  app_tables.snapshot_table.add_rows(df.to_dict(orient = "records"))
  print("Updated to Snapshot")

@anvil.server.callable
def snapshot_to_main():
  print("Uploading Snapshot to Main")
  rows = app_tables.snapshot_table.search()
  app_tables.race_data_table.delete_all_rows()
  app_tables.race_data_table.add_rows(rows)
  print("Snapshot to main completed")

@anvil.server.callable
def copy_main_to_history():
  print("Adding new rows to backup")
  rowsdf = pd.DataFrame(app_tables.race_data_table.search())
  ServerMain.add_unique_rows(rowsdf,"backup_race_data")
  print("New rows added")
  
  