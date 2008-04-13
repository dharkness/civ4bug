## BugScreensOptions								
## Facade for accessing various screen options								
## BUG Mod - Copyright 2007								
								
from CvPythonExtensions import *								
from BugOptions import OptionsFacade, Option, OptionList								
localText = CyTranslator()
								
class BugScreensOptions(OptionsFacade):								
								
	def __init__(self):							
		OptionsFacade.__init__(self)						
								
		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_MAIN_OPTIONSKEY_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_MAIN_OPTIONSKEY_HOVER", ())						
		self.addOption(Option("Main_OptionsKey",						
							  "Screens", "Options Shortcut Reminder", True, zs_Text, zsHover,	
							  InterfaceDirtyBits.GameData_DIRTY_BIT))	

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_MAIN_GPBAR_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_MAIN_GPBAR_HOVER", ())						
		self.addOption(Option("Main_GPBar",						
							  "Screens", "GP Progress Bar", True, zs_Text, zsHover,	
							  InterfaceDirtyBits.GameData_DIRTY_BIT))	

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_MAIN_GPBAR_TYPES_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_MAIN_GPBAR_TYPES_HOVER", ())						
		self.addOption(OptionList("Main_GPBar_Types",						
								  "Screens", "GP Progress Bar Types", 0, zs_Text, zsHover,
								  ['None', 'One', 'Maximum'], None,
								  InterfaceDirtyBits.GameData_DIRTY_BIT))
								
		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_MAIN_COMBAT_COUNTER_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_MAIN_COMBAT_COUNTER_HOVER", ())						
		self.addOption(Option("Main_Combat_Counter",						
							  "Screens", "Combat Counter", True, zs_Text, zsHover,	
							  InterfaceDirtyBits.GameData_DIRTY_BIT))	

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_MAIN_CITYARROWS_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_MAIN_CITYARROWS_HOVER", ())						
		self.addOption(Option("Main_CityArrows",						
							  "Screens", "City Cycle Arrows", True, zs_Text, zsHover,	
							  InterfaceDirtyBits.MiscButtons_DIRTY_BIT))	

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_UNIT_PROMO_AVAILABLE_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_UNIT_PROMO_AVAILABLE_HOVER", ())						
		self.addOption(Option("Unit_Promo_Available",						
							  "PlotList", "Promo Available", True, zs_Text, zsHover,	
							  InterfaceDirtyBits.PlotListButtons_DIRTY_BIT))	

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_UNIT_ACTIONS_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_UNIT_ACTIONS_HOVER", ())						
		self.addOption(Option("Unit_Actions",						
							  "PlotList", "Unit Actions", True, zs_Text, zsHover,	
							  InterfaceDirtyBits.PlotListButtons_DIRTY_BIT))	

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_GREAT_GENERAL_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_GREAT_GENERAL_HOVER", ())						
		self.addOption(Option("Great_General",						
							  "PlotList", "Great General", True, zs_Text, zsHover,	
							  InterfaceDirtyBits.PlotListButtons_DIRTY_BIT))	

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_CDA_ENABLED_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_CDA_ENABLED_HOVER", ())						
		self.addOption(Option("CDA_Enabled",						
							  "Screens", "CustDomAdv", True, zs_Text, zsHover)

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_EFA_GLANCE_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_EFA_GLANCE_HOVER", ())						
		self.addOption(Option("EFA_Glance",						
							  "Screens", "EFA Glance", True, zs_Text, zsHover)

\		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_EFA_GLANCE_SMILIES_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_EFA_GLANCE_SMILIES_HOVER", ())						
		self.addOption(Option("EFA_Glance_Smilies",						
							  "Screens", "EFA Glance Smilies", True, zs_Text, zsHover)

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_TECH_GPPREFS_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_TECH_GPPREFS_HOVER", ())						
		self.addOption(Option("Tech_GPPrefs",						
							  "Screens", "GP Tech Prefs", True, zs_Text, zsHover)

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_TECHSCREEN_WIDE_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_TECHSCREEN_WIDE_HOVER", ())						
		self.addOption(Option("TechScreen_Wide",						
							  "Screens", "Wide Tech Screen", True, zs_Text, zsHover)

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_SEVOPEDIA_ENABLED_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_SEVOPEDIA_ENABLED_HOVER", ())						
		self.addOption(Option("Sevopedia_Enabled",						
							  "Screens", "Sevopedia", True, zs_Text, zsHover)

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_SEVOPEDIA_SORT_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_SEVOPEDIA_SORT_HOVER", ())						
		self.addOption(Option("Sevopedia_Sort",						
							  "Screens", "Sevopedia Sort", True, zs_Text, zsHover)


	def isShowOptionsKeyReminder(self):							
		return self.getBoolean('Main_OptionsKey')						
								
	def isShowGPProgressBar(self):							
		return self.getBoolean('Main_GPBar')						
								
	def getGPBarPercents(self):							
		return self.getInt('Main_GPBar_Types')						
								
	def isGPBarTypesNone(self):							
		return self.getGPBarPercents() == 0						
								
	def isGPBarTypesOne(self):							
		return self.getGPBarPercents() == 1						
								
	def isGPBarTypesMax(self):							
		return self.getGPBarPercents() == 2						
								
	def isShowCombatCounter(self):							
		return self.getBoolean('Main_Combat_Counter')						
								
								
	def isShowCityCycleArrows(self):							
		return self.getBoolean('Main_CityArrows')						
								
								
	def isShowUnitPromo(self):							
		return self.getBoolean('Unit_Promo_Available')						
								
	def isShowUnitActions(self):							
		return self.getBoolean('Unit_Actions')						
								
	def isShowGreatGeneral(self):							
		return self.getBoolean('Great_General')						
								
								
	def isCustDomAdv(self):							
		return self.getBoolean('CDA_Enabled')						
								
								
	def isShowGlance(self):							
		return self.getBoolean("EFA_Glance")						
								
	def isShowGlanceSmilies(self):							
		return self.getBoolean("EFA_Glance_Smilies")						
								
								
	def isShowGPTechPrefs(self):							
		return self.getBoolean("Tech_GPPrefs")						
								
								
	def isSevopedia(self):							
		return self.getBoolean('Sevopedia_Enabled')						
								
	def isSortSevopedia(self):							
		return self.getBoolean('Sevopedia_Sort')						
								
	def isWideTechScreen(self):							
		return self.getBoolean('TechScreen_Wide')						
								
# The singleton BugScreensOptions object								
								
__g_options = BugScreensOptions()								
def getOptions():								
	return __g_options							
								
								
								
								
