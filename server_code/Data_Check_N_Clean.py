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

def sort_df(df):
  df.sort_values(by = "StudentID")

def verify_pr():
  df = pd.DataFrame(app_tables.pr_table.search())
  truth_df = pd.DataFrame(app_tables.pr_from_an.search())

  