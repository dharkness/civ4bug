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
		
		self.addSpacer(screen, left, "MainInterface_TechWindow")
		self.addLabel(screen, left, "TechWindow", "Tech Splash Screen:")
		self.addTextDropdown(screen, left, left, "TechWindow__ViewType", True)
		self.addCheckbox(screen, left, "TechWindow__CivilopediaText")
		
		self.addSpacer(screen, left, "Misc")
		self.addLabel(screen, left, "Misc", "Misc:")
		self.addCheckbox(screen, left, "MainInterface__Combat_Counter")
		self.addCheckbox(screen, left, "MainInterface__CityArrows")
		self.addIntDropdown(screen, left, left, "MainInterface__FieldOfView", True)

		self.addLabel(screen, right, "CityScreen", "CITY SCREEN")
		self.addCheckbox(screen, right, "CityScreen__RawYields")
		self.addTextDropdown(screen, right, right, "CityScreen__RawYields_View", True)
		
		self.addSpacer(screen, right, "CityScreen_TopCenter")
		self.addCheckbox(screen, right, "CityScreen__WhipAssist")
		self.addCheckbox(screen, right, "CityScreen__WhipAssistOverflowCountCurrentProduction")
		self.addCheckbox(screen, right, "CityScreen__Anger_Counter")
		
		self.addSpacer(screen, right, "CityScreen_Bottom")
		self.addLabel(screen, right, "Misc", "Misc:")
		self.addCheckbox(screen, right, "CityScreen__CultureTurns")
		self.addCheckbox(screen, right, "CityScreen__GreatPersonTurns")
		self.addCheckbox(screen, right, "CityScreen__GreatPersonInfo")
		self.addTextDropdown(screen, right, right, "CityScreen__Specialists", True)

