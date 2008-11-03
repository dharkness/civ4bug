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
		
		left, space1, center, space2, right = self.addMultiColumnLayout(screen, column, 5, "Top", False)
		
		self.addLabel(screen, left, "MainInterface", "MAIN INTERFACE")
		self.addCheckbox(screen, left, "MainInterface__GPBar")
		self.addTextDropdown(screen, left, left, "MainInterface__GPBar_Types", True)
		self.addSpacer(screen, left, "MainInterface_FieldOfView")
		self.addCheckbox(screen, left, "MainInterface__FieldOfView")
		self.addCheckbox(screen, left, "MainInterface__FieldOfView_Remember")
		
		self.addSpacer(screen, space1, "Main_TechWindow", 3)
		
		self.addSpacer(screen, center, "MainInterface_TechWindow")
		self.addLabel(screen, center, "TechWindow", "Tech Splash Screen:")
		self.addTextDropdown(screen, center, center, "TechWindow__ViewType", True)
		self.addCheckbox(screen, center, "TechWindow__CivilopediaText")
		
		self.addSpacer(screen, space2, "Main_Misc", 3)
		
		self.addSpacer(screen, right, "Misc")		
		self.addLabel(screen, right, "Misc", "Misc:")
		self.addCheckbox(screen, right, "MainInterface__Combat_Counter")
		self.addCheckbox(screen, right, "MainInterface__CityArrows")
		
		screen.attachHSeparator(column, column + "Sep")
		
		left, space, right = self.addThreeColumnLayout(screen, column, "Bottom", False)
		
		self.addLabel(screen, left, "CityScreen", "CITY SCREEN")
		self.addCheckbox(screen, left, "CityScreen__RawYields")
		self.addTextDropdown(screen, left, left, "CityScreen__RawYields_View", True)
		
		self.addSpacer(screen, left, "CityScreen_TopCenter")
		self.addCheckbox(screen, left, "CityScreen__WhipAssist")
		self.addCheckbox(screen, left, "CityScreen__WhipAssistOverflowCountCurrentProduction")
		self.addCheckbox(screen, left, "CityScreen__Anger_Counter")
		
		self.addSpacer(screen, space, "City_Misc", 3)
		
		self.addSpacer(screen, right, "CityScreen_Bottom")
		self.addLabel(screen, right, "Misc", "Misc:")
		self.addCheckbox(screen, right, "CityScreen__CultureTurns")
		self.addCheckbox(screen, right, "CityScreen__GreatPersonTurns")
		self.addCheckbox(screen, right, "CityScreen__GreatPersonInfo")
		self.addCheckbox(screen, right, "MainInterface__ProgressBarsTickMarks")
		self.addTextDropdown(screen, right, right, "CityScreen__Specialists", True)		
