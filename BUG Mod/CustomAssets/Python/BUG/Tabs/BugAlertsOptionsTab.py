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
		
		# Reminders
		left, right = self.addTwoColumnLayout(screen, column, "Main")
		self.addCheckbox(screen, left, "Alert_Reminders")
		self.addSpacer(screen, right, "Alert")
		self.addTextDropdown(screen, left, left, "Alert_RemindersMethod")
		self.addCheckbox(screen, right, "Alert_LogReminders")
		
		screen.attachHSeparator(column, column + "Sep")
		
		# Civ4lerts
		self.addCheckbox(screen, column, "Alert_Civ4lerts")
		left, center, right = self.addThreeColumnLayout(screen, column, "Civ4lerts", True)
		
		# Cities
		self.addLabel(screen, left, "Alert_City", "Cities:")
		comboBox = "Alert_ComboBoxGrowth"
		screen.attachHBox(left, comboBox)
		self.addCheckbox(screen, comboBox, "Alert_CityPendingGrowth")
		self.addCheckbox(screen, comboBox, "Alert_CityGrowth")
		comboBox = "Alert_ComboBoxHealthiness"
		screen.attachHBox(left, comboBox)
		self.addCheckbox(screen, comboBox, "Alert_CityPendingHealthiness")
		self.addCheckbox(screen, comboBox, "Alert_CityHealthiness")
		comboBox = "Alert_ComboBoxHappiness"
		screen.attachHBox(left, comboBox)
		self.addCheckbox(screen, comboBox, "Alert_CityPendingHappiness")
		self.addCheckbox(screen, comboBox, "Alert_CityHappiness")
		
		self.addCheckbox(screen, left, "Alert_CityPendingBorderExpansion")
		self.addCheckbox(screen, left, "Alert_CityCanHurryPop")
		self.addCheckbox(screen, left, "Alert_CityCanHurryGold")
		
		# Diplomacy
		self.addLabel(screen, center, "Alert_Diplomacy", "Diplomacy:")
		self.addCheckbox(screen, center, "Alert_OpenBordersTrade")
		self.addCheckbox(screen, center, "Alert_DefensivePactTrade")
		self.addCheckbox(screen, center, "Alert_PermanentAllianceTrade")
		
		# Trades
		self.addLabel(screen, right, "Alert_Trade", "Trading:")
		self.addCheckbox(screen, right, "Alert_TechTrade")
		
		self.addCheckboxIntDropdown(screen, right, right, "Alert_GoldTrade", "Alert_GoldTradeThresh")
		self.addCheckboxIntDropdown(screen, right, right, "Alert_GoldPerTurnTrade", "Alert_GoldPerTurnTradeThresh")
		
		# Victories
		self.addLabel(screen, right, "Alert_Victory", "Victory:")
		
		self.addCheckboxFloatDropdown(screen, right, right, "Alert_DomPop", "Alert_DomPopThresh")
		self.addCheckboxFloatDropdown(screen, right, right, "Alert_DomLand", "Alert_DomLandThresh")
