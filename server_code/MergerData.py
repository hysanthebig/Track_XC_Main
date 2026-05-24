import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

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
def merger():
  print("Merging")
  table_1 = [dict(row) for row in app_tables.track_id_table.search()]
  table_2 = [dict(row) for row in app_tables.xc_id_table.search()]
  merged_table = table_1 + table_2
  app_tables.race_data.add_rows(merged_table)
  print("Merged")
  