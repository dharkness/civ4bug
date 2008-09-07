## PlayerUtil
##
## Utilities for dealing with Players and their Teams, Cities and Units.
##
##   getPlayer(playerOtId)
##     Returns the CyPlayer given an ID or CyPlayer
##   getPlayerID(playerOtId)
##     Returns the ID given an ID or CyPlayer
##   getPlayerAndID(playerOtId)
##     Returns the ID and CyPlayer given an ID or CyPlayer
##
## Similar functions exist for Teams, Players and Teams together, and active
## versions that don't require an ID or object, using the active player instead.
##
##   players(), teams(), teamPlayers(teamOrId)
##     Loop over players, teams or players belonging to a team.
##     Only valid objects that were alive at some point are returned, and they can
##     be filtered further by alive, human, and/or barbarian status.
##
##   playerUnits(playerOrId), playerCities(playerOrId)
##     Loop over a player's units or cities.
##
## Copyright (c) 2008 The BUG Mod.
##
## Author: EmperorFool

from CvPythonExtensions import *

gc = CyGlobalContext()

## Players and Teams - Getting IDs and Cy objects 

def getPlayer(playerOrId):
	"""Returns the CyPlayer for the given player."""
	if isinstance(playerOrId, int):
		return gc.getPlayer(playerOrId)
	return playerOrId

def getPlayerID(playerOrId):
	"""Returns the Player ID for the given player."""
	if isinstance(playerOrId, int):
		return playerOrId
	return playerOrId.getID()

def getPlayerAndID(playerOrId):
	"""Returns the Player ID and CyPlayer for the given player."""
	if isinstance(playerOrId, int):
		return playerOrId, gc.getPlayer(playerOrId)
	return playerOrId.getID(), playerOrId


def getTeam(teamOrId):
	"""Returns the CyTeam for the given team."""
	if isinstance(teamOrId, int):
		return gc.getTeam(teamOrId)
	return teamOrId

def getTeamID(teamOrId):
	"""Returns the Team ID for the given team."""
	if isinstance(teamOrId, int):
		return teamOrId
	return teamOrId.getID()

def getTeamAndID(teamOrId):
	"""Returns the Team ID and CyTeam for the given team."""
	if isinstance(teamOrId, int):
		return teamOrId, gc.getTeam(teamOrId)
	return teamOrId.getID(), teamOrId


def getPlayerTeam(playerOrId):
	"""Returns the CyTeam for the given player."""
	return gc.getTeam(getPlayer(playerOrId).getTeam())

def getPlayerTeamID(playerOrId):
	"""Returns the Team ID for the given player."""
	return getPlayer(playerOrId).getTeam()

def getPlayerTeamAndID(playerOrId):
	"""Returns the Team ID and CyTeam for the given player."""
	eTeam = getPlayer(playerOrId).getTeam()
	return eTeam, gc.getTeam(eTeam)


def getPlayerAndTeam(playerOrId):
	"""Returns the CyPlayer and CyTeam for the given player."""
	player = getPlayer(playerOrId)
	return player, gc.getTeam(player.getTeam())

def getPlayerAndTeamIDs(playerOrId):
	"""Returns the Player ID and Team ID for the given player."""
	ePlayer, player = getPlayer(playerOrId)
	return ePlayer, player.getTeam()

def getPlayerAndTeamAndIDs(playerOrId):
	"""Returns the Player ID, CyPlayer, Team ID and CyTeam for the given player."""
	ePlayer, player = getPlayer(playerOrId)
	eTeam = player.getTeam()
	return ePlayer, player, eTeam, gc.getTeam(eTeam)


def getActivePlayer():
	"""Returns the CyPlayer for the active player."""
	return gc.getActivePlayer()

def getActivePlayerID():
	"""Returns the Player ID for the active player."""
	return gc.getGame().getActivePlayer()

def getActivePlayerAndID():
	"""Returns the Player ID and CyPlayer for the active player."""
	return gc.getGame().getActivePlayer(), gc.getActivePlayer()


def getActiveTeam():
	"""Returns the CyTeam for the active player."""
	return gc.getActiveTeam()

