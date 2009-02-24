## MapGenerator
##
## Key to regenerate the map and (hopefully soon) HOF's MapFinder utility.
##
## Adapted from HOF Mod 3.13.001.
##
## Copyright (c) 2009 The BUG Mod.
##
## Author: HOF Team, EmperorFool

from CvPythonExtensions import *
import BugDll
import BugUtil
import CvCameraControls
import CvUtil
import os.path
import time

gc = CyGlobalContext()
cam = CvCameraControls.CvCameraControls()

EVENT_MESSAGE_TIME = gc.getDefineINT("EVENT_MESSAGE_TIME_LONG")

# Regenerate Map

def canRegenerate():
	if BugDll.isPresent():
		return gc.getGame().canRegenerateMap()
	return False

def regenerate(argsList):
	if BugDll.isPresent():
		if canRegenerate():
			if CyGame().regenerateMap():
				cam.setCameraMovementSpeed(CameraMovementSpeeds.CAMERAMOVEMENTSPEED_FAST)
				centerCameraOnPlayer()
				cam.setCameraMovementSpeed(CameraMovementSpeeds.CAMERAMOVEMENTSPEED_NORMAL)
			else:
				CyInterface().addMessage(gc.getGame().getActivePlayer(), True,
										 EVENT_MESSAGE_TIME, "Regenerate Failed", #BugUtil.getPlainText(""),
										 None, 0, None, gc.getInfoTypeForString("COLOR_NEGATIVE_TEXT"), -1, -1, False, False)
		else:
			CyInterface().addMessage(gc.getGame().getActivePlayer(), True,
									 EVENT_MESSAGE_TIME, "Can't Regenerate", #BugUtil.getPlainText(""),
									 None, 0, None, gc.getInfoTypeForString("COLOR_WARNING_TEXT"), -1, -1, False, False)

def centerCameraOnPlayer():
	cam.centerCamera(gc.getActivePlayer().getStartingPlot())
	#CyCamera().JustLookAtPlot(gc.getActivePlayer().getStartingPlot())


# Regeneration Loop

(
	NO_FEATURE,
	FEATURE_ICE,
	FEATURE_JUNGLE,
	FEATURE_OASIS,
	FEATURE_FLOOD_PLAINS,
	FEATURE_FOREST,
	FEATURE_FALLOUT,
) = range(-1, 6)
FEATURE_LAKE = 99

(
	NO_TERRAIN,
	TERRAIN_GRASS,
	TERRAIN_PLAINS,
	TERRAIN_DESERT,
	TERRAIN_TUNDRA,
	TERRAIN_SNOW,
	TERRAIN_COAST,
	TERRAIN_OCEAN,
	TERRAIN_PEAK,
	TERRAIN_HILL,
) = range(-1, 9)

CODES_BY_TYPES = {  # BasicPlot_CodeToTypes
	('water', TERRAIN_OCEAN, NO_FEATURE) : 401,
	('water', TERRAIN_COAST, FEATURE_ICE) : 402,
	('land', TERRAIN_DESERT, NO_FEATURE) : 403,
	('hills', TERRAIN_DESERT, NO_FEATURE) : 404,
	('land', TERRAIN_DESERT, FEATURE_FLOOD_PLAINS) : 405,
	('land', TERRAIN_GRASS, NO_FEATURE) : 406,
	('land', TERRAIN_GRASS, FEATURE_FOREST) : 407,
	('hills', TERRAIN_GRASS, NO_FEATURE) : 408,
	('hills', TERRAIN_GRASS, FEATURE_FOREST) : 409,
	('hills', TERRAIN_GRASS, FEATURE_JUNGLE) : 410,
	('land', TERRAIN_GRASS, FEATURE_JUNGLE) : 411,
	('land', TERRAIN_DESERT, FEATURE_OASIS) : 412,
	('water', TERRAIN_OCEAN, FEATURE_ICE) : 413,
	('peak', TERRAIN_PEAK, NO_FEATURE) : 414,
	('land', TERRAIN_PLAINS, NO_FEATURE) : 415,
	('land', TERRAIN_PLAINS, FEATURE_FOREST) : 416,
	('hills', TERRAIN_PLAINS, NO_FEATURE) : 417,
	('hills', TERRAIN_PLAINS, FEATURE_FOREST) : 418,
	('water', TERRAIN_COAST, NO_FEATURE) : 419,
	('land', TERRAIN_SNOW, NO_FEATURE) : 420,
	('land', TERRAIN_SNOW, FEATURE_FOREST) : 421,
	('hills', TERRAIN_SNOW, NO_FEATURE) : 422,
	('hills', TERRAIN_SNOW, FEATURE_FOREST) : 423,
	('land', TERRAIN_TUNDRA, NO_FEATURE) : 424,
	('land', TERRAIN_TUNDRA, FEATURE_FOREST) : 425,
	('hills', TERRAIN_TUNDRA, NO_FEATURE) : 426,
	('hills', TERRAIN_TUNDRA, FEATURE_FOREST) : 427,
	('water', TERRAIN_COAST, FEATURE_LAKE) : 428,
}

