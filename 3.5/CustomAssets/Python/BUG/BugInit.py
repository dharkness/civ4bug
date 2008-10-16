## BugInit
##
## Initializes the BUG core and loads all of the mods.
##
## Called by BugEventManager during "OnLoad" and "PreGameStart" events.
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
		BugUtil.warn("BugInit - init() called again")
		return
	global g_initRunning
	if g_initRunning:
		BugUtil.warn("BugInit - init() already running")
		return
	g_initRunning = True
	
	BugUtil.debug("BugInit - initializing...")
	timer = BugUtil.Timer("BUG init")
	
	CvUtil.initDynamicFontIcons()
	loadMod("init")
	BugCore.initDone()
	timer.log("read configs").start()
	callInits()
	timer.log("call inits/events").start()
	
	timer.logTotal()
	g_initDone = True
	g_initRunning = False

def loadMod(name):
	"""Load the given mod from its XML file using a custom parser."""
	path = BugPath.findAssetFile(name + ".xml", "Config")
	if path:
		BugUtil.debug("BugInit - loading mod %s...", name)
		parser = BugConfig.XmlParser()
		timer = BugUtil.Timer("load mod")
		parser.parse(path)
		timer.log(name)
	else:
		BugUtil.error("BugInit - cannot find XML file for mod %s", name)

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
	BugUtil.debug("BugInit - calling init functions...")
	while g_initQueue:
		name, func = g_initQueue.pop(0)
		try:
			func()
		except:
			BugUtil.trace("BugInit - init '%s' failed" % name)
