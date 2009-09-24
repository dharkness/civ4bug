## BugNJAGCOptionsTab
## Tab for the BUG NJAGC Options
## BUG Mod - Copyright 2007

from CvPythonExtensions import *
import BugOptionsTab
import BugNJAGCOptions

gc = CyGlobalContext()
localText = CyTranslator()
BugNJAGC = BugNJAGCOptions.getOptions()

class BugNJAGCOptionsTab(BugOptionsTab.BugOptionsTab):
	"BUG NJAGC Options Screen Tab"
	
	def __init__(self, screen):
		BugOptionsTab.BugOptionsTab.__init__(self, "NJAGC", "Clock")

	def create(self, screen):
		tab = self.createTab(screen)
		panel = self.createMainPanel(screen)
		upperPanel = self.addOneColumnLayout(screen, panel)
		
		leftPanel, centerPanel, rightPanel = self.addThreeColumnLayout(screen, upperPanel, "EraColors")
		
		self.addCheckbox(screen, leftPanel, "NJAGCM_Enabled")
		self.addCheckbox(screen, leftPanel, "NJAGCM_ShowEra")
		self.addCheckbox(screen, leftPanel, "NJAGCM_ShowEraColor")
		self.addColorDropdown(screen, centerPanel, centerPanel, "NJAGCM_Color_ERA_ANCIENT", True)
		self.addColorDropdown(screen, centerPanel, centerPanel, "NJAGCM_Color_ERA_CLASSICAL", True)
		self.addColorDropdown(screen, centerPanel, centerPanel, "NJAGCM_Color_ERA_MEDIEVAL", True)
		self.addColorDropdown(screen, centerPanel, centerPanel, "NJAGCM_Color_ERA_RENAISSANCE", True)
		self.addColorDropdown(screen, rightPanel, rightPanel, "NJAGCM_Color_ERA_INDUSTRIAL", True)
		self.addColorDropdown(screen, rightPanel, rightPanel, "NJAGCM_Color_ERA_MODERN", True)
		self.addColorDropdown(screen, rightPanel, rightPanel, "NJAGCM_Color_ERA_FUTURE", True)
		
		screen.attachHSeparator(upperPanel, upperPanel + "Sep")
		leftPanel, rightPanel = self.addTwoColumnLayout(screen, upperPanel, "Views")
		
		self.addCheckbox(screen, leftPanel, "NJAGCM_AlternateText")
		self.addIntDropdown(screen, rightPanel, rightPanel, "NJAGCM_AltTiming")
		
		self.addLabel(screen, leftPanel, "NJAGC_Regular", "Standard View:")
		self.addCheckbox(screen, leftPanel, "NJAGCM_ShowTime")
		self.addCheckbox(screen, leftPanel, "NJAGCM_ShowCompletedTurns")
		self.addCheckbox(screen, leftPanel, "NJAGCM_ShowTotalTurns")
		self.addCheckbox(screen, leftPanel, "NJAGCM_ShowCompletedPercent")
		self.addCheckbox(screen, leftPanel, "NJAGCM_ShowDate")
		
		self.addLabel(screen, rightPanel, "NJAGC_Alternate", "Alternate View:")
		self.addCheckbox(screen, rightPanel, "NJAGCM_ShowAltTime")
		self.addCheckbox(screen, rightPanel, "NJAGCM_ShowAltCompletedTurns")
		self.addCheckbox(screen, rightPanel, "NJAGCM_ShowAltTotalTurns")
		self.addCheckbox(screen, rightPanel, "NJAGCM_ShowAltCompletedPercent")
		self.addCheckbox(screen, rightPanel, "NJAGCM_ShowAltDate")