# unused
TYPES_BY_CODE = {  # BasicPlot_TypesToCode
	401 : ('water', TERRAIN_OCEAN, NO_FEATURE),
	402 : ('water', TERRAIN_COAST, FEATURE_ICE),
	403 : ('land', TERRAIN_DESERT, NO_FEATURE),
	404 : ('hills', TERRAIN_DESERT, NO_FEATURE),
	405 : ('land', TERRAIN_DESERT, FEATURE_FLOOD_PLAINS),
	406 : ('land', TERRAIN_GRASS, NO_FEATURE),
	407 : ('land', TERRAIN_GRASS, FEATURE_FOREST),
	408 : ('hills', TERRAIN_GRASS, NO_FEATURE),
	409 : ('hills', TERRAIN_GRASS, FEATURE_FOREST),
	410 : ('hills', TERRAIN_GRASS, FEATURE_JUNGLE),
	411 : ('land', TERRAIN_GRASS, FEATURE_JUNGLE),
	412 : ('land', TERRAIN_DESERT, FEATURE_OASIS),
	413 : ('water', TERRAIN_OCEAN, FEATURE_ICE),
	414 : ('peak', TERRAIN_PEAK, NO_FEATURE),
	415 : ('land', TERRAIN_PLAINS, NO_FEATURE),
	416 : ('land', TERRAIN_PLAINS, FEATURE_FOREST),
	417 : ('hills', TERRAIN_PLAINS, NO_FEATURE),
	418 : ('hills', TERRAIN_PLAINS, FEATURE_FOREST),
	419 : ('water', TERRAIN_COAST, NO_FEATURE),
	420 : ('land', TERRAIN_SNOW, NO_FEATURE),
	421 : ('land', TERRAIN_SNOW, FEATURE_FOREST),
	422 : ('hills', TERRAIN_SNOW, NO_FEATURE),
	423 : ('hills', TERRAIN_SNOW, FEATURE_FOREST),
	424 : ('land', TERRAIN_TUNDRA, NO_FEATURE),
	425 : ('land', TERRAIN_TUNDRA, FEATURE_FOREST),
	426 : ('hills', TERRAIN_TUNDRA, NO_FEATURE),
	427 : ('hills', TERRAIN_TUNDRA, FEATURE_FOREST),
	428 : ('water', TERRAIN_COAST, FEATURE_LAKE),
}

def getSaveFileName(pathName):
	iActivePlayer = gc.getGame().getActivePlayer()
	activePlayer = gc.getPlayer(iActivePlayer)
	
	objLeaderHead = gc.getLeaderHeadInfo (activePlayer.getLeaderType()).getText()
	
	difficulty = gc.getHandicapInfo(activePlayer.getHandicapType()).getText()
	mapType = gc.getMap().getMapScriptName()
	mapSize = gc.getWorldInfo(gc.getMap().getWorldSize()).getText()
	mapClimate = gc.getClimateInfo(gc.getMap().getClimate()).getText()
	mapLevel = gc.getSeaLevelInfo(gc.getMap().getSeaLevel()).getText()
	era = gc.getEraInfo(gc.getGame().getStartEra()).getText()
	speed = gc.getGameSpeedInfo(gc.getGame().getGameSpeedType()).getText()
	turnYear = CyGameTextMgr().getTimeStr(gc.getGame().getGameTurn(), false)
	
	fileName = objLeaderHead[0:3]
	fileName = fileName + '_' + difficulty[0:3]
	fileName = fileName + '_' + mapSize[0:3]
	fileName = fileName + '_' + mapType[0:3]
	fileName = fileName + '_' + speed[0:3]
	fileName = fileName + '_' + era[0:3]
	fileName = fileName + '_' + turnYear.replace(" ", "-")
	fileName = fileName + '_' + mapClimate[0:3]
	fileName = fileName + '_' + mapLevel[0:3]

	fileName = os.path.join(pathName, fileName)
	baseFileName = CvUtil.convertToStr(fileName)
	fileName = CvUtil.convertToStr(fileName + '_' + time.strftime("%b-%d-%Y_%H-%M-%S"))
	return (fileName, baseFileName)

