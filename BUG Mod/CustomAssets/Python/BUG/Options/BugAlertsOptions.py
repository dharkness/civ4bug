## BugAlertsOptions
## Facade for accessing Civ4lert and Reminder options
## BUG Mod - Copyright 2007

from BugOptions import OptionsFacade, Option, OptionList

class BugAlertsOptions(OptionsFacade):

	def __init__(self):
		OptionsFacade.__init__(self)
		self.addOption(Option("Alert_Reminders",
							  "CIV4LERTS", "Reminders", True,
							  "Enable Reminders (Alt-M)",
							  "When checked, you can create messages using Alt-M that pop up in a specified number of turns using eotinb's Reminders mod."))
		
		# Civ4lerts
		self.addOption(Option("Alert_Civ4lerts",
							  "CIV4LERTS", "Enabled", True,
							  "Enable Civ4lerts",
							  "When checked, messages are displayed to alert you to various pending and existing conditions using Dr. Elmer Jiggle's Civ4lerts mod."))
		
		# City
		self.addOption(Option("Alert_CityPendingGrowth",
							  "CIV4LERTS", "City Pending Growth", False,
							  "Pending Growth",
							  "."))
		self.addOption(Option("Alert_CityPendingUnhealthy",
							  "CIV4LERTS", "City Pending Unhealthy", True,
							  "Pending Unhealthy",
							  "."))
		self.addOption(Option("Alert_CityPendingAngry",
							  "CIV4LERTS", "City Pending Angry", True,
							  "Pending Angry",
							  "."))
		self.addOption(Option("Alert_CityGrowth",
							  "CIV4LERTS", "City Growth", False,
							  "Growth",
							  "."))
		self.addOption(Option("Alert_CityUnhealthy",
							  "CIV4LERTS", "City Growth Unhealthy", True,
							  "Growth Unhealthy",
							  "."))
		self.addOption(Option("Alert_CityAngry",
							  "CIV4LERTS", "City Growth Angry", True,
							  "Growth Angry",
							  "."))
		self.addOption(Option("Alert_CityExpandBorder",
							  "CIV4LERTS", "CheckForCityBorderExpansion", True,
							  "Border Expansion",
							  "."))
		
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
							  "Gold Per Turn Trade",
							  "."))
		self.addOption(OptionList("Alert_GoldPerTurnTradeThresh",
								  "CIV4LERTS", "Gold Per Turn Threshold", 5,
								  "Threshold",
								  ".",
								  [1,2,3,5,10,15,20,25,30,50,100]))
		
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


	def isShowAlerts(self):
		return self.getBoolean('Alert_Civ4lerts')
	

	def isShowCityPendingGrowthAlert(self):
		return self.isShowAlerts() and self.getBoolean('Alert_CityPendingGrowth')

	def isShowCityPendingUnhealthyAlert(self):
		return self.isShowAlerts() and self.getBoolean('Alert_CityPendingUnhealthy')

	def isShowCityPendingAngryAlert(self):
		return self.isShowAlerts() and self.getBoolean('Alert_CityPendingAngry')

	def isShowCityGrowthAlert(self):
		return self.isShowAlerts() and self.getBoolean('Alert_CityGrowth')

	def isShowCityGrowthUnhealthyAlert(self):
		return self.isShowAlerts() and self.getBoolean('Alert_CityUnhealthy')

	def isShowCityGrowthAngryAlert(self):
		return self.isShowAlerts() and self.getBoolean('Alert_CityAngry')

	def isShowCityExpandBorderAlert(self):
		return self.isShowAlerts() and self.getBoolean('Alert_CityExpandBorder')
	

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
