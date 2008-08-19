## BugEventManager
##
## Extended version of CvCustomEventManager by Gillmer J. Derge.
##
## Changes:
##
## * New methods
##   - addEvent(eventType, handler) 
##       Extend the core Civ4 event list
##   - fireEvent(eventType, args...) 
##       Fire an event from Python
##   - reportEvent(eventType, argsList)
##       Print a debug message with the event and its arguments
##       Set self.bReport to True in __init__ to enable
##
## * New events
##   - BeginActivePlayerTurn
##       called from CvMainInterface.updateScreen()
##   - LanguageChanged 
##       called from CvOptionsScreenCallbackInterface.handleLanguagesDropdownBoxInput()
##
## * Calls BugInit.init() once before "OnLoad" or "GameStart" events are handled
##   because CyGlobalContext is not ready during "Init" event.
##
## Copyright (c) 2008 The BUG Mod.
##
## Author: EmperorFool

from CvPythonExtensions import *
import CvEventManager
import BugUtil

gc = CyGlobalContext()

class BugEventManager(CvEventManager.CvEventManager):

	"""
	Extends the standard event manager by adding support for multiple
	handlers for each event.
	
	Instead of modifying this file as you would have done with CvCustomEventManager,
	you should add the names of your event managers to the file "Config/init.xml"
	in the order you want their events to fire.
	
	Methods exist for both adding and removing event handlers.  A set method 
	also exists to override the default handlers.  Clients should not depend 
	on event handlers being called in a particular order.
	
	Note that the naming conventions for the event type strings vary from event
	to event.  Some use initial capitalization, some do not; some eliminate the
	"on..." prefix used in the event handler function name, some do not.  Look
	at the unmodified CvEventManager.py source code to determine the correct
	name for a particular event.
	
	Take care with event handlers that also extend CvEventManager.  Since
	this event manager handles invocation of the base class handler function,
	additional handlers should not also call the base class function themselves.
	
	"""

	def __init__(self):
		CvEventManager.CvEventManager.__init__(self)
		
		self.bReport = True
		self.bDbg = False
		self.bMultiPlayer = False
		self.bAllowCheats = False
		
		# add new core events
		self.addEvent("PreGameStart", self.onPreGameStart)
		self.addEvent("BeginActivePlayerTurn", self.onBeginActivePlayerTurn)
		self.addEvent("LanguageChanged", self.onLanguageChanged)
		
		# map the initial EventHandlerMap values into the new data structure
		for eventType, eventHandler in self.EventHandlerMap.iteritems():
			self.setEventHandler(eventType, eventHandler)

	def checkEventType(self, eventType):
		"""Enforces that eventType is defined.
		
		Raises ConfigError if the eventType is not valid.
		"""
		if eventType not in self.EventHandlerMap:
			raise BugUtil.ConfigError("Event '%s' is not valid" % eventType)

	def addEvent(self, eventType, eventHandler):
		"""Creates a new event type by adding a handler to CvEventManager's map.
		
		Overwrites any existing handler with a warning.
		"""
		if eventType in self.EventHandlerMap:
			BugUtil.debug("WARN: event '%s' is already defined; overriding default handler %r" 
						  % (eventType, self.EventHandlerMap[eventType]))
		self.EventHandlerMap[eventType] = eventHandler

	def addEventHandler(self, eventType, eventHandler):
		"""Adds a handler for the given event type.
		
		A list of supported event types can be found in the initialization 
		of EventHandlerMap in the CvEventManager class.  It is an error if 
		the given handler is not found in the list of installed handlers.
		
		Throws ConfigError if the eventType is not valid.

		"""
		self.checkEventType(eventType)
		self.EventHandlerMap[eventType].append(eventHandler)

	def removeEventHandler(self, eventType, eventHandler):
		"""Removes a handler for the given event type.
		
		A list of supported event types can be found in the initialization 
		of EventHandlerMap in the CvEventManager class.  It is an error if 
		the given handler is not found in the list of installed handlers.
		
		Throws ConfigError if the eventType is not valid.

		"""
		self.checkEventType(eventType)
		self.EventHandlerMap[eventType].remove(eventHandler)
	
	def setEventHandler(self, eventType, eventHandler):
		"""Removes all previously installed event handlers for the given 
		event type and installs a new handler.
		
		A list of supported event types can be found in the initialization 
		of EventHandlerMap in the CvEventManager class.  This method is 
		primarily useful for overriding, rather than extending, the default 
		event handler functionality.
		
		Throws ConfigError if the eventType is not valid.

		"""
		self.checkEventType(eventType)
		self.EventHandlerMap[eventType] = [eventHandler]
	
	def setPopupHandler(self, eventType, popupHandler):
		"""Removes all previously installed popup handlers for the given 
		event type and installs a new handler.
		
		The eventType should be an integer.  It must be unique with respect
		to the integers assigned to built in events.  The popupHandler should
		be a list made up of (name, beginFunction, applyFunction).  The name
		is used in debugging output.  The begin and apply functions are invoked
		by beginEvent and applyEvent, respectively, to manage a popup dialog
		in response to the event.

		"""
		self.Events[eventType] = popupHandler
	
	
	def fireEvent(self, eventType, *args):
		"""Fires the given event passing in all args as a list."""
		argsList = [eventType]
		argsList.extend(args)
		argsList.extend((self.bDbg, self.bMultiPlayer, False, False, False, self.bAllowCheats))
		self.handleEvent(argsList)

	def handleEvent(self, argsList):
		"""Handles events by calling all installed handlers."""
		self.origArgsList = argsList
		flagsIndex = len(argsList) - 6
		self.bDbg, self.bMultiPlayer, self.bAlt, self.bCtrl, self.bShift, self.bAllowCheats = argsList[flagsIndex:]
		eventType = argsList[0]
		if self.bReport:
			self.reportEvent(eventType, argsList[1:flagsIndex])
		return EVENT_FUNCTION_MAP.get(eventType, BugEventManager._handleDefaultEvent)(self, eventType, argsList[1:])

	def reportEvent(self, eventType, argsList):
		if eventType != "gameUpdate":
			if argsList:
				BugUtil.debug("Event: %s - %r" % (eventType, argsList))
			else:
				BugUtil.debug("Event: %s" % eventType)
			BugUtil.debug("BUG: COLOR_BLACK ID = %d" % gc.getInfoTypeForString("COLOR_BLACK"))

	def _handleDefaultEvent(self, eventType, argsList):
		if self.EventHandlerMap.has_key(eventType):
			for eventHandler in self.EventHandlerMap[eventType]:
				# the last 6 arguments are for internal use by handleEvent
				eventHandler(argsList[:len(argsList) - 6])

	def _handleConsumableEvent(self, eventType, argsList):
		"""Handles events that can be consumed by the handlers, such as
		keyboard or mouse events.
		
		If a handler returns non-zero, processing is terminated, and no 
		subsequent handlers are invoked.

		"""
		if self.EventHandlerMap.has_key(eventType):
			for eventHandler in self.EventHandlerMap[eventType]:
				# the last 6 arguments are for internal use by handleEvent
				result = eventHandler(argsList[:len(argsList) - 6])
				if (result > 0):
					return result
		return 0

	# TODO: this probably needs to be more complex
	def _handleOnSaveEvent(self, eventType, argsList):
		"""Handles OnSave events by concatenating the results obtained
		from each handler to form an overall consolidated save string.
		"""
		result = ""
		if self.EventHandlerMap.has_key(eventType):
			for eventHandler in self.EventHandlerMap[eventType]:
				# the last 6 arguments are for internal use by handleEvent
				result = result + eventHandler(argsList[:len(argsList) - 6])
		return result

	def _handleInitBugEvent(self, eventType, argsList):
		"""Initializes BUG before handling event normally."""
		initBug()
		return self._handleDefaultEvent(eventType, argsList)
	
	
	def onPreGameStart(self, argsList):
		"""Fired from CvAppInterface.preGameStart()."""
		pass

	def onBeginActivePlayerTurn(self, argsList):
		"""Called when the active player can start their turn."""
		ePlayer, iGameTurn = argsList
	
	def onLanguageChanged(self, argsList):
		"""Called when the user changes their language selection."""
		iLanguage = argsList[0]


EVENT_FUNCTION_MAP = {
	"kbdEvent": BugEventManager._handleConsumableEvent,
	"mouseEvent": BugEventManager._handleConsumableEvent,
	"OnSave": BugEventManager._handleOnSaveEvent,
	#"OnLoad": BugEventManager._handleInitBugEvent,
	#"PreGameStart": BugEventManager._handleInitBugEvent,
	#"GameStart": BugEventManager._handleInitBugEvent,
	"windowActivation": BugEventManager._handleInitBugEvent,
}


g_initDone = False
def initBug():
	"""Called when Civ starts or loads a game."""
	global g_initDone
	if not g_initDone:
		import BugInit
		BugInit.init()
		g_initDone = True
