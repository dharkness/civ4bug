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
		
		screen.attachLabel(leftPanel, "General_CityLabel", "City Screen:")
		self.addCheckbox(screen, leftPanel, "City_RawCommerce")
		self.addCheckbox(screen, leftPanel, "City_StackSpecialists")
		
		screen.attachLabel(leftPanel, "NJAGC_RegularLabel", "Technology Chooser:")
		self.addCheckbox(screen, leftPanel, "Tech_GPPrefs")
