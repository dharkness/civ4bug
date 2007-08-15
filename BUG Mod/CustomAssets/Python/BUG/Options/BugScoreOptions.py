## BugScoreOptions
## Facade for accessing scoreboard options
## BUG Mod - Copyright 2007

from CvPythonExtensions import *
from BugOptions import OptionsFacade, Option, OptionList

class BugScoreOptions(OptionsFacade):

	def __init__(self):
		OptionsFacade.__init__(self)
		self.addOption(Option("Scores_HideDead",
							  "Scoreboard", "Hide Dead Civilizations", False,
							  "Hide",
							  "When checked, dead civilizations will be hidden.",
							  InterfaceDirtyBits.Score_DIRTY_BIT))
		self.addOption(Option("Scores_TagDead",
							  "Scoreboard", "Show Dead Tag", False,
							  "Tag as \"Dead\"",
							  "When checked, dead civilizations will be tagged as \"Dead\" when not hidden.",
							  InterfaceDirtyBits.Score_DIRTY_BIT))
		self.addOption(Option("Scores_GreyDead",
							  "Scoreboard", "Grey Out Dead Civilizations", False,
							  "Use Grey Color",
							  "When checked, dead civilizations will be greyed out when not hidden.",
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
							  "Scoreboard", "Power Rating", True,
							  "Power Rating",
							  "When checked, shows the power rating of civilizations against whom you have accumulated enough espionage points, including your own.",
							  InterfaceDirtyBits.Score_DIRTY_BIT))


	def isShowDeadCivs(self):
		return not self.getBoolean("Scores_HideDead")

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


# The singleton BugScoreOptions object

__g_options = BugScoreOptions()
def getOptions():
	return __g_options
