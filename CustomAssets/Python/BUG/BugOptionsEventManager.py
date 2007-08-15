## BugOptionsEventManager
## Displays BUG Mod Options Screen in response to CTRL-ALT-O.
## BUG Mod - Copyright 2007

from CvPythonExtensions import *
#import CvUtil
import CvScreensInterface

class BugOptionsEventManager:

	def __init__(self, eventManager):

		BugOptionsEvent(eventManager)

		# additions to self.Events
##		moreEvents = {
##			CvUtil.EventBugOptions : ('', self.__eventBugOptionsApply,  self.__eventBugOptionsBegin),
##		}
##		eventManager.Events.update(moreEvents)

##	def __eventBugOptionsBegin(self, argsList):
##		return 1
##
##	def __eventBugOptionsApply(self, playerID, userData, popupReturn):
##		return 1

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
			"Check if CTRL-ALT-O was hit"
			if (theKey == int(InputTypes.KB_O) and self.eventMgr.bAlt and self.eventMgr.bCtrl):
				CvScreensInterface.showBugOptionsScreen()
				return 1

		return 0
