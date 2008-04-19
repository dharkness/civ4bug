## BugScoresOptionsTab
## Tab for the BUG Scoreboard Options
## BUG Mod - Copyright 2007

import BugOptionsTab

class BugScoreOptionsTab(BugOptionsTab.BugOptionsTab):
    "BUG Scores Options Screen Tab"
    
    def __init__(self, screen):
        BugOptionsTab.BugOptionsTab.__init__(self, "Scores", "Scoreboard")

    def create(self, screen):
        tab = self.createTab(screen)
        panel = self.createMainPanel(screen)
        left, center, right = self.addThreeColumnLayout(screen, panel, panel, True)
        
        self.addTextDropdown(screen, left, left, "Scores_DisplayName")
        self.addCheckbox(screen, left, "Scores_Attitude")
        
        self.addLabel(screen, left, "Scores_Dead_Civs", "Dead Civilizations:")
        self.addCheckbox(screen, left, "Scores_ShowDead")
        self.addCheckbox(screen, left, "Scores_TagDead")
        self.addCheckbox(screen, left, "Scores_GreyDead")
        
#        self.addLabel(screen, center, "Scores_Power", "Power Ratio:")
        self.addCheckbox(screen, center, "Scores_Power")
        self.addColorDropdown(screen, center, center, "Scores_PowerColor", True)
        self.addFloatDropdown(screen, center, center, "Scores_PowerGoodRatio", True)
        self.addColorDropdown(screen, center, center, "Scores_PowerGoodColor", True)
        self.addFloatDropdown(screen, center, center, "Scores_PowerBadRatio", True)
        self.addColorDropdown(screen, center, center, "Scores_PowerBadColor", True)
        
        self.addLabel(screen, right, "Scores_Grid", "Advanced Layout:")
        self.addCheckbox(screen, right, "Scores_AlignIcons")
        self.addLabel(screen, right, "Scores_Order", "Column Order:")
        self.addTextEdit(screen, None, right, "Scores_DisplayOrder")
        self.addCheckbox(screen, right, "Scores_LeftAlignName")
        self.addCheckbox(screen, right, "Scores_ResearchIcons")
