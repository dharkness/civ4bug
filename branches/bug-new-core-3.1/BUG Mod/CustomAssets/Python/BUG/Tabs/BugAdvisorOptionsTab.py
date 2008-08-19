## BugAdvisorOptionsTab
##
## Tab for the BUG Advisor Options.
##
## Copyright (c) 2007-2008 The BUG Mod.
##
## Author: EmperorFool

import BugOptionsTab

class BugAdvisorOptionsTab(BugOptionsTab.BugOptionsTab):
	"BUG General Options Screen Tab"
	
	def __init__(self, screen):
		BugOptionsTab.BugOptionsTab.__init__(self, "Advisors", "Advisors")

	def create(self, screen):
		tab = self.createTab(screen)
		panel = self.createMainPanel(screen)
		column = self.addOneColumnLayout(screen, panel)
		
		left, center, right = self.addThreeColumnLayout(screen, column, column, True)
		
		self.addLabel(screen, left, "Domestic_Advisor", "Domestic [F1]:")
		self.addCheckbox(screen, left, "Advisors__CustDomAdv")

		self.addLabel(screen, left, "Foreign_Advisor", "Foreign [F4]:")
		self.addCheckbox(screen, left, "Advisors__EFAGlanceTab")
		self.addCheckbox(screen, left, "Advisors__EFAGlanceSmilies")
		
		self.addLabel(screen, left, "Military_Advisor", "Military [F5]:")
		self.addCheckbox(screen, left, "Advisors__BugMA")

		self.addLabel(screen, left, "Technology_Advisor", "Technology [F6]:")
		self.addCheckbox(screen, left, "Advisors__GPTechPrefs")
		self.addCheckbox(screen, left, "Advisors__WideTechScreen")

		self.addLabel(screen, center, "Victory_Conditions", "Victory [F8]:")
		self.addCheckbox(screen, center, "Advisors__BugVictoriesTab")
		self.addCheckbox(screen, center, "Advisors__BugMembersTab")

		self.addLabel(screen, center, "Sevopedia", "Sevopedia [F12]:")
		self.addCheckbox(screen, center, "Advisors__Sevopedia")
		self.addCheckbox(screen, center, "Advisors__SevopediaSortItemList")

		self.addLabel(screen, right, "Espionage_Screen", "Espionage [CTRL + E]:")
		self.addCheckbox(screen, right, "BetterEspionage__Enabled")
		
		self.addLabel(screen, right, "Espionage_Ratio", "Ratio:")
		self.addColorDropdown(screen, right, right, "BetterEspionage__RatioColor", True)
		self.addFloatDropdown(screen, right, right, "BetterEspionage__GoodRatio", True)
		self.addColorDropdown(screen, right, right, "BetterEspionage__GoodColor", True)
		self.addFloatDropdown(screen, right, right, "BetterEspionage__BadRatio", True)
		self.addColorDropdown(screen, right, right, "BetterEspionage__BadColor", True)
		
		self.addLabel(screen, right, "Espionage_Missions", "Missions:")
		self.addColorDropdown(screen, right, right, "BetterEspionage__PossibleColor", True)
		self.addFloatDropdown(screen, right, right, "BetterEspionage__ClosePercent", True)
		self.addColorDropdown(screen, right, right, "BetterEspionage__CloseColor", True)