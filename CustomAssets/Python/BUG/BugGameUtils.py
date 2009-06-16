## BugGameUtils
##
## Provides modular access to CvGameUtils-based callback handlers and listeners.
## A handler is a function that overrides the default processing of the callback
## and returns a result of its choosing. A listener is a function that is called
## after the handler(s) for a callback with the original arguments and the result.
##
## Almost every callback has a default value assigned to it. This value is used
## to signal that a handler has decided not to handle the callback. Each callback
## can have multiple handlers assigned to it, and the first handler to return
## a non-default value "wins". Its value is returned as the result of the callback
## and any handlers after it are skipped. All listeners for a callback are called.
##
## Handlers and listeners can be individual module-level functions or members
## of a class such as your own CvGameUtils replacement. You can use the XML tags
## or the module-level functions here to register your handlers and listeners.
##
## When adding a handler or listener function, if its name matches the callback
## you don't need to specify the callback name. Listener functions may put "Listener"
## after the callback name for automatic detection.
##
## The <handler>, <listener>, and <default> elements below must be enclosed within
## a <gameutils> element. If it specifies a "class" attribute, only the listed
## handlers and listeners will be registered.
##
## Registering GameUtils Classes
##
##   <gameutils module="<module>" class="<class>"/>
##
##   addUtils(utils, override)
##     Adds all of the functions from <utils> as handlers and listeners. Every function
##     name must match the name of a callback (with "Listener" appended for listeners).
##     To ignore a function, begin its name with a single underscore ("_").
##     If override (default False) is True, its handlers are placed before existing handlers.
##
## Registering Handlers
##
##   <gameutils module="<module>" handler="<name1> <name2> ..." override="True|False"/>
##
##   addHandler(func, override)
##     Adds <func> as a handler for the callback with the same name.
##     If override (default False) is True, it is placed before existing handlers.
##
##   addNamedHandler(name, func, override)
##     Same as addHandler() above for callback <name>.
##
## Registering Listeners
##
##   <gameutils module="<module>" listener="<name1> <name2> ..."/>
##
##   addListener(func)
##     Adds <func> as a listener for the callback with the same name.
##     If its name ends with "Listener", it is dropped to get the callback name.
##
##   addNamedListener(name, func)
##     Same as addListener() above for callback <name>.
##
## Setting Defaults
##
##   TODO: <gameutils default="<name>" type="<type>" value="<value>"/>
##
##   setDefault(name, value)
##     Sets the default for callback <name> to <value>.
##     Use this only if you have defined new callbacks for your mod.
##
## Notes
##   - Must be initialized externally by calling init()
##
## Copyright (c) 2009 The BUG Mod.
##
## Author: EmperorFool

from CvPythonExtensions import *
import BugUtil
import CvGameUtils
import types


## Constants and Globals

LISTENER_SUFFIX = "Listener"

g_dispatcher = None


## Configuration

def addUtils(utils, override=False):
	getDispatcher()._addUtils(utils)


def addHandler(func, override=False):
	addNamedHandler(func.__name__, func, override)

def addNamedHandler(name, func, override=False):
	getDispatcher()._addHandler(name, func, override)

def addBoundHandler(utils, func, override=False):
	addNamedBoundHandler(func.__name__, utils, func, override)

def addNamedBoundHandler(name, utils, func, override=False):
	getDispatcher()._addBoundHandler(name, func, override)


def addListener(func):
	name = func.__name__
	if name.endswith(LISTENER_SUFFIX):
		name = name[:-len(LISTENER_SUFFIX)]
	addNamedListener(name, func)

def addNamedListener(name, func):
	getDispatcher()._addListener(name, func)

def addBoundListener(utils, func):
	name = func.__name__
	if name.endswith(LISTENER_SUFFIX):
		name = name[:-len(LISTENER_SUFFIX)]
	addNamedBoundListener(name, utils, func)

def addNamedBoundListener(name, utils, func):
	getDispatcher()._addBoundListener(name, utils, func)


def setDefault(name, value):
	getDispatcher()._setDefault(name, value)


def getDispatcher():
	return g_dispatcher


## Dispatcher

