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
import CvMainInterface
import CvUtil
import Popup as PyPopup
import BugCore
import BugUtil
import SdToolKit
import autolog

SD_MOD_ID = "Reminders"
SD_QUEUE_ID = "queue"

STORE_EVENT_ID = CvUtil.getNewEventID("Reminder.Store")
RECALL_EVENT_ID = CvUtil.getNewEventID("Reminder.Recall")
RECALL_AGAIN_EVENT_ID = CvUtil.getNewEventID("Reminder.RecallAgain")

gc = CyGlobalContext()

ReminderOpt = BugCore.game.Reminder
g_eventMgr = None
g_autolog = None

# Used to display flashing end-of-turn text
g_turnReminderTexts = None

def createReminder(argsList):
	g_eventMgr.beginEvent(STORE_EVENT_ID)

class ReminderEventManager:

	def __init__(self, eventManager):

		global g_autolog
		g_autolog = autolog.autologInstance()
		
		global g_eventMgr
		g_eventMgr = eventManager
		ReminderEvent(eventManager, self)

		self.reminders = ReminderQueue()
		self.endOfTurnReminders = ReminderQueue()
		self.reminder = None

		# additions to self.Events
		moreEvents = {
			STORE_EVENT_ID       : ('', self.__eventReminderStoreApply,  self.__eventReminderStoreBegin),
			RECALL_EVENT_ID      : ('', self.__eventReminderRecallApply, self.__eventReminderRecallBegin),
			RECALL_AGAIN_EVENT_ID : ('', self.__eventReminderRecallAgainApply, self.__eventReminderRecallAgainBegin),
		}
		eventManager.Events.update(moreEvents)

	def __eventReminderStoreBegin(self, argsList):
		header = BugUtil.getPlainText("TXT_KEY_REMINDER_HEADER")
		prompt = BugUtil.getPlainText("TXT_KEY_REMINDER_PROMPT")
		ok = BugUtil.getPlainText("TXT_KEY_MAIN_MENU_OK")
		cancel = BugUtil.getPlainText("TXT_KEY_POPUP_CANCEL")
		popup = PyPopup.PyPopup(STORE_EVENT_ID, EventContextTypes.EVENTCONTEXT_SELF)
		popup.setHeaderString(header)
		popup.setBodyString(prompt)
		popup.createSpinBox(0, "", 1, 1, 1500, 0)
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
			if (g_autolog.isLogging() and ReminderOpt.isAutolog()):
				g_autolog.writeLog("Reminder: On Turn %d, %s" % (reminderTurn, reminderText))

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
		global g_turnReminderTexts
		thisTurn = gc.getGame().getGameTurn()
		if (endOfTurn):
			queue = self.endOfTurnReminders
			prompt = BugUtil.getPlainText("TXT_KEY_REMIND_NEXT_TURN_PROMPT")
			eventId = RECALL_AGAIN_EVENT_ID
		else:
			g_turnReminderTexts = ""
			queue = self.reminders
			# endTurnReady isn't firing :(
			prompt = BugUtil.getPlainText("TXT_KEY_REMIND_END_TURN_PROMPT")
			eventId = RECALL_EVENT_ID
#			prompt = BugUtil.getPlainText("TXT_KEY_REMIND_NEXT_TURN_PROMPT")
#			eventId = RECALL_AGAIN_EVENT_ID
		yes = BugUtil.getPlainText("TXT_KEY_POPUP_YES")
		no = BugUtil.getPlainText("TXT_KEY_POPUP_NO")
		while (not queue.isEmpty()):
			nextTurn = queue.nextTurn()
			if (nextTurn > thisTurn):
				break
			elif (nextTurn < thisTurn):
				# invalid (lost) reminder
				queue.pop()
			else:
				self.reminder = queue.pop()
				if (g_autolog.isLogging() and ReminderOpt.isAutolog()):
					g_autolog.writeLog("Reminder: %s" % self.reminder.message)
				if (not endOfTurn):
					if (g_turnReminderTexts):
						g_turnReminderTexts += ", "
					g_turnReminderTexts += self.reminder.message
				if (ReminderOpt.isShowMessage()):
					CyInterface().addMessage(CyGame().getActivePlayer(), True, 10, self.reminder.message, 
											 None, 0, None, ColorTypes(8), 0, 0, False, False)
				if (ReminderOpt.isShowPopup()):
					popup = PyPopup.PyPopup(eventId, EventContextTypes.EVENTCONTEXT_SELF)
					popup.setHeaderString(self.reminder.message)
					popup.setBodyString(prompt)
					popup.addButton(yes)
					popup.addButton(no)
					popup.launch(False)

	def clearReminders(self):
		self.reminders.clear()
		self.endOfTurnReminders.clear()
		global g_turnReminderTexts
		g_turnReminderTexts = None
	
	def setReminders(self, queue):
		self.reminders = queue


class ReminderEvent:

	def __init__(self, eventManager, reminderManager):
		eventManager.addEventHandler("BeginActivePlayerTurn", self.onBeginActivePlayerTurn)
		eventManager.addEventHandler("endTurnReady", self.onEndTurnReady)
		eventManager.addEventHandler("GameStart", self.onGameStart)
		eventManager.addEventHandler("OnLoad", self.onLoadGame)
		eventManager.addEventHandler("PythonReloaded", self.onLoadGame)
		eventManager.addEventHandler("OnPreSave", self.onPreSave)
		eventManager.addEventHandler("SwitchHotSeatPlayer", self.onSwitchHotSeatPlayer)
		
		self.reminderManager = reminderManager
	
	def createReminder(self):
		g_eventMgr.beginEvent(STORE_EVENT_ID)
	
	def onSwitchHotSeatPlayer(self, argsList):
		"Clears the end turn text so hot seat players don't see each others reminders."
		ePlayer = argsList[0]
		
		global g_turnReminderTexts
		g_turnReminderTexts = None
		CvMainInterface.g_mainInterface.resetEndTurnObjects()

	def onBeginActivePlayerTurn(self, argsList):
		"Called at the start of the active player's turn."
		iGameTurn = argsList[0]

		global g_turnReminderTexts
		g_turnReminderTexts = None
		if (ReminderOpt.isEnabled()):
			g_eventMgr.beginEvent(RECALL_EVENT_ID)

	def onEndTurnReady(self, argsList):
		iGameTurn = argsList[0]
		
		if (ReminderOpt.isEnabled()):
			g_eventMgr.beginEvent(RECALL_AGAIN_EVENT_ID)

	def onGameStart(self, argsList):
		'Called when a new game is started'
		self.reminderManager.clearReminders()

	def onLoadGame(self, argsList):
		'Called when a game is loaded'
		self.reminderManager.clearReminders()
		queue = SdToolKit.sdGetGlobal(SD_MOD_ID, SD_QUEUE_ID)
		if (queue):
			self.reminderManager.setReminders(queue)

	def onPreSave(self, argsList):
		"Called before a game is actually saved"
		if (not self.reminderManager.reminders.isEmpty()):
			SdToolKit.sdSetGlobal(SD_MOD_ID, SD_QUEUE_ID, self.reminderManager.reminders)


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
