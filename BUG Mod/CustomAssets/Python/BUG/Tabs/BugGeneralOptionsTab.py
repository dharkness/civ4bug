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

		left, center, right = self.addThreeColumnLayout(screen, column, "Top", True)

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
		self.addCheckbox(screen, left, "MainInterface__FieldOfView")
		self.addCheckbox(screen, left, "MainInterface__FieldOfView_Remember")

		self.addLabel(screen, center, "CityScreen", "CITY SCREEN")
		self.addCheckbox(screen, center, "CityScreen__RawYields")
		self.addTextDropdown(screen, center, center, "CityScreen__RawYields_View", True)

		self.addSpacer(screen, center, "CityScreen_TopCenter")
		self.addCheckbox(screen, center, "CityScreen__WhipAssist")
		self.addCheckbox(screen, center, "CityScreen__WhipAssistOverflowCountCurrentProduction")
		self.addCheckbox(screen, center, "CityScreen__Anger_Counter")

		self.addSpacer(screen, center, "CityScreen_Bottom")
		self.addLabel(screen, center, "Misc", "Misc:")
		self.addCheckbox(screen, center, "CityScreen__CultureTurns")
		self.addCheckbox(screen, center, "CityScreen__GreatPersonTurns")
		self.addCheckbox(screen, center, "CityScreen__GreatPersonInfo")
		self.addTextDropdown(screen, center, center, "CityScreen__Specialists", True)

		self.addCheckbox(screen, right, "MainInterface__ProgressBarsTickMarks")