def MapFinderRegenerator():
	global bSuccess
	i = 0
	while True:
		bSuccess = CyGame().regenerateMap()
		yield i
		i = i + 1

def startStop(argsList=None):
	if not bActive:
		start()
	else:
		stop()
	return 1

def start():
	global bActive, bChecking, iRegenCount, iSavedCount
	cam.setCameraMovementSpeed(CameraMovementSpeeds.CAMERAMOVEMENTSPEED_FAST)
	bActive = True
	bChecking = False
	iRegenCount = 0
	iSavedCount = 0

def stop():
	global bActive, bChecking
	bActive = False
	bChecking = False
	cam.setCameraMovementSpeed(CameraMovementSpeeds.CAMERAMOVEMENTSPEED_NORMAL)

def cycle(argsList=None):
	global iUpdateCounter
	if (bActive and bChecking):
		iUpdateCounter = iUpdateCounter + 1
#		BugUtil.alert("check counter = %d", iUpdateCounter)
		if (iUpdateCounter >= 1): centerCameraOnPlayer()
		if (iUpdateCounter >= iUpdateDelay):
			iUpdateCounter = 0
			check(iRegenCount)
	
	if (bActive and not bChecking):
		iUpdateCounter = iUpdateCounter + 1
#		BugUtil.alert("next counter = %d", iUpdateCounter)
		if (iUpdateCounter >= 4): # iUpdateDelay):
			iUpdateCounter = 0
			next()

def next():
	global bActive, bSuccess, bChecking, iRegenCount
	if not bActive: return

	if CyGame().canRegenerateMap():
		try: x = mfRegen.next()
		except:	return

		if not bSuccess:
			CyInterface().addMessage(gc.getGame().getActivePlayer(), True,
				EVENT_MESSAGE_TIME, BugUtil.getPlainText('TXT_KEY_MAPFINDER_REGEN_FAILED') +
				"\n" + BugUtil.getPlainText('TXT_KEY_MAPFINDER_COUNT') +
				"=" + str(HOFContext.iMapFinderRegenCount) +
				" " + BugUtil.getPlainText('TXT_KEY_MAPFINDER_SAVED') +
				"=" + str(HOFContext.iMapFinderSavedCount), None,
				0, None, ColorTypes(-1), 0, 0, False, False)
			stop()
			return
	else:
		CyInterface().addMessage(gc.getGame().getActivePlayer(), True,
			EVENT_MESSAGE_TIME, BugUtil.getPlainText('TXT_KEY_MAPFINDER_CANNOT_REGEN') +
			"\n" + BugUtil.getPlainText('TXT_KEY_MAPFINDER_COUNT') +
			"=" + str(HOFContext.iMapFinderRegenCount) +
			" " + BugUtil.getPlainText('TXT_KEY_MAPFINDER_SAVED') +
			"=" + str(HOFContext.iMapFinderSavedCount), None,
			0, None, ColorTypes(-1), 0, 0, False, False)
		stop()
		return

	bChecking = True
	iRegenCount = iRegenCount + 1

def check(fNum):
	global bActive, bChecking, iSavedCount
	bSaveMap = False
	sMFSavePath = "C:/Games/Civ4_Map_Finder/Saves" # hof.get_str('HOFUtil', 'MapFinderSavePath', 'Default')
	if sMFSavePath == 'Default': pass # sMFSavePath = HOFContext.MapFinderDftSavePath
	(fileName, baseFileName) = getSaveFileName(sMFSavePath)
	
	mr = {}
	for x in CodeText.iterkeys():
		mr[x] = 0

	iActivePlayer = gc.getGame().getActivePlayer()
	activePlayer = gc.getPlayer(iActivePlayer)
	iTeam = activePlayer.getTeam()

	startplot = activePlayer.getStartingPlot()
	iStartX = startplot.getX()
	iStartY = startplot.getY()
	iMaxX = gc.getMap().getGridWidth()
	iMaxY = gc.getMap().getGridHeight()
	bWrapX = gc.getMap().isWrapX()
	bWrapY = gc.getMap().isWrapY()

	lX = {}
	lY = {}
	if (rs['Range'] != 999):

		lMax = (rs['Range'] * 2) + 1
		iX = iStartX - rs['Range']
		if (iX < 0):
			if (bWrapX):
				iX = iMaxX + iX
			else:
				iX = 0
		for i in range(1, lMax + 1):
			lX[i] = iX
			iX = iX + 1
			if iX > iMaxX: 0
			if iX < 0: iMaxX

		iY = iStartY - rs['Range']
		if (iY < 0):
			if (bWrapY):
				iY = iMaxY + iY
			else:
				iY = 0
		for i in range(1, lMax + 1):
			lY[i] = iY
