## Ruff Mod Options
## Displays mod and civ options screens in response to keystrokes.
##-------------------------------------------------------------------
## Reorganized to work via CvCustomEventManager
## using Civ4lerts as template.
## CvCustomEventManager & Civ4lerts by Gillmer J. Derge
##-------------------------------------------------------------------

from CvPythonExtensions import *
import CvUtil
import CvScreensInterface

class RuffOptionsEventManager:

	def __init__(self, eventManager):

		RuffOptionsEvent(eventManager)

		# additions to self.Events
		moreEvents = {
			CvUtil.EventRuffOptions : ('', self.__eventRuffOptionsApply,  self.__eventRuffOptionsBegin),
		}
		eventManager.Events.update(moreEvents)

	def __eventRuffOptionsBegin(self, argsList):
		return 1

	def __eventRuffOptionsApply(self, playerID, userData, popupReturn):
		return 1

class AbstractRuffOptionsEvent(object):

	def __init__(self, eventManager, *args, **kwargs):
		super(AbstractRuffOptionsEvent, self).__init__(*args, **kwargs)

class RuffOptionsEvent(AbstractRuffOptionsEvent):

	def __init__(self, eventManager, *args, **kwargs):
		super(RuffOptionsEvent, self).__init__(eventManager, *args, **kwargs)

		eventManager.addEventHandler("kbdEvent", self.onKbdEvent)

		self.eventMgr = eventManager

	def onKbdEvent(self, argsList):
		eventType,key,mx,my,px,py = argsList
		if ( eventType == self.eventMgr.EventKeyDown ):
			theKey = int(key)
			'Check if ALT + J was hit == show dialog box and options'
			if (theKey == int(InputTypes.KB_J) and self.eventMgr.bAlt):
				CvScreensInterface.showRuffModScreen()
				return 1

			if (theKey == int(InputTypes.KB_K) and self.eventMgr.bAlt):
				CvScreensInterface.showOptionsScreen()
				return 1

		return 0
