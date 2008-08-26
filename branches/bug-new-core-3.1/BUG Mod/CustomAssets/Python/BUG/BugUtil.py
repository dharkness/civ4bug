## BugUtil
##
## Collection of general-purpose utility functions.
##
## TODO:
##  * Add warn() and error()
##
## Copyright (c) 2008 The BUG Mod.
##
## Author: EmperorFool

from CvPythonExtensions import *
import sys
import time
import types
import ColorUtil

gc = CyGlobalContext()
localText = CyTranslator()

## Getting translated text from CIV4GameText XML files and general formatting

def getPlainText(key, default=None):
	"""
	Looks up a translated message in XML without any replacement parameters.
	If the key isn't found, the default is returned.
	"""
	return getText(key, (), default)

def getText(key, values, default=None):
	"""
	Looks up a translated message in XML with a tuple of replacement parameters.
	It is safe to pass in a single value instead of tuple/list.
	If the key isn't found, the default is returned.
	"""
	if values is None:
		values = ()
	elif not isinstance(values, tuple) and not isinstance(values, list):
		values = (values,)
	text = localText.getText(key, values)
	if (text and text != key):
		return text
	else:
		if default is not None:
			return default
		else:
			return "XML key %s not found" % key

def colorText(text, color):
	if text is not None and color is not None:
		if isinstance(color, types.StringTypes):
			color = ColorUtil.keyToType(color)
		if color >= 0:
			return localText.changeTextColor(text, color)
	return text

def formatFloat(value, decimals=0):
	if decimals <= 0:
		return "%f" % value
	else:
		return ("%." + str(decimals) + "f") % value


## Debug and Error output

printToScreen = False
printToFile = True
includeTime = True

def debug(message, *args):
	"""
	Logs a message on-screen and to a file, both optionally.
	"""
	if printToScreen or printToFile:
		if args:
			message = message % args
		if printToScreen:
			CyInterface().addImmediateMessage(message, "")
		if printToFile:
			if includeTime:
				message = time.asctime()[11:20] + message
			sys.stdout.write(message + "\n")

def readDebugOptions():
	"""
	Pulls the debug options from BugOptions and stores into local copies.
	Done this way to avoid hitting the options in tight loops using debug().
	"""
	import BugOptions
	BugOpt = BugOptions.getOptions()
	global printToScreen
	global printToFile
	printToScreen = BugOpt.isDebugToScreen()
	printToFile = BugOpt.isDebugToFile()

#readDebugOptions()

EVENT_CODES = { NotifyCode.NOTIFY_CURSOR_MOVE_ON        : "Mouse Enter", 
			 	NotifyCode.NOTIFY_CURSOR_MOVE_OFF       : "Mouse Leave", 
			    NotifyCode.NOTIFY_CLICKED               : "Click",
			    NotifyCode.NOTIFY_LISTBOX_ITEM_SELECTED : "List Select",
			  }

def debugEvent(inputClass):
	"Prints a debug message detailing the given event."
	if (inputClass.getNotifyCode() in EVENT_CODES):
		debug("Event: %s for %s #%d (%d/%d)" % 
			  (EVENT_CODES[inputClass.getNotifyCode()], 
			   inputClass.getFunctionName(),
			   inputClass.getID(), 
			   inputClass.getData1(),
			   inputClass.getData2()))


## Binding and calling functions dynamically
## (looking up module and function/class by name rather than directly in Python
## and passing in arguments set up at time of creation or when called)

class Function:
	
	def __init__(self, module, functionOrClass, *args, **kwargs):
		self.module = module
		self.functionOrClass = functionOrClass
		self.function = None
		self.setArguments(*args, **kwargs)
	
	def bind(self):
		try:
			if self.function is None:
				debug("BUG: binding %s.%s" % (self.module, self.functionOrClass))
				self.function = getattr(__import__(self.module), self.functionOrClass)
		except ImportError:
			raise ConfigError("No such module '%s'" % module)
		except AttributeError:
			raise ConfigError("Module '%s' must define function or class '%s'" % (module, functionOrClass))
	
	def setArguments(self, *args, **kwargs):
		self.args = args
		self.kwargs = kwargs
	
	def call(self, *args, **kwargs):
		self.bind()
		if args or kwargs:
			self.setArguments(*args, **kwargs)
		debug("BUG: calling %r" % self)
		return self.function(*self.args, **self.kwargs)
	
	def __call__(self, *args, **kwargs):
		return self.call(*args, **kwargs)
	
	def __repr__(self):
		if self.args or self.kwargs:
			return "<func %s.%s (%r, %r)>" % \
		   	   	   (self.module, self.functionOrClass, self.args, self.kwargs)
		else:
			return "<func %s.%s>" % \
		   	   	   (self.module, self.functionOrClass)

def getFunction(module, functionOrClass, bind=False, *args, **kwargs):
	func = Function(module, functionOrClass, *args, **kwargs)
	if bind:
		func.bind()
	return func

def callFunction(module, functionOrClass, *args, **kwargs):
	func = getFunction(module, functionOrClass, True)
	return func(*args, **kwargs)


## Exception classes

class BugError(Exception):
	"""Generic BUG-related error."""
	def __init__(self, message):
		Exception.__init__(self, message)

class ConfigError(BugError):
	"""Error related to configuration problems.
	
	These are caught and reported during BUG initialization, and initizliation
	is allowed to continue so most problems can be reported at once. This may
	result in false-positive errors being reported.
	"""
	def __init__(self, message):
		ConfigError.__init__(self, message)


## Civ4 helpers

def isNoEspionage():
	"Returns True if using at least 3.17 and the option 'No Espionage' is enabled"
	try:
		return gc.getGame().isOption(GameOptionTypes.GAMEOPTION_NO_ESPIONAGE)
	except:
		return False
