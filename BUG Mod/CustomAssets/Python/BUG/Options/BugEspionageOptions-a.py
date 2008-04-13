## BugEspionageOptions								
## Facade for accessing Better Espionage Screen options								
## BUG Mod - Copyright 2007								
								
from CvPythonExtensions import *								
from BugOptions import OptionsFacade, Option, OptionList								
								
class BugEspionageOptions(OptionsFacade):								
								
	def __init__(self):							
		OptionsFacade.__init__(self)						
								
		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_ESPIONAGE_ENABLED_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_ESPIONAGE_ENABLED_HOVER", ())						
		self.addOption(Option("Espionage_Enabled",						
							  "Better Espionage", "Enabled", True, zs_Text, zsHover, 
							  InterfaceDirtyBits.Espionage_Advisor_DIRTY_BIT))	

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_ESPIONAGE_RATIOCOLOR_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_ESPIONAGE_RATIOCOLOR_HOVER", ())						
		self.addOption(Option("Espionage_RatioColor",						
							  "Better Espionage", "Default Ratio Color", "COLOR_CYAN", zs_Text, zsHover, 
							  InterfaceDirtyBits.Espionage_Advisor_DIRTY_BIT))	

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_ESPIONAGE_GOODRATIO_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_ESPIONAGE_GOODRATIO_HOVER", ())						
		self.addOption(OptionList("Espionage_GoodRatio",						
								  "Better Espionage", "Good Ratio Cutoff", 95.0, zs_Text, zsHover,
								  [100.0, 97.5, 95.0, 92.5, 90.0, 87.5, 85.0, 82.5, 80.0, 77.5, 75.0], "%.1f%%",
								  InterfaceDirtyBits.Espionage_Advisor_DIRTY_BIT))
								
		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_ESPIONAGE_GOODCOLOR_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_ESPIONAGE_GOODCOLOR_HOVER", ())						
		self.addOption(Option("Espionage_GoodColor",						
							  "Better Espionage", "Good Ratio Color", "COLOR_GREEN", zs_Text, zsHover, 
							  InterfaceDirtyBits.Espionage_Advisor_DIRTY_BIT))	

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_ESPIONAGE_BADRATIO_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_ESPIONAGE_BADRATIO_HOVER", ())						
		self.addOption(OptionList("Espionage_BadRatio",						
								  "Better Espionage", "Bad Ratio Cutoff", 105.0, zs_Text, zsHover,
								  [100.0, 102.5, 105.0, 107.5, 110.0, 112.5, 115.0, 117.5, 120.0, 122.5, 125.0], "%.1f%%",
								  InterfaceDirtyBits.Espionage_Advisor_DIRTY_BIT))

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_ESPIONAGE_BADCOLOR_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_ESPIONAGE_BADCOLOR_HOVER", ())						
		self.addOption(Option("Espionage_BadColor",						
							  "Better Espionage", "Bad Ratio Color", "COLOR_YELLOW", zs_Text, zsHover, 
							  InterfaceDirtyBits.Espionage_Advisor_DIRTY_BIT))	

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_ESPIONAGE_POSSIBLECOLOR_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_ESPIONAGE_POSSIBLECOLOR_HOVER", ())						
		self.addOption(Option("Espionage_PossibleColor",						
							  "Better Espionage", "Possible Mission Color", "COLOR_GREEN", zs_Text, zsHover, 
							  InterfaceDirtyBits.Espionage_Advisor_DIRTY_BIT))	

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_ESPIONAGE_CLOSEPERCENT_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_ESPIONAGE_CLOSEPERCENT_HOVER", ())						
		self.addOption(OptionList("Espionage_ClosePercent",						
								  "Better Espionage", "Close Mission Percent", 5.0, zs_Text, zsHover,
								  [2.5, 5.0, 7.5, 10.0, 12.5, 15.0, 17.5, 20.0, 22.5, 25.0], "%.1f%%",
								  InterfaceDirtyBits.Espionage_Advisor_DIRTY_BIT))

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_ESPIONAGE_CLOSECOLOR_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_ESPIONAGE_CLOSECOLOR_HOVER", ())						
		self.addOption(Option("Espionage_CloseColor",						
							  "Better Espionage", "Close Mission Color", "COLOR_CYAN", zs_Text, zsHover, 
							  InterfaceDirtyBits.Espionage_Advisor_DIRTY_BIT))	


	def isEnabled(self):							
		return self.getBoolean('Espionage_Enabled')						
								
								
	def getDefaultRatioColor(self):							
		return self.getString('Espionage_RatioColor')						
								
	def getGoodRatioCutoff(self):							
		return self.getFloat('Espionage_GoodRatio')						
								
	def getGoodRatioColor(self):							
		return self.getString('Espionage_GoodColor')						
								
	def getBadRatioCutoff(self):							
		return self.getFloat('Espionage_BadRatio')						
								
	def getBadRatioColor(self):							
		return self.getString('Espionage_BadColor')						
								
								
	def getPossibleMissionColor(self):							
		return self.getString('Espionage_PossibleColor')						
								
	def getCloseMissionPercent(self):							
		return self.getFloat('Espionage_ClosePercent')						
								
	def getCloseMissionColor(self):							
		return self.getString('Espionage_CloseColor')						
								
								
# The singleton BugEspionageOptions object								
								
__g_options = BugEspionageOptions()								
def getOptions():								
	return __g_options							
								