class Dispatcher:
	
	def __init__(self):
		self._callbacks = {}
		self._baseUtils = CvGameUtils.CvGameUtils()
		clazz = CvGameUtils.CvGameUtils
		for name, func in clazz.__dict__.iteritems():
			if not name.startswith("_") and isinstance(func, types.FunctionType):
				self._createCallback(name, func)
		
		# setup defaults
		self._setDefault("isVictory", True)
		self._setDefault("isPlayerResearch", True)
		self._setDefault("getExtraCost", 0)
		self._setDefault("createBarbarianCities", False)
		self._setDefault("createBarbarianUnits", False)
		self._setDefault("skipResearchPopup", False)
		self._setDefault("showTechChooserButton", True)
		self._setDefault("getFirstRecommendedTech", TechTypes.NO_TECH)
		self._setDefault("getSecondRecommendedTech", TechTypes.NO_TECH)
		self._setDefault("canRazeCity", True)
		self._setDefault("canDeclareWar", True)
		self._setDefault("skipProductionPopup", False)
		self._setDefault("showExamineCityButton", True)
		self._setDefault("getRecommendedUnit", UnitTypes.NO_UNIT)
		self._setDefault("getRecommendedBuilding", BuildingTypes.NO_BUILDING)
		self._setDefault("updateColoredPlots", False)
		self._setDefault("isActionRecommended", False)
		self._setDefault("unitCannotMoveInto", False)
		self._setDefault("cannotHandleAction", False)
		self._setDefault("canBuild", -1)
		self._setDefault("cannotFoundCity", False)
		self._setDefault("cannotSelectionListMove", False)
		self._setDefault("cannotSelectionListGameNetMessage", False)
		self._setDefault("cannotDoControl", False)
		self._setDefault("canResearch", False)
		self._setDefault("cannotResearch", False)
		self._setDefault("canDoCivic", False)
		self._setDefault("cannotDoCivic", False)
		self._setDefault("canTrain", False)
		self._setDefault("cannotTrain", False)
		self._setDefault("canConstruct", False)
		self._setDefault("cannotConstruct", False)
		self._setDefault("canCreate", False)
		self._setDefault("cannotCreate", False)
		self._setDefault("canMaintain", False)
		self._setDefault("cannotMaintain", False)
		self._setDefault("AI_chooseTech", TechTypes.NO_TECH)
		self._setDefault("AI_chooseProduction", False)
		self._setDefault("AI_unitUpdate", False)
		self._setDefault("AI_doWar", False)
		self._setDefault("AI_doDiplo", False)
		self._setDefault("doHolyCity", False)
		self._setDefault("doHolyCityTech", False)
		self._setDefault("doGold", False)
		self._setDefault("doResearch", False)
		self._setDefault("doGoody", False)
		self._setDefault("doGrowth", False)
		self._setDefault("doProduction", False)
		self._setDefault("doCulture", False)
		self._setDefault("doPlotCulture", False)
		self._setDefault("doReligion", False)
		self._setDefault("cannotSpreadReligion", False)
		self._setDefault("doGreatPeople", False)
		self._setDefault("doMeltdown", False)
		self._setDefault("doReviveActivePlayer", False)
		self._setDefault("citiesDestroyFeatures", True)
		self._setDefault("canFoundCitiesOnWater", False)
		self._setDefault("doCombat", False)
		self._setDefault("getConscriptUnitType", UnitTypes.NO_UNIT)
		self._setDefault("getCityFoundValue", -1)
		self._setDefault("canPickPlot", True)
		self._setDefault("getUnitCostMod", -1)
		self._setDefault("getBuildingCostMod", -1)
		self._setDefault("canUpgradeAnywhere", False)
		self._setDefault("getWidgetHelp", u"")
		self._setDefault("getUpgradePriceOverride", -1)
	
	def _createCallback(self, name, func):
		BugUtil.debug("BugGameUtils - creating callback %s", name)
		callback = Callback(name, self._baseUtils, func)
		self._callbacks[name] = callback
		setattr(self.__class__, name, callback)
	
	def _getCallback(self, name):
		try:
			return self._callbacks[name]
		except KeyError:
			BugUtil.trace("Unknown GameUtils callback %s", name)
			raise
	
	def _setDefault(self, name, default):
		self._getCallback(name).setDefault(default)
	
	def _addHandler(self, name, func, override=False):
		self._getCallback(name).addHandler(func)
	
	def _addBoundHandler(self, name, utils, func, override=False):
		self._addHandler(name, self._bind(utils, func), override)
	
	def _addListener(self, name, func):
		self._getCallback(name).addListener(func)
	
	def _addBoundListener(self, name, utils, func):
		self._addListener(name, self._bind(utils, func))
	
	def _addUtils(self, utils, override=False):
		clazz = utils.__class__
		BugUtil.debug("BugGameUtils - registering %s.%s", clazz.__module__, clazz.__name__)
		for name, func in clazz.__dict__.iteritems():
			if not name.startswith("_") and isinstance(func, types.FunctionType):
				if name.endswith(LISTENER_SUFFIX):
					self._addBoundListener(name[:-len(LISTENER_SUFFIX)], utils, func)
				else:
					self._addBoundHandler(name, utils, func, override)
	
	def _bind(self, utils, func):
		bound = lambda *args: func(utils, *args)
		bound.__module__ = func.__module__
		return bound


## Callback

class Callback:
	
	def __init__(self, name, baseUtils, baseHandler, default=None):
		self.name = name
		self.baseUtils = baseUtils
		self.baseHandler = baseHandler
		self.default = default
		self.handlers = []
		self.listeners = []
	
	def setDefault(self, default):
		BugUtil.debug("BugGameUtils - %s - setting default to %s", self.name, default)
		self.default = default
	
	def addHandler(self, func, override=False):
		if override:
			BugUtil.debug("BugGameUtils - %s - overriding %s handler", self.name, func.__module__)
			self.handlers.insert(0, func)
		else:
			BugUtil.debug("BugGameUtils - %s - adding %s handler", self.name, func.__module__)
			self.handlers.append(func)
	
	def addListener(self, func):
		BugUtil.debug("BugGameUtils - %s - adding %s listener", self.name, func.__module__)
		self.listeners.append(func)
	
	def __call__(self, argsList):
		for handler in self.handlers:
			BugUtil.debug("BugGameUtils - %s - dispatching to %s handler", self.name, handler.__module__)
			result = handler(argsList)
			if result is not None and result != self.default:
				break
		else:
			if self.default is not None:
				BugUtil.debug("BugGameUtils - %s - using default %s", self.name, self.default)
				result = self.default
			else:
				BugUtil.debug("BugGameUtils - %s - dispatching to base handler", self.name)
				result = self.baseHandler(self.baseUtils, argsList)
		for listener in self.listeners:
			BugUtil.debug("BugGameUtils - %s - calling %s listener", self.name, listener.__module__)
			listener(argsList, result)
		return result


## Initialization

def init():
	BugUtil.debug("BugGameUtils - initializing")
	global g_dispatcher
	g_dispatcher = Dispatcher()
