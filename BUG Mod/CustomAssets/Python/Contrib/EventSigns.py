## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
##
## EventSigns.py for the BUG Mod by Dresden
##
## Keeps track of plot signs created by the EventSigns random
## event interface and displays them once the plot is visible.
##

from CvPythonExtensions import *

import BugUtil
import SdToolKit

# Bug Options
import BugCore
import BugOptions
EventSignsOpt = BugCore.game.EventSigns

# civ globals
gc = CyGlobalContext()
engine = CyEngine()
localText = CyTranslator()
map = CyMap()

# for sdtoolkit
SD_MOD_ID = "EventSigns"
SD_VAR_ID = "savedSigns"

# globals for data
gSavedSigns = None
gCurrentSigns = None
g_bShowSigns = False
g_bForceUpdate = False

# Module-level access functions
def initData ():
	""" Initialize the internal plot-caption data structure, clearing all previous data. """
	BugUtil.debug("EventSigns.initData() initializing gSavedSigns")
	global gSavedSigns
	gSavedSigns = MapSigns()
	return True

def initOptions ():
	""" Initialization based upon BUG Options. """
	global g_bShowSigns
	g_bShowSigns = EventSignsOpt.isEnabled()
	BugUtil.debug("EventSigns.initOptions() initializing. g_bShowSigns is %s." %(g_bShowSigns))
	return True

def enabledOptionChanged (pIniObject, bNewValue):
	""" Handler function for processing changes to the Enabled option. """
	BugUtil.debug("EventSigns.enabledOptionsChanged(%s, %s) resetting g_bShowSigns." %(str(pIniObject), str(bNewValue)))
	global g_bShowSigns
	if g_bShowSigns != bNewValue:
		g_bShowSigns = bNewValue
		gSavedSigns.processSigns(g_bShowSigns)
	return True

def addSign (pPlot, ePlayer, szCaption):
	""" Wrapper for CyEngine.addSign() which stores sign data. 
	If -1 is passed for ePlayer, the sign is assumed to be a landmark that everyone can see.
	"""
	#BugUtil.debug("EventSigns.addSign(pPlot = %s, ePlayer = %s, szCaption = %s)" % (str(pPlot), str(ePlayer), szCaption))
	if not pPlot or pPlot.isNone():
		BugUtil.warn("EventSigns.addSign() was passed an invalid plot: %s" % (str(pPlot)))
		return False
	if gSavedSigns == None:
		BugUtil.warn("EventSigns.addSign() gSavedSigns is not initialized!")
		return False
	gSavedSigns.storeSign(pPlot, ePlayer, szCaption)
	gSavedSigns.displaySign(pPlot, ePlayer)
	return True

def updateCurrentSigns ():
	""" Updates gCurrentSigns global with all current signs on map. Remeber to clear when done."""
	global gCurrentSigns
	gCurrentSigns = MapSigns()
	for iSign in range(engine.getNumSigns()):
		pSign = engine.getSignByIndex(iSign)
		pPlot = pSign.getPlot()
		ePlayer = pSign.getPlayerType()
		szCaption = pSign.getCaption()
		if not gCurrentSigns.hasPlotSigns(pPlot):
			gCurrentSigns[pPlot] = PlotSigns(pPlot)
		gCurrentSigns[pPlot].setSign(ePlayer, szCaption)
	BugUtil.debug("EventSigns.updateCurrentSigns() finished.\n %s" % (str(gCurrentSigns)))
	return True

def clearCurrentSigns ():
	""" Resets gCurrentSigns global; should always be called when finished after an update. """
	global gCurrentSigns
	gCurrentSigns = None


