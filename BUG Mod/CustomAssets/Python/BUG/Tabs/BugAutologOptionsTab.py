## BugAutologOptionsTab
## Tab for the BUG Scoreboard Options
## BUG Mod - Copyright 2007

import BugOptionsTab

class BugAutologOptionsTab(BugOptionsTab.BugOptionsTab):
	"BUG Autolog Options Screen Tab"
	
	def __init__(self, screen):
		BugOptionsTab.BugOptionsTab.__init__(self, "Autolog", "Logging")

	def create(self, screen):
		tab = self.createTab(screen)
		panel = self.createMainPanel(screen)
		column = self.addOneColumnLayout(screen, panel)
		
		self.addCheckbox(screen, column, "Autolog_Enabled")
		
		# File and Format
		screen.attachHSeparator(column, column + "Sep1")
		left, right = self.addTwoColumnLayout(screen, column, "Options")
		
		self.addCheckbox(screen, left, "Autolog_Silent")
		self.addTextDropdown(screen, left, left, "Autolog_Format")
		self.addCheckbox(screen, left, "Autolog_ColorCoding")
		self.addIntDropdown(screen, left, left, "Autolog_4000BC")
		self.addCheckbox(screen, left, "Autolog_IBT")
		
		self.addCheckbox(screen, right, "Autolog_DefaultFileName")
		self.addTextEdit(screen, right, right, "Autolog_FilePath")
		self.addTextEdit(screen, right, right, "Autolog_FileName")
		self.addTextEdit(screen, right, right, "Autolog_Prefix")
		
		# What to Log
		screen.attachHSeparator(column, column + "Sep2")
		col1, col2, col3, col4, col5 = self.addMultiColumnLayout(screen, column, 5, "Events")
		
		screen.attachLabel(col1, "Autolog_BuildLabel", "Research and Builds:")
		self.addCheckbox(screen, col1, "Autolog_LogTech")
		self.addCheckbox(screen, col1, "Autolog_LogBuildStarted")
		self.addCheckbox(screen, col1, "Autolog_LogBuildCompleted")
		self.addCheckbox(screen, col1, "Autolog_LogProjects")
		self.addCheckbox(screen, col1, "Autolog_LogImprovements")
		
		screen.attachLabel(col2, "Autolog_CitiesLabel", "Cities:")
		self.addCheckbox(screen, col2, "Autolog_LogCityFounded")
		self.addCheckbox(screen, col2, "Autolog_LogCityGrowth")
		self.addCheckbox(screen, col2, "Autolog_LogCityBorders")
		self.addCheckbox(screen, col2, "Autolog_LogCityOwner")
		self.addCheckbox(screen, col2, "Autolog_LogCityRazed")
		
		screen.attachLabel(col3, "Autolog_EventsLabel", "Events:")
		self.addCheckbox(screen, col3, "Autolog_LogGoodies")
		self.addCheckbox(screen, col3, "Autolog_LogReligion")
		self.addCheckbox(screen, col3, "Autolog_LogCorporation")
		self.addCheckbox(screen, col3, "Autolog_LogGP")
		self.addCheckbox(screen, col3, "Autolog_LogGA")
		
		screen.attachLabel(col4, "Autolog_PoliticsLabel", "Diplomacy:")
		self.addCheckbox(screen, col4, "Autolog_LogContact")
		self.addCheckbox(screen, col4, "Autolog_LogAttitude")
		self.addCheckbox(screen, col4, "Autolog_LogWar")
		self.addCheckbox(screen, col4, "Autolog_LogVassals")
		self.addCheckbox(screen, col4, "Autolog_LogCivics")
		
		screen.attachLabel(col5, "Autolog_CombatLabel", "Combat:")
		self.addCheckbox(screen, col5, "Autolog_LogCombat")
		self.addCheckbox(screen, col5, "Autolog_LogPromotions")
		self.addCheckbox(screen, col5, "Autolog_LogPillage")
