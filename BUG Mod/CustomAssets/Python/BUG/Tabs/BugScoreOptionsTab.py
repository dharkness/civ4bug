## BugScoreOptionsTab
##
## Tab for the BUG Scoreboard Options.
##
## Copyright (c) 2007-2008 The BUG Mod.
##
## Author: EmperorFool

import BugOptionsTab

class BugScoreOptionsTab(BugOptionsTab.BugOptionsTab):
	"BUG Scores Options Screen Tab"
	
	def __init__(self, screen):
		BugOptionsTab.BugOptionsTab.__init__(self, "Scores", "Scoreboard")

	def create(self, screen):
		tab = self.createTab(screen)
		panel = self.createMainPanel(screen)
		left, center, right = self.addThreeColumnLayout(screen, panel, panel, True)
		
		self.addCheckbox(screen, left, "Scores__Delta")
		self.addCheckbox(screen, left, "Scores__DeltaIncludeCurrent")
		self.addTextDropdown(screen, left, left, "Scores__DisplayName")
		self.addCheckbox(screen, left, "Scores__UsePlayerName")
		self.addCheckbox(screen, left, "Scores__Attitude")
		self.addCheckbox(screen, left, "Scores__WorstEnemy")
		self.addCheckbox(screen, left, "Scores__WHEOOH")

		self.addSpacer(screen, left, "Scores_Dead_Civs")
		self.addLabel(screen, left, "Scores_Dead_Civs", "Dead Civilizations:")
		self.addCheckbox(screen, left, "Scores__ShowDead")
		self.addCheckbox(screen, left, "Scores__TagDead")
		self.addCheckbox(screen, left, "Scores__GreyDead")
		
		self.addCheckboxTextDropdown(screen, center, center, "Scores__Power", "Scores__PowerFormula")
		self.addIntDropdown(screen, center, center, "Scores__PowerDecimals", True)
		self.addColorDropdown(screen, center, center, "Scores__PowerColor", True)
		self.addFloatDropdown(screen, center, center, "Scores__PowerHighRatio", True)
		self.addColorDropdown(screen, center, center, "Scores__PowerHighColor", True)
		self.addFloatDropdown(screen, center, center, "Scores__PowerLowRatio", True)
		self.addColorDropdown(screen, center, center, "Scores__PowerLowColor", True)
		
		self.addLabel(screen, right, "Scores_Grid", "Advanced Layout:")
		self.addCheckbox(screen, right, "Scores__AlignIcons")
		self.addCheckbox(screen, right, "Scores__GroupVassals")
		self.addCheckbox(screen, right, "Scores__LeftAlignName")
		self.addCheckbox(screen, right, "Scores__ResearchIcons")
		self.addIntDropdown(screen, right, right, "Scores__DefaultSpacing", True)
		self.addLabel(screen, right, "Scores_Order", "Column Order:")
		self.addTextEdit(screen, None, right, "Scores__DisplayOrder")
