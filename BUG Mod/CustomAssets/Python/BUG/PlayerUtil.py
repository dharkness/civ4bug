## PlayerUtil
##
## Utilities for dealing with Players and their Teams, Cities and Units.
##
##   getPlayer(playerOrID)
##     Returns the CyPlayer given an ID or CyPlayer
##   getPlayerID(playerOrID)
##     Returns the ID given an ID or CyPlayer
##   getPlayerAndID(playerOrID)
##     Returns the ID and CyPlayer given an ID or CyPlayer
##
## Similar functions exist for Teams, Players and Teams together, and active
## versions that don't require an ID or object, using the active player instead.
## All of them return -1 and/or None if given -1 or None for playerOrId.
##
##   players(), teams(), teamPlayers(teamOrID)
##     Loop over players, teams or players belonging to a team.
##     Only valid objects that were alive at some point are returned, and they can
##     be filtered further by alive, human, and/or barbarian status.
##
##   playerUnits(playerOrID), playerCities(playerOrID)
##     Loop over a player's units or cities.
##
##   getStateReligion(playerOrID)
##   getFavoriteCivic(playerOrID)
##   getWorstEnemyPlayer(playerOrID, askingPlayerOrID)
##     Returns a single piece of information about the given player.
##
##   getActiveWars(playerOrID, askingPlayerOrID)
##   getPossibleWars(playerOrID, askingPlayerOrID)
##   isWHEOOH(playerOrID, askingPlayerOrID)
##     Returns various information regarding the war situation for the given player.
##
## Copyright (c) 2008 The BUG Mod.
##
## Author: EmperorFool

from CvPythonExtensions import *

gc = CyGlobalContext()

## Players and Teams - Getting IDs and Cy objects 

def getPlayer(playerOrID):
	"""Returns the CyPlayer for the given player."""
	if playerOrID is None or playerOrID == -1:
		return None
	if isinstance(playerOrID, int):
		return gc.getPlayer(playerOrID)
	return playerOrID

def getPlayerID(playerOrID):
	"""Returns the Player ID for the given player."""
	if playerOrID is None or playerOrID == -1:
		return -1
	if isinstance(playerOrID, int):
		return playerOrID
	return playerOrID.getID()

def getPlayerAndID(playerOrID):
	"""Returns the Player ID and CyPlayer for the given player."""
	if playerOrID is None or playerOrID == -1:
		return -1, None
	if isinstance(playerOrID, int):
		return playerOrID, gc.getPlayer(playerOrID)
	return playerOrID.getID(), playerOrID


def getTeam(teamOrID):
	"""Returns the CyTeam for the given team."""
	if teamOrID is None or teamOrID == -1:
		return None
	if isinstance(teamOrID, int):
		return gc.getTeam(teamOrID)
	return teamOrID

def getTeamID(teamOrID):
	"""Returns the Team ID for the given team."""
	if teamOrID is None or teamOrID == -1:
		return -1
	if isinstance(teamOrID, int):
		return teamOrID
	return teamOrID.getID()

def getTeamAndID(teamOrID):
	"""Returns the Team ID and CyTeam for the given team."""
	if teamOrID is None or teamOrID == -1:
		return -1, None
	if isinstance(teamOrID, int):
		return teamOrID, gc.getTeam(teamOrID)
	return teamOrID.getID(), teamOrID


def getPlayerTeam(playerOrID):
	"""Returns the CyTeam for the given player."""
	player = getPlayer(playerOrID)
	if player:
		return gc.getTeam(player.getTeam())
	return None

def getPlayerTeamID(playerOrID):
	"""Returns the Team ID for the given player."""
	player = getPlayer(playerOrID)
	if player:
		return player.getTeam()
	return -1

def getPlayerTeamAndID(playerOrID):
	"""Returns the Team ID and CyTeam for the given player."""
	player = getPlayer(playerOrID)
	if player:
		eTeam = player.getTeam()
		return eTeam, gc.getTeam(eTeam)
	return -1, None


def getPlayerAndTeam(playerOrID):
	"""Returns the CyPlayer and CyTeam for the given player."""
	player = getPlayer(playerOrID)
	if player:
		return player, gc.getTeam(player.getTeam())
	return None, None

