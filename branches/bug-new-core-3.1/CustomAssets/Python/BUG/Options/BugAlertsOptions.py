## BugAlertsOptions
## Facade for accessing Civ4lert and Reminder options
## BUG Mod - Copyright 2007

from BugOptions import OptionsFacade, Option, OptionList

class BugAlertsOptions(OptionsFacade):

	def __init__(self):
		OptionsFacade.__init__(self)
		self.addOption(Option("Alert_Reminders",
							  "CIV4LERTS", "Reminders", True,
							  "Enable Reminders [ALT + M]",
							  "When checked, you can create messages using [ALT + M] that are displayed in a specified number of turns using eotinb's Reminders mod."))
		self.addOption(OptionList("Alert_RemindersMethod",
								  "CIV4LERTS", "Reminder Display Method", 2,
								  "Display Method",
								  "Determines how reminders are displayed to you.\n- On-screen message with entry in the log\n- A modal popup message with the option to retrigger the event next turn\n- Both",
								  ['Message', 'Popup', 'Both'], None))
		self.addOption(Option("Alert_LogReminders",
							  "CIV4LERTS", "Log Reminders", True,
							  "Log w. Autolog",
							  "When checked, reminders will be logged using Autolog when created and triggered."))
		
		# Civ4lerts
		self.addOption(Option("Alert_Civ4lerts",
							  "CIV4LERTS", "Enabled", True,
							  "Enable Civ4lerts",
							  "When checked, messages are displayed to alert you to various pending and existing conditions using Dr. Elmer Jiggle's Civ4lerts mod."))
		
		# City
		self.addOption(Option("Alert_CityPendingGrowth",
							  "CIV4LERTS", "City Pending Growth", False,
							  "Pending",
							  "When checked, displays an alert when a city's population will grow or shrink next turn."))
		self.addOption(Option("Alert_CityPendingHappiness",
							  "CIV4LERTS", "City Pending Happiness", True,
							  "Pending",
							  "When checked, displays an alert when a city will become happy or unhappy next turn."))
		self.addOption(Option("Alert_CityPendingHealthiness",
							  "CIV4LERTS", "City Pending Healthiness", True,
							  "Pending",
							  "When checked, displays an alert when a city will become healthy or unhealthy next turn."))
		self.addOption(Option("Alert_CityPendingBorderExpansion",
							  "CIV4LERTS", "City Pending Border Expansion", True,
							  "Pending Border Expansion",
							  "When checked, displays an alert when a city will expand its curltural borders next turn."))
		self.addOption(Option("Alert_CityGrowth",
							  "CIV4LERTS", "City Growth", False,
							  "Growth",
							  "When checked, displays an alert when a city's population has grown or shrunk."))
		self.addOption(Option("Alert_CityHappiness",
							  "CIV4LERTS", "City Happiness", True,
							  "Happiness",
							  "When checked, displays an alert when a city has become happy or unhappy."))
		self.addOption(Option("Alert_CityHealthiness",
							  "CIV4LERTS", "City Healthiness", True,
							  "Healthiness",
							  "When checked, displays an alert when a city has become healthy or unhealthy."))
		self.addOption(Option("Alert_CityCanHurryPop",
							  "CIV4LERTS", "City Can Hurry Pop", True,
							  "Can Hurry w. Population",
							  "When checked, displays an alert once a city can hurry the item it's building with the whip."))
		self.addOption(Option("Alert_CityCanHurryGold",
							  "CIV4LERTS", "City Can Hurry Gold", True,
							  "Can Hurry w. Gold",
							  "When checked, displays an alert once a city can hurry the item it's building with gold."))
		
		# Trade
		self.addOption(Option("Alert_TechTrade",
							  "CIV4LERTS", "CheckForNewTrades", True,
							  "Technologies",
							  "."))
		self.addOption(Option("Alert_GoldTrade",
							  "CIV4LERTS", "Gold Trade", True,
							  "Gold",
							  "."))
		self.addOption(OptionList("Alert_GoldTradeThresh",
								  "CIV4LERTS", "Gold Trade Threshold", 50,
								  "Threshold",
								  ".",
								  [1,2,3,5,10,20,30,50,100,200,300,500,1000]))
		self.addOption(Option("Alert_GoldPerTurnTrade",
							  "CIV4LERTS", "Gold Per Turn Trade", True,
							  "Gold Per Turn",
							  "."))
		self.addOption(OptionList("Alert_GoldPerTurnTradeThresh",
								  "CIV4LERTS", "Gold Per Turn Threshold", 5,
								  "Threshold",
								  ".",
								  [1,2,3,5,10,15,20,25,30,50,100]))
		
		# Diplomacy
		self.addOption(Option("Alert_OpenBordersTrade",
							  "CIV4LERTS", "Open Borders Trades", True,
							  "Open Borders",
							  "."))
		self.addOption(Option("Alert_DefensivePactTrade",
							  "CIV4LERTS", "Defensive Pact Trades", True,
							  "Defensive Pact",
							  "."))
		self.addOption(Option("Alert_PermanentAllianceTrade",
							  "CIV4LERTS", "Permanent Alliance Trades", True,
							  "Permanent Alliance",
							  "."))
		
		# Victory
		self.addOption(Option("Alert_DomPop",
							  "CIV4LERTS", "CheckForDomPopVictory", True,
							  "Domination: Population",
							  "."))
		self.addOption(OptionList("Alert_DomPopThresh",
								  "CIV4LERTS", "PopThreshold", 1,
								  "Pop Threshold",
								  "Population threshold for Domination victory.",
								  [0.01,0.02,0.05,0.1,0.2,0.5,1.0,2.0,5.0,10.0,20.0,50.0],
								  "%.2f%%"))
		self.addOption(Option("Alert_DomLand",
							  "CIV4LERTS", "CheckForDomLandVictory", True,
							  "Domination: Land",
							  "."))
		self.addOption(OptionList("Alert_DomLandThresh",
								  "CIV4LERTS", "LandThreshold", 1,
								  "Land Threshold",
								  "Land threshold for Domination victory.",
								  [0.01,0.02,0.05,0.1,0.2,0.5,1.0,2.0,5.0,10.0,20.0,50.0],
								  "%.2f%%"))

	def isShowReminders(self):
		return self.getBoolean('Alert_Reminders')

	def getRemindersDisplayMethod(self):
		return self.getInt('Alert_RemindersMethod')

	def isShowRemindersPopup(self):
		return self.getRemindersDisplayMethod() != 0

	def isShowRemindersLog(self):
		return self.getRemindersDisplayMethod() != 1

	def isLogReminders(self):
		return self.getBoolean('Alert_LogReminders')


	def isShowAlerts(self):
		return self.getBoolean('Alert_Civ4lerts')
	

	def isShowCityPendingGrowthAlert(self):
		return self.isShowAlerts() and self.getBoolean('Alert_CityPendingGrowth')

	def isShowCityPendingHappinessAlert(self):
		return self.isShowAlerts() and self.getBoolean('Alert_CityPendingHappiness')

	def isShowCityPendingHealthinessAlert(self):
		return self.isShowAlerts() and self.getBoolean('Alert_CityPendingHealthiness')

	def isShowCityPendingExpandBorderAlert(self):
		return self.isShowAlerts() and self.getBoolean('Alert_CityPendingBorderExpansion')

	def isShowCityGrowthAlert(self):
		return self.isShowAlerts() and self.getBoolean('Alert_CityGrowth')

	def isShowCityHappinessAlert(self):
		return self.isShowAlerts() and self.getBoolean('Alert_CityHappiness')

	def isShowCityHealthinessAlert(self):
		return self.isShowAlerts() and self.getBoolean('Alert_CityHealthiness')

	def isShowCityCanHurryPopAlert(self):
		return self.isShowAlerts() and self.getBoolean('Alert_CityCanHurryPop')

	def isShowCityCanHurryGoldAlert(self):
		return self.isShowAlerts() and self.getBoolean('Alert_CityCanHurryGold')
	

	def isShowTechTradeAlert(self):
		return self.isShowAlerts() and self.getBoolean('Alert_TechTrade')

	def isShowGoldTradeAlert(self):
		return self.isShowAlerts() and self.getBoolean('Alert_GoldTrade')

	def getGoldTradeThreshold(self):
		return self.getInt('Alert_GoldTradeThresh')

	def isShowGoldPerTurnTradeAlert(self):
		return self.isShowAlerts() and self.getBoolean('Alert_GoldPerTurnTrade')

	def getGoldPerTurnTradeThreshold(self):
		return self.getInt('Alert_GoldPerTurnTradeThresh')
	
	def isShowOpenBordersTradeAlert(self):
		return self.isShowAlerts() and self.getBoolean('Alert_OpenBordersTrade')

	def isShowDefensivePactTradeAlert(self):
		return self.isShowAlerts() and self.getBoolean('Alert_DefensivePactTrade')

	def isShowPermanentAllianceTradeAlert(self):
		return self.isShowAlerts() and self.getBoolean('Alert_PermanentAllianceTrade')


	def isShowDomPopAlert(self):
		return self.isShowAlerts() and self.getBoolean('Alert_DomPop')

	def getDomPopThreshold(self):
		return self.getFloat('Alert_DomPopThresh')

	def isShowDomLandAlert(self):
		return self.isShowAlerts() and self.getBoolean('Alert_DomLand')

	def getDomLandThreshold(self):
		return self.getFloat('Alert_DomLandThresh')


# The singleton BugAlertsOptions object

__g_options = BugAlertsOptions()
def getOptions():
	return __g_options
