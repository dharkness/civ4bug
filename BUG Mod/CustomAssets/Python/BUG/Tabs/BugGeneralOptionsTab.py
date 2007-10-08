## BugGeneralOptionsTab
## Tab for the BUG Scoreboard Options
## BUG Mod - Copyright 2007

import BugOptionsTab
import CvModName

class BugGeneralOptionsTab(BugOptionsTab.BugOptionsTab):
	"BUG General Options Screen Tab"
	
	def __init__(self, screen):
		BugOptionsTab.BugOptionsTab.__init__(self, "General", "General")

	def create(self, screen):
		tab = self.createTab(screen)
		panel = self.createMainPanel(screen)
		column = self.addOneColumnLayout(screen, panel)

		left, right = self.addTwoColumnLayout(screen, column, "Top", True)

		screen.attachLabel(left, "MainInterfaceLabel", "Main Interface:")
		screen.setControlFlag("MainInterfaceLabel", "CF_LABEL_DEFAULTSIZE")
		self.addCheckbox(screen, left, "Main_GPBar")
		self.addCheckbox(screen, left, "Main_CityArrows")
		self.addCheckbox(screen, left, "Main_Combat_Counter")
		self.addCheckbox(screen, left, "Unit_Promo_Available")
		self.addCheckbox(screen, left, "Unit_Actions")

		screen.attachLabel(right, "CityScreenLabel", "City Screen:")
		screen.setControlFlag("CityScreenLabel", "CF_LABEL_DEFAULTSIZE")
		self.addCheckbox(screen, right, "City_RawCommerce")
		self.addCheckbox(screen, right, "City_CultureTurns")
		self.addCheckbox(screen, right, "City_GreatPersonTurns")
#		self.addCheckbox(screen, right, "City_StackSpecialists")

		screen.attachHSeparator(column, column + "Sep")
		left, right = self.addTwoColumnLayout(screen, column, "Bottom", False)
		self.addCheckbox(screen, left, "Main_OptionsKey")
		screen.setLayoutFlag(right, "LAYOUT_RIGHT")
		screen.setLayoutFlag(right, "LAYOUT_SIZE_HPREFERREDEXPANDING")
		screen.attachLabel(right, "VersionLabel", 
						   CvModName.getNameAndVersion() + " (" + CvModName.getCivNameAndVersion() + ")")
		screen.setControlFlag("VersionLabel", "CF_LABEL_DEFAULTSIZE")