class MapSigns:
	""" A collection of PlotSigns, organized by plot. """

	def __init__ (self):
		""" Class initialization. """
		self.reset()

	def reset (self):
		""" Resets data for this instance to defaults. """
		self.plotDict = {}

	def isEmpty (self):
		""" Check to see if object has any PlotSigns data. """
		return (len(self.signDict) == 0)

	def getPlotSigns (self, pPlot):
		""" Returns PlotSigns object for given Plot. """
		thisKey = self.__getKey(pPlot)
		if thisKey in self.plotDict:
			return self.plotDict[thisKey]
		else:
			return None

	def __getitem__ (self, pPlot):
		""" Special method to allow access like pPlotSigns = pMapSigns[pPlot] """
		return self.getPlotSigns(pPlot)

	def setPlotSigns (self, pPlot, pPlotSigns):
		""" Sets PlotSigns object for given Plot. """
		thisKey = self.__getKey(pPlot)
		self.plotDict[thisKey] = pPlotSigns
		return None

	def __setitem__ (self, pPlot, pPlotSigns):
		""" Special method to allow access like pMapSigns[pPlot] = pPlotSigns """
		return self.setPlotSigns(pPlot, pPlotSigns)

	def removePlotSigns(self, pPlot):
		""" Removes PlotSigns object for given Plot. """
		thisKey = self.__getKey(pPlot)
		if thisKey in self.plotDict:
			del self.plotDict[thisKey]
			return True
		return False

	def __delitem__ (self, pPlot):
		""" Special method to allow access like del pMapSigns[pPlot] """
		return self.removePlotSigns(pPlot)

	def hasPlotSigns (self, pPlot):
		""" Do we have a PlotSigns element corresponding to that plot? """
		thisKey = self.__getKey(pPlot)
		if thisKey in self.plotDict:
			return True
		return False

	def __str__ (self):
		""" String representation of class instance. """
		#return "MapSigns { plotDict=%s }" % (str(self.plotDict))
		# The above doesn't seem to propagate the %s to the PlotSigns, so we do it the long way
		szText = "MapSigns { plotDict = {"
		for key in self.plotDict:
			pPlotSigns = self.plotDict[key]
			szText = szText + "\n\t" + str(key) + ": " + str(pPlotSigns) + ", "
		szText = szText + " } }"
		return szText

	def storeSign (self, pPlot, ePlayer, szCaption):
		""" Stores sign data in the appropraite PlotSigns element. """
		thisKey = self.__getKey(pPlot)
		if not thisKey:
			BugUtil.warn("MapSigns.storeSign() could not determine valid keyname for Plot %s." % (str(pPlot)))
			return False
		if not thisKey in self.plotDict:
			self.plotDict[thisKey] = PlotSigns(pPlot)
		self.plotDict[thisKey].setSign(ePlayer, szCaption)

	def displaySign (self, pPlot, ePlayer):
		""" Displays stored sign for given player at given plot based on revealed status.
		If there's a pre-existing sign, engine.addSign will silently fail, leaving the plot unchanged.
		"""
		if not g_bShowSigns:
			BugUtil.debug("MapSigns.displaySign() called but EventSigns is disabled.")
			return False
		if not pPlot or pPlot.isNone():
			BugUtil.warn("MapSigns.displaySign() was passed an invalid plot: %s" % (str(pPlot)))
			return False
		thisKey = self.__getKey(pPlot)
		szCaption = ""
		if self.hasPlotSigns(pPlot):
			szCaption = self.plotDict[thisKey].getSign(ePlayer)
		else:
			#BugUtil.debug("MapSigns.displaySign() could not show sign; we don't have any saved signs on plot %s" % (str(thisKey)))
			return False
		if not szCaption:
			BugUtil.debug("MapSigns.displaySign() could not show sign; no caption found for player %d on plot %s" % (ePlayer, str(thisKey)))
			return False
		if ePlayer == -1:
			BugUtil.debug("MapSigns.displaySign() landmark (%s) shown on plot %s" % (szCaption, ePlayer, str(thisKey)))
			engine.addLandmark(pPlot, szCaption.encode('latin_1'))
		else:
			pPlayer = gc.getPlayer(ePlayer)
			if not pPlayer or pPlayer.isNone():
				BugUtil.warn("MapSigns.displaySign() was passed an invalid player id: %s" % (str(ePlayer)))
				return False
			eTeam = pPlayer.getTeam()
			if pPlot.isRevealed(eTeam, False):
				BugUtil.debug("MapSigns.displaySign() sign (%s) shown for player %d on plot %s" % (szCaption, ePlayer, str(thisKey)))
				engine.addSign(pPlot, ePlayer, szCaption.encode('latin_1'))
				return True
			else:
				BugUtil.debug("MapSigns.displaySign() could not show sign; player %d cannot see plot %s" % (ePlayer, str(thisKey)))
		return False

	def hideSign (self, pPlot, ePlayer):
		""" Hides sign for given player at given plot if there's a current sign the same as the stored one. 
		Note that this function assumes gCurrentSigns is up-to-date so make sure you've updated first.
		"""
		if not pPlot or pPlot.isNone():
			BugUtil.warn("MapSigns.hideSign() was passed an invalid plot: %s" % (str(pPlot)))
			return False
		thisKey = self.__getKey(pPlot)
		if gCurrentSigns == None:
			BugUtil.debug("MapSigns.hideSign() finds no current signs so there's nothing to hide.")
			return False
		if self.hasPlotSigns(pPlot):
			szCaption = self.plotDict[thisKey].getSign(ePlayer)
			if gCurrentSigns.hasPlotSigns(pPlot):
				szExistingCaption = gCurrentSigns[pPlot].getSign(ePlayer)
				if szCaption and szCaption == szExistingCaption:
					BugUtil.debug("MapSigns.hideSign() found matching sign (%s) for player %d on plot %s; will remove it" % (szCaption, ePlayer, str(thisKey)))
					if ePlayer == -1:
						engine.removeLandmark(pPlot)
					else:
						engine.removeSign(pPlot, ePlayer)
					return True
				else:
					BugUtil.debug("MapSigns.hideSign() found sign for player %d saying (%s) instead of (%s) on plot %s; will leave alone." % (ePlayer, szExistingCaption, szCaption, str(thisKey)))
			else:
				BugUtil.debug("MapSigns.hideSign() found no sign on plot %s to remove" % (str(thisKey)))
		else:
			BugUtil.debug("MapSigns.hideSign() found no saved signs at all for plot %s" % (str(thisKey)))
		return False

	def removeSign (self, pPlot, ePlayer):
		""" Removes sign for given player at given plot from storage. """
		if self.hasPlotSigns(pPlot):
			thisKey = self.__getKey(pPlot)
			self.plotDict[thisKey].removeSign(ePlayer)
			# If that was the last caption stored, clean up after ourselves
			if self.plotDict[thisKey].isEmpty():
				del self.plotDict[thisKey]
				return True
		return False

	def processSigns (self, bShow = None):
		""" Shows or hides all signs based on boolean argument which defaults to global g_bShowSigns. """
		BugUtil.debug("MapSigns.processSigns() starting. bShow = %s and g_bShowSigns = %s" % (str(bShow), str(g_bShowSigns)))
		updateCurrentSigns()
		if bShow == None:
			bShow = g_bShowSigns
		for pSign in self.plotDict.itervalues():
			pPlot = pSign.getPlot()
			BugUtil.debug("MapSigns.processSigns() Found saved sign data for plot %d, %d ..." % (pPlot.getX(), pPlot.getY()))
			for ePlayer in pSign.getPlayers():
				BugUtil.debug("MapSigns.processSigns() ... and caption for player %d" % (ePlayer))
				if (bShow):
					self.displaySign(pPlot, ePlayer)
				else:
					self.hideSign(pPlot, ePlayer)
		clearCurrentSigns()
		return True

	# Private Methods

	def __getKey(self, pPlot):
		""" Gets keyname used to access this plot object. """
		thisKey = None
		if pPlot and not pPlot.isNone():
			thisKey = (pPlot.getX(), pPlot.getY())
		return thisKey


