import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
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
def retrieve_data_from_tables(table):
  df = pd.DataFrame(app_tables[table].search())
  return df


@anvil.server.callable
def refresh_pr(year):
  list_table = ["xc_table","track_table"]
  for table in list_table:
    df = retrieve_data_from_tables(table)
    for length in df["Length"].unique().tolist:
      df = filter(df,lengthlist = [length],yearlist = [year],)
      
    print(df)
    


  
  