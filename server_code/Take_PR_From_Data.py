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

def retrieve_data_from_tables(table):
  df = pd.DataFrame(app_tables[table].search())
  return df


@anvil.server.callable
def refresh_pr(xc_year,track_year):
  list_table = ["xc_table","track_table"]

  pr_df = None
  for table in list_table:
    
    if table == "xc_table":
      year = xc_year
    else:
      year = track_year
      
    df = retrieve_data_from_tables(table)
    
    for length in df["Length"].unique().tolist():
      dfs = filter_df(df,lengthlist = [length],yearlist = [year])
      mti = dfs.groupby("Runner")["time_seconds"].min().copy()
      dfs = dfs[dfs["time_seconds"] == dfs["Runner"].map(mti)]
      dfs.sort_values(by = "time_seconds")
      pr_df = pd.concat([dfs,pr_df], ignore_index = True)

  if not pr_df.isna().any().any():
    app_tables.pr_table.delete_all_rows()
    app_tables.pr_table.add_rows(pr_df.to_dict(orient = "records"))
    print("PR_table Updated")
  else:
    print("NaN value detected")

    


  