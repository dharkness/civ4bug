## BugGeneralOptionsTab
## Tab for the BUG Scoreboard Options
## BUG Mod - Copyright 2007

import BugOptionsTab

class BugGeneralOptionsTab(BugOptionsTab.BugOptionsTab):
	"BUG General Options Screen Tab"
	
	def __init__(self, screen):
		BugOptionsTab.BugOptionsTab.__init__(self, "General", "General")

	def create(self, screen):
		tab = self.createTab(screen)
		panel = self.createMainPanel(screen)
		leftPanel, rightPanel = self.addTwoColumnLayout(screen, panel)
		
		self.addCheckbox(screen, leftPanel, "Screens_CDA")
		
		screen.attachLabel(leftPanel, "CityScreenLabel", "City Screen:")
		self.addCheckbox(screen, leftPanel, "City_RawCommerce")
		self.addCheckbox(screen, leftPanel, "City_CultureTurns")
		self.addCheckbox(screen, leftPanel, "City_GreatPersonTurns")
		self.addCheckbox(screen, leftPanel, "City_StackSpecialists")
		
		screen.attachLabel(leftPanel, "TechScreenLabel", "Technology Advisor:")
		self.addCheckbox(screen, leftPanel, "Screens_Tech_GPPrefs")
		
		screen.attachLabel(rightPanel, "EspionageScreenLabel", "Espionage Screen:")
		self.addCheckbox(screen, rightPanel, "Screens_Espionage_Better")
		self.addFloatDropdown(screen, rightPanel, rightPanel, "Screens_Espionage_BadRatio", True)
		self.addFloatDropdown(screen, rightPanel, rightPanel, "Screens_Espionage_GoodRatio", True)
