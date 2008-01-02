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
        
        screen.attachLabel(left, "Scores_DeadCivsLabel", "Dead Civilizations:")
        screen.setControlFlag("Scores_DeadCivsLabel", "CF_LABEL_DEFAULTSIZE")
        self.addCheckbox(screen, left, "Scores_ShowDead")
        self.addCheckbox(screen, left, "Scores_TagDead")
        self.addCheckbox(screen, left, "Scores_GreyDead")
        
#        screen.attachLabel(center, "Scores_PowerLabel", "Power Ratio:")
#        screen.setControlFlag("Scores_PowerLabel", "CF_LABEL_DEFAULTSIZE")
        self.addCheckbox(screen, center, "Scores_Power")
        self.addColorDropdown(screen, center, center, "Scores_PowerColor", True)
        self.addFloatDropdown(screen, center, center, "Scores_PowerGoodRatio", True)
        self.addColorDropdown(screen, center, center, "Scores_PowerGoodColor", True)
        self.addFloatDropdown(screen, center, center, "Scores_PowerBadRatio", True)
        self.addColorDropdown(screen, center, center, "Scores_PowerBadColor", True)
        
        screen.attachLabel(right, "Scores_GridLabel", "Advanced Layout:")
        screen.setControlFlag("Scores_GridLabel", "CF_LABEL_DEFAULTSIZE")
        self.addCheckbox(screen, right, "Scores_AlignIcons")
        screen.attachLabel(right, "Scores_OrderLabel", "Column Order:")
        screen.setControlFlag("Scores_OrderLabel", "CF_LABEL_DEFAULTSIZE")
        self.addTextEdit(screen, None, right, "Scores_DisplayOrder")
        self.addCheckbox(screen, right, "Scores_LeftAlignName")
        self.addCheckbox(screen, right, "Scores_ResearchIcons")
