## BugUnitNameOptions								
## Facade for accessing City Screen options								
## BUG Mod - Copyright 2007								
								
from CvPythonExtensions import *								
from BugOptions import OptionsFacade, Option, OptionList								
localText = CyTranslator()
								
class BugUnitNameOptions(OptionsFacade):								
								
	def __init__(self):							
		OptionsFacade.__init__(self)						
								
		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_UNITNAME_ENABLED_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_UNITNAME_ENABLED_HOVER", ())						
		self.addOption(Option("UnitName_Enabled",						
							  "UnitName", "Enabled", False, zs_Text, zsHover)

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_UNITNAME_USEADVANCED_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_UNITNAME_USEADVANCED_HOVER", ())						
		self.addOption(Option("UnitName_UseAdvanced",						
							  "UnitName", "UseAdvanced", False, zs_Text, zsHover)	

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_UNITNAME_DEFAULT_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_UNITNAME_DEFAULT_HOVER", ())						
		self.addOption(Option("UnitName_Default",						
							  "UnitName", "Default", '^u^ ^cnt[r]^ of ^ct^', zs_Text, zsHover)	

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_UNITNAME_COMBAT_AIR_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_UNITNAME_COMBAT_AIR_HOVER", ())						
		self.addOption(Option("UnitName_Combat_AIR",						
							  "UnitName", "CombatAIR", 'DEFAULT', zs_Text, zsHover)	

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_UNITNAME_COMBAT_ARCHER_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_UNITNAME_COMBAT_ARCHER_HOVER", ())						
		self.addOption(Option("UnitName_Combat_ARCHER",						
							  "UnitName", "CombatARCHER", 'DEFAULT', zs_Text, zsHover)	

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_UNITNAME_COMBAT_ARMOR_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_UNITNAME_COMBAT_ARMOR_HOVER", ())						
		self.addOption(Option("UnitName_Combat_ARMOR",						
							  "UnitName", "CombatARMOR", 'DEFAULT', zs_Text, zsHover)	

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_UNITNAME_COMBAT_GUN_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_UNITNAME_COMBAT_GUN_HOVER", ())						
		self.addOption(Option("UnitName_Combat_GUN",						
							  "UnitName", "CombatGUN", 'DEFAULT', zs_Text, zsHover)	

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_UNITNAME_COMBAT_HELICOPTER_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_UNITNAME_COMBAT_HELICOPTER_HOVER", ())						
		self.addOption(Option("UnitName_Combat_HELICOPTER",						
							  "UnitName", "CombatHELICOPTER", 'DEFAULT', zs_Text, zsHover)	

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_UNITNAME_COMBAT_MELEE_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_UNITNAME_COMBAT_MELEE_HOVER", ())						
		self.addOption(Option("UnitName_Combat_MELEE",						
							  "UnitName", "CombatMELEE", 'DEFAULT', zs_Text, zsHover)	

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_UNITNAME_COMBAT_MOUNTED_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_UNITNAME_COMBAT_MOUNTED_HOVER", ())						
		self.addOption(Option("UnitName_Combat_MOUNTED",						
							  "UnitName", "CombatMOUNTED", 'DEFAULT', zs_Text, zsHover)	

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_UNITNAME_COMBAT_NAVAL_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_UNITNAME_COMBAT_NAVAL_HOVER", ())						
		self.addOption(Option("UnitName_Combat_NAVAL",						
							  "UnitName", "CombatNAVAL", 'DEFAULT', zs_Text, zsHover)	

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_UNITNAME_COMBAT_NONE_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_UNITNAME_COMBAT_NONE_HOVER", ())						
		self.addOption(Option("UnitName_Combat_None",						
							  "UnitName", "CombatNone", 'DEFAULT', zs_Text, zsHover)	

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_UNITNAME_COMBAT_RECON_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_UNITNAME_COMBAT_RECON_HOVER", ())						
		self.addOption(Option("UnitName_Combat_RECON",						
							  "UnitName", "CombatRECON", 'DEFAULT', zs_Text, zsHover)	

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_UNITNAME_COMBAT_SIEGE_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_UNITNAME_COMBAT_SIEGE_HOVER", ())						
		self.addOption(Option("UnitName_Combat_SIEGE",						
							  "UnitName", "CombatSIEGE", 'DEFAULT', zs_Text, zsHover)	

								
	def isEnabled(self):							
		return self.getBoolean('UnitName_Enabled')						
								
	def setEnabled(self, value):							
		self.setValue('UnitName_Enabled', value)						
								
	def isAdvanced(self):							
		return self.getBoolean('UnitName_UseAdvanced')						
								
								
	# get standard naming conventions							
	def getDefault(self):							
		return self.getString('UnitName_Default')						
								
	def getCombat(self, Combat_Type):							
		return self.getString('UnitName_Combat_' + Combat_Type)						
								
	def getAdvanced(self, Era, UnitClass):							
		return self.getAdvUnitName('UnitName', Era + '_' + UnitClass, 'DEFAULT')						
								
								
# The singleton BugUnitNameOptions object								
								
__g_options = BugUnitNameOptions()								
def getOptions():								
	return __g_options							
								
								
