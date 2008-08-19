## BugOptionsEventManager
## Displays BUG Mod Options Screen in response to Alt + Ctrl + O and Alt + J.
## BUG Mod - Copyright 2007

from CvPythonExtensions import *
import CvScreensInterface

class BugOptionsEventManager:

	def __init__(self, eventManager):

		BugOptionsEvent(eventManager)

class AbstractBugOptionsEvent(object):

	def __init__(self, eventManager, *args, **kwargs):
		super(AbstractBugOptionsEvent, self).__init__(*args, **kwargs)

class BugOptionsEvent(AbstractBugOptionsEvent):

	def __init__(self, eventManager, *args, **kwargs):
		super(BugOptionsEvent, self).__init__(eventManager, *args, **kwargs)

		eventManager.addEventHandler("kbdEvent", self.onKbdEvent)

		self.eventMgr = eventManager

	def onKbdEvent(self, argsList):
		eventType, key, mx, my, px, py = argsList
		if ( eventType == self.eventMgr.EventKeyDown ):
			theKey = int(key)
			# Check if Alt + Ctrl + O or ALT-J were hit (the latter for Ruff's users).
			if ((theKey == int(InputTypes.KB_O) and self.eventMgr.bAlt and self.eventMgr.bCtrl)
			or (theKey == int(InputTypes.KB_J) and self.eventMgr.bAlt)):
				CvScreensInterface.showBugOptionsScreen()
				return 1
		return 0
