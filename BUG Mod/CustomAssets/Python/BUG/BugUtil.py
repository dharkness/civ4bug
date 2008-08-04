## BugUtil
## Collection of utility functions.
##
## Copyright (c) 2008 The BUG Mod.

from CvPythonExtensions import *
import CvUtil
import sys

gc = CyGlobalContext()
localText = CyTranslator()

def getPlainText(key, default=None):
	"""
	Looks up a translated message in XML without any replacement parameters.
	If the key isn't found, the default is returned.
	"""
	return getText(key, (), default)

def getText(key, values, default=None):
	"""
	Looks up a translated message in XML with a tuple of replacement parameters.
	If the key isn't found, the default is returned.
	"""
	text = localText.getText(key, values)
	if (text and text != key):
		return text
	else:
		if default:
			return default
		else:
			return "XML key %s not found" % key

def formatFloat(value, decimals=None):
	if decimals is None:
		return "%f" % value
	else:
		return ("%." + str(decimals) + "f") % value


def readDebugOptions():
	"""
	Pulls the debug options from BugOptions and stores into local copies.
	Done this way to avoid hitting the options in tight loops using debug().
	"""
	import BugOptions
	BugOpt = BugOptions.getOptions()
	global printToScreen, printToFile
	printToScreen = BugOpt.isDebugToScreen()
	printToFile = BugOpt.isDebugToFile()

def debug(message):
	"""
	Logs a message on-screen and to a file, both optionally.
	"""
	if printToScreen:
		CyInterface().addImmediateMessage(message, "")
	if printToFile:
		sys.stdout.write(message + "\n")

# Hold current values of debug options, and read them upon loading this module
printToScreen = False
printToFile = False
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


def isNoEspionage():
	"Returns True if using at least 3.17 and the option 'No Espionage' is enabled"
	try:
		return gc.getGame().isOption(GameOptionTypes.GAMEOPTION_NO_ESPIONAGE)
	except:
		return False
