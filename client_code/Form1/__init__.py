from ._anvil_designer import Form1Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import m3.components as m3
import time
import datetime


class Form1(Form1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    super().__init__(**properties)
    self.year_button.text = datetime.datetime.now().year
    self.gender_button.text = "Male"

    # Any code you write here will run before the form opens.
  def load_years(self):
    start_year = 2019
    current_year = datetime.datetime.now().year
    years = list(range(start_year,current_year+1))
    year_list = []
    for year in years:
      menu_item = m3.MenuItem(text = year)
      menu_item.set_event_handler('click',self.year_item_click)
      year_list.append(menu_item)
    self.year_button.menu_items = year_list

  def load_gender(self):
    gender_list = []
    for gender in ["Male","Female"]:
      menu_item = m3.MenuItem(text = gender)
      menu_item.set_event_handler('click',self.gender_item_click)
      gender_list.append(menu_item)
    self.gender_button.menu_items = gender_list    


  if 1 == 0:
    anvil.server.call("retrieve_id","1619","2026","track")
  if 1 == 0:
    anvil.server.call('start_import',"xc")
  if 1 == 0:
    anvil.server.call("refresh_pr")

  

  def display_pr(self,panel,length,gender,year):
    rows = app_tables.pr_table.search(tables.order_by("time_seconds"),Length=length,Gender=gender,Year=year)
    panel.items = rows






  @handle("refresh_button", "click")
  def refresh_button_click(self, **event):
    selected_year = self.year_button.text
    selected_gender = self.gender_button.text
    self.display_pr(panel = self.repeating_panel_1, length = "800 Meters",gender = selected_gender,year = selected_year)
    self.display_pr(panel = self.repeating_panel_2, length = "1600 Meters",gender = selected_gender,year = selected_year)
    self.display_pr(panel = self.repeating_panel_4, length = "3200 Meters",gender = selected_gender,year = selected_year)

  @handle("", "show")
  def form_show(self,**event_args):
    self.load_years()
    self.load_gender()

  def year_item_click(self,sender, **event_args):
    self.year_button.text = sender.text


  def gender_item_click(self,sender, **event_args):
    self.gender_button.text = sender.text