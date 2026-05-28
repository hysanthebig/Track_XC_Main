import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import pandas as pd
import plotly.express as px

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
@anvil.server.callable
def average_time(gender,length,grade):
  print("loaded")
  df = pd.DataFrame(app_tables.race_data_table.search(
    Gender = q.any_of(*gender),
    Length = q.any_of(*length),
    Grade = q.any_of(*grade)
  ))
  
  averaged_df = df.groupby(["Year","Length"])["time_seconds"].agg("mean").reset_index()
  figure = px.line(averaged_df, x = 'Year', y = "timne_seconds", title = "Average Times")
  return(figure)
  

