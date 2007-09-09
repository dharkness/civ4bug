## UnitName
## by Ruff_Hi
## for BUG Mod
##-------------------------------------------------------------------
## Naming Convention
##  - ^civ4^ - no naming convention, uses standard civ4
##  - ^rd^ - random name
##  - ^rc^ - random civ related name
##  - ^ct^ - City
##  - ^cv^ - Civilization
##  - ^ut^ - unit (eg Archer)
##  - ^cb^ - combat type (Melee)
##  - ^dm^ - domain (Water)
##  - ^ld^ - leader
##  - ^cnt[f]^ - count across all units (increments based on unit)
##  - ^cntu[f]^ - count across same unit (increments based on unit)
##  - ^cntct[f]^ - count across same city (increments based on unit)
##  - ^cntuct[f]^ - count across same unit / city (increments based on unit)
##  - ^cntc[f]^ - count across same combat type (increments based on combat type)
##  - ^cntd[f]^ - count across same domain (increments based on domain)
##  - ^tt1[f][x:y]^ - total where the total is a random number between x and y (number)
##  - ^tt2[f][x]^ - total count (starts at x, incremented by 1 each time ^tt is reset to 1)
##
## Where [f] can be either 's', 'A', 'a', 'p', 'g', 'n', 'o' or 'r' for ...
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
##    a. try to get the advanced naming convention
##    b. if it returns 'DEFAULT', then get the combat based naming convention
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
import RandomNameUtils
import random
import Popup as PyPopup

#######SD Tool Kit#######

import SdToolKit
sdEcho			= SdToolKit.sdEcho
sdModInit		= SdToolKit.sdModInit
sdModLoad		= SdToolKit.sdModLoad
sdModSave		= SdToolKit.sdModSave
sdEntityInit	= SdToolKit.sdEntityInit
sdEntityExists	= SdToolKit.sdEntityExists
sdEntityWipe	= SdToolKit.sdEntityWipe
sdGetVal		= SdToolKit.sdGetVal
sdSetVal		= SdToolKit.sdSetVal
sdGroup			= "UnitCnt"

############################

gc = CyGlobalContext()
PyInfo = PyHelpers.PyInfo
BugUnitName = BugUnitNameOptions.getOptions()

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
#		if ( eventType == self.eventMgr.EventKeyDown ):
#			if (int(key) == int(InputTypes.KB_N)
#			and self.eventMgr.bCtrl
#			and self.eventMgr.bAlt):

#				popup = PyPopup.PyPopup(CvUtil.EventReminderStore, EventContextTypes.EVENTCONTEXT_SELF)
#				popup.setHeaderString("Enter unit name code")
#				popup.createEditBox("", 1)
#				popup.addButton("Ok")
#				popup.addButton("Cancel")
#				popup.launch(False, PopupStates.POPUPSTATE_IMMEDIATE)

#				if (popup.getButtonClicked() != 1):
#					zsUnitNameConv = popup.getEditBoxString(1)
				
#				player = gc.getActivePlayer()
#				for i in range(player.getNumUnits()):
#					unit = player.getUnit(i)
#					self.RuffEcho("Unit %d is a %s" %(i, unit.getName()), true, true)
#					if (unit.getName() == "Worker"):
#						city = unit.plot().getPlotCity()
#						self.RuffEcho("...in city %s" %(city.getName()), true, true)
#						self.onUnitBuilt([city, unit])
#						break

