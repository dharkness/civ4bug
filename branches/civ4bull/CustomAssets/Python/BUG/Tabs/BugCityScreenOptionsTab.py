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
		#self.addLabel(screen, left, "Misc", "Misc:")
		self.addCheckbox(screen, left, "CityScreen__CultureTurns")
		self.addCheckbox(screen, left, "CityScreen__GreatPersonTurns")
		self.addCheckbox(screen, left, "CityScreen__GreatPersonInfo")
		self.addCheckbox(screen, left, "CityScreen__FoodAssist")
		self.addCheckbox(screen, left, "MainInterface__ProgressBarsTickMarks")
		self.addTextDropdown(screen, left, left, "CityScreen__Specialists", True)
		
		left2, right2 = self.addTwoColumnLayout(screen, right, "Right", False)
		
		self.addCheckbox(screen, left2, "CityBar__AirportIcons")
		self.addSpacer(screen, right2, "")
		
		self.addLabel(screen, left2, "Hover", "City Bar Hover:")
		self.addSpacer(screen, right2, "")
		
		self.addCheckbox(screen, left2, "CityBar__Health")
		self.addCheckbox(screen, right2, "CityBar__Happiness")
		self.addCheckbox(screen, left2, "CityBar__HurryAnger")
		self.addCheckbox(screen, right2, "CityBar__DraftAnger")
		
		self.addCheckbox(screen, left2, "CityBar__FoodAssist")
		self.addSpacer(screen, right2, "")
		self.addCheckbox(screen, left2, "CityBar__BaseProduction")
		self.addCheckbox(screen, right2, "CityBar__BaseValues")
		
		self.addCheckbox(screen, left2, "CityBar__HurryAssist")
		self.addSpacer(screen, right2, "")
		self.addCheckbox(screen, left2, "CityBar__TradeDetail")
		self.addCheckbox(screen, right2, "CityBar__Commerce")
		
		self.addCheckbox(screen, left2, "CityBar__BuildingIcons")
		self.addSpacer(screen, right2, "")
		self.addCheckbox(screen, left2, "CityBar__CultureTurns")
		self.addCheckbox(screen, right2, "CityBar__GreatPersonTurns")
		self.addCheckbox(screen, left2, "CityBar__Specialists")
		
		self.addCheckbox(screen, left2, "CityBar__HideInstructions")
