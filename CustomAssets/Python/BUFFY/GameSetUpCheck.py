## GameSetUpChecks
##
## Checks the current map against the GameSetUpChecks.txt configuration file.

from CvPythonExtensions import *

import os
import os.path
import AutoSave
import BugCore
import BugPath
import BugUtil
import MapFinder

WRAP_FLAT = "Flat"
WRAP_TOROIDAL = "Toroidal"
WRAP_CYLINDRICAL = "Cylindrical"

gc = CyGlobalContext()
options = BugCore.game.BUFFY
AutoSaveOpt = BugCore.game.AutoSave

minHOFOpponents = []
maxHOFOpponents = []
# -1 = must not be checked
#  0 = any
#  1 = must be checked
hofGameOptionRequirements = []

crcResult = 0
modCRC = ""
dllCRC = ""
shaderCRC = ""
pythonCRC = ""
xmlCRC = ""

balancedOptionIndex = {}

## Note if map not found here then no check will be made.
## EF: these are read from the file but never used
worldWrapOptionIndex = {}
allowedWorldWrapValue = {}

hofAllowedMapScripts = {}
hofAllowedCylindrical = {}
hofAllowedToroidal = {}

def init():
	"""
	Initializes this module if BUFFY is enabled.
	"""
	if options.isEnabled():
		if processSetupFile():
			overrideSaveGameStart()
	else:
		BugUtil.debug("GameSetUpCheck - module disabled")

def processSetupFile():
	"""
	Reads and processes the GameSetUpCheck.txt file.
	"""
	filename = BugPath.findDataFile("GameSetUpCheck.txt", "GameSetUpCheck")
	if not filename:
		BugUtil.error("Cannot find GameSetUpCheck.txt")
	else:
		try:
			BugUtil.debug("GameSetUpCheck - processing GameSetUpCheck.txt")
			fp = open(filename, 'r')
			for line in fp:
				BugUtil.debug("GameSetUpCheck - %s", line)
				(type, key, value) = line.split(",")
				if (type == 'minHOFOpponents'):
					minHOFOpponents.append(int(value.strip()))
				elif (type == 'maxHOFOpponents'):
					maxHOFOpponents.append(int(value.strip()))
				elif (type == 'reqHOFGameOptions'):
					hofGameOptionRequirements.append(int(value.strip()))
				elif (type == 'hofAllowedMapScripts'):
					hofAllowedMapScripts[key.strip()] = int(value.strip())
				elif (type == 'hofAllowedCylindrical'):
					hofAllowedCylindrical[key.strip()] = int(value.strip())
				elif (type == 'hofAllowedToroidal'):
					hofAllowedToroidal[key.strip()] = int(value.strip())
				elif (type == 'balancedOptionIndex'):
					balancedOptionIndex[key.strip()] = int(value.strip())
				elif (type == 'worldWrapOptionIndex'):
					worldWrapOptionIndex[key.strip()] = int(value.strip())
				elif (type == 'allowedWorldWrapValue'):
					allowedWorldWrapValue[key.strip()] = int(value.strip())
				elif (type == 'modCRC'):
					global modCRC
					modCRC = key
				elif (type == 'dllCRC'):
					global dllCRC
					dllCRC = key
				elif (type == 'shaderCRC'):
					global shaderCRC
					shaderCRC = key
				elif (type == 'pythonCRC'):
					global pythonCRC
					pythonCRC = key
				elif (type == 'xmlCRC'):
					global xmlCRC
					xmlCRC = key
				else:
					BugUtil.warn("Unknown type '%s' in GameSetUpCheck.txt", type)
			fp.close()
			return True
		except:
			BugUtil.trace("Error processing GameSetUpCheck.txt")
			try:
				fp.close()
			except:
				pass
	return False

def overrideSaveGameStart():
	"""
	Replaces AutoSave.saveGameStart() with the one from this module that checks CRCs.
	"""
	BugUtil.debug("GameSetUpCheck - overriding AutoSave.saveGameStart()")
	AutoSave.saveGameStart = saveGameStart


def saveGameStart():
	"""
	Saves the single-player game when the map is generated as long as MapFinder isn't active.
	
	Checks the CRCs and map settings if BUFFY is active.
	
	NOTE: The save is created and deleted in some cases because it is needed to check the CRCs.
	      Do not try to optimize this unless you are sure you know what's up!
	"""
	if not CyGame().isGameMultiPlayer() and not MapFinder.isActive():
		if isNeedToCheckCRCs() or AutoSaveOpt.isCreateStartSave():
			fileName = AutoSave.saveGame()
			if isNeedToCheckCRCs():
				checkCRCs(fileName)
				if not settingsOK():
					BugUtil.error(getWarningMessage())
			if not AutoSaveOpt.isCreateStartSave():
				os.remove(fileName)