## HOF MOD V1.61.005
##			iy = iX + 1
			iY = iY + 1
## end HOF MOD V1.61.005
			if iY > iMaxY: 0
			if iY < 0: iMaxY
			
##	displayMsg(str(lX.values()) + "\n" + str(lY.values()))

	for iY in range(0, iMaxY):
		for iX in range(0, iMaxX):

			if (rs['Range'] != 999):
## HOF MOD V1.61.005
				# skip if outside range
				if iX not in lX.values(): continue
				if iY not in lY.values(): continue
			    # use fat-cross if over 1 range
				if  (rs['Range'] > 1):
					# fat cross, skip diagonal corners
					if (iX == lX[1] and iY == lY[1]): continue
					if (iX == lX[1] and iY == lY[lMax]): continue
					if (iX == lX[lMax] and iY == lY[1]): continue
					if (iX == lX[lMax] and iY == lY[lMax]): continue
## end HOF MOD V1.61.005
##			displayMsg(str(iX) + "/" + str(iY))
			
			plot = gc.getMap().plot(iX, iY)
			if (plot.isRevealed(iTeam, False)):
				
				if (plot.isFlatlands()): p = 'land'
				elif (plot.isWater()): p = 'water'
				elif (plot.isHills()): p = 'hills'
				elif (plot.isPeak()): p = 'peak'
				t = plot.getTerrainType()
				if (plot.isLake()):
					f = FEATURE_LAKE
				else:
					f = plot.getFeatureType()
				ip = -1
				if CODES_BY_TYPES.has_key((p, t, f)):
					ip = CODES_BY_TYPES[(p, t, f)]
					mr[ip] = mr[ip] + 1
					for k, l in Category_Types.iteritems():
					    if (ip in l): mr[k] = mr[k] + 1

				ib = plot.getBonusType(iTeam) + 500
				if mr.has_key(ib):
					mr[ib] = mr[ib] + 1
					for k, l in Category_Types.iteritems():
					    if (ib in l): mr[k] = mr[k] + 1

				# Base Commerce
				xc = plot.calculateYield(YieldTypes.YIELD_COMMERCE, True)
				mr[301] = mr[301] + xc
				# Base Food
				xf = plot.calculateYield(YieldTypes.YIELD_FOOD, True)
				mr[302] = mr[302] + xf
				# Extra Base Food
				if (xf > 2): mr[310] = mr[310] + (xf - 2)
				# Base Production
				xp = plot.calculateYield(YieldTypes.YIELD_PRODUCTION, True)
				mr[303] = mr[303] + xp
				
				if (plot.isGoody()): mr[601] = mr[601] + 1
				
## HOF MOD V1.61.005
				if Combo_Types.has_key((ib, ip)):
				    ic = Combo_Types[(ib, ip)]
				    if mr.has_key(ic):
				    	mr[ic] = mr[ic] + 1
				    	
				# Starting Plot?
				if iX == iStartX and iY == iStartY:
					if Combo_Types.has_key((999, ip)):
					    ic = Combo_Types[(999, ip)]
					    if mr.has_key(ic):
					    	mr[ic] = mr[ic] + 1

				if (plot.isRiver()):
					mr[602] = mr[602] + 1
					ipr = ip + 50
					if mr.has_key(ipr):
						mr[ipr] = mr[ipr] + 1
					if Combo_Types.has_key((ib, ipr)):
					    ic = Combo_Types[(ib, ipr)]
					    if mr.has_key(ic):
					    	mr[ic] = mr[ic] + 1
                    # Starting Plot?
					if iX == iStartX and iY == iStartY:
						if Combo_Types.has_key((999, ipr)):
						    ic = Combo_Types[(999, ipr)]
						    if mr.has_key(ic):
						    	mr[ic] = mr[ic] + 1

				if (plot.isFreshWater()):
					mr[603] = mr[603] + 1
					ipf = ip + 150
					if mr.has_key(ipf):
						mr[ipf] = mr[ipf] + 1
					if Combo_Types.has_key((ib, ipf)):
					    ic = Combo_Types[(ib, ipf)]
					    if mr.has_key(ic):
					    	mr[ic] = mr[ic] + 1
                    # Starting Plot?
					if iX == iStartX and iY == iStartY:
						if Combo_Types.has_key((999, ipf)):
						    ic = Combo_Types[(999, ipf)]
						    if mr.has_key(ic):
						    	mr[ic] = mr[ic] + 1
