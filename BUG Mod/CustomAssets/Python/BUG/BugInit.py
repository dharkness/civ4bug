## BugInit
##
## Initializes the BUG core and loads all of the mods.
## Called by BugEventManager during "windowActivation" event.
##
## Copyright (c) 2008 The BUG Mod.
##
## Author: EmperorFool

import CvUtil
import BugConfig
import BugCore
import BugOptions
import BugPath
import BugUtil

g_initRunning = False
g_initDone = False

g_initQueue = []

def init():
	"""Performs the one-time initialization of the BUG core and all mods."""
	global g_initDone
	if g_initDone:
		BugUtil.debug("WARN: BugInit.init() called again")
		return
	global g_initRunning
	if g_initRunning:
		BugUtil.debug("WARN: BugInit.init() called while running")
		return
	g_initRunning = True
	
	BugUtil.debug("BUG: initializing...")
	timer = BugUtil.Timer("BUG init")
	
	CvUtil.initDynamicFontIcons()
	timer.log("fonts").start()
	loadMod("init")
	timer.log("config").start()
	BugCore.initDone()
	BugOptions.read()
	timer.log("read options").start()
	callInits()
	timer.log("call inits/events").start()
	
	timer.logTotal()
	g_initDone = True
	g_initRunning = False

def loadMod(name):
	"""Load the given mod from its XML file using a custom parser."""
	path = BugPath.findAssetFile(name + ".xml", "Config")
	if path:
		BugUtil.debug("BUG: loading mod %s..." % name)
		parser = BugConfig.XmlParser()
		timer = BugUtil.Timer("load mod")
		parser.parse(path)
		timer.log(name)
	else:
		BugUtil.debug("BUG: cannot find XML file for mod %s" % name)

def addInit(name, function):
	"""
	Calls function after all mods are loaded.
	
	If all mods have been loaded, the function is called immediately.
	Modules should use this function to setup a one-time initialization function
	that requires an initialized CyGlobalContext.
	
	name - short descriptive string used in debug messages, typically the module's name
	function - the function to call
	
	Use BugUtil.getFunction() to pass arguments to your function.
	"""
	g_initQueue.append((name, function))
	if g_initDone:
		callInits()

def callInits():
	"""Calls all of the stored init functions in the order they were added."""
	BugUtil.debug("BUG: calling init functions...")
	while g_initQueue:
		name, func = g_initQueue.pop(0)
		try:
			func()
#		except BugUtil.ConfigError, e:
#			# TODO: register with ConfigTracker
#			BugUtil.debug("ERROR: init for module '%s' failed: %s" % (name, e))
		except:
			import sys
			info = sys.exc_info()
			# TODO: register with ConfigTracker
			BugUtil.debug("ERROR: init for module '%s' failed: %s" % (name, info[1]))
			import traceback
			traceback.print_exc()