def getPlayerAndTeamIDs(playerOrID):
	"""Returns the Player ID and Team ID for the given player."""
	ePlayer, player = getPlayer(playerOrID)
	if player:
		return ePlayer, player.getTeam()
	return -1, -1

def getPlayerAndTeamAndIDs(playerOrID):
	"""Returns the Player ID, CyPlayer, Team ID and CyTeam for the given player."""
	ePlayer, player = getPlayer(playerOrID)
	if player:
		eTeam = player.getTeam()
		return ePlayer, player, eTeam, gc.getTeam(eTeam)
	return -1, None, -1, None


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

def players(alive=None, human=None, barbarian=None, minor=None):
	"""
	Creates an iterator for all valid CyPlayers that were ever alive.
	
	Pass in True or False for alive to limit to alive or dead players, respectively.
	Pass in True or False for human to limit to human or AI players, respectively.
	Pass in True or False for barbarian to limit to/from barbarian players, respectively.
	Pass in True or False for minor to limit to/from minor players, respectively.
	
	for player in PlayerUtil.players():
		...
	"""
	for ePlayer in range(gc.getMAX_PLAYERS()):
		player = gc.getPlayer(ePlayer)
		if not player.isNone() and player.isEverAlive():
			if matchPlayerOrTeam(player, alive, human, barbarian, minor):
				yield player

def teamPlayers(teamOrID, alive=None, human=None, barbarian=None, minor=None):
	"""
	Creates an iterator for the CyPlayers on the given team.
	
	Pass in True or False for alive to limit to alive or dead players, respectively.
	Pass in True or False for human to limit to human or AI players, respectively.
	Pass in True or False for barbarian to limit to/from barbarian players, respectively.
	Pass in True or False for minor to limit to/from minor players, respectively.
	These restrictions are first applied to the CyTeam itself.
	
	for player in PlayerUtil.teamPlayers(PlayerUtil.getActiveTeamID()):
		...
	"""
	eTeam, team = getTeamAndID(teamOrID)
	if matchPlayerOrTeam(team, alive, human, barbarian, minor):
		for player in players(alive, human, barbarian, minor):
			if player.getTeam() == eTeam:
				yield player

def teams(alive=None, human=None, barbarian=None, minor=None):
	"""
	Creates an iterator for all valid CyTeams that were ever alive.
	
	Pass in True or False for alive to limit to alive or dead teams, respectively.
	Pass in True or False for human to limit to human or AI teams, respectively.
	Pass in True or False for barbarian to limit to/from barbarian teams, respectively.
	Pass in True or False for minor to limit to/from minor players, respectively.
	
	for team in PlayerUtil.teams():
		...
	"""
	for eTeam in range(gc.getMAX_TEAMS()):
		team = gc.getTeam(eTeam)
		if (not team.isNone() and team.isEverAlive() 
				and matchPlayerOrTeam(team, alive, human, barbarian, minor)):
			yield team

def matchPlayerOrTeam(teamOrPlayer, alive=None, human=None, barbarian=None, minor=None):
	"""
	Returns True of the CyPlayer or CyTeam matches the selected filters.
	
	Pass in True or False for alive to limit to alive or dead teams, respectively.
	Pass in True or False for human to limit to human or AI teams, respectively.
	Pass in True or False for barbarian to limit to/from barbarian teams, respectively.
	Pass in True or False for minor to limit to/from minor players, respectively.
	
	Pass None (or leave out) for any filter to ignore it.
	"""
	return ((alive is None or alive == teamOrPlayer.isAlive())
			and (human is None or human == teamOrPlayer.isHuman())
			and (barbarian is None or barbarian == teamOrPlayer.isBarbarian())
			and (minor is None or minor == teamOrPlayer.isMinorCiv()))


## Units and Cities - Iteration

def playerUnits(playerOrID):
	"""
	Creates an iterator for the CyUnits owned by the given player.
	
	for unit in PlayerUtil.playerUnits(PlayerUtil.getActivePlayerID()):
		...
	"""
	ePlayer, player = getPlayerAndID(playerOrID)
	unit, iter = player.firstUnit(False)
	while unit:
		if not unit.isDead():
			yield unit
		unit, iter = player.nextUnit(iter, False)

