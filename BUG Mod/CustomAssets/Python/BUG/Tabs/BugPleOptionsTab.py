## BugScoresOptionsTab
## Tab for the BUG Scoreboard Options
## BUG Mod - Copyright 2007

import BugOptionsTab

class BugPleOptionsTab(BugOptionsTab.BugOptionsTab):
	"Plot List Enhancement Tab"
	
	def __init__(self, screen):
		BugOptionsTab.BugOptionsTab.__init__(self, "PLE", "Unit Icons")

	def create(self, screen):
		tab = self.createTab(screen)
		panel = self.createMainPanel(screen)
		left, center, right = self.addThreeColumnLayout(screen, panel, panel, True)
		
		#self.addCheckbox(screen, left, "PLE_Enabled")
		#self.addTextDropdown(screen, left, left, "PLE_Default_View_Mode")
		#self.addTextDropdown(screen, left, left, "PLE_Default_Group_Mode")
		#self.addCheckbox(screen, left, "PLE_Negative_Filters")
		self.addCheckbox(screen, left, "PLE_Move_Highlighter")
		
		self.addSpacer(screen, left, "PLE_Indicators")
		self.addLabel(screen, left, "PLE_Indicators")
		self.addCheckbox(screen, left, "PLE_Wounded_Indicator")
		#self.addCheckbox(screen, left, "PLE_Lead_By_GG_Indicator")
		self.addCheckbox(screen, left, "PLE_Promotion_Indicator")
		self.addCheckbox(screen, left, "PLE_Upgrade_Indicator")
		self.addCheckbox(screen, left, "PLE_Mission_Info")
		
		#self.addSpacer(screen, left, "PLE_Spacing")
		#self.addTextEdit(screen, left, left, "PLE_Horizontal_Spacing")
		#self.addTextEdit(screen, left, left, "PLE_Vertical_Spacing")
		
		
		self.addCheckbox(screen, center, "PLE_Health_Bar")
		self.addColorDropdown(screen, center, center, "PLE_Healthy_Color")
		self.addColorDropdown(screen, center, center, "PLE_Wounded_Color")
		self.addCheckbox(screen, center, "PLE_Hide_Health_Fighting")
		
		self.addSpacer(screen, center, "PLE_Bars")
		self.addCheckbox(screen, center, "PLE_Move_Bar")
		self.addColorDropdown(screen, center, center, "PLE_Full_Movement_Color")
		self.addColorDropdown(screen, center, center, "PLE_Has_Moved_Color")
		#self.addColorDropdown(screen, center, center, "PLE_No_Movement_Color")
		
		
		self.addCheckbox(screen, right, "PLE_Info_Pane")
		#self.addTextEdit(screen, right, right, "PLE_Info_Pane_X")
		#self.addTextEdit(screen, right, right, "PLE_Info_Pane_Y")
		self.addColorDropdown(screen, right, right, "PLE_Unit_Name_Color")
		
		self.addSpacer(screen, right, "PLE_Upgrade")
		self.addColorDropdown(screen, right, right, "PLE_Upgrade_Possible_Color")
		self.addColorDropdown(screen, right, right, "PLE_Upgrade_Not_Possible_Color")
		
		self.addSpacer(screen, right, "PLE_Specialties")
		self.addColorDropdown(screen, right, right, "PLE_Promotion_Specialties_Color")
		self.addColorDropdown(screen, right, right, "PLE_Unit_Type_Specialties_Color")
 