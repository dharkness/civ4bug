## BugEventManager
##
## Extended version of CvCustomEventManager by Gillmer J. Derge.
##
## Changes:
##
## * New public methods
##
##   - addEvent(eventType)
##       Extend the core Civ4 event list
##   - fireEvent(eventType, args...)
##       Fire an event from Python
##
## * Added force parameter to addEventHandler() [default False]
##   to call addEvent() before adding the handler.
##
## * New events
##
##   - BeginActivePlayerTurn
##       called from CvMainInterface.updateScreen()
##   - LanguageChanged 
##       called from CvOptionsScreenCallbackInterface.handleLanguagesDropdownBoxInput()
##   - PreGameStart
##       called from CvAppInterface.preGameStart()
##
## * Events and their arguments are optionally logged.
## * Added configure() to set the options.
##
## * Calls BugInit.init() once before "OnLoad" or "PreGameStart" events
##   are handled because CyGlobalContext is not ready during "Init" event.
##   Both must do it because "OnLoad" happens before "PreGameStart", but
##   the latter happens before "GameStart" (as expected).
##
## Copyright (c) 2008 The BUG Mod.
##
## Author: EmperorFool

from CvPythonExtensions import *
import CvEventManager
import BugUtil

DEFAULT_REPORT = False
DEFAULT_NOLOG_EVENTS = set((
	"gameUpdate",
))

gc = CyGlobalContext()
g_eventManager = None

class BugEventManager(CvEventManager.CvEventManager):

	"""
	Extends the standard event manager by adding support for multiple
	handlers for each event.
	
	Instead of modifying this file as you would have done with CvCustomEventManager,
	use the <event> and <events> tags in your mod's initialization XML file.
	
	Methods exist for both adding and removing event handlers.  A set method 
	also exists to override the default handlers.  Clients should not depend 
	on event handlers being called in a particular order, though they are
	called in the order in which they are added.
	
	Note that the naming conventions for the event type strings vary from event
	to event.  Some use initial capitalization, some do not; some eliminate the
	"on..." prefix used in the event handler function name, some do not.  Look
	at the unmodified CvEventManager.py source code to determine the correct
	name for a particular event.
	
	Take care with event handlers that also extend CvEventManager.  Since
	this event manager handles invocation of the base class handler function,
	additional handlers should not also call the base class function themselves.
	
	It's best *not* to extend CvEventManager or CvCustomEventManager. In fact,
	you are free to use module methods outside classes if you wish. 
	
	"""

	def __init__(self, logging=None, noLogEvents=None):
		CvEventManager.CvEventManager.__init__(self)
		
		global g_eventManager
		if g_eventManager is not None:
			raise ConfigError("BugEventManager already created")
		g_eventManager = self
		
		if logging is None:
			self.setLogging(DEFAULT_REPORT)
		else:
			self.setLogging(logging)
		if noLogEvents is None:
			self.setNoLogEvents(DEFAULT_NOLOG_EVENTS)
		else:
			self.setNoLogEvents(noLogEvents)
		
		self.bDbg = False
		self.bMultiPlayer = False
		self.bAllowCheats = False
		
		# add new core events
		self.addEvent("PreGameStart")
		self.addEvent("BeginActivePlayerTurn")
		self.addEvent("LanguageChanged")
		
		# map the initial EventHandlerMap values into the new data structure
		for eventType, eventHandler in self.EventHandlerMap.iteritems():
			self.setEventHandler(eventType, eventHandler)
	
	def setLogging(self, logging):
		if logging is not None:
			self.logging = bool(logging)
	
	def setNoLogEvents(self, noLogEvents):
		if noLogEvents is not None:
			try:
				x = "update" in noLogEvents
			except:
				raise ConfigError("noLogEvents must be tuple, list or set")
			else:
				self.noLogEvents = noLogEvents

	def _checkEvent(self, eventType):
		"""Enforces that eventType is defined.
		
		Raises ConfigError if the eventType is undefined.
		"""
		if eventType not in self.EventHandlerMap:
			raise BugUtil.ConfigError("Event '%s' is undefined" % eventType)

	def addEvent(self, eventType):
		"""Creates a new event type by adding it to CvEventManager's map.
		
		Prints a warning if eventType is already defined but does not
		alter its default handler.
		"""
		if eventType in self.EventHandlerMap:
			BugUtil.debug("WARN: event '%s' is already defined" % eventType)
		else:
			self.EventHandlerMap[eventType] = None

	def addEventHandler(self, eventType, eventHandler, force=False):
		"""Adds a handler for the given event type.
		
		A list of supported event types can be found in the initialization 
		of EventHandlerMap in the CvEventManager class.  It is an error if 
		the given handler is not found in the list of installed handlers.
		
		Throws ConfigError if the eventType is undefined and force is False.

		"""
		if force:
			self.addEvent(eventType)
		else:
			self._checkEvent(eventType)
		self.EventHandlerMap[eventType].append(eventHandler)

	def removeEventHandler(self, eventType, eventHandler):
		"""Removes a handler for the given event type.
		
		A list of supported event types can be found in the initialization 
		of EventHandlerMap in the CvEventManager class.  It is an error if 
		the given handler is not found in the list of installed handlers.
		
		Throws ConfigError if the eventType is undefined.

		"""
		self._checkEvent(eventType)
		self.EventHandlerMap[eventType].remove(eventHandler)
	
	def setEventHandler(self, eventType, eventHandler, force=False):
		"""Removes all previously installed event handlers for the given 
		event type and installs a new handler.
		
		A list of supported event types can be found in the initialization 
		of EventHandlerMap in the CvEventManager class.  This method is 
		primarily useful for overriding, rather than extending, the default 
		event handler functionality.
		
		Throws ConfigError if the eventType is undefined and force is False.

		"""
		if force:
			self.addEvent(eventType)
		else:
			self._checkEvent(eventType)
		if eventHandler is not None:
			self.EventHandlerMap[eventType] = [eventHandler]
		else:
			self.EventHandlerMap[eventType] = []
	
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
		if self.logging:
			self._reportEvent(eventType, argsList[1:flagsIndex])
		return EVENT_FUNCTION_MAP.get(eventType, BugEventManager._handleDefaultEvent)(self, eventType, argsList[1:])

	def _reportEvent(self, eventType, argsList):
		if eventType not in self.noLogEvents:
			if argsList:
				BugUtil.debug("Event: %s - %r" % (eventType, argsList))
			else:
				BugUtil.debug("Event: %s" % eventType)

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
	"OnLoad": BugEventManager._handleInitBugEvent,
	"PreGameStart": BugEventManager._handleInitBugEvent,
	#"GameStart": BugEventManager._handleInitBugEvent,
	#"windowActivation": BugEventManager._handleInitBugEvent,
}


def configure(logging=None, noLogEvents=None):
	"""Sets the global event manager's logging options."""
	if g_eventManager is not None:
		g_eventManager.setLogging(logging)
		g_eventManager.setNoLogEvents(noLogEvents)

g_initDone = False
def initBug():
	"""Called once after Civ has initialized its data structures."""
	global g_initDone
	if not g_initDone:
		import BugInit
		BugInit.init()
		g_initDone = True