## end HOF MOD V1.61.005

	lPF = []
	for g, r in rs.iteritems():
		if (g == 'Range'): continue
		grp = True
		for k, v in r.iteritems():
			if (mr.has_key(k)):
				if ((v[1] == 0 and mr[k] != 0) or (mr[k] < v[0]) or (mr[k] > v[1])):
					grp = False
					break
			else:
				grp = False
				break

		lPF.append(grp)

	for i in range(len(lPF)):
	    if (lPF[i]):
	    	bSaveMap = True
	    	break
	    
	if (bSaveMap):
		iSavedCount = iSavedCount + 1
		reportFile = str(fileName + "_" + str(fNum) + "_" + str(iSavedCount) + ".txt")
		sPath, sName = os.path.split(sMFRuleFile)

		fp = open(reportFile, "a")

## HOF MOD V1.61.005
		# don't change unless file format changes!
		fp.write("HOF MOD V1.61.004,HOF MOD V1.61.005,\n")
## end HOF MOD V1.61.005

		fp.write("Name,Name," + str(fileName) + "_" + str(fNum) + "_" + str(iSavedCount) + "\n")
		fp.write("Rule File,Rule File," + str(sName) + "\n")
		fp.write("Range,Range," + str(rs['Range']) + "\n")

		lKeys = mr.keys()
		lKeys.sort()
		for x in lKeys:
			if (x < 900):
				fp.write(str(x) + "," + str(CodeText[x]) + "," + str(mr[x]) + "\n")

		fp.close

		fileNameX = str(fileName + "_" + str(fNum) + "_" + str(iSavedCount) + ".CivBeyondSwordSave")
		CyGame().saveGame(fileNameX)


#	CyInterface().addImmediateMessage(BugUtil.getPlainText('TXT_KEY_MAPFINDER_ALTX_TO_STOP') +
#					"\n" + BugUtil.getPlainText('TXT_KEY_MAPFINDER_COUNT') +
#					"=" + str(iRegenCount) +
#					" " + BugUtil.getPlainText('TXT_KEY_MAPFINDER_SAVED') +
#					"=" + str(iSavedCount), "")
	CyInterface().addImmediateMessage("MapFinder running . . ." +
					"\n" + "Count" +
					"=" + str(iRegenCount) +
					" " + "Saved" +
					"=" + str(iSavedCount), "")

	if (bSaveMap):
		fileNameX = str(fileName + "_" + str(fNum) + "_" + str(iSavedCount) + ".jpg")
		CyGame().takeJPEGScreenShot(fileNameX)

	if ((iRegenCount >= iRegenLimit) or
	    (iSavedCount >= iSavedLimit)):
		BugUtil.alert(BugUtil.getPlainText('TXT_KEY_MAPFINDER_STOPPED') +
					"\n" + BugUtil.getPlainText('TXT_KEY_MAPFINDER_COUNT') +
					"=" + str(iRegenCount) +
					" " + BugUtil.getPlainText('TXT_KEY_MAPFINDER_SAVED') +
					"=" + str(iSavedCount))
		stop()

	bChecking = False

def getRuleSet():
	global sMFRuleFile
	ruleset = {}
	ruleset['Range'] = 2
	
	sMFRuleFile = "C:/Games/Civ4_Map_Finder/Rules/Default.rul"  # hof.get_str('HOFUtil', 'MapFinderRuleFile', 'Default')
	if sMFRuleFile == 'Default':  sMFRuleFile = HOFContext.MapFinderDftRuleFile
	if not os.path.isfile(sMFRuleFile):	return ruleset

	iGrpSave = 0
	ruleset = {}
	fp = open(sMFRuleFile, "r")
	temp = fp.readline()
	while (temp != ''):
		(sGrp, sCat, sRule, sMin, sMax) = temp.split(",")
		iGrp = int(sGrp.strip())
		iCat = int(sCat.strip())
		if (iGrp == 0):
			ruleset['Range'] = iCat
		else:
			iRule = int(sRule.strip())
			iMin = int(sMin.strip())
			iMax = int(sMax.strip())
			if (iGrp != iGrpSave):
				ruleset[iGrp] = {iRule : (iMin, iMax)}
			else:
				ruleset[iGrp][iRule] = (iMin, iMax)
		iGrpSave = iGrp
		temp = fp.readline()
	fp.close
	fp = None

	return ruleset

