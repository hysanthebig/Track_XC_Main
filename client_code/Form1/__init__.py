from ._anvil_designer import Form1Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import m3.components as m3


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

  








  @handle("refresh_button", "click")
  def refresh_button_click(self, **event):
    self.repeating_panel_1.items = app_tables.pr_table.search(tables.order_by("time_seconds"),Length="1600 Meters")