class PlotSigns:
	""" Sign information for all players for a given plot. """

	def __init__(self, pPlot):
		""" Class initialization. Parameter is Plot Object. """
		if pPlot and not pPlot.isNone():
			self.reset()
			self.iX = pPlot.getX()
			self.iY = pPlot.getY()

	def reset(self):
		""" Resets data for this instance to defaults. """
		self.iX = -1
		self.iY = -1
		self.signDict = {}

	def isEmpty(self):
		""" Check to see if object has any caption data. """
		return (len(self.signDict) == 0)

	def getPlot(self):
		""" Returns plot object. """
		return map.plot(self.iX, self.iY)

	def setPlot(self, pPlot):
		""" Assigns plot object. """
		if pPlot and not pPlot.isNone():
			self.iX = pPlot.getX()
			self.iY = pPlot.getY()

	def getPlayers(self):
		""" Returns a set of player IDs corresponding to stored signs. """
		ePlayerSet = set()
		for ePlayer in self.signDict:
			ePlayerSet.add(ePlayer)
		return ePlayerSet

	def getSign(self, ePlayer):
		""" Returns Caption for a given player on this plot. """
		szCaption = ""
		if ePlayer in self.signDict:
			szCaption = self.signDict[ePlayer] 
		return szCaption

	def setSign(self, ePlayer, szCaption):
		""" Sets Caption for a given player on this plot. """
		if ePlayer in ([-1] + range(gc.getMAX_PLAYERS())):
			self.signDict[ePlayer] = szCaption
		else:
			BugUtil.warn("EventSigns PlotSigns.setSign() was passed an invalid Player ID %s at Plot (%d,%d)" % (str(ePlayer), self.iX, self.iY))

	def removeSign(self, ePlayer):
		""" Removes Caption for a given player on this plot. """
		szCaption = ""
		if ePlayer in self.signDict:
			del self.signDict[ePlayer] 
		else:
			BugUtil.warn("EventSigns PlotSigns.removeSign() failed to find a caption for Player %d at Plot (%d,%d)" % (ePlayer, self.iX, self.iY))

	def __str__ (self):
		""" String representation of class instance. """
		return "PlotSigns { iX = %d, iY = %d, signDict = %s }" % (self.iX, self.iY, str(self.signDict))


