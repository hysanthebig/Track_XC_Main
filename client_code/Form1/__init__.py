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
    self.meet_button.visible = False

    self.empty_row = []
    self.empty_row.append({"Team Position":0, "Runner":"No runners matching these filters","Meet":"If in XC,i"})

    

    # Any code you write here will run before the form opens.

  #IMPORT DATA AND TABLES================================================================================================================================================================================================================
    #When updating anything, sport is 'track' and 'xc', all lowercase
    if 1 == 0:
      anvil.server.call("get_id_launcher")
    if 1 == 0:
      anvil.server.call('start_import')
    if 1 == 0:
      anvil.server.call("refresh_pr")
    if 1 == 0:
      anvil.server.call("load_all_time")
  
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

  #=UI CALLS====================================================================================================================
    if 1 == 0:
      race_dict = {"XC":2025,"Track":2026}
      anvil.server.call('get_races',race_dict)
  #================================================================================================================================================================================================================

  def enter_data_into_grids(self,rows,panel):
    if len(rows) == 0:
      panel.items = self.empty_row
    else:
      panel.items = rows





  
  def display_pr(self,panel,length,gender,year):
    rows = app_tables.pr_table.search(tables.order_by("time_seconds"),Length=length,Gender=gender,Year=year)
    self.enter_data_into_grids(rows,panel)

  def display_atime(self,panel,length,gender):
    rows = app_tables.all_time_table.search(tables.order_by("time_seconds"),Length=length,Gender=gender)
    self.enter_data_into_grids(rows,panel)

  def display_race(self,panel,length,gender,year,meet):
    rows = app_tables.race_data_table.search(tables.order_by("time_seconds"),Length=length,Gender=gender,Year=year,Meet= meet)
    self.enter_data_into_grids(rows,panel)







  

  def refresh_pr(self):
    self.all_grids_visible(False)
    self.pr_dg_visible(True)
    selected_year = self.year_button.text
    selected_gender = self.gender_button.text
    selected_sport = self.sport_button.text

    if selected_sport == "Track":
      self.display_pr(panel = self.repeating_panel_1, length = "800 Meters",gender = selected_gender,year = selected_year)
      self.display_pr(panel = self.repeating_panel_2, length = "1600 Meters",gender = selected_gender,year = selected_year)
      self.display_pr(panel = self.repeating_panel_3, length = "3200 Meters",gender = selected_gender,year = selected_year)
    else:
      self.display_pr(panel = self.repeating_panel_1, length = "3.0",gender = selected_gender,year = selected_year)
      self.display_pr(panel = self.repeating_panel_2, length = "2.0",gender = selected_gender,year = selected_year)
      self.data_grid_3.visible = False


  
  def refresh_all_time(self):
    self.all_choice_button_visible(False)
    self.all_grids_visible(False)
    self.atime_dg_visible(True)
    self.gender_button.visible = True
    self.sport_button.visible = True

    selected_gender = self.gender_button.text
    selected_sport = self.sport_button.text

    if selected_sport == "Track":
      self.display_atime(panel = self.repeating_panel_4, length = "800 Meters",gender = selected_gender)
      self.display_atime(panel = self.repeating_panel_5, length = "1600 Meters",gender = selected_gender)
      self.display_atime(panel = self.repeating_panel_6, length = "3200 Meters",gender = selected_gender)
    else:
      self.display_atime(panel = self.repeating_panel_4, length = "3.0",gender = selected_gender)
      self.display_atime(panel = self.repeating_panel_5, length = "2.0",gender = selected_gender)
      self.data_grid_atime_3.visible = False
      

  
  def refresh_race(self):
    self.all_choice_button_visible(True)
    self.year_button.visible = False
    self.all_grids_visible(False)
    self.pr_dg_visible(True)
    
    selected_gender = self.gender_button.text
    selected_sport = self.sport_button.text
    selected_meet = self.meet_button.text
    current_year = datetime.datetime.now().year
  

    if selected_sport == "Track":
      selected_year = current_year
      self.display_race(panel = self.repeating_panel_1, length = "800 Meters",gender = selected_gender,year = selected_year,meet = selected_meet)
      self.display_race(panel = self.repeating_panel_2, length = "1600 Meters",gender = selected_gender,year = selected_year,meet = selected_meet)
      self.display_race(panel = self.repeating_panel_3, length = "3200 Meters",gender = selected_gender,year = selected_year,meet = selected_meet)
    else:
      if datetime.datetime.now().month <= 7:
        selected_year = current_year-1
      else:
        selected_year = current_year
      self.display_race(panel = self.repeating_panel_1, length = "3.0",gender = selected_gender,year = selected_year,meet = selected_meet)
      self.display_race(panel = self.repeating_panel_2, length = "2.0",gender = selected_gender,year = selected_year,meet = selected_meet)
      self.data_grid_3.visible = False
      





    
  def refresh_grids(self):
    if self.PR_button.appearance == "filled":
      self.refresh_pr()
    elif self.all_time_button.appearance == "filled":
      self.refresh_all_time()
    elif self.race_results.appearance == "filled":
      self.refresh_race()




  
  #________________________________________________________________________________________________________________________________________________
  # LOAD BUTTON MENUS
  #________________________________________________________________________________________________________________________________________________

  def load_years(self):
    start_year = 2022
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

  def load_race(self,sport = "Track"):


    race_list = []
    for race in list(app_tables.race_names_for_race_button.search()):
      menu_item = m3.MenuItem(text = race["Meet"])
      menu_item.set_event_handler('click',self.meet_item_click)
      menu_item.tag = race["Sport"]
      if menu_item.tag != sport:
        menu_item.visible = False
      race_list.append(menu_item)
    self.meet_button.menu_items = race_list
    
  def refresh_race_button(self,sport):
    counta = 0
    for menu_item in self.meet_button.menu_items:
      if menu_item.tag == sport:
        menu_item.visible = True
        if counta == 0:
          self.meet_button.text = menu_item.text
          counta += 1
      else:
        menu_item.visible = False




