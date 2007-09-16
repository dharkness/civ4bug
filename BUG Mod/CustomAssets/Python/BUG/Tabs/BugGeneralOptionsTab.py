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
		column = self.addOneColumnLayout(screen, panel)
		
		leftPanel, rightPanel = self.addTwoColumnLayout(screen, column, column, True)
		
		screen.attachLabel(leftPanel, "MainInterfaceLabel", "Main Interface:")
		screen.setControlFlag("MainInterfaceLabel", "CF_LABEL_DEFAULTSIZE")
		self.addCheckbox(screen, leftPanel, "Main_GPBar")
		self.addCheckbox(screen, leftPanel, "Main_CityArrows")
		
		screen.attachLabel(leftPanel, "CityScreenLabel", "City Screen:")
		screen.setControlFlag("CityScreenLabel", "CF_LABEL_DEFAULTSIZE")
		self.addCheckbox(screen, leftPanel, "City_RawCommerce")
		self.addCheckbox(screen, leftPanel, "City_CultureTurns")
		self.addCheckbox(screen, leftPanel, "City_GreatPersonTurns")
#		self.addCheckbox(screen, leftPanel, "City_StackSpecialists")
		
		screen.attachLabel(leftPanel, "DomAdvScreenLabel", "Domestic Advisor:")
		screen.setControlFlag("DomAdvScreenLabel", "CF_LABEL_DEFAULTSIZE")
		self.addCheckbox(screen, leftPanel, "CDA_Enabled")
		
		screen.attachLabel(leftPanel, "TechScreenLabel", "Technology Advisor:")
		screen.setControlFlag("TechScreenLabel", "CF_LABEL_DEFAULTSIZE")
		self.addCheckbox(screen, leftPanel, "Tech_GPPrefs")
		
		screen.attachLabel(rightPanel, "EspionageScreenLabel", "Espionage Screen:")
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
		
		screen.attachHSeparator(column, column + "Sep")
		self.addCheckbox(screen, column, "Main_OptionsKey")
