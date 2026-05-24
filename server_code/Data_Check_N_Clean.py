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
distance_list = ["800 Meters","1600 Meters","3200 Meters"]
xc_distance_list = ["2.0","3.0"]
allowed_distances = ["800 Meters","1600 Meters","3200 Meters","2.0","3.0"]



def normalize_df(df):
  df = df.sort_index(axis = 1)
  df = df.sort_values(by = ["StudentID","Length","Year","time_seconds","Meet"])
  df = df.reset_index(drop = True)
  return df

@anvil.server.callable
def verify_pr():
  print("Verification Started")
  df = normalize_df(pd.DataFrame(app_tables.pr_table.search()).drop(columns = "Team Position"))
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

  
def clean_data(df):
  df = normalize_df(df)

  if df.isna().any().any():
    print(df[df.isna().any(axis = 1)])
    print("Check NAN rows")

  df = filter_df(df,lengthlist = allowed_distances)
  df.drop_duplicates(inplace = True)
  return df

  
def table_cleaner(table):
  df = df = pd.DataFrame(app_tables[table].search())
  clean_data(df)
  
  