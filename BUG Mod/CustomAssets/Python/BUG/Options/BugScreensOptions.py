## BugScreensOptions
## Facade for accessing Customizable Domestic Advisor options
## BUG Mod - Copyright 2007

from CvPythonExtensions import *
from BugOptions import OptionsFacade, Option, OptionList

class BugScreensOptions(OptionsFacade):

	def __init__(self):
		OptionsFacade.__init__(self)
		self.addOption(Option("Screens_CDA",
							  "Screens", "CustDomAdv", False,
							  "Customizable Domestic Advisor",
							  "When checked, uses the Customizable Domestic Advisor (requires restart)."))

		self.addOption(Option("Screens_Espionage_Compact",
							  "Screens", "Compact Espionage List", False,
							  "Compact Espionage List",
							  "When checked, uses the Better Espionage Advisor.",
							  InterfaceDirtyBits.Espionage_Advisor_DIRTY_BIT))
		self.addOption(OptionList("Screens_Espionage_BadRatio",
								  "Screens", "Bad Espionage Ratio Cutoff", 105.0,
								  "Bad Ratio Cutoff",
								  "Ratios greater than or equal to this value are colored red.",
								  [100.0, 102.5, 105.0, 107.5, 110.0, 112.5, 115.0, 117.5, 120.0, 122.5, 125.0], "%.2f%%",
								  InterfaceDirtyBits.Espionage_Advisor_DIRTY_BIT))
		self.addOption(OptionList("Screens_Espionage_GoodRatio",
								  "Screens", "Good Espionage Ratio Cutoff", 95.0,
								  "Good Ratio Cutoff",
								  "Ratios less than or equal to this value are colored green.",
								  [100.0, 97.5, 95.0, 92.5, 90.0, 87.5, 85.0, 82.5, 80.0, 77.5, 75.0], "%.2f%%",
								  InterfaceDirtyBits.Espionage_Advisor_DIRTY_BIT))

		self.addOption(Option("Screens_Tech_GPPrefs",
							  "Tech", "GP Tech Prefs", False,
							  "Great Person Research",
							  "When checked, displays the technology each type of great person will research."))


	def isCustDomAdv(self):
		return self.getBoolean('Screens_CDA')


	def isCompactEspionageList(self):
		return self.getBoolean('Screens_Espionage_Compact')

	def getBadEspionageRatioCutoff(self):
		return self.getFloat('Screens_Espionage_BadRatio')

	def getGoodEspionageRatioCutoff(self):
		return self.getFloat('Screens_Espionage_GoodRatio')


	def isShowGPTechPrefs(self):
		return self.getBoolean("Screens_Tech_GPPrefs")


# The singleton BugScreensOptions object

__g_options = BugScreensOptions()
def getOptions():
	return __g_options
