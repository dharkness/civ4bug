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
		
		self.addCheckbox(screen, upperPanel, "NJAGCM_Enabled")
		
		self.addCheckbox(screen, upperPanel, "NJAGCM_ShowEra")
		self.addCheckbox(screen, upperPanel, "NJAGCM_ShowEraColor")
		
		screen.attachHSeparator(upperPanel, upperPanel + "Sep")
		leftPanel, rightPanel = self.addTwoColumnLayout(screen, upperPanel)
		
		self.addCheckbox(screen, leftPanel, "NJAGCM_AlternateText")
		self.addIntDropdown(screen, rightPanel, rightPanel, "NJAGCM_AltTiming")
		
		screen.attachLabel(leftPanel, "NJAGC_RegularLabel", "Standard View:")
		self.addCheckbox(screen, leftPanel, "NJAGCM_ShowTime")
		self.addCheckbox(screen, leftPanel, "NJAGCM_ShowCompletedTurns")
		self.addCheckbox(screen, leftPanel, "NJAGCM_ShowTotalTurns")
		self.addCheckbox(screen, leftPanel, "NJAGCM_ShowCompletedPercent")
		self.addCheckbox(screen, leftPanel, "NJAGCM_ShowDate")
		
		screen.attachLabel(rightPanel, "NJAGC_AltLabel", "Alternate View:")
		self.addCheckbox(screen, rightPanel, "NJAGCM_ShowAltTime")
		self.addCheckbox(screen, rightPanel, "NJAGCM_ShowAltCompletedTurns")
		self.addCheckbox(screen, rightPanel, "NJAGCM_ShowAltTotalTurns")
		self.addCheckbox(screen, rightPanel, "NJAGCM_ShowAltCompletedPercent")
		self.addCheckbox(screen, rightPanel, "NJAGCM_ShowAltDate")
