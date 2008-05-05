## BugOptionsScreen
## Displays the BUG Options Screen
## BUG Mod - Copyright 2007

# For input see CvOptionsScreenCallbackInterface in Python\EntryPoints\

from CvPythonExtensions import *
import BugInitOptions
import BugOptions
import BugUtil

import BugGeneralOptionsTab
import BugAdvisorOptionsTab
import BugNJAGCOptionsTab
import BugScoreOptionsTab
import BugAlertsOptionsTab
import BugAutologOptionsTab
import BugUnitNameOptionsTab
import BUGPlotListTab
import BugConfigTrackerTab
import BugCreditsOptionsTab

import BugErrorOptionsTab

class BugOptionsScreen:
	"BUG Mod Options Screen"
	
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
			self.addTab(BugPlotListOptionsTab.BugPlotListOptionsTab(self))
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
		title = BugUtil.getPlainText("TXT_KEY_BUG_OPT_TITLE", "BUG Mod Options")
		self.pTabControl = CyGTabCtrl(title, False, False)
		self.pTabControl.setModal(1)
		self.pTabControl.setSize(850, 700)
		self.pTabControl.setControlsExpanding(False)
		self.pTabControl.setColumnLength(self.iScreenHeight)
		
		self.createTabs()

	def createTabs(self):
		for tab in self.tabs:
			tab.create(self.pTabControl)

	def clearAllTranslations(self):
		"Clear the translations of all tabs in response to the user choosing a language"
		for tab in self.tabs:
			tab.clearTranslation()
