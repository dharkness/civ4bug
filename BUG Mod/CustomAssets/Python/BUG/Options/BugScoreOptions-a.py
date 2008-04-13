## BugScoreOptions								
## Facade for accessing scoreboard options								
## BUG Mod - Copyright 2007								
								
from CvPythonExtensions import *								
from BugOptions import OptionsFacade, Option, OptionList								
localText = CyTranslator()
								
class BugScoreOptions(OptionsFacade):								
								
	def __init__(self):							
		OptionsFacade.__init__(self)						
								
		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_SCORES_SHOWDEAD_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_SCORES_SHOWDEAD_HOVER", ())						
		self.addOption(Option("Scores_ShowDead",						
							  "Scoreboard", "Show Dead Civilizations", True, zs_Text, zsHover,	
							  InterfaceDirtyBits.Score_DIRTY_BIT))	

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_SCORES_TAGDEAD_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_SCORES_TAGDEAD_HOVER", ())						
		self.addOption(Option("Scores_TagDead",						
							  "Scoreboard", "Show Dead Tag", False, zs_Text, zsHover,	
							  InterfaceDirtyBits.Score_DIRTY_BIT))	

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_SCORES_GREYDEAD_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_SCORES_GREYDEAD_HOVER", ())						
		self.addOption(Option("Scores_GreyDead",						
							  "Scoreboard", "Grey Out Dead Civilizations", False, zs_Text, zsHover,	
							  InterfaceDirtyBits.Score_DIRTY_BIT))	

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_SCORES_DISPLAYNAME_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_SCORES_DISPLAYNAME_HOVER", ())						
		self.addOption(OptionList("Scores_DisplayName",						
								  "Scoreboard", "Display Name", False, zs_Text, zsHover,
								  ['Leader', 'Civilization', 'Both'], None,
								  InterfaceDirtyBits.Score_DIRTY_BIT))
								
		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_SCORES_ATTITUDE_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_SCORES_ATTITUDE_HOVER", ())						
		self.addOption(Option("Scores_Attitude",						
							  "Scoreboard", "Attitude Icons", True, zs_Text, zsHover,	
							  InterfaceDirtyBits.Score_DIRTY_BIT))	

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_SCORES_ALIGNICONS_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_SCORES_ALIGNICONS_HOVER", ())						
		self.addOption(Option("Scores_AlignIcons",						
							  "Scoreboard", "Align Icons", True, zs_Text, zsHover,	
							  InterfaceDirtyBits.Score_DIRTY_BIT))	

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_SCORES_DISPLAYORDER_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_SCORES_DISPLAYORDER_HOVER", ())						
		self.addOption(Option("Scores_DisplayOrder",						
							  "Scoreboard", "Display Order", "SC?WEPTUNBDRA*LO", zs_Text, zsHover,	
							  InterfaceDirtyBits.Score_DIRTY_BIT))	

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_SCORES_LEFTALIGNNAME_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_SCORES_LEFTALIGNNAME_HOVER", ())						
		self.addOption(Option("Scores_LeftAlignName",						
							  "Scoreboard", "Left-Align Name", True, zs_Text, zsHover,	
							  InterfaceDirtyBits.Score_DIRTY_BIT))	

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_SCORES_RESEARCHICONS_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_SCORES_RESEARCHICONS_HOVER", ())						
		self.addOption(Option("Scores_ResearchIcons",						
							  "Scoreboard", "Research Icons", True, zs_Text, zsHover,	
							  InterfaceDirtyBits.Score_DIRTY_BIT))	

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_SCORES_POWER_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_SCORES_POWER_HOVER", ())						
		self.addOption(Option("Scores_Power",						
							  "Scoreboard", "Power", True, zs_Text, zsHover,	
							  InterfaceDirtyBits.Score_DIRTY_BIT))	

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_SCORES_POWERCOLOR_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_SCORES_POWERCOLOR_HOVER", ())						
		self.addOption(Option("Scores_PowerColor",						
							  "Scoreboard", "Power Color", "COLOR_WHITE", zs_Text, zsHover,	
							  InterfaceDirtyBits.Score_DIRTY_BIT))	

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_SCORES_POWERGOODRATIO_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_SCORES_POWERGOODRATIO_HOVER", ())						
		self.addOption(OptionList("Scores_PowerGoodRatio",						
								  "Scoreboard", "Power Good", 1.2, zs_Text, zsHover,
								  [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0], "%.1f",
								  InterfaceDirtyBits.Score_DIRTY_BIT))
								
		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_SCORES_POWERGOODCOLOR_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_SCORES_POWERGOODCOLOR_HOVER", ())						
		self.addOption(Option("Scores_PowerGoodColor",						
							  "Scoreboard", "Power Good Color", "COLOR_GREEN", zs_Text, zsHover,	
							  InterfaceDirtyBits.Score_DIRTY_BIT))	

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_SCORES_POWERBADRATIO_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_SCORES_POWERBADRATIO_HOVER", ())						
		self.addOption(OptionList("Scores_PowerBadRatio",						
								  "Scoreboard", "Power Bad", 0.8, zs_Text, zsHover,
								  [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0], "%.1f",
								  InterfaceDirtyBits.Score_DIRTY_BIT))
								
		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_SCORES_POWERBADCOLOR_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_SCORES_POWERBADCOLOR_HOVER", ())						
		self.addOption(Option("Scores_PowerBadColor",						
							  "Scoreboard", "Power Bad Color", "COLOR_YELLOW", zs_Text, zsHover,	
							  InterfaceDirtyBits.Score_DIRTY_BIT))	


	def isShowDeadCivs(self):							
		return self.getBoolean("Scores_ShowDead")						
								
	def isShowDeadTag(self):							
		return self.getBoolean("Scores_TagDead")						
								
	def isGreyOutDeadCivs(self):							
		return self.getBoolean("Scores_GreyDead")						
								
								
	def getShowNameEnum(self):							
		"0 = Leader, 1 = Civ, 2 = Both"						
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
								
