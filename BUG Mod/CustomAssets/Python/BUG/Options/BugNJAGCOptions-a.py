## BugNJAGCOptions								
## Facade for accessing NJAGC options								
## BUG Mod - Copyright 2007								
								
from CvPythonExtensions import *								
from BugOptions import OptionsFacade, Option, OptionList								
localText = CyTranslator()
								
class BugNJAGCOptions(OptionsFacade):								
								
	def __init__(self):							
		OptionsFacade.__init__(self)						
								
		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_NJAGCM_ENABLED_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_NJAGCM_ENABLED_HOVER", ())						
		self.addOption(Option("NJAGCM_Enabled",						
						 "NJAGCM", "Enabled", True, zs_Text, zsHover,		
						 InterfaceDirtyBits.GameData_DIRTY_BIT))		

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_NJAGCM_SHOWERA_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_NJAGCM_SHOWERA_HOVER", ())						
		self.addOption(Option("NJAGCM_ShowEra",						
						 "NJAGCM", "Show Era", True, zs_Text, zsHover,		
						 InterfaceDirtyBits.GameData_DIRTY_BIT))		

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_NJAGCM_SHOWERACOLOR_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_NJAGCM_SHOWERACOLOR_HOVER", ())						
		self.addOption(Option("NJAGCM_ShowEraColor",						
						 "NJAGCM", "Show Reflect Era In Turn Color", True, zs_Text, zsHover,		
						 InterfaceDirtyBits.GameData_DIRTY_BIT))		

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_NJAGCM_COLOR_ERA_ANCIENT_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_NJAGCM_COLOR_ERA_ANCIENT_HOVER", ())						
		self.addOption(Option("NJAGCM_Color_ERA_ANCIENT",						
						 "NJAGCM", "ERA_ANCIENT", "COLOR_RED", zs_Text, zsHover,		
						 InterfaceDirtyBits.GameData_DIRTY_BIT))		

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_NJAGCM_COLOR_ERA_CLASSICAL_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_NJAGCM_COLOR_ERA_CLASSICAL_HOVER", ())						
		self.addOption(Option("NJAGCM_Color_ERA_CLASSICAL",						
						 "NJAGCM", "ERA_CLASSICAL", "COLOR_YELLOW", zs_Text, zsHover,		
						 InterfaceDirtyBits.GameData_DIRTY_BIT))		

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_NJAGCM_COLOR_ERA_MEDIEVAL_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_NJAGCM_COLOR_ERA_MEDIEVAL_HOVER", ())						
		self.addOption(Option("NJAGCM_Color_ERA_MEDIEVAL",						
						 "NJAGCM", "ERA_MEDIEVAL", "COLOR_GREEN", zs_Text, zsHover,		
						 InterfaceDirtyBits.GameData_DIRTY_BIT))		

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_NJAGCM_COLOR_ERA_RENAISSANCE_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_NJAGCM_COLOR_ERA_RENAISSANCE_HOVER", ())						
		self.addOption(Option("NJAGCM_Color_ERA_RENAISSANCE",						
						 "NJAGCM", "ERA_RENAISSANCE", "COLOR_CYAN", zs_Text, zsHover,		
						 InterfaceDirtyBits.GameData_DIRTY_BIT))		

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_NJAGCM_COLOR_ERA_INDUSTRIAL_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_NJAGCM_COLOR_ERA_INDUSTRIAL_HOVER", ())						
		self.addOption(Option("NJAGCM_Color_ERA_INDUSTRIAL",						
						 "NJAGCM", "ERA_INDUSTRIAL", "COLOR_BLUE", zs_Text, zsHover,		
						 InterfaceDirtyBits.GameData_DIRTY_BIT))		

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_NJAGCM_COLOR_ERA_MODERN_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_NJAGCM_COLOR_ERA_MODERN_HOVER", ())						
		self.addOption(Option("NJAGCM_Color_ERA_MODERN",						
						 "NJAGCM", "ERA_MODERN", "COLOR_MAGENTA", zs_Text, zsHover,		
						 InterfaceDirtyBits.GameData_DIRTY_BIT))		

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_NJAGCM_COLOR_ERA_FUTURE_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_NJAGCM_COLOR_ERA_FUTURE_HOVER", ())						
		self.addOption(Option("NJAGCM_Color_ERA_FUTURE",						
						 "NJAGCM", "ERA_FUTURE", "COLOR_WHITE", zs_Text, zsHover,		
						 InterfaceDirtyBits.GameData_DIRTY_BIT))		

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_NJAGCM_SHOWTIME_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_NJAGCM_SHOWTIME_HOVER", ())						
		self.addOption(Option("NJAGCM_ShowTime",						
						 "NJAGCM", "Show Game Clock", False, zs_Text, zsHover,		
						 InterfaceDirtyBits.GameData_DIRTY_BIT))		

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_NJAGCM_SHOWCOMPLETEDTURNS_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_NJAGCM_SHOWCOMPLETEDTURNS_HOVER", ())						
		self.addOption(Option("NJAGCM_ShowCompletedTurns",						
						 "NJAGCM", "Show Game Completed Turns", True, zs_Text, zsHover,		
						 InterfaceDirtyBits.GameData_DIRTY_BIT))		

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_NJAGCM_SHOWTOTALTURNS_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_NJAGCM_SHOWTOTALTURNS_HOVER", ())						
		self.addOption(Option("NJAGCM_ShowTotalTurns",						
						 "NJAGCM", "Show Game Total Turns", True, zs_Text, zsHover,		
						 InterfaceDirtyBits.GameData_DIRTY_BIT))		

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_NJAGCM_SHOWCOMPLETEDPERCENT_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_NJAGCM_SHOWCOMPLETEDPERCENT_HOVER", ())						
		self.addOption(Option("NJAGCM_ShowCompletedPercent",						
						 "NJAGCM", "Show Game Completed Percent", False, zs_Text, zsHover,		
						 InterfaceDirtyBits.GameData_DIRTY_BIT))		

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_NJAGCM_SHOWDATE_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_NJAGCM_SHOWDATE_HOVER", ())						
		self.addOption(Option("NJAGCM_ShowDate",						
						 "NJAGCM", "Show Turns", True, zs_Text, zsHover,		
						 InterfaceDirtyBits.GameData_DIRTY_BIT))		

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_NJAGCM_ALTERNATETEXT_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_NJAGCM_ALTERNATETEXT_HOVER", ())						
		self.addOption(Option("NJAGCM_AlternateText",						
						 "NJAGCM", "Alternate Views", False, zs_Text, zsHover,		
						 InterfaceDirtyBits.GameData_DIRTY_BIT))		

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_NJAGCM_ALTTIMING_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_NJAGCM_ALTTIMING_HOVER", ())						
		self.addOption(OptionList("NJAGCM_AltTiming",						
							 "NJAGCM", "Alternating Time", 5, zs_Text, zsHover,	
							 [2, 5, 10, 15, 30, 45, 60, 300, 600],	
							 InterfaceDirtyBits.GameData_DIRTY_BIT))	

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_NJAGCM_SHOWALTTIME_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_NJAGCM_SHOWALTTIME_HOVER", ())						
		self.addOption(Option("NJAGCM_ShowAltTime",						
						 "NJAGCM", "Alternate Show Game Clock", False, zs_Text, zsHover,		
						 InterfaceDirtyBits.GameData_DIRTY_BIT))		

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_NJAGCM_SHOWALTCOMPLETEDTURNS_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_NJAGCM_SHOWALTCOMPLETEDTURNS_HOVER", ())						
		self.addOption(Option("NJAGCM_ShowAltCompletedTurns",						
						 "NJAGCM", "Alternate Show Game Completed Turns", False, zs_Text, zsHover,		
						 InterfaceDirtyBits.GameData_DIRTY_BIT))		

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_NJAGCM_SHOWALTTOTALTURNS_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_NJAGCM_SHOWALTTOTALTURNS_HOVER", ())						
		self.addOption(Option("NJAGCM_ShowAltTotalTurns",						
						 "NJAGCM", "Alternate Show Game Total Turns", False, zs_Text, zsHover,		
						 InterfaceDirtyBits.GameData_DIRTY_BIT))		

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_NJAGCM_SHOWALTCOMPLETEDPERCENT_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_NJAGCM_SHOWALTCOMPLETEDPERCENT_HOVER", ())						
		self.addOption(Option("NJAGCM_ShowAltCompletedPercent",						
						 "NJAGCM", "Alternate Show Game Completed Percent", True, zs_Text, zsHover,		
						 InterfaceDirtyBits.GameData_DIRTY_BIT))		

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_NJAGCM_SHOWALTDATE_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_NJAGCM_SHOWALTDATE_HOVER", ())						
		self.addOption(Option("NJAGCM_ShowAltDate",						
						 "NJAGCM", "Alternate Show Turns", True, zs_Text, zsHover,		
						 InterfaceDirtyBits.GameData_DIRTY_BIT))		


	def isEnabled(self):							
		return self.getBoolean('NJAGCM_Enabled')						
								
	def isShowEra(self):							
		return self.getBoolean('NJAGCM_ShowEra')						
								
	def isUseEraColor(self):							
		return self.getBoolean('NJAGCM_ShowEraColor')						
								
	def getEraColor(self, era):							
		return self.getString('NJAGCM_Color_' + era)						
								
								
	def isShowTime(self):							
		return self.getBoolean('NJAGCM_ShowTime')						
								
	def isShowGameTurn(self):							
		return self.getBoolean('NJAGCM_ShowCompletedTurns')						
								
	def isShowTotalTurns(self):							
		return self.getBoolean('NJAGCM_ShowTotalTurns')						
								
	def isShowPercentComplete(self):							
		return self.getBoolean('NJAGCM_ShowCompletedPercent')						
								
	def isShowDateGA(self):							
		return self.getBoolean('NJAGCM_ShowDate')						
								
								
	def isAlternateTimeText(self):							
		return self.getBoolean('NJAGCM_AlternateText')						
								
	def getAlternatePeriod(self):							
		return self.getInt('NJAGCM_AltTiming')						
								
								
	def isShowAltTime(self):							
		return self.getBoolean('NJAGCM_ShowAltTime')						
								
	def isShowAltGameTurn(self):							
		return self.getBoolean('NJAGCM_ShowAltCompletedTurns')						
								
	def isShowAltTotalTurns(self):							
		return self.getBoolean('NJAGCM_ShowAltTotalTurns')						
								
	def isShowAltPercentComplete(self):							
		return self.getBoolean('NJAGCM_ShowAltCompletedPercent')						
								
	def isShowAltDateGA(self):							
		return self.getBoolean('NJAGCM_ShowAltDate')						
								
								
# The singleton BugNJAGCOptions object								
								
__g_options = BugNJAGCOptions()								
def getOptions():								
	return __g_options							
								
