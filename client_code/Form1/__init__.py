from ._anvil_designer import Form1Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import m3.components as m3
import time


class Form1(Form1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    super().__init__(**properties)

    # Any code you write here will run before the form opens.

  if 1 == 0:
    anvil.server.call("retrieve_id","1619","2026","track")
  if 1 == 0:
    anvil.server.call('start_import',"xc")
  if 1 == 0:
    anvil.server.call("refresh_pr",xc_year = 2025,track_year = 2026)

  

  def display_pr(self,panel,length,gender,year):
    start = time.time()
    rows = app_tables.pr_table.search(tables.order_by("time_seconds"),Length=length,Gender=gender,Year=year)
    int_time=time.time()
    print(f"intermediate time {int_time-start}")
    list_rows = []
    for i, row in enumerate(rows):
      row = dict(row)
      row["Team Position"] = i + 1
      list_rows.append(row)
    panel.items = list_rows
    print(f"final_time {time.time()-start}")






  @handle("refresh_button", "click")
  def refresh_button_click(self, **event):
    self.display_pr(panel = self.repeating_panel_1, length = "800 Meters",gender = "Female",year = 2026)
    self.display_pr(panel = self.repeating_panel_2, length = "1600 Meters",gender = "Female",year = 2026)
    self.display_pr(panel = self.repeating_panel_4, length = "3200 Meters",gender = "Female",year = 2026)