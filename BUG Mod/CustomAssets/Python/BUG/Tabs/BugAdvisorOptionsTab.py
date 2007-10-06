## BugGeneralOptionsTab
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
		
		screen.attachLabel(leftPanel, "DomAdvScreenLabel", "Domestic (F1):")
		screen.setControlFlag("DomAdvScreenLabel", "CF_LABEL_DEFAULTSIZE")
		self.addCheckbox(screen, leftPanel, "CDA_Enabled")
		
		screen.attachLabel(leftPanel, "TechScreenLabel", "Foreign (F4):")
		screen.setControlFlag("TechScreenLabel", "CF_LABEL_DEFAULTSIZE")
		self.addCheckbox(screen, leftPanel, "EFA_Glance")
		self.addCheckbox(screen, leftPanel, "EFA_Glance_Smilies")
		
		screen.attachLabel(leftPanel, "TechScreenLabel", "Technology (F6):")
		screen.setControlFlag("TechScreenLabel", "CF_LABEL_DEFAULTSIZE")
		self.addCheckbox(screen, leftPanel, "Tech_GPPrefs")

		screen.attachLabel(leftPanel, "SevopdiaLabel", "Sevopdia (F12):")
		screen.setControlFlag("SevopdiaLabel", "CF_LABEL_DEFAULTSIZE")
		self.addCheckbox(screen, leftPanel, "Sevopedia_Enabled")
		self.addCheckbox(screen, leftPanel, "Sevopedia_Sort")
		
		screen.attachLabel(rightPanel, "EspionageScreenLabel", "Espionage (Ctrl-E):")
		screen.setControlFlag("EspionageScreenLabel", "CF_LABEL_DEFAULTSIZE")
		self.addCheckbox(screen, rightPanel, "Espionage_Enabled")
		self.addColorDropdown(screen, rightPanel, rightPanel, "Espionage_RatioColor", True)
		self.addFloatDropdown(screen, rightPanel, rightPanel, "Espionage_GoodRatio", True)
		self.addColorDropdown(screen, rightPanel, rightPanel, "Espionage_GoodColor", True)
		self.addFloatDropdown(screen, rightPanel, rightPanel, "Espionage_BadRatio", True)
		self.addColorDropdown(screen, rightPanel, rightPanel, "Espionage_BadColor", True)
		
		self.addColorDropdown(screen, rightPanel, rightPanel, "Espionage_PossibleColor", True)
		self.addFloatDropdown(screen, rightPanel, rightPanel, "Espionage_ClosePercent", True)
		self.addColorDropdown(screen, rightPanel, rightPanel, "Espionage_CloseColor", True)
