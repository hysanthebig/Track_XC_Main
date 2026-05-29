import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import pandas as pd
import plotly.express as px
from ServerMain import get_tickvals

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





@anvil.server.callable
def individual_graph(runner,length,grade):
  print("loaded")

  if "All Grades" == grade:
    grade = [9,10,11,12]
  else:
    grade = [grade]

  df = pd.DataFrame(app_tables.pr_table.search(
    Runner = q.any_of(runner),
    Length = q.any_of(*length),
    Grade = q.any_of(*grade)
  ))


  sorted_df = df.sort_values(by = ["Runner","Length"])
  
  sorted_df["time_display"] = sorted_df["time_seconds"].apply(lambda s:f"{int(s//60)}:{int(s%60):02d}")
  sorted_df["date_dt"] = pd.to_datetime(df["Date"])
  
  figure = px.line(sorted_df, x = 'date_dt', y = "time_seconds",
                     color = "Length",
                     title = "Average Times",
                     labels = {
                       "time_seconds":"Time"
                     },
                     hover_data = {"time_display":True,"time_seconds":False})


  tickvals, ticktext = get_tickvals(sorted_df)

  figure.update_yaxes(tickvals = tickvals,ticktext = ticktext)
  figure.update_xaxes(tickformat = "")

  return(figure)



