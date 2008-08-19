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

		self.addLabel(screen, left, "Main__Interface", "Main Interface:")
		self.addCheckbox(screen, left, "Main__GPBar")
		self.addTextDropdown(screen, left, left, "Main__GPBar_Types")
		self.addCheckbox(screen, left, "Main__Combat_Counter")
		self.addCheckbox(screen, left, "Main__CityArrows")

		self.addLabel(screen, right, "CityScreen", "City Screen:")
		self.addCheckbox(screen, right, "City__RawYields")
		self.addTextDropdown(screen, right, right, "City__RawYields_View")
		self.addCheckbox(screen, right, "City__WhipAssist")
		self.addCheckbox(screen, right, "City__WhipAssistOverflowCountCurrentProduction")
		self.addCheckbox(screen, right, "City__Anger_Counter")
		self.addCheckbox(screen, right, "City__CultureTurns")
		self.addCheckbox(screen, right, "City__GreatPersonTurns")
		self.addCheckbox(screen, right, "City__GreatPersonInfo")
		self.addTextDropdown(screen, right, right, "City__Specialists")

		screen.attachHSeparator(column, column + "Sep")
		left, right = self.addTwoColumnLayout(screen, column, "Bottom", False)
		self.addCheckbox(screen, left, "Main__OptionsKey")
		screen.setLayoutFlag(right, "LAYOUT_RIGHT")
		screen.setLayoutFlag(right, "LAYOUT_SIZE_HPREFERREDEXPANDING")
		self.addLabel(screen, right, "Version", 
					  CvModName.getDisplayNameAndVersion() + " (" + CvModName.getCivNameAndVersion() + ")")
