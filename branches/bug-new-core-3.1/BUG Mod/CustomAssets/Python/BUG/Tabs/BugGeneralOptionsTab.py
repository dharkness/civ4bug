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

		self.addLabel(screen, left, "MainInterface", "Main Interface:")
		self.addCheckbox(screen, left, "MainInterface__GPBar")
		self.addTextDropdown(screen, left, left, "MainInterface__GPBar_Types")
		
		self.addSpacer(screen, left, "MainInterface_Combat_Counter")
		self.addCheckbox(screen, left, "MainInterface__Combat_Counter")
		
		self.addSpacer(screen, left, "MainInterface_CityArrows")
		self.addCheckbox(screen, left, "MainInterface__CityArrows")

		self.addLabel(screen, right, "CityScreen", "City Screen:")
		self.addCheckbox(screen, right, "CityScreen__RawYields")
		self.addTextDropdown(screen, right, right, "CityScreen__RawYields_View")
		
		self.addSpacer(screen, right, "CityScreen_TopCenter")
		self.addCheckbox(screen, right, "CityScreen__WhipAssist")
		self.addCheckbox(screen, right, "CityScreen__WhipAssistOverflowCountCurrentProduction")
		self.addCheckbox(screen, right, "CityScreen__Anger_Counter")
		
		self.addSpacer(screen, right, "CityScreen_Bottom")
		self.addCheckbox(screen, right, "CityScreen__CultureTurns")
		self.addCheckbox(screen, right, "CityScreen__GreatPersonTurns")
		self.addCheckbox(screen, right, "CityScreen__GreatPersonInfo")
		self.addTextDropdown(screen, right, right, "CityScreen__Specialists")

		screen.attachHSeparator(column, column + "Sep")
		left, right = self.addTwoColumnLayout(screen, column, "Bottom", False)
		self.addCheckbox(screen, left, "MainInterface__OptionsKey")
		screen.setLayoutFlag(right, "LAYOUT_RIGHT")
		screen.setLayoutFlag(right, "LAYOUT_SIZE_HPREFERREDEXPANDING")
		self.addLabel(screen, right, "Version", 
					  CvModName.getDisplayNameAndVersion() + " (" + CvModName.getCivNameAndVersion() + ")")
