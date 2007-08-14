## BugAlertsOptionsTab
## Tab for the BUG Civ4lerts and Reminders Options
## BUG Mod - Copyright 2007

import BugOptionsTab

class BugAlertsOptionsTab(BugOptionsTab.BugOptionsTab):
	"BUG NJAGC Options Screen Tab"
	
	def __init__(self, screen):
		BugOptionsTab.BugOptionsTab.__init__(self, "Alerts", "Alerts")

	def create(self, screen):
		tab = self.createTab(screen)
		panel = self.createMainPanel(screen)
		column = self.addOneColumnLayout(screen, panel)
		
		self.addCheckbox(screen, column, "Alert_Reminders")
		self.addCheckbox(screen, column, "Alert_Civ4lerts")
		
		screen.attachHSeparator(column, column + "Sep")
		cityPanel, rightPanel = self.addTwoColumnLayout(screen, column, "Civ4lerts", True)
		
		# Cities
		self.addCheckbox(screen, cityPanel, "Alert_CityPendingGrowth")
		self.addCheckbox(screen, cityPanel, "Alert_CityPendingUnhealthy")
		self.addCheckbox(screen, cityPanel, "Alert_CityPendingAngry")
		self.addCheckbox(screen, cityPanel, "Alert_CityGrowth")
		self.addCheckbox(screen, cityPanel, "Alert_CityUnhealthy")
		self.addCheckbox(screen, cityPanel, "Alert_CityAngry")
		self.addCheckbox(screen, cityPanel, "Alert_CityExpandBorder")
		
		# Trades
		screen.attachLabel(rightPanel, "Alert_TradeLabel", "Trade Opportunities:")
		screen.setControlFlag("Alert_TradeLabel", "CF_LABEL_DEFAULTSIZE")
		self.addCheckbox(screen, rightPanel, "Alert_TechTrade")
		
		self.addCheckboxIntDropdown(screen, rightPanel, rightPanel, "Alert_GoldTrade", "Alert_GoldTradeThresh")
		self.addCheckboxIntDropdown(screen, rightPanel, rightPanel, "Alert_GoldPerTurnTrade", "Alert_GoldPerTurnTradeThresh")
		
		# Victories
		screen.attachLabel(rightPanel, "Alert_VictoryLabel", "Victory Conditions:")
		screen.setControlFlag("Alert_VictoryLabel", "CF_LABEL_DEFAULTSIZE")
		
		self.addCheckboxFloatDropdown(screen, rightPanel, rightPanel, "Alert_DomPop", "Alert_DomPopThresh")
		self.addCheckboxFloatDropdown(screen, rightPanel, rightPanel, "Alert_DomLand", "Alert_DomLandThresh")
