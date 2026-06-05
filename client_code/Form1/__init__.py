from ._anvil_designer import Form1Template
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import m3.components as m3
import time
import datetime

track_events = ["800 Meters","1600 Meters", "3200 Meters"]
xc_events = ["2.0","3.0"]

class Form1(Form1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    super().__init__(**properties)
    self.year_button.text = datetime.datetime.now().year
    self.gender_button.text = "Male"
    self.sport_button.text = "Track"
    self.meet_button.visible = False
    self.grade_button.text = "All Grades"
    self.length_button.text = "1600 Meters"

    self.empty_row = []
    self.empty_row.append({"Team Position":0, "Runner":"No runners matching these filters"})
    self.data_grid_1.role = "wide"
    self.data_grid_2.role = "wide"
    self.data_grid_3.role = "wide"
    self.data_grid_atime_1.role = "wide"
    self.data_grid_atime_2.role = "wide"
    self.data_grid_atime_3.role = "wide"

    function_list = []
    for function in ["Average Team Times","Average Team Times Scatter Graph"]:
      menu_item = m3.MenuItem(text = function)
      menu_item.set_event_handler('click',self.additional_item_click)
      function_list.append(menu_item)
    self.functions_menus.menu_items = function_list   

    self.panel_dict = {"800 Meters":self.repeating_panel_1,
                       "1600 Meters":self.repeating_panel_2,
                       "3200 Meters":self.repeating_panel_3,
                       "2.0":self.repeating_panel_1,
                       "3.0":self.repeating_panel_2,
                      }

  

    
    if 1 == 0:
      self.plot_1.figure = anvil.server.call('individual_graph',"Hysan (Ka Hei) Chiu",["1600 Meters"],"All Grades")

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
    if len(rows) == 0 and self.sport_button.text != "Cross Country":
      panel.items = self.empty_row
    elif len(rows) == 0 and self.sport_button.text == "Cross Country":
      self.hide_parent(panel)
    else:
      panel.items = rows

  def hide_parent(self,object_to_hide):
    object_to_hide.parent.visible = False



  
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
      for lengths,length_panel in self.panel_dict.items():
        if lengths in track_events:
          self.display_pr(panel = length_panel,length = lengths,gender = selected_gender,year = selected_year)
          
    else:
      for lengths,length_panel in self.panel_dict.items():
        if lengths in xc_events:
          self.display_pr(panel = length_panel,length = lengths,gender = selected_gender,year = selected_year)
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
    self.all_grids_visible(True)
    self.atime_dg_visible(False)
    
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
      
  def graph_average_times(self,type):

    selected_gender = self.gender_button.text
    selected_length = self.length_button.text
    selected_grade = self.grade_button.text

    self.plot_1.figure = anvil.server.call('average_time',[selected_gender],[selected_length],selected_grade,plottype = type)

  def graph_indi_times(self):
    selected_length = self.length_button.text
    selected_grade = self.grade_button.text
    selected_runner = self.runner_button.text

    self.plot_1.figure = anvil.server.call("individual_graph",selected_runner,selected_length,selected_grade)


    
  def refresh_grids(self):
    if self.PR_button.appearance == "filled":
      self.refresh_pr()
    elif self.all_time_button.appearance == "filled":
      self.refresh_all_time()
    elif self.race_results.appearance == "filled":
      self.refresh_race()
    elif self.functions_menus.appearance == "filled":
      if self.functions_menus.text == "Average Team Times":
        self.graph_average_times("Line")
      elif self.functions_menus.text == "Average Team Times Scatter Graph":
        self.graph_average_times("Scatter")




  
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

  def load_grade(self):
    grade_list = []
    for grade in ["All Grades",9,10,11,12]:
      menu_item = m3.MenuItem(text = grade)
      menu_item.set_event_handler('click',self.grade_item_click)
      grade_list.append(menu_item)
    self.grade_button.menu_items = grade_list   

  
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


  
  def load_events(self,sport = "Track"):

    length_list = []
    length_dict = {"1600 Meters":"Track","800 Meters":"Track","3200 Meters":"Track","3.0":"XC","2.0":"XC"}
    for length in length_dict:
      menu_item = m3.MenuItem(text = length)
      menu_item.set_event_handler('click',self.length_item_click)
      menu_item.tag = length_dict[length]
      if menu_item.tag != sport:
        menu_item.visible = False
      length_list.append(menu_item)
    self.length_button.menu_items = length_list

    
  def refresh_length_button(self,sport):
    counta = 0
    for menu_item in self.length_button.menu_items:
      if menu_item.tag == sport:
        menu_item.visible = True
        if counta == 0:
          self.length_button.text = menu_item.text
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
    self.grade_button.visible = boolean
    self.length_button.visible = boolean

  def all_main_button_appearance(self,appearance):
    self.PR_button.appearance = appearance
    self.all_time_button.appearance = appearance
    self.race_results.appearance = appearance
    self.functions_menus.appearance = appearance
    
  @handle("", "show")
  def form_show(self,**event_args):
    self.load_years()
    self.load_gender()
    self.load_sport()
    self.load_race()
    self.load_grade()
    self.load_events()
    self.refresh_grids()

  def year_item_click(self,sender, **event_args):
    self.year_button.text = sender.text
    self.refresh_grids()

  def gender_item_click(self,sender, **event_args):
    self.gender_button.text = sender.text
    self.refresh_grids()


  def grade_item_click(self,sender, **event_args):
    self.grade_button.text = sender.text
    self.refresh_grids()
    
  def sport_item_click(self,sender, **event_args):
    self.sport_button.text = sender.text
    self.refresh_grids()
    if self.race_results.appearance == "filled":
      if self.sport_button.text == "Cross Country":
        self.refresh_race_button(sport = "XC")
      else:
        self.refresh_race_button(sport = self.sport_button.text)
    elif self.functions_menus.appearance == "filled":
      if self.sport_button.text == "Cross Country":
        self.refresh_length_button(sport = "XC")
      else:
        self.refresh_length_button(sport = self.sport_button.text)
        
  def length_item_click(self,sender, **event_args):
    self.length_button.text = sender.text
    self.refresh_grids()

        
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
    self.grade_button.visible = False
    self.meet_button.visible = False
    self.length_button.visible = False
    self.PR_button.appearance = "filled"
    self.refresh_grids()

    
  @handle("race_results", "click")
  def race_results_click(self, **event_args):
    self.all_main_button_appearance("outlined")
    self.all_choice_button_visible(True)
    self.length_button.visible = False
    self.grade_button.visible = False
    self.race_results.appearance = "filled"
    if self.sport_button.text == "Cross Country":
      self.refresh_race_button(sport = "XC")
    else:
      self.refresh_race_button(sport = self.sport_button.text)
    self.refresh_grids()


  def additional_item_click(self,sender, **event_args):
    self.all_main_button_appearance("outlined")
    self.all_choice_button_visible(True)
    self.year_button.visible = False
    self.meet_button.visible = False
    self.all_grids_visible(False)
    self.plot_1.visible = True
    self.functions_menus.appearance = "filled"
    self.functions_menus.text = sender.text

