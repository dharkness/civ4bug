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
	"""Applies the color (string or int) to text and returns the resulting string."""
	if text is not None and color is not None:
		if isinstance(color, types.StringTypes):
			color = ColorUtil.keyToType(color)
		if color >= 0:
			return localText.changeTextColor(text, color)
	return text

def formatFloat(value, decimals=0):
	"""
	Formats value as a floating point number with decimals digits in the mantissa
	and returns the resulting string.
	"""
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


## Event Tracking and Output

INPUT_CODES = {
	NotifyCode.NOTIFY_MOUSEMOVE             : "Mouse Move", 
	NotifyCode.NOTIFY_MOUSEWHEELDOWN        : "Mouse Wheel Down", 
	NotifyCode.NOTIFY_MOUSEWHEELUP          : "Mouse Wheel Up", 
	NotifyCode.NOTIFY_CURSOR_MOVE_ON        : "Mouse Enter", 
 	NotifyCode.NOTIFY_CURSOR_MOVE_OFF       : "Mouse Leave", 
    NotifyCode.NOTIFY_CLICKED               : "Click",
    NotifyCode.NOTIFY_DBL_CLICKED           : "Double Click",
    
	NotifyCode.NOTIFY_CHARACTER             : "Character", 
    
    NotifyCode.NOTIFY_TABLE_HEADER_SELECTED : "Table Header Select",
    NotifyCode.NOTIFY_LISTBOX_ITEM_SELECTED : "List Select",
    NotifyCode.NOTIFY_SCROLL_DOWN           : "Scroll Down",
    NotifyCode.NOTIFY_SCROLL_UP             : "Scroll Up",
    
    NotifyCode.NOTIFY_NEW_HORIZONTAL_STOP   : "New Horizontal Stop",
    NotifyCode.NOTIFY_NEW_VERTICAL_STOP     : "New Vertical Stop",
    NotifyCode.NOTIFY_SLIDER_NEWSTOP        : "Slider New Stop",
    
    NotifyCode.NOTIFY_FOCUS                 : "Focus",
    NotifyCode.NOTIFY_UNFOCUS               : "Unfocus",
    
    NotifyCode.NOTIFY_LINKEXECUTE           : "Link Execute",
    NotifyCode.NOTIFY_FLYOUT_ITEM_SELECTED  : "Flyout Item Selected",
    NotifyCode.NOTIFY_MOVIE_DONE            : "Movie Done",
}

def debugInput(inputClass):
	"""
	Prints a debug message detailing the given input event.
	
	Add this to the handleInput function to see all events as they occur.
	
	def handleInput(self, inputClass):
		BugUtil.debugInput(inputClass)
	"""
	if (inputClass.getNotifyCode() in INPUT_CODES):
		debug("Input - %s for %s #%d (%d/%d/%d)" % 
			  (INPUT_CODES[inputClass.getNotifyCode()], 
			   inputClass.getFunctionName(),
			   inputClass.getID(), 
			   inputClass.getData(),
			   inputClass.getData1(),
			   inputClass.getData2()))


## Timing Code Execution

class Timer:
	"""
	Stopwatch for timing code execution and logging the results.
	
	timer = BugUtil.Timer('function')
	... code to time ...
	timer.log()
	
	A single Timer can be reused for timing loops without creating a new Timer
	for each iteration by calling restart().
	
	timer = BugUtil.Timer('draw loop')
	for/while ...
		timer.restart()
		... code to time ...
		timer.log()
	"""
	def __init__(self, item):
		self.item = item
		self.restart()
	
	def restart(self):
		self.total = 0
		self.start = time.clock()
		return self
	
	def start(self):
		if not self.running():
			self.start = time.clock()
		return self
		
	def stop(self):
		if self.running():
			self.total += time.clock() - self.start
			self.start = None
		return self
		
	def running(self):
		return self.start is not None
		
	def time(self):
		return self.total
	
	def log(self):
		debug("Timer - %s took %d ms" % (self.item, 1000 * self.stop().time()))


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
			raise ConfigError("No such module '%s'" % self.module)
		except AttributeError:
			raise ConfigError("Module '%s' must define function or class '%s'" % (self.module, self.functionOrClass))
	
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
	"""
	Error related to configuration problems.
	
	These are caught and reported during BUG initialization, and initizliation
	is allowed to continue so most problems can be reported at once. This may
	result in false-positive errors being reported.
	"""
	def __init__(self, message):
		BugError.__init__(self, message)


## Civ4 helpers

def isNoEspionage():
	"""Returns True if using at least 3.17 and the 'No Espionage' option is enabled."""
	try:
		return gc.getGame().isOption(GameOptionTypes.GAMEOPTION_NO_ESPIONAGE)
	except:
		return False
