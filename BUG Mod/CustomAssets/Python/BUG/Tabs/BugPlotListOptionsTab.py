## BugScoresOptionsTab
## Tab for the BUG Scoreboard Options
## BUG Mod - Copyright 2007

import BugOptionsTab

class BugPlotListOptionsTab(BugOptionsTab.BugOptionsTab):
    "Plot List Enhancement Tab"
    
    def __init__(self, screen):
        BugOptionsTab.BugOptionsTab.__init__(self, "PLE", "PlotList")

    def create(self, screen):
        tab = self.createTab(screen)
        panel = self.createMainPanel(screen)
        left, center = self.addTwoColumnLayout(screen, panel, panel, True)
        
        self.addCheckbox(screen, left, "PLE_Mission_info")
        self.addSpacer(screen,left,"PLE_Movement")
        
        self.addCheckbox(screen, left, "PLE_Move_Bar")
        self.addColorDropdown(screen, left, left, "PLE_Full_Movement_Color")
        self.addColorDropdown(screen, left, left, "PLE_Has_Moved_Color")
        self.addSpacer(screen,left,"PLE_Health")
        
        
        self.addCheckbox(screen, left, "PLE_Health_Bar")
        self.addColorDropdown(screen, left, left, "PLE_Healthy_Color")
        self.addColorDropdown(screen, left, left, "PLE_Wounded_Color")
                        
        self.addColorDropdown(screen, center, center, "PLE_Unit_Name_Color")
        self.addSpacer(screen,center,"PLE_Upgrade")
        
        self.addColorDropdown(screen, center, center, "PLE_Upgrade_Possible_Color")
        self.addColorDropdown(screen, center, center, "PLE_Upgrade_Not_Possible_Color")
        self.addSpacer(screen,center,"PLE_Specialties")
        
        self.addColorDropdown(screen, center, center, "PLE_Promotion_Specialties_Color")
        self.addColorDropdown(screen, center, center, "PLE_Unit_Type_Specialties_Color")
 