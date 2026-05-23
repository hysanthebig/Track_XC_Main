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

@anvil.server.callable
def get_table(sport):
  if sport == "track":
    data = app_tables.track_id_table.search()
  else:
    data = app_tables.xc_table.search()
  return data

def filter_df(df,runnerlist = None,schoollist = None,lengthlist= None,gender = None,gradelist =None, meetlist = None, yearlist = None):
  ####################Filter#######################
  readmask = pd.Series(True,index = df.index)

  if runnerlist:
    readmask &= df["Runner"].isin(runnerlist)

  if schoollist:
    readmask &= df["School"].isin(schoollist)

  if gradelist:
    readmask &= df["Grade"].isin(gradelist)

  if gender:
    readmask &= df["Gender"].isin([gender])

  if lengthlist:
    readmask &= df["Length"].isin(lengthlist)

  if meetlist:
    readmask &= df["Meet"].isin(meetlist)

  if yearlist:
    readmask &= df["Year"].isin(yearlist)

  df_filtered = df.loc[readmask]

  return(df_filtered)


