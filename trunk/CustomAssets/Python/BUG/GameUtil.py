## BugUtil
##
## Collection of utility functions for dealing with the game and its options.
##
## Versions
##
##   getVersion()
##     Returns the running BTS version as an integer (e.g. 317).
##
##   isVersion(version)
##     Returns True if the BTS version is exactly <version>.
##
##   isVersionAtLeast(version)
##     Returns True if the BTS version is <version> or greater.
##
##   getSaveVersion()
##     Returns the saved game version as an integer (e.g. 301).
##
##   isSaveVersion(version)
##     Returns True if the saved game version is exactly <version>.
##
##   isSaveVersionAtLeast(version)
##     Returns True if the saved game version is <version> or greater.
##
## Game Values
##
##   getCultureThreshold(level)
##     Returns the culture required to achieve the <level> for the current game speed.
##
## Game Options
##
##   isEspionage()
##     Returns True if running at least 3.17 and the No Espionage option is set
##     for the game in progress.
##
## Copyright (c) 2009 The BUG Mod.
##
## Author: EmperorFool

from CvPythonExtensions import *


## Globals

gc = CyGlobalContext()


## Versions

def getVersion():
	return gc.getDefineINT("CIV4_VERSION")

def isVersion(version):
	return getVersion() == version

def isVersionAtLeast(version):
	return getVersion() >= version


def getSaveVersion():
	return gc.getDefineINT("SAVE_VERSION")

def isSaveVersion(version):
	return getSaveVersion() == version

def isSaveVersionAtLeast(version):
	return getSaveVersion() >= version


## Game Values

def getCultureThreshold(level):
	if isVersionAtLeast(319):
		return gc.getGame().getCultureThreshold(level)
	else:
		return gc.getCultureLevelInfo(level).getSpeedThreshold(gc.getGame().getGameSpeedType())


## Game Options

def isEspionage():
	"""
	Returns True if using at least 3.17 and the 'No Espionage' option is not enabled.
	"""
	if isVersionAtLeast(317):
		return not gc.getGame().isOption(GameOptionTypes.GAMEOPTION_NO_ESPIONAGE)
	return True
