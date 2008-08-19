## BugAutologOptionsTab
##
## Tab for the BUG Autolog Options.
##
## Copyright (c) 2007-2008 The BUG Mod.
##
## Author: EmperorFool

import BugOptionsTab

class BugAutologOptionsTab(BugOptionsTab.BugOptionsTab):
	"BUG Autolog Options Screen Tab"
	
	def __init__(self, screen):
		BugOptionsTab.BugOptionsTab.__init__(self, "Autolog", "Logging")

	def create(self, screen):
		tab = self.createTab(screen)
		panel = self.createMainPanel(screen)
		column = self.addOneColumnLayout(screen, panel)
		
		self.addCheckbox(screen, column, "Autolog__Enabled")
		
		# File and Format
		screen.attachHSeparator(column, column + "Sep1")
		left, right = self.addTwoColumnLayout(screen, column, "Options")
		
		self.addCheckbox(screen, left, "Autolog__Silent")
		self.addCheckbox(screen, left, "Autolog__ColorCoding")
		self.addIntDropdown(screen, left, left, "Autolog__4000BC")
		self.addCheckbox(screen, left, "Autolog__IBT")
		
		self.addCheckbox(screen, right, "Autolog__DefaultFileName")
		self.addTextEdit(screen, right, right, "Autolog__FilePath")
		self.addTextEdit(screen, right, right, "Autolog__FileName")
		self.addTextEdit(screen, right, right, "Autolog__Prefix")
		self.addTextDropdown(screen, right, right, "Autolog__Format")
		
		# What to Log
		screen.attachHSeparator(column, column + "Sep2")
		col1, col2, col3, col4, col5 = self.addMultiColumnLayout(screen, column, 5, "Events")
		
		self.addLabel(screen, col1, "Autolog_Builds", "Research and Builds:")
		self.addCheckbox(screen, col1, "Autolog__LogTech")
		self.addCheckbox(screen, col1, "Autolog__LogBuildStarted")
		self.addCheckbox(screen, col1, "Autolog__LogBuildCompleted")
		self.addCheckbox(screen, col1, "Autolog__LogProjects")
		self.addCheckbox(screen, col1, "Autolog__LogImprovements")
		
		self.addLabel(screen, col2, "Autolog_Cities", "Cities:")
		self.addCheckbox(screen, col2, "Autolog__LogCityFounded")
		self.addCheckbox(screen, col2, "Autolog__LogCityGrowth")
		self.addCheckbox(screen, col2, "Autolog__LogCityBorders")
		self.addCheckbox(screen, col2, "Autolog__LogCityOwner")
		self.addCheckbox(screen, col2, "Autolog__LogCityRazed")
		self.addCheckbox(screen, col2, "Autolog__LogCityWhipStatus")

		self.addLabel(screen, col3, "Autolog_Events", "Events:")
		self.addCheckbox(screen, col3, "Autolog__LogGoodies")
		self.addCheckbox(screen, col3, "Autolog__LogReligion")
		self.addCheckbox(screen, col3, "Autolog__LogCorporation")
		self.addCheckbox(screen, col3, "Autolog__LogGP")
		self.addCheckbox(screen, col3, "Autolog__LogGA")

		self.addLabel(screen, col4, "Autolog_Politics", "Diplomacy:")
		self.addCheckbox(screen, col4, "Autolog__LogContact")
		self.addCheckbox(screen, col4, "Autolog__LogAttitude")
		self.addCheckbox(screen, col4, "Autolog__LogWar")
		self.addCheckbox(screen, col4, "Autolog__LogVassals")
		self.addCheckbox(screen, col4, "Autolog__LogCivics")
		
		self.addLabel(screen, col5, "Autolog_Combat", "Combat:")
		self.addCheckbox(screen, col5, "Autolog__LogCombat")
		self.addCheckbox(screen, col5, "Autolog__LogPromotions")
		self.addCheckbox(screen, col5, "Autolog__LogPillage")
