## BugSystemOptionsTab
##
## Tab for the BUG System Options (check for updates and SVN).
##
## Copyright (c) 2008 The BUG Mod.
##
## Author: EmperorFool

import BugOptionsTab
import CvModName

class BugSystemOptionsTab(BugOptionsTab.BugOptionsTab):
	"BUG System Options Screen Tab"
	
	def __init__(self, screen):
		BugOptionsTab.BugOptionsTab.__init__(self, "System", "System")

	def create(self, screen):
		tab = self.createTab(screen)
		panel = self.createMainPanel(screen)
		column = self.addOneColumnLayout(screen, panel)

		self.addLabel(screen, column, "Subversion", "Subversion (SVN):")
		self.addCheckbox(screen, column, "Core__CheckForUpdates")
		self.addTextEdit(screen, column, column, "Core__LocalRoot")
		self.addTextEdit(screen, column, column, "Core__RepositoryUrl")

		screen.attachHSeparator(column, column + "Sep1")
		self.addLabel(screen, column, "Debug_Logging", "Debugging Output:")
		left, center, right = self.addThreeColumnLayout(screen, column)
		self.addTextDropdown(screen, left, left, "Core__ScreenLogLevel")
		self.addTextDropdown(screen, center, center, "Core__FileLogLevel")
		self.addCheckbox(screen, right, "Core__LogTime")
		
		screen.attachHSeparator(column, column + "Sep2")
		left, right = self.addTwoColumnLayout(screen, column, "Bottom", False)
		self.addCheckbox(screen, left, "MainInterface__OptionsKey")
		screen.setLayoutFlag(right, "LAYOUT_RIGHT")
		screen.setLayoutFlag(right, "LAYOUT_SIZE_HPREFERREDEXPANDING")
		self.addLabel(screen, right, "Version", 
					  CvModName.getDisplayNameAndVersion() + " (" + CvModName.getCivNameAndVersion() + ")")
