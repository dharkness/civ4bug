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
		
		screen.attachHSeparator(left, left + "SepL1")
		
		self.addCheckbox(screen, left, "MainInterface__FieldOfView")
		self.addCheckbox(screen, left, "MainInterface__FieldOfView_Remember")
		
		screen.attachHSeparator(left, left + "SepL2")
		
		self.addLabel(screen, left, "TechWindow", "Tech Splash Screen:")
		self.addTextDropdown(screen, left, left, "TechWindow__ViewType", True)
		self.addCheckbox(screen, left, "TechWindow__CivilopediaText")
		
		screen.attachHSeparator(left, left + "SepL3")
		
		self.addLabel(screen, left, "Misc", "Misc:")
		self.addCheckbox(screen, left, "MainInterface__CityArrows")
		self.addCheckbox(screen, left, "EventSigns__Enabled")
		self.addCheckbox(screen, left, "MainInterface__MinMax_Commerce")
		
		
		self.addLabel(screen, right, "CityScreen", "CITY SCREEN")
		self.addCheckbox(screen, right, "CityScreen__WhipAssist")
		self.addCheckbox(screen, right, "CityScreen__WhipAssistOverflowCountCurrentProduction")
		self.addCheckbox(screen, right, "CityScreen__Anger_Counter")
		
		screen.attachHSeparator(right, right + "SepR1")
		
		self.addCheckbox(screen, right, "CityScreen__RawYields")
		self.addTextDropdown(screen, right, right, "CityScreen__RawYields_View", True)
		
		screen.attachHSeparator(right, right + "SepR2")
		
		self.addLabel(screen, right, "Misc", "Misc:")
		self.addCheckbox(screen, right, "CityScreen__CultureTurns")
		self.addCheckbox(screen, right, "CityScreen__GreatPersonTurns")
		self.addCheckbox(screen, right, "CityScreen__GreatPersonInfo")
		self.addCheckbox(screen, right, "CityScreen__FoodAssist")
		self.addCheckbox(screen, right, "MainInterface__ProgressBarsTickMarks")
		self.addTextDropdown(screen, right, right, "CityScreen__Specialists", True)		
