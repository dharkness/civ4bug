## BugCityScreenOptionsTab
##
## Tab for the BUG City Screen Options.
##
## Copyright (c) 2007-2008 The BUG Mod.
##
## Author: EmperorFool

import BugOptionsTab

class BugCityScreenOptionsTab(BugOptionsTab.BugOptionsTab):
	"BUG City Screen Options Screen Tab"
	
	def __init__(self, screen):
		BugOptionsTab.BugOptionsTab.__init__(self, "CityScreen", "City Screen")

	def create(self, screen):
		tab = self.createTab(screen)
		panel = self.createMainPanel(screen)
		column = self.addOneColumnLayout(screen, panel)
		
		left, right = self.addTwoColumnLayout(screen, column, "Page", True)
		
		#self.addCheckboxTextDropdown(screen, left, left, "CityScreen__RawYields", "CityScreen__RawYields_View")
		self.addCheckbox(screen, left, "CityScreen__RawYields")
		self.addTextDropdown(screen, left, left, "CityScreen__RawYields_View", True)
		
		self.addSpacer(screen, left, "CityScreen1")
		self.addLabel(screen, left, "HurryDetail", "Hurry Detail:")
		leftL, leftR = self.addTwoColumnLayout(screen, left, "WhipBuyInfo", False)
		self.addCheckbox(screen, leftL, "CityBar__HurryAssist")
		self.addCheckbox(screen, leftR, "CityBar__HurryAssistIncludeCurrent")
		self.addCheckbox(screen, leftL, "CityScreen__WhipAssist")
		self.addCheckbox(screen, leftR, "CityScreen__WhipAssistOverflowCountCurrentProduction")
		self.addCheckbox(screen, leftL, "MiscHover__HurryOverflow")
		self.addCheckbox(screen, leftR, "MiscHover__HurryOverflowIncludeCurrent")
		
		self.addSpacer(screen, left, "CityScreen2")
		self.addLabel(screen, left, "BuildingEffects", "Building Actual Effects in Hovers:")
		leftL, leftR = self.addTwoColumnLayout(screen, left, "BuildingEffects", False)
		self.addCheckbox(screen, leftL, "MiscHover__BuildingAdditionalFood")
		self.addCheckbox(screen, leftL, "MiscHover__BuildingAdditionalProduction")
		self.addCheckbox(screen, leftL, "MiscHover__BuildingAdditionalCommerce")
		self.addCheckbox(screen, leftL, "MiscHover__BuildingSavedMaintenance")
		self.addCheckbox(screen, leftR, "MiscHover__BuildingAdditionalHealth")
		self.addCheckbox(screen, leftR, "MiscHover__BuildingAdditionalHappiness")
		self.addCheckbox(screen, leftR, "MiscHover__BuildingAdditionalGreatPeople")
		self.addCheckbox(screen, leftR, "MiscHover__BuildingActualEffects")
		
		self.addSpacer(screen, left, "CityScreen3")
		self.addLabel(screen, left, "GreatPersonBar", "Great Person Bar:")
		self.addCheckbox(screen, left, "CityScreen__GreatPersonTurns")
		self.addCheckbox(screen, left, "CityScreen__GreatPersonInfo")
		self.addCheckbox(screen, left, "MiscHover__GreatPeopleRateBreakdown")
		
		self.addSpacer(screen, left, "CityScreen4")
		self.addLabel(screen, left, "ProductionDecay", "Production Decay:")
		leftL, leftC, leftR = self.addThreeColumnLayout(screen, left, "ProductionDecay")
		self.addSpacer(screen, leftL, "CityScreen41")
		self.addCheckbox(screen, leftC, "CityScreen__ProductionDecayQueue")
		self.addCheckbox(screen, leftR, "CityScreen__ProductionDecayHover")
		#leftLL, leftLR = self.addTwoColumnLayout(screen, leftL, "ProductionDecayQueue")
		self.addIntDropdown(screen, leftL, leftC, "CityScreen__ProductionDecayQueueUnitThreshold")
		self.addIntDropdown(screen, leftL, leftC, "CityScreen__ProductionDecayQueueBuildingThreshold")
		#leftRL, leftRR = self.addTwoColumnLayout(screen, leftR, "ProductionDecayHover")
		self.addIntDropdown(screen, None, leftR, "CityScreen__ProductionDecayHoverUnitThreshold")
		self.addIntDropdown(screen, None, leftR, "CityScreen__ProductionDecayHoverBuildingThreshold")
		
		
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
		
		self.addLabel(screen, rightR, "Cityanger", "City Anger:")
		self.addCheckbox(screen, rightR, "CityBar__HurryAnger")
		self.addCheckbox(screen, rightR, "CityBar__DraftAnger")
		
		self.addSpacer(screen, rightR, "CityScreen5")
		self.addCheckbox(screen, rightR, "CityBar__BuildingIcons")
		self.addCheckbox(screen, rightR, "CityBar__Specialists")
		self.addCheckbox(screen, rightR, "CityBar__HideInstructions")
		#self.addCheckbox(screen, rightR, "CityBar__AirportIcons")
		
		self.addSpacer(screen, right, "CityScreen6")
		self.addLabel(screen, right, "Misc", "Miscellaneous:")
		self.addCheckbox(screen, right, "MiscHover__BaseCommerce")
		self.addCheckbox(screen, right, "CityScreen__FoodAssist")
		self.addCheckbox(screen, right, "CityScreen__Anger_Counter")
		self.addCheckbox(screen, right, "CityScreen__CultureTurns")
		self.addCheckbox(screen, right, "MainInterface__ProgressBarsTickMarks")
		self.addTextDropdown(screen, right, right, "CityScreen__Specialists", True)
		#self.addCheckbox(screen, right, "MiscHover__RemoveSpecialist")
