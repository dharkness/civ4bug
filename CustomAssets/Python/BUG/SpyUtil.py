## SpyUtil
##
## Tracks each player's espionage point values per player to provide access to spending levels.
##
## Copyright (c) 2009 The BUG Mod.
##
## Author: EmperorFool, ruff_hi

from CvPythonExtensions import *
import BugUtil
import PlayerUtil
import SdToolKit

gc = CyGlobalContext()


## Tracking Values for Previous and Current Turns

g_previousGameTurn = None
g_previousValues = None

def getDifferenceByPlayer(playerOrID, targetPlayerOrID=None):
	if targetPlayerOrID is None:
		return getDifferenceByTeam(PlayerUtil.getPlayerTeam(playerOrID))
	else:
		return getDifferenceByTeam(PlayerUtil.getPlayerTeam(playerOrID), PlayerUtil.getPlayerTeamID(playerOrID))

def getDifferenceByTeam(teamOrID, targetTeamOrID=None):
	eTeam, team = PlayerUtil.getTeamAndID(teamOrID)
	if targetTeamOrID is None:
		eTargetTeam = PlayerUtil.getActiveTeamID()
	else:
		eTargetTeam = PlayerUtil.getTeamID(targetTeamOrID)
	iPrevious = getPreviousValue(eTeam, eTargetTeam)
	if iPrevious is not None:
		return team.getEspionagePointsAgainstTeam(eTargetTeam) - iPrevious

def getPreviousValue(teamOrID, targetTeamOrID=None):
	if g_previousGameTurn == gc.getGame().getGameTurn():
		eTeam = PlayerUtil.getTeamID(teamOrID)
		if targetTeamOrID is None:
			eTargetTeam = PlayerUtil.getActiveTeamID()
		else:
			eTargetTeam = PlayerUtil.getTeamID(targetTeamOrID)
		if eTeam in g_previousValues:
			return g_previousValues[eTeam][eTargetTeam]
	return None

def getCurrentValues():
	valuesByTeam = {}
	for team in PlayerUtil.teams(True, None, False):
		valuesByTeam[team.getID()] = values = []
		for targetTeam in PlayerUtil.teams():
			values.append(team.getEspionagePointsAgainstTeam(targetTeam.getID()))
	return valuesByTeam


## Storing Values for Previous Turn

STORAGE_VERSION = 1

SD_MOD_ID = "SpyUtil"
SD_VERSION_ID = "version"
SD_TURN_ID = "turn"
SD_VALUES_ID = "values"

def clear(argsList=None):
	global g_previousValues, g_previousGameTurn
	g_previousGameTurn = None
	g_previousValues = None

def load(argsList=None):
	global g_previousValues, g_previousGameTurn
	clear()
	data = SdToolKit.sdModLoad(SD_MOD_ID)
	BugUtil.debug("SpyUtil - loaded: %s", data)
	if SD_VERSION_ID in data:
		if data[SD_VERSION_ID] == 1:
			g_previousGameTurn = data[SD_TURN_ID]
			g_previousValues = data[SD_VALUES_ID]
			if g_previousGameTurn != gc.getGame().getGameTurn():
				clear()
				BugUtil.warn("SpyUtil - incorrect previous game turn found, resetting")
		elif data[SD_VERSION_ID] > 1:
			BugUtil.warn("SpyUtil - newer data storage format detected, resetting")
			clear()

def store(argsList=None):
	global g_previousValues, g_previousGameTurn
	g_previousGameTurn = gc.getGame().getGameTurn()
	g_previousValues = getCurrentValues()
	data = {
		SD_VERSION_ID: STORAGE_VERSION,
		SD_TURN_ID: g_previousGameTurn,
		SD_VALUES_ID: g_previousValues
	}
	SdToolKit.sdModSave(SD_MOD_ID, data)
	BugUtil.debug("SpyUtil - stored: %s", data)
