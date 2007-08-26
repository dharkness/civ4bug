## BugUnitNameOptions
## Facade for accessing City Screen options
## BUG Mod - Copyright 2007

from CvPythonExtensions import *
from BugOptions import OptionsFacade, Option, OptionList

class BugUnitNameOptions(OptionsFacade):

	def __init__(self):
		OptionsFacade.__init__(self)
		self.addOption(Option("UnitName_Enable",
							  "UnitName", "Enable", False,
							  "Enabled",
							  "When checked, the player's units will be named."))
		self.addOption(Option("UnitName_UseAdvanced",
							  "UnitName", "UseAdvanced", False,
							  "Use Advanced Methods",
							  "When checked, the advanced naming conventions in 'BUG_UnitName.ini' file will be used."))
		self.addOption(Option("UnitName_Default",
							  "UnitName", "UserDefined", 'blah blah blah',
							  "Naming Convention: DEFAULT",
							  "Enter the user defined naming convention (see docs for further information)."))
		self.addOption(Option("UnitName_Combat_AIR",
							  "UnitName", "CombatAIR", 'DEFAULT',
							  "Naming Convention: Combat[AIR]",
							  "Enter the user defined naming convention for combat units 'AIR'."))
		self.addOption(Option("UnitName_Combat_ARCHER",
							  "UnitName", "CombatARCHER", 'DEFAULT',
							  "Naming Convention: Combat[ARCHER]",
							  "Enter the user defined naming convention for combat units 'ARCHER'."))
		self.addOption(Option("UnitName_Combat_ARMOR",
							  "UnitName", "CombatARMOR", 'DEFAULT',
							  "Naming Convention: Combat[ARMOR]",
							  "Enter the user defined naming convention for combat units 'ARMOR'."))
		self.addOption(Option("UnitName_Combat_GUN",
							  "UnitName", "CombatGUN", 'DEFAULT',
							  "Naming Convention: Combat[GUN]",
							  "Enter the user defined naming convention for combat units 'GUN'."))
		self.addOption(Option("UnitName_Combat_HELICOPTER",
							  "UnitName", "CombatHELICOPTER", 'DEFAULT',
							  "Naming Convention: Combat[HELICOPTER]",
							  "Enter the user defined naming convention for combat units 'HELICOPTER'."))
		self.addOption(Option("UnitName_Combat_MELEE",
							  "UnitName", "CombatMELEE", 'DEFAULT',
							  "Naming Convention: Combat[MELEE]",
							  "Enter the user defined naming convention for combat units 'MELEE'."))
		self.addOption(Option("UnitName_Combat_MOUNTED",
							  "UnitName", "CombatMOUNTED", 'DEFAULT',
							  "Naming Convention: Combat[MOUNTED]",
							  "Enter the user defined naming convention for combat units 'MOUNTED'."))
		self.addOption(Option("UnitName_Combat_NAVAL",
							  "UnitName", "CombatNAVAL", 'DEFAULT',
							  "Naming Convention: Combat[NAVAL]",
							  "Enter the user defined naming convention for combat units 'NAVAL'."))
		self.addOption(Option("UnitName_Combat_RECON",
							  "UnitName", "CombatRECON", 'DEFAULT',
							  "Naming Convention: Combat[RECON]",
							  "Enter the user defined naming convention for combat units 'RECON'."))
		self.addOption(Option("UnitName_Combat_SIEGE",
							  "UnitName", "CombatSIEGE", 'DEFAULT',
							  "Naming Convention: Combat[SIEGE]",
							  "Enter the user defined naming convention for combat units 'SIEGE'."))

	def isEnabled(self):
		return self.getBoolean('UnitName_Enable')

	def setEnabled(self, value):
		self.setValue('UnitName_Enable', value)

	def isAdvanced(self):
		return self.getBoolean('UnitName_UseAdvanced')


# get standard naming conventions
	def getDefault(self):
		return self.getString('UnitName_Default')
	
	def getCombat(self, Combat_Type):
		return self.getString('UnitName_Combat_' + Combat_Type)


# The singleton BugUnitNameOptions object

__g_options = BugUnitNameOptions()
def getOptions():
	return __g_options