def getActiveTeamID():
	"""Returns the Team ID for the active player."""
	return gc.getGame().getActiveTeam()

def getActiveTeamAndID():
	"""Returns the Team ID and CyTeam for the active player."""
	return gc.getGame().getActiveTeam(), gc.getActiveTeam()


def getActivePlayerAndTeam():
	"""Returns the CyPlayer and CyTeam for the active player."""
	return getActivePlayer(), getActiveTeam()

def getActivePlayerAndTeamIDs():
	"""Returns the Player ID and Team ID for the active player."""
	return getActivePlayerID(), getActiveTeamID()

def getActivePlayerAndTeamAndIDs():
	"""Returns the Player ID, CyPlayer, Team ID and CyTeam for the active player."""
	return getActivePlayerAndID() + getActiveTeamAndID()


## Players and Teams - Iteration

def players(alive=None, human=None, barbarian=None):
	"""
	Creates an iterator for all valid CyPlayers that were ever alive.
	
	Pass in True or False for alive to limit to alive or dead players, respectively.
	Pass in True or False for human to limit to human or AI players, respectively.
	Pass in True or False for barbarian to limit to/from barbarian players, respectively.
	
	for player in PlayerUtil.players():
		...
	"""
	for ePlayer in range(gc.getMAX_PLAYERS()):
		player = gc.getPlayer(ePlayer)
		if not player.isNone() and player.isEverAlive():
			if matchPlayerOrTeam(player, alive, human, barbarian):
				yield player

def teamPlayers(teamOrId, alive=None, human=None, barbarian=None):
	"""
	Creates an iterator for the CyPlayers on the given team.
	
	Pass in True or False for alive to limit to alive or dead players, respectively.
	Pass in True or False for human to limit to human or AI players, respectively.
	Pass in True or False for barbarian to limit to/from barbarian players, respectively.
	These restrictions are first applied to the CyTeam itself.
	
	for player in PlayerUtil.teamPlayers(PlayerUtil.getActiveTeamID()):
		...
	"""
	eTeam, team = getTeamAndID(teamOrId)
	if matchPlayerOrTeam(team, alive, human, barbarian):
		for player in players(alive, human, barbarian):
			if player.getTeam() == eTeam:
				yield player

def teams(alive=None, human=None, barbarian=None):
	"""
	Creates an iterator for all valid CyTeams that were ever alive.
	
	Pass in True or False for alive to limit to alive or dead teams, respectively.
	Pass in True or False for human to limit to human or AI teams, respectively.
	Pass in True or False for barbarian to limit to/from barbarian teams, respectively.
	
	for team in PlayerUtil.teams():
		...
	"""
	for eTeam in range(gc.getMAX_TEAMS()):
		team = gc.getTeam(eTeam)
		if (not team.isNone() and team.isEverAlive() 
				and matchPlayerOrTeam(team, alive, human, barbarian)):
			yield team

def matchPlayerOrTeam(teamOrPlayer, alive=None, human=None, barbarian=None):
	return ((alive is None or alive == teamOrPlayer.isAlive())
			and (human is None or human == teamOrPlayer.isHuman())
			and (barbarian is None or barbarian == teamOrPlayer.isBarbarian()))

## Units and Cities - Iteration

def playerUnits(playerOrId):
	"""
	Creates an iterator for the CyUnits owned by the given player.
	
	for unit in PlayerUtil.playerUnits(PlayerUtil.getActivePlayerID()):
		...
	"""
	ePlayer, player = getPlayerAndID(playerOrId)
	unit, iter = player.firstUnit(False)
	while unit:
		if not unit.isDead():
			yield unit
		unit, iter = player.nextUnit(iter, False)

def playerCities(playerOrId):
	"""
	Creates an iterator for the CyCities owned by the given player.
	
	for city in PlayerUtil.playerCities(PlayerUtil.getActivePlayerID()):
		...
	"""
	ePlayer, player = getPlayerAndID(playerOrId)
	city, iter = player.firstCity(False)
	while city:
		if not city.isNone() and city.getOwner() == ePlayer:
			yield city
		city, iter = player.nextCity(iter, False)
