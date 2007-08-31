## UnitName
## by Ruff_Hi
## for BUG Mod
##-------------------------------------------------------------------
## Naming Convention
##  - %n% - no naming convention, uses standard civ4
##  - %ct% - City
##  - %v% - Civilization
##  - %c[n]% - count across all units (increments based on unit)
##  - %cu[n]% - count across same unit (increments based on unit)
##  - %cc[n]% - count across same combat type (increments based on combat type)
##  - %cd[n]% - count across same domain (increments based on domain)
##  - %tt[n][x:y]% - total where the total is a random number between x and y (number)
##  - %tc[n][x]% - total count (starts at x, incremented by 1 each time %tt is reset to 1)
##  - %r% - random name
##  - %rc% - random civ related name
##  - %u% - unit (eg Archer)
##  - %t% - combat type (Melee)
##  - %d% - domain (Water)
##  - %l% - leader
##
## Where [n] can be either 's', 'A', 'a', 'p', 'g', 'n', 'o' or 'r' for ...
##  - silent (not shown)
##  - alpha (A, B, C, D, ...)
##  - alpha (a, b, c, d, ...)
##  - phonetic (alpha, bravo, charlie, delta, echo, ...)
##  - greek (alpha, beta, gamma, delta, epsilon, ...)
##  - number
##  - ordinal (1st, 2nd, 3rd, 4th, ...)
##  - roman (I, IV, V, X, ...)
##
## Coding Steps
##
## 1. check if a unit exists, if not, do nothing
## 2. call unit name engine
## 3. update unit name if returned name is not NULL
##
## Unit name engine:
##
## 1. get naming convention from ini file
##    a. if isAdvanced, get advanced naming convention
##    b. otherwise, get combat based naming convention
##    c. if naming convention is 'DEFAULT', get default naming convention
## 
## 2. determine if you have 'civ naming' or no valid naming codes in your naming convention, if YES, return 'NULL'
## 3. determine if you have 'random' in your naming convention, if YES, call random engine and return value
## 4. determine if you have 'random civ related' in your naming convention, if YES, call random civ related engine and return value
## 
## 5. swap out fixed items (ie unit, combat type, domain, leader, civilization, city, etc) from naming convention
## 
## 6. determine if you have any count items in naming convention; return if FALSE
## 
## 7. determine key for counting (this information is stored in the save file)
## a. get latest count from save (if not found, initilize)
## b. increment count by 1
## c. test against total (if required), adjust total and 2nd total if required
## 
## 8. format count items
## 
## 9. replace formatted count items in naming convention
## 
## 10. return name
##-------------------------------------------------------------------

from CvPythonExtensions import *
import CvUtil
import PyHelpers
import BugUnitNameOptions
import Roman

gc = CyGlobalContext()
BugUnitName = BugUnitNameOptions.BugUnitNameOptions()

phonetic_array = ['ALPHA', 'BRAVO', 'CHARLIE', 'DELTA', 'ECHO', 'FOXTROT', 'GOLF', 'HOTEL', 'INDIA', 'JULIETT', 'KILO', 'LIMA', 'MIKE',
                  'NOVEMBER', 'OSCAR', 'PAPA', 'QUEBEC', 'ROMEO', 'SIERRA', 'TANGO', 'UNIFORM', 'VICTOR', 'WHISKEY', 'X-RAY', 'YANKEE', 'ZULU']

greek_array = ['ALPHA', 'BETA', 'GAMMA', 'DELTA', 'EPSILON', 'ZETA', 'ETA', 'THETA', 'IOTA', 'KAPPA', 'LAMBDA', 'MU', 'NU', 'XI',
               'OMICRON', 'PI', 'RHO', 'SIGMA', 'TAU', 'UPSILON', 'PHI', 'CHI', 'PSI', 'OMEGA']

ordinal_array = 'th st nd rd th th th th th th'.split()

class UnitNameEventManager:

	def __init__(self, eventManager):

		BuildUnitName(eventManager)

class AbstractBuildUnitName(object):

	def __init__(self, eventManager, *args, **kwargs):
		super(AbstractBuildUnitName, self).__init__(*args, **kwargs)

class BuildUnitName(AbstractBuildUnitName):

	def __init__(self, eventManager, *args, **kwargs):
		super(BuildUnitName, self).__init__(eventManager, *args, **kwargs)

#		eventManager.addEventHandler("kbdEvent", self.onKbdEvent)
		eventManager.addEventHandler("unitBuilt", self.onUnitBuilt)

		self.eventMgr = eventManager

	def onKbdEvent(self, argsList):
		eventType,key,mx,my,px,py = argsList
		if ( eventType == self.eventMgr.EventKeyDown ):
			if (int(key) == int(InputTypes.KB_T)
			and self.eventMgr.bCtrl
			and self.eventMgr.bAlt):
				for j in range(pPlot.getNumUnits()):
					pLoopUnit = CyInterface().getInterfacePlotUnit(pPlot, j)
					zsEra = getEra(pUnit)
					zsUnitType = getUnitType(pUnit)
					zsUnitCombat = getUnitCombat(pUnit)
					zsUnitClass = getUnitClass(pUnit)
					zMsg = "%s %s %s %s" % (zsEra, zsUnitClass, zsUnitCombat, zsUnitType)
					CyInterface().addImmediateMessage(zMsg, "")

		return 1


	def onUnitBuilt(self, argsList):
		'Unit Completed'

