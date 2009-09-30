## BugGeneralOptionsTab
##
## Tab for the BUG General Options (Main and City Screens).
##
## Copyright (c) 2007-2008 The BUG Mod.
##
## Author: EmperorFool

import BugOptionsTab

class BugGeneralOptionsTab(BugOptionsTab.BugOptionsTab):
	"BUG General Options Screen Tab"
	
	def __init__(self, screen):
		BugOptionsTab.BugOptionsTab.__init__(self, "General", "General")

	def create(self, screen):
		tab = self.createTab(screen)
		panel = self.createMainPanel(screen)
		column = self.addOneColumnLayout(screen, panel)
		
		left, right = self.addTwoColumnLayout(screen, column, "Top", True)
		
		self.addCheckboxTextDropdown(screen, left, left, "MainInterface__GPBar", "MainInterface__GPBar_Types")
		#self.addCheckbox(screen, left, "MainInterface__GPBar")
		#self.addTextDropdown(screen, left, left, "MainInterface__GPBar_Types", True)
		self.addCheckbox(screen, left, "MainInterface__Combat_Counter")
		
		self.addSpacer(screen, left, "General1")
		
		self.addLabel(screen, left, "AutoSave", "AutoSave:")
		self.addCheckbox(screen, left, "AutoSave__CreateStartSave")
		self.addCheckbox(screen, left, "AutoSave__CreateEndSave")
		self.addCheckbox(screen, left, "AutoSave__CreateExitSave")
		self.addCheckbox(screen, left, "AutoSave__UsePlayerName")
		
		self.addSpacer(screen, left, "General2")
		
		self.addLabel(screen, left, "Actions", "Actions:")
		self.addCheckbox(screen, left, "Actions__SentryHealing")
		self.addCheckbox(screen, left, "Actions__SentryHealingOnlyNeutral", True)
		self.addCheckbox(screen, left, "Actions__PreChopForests")
		self.addCheckbox(screen, left, "Actions__PreChopImprovements")
		
		
		self.addLabel(screen, right, "TechWindow", "Tech Splash Screen:")
		self.addTextDropdown(screen, right, right, "TechWindow__ViewType", True)
		self.addCheckbox(screen, right, "TechWindow__CivilopediaText")
		
		self.addSpacer(screen, right, "General3")
		
		self.addLabel(screen, right, "Misc", "Misc:")
		self.addCheckbox(screen, right, "MainInterface__GoldRateWarning")
		self.addCheckbox(screen, right, "MainInterface__MinMax_Commerce")
		self.addCheckbox(screen, right, "MainInterface__ProgressBarsTickMarks")
		self.addCheckbox(screen, right, "MainInterface__CityArrows")
		self.addCheckbox(screen, right, "MainInterface__UnitMovementPointsFraction")
		self.addCheckbox(screen, right, "MainInterface__StackMovementPoints")
		
		self.addCheckboxTextDropdown(screen, right, right, "ACO__Enabled", "ACO__Detail")
