## GPUtil
##
## Utilities for dealing with Great People.
##
## MODDERS
##
##   There are four places where you must add information about your new great people.
##   This is also necessary if you assign GP points to buildings that don't normally get them,
##   for example GG points to Heroic Epic.
##
##     1. Unit Type
##     2. Named constant
##     3. Color
##     4. Icon (font glyph or string)
##
## Notes
##   - Must be initialized externally by calling init()
##
## Copyright (c) 2007-2009 The BUG Mod.
##
## Author: EmperorFool

from CvPythonExtensions import *
import BugUtil

gc = CyGlobalContext()
localText = CyTranslator()

# Unit Type of each great person that can gain GP points

g_gpBarList = (
	"UNIT_GREAT_SPY",
	"UNIT_ENGINEER",
	"UNIT_MERCHANT",
	"UNIT_SCIENTIST",
	"UNIT_ARTIST",
	"UNIT_PROPHET",
# MOD: specify the unit type (XML key) for each new great person (1)
	#"UNIT_DOCTOR",
)

# Named constants for each great person and total number of GP types
# These must be in the exact same order as the list above

NUM_GP = len(g_gpBarList)
(
	GP_SPY,
	GP_ENGINEER,
	GP_MERCHANT,
	GP_SCIENTIST,
	GP_ARTIST,
	GP_PROPHET,
# MOD: define a constant for each new great person in same order as above (2)
	#GP_DOCTOR,
) = range(NUM_GP)

# Maps GP type to unit ID and color to show in GP Bar

g_gpUnitTypes = None
g_gpColors = None
g_unitIcons = None

def init():
	global g_gpUnitTypes
	g_gpUnitTypes = [None] * NUM_GP
	for i, s in enumerate(g_gpBarList):
		g_gpUnitTypes[i] = gc.getInfoTypeForString(s)
	
	global g_gpColors
	g_gpColors = [None] * NUM_GP
	g_gpColors[GP_SPY] = gc.getInfoTypeForString("COLOR_WHITE")
	g_gpColors[GP_ENGINEER] = gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getColorType()
	g_gpColors[GP_MERCHANT] = gc.getInfoTypeForString("COLOR_YELLOW")
	g_gpColors[GP_SCIENTIST] = gc.getInfoTypeForString("COLOR_RESEARCH_STORED")
	g_gpColors[GP_ARTIST] = gc.getInfoTypeForString("COLOR_CULTURE_STORED")
	g_gpColors[GP_PROPHET] = gc.getInfoTypeForString("COLOR_BLUE")
	# MOD: specify color for each new great person (3)
	#g_gpColors[GP_DOCTOR] = gc.getInfoTypeForString("COLOR_WHITE")
	
	global g_unitIcons
	g_unitIcons = {}
	g_unitIcons[g_gpUnitTypes[GP_SPY]] = u"%c" %(gc.getCommerceInfo(CommerceTypes.COMMERCE_ESPIONAGE).getChar())
	g_unitIcons[g_gpUnitTypes[GP_ENGINEER]] = u"%c" %(gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getChar())
	g_unitIcons[g_gpUnitTypes[GP_MERCHANT]] = u"%c" %(gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getChar())
	g_unitIcons[g_gpUnitTypes[GP_SCIENTIST]] = u"%c" %(gc.getCommerceInfo(CommerceTypes.COMMERCE_RESEARCH).getChar())
	g_unitIcons[g_gpUnitTypes[GP_ARTIST]] = u"%c" %(gc.getCommerceInfo(CommerceTypes.COMMERCE_CULTURE).getChar())
	g_unitIcons[g_gpUnitTypes[GP_PROPHET]] = u"%c" % CyGame().getSymbolID(FontSymbols.RELIGION_CHAR)
	# MOD: specify icon (font glyph) for each new great person (4)
	#g_unitIcons[g_gpUnitTypes[GP_DOCTOR]] = u"%c" % CyGame().getSymbolID(FontSymbols.HEALTHY_CHAR)

def getUnitType(gpType):
	return g_gpUnitTypes[gpType]

def getColor(gpType):
	return g_gpColors[gpType]

def getUnitIcon(iUnit):
	try:
		return g_unitIcons[iUnit]
	except:
		BugUtil.warn("no GP icon for unit %d", iUnit)
		return u"%c" % CyGame().getSymbolID(FontSymbols.GREAT_PEOPLE_CHAR)

def findNextCity():
	iMinTurns = None
	iTurns = 0
	pPlayer = gc.getPlayer(gc.getGame().getActivePlayer())
	iThreshold = pPlayer.greatPeopleThreshold(False)
	pBestCity = None
	
	for iCity in range(pPlayer.getNumCities()):
		pCity = pPlayer.getCity(iCity)
		if (pCity):
			iRate = pCity.getGreatPeopleRate()
			if (iRate > 0):
				iProgress = pCity.getGreatPeopleProgress()
				iTurns = (iThreshold - iProgress + iRate - 1) / iRate
				if (iMinTurns is None or iTurns < iMinTurns):
					iMinTurns = iTurns
					pBestCity = pCity
	return (pBestCity, iMinTurns)

def findMaxCity():
	iMaxProgress = 0
	pPlayer = gc.getPlayer(gc.getGame().getActivePlayer())
	pBestCity = None
	
	for iCity in range(pPlayer.getNumCities()):
		pCity = pPlayer.getCity(iCity)
		if (pCity):
			iProgress = pCity.getGreatPeopleProgress()
			if (iProgress > iMaxProgress):
				iMaxProgress = iProgress
				pBestCity = pCity
	return (pBestCity, iMaxProgress)