#		put in while I am developing this feature
		return

#		city = argsList[0]
#		pUnit = argsList[1]
#		iOwner = gc.getPlayer(pUnit.getOwner())

#		if (not pUnit.getOwner() == CyGame().getActivePlayer()
#		or not BugUnitName.isEnabled()):
#			return

#		zsEra = getEra(pUnit)
#		zsUnitType = getUnitType(pUnit)
#		zsUnitCombat = getUnitCombat(pUnit)
#		zsUnitClass = getUnitClass(pUnit)

#		if (BugUnitName.isAdvanced()):
#			zsUnitNameConv = BugUnitName.getAdvanced(zsEra[4:], zsUnitClass[10:])
#		else:
#			zsUnitNameConv = BugUnitName.getCombat(zsUnitCombat)

#		if (zsUnitNameConv = "DEFAULT"): zsUnitNameConv = BugUnitName.getDefault()

#		zsName = zsUnitNameConv
#		zsName = "%u% %c[o]% of %c%"

#		zsName = zsName.replace("%ct%", zsCity)
#		zsName = zsName.replace("%v%", zsCiv)
#		zsName = zsName.replace("%u%", zsUnit)
#		zsName = zsName.replace("%t%", zsCombat)
#		zsName = zsName.replace("%d%", zsDomain)
#		zsName = zsName.replace("%l%", zsLeader)





#		civtype = iOwner.getCivilizationType()








#		zsUnitNameConv = BugUnitName.getCombat(zsUnitCombat)
#		if zsUnitNameConv == 'DEFAULT':
#			zsUnitNameConv = BugUnitName.getDefault()

#		unit.setName(zsUnitNameConv)

#		return


	def getEra(self, pUnit):

		# Return immediately if the unit passed in is invalid
		if (pUnit == None):
			return None
	
		# Return immediately if the unit passed in is invalid
		if (pUnit.isNone()):
			return None

		iPlayer = pUnit.getOwner()
		pPlayer = gc.getPlayer(iPlayer)
		iPlayerEra = pPlayer.getCurrentEra()
		infoPlayerEra = gc.getEraInfo(iPlayerEra)
		return infoPlayerEra.getType()





	def getUnitCombat(self, pUnit):

		# Return immediately if the unit passed in is invalid
		if (pUnit == None):
			return "None"
			
		# Return immediately if the unit passed in is invalid
		if (pUnit.isNone()):
			return "None"

		iUnitCombat = pUnit.getUnitCombatType()
		infoUnitCombat = gc.getUnitCombatInfo(iUnitCombat)

		if (infoUnitCombat == None):
			return "None"

		return infoUnitCombat.getType()



	def getUnitClass(self, pUnit):

		# Return immediately if the unit passed in is invalid
		if (pUnit == None):
			return "None"
	
		# Return immediately if the unit passed in is invalid
		if (pUnit.isNone()):
			return "None"

		iUnitClass = pUnit.getUnitClassType()
		infoUnitClass = gc.getUnitClassInfo(iUnitClass)
		return infoUnitClass.getType()




	def getUnitType(self, pUnit):

		# Return immediately if the unit passed in is invalid
		if (pUnit == None):
			return "None"
	
		# Return immediately if the unit passed in is invalid
		if (pUnit.isNone()):
			return "None"

		iUnitType = pUnit.getUnitType()
		infoUnitType = gc.getUnitInfo(iUnitType)
		return str(infoUnitType.getType())


	def getNumberFormat(self, n, i):
		if (n == "s"):     # silent
			return ""
		elif (n == "a"):   # lower case alpha
			return chr(96+i)
		elif (n == "A"):   # upper case alpha
			return chr(64+i)
		elif (n == "p"):   # phonetic
			return phonetic_array[i]
		elif (n == "g"):   # greek
			return greek_array[i]
		elif (n == "n"):   # number    
			return str(i)
		elif (n == "o"):   # ordinal
			return getOrdinal(i)
		elif (n == "r"):   # roman
			return Roman.toRoman(i)
		else:
			return str(i)


	def getOrdinal(i):
		if i % 100 in (11, 12, 13): #special case
			return '%dth' % i
		return str(i) + ordinal_array[i % 10]











#zsName = zsName.replace("%ct%", zsCity)



#    * getting a single char: "banana"[3] -> "a"
#    * slice notation (like sub/midstr): "banana"[2:4] -> "na"
#    * "banana".find("an") -> 1
#    * "banana".find("an", 2) -> 3
#    * "banana".find("an", 2, 4) -> -1
#    * "banana".split("n") -> [ "ba", "a", "a" ]