#########################################________________________________________________________________________
#Buttons
#################################################________________________________________________________________________

  def all_grids_visible(self,boolean):
    self.data_grid_1.visible = boolean
    self.data_grid_2.visible = boolean
    self.data_grid_3.visible = boolean
    self.data_grid_atime_1.visible = boolean
    self.data_grid_atime_2.visible = boolean
    self.data_grid_atime_3.visible = boolean

  def pr_dg_visible(self,boolean):
    self.data_grid_1.visible = boolean
    self.data_grid_2.visible = boolean
    self.data_grid_3.visible = boolean

  def atime_dg_visible(self,boolean):
    self.data_grid_atime_1.visible = boolean
    self.data_grid_atime_2.visible = boolean
    self.data_grid_atime_3.visible = boolean

  def all_choice_button_visible(self,boolean):
    self.gender_button.visible = boolean
    self.year_button.visible = boolean
    self.sport_button.visible = boolean
    self.meet_button.visible = boolean

  def all_main_button_appearance(self,appearance):
    self.PR_button.appearance = appearance
    self.all_time_button.appearance = appearance
    self.race_results.appearance = appearance
    
  @handle("", "show")
  def form_show(self,**event_args):
    self.load_years()
    self.load_gender()
    self.load_sport()
    self.load_race()
    self.refresh_grids()

  def year_item_click(self,sender, **event_args):
    self.year_button.text = sender.text
    self.refresh_grids()

  def gender_item_click(self,sender, **event_args):
    self.gender_button.text = sender.text
    self.refresh_grids()

  def sport_item_click(self,sender, **event_args):
    self.sport_button.text = sender.text
    self.refresh_grids()
    if self.race_results.appearance == "filled":
      if self.sport_button.text == "Cross Country":
        self.refresh_race_button(sport = "XC")
      else:
        self.refresh_race_button(sport = self.sport_button.text)

  def meet_item_click(self,sender, **event_args):
    self.meet_button.text = sender.text
    self.refresh_grids()

  @handle("all_time_button", "click")
  def all_time_button_click(self, **event_args):
    self.all_main_button_appearance("outlined")
    self.all_choice_button_visible(False)
    self.sport_button.visible = True
    self.gender_button.visible = True
    self.all_time_button.appearance = "filled"
    self.refresh_grids()

  @handle("PR_button", "click")
  def PR_button_click(self, **event_args):
    self.all_main_button_appearance("outlined")
    self.all_choice_button_visible(True)
    self.meet_button.visible = False
    self.PR_button.appearance = "filled"
    self.refresh_grids()

    
  @handle("race_results", "click")
  def race_results_click(self, **event_args):
    self.all_main_button_appearance("outlined")
    self.all_choice_button_visible(True)
    self.race_results.appearance = "filled"
    if self.sport_button.text == "Cross Country":
      self.refresh_race_button(sport = "XC")
    else:
      self.refresh_race_button(sport = self.sport_button.text)
    self.refresh_grids()

