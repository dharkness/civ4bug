##-------------------------------------------------------------------
## Modified from reminder by eotinb
## by Ruff and EF
##-------------------------------------------------------------------
## Reorganized to work via CvCustomEventManager
## using Civ4lerts as template.
## CvCustomEventManager & Civ4lerts by Gillmer J. Derge
##-------------------------------------------------------------------
## EF: Turned into a real queue, can be disabled
##-------------------------------------------------------------------

from CvPythonExtensions import *
import CvUtil
import Popup as PyPopup
import BugAlertsOptions

gc = CyGlobalContext()
BugAlerts = BugAlertsOptions.getOptions()

class ReminderEventManager:

	def __init__(self, eventManager):

		ReminderEvent(eventManager, self)

		self.reminders = ReminderQueue()

		# additions to self.Events
		moreEvents = {
			CvUtil.EventReminderStore  : ('', self.__eventReminderStoreApply,  self.__eventReminderStoreBegin),
			CvUtil.EventReminderRecall : ('', self.__eventReminderRecallApply, self.__eventReminderRecallBegin),
		}
		eventManager.Events.update(moreEvents)

	def __eventReminderStoreBegin(self, argsList):
		popup = PyPopup.PyPopup(CvUtil.EventReminderStore, EventContextTypes.EVENTCONTEXT_SELF)
		popup.setHeaderString("Enter number of turns until reminder goes off and reminder text")
		popup.createSpinBox(0, "", 0, 1, 100, 0)
		popup.createEditBox("", 1)
		popup.addButton("Ok")
		popup.addButton("Cancel")
		popup.launch(False, PopupStates.POPUPSTATE_IMMEDIATE)

	def __eventReminderStoreApply(self, playerID, userData, popupReturn):
		if (popupReturn.getButtonClicked() != 1):
			reminderTurn = popupReturn.getSpinnerWidgetValue(0) + gc.getGame().getGameTurn()
			reminderText = popupReturn.getEditBoxString(1)
			reminder = Reminder(reminderTurn, reminderText)
			self.reminders.push(reminder)

	def __eventReminderRecallBegin(self, argsList):
		thisTurn = gc.getGame().getGameTurn() + 1 # remove +1 ?
		
		while (not self.reminders.isEmpty()):
			nextTurn = self.reminders.nextTurn()
			if (nextTurn > thisTurn):
				break
			elif (nextTurn < thisTurn):
				# invalid (lost) reminder
				self.reminders.pop()
			else:
				message = self.reminders.pop().message
				CyInterface().addMessage(CyGame().getActivePlayer(), True, 10, message, None, 2, None, ColorTypes(8), 0, 0, False, False)
				
				popup = PyPopup.PyPopup(CvUtil.EventReminderRecall, EventContextTypes.EVENTCONTEXT_SELF)
				popup.setHeaderString("Reminder!")
				popup.setBodyString(message)
				popup.launch()

	def __eventReminderRecallApply(self, playerID, userData, popupReturn):
		message = "eventReminderRecallApply"

	def clearReminders(self):
		self.reminders.clear()


class AbstractReminderEvent(object):

	def __init__(self, eventManager, *args, **kwargs):
		super(AbstractReminderEvent, self).__init__(*args, **kwargs)

class ReminderEvent(AbstractReminderEvent):

	def __init__(self, eventManager, reminderManager, *args, **kwargs):
		super(ReminderEvent, self).__init__(eventManager, *args, **kwargs)

		eventManager.addEventHandler("kbdEvent", self.onKbdEvent)
		eventManager.addEventHandler("BeginPlayerTurn", self.onBeginPlayerTurn)
		eventManager.addEventHandler("GameStart", self.onGameStart)
		eventManager.addEventHandler("OnLoad", self.onLoadGame)

		self.eventMgr = eventManager
		self.reminderManager = reminderManager

	def onKbdEvent(self, argsList):
		eventType,key,mx,my,px,py = argsList
		if ( eventType == self.eventMgr.EventKeyDown ):
			theKey=int(key)
			'Check if ALT + M was hit == show dialog box to set up reminder'
			if (theKey == int(InputTypes.KB_M) and self.eventMgr.bAlt):
				if (BugAlerts.isShowReminders()):
					self.eventMgr.beginEvent(CvUtil.EventReminderStore)
					return 1
		return 0

	def onBeginPlayerTurn(self, argsList):
		'Called at the beginning of a players turn'
		iGameTurn, iPlayer = argsList

		if (gc.getPlayer(iPlayer).isHuman()):
			if (BugAlerts.isShowReminders()):
				self.eventMgr.beginEvent(CvUtil.EventReminderRecall)
				return 1

	def onGameStart(self, argsList):
		'Called when a new game is started'
		self.reminderManager.clearReminders()
		return 1

	def onLoadGame(self, argsList):
		'Called when a game is loaded' # would be nice to save/load events with game
		self.reminderManager.clearReminders()
		return 1

class Reminder(object):

	def __init__(self, turn, message):
		self.turn = turn
		self.message = message

class ReminderQueue(object):

	def __init__(self):
		self.queue = []

	def clear(self):
		self.queue = []

	def isEmpty(self):
		return len(self.queue) == 0

	def nextTurn(self):
		if (self.isEmpty()):
			return -1
		return self.queue[0].turn

	def push(self, reminder):
		for i, r in enumerate(self.queue):
			if (reminder.turn < r.turn):
				self.queue.insert(i, reminder)
				return
		self.queue.append(reminder)

	def pop(self):
		if (self.isEmpty()):
			return None
		return self.queue.pop(0)