#					for i in range(CyMap().numPlots()):
#						tPlot = CyMap().plot(CyMap().plotX(i),CyMap().plotY(i))
#						if (tPlot.isCity()
#						and tPlot.getOwner() == CyGame().getActivePlayer()):
#							pPlot = tPlot
#							i = CyMap().numPlots()
#
#					for j in range(pPlot.getNumUnits()):
#						pLoopUnit = CyInterface().getInterfacePlotUnit(pPlot, j)
#
#						iPlayer = pLoopUnit.getOwner()
#						pPlayer = gc.getPlayer(iPlayer)
#						pCity = pPlayer.getCity(0)
#
#						zsEra = gc.getEraInfo(pPlayer.getCurrentEra()).getType()
#						zsUnitCombat = self.getUnitCombat(pLoopUnit)
#						zsUnitClass = gc.getUnitClassInfo(pLoopUnit.getUnitClassType()).getType()
#
#						zsUnitNameConv = self.getUnitNameConvFromIniFile(zsEra, zsUnitClass, zsUnitCombat)
#						self.RuffEcho("UnitNameEM [" + zsUnitNameConv + "]", false, true)
#
#						zsUnitNameConv = "^ut^ ^cnt[r]^ ^tt1[g][5:7]^ : ^ct^ ^tt2[o][101]^"
#
#						self.RuffEcho("UnitNameEM-0 [" + zsUnitNameConv + "]", false, true)
#
#						zsUnitName = self.getUnitName(zsUnitNameConv, pLoopUnit, pCity)
#
#						if not (zsUnitName == ""):
#							pLoopUnit.setName(zsUnitName)
#
#						zMsg = "unit name is %s" % (zsUnitName)
#						CyInterface().addImmediateMessage(zMsg, "")

#				return 1
		return 0


	def onUnitBuilt(self, argsList):
		'Unit Completed'

# I have this in as it doesn't work yet
#		return
	
		pCity = argsList[0]
		pUnit = argsList[1]
		iPlayer = pUnit.getOwner()
		pPlayer = gc.getPlayer(iPlayer)

		self.RuffEcho("onUnitBuild-A", false, true)

		if (pUnit == None
		or pUnit.isNone()):
			return

		self.RuffEcho("onUnitBuild-B %s %s %s" % (iPlayer, CyGame().getActivePlayer(), BugUnitName.isEnabled()), false, true)

		if not (iPlayer == CyGame().getActivePlayer()
		and BugUnitName.isEnabled()):
			return

		self.RuffEcho("onUnitBuild-C", false, true)

		zsEra = gc.getEraInfo(pPlayer.getCurrentEra()).getType()
		zsUnitCombat = self.getUnitCombat(pUnit)
		zsUnitClass = gc.getUnitClassInfo(pUnit.getUnitClassType()).getType()

		self.RuffEcho("ERA(%s)" % (zsEra), false, true)
		self.RuffEcho("Combat(%s)" % (zsUnitCombat), false, true)
		self.RuffEcho("Class(%s)" % (zsUnitClass), false, true)

		zsUnitNameConv = self.getUnitNameConvFromIniFile(zsEra, zsUnitClass, zsUnitCombat)
		zsUnitName = self.getUnitName(zsUnitNameConv, pUnit, pCity)

		self.RuffEcho("onUnitBuild-D", false, true)

		if not (zsUnitName == ""):
			pUnit.setName(zsUnitName)

		self.RuffEcho("onUnitBuild-E", false, true)

		return


	def getUnitName(self, sUnitNameConv, pUnit, pCity):

		iPlayer = pUnit.getOwner()
		pPlayer = gc.getPlayer(iPlayer)

		zsEra = gc.getEraInfo(pPlayer.getCurrentEra()).getType()
		zsCiv = gc.getPlayer(iPlayer).getCivilizationShortDescription(0)
		zsLeader = gc.getPlayer(iPlayer).getName()
		zsUnitCombat = self.getUnitCombat(pUnit)
		zsUnitClass = gc.getUnitClassInfo(pUnit.getUnitClassType()).getType()
		zsUnitType = gc.getUnitInfo(pUnit.getUnitType()).getType()
		zsUnitDomain = gc.getDomainInfo(pUnit.getDomainType()).getType()
		zsUnit = PyInfo.UnitInfo(pUnit.getUnitType()).getDescription()
		zsCity = pCity.getName()

		self.RuffEcho("ERA(%s)" % (zsEra), false, true)
		self.RuffEcho("Civ(%s)" % (zsCiv), false, true)
		self.RuffEcho("Leader(%s)" % (zsLeader), false, true)
		self.RuffEcho("Combat(%s)" % (zsUnitCombat), false, true)
		self.RuffEcho("Class(%s)" % (zsUnitClass), false, true)
		self.RuffEcho("Type(%s)" % (zsUnitType), false, true)
		self.RuffEcho("Domain(%s)" % (zsUnitDomain), false, true)
		self.RuffEcho("Unit(%s)" % (zsUnit), false, true)
		self.RuffEcho("City(%s)" % (zsCity), false, true)

		zsName = sUnitNameConv

		#if zsName == "":
		#zsName = "^ut^ ^cnt[r]^ Div ^tt1[s][5:7]^ : ^ct^ ^tt2[o][101]^"

		self.RuffEcho("UnitNameEM-A [" + zsName + "]", false, true)

