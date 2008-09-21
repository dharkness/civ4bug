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
		column, right = self.addTwoColumnLayout(screen, panel, panel, True)
		
		left, space, center = self.addThreeColumnLayout(screen, column, column, False)
		self.addLabel(screen, left, "Scores_General", "General:")
		self.addTextDropdown(screen, left, left, "Scores__DisplayName")
		self.addCheckbox(screen, left, "Scores__UsePlayerName")
		self.addCheckbox(screen, left, "Scores__ShowMinor")
		
		self.addSpacer(screen, space, "Scores_General", 3)
		
		self.addLabel(screen, center, "Scores_Dead_Civs", "Dead Civilizations:")
		self.addCheckbox(screen, center, "Scores__ShowDead")
		self.addCheckbox(screen, center, "Scores__TagDead")
		self.addCheckbox(screen, center, "Scores__GreyDead")
		self.addSpacer(screen, center, "Scoreboard_Tab")
		
		screen.attachHSeparator(column, column + "Sep")
		
		left, center = self.addTwoColumnLayout(screen, column, column, False)
		self.addLabel(screen, left, "Scores_New_Columns", "Additional Columns:")
		leftL, leftR = self.addTwoColumnLayout(screen, left, "Scores_Power_Column")
		self.addCheckboxTextDropdown(screen, leftL, leftR, "Scores__Power", "Scores__PowerFormula", "LAYOUT_LEFT")
		self.addIntDropdown(screen, leftL, leftR, "Scores__PowerDecimals", True, "LAYOUT_LEFT")
		self.addColorDropdown(screen, leftL, leftR, "Scores__PowerColor", True, "LAYOUT_LEFT")
		self.addFloatDropdown(screen, leftL, leftR, "Scores__PowerHighRatio", True, "LAYOUT_LEFT")
		self.addColorDropdown(screen, leftL, leftR, "Scores__PowerHighColor", True, "LAYOUT_LEFT")
		self.addFloatDropdown(screen, leftL, leftR, "Scores__PowerLowRatio", True, "LAYOUT_LEFT")
		self.addColorDropdown(screen, leftL, leftR, "Scores__PowerLowColor", True, "LAYOUT_LEFT")
		
		self.addSpacer(screen, space, "Scores_New_Columns", 3)
		
		self.addSpacer(screen, center, "Scores_New_Columns")
		self.addCheckbox(screen, center, "Scores__Delta")
		self.addCheckbox(screen, center, "Scores__DeltaIncludeCurrent")
		self.addLabel(screen, center, "Scores_Icons", "Icons:")
		self.addCheckbox(screen, center, "Scores__Attitude")
		self.addCheckbox(screen, center, "Scores__WorstEnemy")
		self.addCheckbox(screen, center, "Scores__WHEOOH")
		
		self.addLabel(screen, right, "Scores_Grid", "Advanced Layout:")
		self.addCheckbox(screen, right, "Scores__AlignIcons")
		self.addCheckbox(screen, right, "Scores__GroupVassals")
		self.addCheckbox(screen, right, "Scores__LeftAlignName")
		self.addCheckbox(screen, right, "Scores__ResearchIcons")
		self.addLabel(screen, right, "Scores_Order", "Column Order:")
		self.addTextEdit(screen, None, right, "Scores__DisplayOrder")
		self.addIntDropdown(screen, right, right, "Scores__DefaultSpacing", True)
