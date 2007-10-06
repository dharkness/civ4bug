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
		
		screen.attachLabel(rightPanel, "CityScreenLabel", "City Screen:")
		screen.setControlFlag("CityScreenLabel", "CF_LABEL_DEFAULTSIZE")
		self.addCheckbox(screen, rightPanel, "City_RawCommerce")
		self.addCheckbox(screen, rightPanel, "City_CultureTurns")
		self.addCheckbox(screen, rightPanel, "City_GreatPersonTurns")
#		self.addCheckbox(screen, rightPanel, "City_StackSpecialists")

		screen.attachHSeparator(column, column + "Sep")
		self.addCheckbox(screen, column, "Main_OptionsKey")
