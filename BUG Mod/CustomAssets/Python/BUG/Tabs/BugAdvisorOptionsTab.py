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
		left, center, right = self.addThreeColumnLayout(screen, panel, panel, True)
		
		self.addLabel(screen, left, "Domestic_Advisor", "Domestic [F1]:")
		self.addCheckbox(screen, left, "Advisors__CustDomAdv")

		self.addSpacer(screen, left, "Foreign_Advisor")
		self.addLabel(screen, left, "Foreign_Advisor", "Foreign [F4]:")
		self.addCheckbox(screen, left, "Advisors__EFAGlanceTab")
		self.addCheckbox(screen, left, "Advisors__EFAGlanceSmilies")
		
		self.addLabel(screen, left, "Military_Advisor", "Military [F5]:")
		self.addCheckbox(screen, left, "Advisors__BugMA")

		self.addSpacer(screen, left, "Technology_Advisor")
		self.addLabel(screen, left, "Technology_Advisor", "Technology [F6]:")
		self.addCheckbox(screen, left, "Advisors__GPTechPrefs")
		self.addCheckbox(screen, left, "Advisors__WideTechScreen")

		self.addLabel(screen, center, "Victory_Conditions", "Victory [F8]:")
		self.addCheckbox(screen, center, "Advisors__BugVictoriesTab")
		self.addCheckbox(screen, center, "Advisors__BugMembersTab")

		self.addLabel(screen, center, "Info_Screens", "Info [F9]:")
		self.addCheckbox(screen, center, "Advisors__BugGraphsTab")

		self.addSpacer(screen, center, "Sevopedia")
		self.addLabel(screen, center, "Sevopedia", "Sevopedia [F12]:")
		self.addCheckbox(screen, center, "Advisors__Sevopedia")
		self.addCheckbox(screen, center, "Advisors__SevopediaSortItemList")

		self.addLabel(screen, right, "Espionage_Screen", "Espionage [CTRL + E]:")
		self.addCheckbox(screen, right, "BetterEspionage__Enabled")
		
		self.addLabel(screen, right, "Espionage_Ratio", "Ratio:")
		rightL, rightR = self.addTwoColumnLayout(screen, right, "Espionage_Screen_Column")
		self.addColorDropdown(screen, rightL, rightR, "BetterEspionage__DefaultRatioColor", True)
		self.addFloatDropdown(screen, rightL, rightR, "BetterEspionage__GoodRatioCutoff", True, "LAYOUT_LEFT")
		self.addColorDropdown(screen, rightL, rightR, "BetterEspionage__GoodRatioColor", True)
		self.addFloatDropdown(screen, rightL, rightR, "BetterEspionage__BadRatioCutoff", True, "LAYOUT_LEFT")
		self.addColorDropdown(screen, rightL, rightR, "BetterEspionage__BadRatioColor", True)
		
		self.addLabel(screen, rightL, "Espionage_Missions", "Missions:")
		self.addSpacer(screen, rightR, "Espionage_Missions")
		self.addColorDropdown(screen, rightL, rightR, "BetterEspionage__PossibleMissionColor", True)
		self.addFloatDropdown(screen, rightL, rightR, "BetterEspionage__CloseMissionPercent", True, "LAYOUT_LEFT")
		self.addColorDropdown(screen, rightL, rightR, "BetterEspionage__CloseMissionColor", True)
		
		self.addSpacer(screen, right, "Advisors_Tab")