def getCodeText():
	lLang = []
	CodeTextDict = {}
	
	iLang = CyGame().getCurrentLanguage()
	sMFPath = "C:/Games/Civ4_Map_Finder"  # hof.get_str('HOFUtil', 'MapFinderPath', 'Default')
	if sMFPath == 'Default': sMFPath = HOFContext.MapFinderDftPath
	CodeTextFile = os.path.join(sMFPath, 'MF_Text.dat')
	if not os.path.isfile(CodeTextFile): 
##		displayMsg(BugUtil.getPlainText('TXT_KEY_MAPFINDER_INVALID_PATH') +
##			"\n" + BugUtil.getPlainText('TXT_KEY_MAPFINDER_ABORTING'))
##		bActive = False
##		bChecking = False
		return

	fp = open(CodeTextFile, "r")
	temp = fp.readline()
	while (temp != ''):
		(sCat, sCode, sLang0,sLang1,sLang2,sLang3,sLang4) = temp.split(",")
		iCat = int(sCat.strip())
		iCode = int(sCode.strip())
		lLang = [sLang0.strip(), sLang1.strip(), sLang2.strip(),
					sLang3.strip(), sLang4.strip()]
		CodeTextDict[iCode] = lLang[iLang]
		temp = fp.readline()
	fp.close
	fp = None

	return CodeTextDict

def getCategory_Types():
	Category_TypesDict = {}
	
	sMFPath = "C:/Games/Civ4_Map_Finder"  # hof.get_str('HOFUtil', 'MapFinderPath', 'Default')
	if sMFPath == 'Default': sMFPath = HOFContext.MapFinderDftPath
	CatTypesFile  = os.path.join(sMFPath, 'MF_Cat_Rules.dat')
	if not os.path.isfile(CatTypesFile):
##		displayMsg(BugUtil.getPlainText('TXT_KEY_MAPFINDER_INVALID_PATH') +
##			"\n" + BugUtil.getPlainText('TXT_KEY_MAPFINDER_ABORTING'))
##		bActive = False
##		bChecking = False
		return

	fp = open(CatTypesFile, "r")
	temp = fp.readline()
	iCatSave = -1
	while (temp != ''):
		(sCat, sRule) = temp.split(",")
		iCat = int(sCat.strip())
		iRule = int(sRule.strip())
		if (iCat != iCatSave):
			Category_TypesDict[iCat] = (iRule,)
		else:
		    Category_TypesDict[iCat] = Category_TypesDict[iCat] + (iRule,)

		iCatSave = iCat
		temp = fp.readline()
	fp.close
	fp = None

	return Category_TypesDict

def getCombo_Types():
	Combo_TypesDict = {}

	sMFPath = "C:/Games/Civ4_Map_Finder"  # hof.get_str('HOFUtil', 'MapFinderPath', 'Default')
	if sMFPath == 'Default': sMFPath = HOFContext.MapFinderDftPath
	ComboTypesFile  = os.path.join(sMFPath, 'MF_Combo_Rules.dat')
	if not os.path.isfile(ComboTypesFile):
		return

	fp = open(ComboTypesFile, "r")
	temp = fp.readline()
	while (temp != ''):
		(sCat, sBonus, sTerrain) = temp.split(",")
		iCat = int(sCat.strip())
		iBonus = int(sBonus.strip())
		iTerrain = int(sTerrain.strip())
		Combo_TypesDict[(iBonus, iTerrain)] = iCat
		temp = fp.readline()
	fp.close
	fp = None

	return Combo_TypesDict

mfRegen = MapFinderRegenerator()

CodeText = getCodeText()
Category_Types = getCategory_Types()
Combo_Types = getCombo_Types()
rs =  getRuleSet()

iRegenCount = 0
iRegenLimit = 10
iSavedCount = 0
iSavedLimit = 5

iUpdateCounter = 0
iUpdateDelay = 20

bActive = False
bChecking = False
bSuccess = False
