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
		
		self.createGreatPersonGeneralPanel(screen, left)
		self.addSpacer(screen, left, "General1")
		self.createTechSplashPanel(screen, left)
		self.addSpacer(screen, left, "General2")
		self.createActionsPanel(screen, left)
		
		self.createAutoSavePanel(screen, right)
		self.addSpacer(screen, right, "General3")
		self.createMiscellaneousPanel(screen, right)
		
	def createGreatPersonGeneralPanel(self, screen, panel):
		self.addLabel(screen, panel, "ProgressBars", "Progress Bars:")
		self.addCheckboxTextDropdown(screen, panel, panel, "MainInterface__GPBar", "MainInterface__GPBar_Types")
		#self.addCheckbox(screen, panel, "MainInterface__GPBar")
		#self.addTextDropdown(screen, panel, panel, "MainInterface__GPBar_Types", True)
		self.addCheckbox(screen, panel, "MainInterface__Combat_Counter")
		
	def createAutoSavePanel(self, screen, panel):
		self.addLabel(screen, panel, "AutoSave", "AutoSave:")
		self.addCheckbox(screen, panel, "AutoSave__CreateStartSave")
		self.addCheckbox(screen, panel, "AutoSave__CreateEndSave")
		self.addCheckbox(screen, panel, "AutoSave__CreateExitSave")
		self.addCheckbox(screen, panel, "AutoSave__UsePlayerName")
		
	def createActionsPanel(self, screen, panel):
		self.addLabel(screen, panel, "Actions", "Actions:")
		self.addCheckbox(screen, panel, "Actions__DeclareWarUnits")
		self.addCheckbox(screen, panel, "Actions__SentryHealing")
		self.addCheckbox(screen, panel, "Actions__SentryHealingOnlyNeutral", True)
		self.addCheckbox(screen, panel, "Actions__PreChopForests")
		self.addCheckbox(screen, panel, "Actions__PreChopImprovements")
		
	def createTechSplashPanel(self, screen, panel):
		self.addLabel(screen, panel, "TechWindow", "Tech Splash Screen:")
		self.addTextDropdown(screen, panel, panel, "TechWindow__ViewType", True)
		self.addCheckbox(screen, panel, "TechWindow__CivilopediaText")
		
	def createMiscellaneousPanel(self, screen, panel):
		self.addLabel(screen, panel, "Misc", "Misc:")
		self.addCheckbox(screen, panel, "MainInterface__GoldRateWarning")
		self.addCheckbox(screen, panel, "MainInterface__MinMax_Commerce")
		self.addCheckbox(screen, panel, "MainInterface__ProgressBarsTickMarks")
		self.addCheckbox(screen, panel, "MainInterface__CityArrows")
		self.addCheckbox(screen, panel, "MainInterface__UnitMovementPointsFraction")
		self.addCheckbox(screen, panel, "MainInterface__StackMovementPoints")
