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
    anvil.server.call('start_import',"track")
  anvil.server.call("refresh_pr")






  def create_grids(self):
    self.event_grids = {}
    self.event_panels = {}
    event_list = ["1"]
    
    for event in event_list:
      df = anvil.server.call("get_table","xc")
      grid = DataGrid()
      self.event_grids[event] = grid
      self.flow_panel_1.add_component(grid)
      grid.columns = [{"id":"A","title": event,"data_key":"Rank"},
                      {"id":"B","title":"School","data_key":"School"},
                      {"id":"C","title":"Runner","data_key":"Runner"},
                      {"id":"D","title":"Grade","data_key":"Grade"},
                      {"id":"E","title":"Length","data_key":"Length"},
                      {"id":"F","title":"Time","data_key": "Time","width":140 }]
      rp = RepeatingPanel(item_template=DataRowPanel)
      if not df:
        grid.remove_from_parent()
        pass

      rp.items = [

        {
          **row,
          "Rank": i + 1,
        }
        for i, row in enumerate(df)
      ]

      grid.add_component(rp)
      self.event_panels[event] = rp

  @handle("refresh_button", "click")
  def refresh_button_click(self, **event):
    self.create_grids()