## BugAlertsOptions								
## Facade for accessing Civ4lert and Reminder options								
## BUG Mod - Copyright 2007								
								
from BugOptions import OptionsFacade, Option, OptionList								
localText = CyTranslator()
								
class BugAlertsOptions(OptionsFacade):								
								
	def __init__(self):							
		OptionsFacade.__init__(self)						
								
		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_ALERT_REMINDERS_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_ALERT_REMINDERS_HOVER", ())						
		self.addOption(Option("Alert_Reminders",						
							  "CIV4LERTS", "Reminders", True, zs_Text, zsHover))	

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_ALERT_REMINDERSMETHOD_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_ALERT_REMINDERSMETHOD_HOVER", ())						
		self.addOption(OptionList("Alert_RemindersMethod",						
								  "CIV4LERTS", "Reminder Display Method", 2, zs_Text, zsHover,
								  ['Message', 'Popup', 'Both'], None))
								
		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_ALERT_LOGREMINDERS_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_ALERT_LOGREMINDERS_HOVER", ())						
		self.addOption(Option("Alert_LogReminders",						
							  "CIV4LERTS", "Log Reminders", True, zs_Text, zsHover))	

		# Civ4lerts						
		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_ALERT_CIV4LERTS_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_ALERT_CIV4LERTS_HOVER", ())						
		self.addOption(Option("Alert_Civ4lerts",						
							  "CIV4LERTS", "Enabled", True, zs_Text, zsHover))	

		# City						
		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_ALERT_CITYPENDINGGROWTH_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_ALERT_CITYPENDINGGROWTH_HOVER", ())						
		self.addOption(Option("Alert_CityPendingGrowth",						
							  "CIV4LERTS", "City Pending Growth", False, zs_Text, zsHover))	

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_ALERT_CITYPENDINGHAPPINESS_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_ALERT_CITYPENDINGHAPPINESS_HOVER", ())						
		self.addOption(Option("Alert_CityPendingHappiness",						
							  "CIV4LERTS", "City Pending Happiness", True, zs_Text, zsHover))	

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_ALERT_CITYPENDINGHEALTHINESS_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_ALERT_CITYPENDINGHEALTHINESS_HOVER", ())						
		self.addOption(Option("Alert_CityPendingHealthiness",						
							  "CIV4LERTS", "City Pending Healthiness", True, zs_Text, zsHover))	

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_ALERT_CITYPENDINGBORDEREXPANSION_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_ALERT_CITYPENDINGBORDEREXPANSION_HOVER", ())						
		self.addOption(Option("Alert_CityPendingBorderExpansion",						
							  "CIV4LERTS", "City Pending Border Expansion", True, zs_Text, zsHover))	

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_ALERT_CITYGROWTH_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_ALERT_CITYGROWTH_HOVER", ())						
		self.addOption(Option("Alert_CityGrowth",						
							  "CIV4LERTS", "City Growth", False, zs_Text, zsHover))	

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_ALERT_CITYHAPPINESS_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_ALERT_CITYHAPPINESS_HOVER", ())						
		self.addOption(Option("Alert_CityHappiness",						
							  "CIV4LERTS", "City Happiness", True, zs_Text, zsHover))	

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_ALERT_CITYHEALTHINESS_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_ALERT_CITYHEALTHINESS_HOVER", ())						
		self.addOption(Option("Alert_CityHealthiness",						
							  "CIV4LERTS", "City Healthiness", True, zs_Text, zsHover))	

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_ALERT_CITYCANHURRYPOP_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_ALERT_CITYCANHURRYPOP_HOVER", ())						
		self.addOption(Option("Alert_CityCanHurryPop",						
							  "CIV4LERTS", "City Can Hurry Pop", True, zs_Text, zsHover))	

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_ALERT_CITYCANHURRYGOLD_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_ALERT_CITYCANHURRYGOLD_HOVER", ())						
		self.addOption(Option("Alert_CityCanHurryGold",						
							  "CIV4LERTS", "City Can Hurry Gold", True, zs_Text, zsHover))	

		# Trade						
		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_ALERT_TECHTRADE_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_ALERT_TECHTRADE_HOVER", ())						
		self.addOption(Option("Alert_TechTrade",						
							  "CIV4LERTS", "CheckForNewTrades", True, zs_Text, zsHover))	

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_ALERT_GOLDTRADE_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_ALERT_GOLDTRADE_HOVER", ())						
		self.addOption(Option("Alert_GoldTrade",						
							  "CIV4LERTS", "Gold Trade", True, zs_Text, zsHover))	

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_ALERT_GOLDTRADETHRESH_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_ALERT_GOLDTRADETHRESH_HOVER", ())						
		self.addOption(OptionList("Alert_GoldTradeThresh",						
								  "CIV4LERTS", "Gold Trade Threshold", 50, zs_Text, zsHover,
								  [1,2,3,5,10,20,30,50,100,200,300,500,1000]))
								
		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_ALERT_GOLDPERTURNTRADE_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_ALERT_GOLDPERTURNTRADE_HOVER", ())						
		self.addOption(Option("Alert_GoldPerTurnTrade",						
							  "CIV4LERTS", "Gold Per Turn Trade", True, zs_Text, zsHover))	

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_ALERT_GOLDPERTURNTRADETHRESH_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_ALERT_GOLDPERTURNTRADETHRESH_HOVER", ())						
		self.addOption(OptionList("Alert_GoldPerTurnTradeThresh",						
								  "CIV4LERTS", "Gold Per Turn Threshold", 5, zs_Text, zsHover,
								  [1,2,3,5,10,15,20,25,30,50,100]))
								
		# Diplomacy						
		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_ALERT_OPENBORDERSTRADE_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_ALERT_OPENBORDERSTRADE_HOVER", ())						
		self.addOption(Option("Alert_OpenBordersTrade",						
							  "CIV4LERTS", "Open Borders Trades", True, zs_Text, zsHover))	

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_ALERT_DEFENSIVEPACTTRADE_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_ALERT_DEFENSIVEPACTTRADE_HOVER", ())						
		self.addOption(Option("Alert_DefensivePactTrade",						
							  "CIV4LERTS", "Defensive Pact Trades", True, zs_Text, zsHover))	

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_ALERT_PERMANENTALLIANCETRADE_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_ALERT_PERMANENTALLIANCETRADE_HOVER", ())						
		self.addOption(Option("Alert_PermanentAllianceTrade",						
							  "CIV4LERTS", "Permanent Alliance Trades", True, zs_Text, zsHover))	

		# Victory						
		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_ALERT_DOMPOP_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_ALERT_DOMPOP_HOVER", ())						
		self.addOption(Option("Alert_DomPop",						
							  "CIV4LERTS", "CheckForDomPopVictory", True, zs_Text, zsHover))	

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_ALERT_DOMPOPTHRESH_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_ALERT_DOMPOPTHRESH_HOVER", ())						
		self.addOption(OptionList("Alert_DomPopThresh",						
								  "CIV4LERTS", "PopThreshold", 1, zs_Text, zsHover,
								  [0.01,0.02,0.05,0.1,0.2,0.5,1.0,2.0,5.0,10.0,20.0,50.0],
								  "%.2f%%"))
								
		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_ALERT_DOMLAND_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_ALERT_DOMLAND_HOVER", ())						
		self.addOption(Option("Alert_DomLand",						
							  "CIV4LERTS", "CheckForDomLandVictory", True, zs_Text, zsHover))	

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_ALERT_DOMLANDTHRESH_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_ALERT_DOMLANDTHRESH_HOVER", ())						
		self.addOption(OptionList("Alert_DomLandThresh",						
								  "CIV4LERTS", "LandThreshold", 1, zs_Text, zsHover,
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