def getCityTurns(pCity):
	if (pCity):
		pPlayer = gc.getPlayer(pCity.getOwner())
		iThreshold = pPlayer.greatPeopleThreshold(False)
		iRate = pCity.getGreatPeopleRate()
		if (iRate > 0):
			iProgress = pCity.getGreatPeopleProgress()
			iTurns = (iThreshold - iProgress + iRate - 1) / iRate
			return iTurns
	return None

def calcPercentages(pCity):
	# Calc total rate
	iTotal = 0
	for iUnit in g_gpUnitTypes:
		iTotal += pCity.getGreatPeopleUnitProgress(iUnit)
	
	# Calc individual percentages based on rates and total
	percents = []
	if (iTotal > 0):
		iLeftover = 100
		for iUnit in range(gc.getNumUnitInfos()):
#			iUnit = getUnitType(gpType)
			iProgress = pCity.getGreatPeopleUnitProgress(iUnit)
			if (iProgress > 0):
				iPercent = 100 * iProgress / iTotal
				iLeftover -= iPercent
				percents.append((iPercent, iUnit))
		# Add remaining from 100 to first in list to match Civ4
		if (iLeftover > 0):
			percents[0] = (percents[0][0] + iLeftover, percents[0][1])
	return percents

def createHoverText(pCity, iTurns):
	if (not pCity):
		return None
	iProgress = pCity.getGreatPeopleProgress()
	iThreshold = gc.getPlayer(pCity.getOwner()).greatPeopleThreshold(False)
	szText = localText.getText("TXT_KEY_MISC_GREAT_PERSON", (iProgress, iThreshold))
	iRate = pCity.getGreatPeopleRate()
	szText += u"\n"
	szText += localText.getText("INTERFACE_CITY_TURNS", (iTurns,))
	
	percents = calcPercentages(pCity)
	if (len(percents) > 0):
		percents.sort()
		percents.reverse()
		for iPercent, iUnit in percents:
#			iUnit = getUnitType(gpType)
			szText += u"\n%s - %d%%" % (gc.getUnitInfo(iUnit).getDescription(), iPercent)
	return szText

def getGreatPeopleText(pCity, iGPTurns, iGPBarWidth, bGPBarTypesNone, bGPBarTypesOne, bIncludeCityName):
	sGreatPeopleChar = u"%c" % CyGame().getSymbolID(FontSymbols.GREAT_PEOPLE_CHAR)
	if (not pCity):
		szText = localText.getText("INTERFACE_GREAT_PERSON_NONE", (sGreatPeopleChar, ))
	elif (bGPBarTypesNone):
		if (iGPTurns):
			if (bIncludeCityName):
				szText = localText.getText("INTERFACE_GREAT_PERSON_CITY_TURNS", (sGreatPeopleChar, pCity.getName(), iGPTurns))
			else:
				szText = localText.getText("INTERFACE_GREAT_PERSON_TURNS", (sGreatPeopleChar, iGPTurns))
		else:
			if (bIncludeCityName):
				szText = localText.getText("INTERFACE_GREAT_PERSON_CITY", (sGreatPeopleChar, pCity.getName()))
			else:
				szText = sGreatPeopleChar
	else:
		lPercents = calcPercentages(pCity)
		if (len(lPercents) == 0):
			if (iGPTurns):
				if (bIncludeCityName):
					szText = localText.getText("INTERFACE_GREAT_PERSON_CITY_TURNS", (sGreatPeopleChar, pCity.getName(), iGPTurns))
				else:
					szText = localText.getText("INTERFACE_GREAT_PERSON_TURNS", (sGreatPeopleChar, iGPTurns))
			else:
				if (bIncludeCityName):
					szText = localText.getText("INTERFACE_GREAT_PERSON_CITY", (sGreatPeopleChar, pCity.getName()))
				else:
					szText = sGreatPeopleChar
		else:
			lPercents.sort()
			lPercents.reverse()
			if (bGPBarTypesOne or len(lPercents) == 1):
				iPercent, iUnit = lPercents[0]
				pInfo = gc.getUnitInfo(iUnit)
				if (iGPTurns):
					if (bIncludeCityName):
						szText = localText.getText("INTERFACE_GREAT_PERSON_CITY_TURNS", (pInfo.getDescription(), pCity.getName(), iGPTurns))
					else:
						szText = localText.getText("INTERFACE_GREAT_PERSON_TURNS", (pInfo.getDescription(), iGPTurns))
				else:
					if (bIncludeCityName):
						szText = localText.getText("INTERFACE_GREAT_PERSON_CITY", (pInfo.getDescription(), pCity.getName()))
					else:
						szText = unicode(pInfo.getDescription())
			else:
				if (iGPTurns):
					if (bIncludeCityName):
						szText = localText.getText("INTERFACE_GREAT_PERSON_CITY_TURNS", (sGreatPeopleChar, pCity.getName(), iGPTurns))
					else:
						szText = localText.getText("INTERFACE_GREAT_PERSON_TURNS", (sGreatPeopleChar, iGPTurns))
				else:
					if (bIncludeCityName):
						szText = localText.getText("INTERFACE_GREAT_PERSON_CITY", (sGreatPeopleChar, pCity.getName()))
					else:
						szText = sGreatPeopleChar + u":"
				szTypes = ""
				for iPercent, iUnit in lPercents:
					szNewTypes = szTypes + u" %c%d%%" % (getUnitIcon(iUnit), iPercent)
					szNewText = szText + u"<font=2> -%s</font>" % szTypes
					if (CyInterface().determineWidth(szNewText) > iGPBarWidth - 10):
						# Keep under width
						break
					szTypes = szNewTypes
				if (len(szTypes) > 0):
					szText += u"<font=2> -%s</font>" % szTypes
	return szText