##  - ^civ4^ - no naming convention, uses standard civ4
#		check if Civ4 naming convention is required
		if not (zsName.find("^civ4^") == -1):
			return ""

##  - ^rd^ - random name
#		check if random naming convention is required
		if not (zsName.find("^rd^") == -1):
			return RandomNameUtils.getRandomName()

		self.RuffEcho("UnitNameEM-B", false, true)

##  - ^rc^ - random civ related name
#		check if random civ related naming convention is required
		if not (zsName.find("^rc^") == -1):
			return RandomNameUtils.getRandomCivilizationName(iPlayer.getCivilizationType())

		self.RuffEcho("UnitNameEM-C [" + zsName + "]", false, true)

##  - ^ct^ - City
##  - ^cv^ - Civilization
##  - ^ut^ - unit (eg Archer)
##  - ^cb^ - combat type (Melee)
##  - ^dm^ - domain (Water)
##  - ^ld^ - leader
#		replace the fixed items in the naming conv
		zsName = zsName.replace("^ct^", zsCity)
		zsName = zsName.replace("^cv^", zsCiv)
		zsName = zsName.replace("^ut^", zsUnit)
		zsName = zsName.replace("^cb^", zsUnitCombat)
		zsName = zsName.replace("^dm^", zsUnitDomain)
		zsName = zsName.replace("^ld^", zsLeader)

		self.RuffEcho("UnitNameEM-D [" + zsName + "]", false, true)

#		check if there are any more codes to swap out, return if not
		if (zsName.find("^") == -1):
			return zsName

#		determine what I am counting across
		zsSDKey = self.getCounter(zsName)
		if zsSDKey == "UNIT":		zsSDKey = zsSDKey + zsUnit
		elif zsSDKey == "COMBAT":	zsSDKey = zsSDKey + zsUnitCombat
		elif zsSDKey == "CITY":		zsSDKey = zsSDKey + zsCity
		elif zsSDKey == "UNITCITY": zsSDKey = zsSDKey + zsUnit + zsCity
		elif zsSDKey == "DOMAIN":	zsSDKey = zsSDKey + zsUnitDomain

		self.RuffEcho("UnitNameEM-E [" + zsSDKey + "]", false, true)

#		see if we have already started this counter
		if (sdEntityExists(sdGroup, zsSDKey) == False):
			#Since no record create entries
			ziTT1 = self.getTotal1(zsName)
			ziTT2 = self.getTotal2(zsName)
			zDic = {'cnt':0, 'tt1':ziTT1, 'tt2':ziTT2}
			sdEntityInit(sdGroup, zsSDKey, zDic)

#		get the count values
		ziCnt = sdGetVal(sdGroup, zsSDKey, "cnt")
		ziTT1 = sdGetVal(sdGroup, zsSDKey, "tt1")
		ziTT2 = sdGetVal(sdGroup, zsSDKey, "tt2")

		self.RuffEcho("UnitNameEM-F [" + str(ziCnt) + "] [" + str(ziTT1) + "] [" + str(ziTT2) + "]", false, true)

