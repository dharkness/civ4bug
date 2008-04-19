## BugAdvisorOptionsTab
## Tab for the BUG Scoreboard Options
## BUG Mod - Copyright 2007

import BugOptionsTab

class BugAdvisorOptionsTab(BugOptionsTab.BugOptionsTab):
	"BUG General Options Screen Tab"
	
	def __init__(self, screen):
		BugOptionsTab.BugOptionsTab.__init__(self, "Advisor", "Advisors")

	def create(self, screen):
		tab = self.createTab(screen)
		panel = self.createMainPanel(screen)
		column = self.addOneColumnLayout(screen, panel)
		
		leftPanel, rightPanel = self.addTwoColumnLayout(screen, column, column, True)
		
		self.addLabel(screen, leftPanel, "Domestic_Advisor", "Domestic (F1):")
		self.addCheckbox(screen, leftPanel, "CDA_Enabled")

		self.addLabel(screen, leftPanel, "Foreign_Advisor", "Foreign (F4):")
		self.addCheckbox(screen, leftPanel, "EFA_Glance")
		self.addCheckbox(screen, leftPanel, "EFA_Glance_Smilies")
		
		self.addLabel(screen, leftPanel, "Technology_Advisor", "Technology (F6):")
		self.addCheckbox(screen, leftPanel, "Tech_GPPrefs")
		self.addCheckbox(screen, leftPanel, "TechScreen_Wide")

		self.addLabel(screen, leftPanel, "Sevopedia", "Sevopdia (F12):")
		self.addCheckbox(screen, leftPanel, "Sevopedia_Enabled")
		self.addCheckbox(screen, leftPanel, "Sevopedia_Sort")
		
		self.addLabel(screen, rightPanel, "Espionage_Screen", "Espionage (Ctrl-E):")
		self.addCheckbox(screen, rightPanel, "Espionage_Enabled")
		self.addColorDropdown(screen, rightPanel, rightPanel, "Espionage_RatioColor", True)
		self.addFloatDropdown(screen, rightPanel, rightPanel, "Espionage_GoodRatio", True)
		self.addColorDropdown(screen, rightPanel, rightPanel, "Espionage_GoodColor", True)
		self.addFloatDropdown(screen, rightPanel, rightPanel, "Espionage_BadRatio", True)
		self.addColorDropdown(screen, rightPanel, rightPanel, "Espionage_BadColor", True)
		
		self.addColorDropdown(screen, rightPanel, rightPanel, "Espionage_PossibleColor", True)
		self.addFloatDropdown(screen, rightPanel, rightPanel, "Espionage_ClosePercent", True)
		self.addColorDropdown(screen, rightPanel, rightPanel, "Espionage_CloseColor", True)
