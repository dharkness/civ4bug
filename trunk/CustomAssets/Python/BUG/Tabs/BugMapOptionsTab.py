## BugMapOptionsTab
##
## Tab for the BUG Map Options.
##
## Copyright (c) 2009 The BUG Mod.
##
## Author: EmperorFool

import BugOptionsTab

class BugMapOptionsTab(BugOptionsTab.BugOptionsTab):
	"BUG Nap Options Screen Tab"
	
	def __init__(self, screen):
		BugOptionsTab.BugOptionsTab.__init__(self, "Map", "Map")

	def create(self, screen):
		tab = self.createTab(screen)
		panel = self.createMainPanel(screen)
		column = self.addOneColumnLayout(screen, panel)
		
		left, right = self.addTwoColumnLayout(screen, column, "Top", True)
		
		self.addLabel(screen, left, "StrategyOverlay", "Strategy Layer:")
		self.addCheckbox(screen, left, "StrategyOverlay__Enabled")
		self.addCheckbox(screen, left, "StrategyOverlay__ShowDotMap")
		self.addCheckbox(screen, left, "StrategyOverlay__DotMapDrawDots")
		leftL, leftR = self.addTwoColumnLayout(screen, left, "DotMapBrightness")
		#self.addTextEdit(screen, leftL, leftR, "StrategyOverlay__DotMapDotIcon")
		self.addSlider(screen, leftL, leftR, "StrategyOverlay__DotMapBrightness", False, False, False, "up", 0, 100)
		self.addSlider(screen, leftL, leftR, "StrategyOverlay__DotMapHighlightBrightness", False, False, False, "up", 0, 100)
		
		
		self.addCheckbox(screen, right, "MainInterface__FieldOfView")
		self.addCheckbox(screen, right, "MainInterface__FieldOfView_Remember", True)
		
		self.addSpacer(screen, right, "Map2")
		self.addLabel(screen, right, "Misc", "Misc:")
		self.addCheckbox(screen, right, "EventSigns__Enabled")
		self.addCheckbox(screen, right, "CityBar__AirportIcons")
		
		
		screen.attachHSeparator(column, column + "Sep1")
		
		self.addLabel(screen, column, "MapFinder", "MapFinder:")
		self.addCheckbox(screen, column, "MapFinder__Enabled")
		self.addTextEdit(screen, column, column, "MapFinder__Path")
		
		left, right = self.addTwoColumnLayout(screen, column, "MapFinder", True)
		leftL, leftR = self.addTwoColumnLayout(screen, left, "MapFinderDelays")
		self.addFloatDropdown(screen, leftL, leftR, "MapFinder__RegenerationDelay")
		self.addFloatDropdown(screen, leftL, leftR, "MapFinder__SkipDelay")
		self.addFloatDropdown(screen, leftL, leftR, "MapFinder__SaveDelay")
		
		rightL, rightR = self.addTwoColumnLayout(screen, right, "MapFinderLimits")
		self.addTextEdit(screen, rightL, rightR, "MapFinder__RuleFile")
		self.addTextEdit(screen, rightL, rightR, "MapFinder__RegenerationLimit")
		self.addTextEdit(screen, rightL, rightR, "MapFinder__SaveLimit")
