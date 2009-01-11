## BugGeneralOptionsTab
##
## Tab for the BUG General Options (Main and City Screens).
##
## Copyright (c) 2007-2008 The BUG Mod.
##
## Author: EmperorFool

import BugOptionsTab
import CvModName

class BugGeneralOptionsTab(BugOptionsTab.BugOptionsTab):
	"BUG General Options Screen Tab"
	
	def __init__(self, screen):
		BugOptionsTab.BugOptionsTab.__init__(self, "General", "General")

	def create(self, screen):
		tab = self.createTab(screen)
		panel = self.createMainPanel(screen)
		column = self.addOneColumnLayout(screen, panel)
		
		left, center, right = self.addThreeColumnLayout(screen, column, "Top", True)
		
		self.addLabel(screen, left, "MainInterface", "MAIN INTERFACE")
		self.addCheckbox(screen, left, "MainInterface__GPBar")
		self.addTextDropdown(screen, left, left, "MainInterface__GPBar_Types", True)
		self.addCheckbox(screen, left, "MainInterface__Combat_Counter")
		
		screen.attachHSeparator(left, left + "SepL1")
		
		self.addCheckbox(screen, left, "MainInterface__FieldOfView")
		self.addCheckbox(screen, left, "MainInterface__FieldOfView_Remember")
		
		screen.attachHSeparator(left, left + "SepL2")
		
		self.addLabel(screen, left, "TechWindow", "Tech Splash Screen:")
		self.addTextDropdown(screen, left, left, "TechWindow__ViewType", True)
		self.addCheckbox(screen, left, "TechWindow__CivilopediaText")
		
		screen.attachHSeparator(left, left + "SepL3")
		
		self.addLabel(screen, left, "Misc", "Misc:")
		self.addCheckbox(screen, left, "MainInterface__CityArrows")
		self.addCheckbox(screen, left, "EventSigns__Enabled")
		self.addCheckbox(screen, left, "MainInterface__MinMax_Commerce")
		
		
		self.addLabel(screen, center, "CityScreen", "CITY SCREEN")
		self.addCheckbox(screen, center, "CityScreen__WhipAssist")
		self.addCheckbox(screen, center, "CityScreen__WhipAssistOverflowCountCurrentProduction")
		self.addCheckbox(screen, center, "CityScreen__Anger_Counter")
		
		screen.attachHSeparator(center, center + "SepC1")
		
		self.addCheckbox(screen, center, "CityScreen__RawYields")
		self.addTextDropdown(screen, center, center, "CityScreen__RawYields_View", True)
		
		screen.attachHSeparator(center, center + "SepC2")
		
		self.addLabel(screen, center, "Misc", "Misc:")
		self.addCheckbox(screen, center, "CityScreen__CultureTurns")
		self.addCheckbox(screen, center, "CityScreen__GreatPersonTurns")
		self.addCheckbox(screen, center, "CityScreen__GreatPersonInfo")
		self.addCheckbox(screen, center, "CityScreen__FoodAssist")
		self.addCheckbox(screen, center, "MainInterface__ProgressBarsTickMarks")
		self.addTextDropdown(screen, center, center, "CityScreen__Specialists", True)
		
		
		self.addLabel(screen, right, "StrategyOverlay", "STRATEGY LAYER")
		self.addCheckbox(screen, right, "StrategyOverlay__Enabled")
		
		self.addSpacer(screen, right, "StrategyOverlay_DotMap")
		self.addCheckbox(screen, right, "StrategyOverlay__ShowDotMap")
		self.addCheckbox(screen, right, "StrategyOverlay__DotMapDrawDots")
		rightLeft, rightRight = self.addTwoColumnLayout(screen, right, right)
		#self.addTextEdit(screen, rightLeft, rightRight, "StrategyOverlay__DotMapDotIcon")
		self.addSlider(screen, rightLeft, rightRight, "StrategyOverlay__DotMapBrightness", 
				False, False, True, "up", 0, 100)
		self.addSlider(screen, rightLeft, rightRight, "StrategyOverlay__DotMapHighlightBrightness", 
				False, False, True, "up", 0, 100)
