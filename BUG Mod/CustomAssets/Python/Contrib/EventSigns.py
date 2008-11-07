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
SD_VAR_ID = "data"

# globals for data
gPlotCaptions = None

# Module-level access functions
def addSign (pPlot, ePlayer, szCaption):
	""" Wrapper for CyEngine.addSign() based on plot's revealed status.

	If the plot is revealed for the given player, simply calls CyEngine.addSign()
	If the plot is not revealed, stores sign for later display.
	"""
	BugUtil.debug("EventSigns.addSign(pPlot = %s, ePlayer = %s, szCaption = %s)" % (str(pPlot), str(ePlayer), str(szCaption)))
	pPlayer = gc.getPlayer(ePlayer)

	if not pPlot or pPlot.isNone():
		BugUtil.warn("EventSigns.addSign was passed an invalid plot: %s" % (str(pPlot)))
		return False
	if not pPlayer or pPlayer.isNone():
		BugUtil.warn("EventSigns.addSign was passed an invalid player id: %s" % (str(ePlayer)))
		return False
	
	eTeam = pPlayer.getTeam()
	if pPlot.isRevealed(eTeam, False):
		BugUtil.debug("EventSigns.addSign(): Plot revealed, adding sign.")
		engine.addSign(pPlot, ePlayer, szCaption)
	else:
		BugUtil.debug("EventSigns.addSign(): Plot NOT revealed, storing sign.")
		storeSign(pPlot, ePlayer, szCaption)
	return True

def storeSign (pPlot, ePlayer, szCaption):
	""" Stores sign data in PlotCaptions structure. """
	BugUtil.debug("EventSigns.storeSign(pPlot = %s, ePlayer = %s, szCaption = %s)" % (str(pPlot), str(ePlayer), str(szCaption)))
	szKey = getKey(pPlot)
	if not szKey:
		BugUtil.warn("EventSigns.storeSign() could not determine valid keyname for Plot %s." % (pPlot))
		return False
	if not szKey in gPlotCaptions:
		gPlotCaptions[szKey] = PlotCaptions(pPlot)
	gPlotCaptions[szKey].setCaption(ePlayer, szCaption)
	BugUtil.debug("EventSigns.storeSign(): Sign successfully stored to gPlotCaptions['%s']." % (szKey))

def hasSign (pPlot, ePlayer):
	""" Do we have sign data for given player in PlotCaptions structure? """
	#BugUtil.debug("EventSigns.hasSign(pPlot = %s, ePlayer = %s)" % (str(pPlot), str(ePlayer)))
	szKey = getKey(pPlot)
	if not szKey:
		BugUtil.warn("EventSigns.hasSign() could not determine valid keyname for Plot %s." % (pPlot))
		return False
	if szKey in gPlotCaptions:
		return True
	return False

def displaySign (pPlot, ePlayer):
	""" Displays stored sign for given player at given plot and removes from storage. """
	#BugUtil.debug("EventSigns.displaySign(pPlot = %s, ePlayer = %s)" % (str(pPlot), str(ePlayer)))
	if hasSign(pPlot, ePlayer):
		szKey = getKey(pPlot)
		szCaption = gPlotCaptions[szKey].getCaption(ePlayer)
		if szCaption:
			engine.addSign(pPlot, ePlayer, szCaption)
		gPlotCaptions[szKey].removeCaption(ePlayer)
		# If that was the last caption stored, clean up after ourselves
		if gPlotCaptions[szKey].isEmpty():
			del gPlotCaptions[szKey]
		
def getKey (pPlot):
	""" Gets keyname used to access this plot object. """
	#BugUtil.debug("EventSigns.getKey(pPlot = %s)" % (str(pPlot)))
	szKey = None
	if pPlot and not pPlot.isNone():
		iX = pPlot.getX()
		iY = pPlot.getY()
		szKey = "%d,%d" % (iX, iY)
	return szKey

def initData ():
	""" Initialize the internal plot-caption data structure, clearing all previous data. """
	BugUtil.debug("EventSigns.initData() initializing gPlotCaptions")
	global gPlotCaptions
	gPlotCaptions = {}

def dump ():
	""" Outputs all Plot-caption data, 1 entry per line. """
	szText = "EventSigns.dump() dumping all plot captions:\n"
	for key in gPlotCaptions:
		szText = szText + "  %s\n" % (gPlotCaptions[key])
	BugUtil.debug(szText)

