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
		self.addCheckbox(screen, leftPanel, "Screens_Espionage")
		
		screen.attachLabel(leftPanel, "General_CityScreenLabel", "City Screen:")
		self.addCheckbox(screen, leftPanel, "City_RawCommerce")
		self.addCheckbox(screen, leftPanel, "City_CultureTurns")
		self.addCheckbox(screen, leftPanel, "City_GreatPersonTurns")
		self.addCheckbox(screen, leftPanel, "City_StackSpecialists")
		
		screen.attachLabel(leftPanel, "General_TechScreenLabel", "Technology Chooser:")
		self.addCheckbox(screen, leftPanel, "Tech_GPPrefs")
