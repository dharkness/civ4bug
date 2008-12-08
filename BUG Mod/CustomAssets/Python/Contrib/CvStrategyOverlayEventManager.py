###########################################
## StrategyOverlayEventManager.py
## Event manager for Strategy Overlay
## Customized from BugOptionsEventManager
## 10/20/2008
## Place in CustomAssets/Python/Contrib/ for bug mod use
###########################################

from CvPythonExtensions import *
import CvOverlayScreenUtils

class CvStrategyOverlayEventManager:
	"""
	Custom event manager for Strategy Overlay
	Adds a handler to check for a kepress and open the Strategy Overlay screen
	"""
	def __init__(self, eventManager):
		eventManager.addEventHandler("kbdEvent", self.onKbdEvent)
		self.eventMgr = eventManager

	def onKbdEvent(self, argsList):
		eventType, key, mx, my, px, py = argsList
		if ( eventType == self.eventMgr.EventKeyDown ):
			theKey = int(key)
			# Open overlay screen on alt-f10
			if ((theKey == int(InputTypes.KB_F10) and self.eventMgr.bAlt)):
				CvOverlayScreenUtils.showOverlayScreen()
				return 1
		return 0