def playerCities(playerOrID):
	"""
	Creates an iterator for the CyCities owned by the given player.
	
	for city in PlayerUtil.playerCities(PlayerUtil.getActivePlayerID()):
		...
	"""
	ePlayer, player = getPlayerAndID(playerOrID)
	city, iter = player.firstCity(False)
	while city:
		if not city.isNone() and city.getOwner() == ePlayer:
			yield city
		city, iter = player.nextCity(iter, False)


## Player Information

def getStateReligion(playerOrID):
	"""Returns the state religion of the given player or -1 if none."""
	player = getPlayer(playerOrID)
	return player.getStateReligion()

def getFavoriteCivic(playerOrID):
	"""Returns the favorite civic of the given player's leader or -1 if none."""
	eLeaderType = getPlayer(playerOrID).getLeaderType()
	if eLeaderType != -1:
		leader = gc.getLeaderHeadInfo(eLeaderType)
		if leader:
			return leader.getFavoriteCivic()
	return CivicTypes.NO_CIVIC

def getWorstEnemyPlayer(playerOrID, askingPlayerOrID=None):
	"""
	Returns the CyPlayer who is the worst enemy of the given player or None.
	
	If askingPlayerOrID is given, the check is restricted to players they have met.
	"""
	name = getPlayer(playerOrID).getWorstEnemyName()
	if name:
		for player in players(alive=True, barbarian=False, minor=False):
			if player.getName() == name:
				if askingPlayerOrID is not None:
					askingTeam = getPlayerTeam(askingPlayerOrID)
					if (askingTeam and (askingTeam.isHasMet(player.getTeam())
							or gc.getGame().isDebugMode())):
						return player
					return None
				return player
	return None


## Wars

def getActiveWars(playerOrID, askingPlayerOrID):
	wars = []
	askedPlayer, askedTeam = getPlayerAndTeam(playerOrID)
	askingPlayer, askingTeam = getPlayerAndTeam(askingPlayerOrID)
	for player in players(alive=True, barbarian=False, minor=False):
		if askingTeam.isHasMet(player.getTeam()) or gc.getGame().isDebugMode():
			if askedTeam.isAtWar(player.getTeam()):
				wars.append(player)
	return wars

def getPossibleWars(playerOrID, askingPlayerOrID, justWHEOOH=False):
	"""
	Returns a tuple containing the WHEOOH status of the given player and 
	a list of all CyPlayers on which the given player will declare war in a trade.
	
	If askingPlayerOrID is given, the check is restricted to players they have both met.
	
	If justWHEOOH is True, only the WHOOH status is returned as soon as it's found.
	"""
	wheooh = False
	wars = []
	tradeData = TradeData()
	tradeData.ItemType = TradeableItems.TRADE_WAR
	askedPlayer, askedTeam = getPlayerAndTeam(playerOrID)
	askingPlayer, askingTeam = getPlayerAndTeam(askingPlayerOrID)
	for player in players(alive=True, barbarian=False, minor=False):
		if (askingPlayer.getID() == player.getID()
				or not (askingTeam.isHasMet(player.getTeam()) or gc.getGame().isDebugMode())):
			continue
		if (player.getID() == askedPlayer.getID() or askedTeam.isAtWar(player.getTeam())
				or not (askedTeam.isHasMet(player.getTeam()) or gc.getGame().isDebugMode())):
			continue
		tradeData.iData = player.getID()
		if askedPlayer.canTradeItem(askingPlayer.getID(), tradeData, False):
			denial = askedPlayer.getTradeDenial(askingPlayer.getID(), tradeData)
			if denial == DenialTypes.NO_DENIAL:
				wars.append(player)
			elif denial == DenialTypes.DENIAL_TOO_MANY_WARS:
				if justWHEOOH:
					return True
				wheooh = True
	if justWHEOOH:
		return wheooh
	return (wheooh, wars)

def isWHEOOH(playerOrID, askingPlayerOrID):
	"""Returns True if askingPlayerOrID can see that playerOrID is WHEOOH."""
	return getPossibleWars(playerOrID, askingPlayerOrID, True)
