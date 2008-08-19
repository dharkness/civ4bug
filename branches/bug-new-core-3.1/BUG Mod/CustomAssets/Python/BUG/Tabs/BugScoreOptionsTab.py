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
        self.addCheckbox(screen, left, "Scores__Attitude")
        self.addCheckbox(screen, left, "Scores__WorstEnemy")
        
        self.addLabel(screen, left, "Scores_Dead_Civs", "Dead Civilizations:")
        self.addCheckbox(screen, left, "Scores__ShowDead")
        self.addCheckbox(screen, left, "Scores__TagDead")
        self.addCheckbox(screen, left, "Scores__GreyDead")
        
#        self.addLabel(screen, center, "Scores__Power", "Power Ratio:")
        self.addCheckbox(screen, center, "Scores__Power")
        self.addColorDropdown(screen, center, center, "Scores__PowerColor", True)
        self.addFloatDropdown(screen, center, center, "Scores__PowerGoodRatio", True)
        self.addColorDropdown(screen, center, center, "Scores__PowerGoodColor", True)
        self.addFloatDropdown(screen, center, center, "Scores__PowerBadRatio", True)
        self.addColorDropdown(screen, center, center, "Scores__PowerBadColor", True)
        
        self.addLabel(screen, right, "Scores_Grid", "Advanced Layout:")
        self.addCheckbox(screen, right, "Scores__AlignIcons")
        self.addLabel(screen, right, "Scores_Order", "Column Order:")
        self.addTextEdit(screen, None, right, "Scores__DisplayOrder")
        self.addCheckbox(screen, right, "Scores__LeftAlignName")
        self.addCheckbox(screen, right, "Scores__ResearchIcons")