class PlotCaptions:
	""" Fake class needed to load games made with first development version. """
	def __init__ (self):
		self.iX = None
		self.iY = None
		self.teamDict = None


class EventSignsEventHandler:
	""" Event Handler for this module. """

	def __init__(self, eventManager):
		BugUtil.debug("EventSigns EventSignsEventHandler.__init__(). Resetting data and initing event manager.")
		initOptions()
		initData()
		## Init event handlers
		eventManager.addEventHandler("GameStart", self.onGameStart)
		eventManager.addEventHandler("OnLoad", self.onLoadGame)
		eventManager.addEventHandler("OnPreSave", self.onPreSave)
		eventManager.addEventHandler("plotRevealed", self.onPlotRevealed)
		eventManager.addEventHandler("BeginActivePlayerTurn", self.onBeginActivePlayerTurn)

	def onGameStart(self, argsList):
		""" Called when a new game is started """
		#BugUtil.debug("EventSignsEventHandler.onGameStart()")
		initOptions()
		initData()

	def onLoadGame(self, argsList):
		""" Called when a game is loaded """
		BugUtil.debug("EventSignsEventHandler.onLoadGame()")
		initOptions()
		## Clean up after early development mistake
		SdToolKit.sdDelGlobal(SD_MOD_ID, 'data')
		data = SdToolKit.sdGetGlobal(SD_MOD_ID, SD_VAR_ID)
		if (data):
			global gSavedSigns
			gSavedSigns = data
			SdToolKit.sdSetGlobal(SD_MOD_ID, SD_VAR_ID, None)
			BugUtil.debug("EventSigns Data Loaded:\n %s" % (gSavedSigns))
		else:
			BugUtil.debug("EventSigns has no saved data. Initializing new data.")
			initData()
		# Hey guess what? The map isn't fully loaded yet so we can't update the signs yet. Super.
		global g_bForceUpdate
		g_bForceUpdate = True

	def onPreSave(self, argsList):
		""" Called before a game is actually saved """
		#BugUtil.debug("EventSignsEventHandler.onPreSave()")
		if (gSavedSigns):
			SdToolKit.sdSetGlobal(SD_MOD_ID, SD_VAR_ID, gSavedSigns)
			#BugUtil.debug("Data Saved to sdtoolkit\n %s" % (gSavedSigns))

	def onPlotRevealed(self, argsList):
		""" Called when plot is revealed to team. """
		(pPlot, eTeam) = argsList
		#BugUtil.debug("EventSignsEventHandler.onPlotRevealed(pPlot = %s, eTeam = %s)" % (str(pPlot), str(eTeam)))
		if (g_bShowSigns):
			if (gSavedSigns):
				for ePlayer in range(gc.getMAX_PLAYERS()):
					pPlayer = gc.getPlayer(ePlayer)
					if pPlayer.getTeam() == eTeam:
						gSavedSigns.displaySign(pPlot, ePlayer)

	def onBeginActivePlayerTurn(self, argsList):
		""" Called at start of active player's turn """
		#BugUtil.debug("EventSignsEventHandler.onBeginActivePlayerTurn()")
		global g_bForceUpdate
		if g_bForceUpdate:
			gSavedSigns.processSigns(g_bShowSigns)
			g_bForceUpdate = False
