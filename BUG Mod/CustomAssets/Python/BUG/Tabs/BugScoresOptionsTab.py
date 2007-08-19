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
        leftPanel, rightPanel = self.addTwoColumnLayout(screen, panel)
        
        self.addTextDropdown(screen, leftPanel, leftPanel, "Scores_DisplayName")
        self.addCheckbox(screen, leftPanel, "Scores_Attitude")
        
        screen.attachLabel(leftPanel, "Scores_DeadCivsLabel", "Dead Civilizations:")
        screen.setControlFlag("Scores_DeadCivsLabel", "CF_LABEL_DEFAULTSIZE")
        self.addCheckbox(screen, leftPanel, "Scores_ShowDead")
        self.addCheckbox(screen, leftPanel, "Scores_TagDead")
        self.addCheckbox(screen, leftPanel, "Scores_GreyDead")
        
#        screen.attachLabel(rightPanel, "Scores_PowerLabel", "Power Ratio:")
#        screen.setControlFlag("Scores_PowerLabel", "CF_LABEL_DEFAULTSIZE")
        self.addCheckbox(screen, rightPanel, "Scores_Power")
        self.addColorDropdown(screen, rightPanel, rightPanel, "Scores_PowerColor", True)
        self.addFloatDropdown(screen, rightPanel, rightPanel, "Scores_PowerGoodRatio", True)
        self.addColorDropdown(screen, rightPanel, rightPanel, "Scores_PowerGoodColor", True)
        self.addFloatDropdown(screen, rightPanel, rightPanel, "Scores_PowerBadRatio", True)
        self.addColorDropdown(screen, rightPanel, rightPanel, "Scores_PowerBadColor", True)
