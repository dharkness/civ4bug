## BugScoresOptionsTab
## Tab for the BUG Scoreboard Options
## BUG Mod - Copyright 2007

import BugOptionsTab

class BugScoresOptionsTab(BugOptionsTab.BugOptionsTab):
	"BUG Scores Options Screen Tab"
	
	def __init__(self, screen):
		BugOptionsTab.BugOptionsTab.__init__(self, "Scores", "Scoreboard")

	def create(self, screen):
		tab = self.createTab(screen)
		panel = self.createMainPanel(screen)
		leftPanel = self.addOneColumnLayout(screen, panel)
		
		self.addTextDropdown(screen, leftPanel, leftPanel, "Scores_DisplayName")
		self.addCheckbox(screen, leftPanel, "Scores_Attitude")
		self.addCheckbox(screen, leftPanel, "Scores_Power")
		
		screen.attachLabel(leftPanel, "Scores_DeadCivsLabel", "Dead Civilizations:")
		screen.setControlFlag("Scores_DeadCivsLabel", "CF_LABEL_DEFAULTSIZE")
		self.addCheckbox(screen, leftPanel, "Scores_HideDead")
		self.addCheckbox(screen, leftPanel, "Scores_TagDead")
		self.addCheckbox(screen, leftPanel, "Scores_GreyDead")