#		increment count, adjust totals if required
		ziCnt = ziCnt + 1
		if (ziCnt > ziTT1
		and ziTT1 > 0):
			ziCnt = 1
			ziTT1 = self.getTotal1(zsName)
			ziTT2 = ziTT2 + 1

#		store the new values
		sdSetVal(sdGroup, zsSDKey, "cnt", ziCnt)
		sdSetVal(sdGroup, zsSDKey, "tt1", ziTT1)
		sdSetVal(sdGroup, zsSDKey, "tt2", ziTT2)

#		swap out the count code items for count value
		zsName = self.swapCountCode(zsName, "^cnt", ziCnt)
		zsName = self.swapCountCode(zsName, "^tt1", ziTT1)
		zsName = self.swapCountCode(zsName, "^tt2", ziTT2)

		return zsName


	def getUnitNameConvFromIniFile(self, Era, UnitClass, UnitCombat):
##    a. try to get the advanced naming convention
##    b. if it returns 'DEFAULT', then get the combat based naming convention
##    c. if naming convention is 'DEFAULT', get default naming convention

		self.RuffEcho("UnitNameEM-ini [" + Era[4:] + "_" + UnitClass[10:] + "]", false, true)

		zsUnitNameConv = BugUnitName.getAdvanced(Era[4:], UnitClass[10:])

		self.RuffEcho("UnitNameEM-iniA [" + zsUnitNameConv + "]" + UnitCombat[11:], false, true)

		if not (zsUnitNameConv == "DEFAULT"):
			return zsUnitNameConv

		zsUnitNameConv = BugUnitName.getCombat(UnitCombat[11:])

		self.RuffEcho("UnitNameEM-iniB [" + zsUnitNameConv + "]", false, true)

		if not (zsUnitNameConv == "DEFAULT"):
			return zsUnitNameConv

		self.RuffEcho("UnitNameEM-iniC [" + zsUnitNameConv + "]", false, true)

		zsUnitNameConv = BugUnitName.getDefault()
		return zsUnitNameConv


	def getUnitCombat(self, pUnit):

# Return immediately if the unit passed in is invalid
		if (pUnit == None
		or pUnit.isNone()):
			return "UNITCOMBAT_None"

		iUnitCombat = pUnit.getUnitCombatType()
		infoUnitCombat = gc.getUnitCombatInfo(iUnitCombat)

		if (infoUnitCombat == None):
			return "UNITCOMBAT_None"

		return infoUnitCombat.getType()


	def getCounter(self, conv):
##  - ^cnt[f]^ - count across all units (increments based on unit)
##  - ^cntu[f]^ - count across same unit (increments based on unit)
##  - ^cntct[f]^ - count across same city (increments based on unit)
##  - ^cntuct[f]^ - count across same unit / city (increments based on unit)
##  - ^cntc[f]^ - count across same combat type (increments based on combat type)
##  - ^cntd[f]^ - count across same domain (increments based on domain)

		if not (conv.find("^cnt[") == -1):
			return "ALL"

		if not (conv.find("^cntu[") == -1):
			return "UNIT"

		if not (conv.find("^cntc[") == -1):
			return "COMBAT"

		if not (conv.find("^cntct[") == -1):
			return "CITY"

		if not (conv.find("^cntuct[") == -1):
			return "UNITCITY"

		if not (conv.find("^cntd[") == -1):
			return "DOMAIN"

		return "ALL"


	def getTotal1(self, conv):
##  - ^tt1[f][x:y]^ - total where the total is a random number between x and y (number)

#		return 'not found' indicator
		ziStart = conv.find("^tt1[")
		if (ziStart == -1):
			return -1

#		locate and extract the 'low' value
		ziStart = conv.find("[",ziStart)
		ziStart = conv.find("[",ziStart + 1)
		ziEnd = conv.find(":",ziStart)
		ziLow = int(conv[ziStart + 1:ziEnd])
		if (ziLow < 1): ziLow = 1

