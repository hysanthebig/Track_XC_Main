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
    self.sport_button.text = "Track"

    

    # Any code you write here will run before the form opens.

#IMPORT DATA AND TABLES================================================================================================================================================================================================================
  #When updating anything, sport is 'track' and 'xc', all lowercase
  if 1 == 0:
    anvil.server.call("get_id_launcher")
  if 1 == 0:
    anvil.server.call('start_import')
  if 1 == 0:
    anvil.server.call("refresh_pr")

#CLEAN DATA AND VERIFY=========================================================================================================================
  if 1 == 0:
    anvil.server.call('verify_key_pr_retrival')
  if 1 == 0: #table cleaner includes a verification check
    anvil.server.call("table_cleaner","race_data_table")
  if 1 == 0:
    anvil.server.call("snapshot_to_main")
    
  if 1 == 0:
    anvil.server.call("verify_pr")
  if 1 == 0:
    anvil.server.call("copy_main_to_history")


#================================================================================================================================================================================================================






  
  def display_pr(self,panel,length,gender,year):
    rows = app_tables.pr_table.search(tables.order_by("time_seconds"),Length=length,Gender=gender,Year=year)
    panel.items = rows



  def refresh_grids(self):
    self.all_grids_visible()

    selected_year = self.year_button.text
    selected_gender = self.gender_button.text
    selected_sport = self.sport_button.text

    if selected_sport == "Track":
      self.display_pr(panel = self.repeating_panel_1, length = "800 Meters",gender = selected_gender,year = selected_year)
      self.display_pr(panel = self.repeating_panel_2, length = "1600 Meters",gender = selected_gender,year = selected_year)
      self.display_pr(panel = self.repeating_panel_4, length = "3200 Meters",gender = selected_gender,year = selected_year)
    else:
      self.display_pr(panel = self.repeating_panel_1, length = "3.0",gender = selected_gender,year = selected_year)
      self.display_pr(panel = self.repeating_panel_2, length = "2.0",gender = selected_gender,year = selected_year)
      self.data_grid_4.visible = False






#########################################________________________________________________________________________
#Buttons
#################################################________________________________________________________________________

  def all_grids_visible(self):
    self.data_grid_1.visible = True
    self.data_grid_2.visible = True
    self.data_grid_4.visible = True
    
  
  @handle("refresh_button", "click")
  def refresh_button_click(self, **event):
    self.refresh_grids()
    
  @handle("", "show")
  def form_show(self,**event_args):
    self.load_years()
    self.load_gender()
    self.load_sport()

  def year_item_click(self,sender, **event_args):
    self.year_button.text = sender.text
    self.refresh_grids()

  def gender_item_click(self,sender, **event_args):
    self.gender_button.text = sender.text
    self.refresh_grids()

  def sport_item_click(self,sender, **event_args):
    self.sport_button.text = sender.text
    self.refresh_grids()





#________________________________________________________________________________________________________________________________________________
# LOAD BUTTON MENUS
#________________________________________________________________________________________________________________________________________________

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

  def load_sport(self):
    sport_list = []
    for sport in ["Cross Country","Track"]:
      menu_item = m3.MenuItem(text = sport)
      menu_item.set_event_handler('click',self.sport_item_click)
      sport_list.append(menu_item)
    self.sport_button.menu_items = sport_list   