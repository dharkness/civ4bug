## BugOptionsScreen
##
## Displays the BUG Options Screen and its tabs.
##
## For input handlers see CvOptionsScreenCallbackInterface in Python/EntryPoints.
##
## Notes
##   - Must be initialized when the module loads
##
## Copyright (c) 2007 The BUG Mod.
##
## Author: EmperorFool

from CvPythonExtensions import *
import BugConfig
import BugCore
import BugErrorOptionsTab
import BugOptions
import BugUtil


## Globals

g_optionsScreen = None


## Using and Showing

def getOptionsScreen():
	return g_optionsScreen

def showOptionsScreen(argsList=None):
	getOptionsScreen().interfaceScreen()


## Event Handlers

def clearAllTranslations(argsList=None):
	g_optionsScreen.clearAllTranslations()


## Class

class BugOptionsScreen:
	"BUG Mod Options Screen"
	
	def __init__(self):
		self.iScreenHeight = 50
		self.options = BugOptions.getOptions()
		self.tabs = []
		self.reopen = False

	def addTab(self, tab):
		self.tabs.append(tab)
		tab.setOptions(self.options)

	def getTabControl(self):
		return self.pTabControl

	def refreshScreen(self):
		return 1		

	def interfaceScreen(self):
		"Initial creation of the screen"
		title = BugUtil.getPlainText("TXT_KEY_BUG_OPT_TITLE", "BUG Mod Options")
		self.pTabControl = CyGTabCtrl(title, False, False)
		self.pTabControl.setModal(1)
		self.pTabControl.setSize(900, 715)
		self.pTabControl.setControlsExpanding(False)
		self.pTabControl.setColumnLength(self.iScreenHeight)
		
		if self.options.isLoaded():
			self.createTabs()
		else:
			BugErrorOptionsTab.BugErrorOptionsTab(self).create(self.pTabControl)

	def createTabs(self):
		for i, tab in enumerate(self.tabs):
			if not self.reopen or i % 2:
				tab.create(self.pTabControl)

	def clearAllTranslations(self):
		"Clear the translations of all tabs in response to the user choosing a language"
		for tab in self.tabs:
			tab.clearTranslation()
	
	def close(self):
		# TODO: check for error
		self.options.write()
		self.pTabControl.destroy()
		self.pTabControl = None
		if self.reopen:
			self.reopen = False
			self.interfaceScreen()


## Configuration

class ScreenConfig:
	
	def __init__(self, id):
		self.id = id
		self.tabs = []
	
	def addTab(self, tab):
		self.tabs.append(tab)

class ScreenHandler(BugConfig.Handler):
	
	TAG = "screen"
	
	def __init__(self):
		BugConfig.Handler.__init__(self, ScreenHandler.TAG, "id", TabHandler.TAG)
		self.addAttribute("id", True)
	
	def handle(self, element, id):
		screen = ScreenConfig(id)
		element.setState("options-screen", screen)
		BugCore.game._addScreen(screen)

class TabHandler(BugConfig.Handler):
	
	TAG = "tab"
	
	def __init__(self):
		BugConfig.Handler.__init__(self, TabHandler.TAG, "id screen module class")
		self.addAttribute("screen")
		self.addAttribute("module", True, True)
		self.addAttribute("class", True, False, None, "module")
		self.addAttribute("id", True, False, None, "module")
	
	def handle(self, element, screenId, module, clazz, id):
		if screenId:
			screen = BugCore.game._getScreen(screenId)
		else:
			screen = element.getState("options-screen")
		if not screen:
			raise BugUtil.ConfigError("Element <%s> %s must be in <screen> or have screen attribute", id, element.tag)
		screen.addTab(id)
		tab = BugUtil.callFunction(module, clazz, g_optionsScreen)
		g_optionsScreen.addTab(tab)


## Initialization

def init():
	global g_optionsScreen
	g_optionsScreen = BugOptionsScreen()

init()