#		locate and extract the 'high' value
		ziStart = ziEnd
		ziEnd = conv.find("]",ziStart)
		ziHigh = int(conv[ziStart + 1:ziEnd])
		if (ziHigh < 1): ziHigh = 1

#		check that the user isn't an idiot
		if (ziLow > ziHigh): return ziLow

#		return the value
		return random.randint(ziLow, ziHigh)


	def getTotal2(self, conv):
##  - ^tt2[f][x]^ - total count (starts at x, incremented by 1 each time ^tt is reset to 1)

#		return 'not found' indicator
		ziStart = conv.find("^tt2[")
		if (ziStart == -1):
			return -1

#		locate and extract the value
		ziStart = conv.find("[",ziStart)
		ziStart = conv.find("[",ziStart + 1)
		ziEnd = conv.find("]",ziStart)
		ziValue = int(conv[ziStart + 1:ziEnd])

		if (ziValue < 1): ziValue = 1
		return ziValue


	def getNumberFormat(self, conv, searchStr):
#		return 'not found' indicator
		ziStart = conv.find(searchStr)
		ziStart = conv.find("[",ziStart)
		if (ziStart == -1):
			return "s"   # s for silent, hides number
		else:
			return conv[ziStart + 1:ziStart + 2]


	def getCountCode(self, conv, searchStr):
#		return 'not found' indicator
		ziStart = conv.find(searchStr)
		if (ziStart == -1):
			return ""
		else:
			ziEnd = conv.find("^", ziStart + 1)
			return conv[ziStart:ziEnd + 1]


	def swapCountCode(self, conv, searchStr, iCnt):

#		return if iCnt is negative (this means that the code is not in the unitnameconv)
		if iCnt < 0: return conv

		self.RuffEcho("UnitNameEM-SCC [" + conv + "] [" + searchStr + "] [" + str(iCnt) + "]", false, true)

		zsCntCode = self.getCountCode(conv, searchStr)

		if zsCntCode == "": return conv

		self.RuffEcho("UnitNameEM-SCC [" + zsCntCode + "]", false, true)

		zsNumberFormat = self.getNumberFormat(conv, searchStr)

		self.RuffEcho("UnitNameEM-SCC [" + zsNumberFormat + "]", false, true)

		zsCnt = self.FormatNumber(zsNumberFormat, iCnt)

		self.RuffEcho("UnitNameEM-SCC [" + zsCnt + "]", false, true)

		if zsCntCode == "":
			return conv
		else:
			return conv.replace(zsCntCode, zsCnt)


	def FormatNumber(self, fmt, i):
		if (fmt == "s"):     # silent
			return ""
		elif (fmt == "a"):   # lower case alpha
			i = ((i + 1) % 26) - 1
			return chr(96+i)
		elif (fmt == "A"):   # upper case alpha
			i = ((i + 1) % 26) - 1
			return chr(64+i)
		elif (fmt == "p"):   # phonetic
			i = ((i + 1) % 26) - 1
			return phonetic_array[i]
		elif (fmt == "g"):   # greek
			i = ((i + 1) % 24) - 1
			return greek_array[i]
		elif (fmt == "n"):   # number    
			return str(i)
		elif (fmt == "o"):   # ordinal
			return self.getOrdinal(i)
		elif (fmt == "r"):   # roman
			return Roman.toRoman(i)
		else:
			return str(i)


	def getOrdinal(self, i):
		if i % 100 in (11, 12, 13): #special case
			return '%dth' % i
		return str(i) + ordinal_array[i % 10]


	def RuffEcho(self, echoString, printToScr, printToLog):
#		printToScr = true
#		printToLog = true

		szMessage = "%s" % (echoString)
		if (printToScr):
			CyInterface().addMessage(CyGame().getActivePlayer(), True, 10, szMessage, "", 2, None, ColorTypes(8), 0, 0, False, False)
		if (printToLog):
			CvUtil.pyPrint(szMessage)
		return 0