def getWarningMessage():
	"""
	Returns either a HOF-only or HOF-and-GOTM warning message based on CyGame.getWarningStatus().
	"""
	if CyGame().getWarningStatus() == 1:
		return BugUtil.getText("TXT_KEY_BUFFY_INVALID_HOF_GOTM")
	else:
		return BugUtil.getText("TXT_KEY_BUFFY_INVALID_HOF")

def isNeedToCheckCRCs():
	"""
	Returns True if the CRCs need to be checked during the starting save process.
	
	For now we always check the CRCs so the warning can show on DoM screen and Settings tab.
	"""
	return True

def checkCRCs(fileName):
	"""
	Checks the saved game's CRCs and returns the result, storing it for use during settingsOK().
	"""
	global crcResult
	crcResult = CyGame().checkCRCs(fileName, modCRC, dllCRC, shaderCRC, pythonCRC, xmlCRC)
	return crcResult


def getBalanced():
	"""
	Returns True if the map has a Balanced option and it was chosen by the player.
	"""
	map = gc.getMap()
	balanced = False
	if balancedOptionIndex.has_key(map.getMapScriptName()):
		balancedIndex = balancedOptionIndex[map.getMapScriptName()]
		if balancedIndex>=0:
			if map.getCustomMapOption(balancedIndex)==1:
				balanced = True
	return balanced

def getWorldWrap():
	"""
	Returns the map's wrap setting: Flat, Cylindrical, or Toroidal.
	"""
	map = gc.getMap()
	worldWrap = WRAP_FLAT
	if map.isWrapY():
		worldWrap = WRAP_TOROIDAL
	elif map.isWrapX():
		worldWrap = WRAP_CYLINDRICAL
	return worldWrap

def getWorldWrapSettingOK():
	"""
	Returns True if the map's wrap setting is acceptable.
	"""
	map = gc.getMap()
	mapScript = gc.getMap().getMapScriptName()
	worldWrapOK = True
	if hofAllowedCylindrical.has_key(mapScript):
		if hofAllowedCylindrical[mapScript] == 0:
			if map.isWrapX():
				worldWrapOK = False
	if hofAllowedToroidal.has_key(mapScript):
		if hofAllowedToroidal[mapScript] == 0:
			if map.isWrapY():
				worldWrapOK = False
	return worldWrapOK

def settingsOK():
	"""
	Returns True if BUFFY is enabled and all game/map settings and CRCs are acceptable.
	"""
	game = gc.getGame()
	map = gc.getMap()
	
	if game.getWarningStatus() == 1:
		return False

	# Check that the map script used is a valid one
	if (map.getMapScriptName().upper().find('GOTM') != -1 or
		map.getMapScriptName().upper().find('WOTM') != -1 or
		map.getMapScriptName().upper().find('BOTM') != -1):
			return true
	if not hofAllowedMapScripts.has_key(map.getMapScriptName()):
		return False

	# Don't allow the balanced option
	if getBalanced():
		return False

	# Check that the world wrap setting is OK
	if not getWorldWrapSettingOK():
		return False

	# Check that all victory conditions are enabled
	for iVCLoop in range(gc.getNumVictoryInfos()):
		if not game.isVictoryValid(iVCLoop):
			return False

	# Ensure the game is single player
	if game.isGameMultiPlayer():
		return False

	# Check the options
	for i in range(GameOptionTypes.NUM_GAMEOPTION_TYPES):
		if game.isOption(i):
			if hofGameOptionRequirements[i]==-1:
				return False
		else:
			if hofGameOptionRequirements[i]==1:
				return False

	iActivePlayer = game.getActivePlayer()
	leaderCounts = [0] * gc.getNumLeaderHeadInfos()
	opponentCount = 0
	for iLoopPlayer in range(gc.getMAX_CIV_PLAYERS()):
		player = gc.getPlayer(iLoopPlayer)
		if (player.isEverAlive() and not player.isBarbarian() and not player.isMinorCiv()):
			if iLoopPlayer != iActivePlayer:
				opponentCount += 1
			iLeader = player.getLeaderType()
			if iLeader >= 0:
				leaderCounts[iLeader] += 1

	if (opponentCount < minHOFOpponents[map.getWorldSize()] or opponentCount > maxHOFOpponents[map.getWorldSize()]):
		return False

	for count in leaderCounts:
		if count > 1:
			return False

	if game.isTeamGame():
		return False

	dllPath = game.getDLLPath()
	exePath = game.getExePath()
	
	dllPathThenUp3 = os.path.split(os.path.split(os.path.split(dllPath)[0])[0])[0]
	if dllPathThenUp3 != exePath:
		return False

	if crcResult != 0:
		return False

	return True
