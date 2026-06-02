import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
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
def average_time(gender,length,grade,plottype = "Line"):
  print("loaded")
  
  if "All Grades" == grade:
    grade = [9,10,11,12]
  else:
    grade = [grade]
    
  df = pd.DataFrame(app_tables.pr_table.search(
    Gender = q.any_of(*gender),
    Length = q.any_of(*length),
    Grade = q.any_of(*grade)
  ))

  if plottype == "Line":
    averaged_df = df.groupby(["Year","Length"])["time_seconds"].agg("mean").reset_index()

    averaged_df["time_display"] = averaged_df["time_seconds"].apply(lambda s:f"{int(s//60)}:{int(s%60):02d}")
    
    figure = px.line(averaged_df, x = 'Year', y = "time_seconds",
                    color = "Length",
                    title = "Average Times",
                    labels = {
                      "time_seconds":"Time"
                    },
                    hover_data = {"time_display":True,"time_seconds":False})



    tickvals, ticktext = get_tickvals(averaged_df,15)
    
    figure.update_yaxes(tickvals = tickvals,ticktext = ticktext)
  
    return(figure)

  else:
    sorted_df = df.sort_values(by = ["Year","Length"])

    sorted_df["time_display"] = sorted_df["time_seconds"].apply(lambda s:f"{int(s//60)}:{int(s%60):02d}")

    figure = px.scatter(sorted_df, x = 'Year', y = "time_seconds",
                     trendline = "ols",
                     title = "Times by Year",
                     labels = {
                       "time_seconds":"Time"
                     },
                      hover_data = {"time_display":True,"time_seconds":False})

    tickvals, ticktext = get_tickvals(sorted_df,30)
    
    figure.update_yaxes(tickvals = tickvals,
                        ticktext = ticktext)

    

    
    
    return figure
  

