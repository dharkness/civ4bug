## BugGeneralOptionsTab
##
## Tab for the BUG General Options (Main and City Screens).
##
## Copyright (c) 2007-2008 The BUG Mod.
##
## Author: EmperorFool

import BugOptionsTab
import CvModName

class BugGeneralOptionsTab(BugOptionsTab.BugOptionsTab):
	"BUG General Options Screen Tab"
	
	def __init__(self, screen):
		BugOptionsTab.BugOptionsTab.__init__(self, "General", "General")

	def create(self, screen):
		tab = self.createTab(screen)
		panel = self.createMainPanel(screen)
		column = self.addOneColumnLayout(screen, panel)
		
		left, right = self.addTwoColumnLayout(screen, column, "Top", True)
		
		self.addLabel(screen, left, "MainInterface", "MAIN INTERFACE")
		self.addCheckbox(screen, left, "MainInterface__GPBar")
		self.addTextDropdown(screen, left, left, "MainInterface__GPBar_Types", True)
		self.addCheckbox(screen, left, "MainInterface__Combat_Counter")
		self.addSpacer(screen, left, "MainInterface_FieldOfView")
		self.addCheckbox(screen, left, "MainInterface__FieldOfView")
		self.addCheckbox(screen, left, "MainInterface__FieldOfView_Remember")
		
		self.addSpacer(screen, right, "MainInterface_TechWindow")
		self.addLabel(screen, right, "TechWindow", "Tech Splash Screen:")
		self.addTextDropdown(screen, right, right, "TechWindow__ViewType", True)
		self.addCheckbox(screen, right, "TechWindow__CivilopediaText")
		
		self.addSpacer(screen, right, "Misc")		
		self.addLabel(screen, right, "Misc", "Misc:")
		self.addCheckbox(screen, right, "MainInterface__CityArrows")
		self.addCheckbox(screen, right, "EventSigns__Enabled")
		self.addCheckbox(screen, right, "MainInterface__MinMax_Commerce")
		
		screen.attachHSeparator(column, column + "Sep")
		
		left, right = self.addTwoColumnLayout(screen, column, "Bottom", True)
		
		self.addLabel(screen, left, "CityScreen", "CITY SCREEN")
		self.addCheckbox(screen, left, "CityScreen__RawYields")
		self.addTextDropdown(screen, left, left, "CityScreen__RawYields_View", True)
		
		self.addSpacer(screen, left, "CityScreen_TopCenter")
		self.addCheckbox(screen, left, "CityScreen__FoodAssist")
		self.addCheckbox(screen, left, "CityScreen__WhipAssist")
		self.addCheckbox(screen, left, "CityScreen__WhipAssistOverflowCountCurrentProduction")
		self.addCheckbox(screen, left, "CityScreen__Anger_Counter")
		
		self.addSpacer(screen, right, "CityScreen_Bottom")
		self.addLabel(screen, right, "Misc", "Misc:")
		self.addCheckbox(screen, right, "CityScreen__CultureTurns")
		self.addCheckbox(screen, right, "CityScreen__GreatPersonTurns")
		self.addCheckbox(screen, right, "CityScreen__GreatPersonInfo")
		self.addCheckbox(screen, right, "MainInterface__ProgressBarsTickMarks")
		self.addTextDropdown(screen, right, right, "CityScreen__Specialists", True)		
