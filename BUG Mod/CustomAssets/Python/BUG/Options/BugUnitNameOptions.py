## BugUnitNameOptions
## Facade for accessing City Screen options
## BUG Mod - Copyright 2007

from CvPythonExtensions import *
from BugOptions import OptionsFacade, Option, OptionList

class BugUnitNameOptions(OptionsFacade):

	def __init__(self):
		OptionsFacade.__init__(self)
		self.addOption(Option("UnitName_Enabled",
							  "UnitName", "Enabled", False,
							  "Enabled (There are also naming options in the ini file that take up too much room here).",
							  "When checked, uses the formats on this tab and in the INI file to name the player's units. \
Names can be built from plain text and format codes that appear between matching carets (^).\n\
    e.g. \"^cv^ ^ut^ from ^ct^\" --> \"American Archer from Boston\"\n\n\
General Codes:\n\
    civ4 - Use built-in Civ4 names\n\
    rd - Random name\n\
    rc - Random civ-related name\n\
Unit Info Codes:\n\
    ct - City where unit was built (e.g. Boston)\n\
    cv - Civilization that built the unit in adjective form (e.g. American)\n\
    ut - Unit type (e.g. Archer)\n\
    cb - Combat type (e.g. Melee)\n\
    dm - Domain type (e.g. Water)\n\
    ld - Leader that built the unit (e.g. Roosevelt)\n\
Counting Codes:\n\
    cnt[f] - Count across all units\n\
    cntu[f] - Count per unit type\n\
    cntct[f] - Count per city\n\
    cntuct[f] - Count per unit/city combination\n\
    cntc[f] - Count per combat type\n\
    cntd[f] - Count per domain\n\
    tt1[f][x:y] - Count up to a number chosen between x and y\n\
    tt1[f][x] - Count from x, incrementing each time tt1 code is reset\n\
    * f in [f] is one of s, A, a, p, g, n, o, r (see readme)"))
#		self.addOption(Option("UnitName_UseAdvanced",
#							  "UnitName", "UseAdvanced", False,
#							  "Use Advanced Methods - see ini file for Era_UnitClass options",
#							  "When checked, the advanced naming conventions in 'BUG Mod.ini' file will be used."))
		self.addOption(Option("UnitName_Default",
							  "UnitName", "Default", '^u^ ^cnt[r]^ of ^ct^',
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
		self.addOption(Option("UnitName_Combat_None",
							  "UnitName", "CombatNone", 'DEFAULT',
							  "Naming Convention: Combat[None]",
							  "Enter the user defined naming convention for combat units 'None'."))
		self.addOption(Option("UnitName_Combat_RECON",
							  "UnitName", "CombatRECON", 'DEFAULT',
							  "Naming Convention: Combat[RECON]",
							  "Enter the user defined naming convention for combat units 'RECON'."))
		self.addOption(Option("UnitName_Combat_SIEGE",
							  "UnitName", "CombatSIEGE", 'DEFAULT',
							  "Naming Convention: Combat[SIEGE]",
							  "Enter the user defined naming convention for combat units 'SIEGE'."))

	def isEnabled(self):
		return self.getBoolean('UnitName_Enabled')

	def setEnabled(self, value):
		self.setValue('UnitName_Enabled', value)

#	def isAdvanced(self):
#		return self.getBoolean('UnitName_UseAdvanced')


	# get standard naming conventions
	def getDefault(self):
		return self.getString('UnitName_Default')
	
	def getCombat(self, Combat_Type):
		return self.getString('UnitName_Combat_' + Combat_Type)

	def getAdvanced(self, Era, UnitClass):
		return self.getRawString('UnitName', Era + '_' + UnitClass, 'DEFAULT')


# The singleton BugUnitNameOptions object

__g_options = BugUnitNameOptions()
def getOptions():
	return __g_options
