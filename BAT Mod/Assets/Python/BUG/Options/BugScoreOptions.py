## BugScoreOptions
## Facade for accessing scoreboard options
## BUG Mod - Copyright 2007

from CvPythonExtensions import *
from BugOptions import OptionsFacade, Option, OptionList

class BugScoreOptions(OptionsFacade):

	def __init__(self):
		OptionsFacade.__init__(self)
		self.addOption(Option("Scores_ShowDead",
							  "Scoreboard", "Show Dead Civilizations", True,
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
		
		self.addOption(Option("Scores_AlignIcons",
							  "Scoreboard", "Align Icons", True,
							  "Enabled",
							  "When checked, the scoreboard is drawn as a grid, and the other options in this column affect it.",
							  InterfaceDirtyBits.Score_DIRTY_BIT))
		self.addOption(Option("Scores_DisplayOrder",
							  "Scoreboard", "Display Order", "SC?WEPTUNBDRA*LO",
							  "Display Order",
							  "This determines the order in which the score columns appear.\n\
S - The civ's score.\n\
C - The civ's/leader's name.\n\
? - You have not yet met the civ.\n\
W - You are at war with the civ.\n\
E - You have a positive espionage point ratio against the civ.\n\
P - The civ's power ratio compared to you.\n\
T - The tech the civ is researching (vassals, teammates and espionage).\n\
U - The number of research turns left.\n\
N - The civ is connected to your trade network.\n\
B - You have an open borders agreement with the civ.\n\
D - You have a defensive pact with the civ.\n\
R - The civ's state religion.\n\
A - The civ's attitude toward you.\n\
* - You are waiting for this civ to finish its turn.\n\
L - Civ's network stats (ping).\n\
O - The network player is out-of-sync.",
							  InterfaceDirtyBits.Score_DIRTY_BIT))
		self.addOption(Option("Scores_LeftAlignName",
							  "Scoreboard", "Left-Align Name", True,
							  "Left-Align Name",
							  "When checked, the civ/leader name is left-aligned instead of right-aligned.",
							  InterfaceDirtyBits.Score_DIRTY_BIT))
		self.addOption(Option("Scores_ResearchIcons",
							  "Scoreboard", "Research Icons", True,
							  "Research Icons",
							  "When checked, shows icons instead of names for civs whose research you can see.",
							  InterfaceDirtyBits.Score_DIRTY_BIT))
		
		self.addOption(Option("Scores_Power",
							  "Scoreboard", "Power", True,
							  "Power Ratio",
							  "When checked, shows the ratio of your power rating to those of civilizations against whom you have accumulated enough espionage points.",
							  InterfaceDirtyBits.Score_DIRTY_BIT))
		self.addOption(Option("Scores_PowerColor",
							  "Scoreboard", "Power Color", "COLOR_WHITE",
							  "Default Color",
							  "Color used by default for power ratios.",
							  InterfaceDirtyBits.Score_DIRTY_BIT))
		self.addOption(OptionList("Scores_PowerGoodRatio",
								  "Scoreboard", "Power Good", 1.2,
								  "Good Ratio Cutoff",
								  "Power ratings greater than or equal to this value are shown in the Good Color.",
								  [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0], "%.1f",
								  InterfaceDirtyBits.Score_DIRTY_BIT))
		self.addOption(Option("Scores_PowerGoodColor",
							  "Scoreboard", "Power Good Color", "COLOR_GREEN",
							  "Good Color",
							  "Color used for good power ratios.",
							  InterfaceDirtyBits.Score_DIRTY_BIT))
		self.addOption(OptionList("Scores_PowerBadRatio",
								  "Scoreboard", "Power Bad", 0.8,
								  "Bad Ratio Cutoff",
								  "Power ratings less than or equal to this value are shown in in the Bad Color.",
								  [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0], "%.1f",
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


	def isAlignIcons(self):
		return self.getBoolean("Scores_AlignIcons")

	def isLeftAlignName(self):
		return self.getBoolean("Scores_LeftAlignName")

	def getDisplayOrder(self):
		return self.getString("Scores_DisplayOrder")

	def isShowResearchIcons(self):
		return self.getBoolean("Scores_ResearchIcons")


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
