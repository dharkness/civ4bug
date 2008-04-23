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

		self.addLabel(screen, left, "Main_Interface", "Main Interface:")
		self.addCheckbox(screen, left, "Main_GPBar")
		self.addTextDropdown(screen, left, left, "Main_GPBar_Types")
		self.addCheckbox(screen, left, "Main_Combat_Counter")
		self.addCheckbox(screen, left, "Main_CityArrows")
		self.addLabel(screen, left, "PlotList", "Unit Icons (Plot List):")
		self.addCheckbox(screen, left, "Unit_Promo_Available")
		self.addCheckbox(screen, left, "Unit_Actions")
		self.addCheckbox(screen, left, "Unit_Great_General")

		self.addLabel(screen, right, "CityScreen", "City Screen:")
		self.addCheckbox(screen, right, "City_RawCommerce")
		self.addCheckbox(screen, right, "City_CultureTurns")
		self.addCheckbox(screen, right, "City_GreatPersonTurns")
		self.addCheckbox(screen, right, "City_GreatPersonInfo")
		self.addCheckbox(screen, right, "City_Anger_Counter")
		self.addTextDropdown(screen, right, right, "City_Specialists")

		screen.attachHSeparator(column, column + "Sep")
		left, right = self.addTwoColumnLayout(screen, column, "Bottom", False)
		self.addCheckbox(screen, left, "Main_OptionsKey")
		screen.setLayoutFlag(right, "LAYOUT_RIGHT")
		screen.setLayoutFlag(right, "LAYOUT_SIZE_HPREFERREDEXPANDING")
		self.addLabel(screen, right, "Version", 
					  CvModName.getNameAndVersion() + " (" + CvModName.getCivNameAndVersion() + ")")
