## BugCityScreenOptionsTab
##
## Tab for the BUG City Screen Options (City Screen).
##
## Copyright (c) 2007-2008 The BUG Mod.
##
## Author: EmperorFool

import BugOptionsTab
import CvModName

class BugCityScreenOptionsTab(BugOptionsTab.BugOptionsTab):
	"BUG City Screen Options Screen Tab"
	
	def __init__(self, screen):
		BugOptionsTab.BugOptionsTab.__init__(self, "CityScreen", "City Screen")

	def create(self, screen):
		tab = self.createTab(screen)
		panel = self.createMainPanel(screen)
		column = self.addOneColumnLayout(screen, panel)
		
		left, right = self.addTwoColumnLayout(screen, column, "Page", True)
		
		#self.addLabel(screen, left, "CityScreen", "CITY SCREEN")
		self.addCheckbox(screen, left, "CityScreen__WhipAssist")
		self.addCheckbox(screen, left, "CityScreen__WhipAssistOverflowCountCurrentProduction")
		self.addCheckbox(screen, left, "CityScreen__Anger_Counter")
		
		self.addSpacer(screen, left, "CityScreen1")
		self.addCheckbox(screen, left, "CityScreen__RawYields")
		self.addTextDropdown(screen, left, left, "CityScreen__RawYields_View", True)
		
		self.addSpacer(screen, left, "CityScreen2")
		self.addLabel(screen, left, "Misc", "Misc:")
		self.addCheckbox(screen, left, "CityScreen__CultureTurns")
		self.addCheckbox(screen, left, "CityScreen__GreatPersonTurns")
		self.addCheckbox(screen, left, "CityScreen__GreatPersonInfo")
		self.addCheckbox(screen, left, "CityScreen__FoodAssist")
		self.addCheckbox(screen, left, "MainInterface__ProgressBarsTickMarks")
		self.addTextDropdown(screen, left, left, "CityScreen__Specialists", True)
		
		self.addLabel(screen, right, "Citybar", "City Bar Hover:")
		rightL, rightR = self.addTwoColumnLayout(screen, right, "Right", False)
		
		self.addCheckbox(screen, rightL, "CityBar__BaseValues")
		self.addCheckbox(screen, rightL, "CityBar__Health")
		self.addCheckbox(screen, rightL, "CityBar__Happiness")
		self.addCheckbox(screen, rightL, "CityBar__FoodAssist")
		self.addCheckbox(screen, rightL, "CityBar__BaseProduction")
		self.addCheckbox(screen, rightL, "CityBar__TradeDetail")
		self.addCheckbox(screen, rightL, "CityBar__Commerce")
		self.addCheckbox(screen, rightL, "CityBar__CultureTurns")
		self.addCheckbox(screen, rightL, "CityBar__GreatPersonTurns")
		
		self.addCheckbox(screen, rightR, "CityBar__HurryAssist")
		self.addLabel(screen, rightR, "CityAnger", "City Anger:")
		self.addCheckbox(screen, rightR, "CityBar__HurryAnger")
		self.addCheckbox(screen, rightR, "CityBar__DraftAnger")
		
		self.addSpacer(screen, rightR, "CityScreen3")
		self.addCheckbox(screen, rightR, "CityBar__Specialists")
		self.addCheckbox(screen, rightR, "CityBar__BuildingIcons")		
		self.addCheckbox(screen, rightR, "CityBar__AirportIcons")
		self.addCheckbox(screen, rightR, "CityBar__HideInstructions")