# The class that handles internal data management of the plot captions
class PlotCaptions:
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
		self.teamDict = {}

	def isEmpty(self):
		""" Check to see if object has any caption data. """
		return (len(self.teamDict) == 0)

	def getPlot(self):
		""" Returns plot object. """
		return map.plot(self.iX, self.iY)

	def setPlot(self, pPlot):
		""" Assigns plot object. """
		if pPlot and not pPlot.isNone():
			self.iX = pPlot.getX()
			self.iY = pPlot.getY()

	def getCaption(self, ePlayer):
		""" Returns Caption for a given player on this plot. """
		pPlayer = gc.getPlayer(ePlayer)
		szCaption = ""
		if pPlayer and not pPlayer.isNone():
			eTeam = pPlayer.getTeam()
			try:
				szCaption = self.teamDict[eTeam][ePlayer] 
			except:
				BugUtil.warn("EventSigns PlotCaptions.getCaption() failed to find a caption for Player %d at Plot (%d,%d)" % (ePlayer, self.iX, self.iY))
				szCaption = ""
		return szCaption

	def setCaption(self, ePlayer, szCaption):
		""" Sets Caption for a given player on this plot. """
		pPlayer = gc.getPlayer(ePlayer)
		if pPlayer and not pPlayer.isNone():
			eTeam = pPlayer.getTeam()
			if not eTeam in self.teamDict:
				self.teamDict[eTeam] = {}
			self.teamDict[eTeam][ePlayer] = szCaption
		else:
			BugUtil.warn("EventSigns PlotCaptions.setCaption() was passed an invalid Player ID %s at Plot (%d,%d)" % (str(ePlayer), self.iX, self.iY))

	def removeCaption(self, ePlayer):
		""" Removes Caption for a given player on this plot. """
		pPlayer = gc.getPlayer(ePlayer)
		szCaption = ""
		if pPlayer and not pPlayer.isNone():
			eTeam = pPlayer.getTeam()
			try:
				del self.teamDict[eTeam][ePlayer] 
			except:
				BugUtil.warn("EventSigns PlotCaptions.removeCaption() failed to find a caption for Player %d at Plot (%d,%d)" % (ePlayer, self.iX, self.iY))
			if len(self.teamDict[eTeam]) == 0:
				del self.teamDict[eTeam]

	def __str__ (self):
		""" String representation of class instance. """
		return "PlotCaptions { iX=%d, iY=%d, teamDict=%s }" % (self.iX, self.iY, str(self.teamDict))

class EventSignsEventHandler:
	def __init__(self, eventManager):
		BugUtil.debug("EventSigns EventSignsEventHandler.__init__(). Resetting data and initing event manager.")
		initData()
		## Init event handlers
		eventManager.addEventHandler("GameStart", self.onGameStart)
		eventManager.addEventHandler("OnLoad", self.onLoadGame)
		eventManager.addEventHandler("OnPreSave", self.onPreSave)
		eventManager.addEventHandler("plotRevealed", self.onPlotRevealed)

	def onGameStart(self, argsList):
		""" Called when a new game is started """
		#BugUtil.debug("EventSignsEventHandler.onGameStart()")
		initData()

	def onLoadGame(self, argsList):
		""" Called when a game is loaded """
		BugUtil.debug("EventSignsEventHandler.onLoadGame()")
		if EventSignsOpt.isEnabled():
			data = SdToolKit.sdGetGlobal(SD_MOD_ID, SD_VAR_ID)
			if (data):
				global gPlotCaptions
				gPlotCaptions = data
				SdToolKit.sdSetGlobal(SD_MOD_ID, SD_VAR_ID, None)
				BugUtil.debug("Data Loaded:")
				dump()
			else:
				BugUtil.debug("No saved data. Initializing new data.")
				initData()

	def onPreSave(self, argsList):
		""" Called before a game is actually saved """
		#BugUtil.debug("EventSignsEventHandler.onPreSave()")
		if EventSignsOpt.isEnabled():
			if (gPlotCaptions):
				SdToolKit.sdSetGlobal(SD_MOD_ID, SD_VAR_ID, gPlotCaptions)
				#BugUtil.debug("Data Saved to sdtoolkit")
				#dump()

	def onPlotRevealed(self, argsList):
		""" Called when plot is revealed to team. """
		(pPlot, eTeam) = argsList
		#BugUtil.debug("EventSignsEventHandler.onPlotRevealed(pPlot = %s, eTeam = %s)" % (str(pPlot), str(eTeam)))
		if EventSignsOpt.isEnabled():
			if (gPlotCaptions):
				for ePlayer in range(gc.getMAX_PLAYERS()):
					pPlayer = gc.getPlayer(ePlayer)
					if pPlayer.getTeam() == eTeam:
						displaySign(pPlot, ePlayer)
