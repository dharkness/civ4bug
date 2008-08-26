## BugPleOptionsTab
##
## Tab for the BUG PLE Options.
##
## Copyright (c) 2008 The BUG Mod.
##
## Author: EmperorFool

import BugOptionsTab

class BugPleOptionsTab(BugOptionsTab.BugOptionsTab):
	"Plot List Enhancement Tab"
	
	def __init__(self, screen):
		BugOptionsTab.BugOptionsTab.__init__(self, "PLE", "Plot List")

	def create(self, screen):
		tab = self.createTab(screen)
		panel = self.createMainPanel(screen)
		left, center, right = self.addThreeColumnLayout(screen, panel, panel, True)
		
		#self.addCheckbox(screen, left, "PLE__Enabled")
		self.addCheckbox(screen, left, "PLE__Show_Buttons")
		self.addTextDropdown(screen, left, left, "PLE__Default_View_Mode")
		self.addTextDropdown(screen, left, left, "PLE__Default_Group_Mode")
		self.addTextDropdown(screen, left, left, "PLE__Filter_Behavior")
		
		self.addSpacer(screen, left, "PLE_Indicators")
		self.addLabel(screen, left, "PLE_Indicators")
		self.addCheckbox(screen, left, "PLE__Wounded_Indicator")
		self.addCheckbox(screen, left, "PLE__Lead_By_GG_Indicator")
		self.addCheckbox(screen, left, "PLE__Promotion_Indicator")
		self.addCheckbox(screen, left, "PLE__Upgrade_Indicator")
		self.addCheckbox(screen, left, "PLE__Mission_Info")
		
		#self.addSpacer(screen, left, "PLE__Spacing")
		#self.addTextEdit(screen, left, left, "PLE__Horizontal_Spacing")
		#self.addTextEdit(screen, left, left, "PLE__Vertical_Spacing")
		
		
		self.addCheckbox(screen, center, "PLE__Health_Bar")
		self.addColorDropdown(screen, center, center, "PLE__Healthy_Color")
		self.addColorDropdown(screen, center, center, "PLE__Wounded_Color")
		self.addCheckbox(screen, center, "PLE__Hide_Health_Fighting")
		
		self.addSpacer(screen, center, "PLE__Bars")
		self.addCheckbox(screen, center, "PLE__Move_Bar")
		self.addColorDropdown(screen, center, center, "PLE__Full_Movement_Color")
		self.addColorDropdown(screen, center, center, "PLE__Has_Moved_Color")
		self.addColorDropdown(screen, center, center, "PLE__No_Movement_Color")
		
		
		self.addLabel(screen, right, "PLE_Unit_Info_Tooltip")
		#self.addCheckbox(screen, right, "PLE__Info_Pane")  # EF: Can't get it to work
		#self.addTextEdit(screen, right, right, "PLE__Info_Pane_X")
		#self.addTextEdit(screen, right, right, "PLE__Info_Pane_Y")
		self.addColorDropdown(screen, right, right, "PLE__Unit_Name_Color")
		
		self.addLabel(screen, right, "PLE_Upgrade_Cost")
		self.addColorDropdown(screen, right, right, "PLE__Upgrade_Possible_Color")
		self.addColorDropdown(screen, right, right, "PLE__Upgrade_Not_Possible_Color")
		
		self.addLabel(screen, right, "PLE_Specialties")
		self.addColorDropdown(screen, right, right, "PLE__Unit_Type_Specialties_Color")
		self.addColorDropdown(screen, right, right, "PLE__Promotion_Specialties_Color")

		self.addSpacer(screen, right, "PLE_Move_Highlighter") 
 		self.addCheckbox(screen, right, "PLE__Move_Highlighter")
 