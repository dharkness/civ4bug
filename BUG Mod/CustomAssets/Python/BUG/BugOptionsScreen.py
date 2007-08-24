## BugOptionsScreen
## Displays the BUG Options Screen
## BUG Mod - Copyright 2007

# For Input see BugOptionsScreenCallbackInterface in Python\EntryPoints\

from CvPythonExtensions import *
import BugInitOptions
import BugOptions

import BugGeneralOptionsTab
import BugNJAGCOptionsTab
import BugScoresOptionsTab
import BugAlertsOptionsTab
import BugAutologOptionsTab

class BugOptionsScreen:
	"Options Screen"
	
	def __init__(self):
		self.iScreenHeight = 50
		self.options = BugOptions.getOptions()
		self.tabs = []
		
		# instantiate all the tab objects
		self.addTab(BugGeneralOptionsTab.BugGeneralOptionsTab(self))
		self.addTab(BugNJAGCOptionsTab.BugNJAGCOptionsTab(self))
		self.addTab(BugScoresOptionsTab.BugScoresOptionsTab(self))
		self.addTab(BugAlertsOptionsTab.BugAlertsOptionsTab(self))
		self.addTab(BugAutologOptionsTab.BugAutologOptionsTab(self))

	def addTab(self, tab):
		self.tabs.append(tab)
		tab.setOptions(self.options)

	def getTabControl(self):
		return self.pTabControl

	def refreshScreen(self):
		return 1		

	def interfaceScreen(self):
		"Initial creation of the screen"
		self.pTabControl = CyGTabCtrl("BUG Mod Options", False, False)
		self.pTabControl.setModal(1)
		self.pTabControl.setSize(800, 695)
		self.pTabControl.setControlsExpanding(False)
		self.pTabControl.setColumnLength(self.iScreenHeight)
		
		self.createTabs()

	def createTabs(self):
		for tab in self.tabs:
			tab.create(self.pTabControl)
