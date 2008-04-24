## BugOptionsScreen
## Displays the BUG Options Screen
## BUG Mod - Copyright 2007

# For Input see BugOptionsScreenCallbackInterface in Python\EntryPoints\

from CvPythonExtensions import *
import BugInitOptions
import BugOptions

import BugGeneralOptionsTab
import BugAdvisorOptionsTab
import BugNJAGCOptionsTab
import BugScoreOptionsTab
import BugAlertsOptionsTab
import BugAutologOptionsTab
import BugUnitNameOptionsTab
import BugConfigTrackerTab
import BugCreditsOptionsTab

import BugErrorOptionsTab

class BugOptionsScreen:
	"Options Screen"
	
	def __init__(self):
		self.iScreenHeight = 50
		self.options = BugOptions.getOptions()
		self.tabs = []
		
		if (not self.options.isLoaded()):
			self.addTab(BugErrorOptionsTab.BugErrorOptionsTab(self))
		else:
			# instantiate all the tab objects
			self.addTab(BugGeneralOptionsTab.BugGeneralOptionsTab(self))
			self.addTab(BugAdvisorOptionsTab.BugAdvisorOptionsTab(self))
			self.addTab(BugNJAGCOptionsTab.BugNJAGCOptionsTab(self))
			self.addTab(BugScoreOptionsTab.BugScoreOptionsTab(self))
			self.addTab(BugAlertsOptionsTab.BugAlertsOptionsTab(self))
			self.addTab(BugAutologOptionsTab.BugAutologOptionsTab(self))
			self.addTab(BugUnitNameOptionsTab.BugUnitNameOptionsTab(self))
			self.addTab(BugConfigTrackerTab.BugConfigTrackerTab(self))
			self.addTab(BugCreditsOptionsTab.BugCreditsOptionsTab(self))

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
