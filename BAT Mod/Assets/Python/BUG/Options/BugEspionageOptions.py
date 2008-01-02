## BugEspionageOptions
## Facade for accessing Better Espionage Screen options
## BUG Mod - Copyright 2007

from CvPythonExtensions import *
from BugOptions import OptionsFacade, Option, OptionList

class BugEspionageOptions(OptionsFacade):

	def __init__(self):
		OptionsFacade.__init__(self)
		self.addOption(Option("Espionage_Enabled",
							  "Better Espionage", "Enabled", True,
							  "Better Espionage Screen",
							  "When checked, uses Almightix's Better Espionage Screen.",
							  InterfaceDirtyBits.Espionage_Advisor_DIRTY_BIT))
		self.addOption(Option("Espionage_RatioColor",
							  "Better Espionage", "Default Ratio Color", "COLOR_CYAN",
							  "Ratio Color",
							  "Default color used for espionage ratios.",
							  InterfaceDirtyBits.Espionage_Advisor_DIRTY_BIT))
		self.addOption(OptionList("Espionage_GoodRatio",
								  "Better Espionage", "Good Ratio Cutoff", 95.0,
								  "Good Ratio Cutoff",
								  "Ratios less than or equal to this value are colored with the following color.",
								  [100.0, 97.5, 95.0, 92.5, 90.0, 87.5, 85.0, 82.5, 80.0, 77.5, 75.0], "%.1f%%",
								  InterfaceDirtyBits.Espionage_Advisor_DIRTY_BIT))
		self.addOption(Option("Espionage_GoodColor",
							  "Better Espionage", "Good Ratio Color", "COLOR_GREEN",
							  "Good Color",
							  "Color used for good espionage ratios.",
							  InterfaceDirtyBits.Espionage_Advisor_DIRTY_BIT))
		self.addOption(OptionList("Espionage_BadRatio",
								  "Better Espionage", "Bad Ratio Cutoff", 105.0,
								  "Bad Ratio Cutoff",
								  "Ratios greater than or equal to this value are colored with the following color.",
								  [100.0, 102.5, 105.0, 107.5, 110.0, 112.5, 115.0, 117.5, 120.0, 122.5, 125.0], "%.1f%%",
								  InterfaceDirtyBits.Espionage_Advisor_DIRTY_BIT))
		self.addOption(Option("Espionage_BadColor",
							  "Better Espionage", "Bad Ratio Color", "COLOR_YELLOW",
							  "Bad Color",
							  "Color used for bad espionage ratios.",
							  InterfaceDirtyBits.Espionage_Advisor_DIRTY_BIT))
		self.addOption(Option("Espionage_PossibleColor",
							  "Better Espionage", "Possible Mission Color", "COLOR_GREEN",
							  "Possible Mission Color",
							  "Color used for missions that you can perform now (you have enough EPs against the target).",
							  InterfaceDirtyBits.Espionage_Advisor_DIRTY_BIT))
		self.addOption(OptionList("Espionage_ClosePercent",
								  "Better Espionage", "Close Mission Percent", 5.0,
								  "Close Percent Cutoff",
								  "Determines how close your EPs have to be to the cost of a mission for it to be considered close to possible.",
								  [2.5, 5.0, 7.5, 10.0, 12.5, 15.0, 17.5, 20.0, 22.5, 25.0], "%.1f%%",
								  InterfaceDirtyBits.Espionage_Advisor_DIRTY_BIT))
		self.addOption(Option("Espionage_CloseColor",
							  "Better Espionage", "Close Mission Color", "COLOR_CYAN",
							  "Close Mission Color",
							  "Color used for missions that you can perform soon (you have close to enough EPs against the target).",
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
