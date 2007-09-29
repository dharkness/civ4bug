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
import SdToolKit

import BugAlertsOptions
BugAlerts = BugAlertsOptions.getOptions()

gc = CyGlobalContext()
localText = CyTranslator()

SD_MOD_ID = "Reminders"
SD_QUEUE_ID = "queue"

class ReminderEventManager:

	def __init__(self, eventManager):

		ReminderEvent(eventManager, self)

		self.reminders = ReminderQueue()
		self.endOfTurnReminders = ReminderQueue()
		self.reminder = None

		# additions to self.Events
		moreEvents = {
			CvUtil.EventReminderStore       : ('', self.__eventReminderStoreApply,  self.__eventReminderStoreBegin),
			CvUtil.EventReminderRecall      : ('', self.__eventReminderRecallApply, self.__eventReminderRecallBegin),
			CvUtil.EventReminderRecallAgain : ('', self.__eventReminderRecallAgainApply, self.__eventReminderRecallAgainBegin),
		}
		eventManager.Events.update(moreEvents)

	def __eventReminderStoreBegin(self, argsList):
		header = localText.getText("TXT_KEY_REMINDER_HEADER", ())
		prompt = localText.getText("TXT_KEY_REMINDER_PROMPT", ())
		ok = localText.getText("TXT_KEY_MAIN_MENU_OK", ())
		cancel = localText.getText("TXT_KEY_POPUP_CANCEL", ())
		popup = PyPopup.PyPopup(CvUtil.EventReminderStore, EventContextTypes.EVENTCONTEXT_SELF)
		popup.setHeaderString(header)
		popup.setBodyString(prompt)
		popup.createSpinBox(0, "", 1, 1, 100, 0)
		popup.createEditBox("", 1)
		popup.addButton(ok)
		popup.addButton(cancel)
		popup.launch(False, PopupStates.POPUPSTATE_IMMEDIATE)

	def __eventReminderStoreApply(self, playerID, userData, popupReturn):
		if (popupReturn.getButtonClicked() != 1):
			reminderTurn = popupReturn.getSpinnerWidgetValue(0) + gc.getGame().getGameTurn()
			reminderText = popupReturn.getEditBoxString(1)
			reminder = Reminder(reminderTurn, reminderText)
			self.reminders.push(reminder)

	def __eventReminderRecallBegin(self, argsList):
		self.showReminders(False)

	def __eventReminderRecallApply(self, playerID, userData, popupReturn):
		if (popupReturn.getButtonClicked() != 1):
			if (self.reminder):
				self.endOfTurnReminders.push(self.reminder)
				self.reminder = None

	def __eventReminderRecallAgainBegin(self, argsList):
		self.showReminders(True)

	def __eventReminderRecallAgainApply(self, playerID, userData, popupReturn):
		if (popupReturn.getButtonClicked() != 1):
			if (self.reminder):
				# Put it back into the queue for next turn
				self.reminder.turn += 1
				self.reminders.push(self.reminder)
				self.reminder = None

	def showReminders(self, endOfTurn):
		thisTurn = gc.getGame().getGameTurn() + 1
		if (endOfTurn):
			queue = self.endOfTurnReminders
			prompt = localText.getText("TXT_KEY_REMIND_NEXT_TURN_PROMPT", ())
			eventId = CvUtil.EventReminderRecallAgain
		else:
			queue = self.reminders
			# endTurnReady isn't firing :(
#			prompt = localText.getText("TXT_KEY_REMIND_END_TURN_PROMPT", ())
#			eventId = CvUtil.EventReminderRecall
			prompt = localText.getText("TXT_KEY_REMIND_NEXT_TURN_PROMPT", ())
			eventId = CvUtil.EventReminderRecallAgain
		yes = localText.getText("TXT_KEY_POPUP_YES", ())
		no = localText.getText("TXT_KEY_POPUP_NO", ())
		while (not queue.isEmpty()):
			nextTurn = queue.nextTurn()
			if (nextTurn > thisTurn):
				break
			elif (nextTurn < thisTurn):
				# invalid (lost) reminder
				self.reminders.pop()
			else:
				self.reminder = queue.pop()
				if (BugAlerts.isShowRemindersLog()):
					CyInterface().addMessage(CyGame().getActivePlayer(), True, 10, self.reminder.message, 
											 None, 0, None, ColorTypes(8), 0, 0, False, False)
				if (BugAlerts.isShowRemindersPopup()):
					popup = PyPopup.PyPopup(eventId, EventContextTypes.EVENTCONTEXT_SELF)
					popup.setHeaderString(self.reminder.message)
					popup.setBodyString(prompt)
					popup.addButton(yes)
					popup.addButton(no)
					popup.launch(False)

	def clearReminders(self):
		self.reminders.clear()
		self.endOfTurnReminders.clear()
	
	def setReminders(self, queue):
		self.reminders = queue


class AbstractReminderEvent(object):

	def __init__(self, eventManager, *args, **kwargs):
		super(AbstractReminderEvent, self).__init__(*args, **kwargs)

class ReminderEvent(AbstractReminderEvent):

	def __init__(self, eventManager, reminderManager, *args, **kwargs):
		super(ReminderEvent, self).__init__(eventManager, *args, **kwargs)

		eventManager.addEventHandler("kbdEvent", self.onKbdEvent)
		eventManager.addEventHandler("BeginPlayerTurn", self.onBeginPlayerTurn)
		eventManager.addEventHandler("endTurnReady", self.onEndTurnReady)
		eventManager.addEventHandler("GameStart", self.onGameStart)
		eventManager.addEventHandler("OnLoad", self.onLoadGame)
		eventManager.addEventHandler("OnPreSave", self.onPreSave)

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
#				return 1

	def onEndTurnReady(self, argsList):
		iGameTurn = argsList[0]
		
		if (gc.getPlayer(iPlayer).isHuman()):
			if (BugAlerts.isShowReminders()):
				self.eventMgr.beginEvent(CvUtil.EventReminderRecallAgain)
#				return 1

	def onGameStart(self, argsList):
		'Called when a new game is started'
		self.reminderManager.clearReminders()
#		return 1

	def onLoadGame(self, argsList):
		'Called when a game is loaded'
		self.reminderManager.clearReminders()
		queue = SdToolKit.sdGetGlobal(SD_MOD_ID, SD_QUEUE_ID)
		if (queue):
			self.reminderManager.setReminders(queue)
			SdToolKit.sdSetGlobal(SD_MOD_ID, SD_QUEUE_ID, None)
#		return 1

	def onPreSave(self, argsList):
		"Called before a game is actually saved"
		if (not self.reminderManager.reminders.isEMpty()):
			SdToolKit.sdSetGlobal(SD_MOD_ID, SD_QUEUE_ID, self.reminderManager.reminders)
#		return 1


class Reminder(object):

	def __init__(self, turn, message):
		self.turn = turn
		self.message = message


class ReminderQueue(object):

	def __init__(self):
		self.queue = []

	def clear(self):
		self.queue = []

	def size(self):
		return len(self.queue)

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
