import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import pandas as pd
from Data_Check_N_Clean import normalize_df

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

##
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


###appends unique data to table    works for now, must fix later because its inefficent.
def add_unique_rows(rows,table):
  previous_df = normalize_df(pd.DataFrame(app_tables[table].search()))

  if isinstance(rows,pd.DataFrame):
    df = normalize_df(rows)
  else:
    df = normalize_df(pd.DataFrame(rows))

  combined = pd.concat([previous_df,df])
  combined = combined.drop_duplicates(keep = False, ignore_index = True)
  app_tables[table].add_rows(combined.to_dict(orient = "records"))
  print(f"Added {len(combined)} rows")

@anvil.server.callable
def get_races(sport_year_dict):
  all_list = []
  for sport,year in sport_year_dict.items():
    df = pd.DataFrame(app_tables.race_data_table.search(q.fetch_only("Meet","Year","Sport"),Year = year,Sport = sport))
    df = df.drop(columns = ["time_seconds","Length","StudentID","School","Runner","Date","Grade","Time","Gender"])
    df = df.drop_duplicates()
    all_list.append(df)
  df = pd.concat(all_list,ignore_index = True)
  app_tables.race_names_for_race_button.delete_all_rows()
  app_tables.race_names_for_race_button.add_rows(df.to_dict(orient = "records"))
  print("Get_Races finished")

def get_tickvals(df,by):
  min_time = df['time_seconds'].min()
  max_time = df['time_seconds'].max()

  tickvals = list(range(int(min_time // by)*by,int(max_time//by +1)*by,by))
  ticktext = [f"{t//60}:{t%60:02d}" for t in tickvals]

  return tickvals,ticktext


  
