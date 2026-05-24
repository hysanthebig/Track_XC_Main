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


@anvil.server.callable
def refresh_pr():
  df = pd.DataFrame(app_tables.race_data_table.search())

  all_df = []
  
  for (year,length,gender), dfs in df.groupby(["Year","Length","Gender"]):
    dfs = dfs.sort_values(by = "time_seconds").drop_duplicates("Runner",keep = "first").reset_index(drop = True)
    print(dfs)
    dfs["Team Position"] = dfs.index + 1
    all_df.append(dfs)
      
  pr_df = pd.concat(all_df, ignore_index = True)

  if not pr_df.isna().any().any():
    app_tables.pr_table.delete_all_rows()
    app_tables.pr_table.add_rows(pr_df.to_dict(orient = "records"))
    print("PR_table Updated")
  else:
    print("NaN value detected")

    


  