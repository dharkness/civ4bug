## BugScoreOptions
## Facade for accessing scoreboard options
## BUG Mod - Copyright 2007

from CvPythonExtensions import *
from BugOptions import OptionsFacade, Option, OptionList

class BugScoreOptions(OptionsFacade):

	def __init__(self):
		OptionsFacade.__init__(self)
		self.addOption(Option("Scores_ShowDead",
							  "Scoreboard", "Hide Dead Civilizations", False,
							  "Show",
							  "When checked, dead civilizations will remain on the scoreboard.",
							  InterfaceDirtyBits.Score_DIRTY_BIT))
		self.addOption(Option("Scores_TagDead",
							  "Scoreboard", "Show Dead Tag", False,
							  "Tag as \"Dead\"",
							  "When checked, dead civilizations will be tagged as \"Dead\" when shown.",
							  InterfaceDirtyBits.Score_DIRTY_BIT))
		self.addOption(Option("Scores_GreyDead",
							  "Scoreboard", "Grey Out Dead Civilizations", False,
							  "Use Grey Color",
							  "When checked, dead civilizations will be greyed out when not shown.",
							  InterfaceDirtyBits.Score_DIRTY_BIT))
		
		self.addOption(OptionList("Scores_DisplayName",
								  "Scoreboard", "Display Name", False,
								  "Display Name",
								  "Determines how civilizations are labeled on the scoreboard.",
								  ['Leader', 'Civilization', 'Both'], None,
								  InterfaceDirtyBits.Score_DIRTY_BIT))
		
		self.addOption(Option("Scores_Attitude",
							  "Scoreboard", "Attitude Icons", True,
							  "Attitude Icons",
							  "When checked, shows faces depicting each AI's attitude toward you.",
							  InterfaceDirtyBits.Score_DIRTY_BIT))
		
		self.addOption(Option("Scores_Power",
							  "Scoreboard", "Power", True,
							  "Power Ratio",
							  "When checked, shows the power of civilizations against whom you have accumulated enough espionage points as a ratio of theirs to yours.",
							  InterfaceDirtyBits.Score_DIRTY_BIT))
		self.addOption(Option("Scores_PowerColor",
							  "Scoreboard", "Power Color", "COLOR_WHITE",
							  "Default Color",
							  "Color used by default for power ratios.",
							  InterfaceDirtyBits.Score_DIRTY_BIT))
		self.addOption(OptionList("Scores_PowerGoodRatio",
								  "Scoreboard", "Power Good", 1.0,
								  "Good Ratio Cutoff",
								  "Power ratings less than or equal to this value are shown in green.",
								  [0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5], "%.1f",
								  InterfaceDirtyBits.Score_DIRTY_BIT))
		self.addOption(Option("Scores_PowerGoodColor",
							  "Scoreboard", "Power Good Color", "COLOR_GREEN",
							  "Good Color",
							  "Color used for good power ratios.",
							  InterfaceDirtyBits.Score_DIRTY_BIT))
		self.addOption(OptionList("Scores_PowerBadRatio",
								  "Scoreboard", "Power Bad", 1.0,
								  "Bad Ratio Cutoff",
								  "Power ratings greater than or equal to this value are shown in yellow.",
								  [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.5, 3.0, 3.5, 4.0], "%.1f",
								  InterfaceDirtyBits.Score_DIRTY_BIT))
		self.addOption(Option("Scores_PowerBadColor",
							  "Scoreboard", "Power Bad Color", "COLOR_YELLOW",
							  "Bad Color",
							  "Color used for bad power ratios.",
							  InterfaceDirtyBits.Score_DIRTY_BIT))


	def isShowDeadCivs(self):
		return self.getBoolean("Scores_ShowDead")

	def isShowDeadTag(self):
		return self.getBoolean("Scores_TagDead")

	def isGreyOutDeadCivs(self):
		return self.getBoolean("Scores_GreyDead")


	def getShowNameEnum(self):
		"""0 = Leader, 1 = Civ, 2 = Both"""
		return self.getInt("Scores_DisplayName")

	def isShowLeaderName(self):
		return self.getShowNameEnum() != 1

	def isShowCivName(self):
		return self.getShowNameEnum() != 0

	def isShowBothNames(self):
		return self.getShowNameEnum() == 2


	def isShowAttitude(self):
		return self.getBoolean("Scores_Attitude")


	def isShowPower(self):
		return self.getBoolean("Scores_Power")
	
	def getPowerColor(self):
		return self.getString("Scores_PowerColor")
	
	def getGoodPowerRatio(self):
		return self.getFloat("Scores_PowerGoodRatio")
	
	def getGoodPowerColor(self):
		return self.getString("Scores_PowerGoodColor")
	
	def getBadPowerRatio(self):
		return self.getFloat("Scores_PowerBadRatio")

	def getBadPowerColor(self):
		return self.getString("Scores_PowerBadColor")
	

# The singleton BugScoreOptions object

__g_options = BugScoreOptions()
def getOptions():
	return __g_options
