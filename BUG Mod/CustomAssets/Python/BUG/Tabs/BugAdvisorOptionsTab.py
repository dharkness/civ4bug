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
		left, center, right = self.addThreeColumnLayout(screen, panel, panel, True)
		
		self.addLabel(screen, left, "Domestic_Advisor", "Domestic (F1):")
		self.addCheckbox(screen, left, "CDA_Enabled")

		self.addSpacer(screen, left, "Foreign_Advisor")
		self.addSpacer(screen, left, "Foreign_Advisor")
		self.addLabel(screen, left, "Foreign_Advisor", "Foreign (F4):")
		self.addCheckbox(screen, left, "EFA_Glance")
		self.addCheckbox(screen, left, "EFA_Glance_Smilies")
		
		self.addSpacer(screen, left, "Military_Advisor")
		self.addLabel(screen, left, "Military_Advisor", "Military (F5):")
		self.addCheckbox(screen, left, "BMA_Enabled")

		self.addLabel(screen, center, "Technology_Advisor", "Technology (F6):")
		self.addCheckbox(screen, center, "Tech_GPPrefs")
		self.addCheckbox(screen, center, "TechScreen_Wide")

		self.addSpacer(screen, center, "Victory_Conditions")
		self.addLabel(screen, center, "Victory_Conditions", "Victory:")
		self.addCheckbox(screen, center, "Victories_Enabled")
		self.addCheckbox(screen, center, "Members_Enabled")

		self.addSpacer(screen, center, "Sevopedia")
		self.addLabel(screen, center, "Sevopedia", "Sevopdia (F12):")
		self.addCheckbox(screen, center, "Sevopedia_Enabled")
		self.addCheckbox(screen, center, "Sevopedia_Sort")

		self.addLabel(screen, right, "Espionage_Screen", "Espionage (Ctrl-E):")
		self.addCheckbox(screen, right, "Espionage_Enabled")
		
		self.addLabel(screen, right, "Espionage_Ratio", "Ratio:")
		self.addColorDropdown(screen, right, right, "Espionage_RatioColor", True)
		self.addFloatDropdown(screen, right, right, "Espionage_GoodRatio", True)
		self.addColorDropdown(screen, right, right, "Espionage_GoodColor", True)
		self.addFloatDropdown(screen, right, right, "Espionage_BadRatio", True)
		self.addColorDropdown(screen, right, right, "Espionage_BadColor", True)
		
		self.addLabel(screen, right, "Espionage_Missions", "Missions:")
		self.addColorDropdown(screen, right, right, "Espionage_PossibleColor", True)
		self.addFloatDropdown(screen, right, right, "Espionage_ClosePercent", True)
		self.addColorDropdown(screen, right, right, "Espionage_CloseColor", True)
