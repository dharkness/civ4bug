## TechUtil
##
## Utilities for dealing with Technologies
##
## Copyright (c) 2008 The BUG Mod.

from CvPythonExtensions import *
import BugUtil

gc = CyGlobalContext()

NUM_TECHS = -1
NUM_AND_PREREQS = -1
NUM_OR_PREREQS = -1

g_initDone = False

def init():
	global g_initDone
	if g_initDone: return
	
	global NUM_TECHS, NUM_AND_PREREQS, NUM_OR_PREREQS
	NUM_TECHS = gc.getNumTechInfos()
	NUM_AND_PREREQS = gc.getNUM_AND_TECH_PREREQS()
	NUM_OR_PREREQS = gc.getNUM_OR_TECH_PREREQS()
	
	g_initDone = True

def getPlayer(ePlayer):
	"Returns the CyPlayer for the given player ID."
	return gc.getPlayer(ePlayer)

def getTeam(ePlayer):
	"Returns the CyTeam for the given player ID."
	return gc.getTeam(getPlayer(ePlayer).getTeam())

def getPlayerAndTeam(ePlayer):
	"Returns the CyPlayer and CyTeam for the given player ID."
	player = getPlayer(ePlayer)
	return player, gc.getTeam(player.getTeam())

def getKnownTechs(ePlayer):
	"""
	Returns a set of tech IDs that ePlayer knows.
	"""
	init()
	knowingTeam = getTeam(ePlayer)
	techs = set()
	for eTech in range(NUM_TECHS):
		if knowingTeam.isHasTech(eTech):
			techs.add(eTech)
	return techs

def getVisibleKnownTechs(ePlayer, eAskingPlayer):
	"""
	Returns a set of tech IDs that eAskingPlayer knows that ePlayer knows.
	
	Any techs that eAskingPlayer doesn't know and cannot research yet are removed
	from the set of all techs that ePlayer knows.
	"""
	init()
	knowingTeam = getTeam(ePlayer)
	askingPlayer, askingTeam = getPlayerAndTeam(eAskingPlayer)
	techs = set()
	for eTech in range(NUM_TECHS):
		if knowingTeam.isHasTech(eTech):
			if askingTeam.isHasTech(eTech) or askingPlayer.canResearch(eTech, False):
				techs.add(eTech)
	return techs
