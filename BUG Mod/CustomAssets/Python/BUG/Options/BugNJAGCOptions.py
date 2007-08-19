## BugNJAGCOptions
## Facade for accessing NJAGC options
## BUG Mod - Copyright 2007

from BugOptions import OptionsFacade, Option, OptionList

class BugNJAGCOptions(OptionsFacade):

	def __init__(self):
		OptionsFacade.__init__(self)
		self.addOption(Option("NJAGCM_Enabled",
						 "NJAGCM", "Enabled", True,
						 "Enable Not Just Another Game Clock Mod",
						 "When checked, the other settings on this tab affect the game clock."))
		self.addOption(Option("NJAGCM_ShowEra",
						 "NJAGCM", "Show Era", True,
						 "Display Era Name",
						 "When checked, the name of the current era is displayed."))
		
		self.addOption(Option("NJAGCM_ShowEraColor",
						 "NJAGCM", "Show Reflect Era In Turn Color", True,
						 "Use Era-Related Colors",
						 "When checked, the game date and era are displayed using a color for each era."))
		self.addOption(Option("NJAGCM_Color_ERA_ANCIENT",
						 "NJAGCM", "ERA_ANCIENT", "COLOR_RED",
						 "Ancient Era",
						 "Color to use for the Ancient era."))
		self.addOption(Option("NJAGCM_Color_ERA_CLASSICAL",
						 "NJAGCM", "ERA_CLASSICAL", "COLOR_YELLOW",
						 "Classical Era",
						 "Color to use for the Classical era."))
		self.addOption(Option("NJAGCM_Color_ERA_MEDIEVAL",
						 "NJAGCM", "ERA_MEDIEVAL", "COLOR_GREEN",
						 "Medieval Era",
						 "Color to use for the Medieval era."))
		self.addOption(Option("NJAGCM_Color_ERA_RENAISSANCE",
						 "NJAGCM", "ERA_RENAISSANCE", "COLOR_CYAN",
						 "Renaissance Era",
						 "Color to use for the Renaissance era."))
		self.addOption(Option("NJAGCM_Color_ERA_INDUSTRIAL",
						 "NJAGCM", "ERA_INDUSTRIAL", "COLOR_BLUE",
						 "Industrial Era",
						 "Color to use for the Industrial era."))
		self.addOption(Option("NJAGCM_Color_ERA_MODERN",
						 "NJAGCM", "ERA_MODERN", "COLOR_MAGENTA",
						 "Modern Era",
						 "Color to use for the Modern era."))
		self.addOption(Option("NJAGCM_Color_ERA_FUTURE",
						 "NJAGCM", "ERA_FUTURE", "COLOR_WHITE",
						 "Future Era",
						 "Color to use for the Future era."))
		
		self.addOption(Option("NJAGCM_ShowTime",
						 "NJAGCM", "Show Game Clock", False,
						 "Clock",
						 "When checked, the real time is displayed."))
		self.addOption(Option("NJAGCM_ShowCompletedTurns",
						 "NJAGCM", "Show Game Completed Turns", True,
						 "Completed Turns",
						 "When checked, the number of turns completed is displayed."))
		self.addOption(Option("NJAGCM_ShowTotalTurns",
						 "NJAGCM", "Show Game Total Turns", True,
						 "Total Turns (Time Victory Only)",
						 "When checked, the total turns in the game is displayed."))
		self.addOption(Option("NJAGCM_ShowCompletedPercent",
						 "NJAGCM", "Show Game Completed Percent", False,
						 "Completed Percentage",
						 "When checked, the completed percentage is displayed."))
		self.addOption(Option("NJAGCM_ShowDate",
						 "NJAGCM", "Show Turns", True,
						 "In-game Date",
						 "When checked, the in-game date is displayed."))
		
		self.addOption(Option("NJAGCM_AlternateText",
						 "NJAGCM", "Alternate Views", False,
						 "Alternate Game Clock",
						 "When checked, the game clock switches between two views: standard and alternate."))
		self.addOption(OptionList("NJAGCM_AltTiming",
							 "NJAGCM", "Alternating Time", 5,
							 "Period (in seconds)",
							 "Select the time each view of the game clock is displayed when alternating is enabled.",
							 [2, 5, 10, 15, 30, 45, 60, 300, 600]))
		
		self.addOption(Option("NJAGCM_ShowAltTime",
						 "NJAGCM", "Alternate Show Game Clock", False,
						 "Clock",
						 "When checked, the real time is displayed."))
		self.addOption(Option("NJAGCM_ShowAltCompletedTurns",
						 "NJAGCM", "Alternate Show Game Completed Turns", False,
						 "Completed Turns",
						 "When checked, the number of turns completed is displayed."))
		self.addOption(Option("NJAGCM_ShowAltTotalTurns",
						 "NJAGCM", "Alternate Show Game Total Turns", False,
						 "Total Turns (Time Victory Only)",
						 "When checked, the total turns in the game is displayed."))
		self.addOption(Option("NJAGCM_ShowAltCompletedPercent",
						 "NJAGCM", "Alternate Show Game Completed Percent", True,
						 "Completed Percentage",
						 "When checked, the completed percentage is displayed."))
		self.addOption(Option("NJAGCM_ShowAltDate",
						 "NJAGCM", "Alternate Show Turns", True,
						 "In-game Date",
						 "When checked, the in-game date is displayed."))

	def isEnabled(self):
		return self.getBoolean('NJAGCM_Enabled')

	def isShowEra(self):
		return self.getBoolean('NJAGCM_ShowEra')

	def isUseEraColor(self):
		return self.getBoolean('NJAGCM_ShowEraColor')
	
	def getEraColor(self, era):
		return self.getString('NJAGCM_Color_' + era)


	def isShowTime(self):
		return self.getBoolean('NJAGCM_ShowTime')

	def isShowGameTurn(self):
		return self.getBoolean('NJAGCM_ShowCompletedTurns')

	def isShowTotalTurns(self):
		return self.getBoolean('NJAGCM_ShowTotalTurns')

	def isShowPercentComplete(self):
		return self.getBoolean('NJAGCM_ShowCompletedPercent')

	def isShowDateGA(self):
		return self.getBoolean('NJAGCM_ShowDate')


	def isAlternateTimeText(self):
		return self.getBoolean('NJAGCM_AlternateText')

	def getAlternatePeriod(self):
		return self.getInt('NJAGCM_AltTiming')


	def isShowAltTime(self):
		return self.getBoolean('NJAGCM_ShowAltTime')

	def isShowAltGameTurn(self):
		return self.getBoolean('NJAGCM_ShowAltCompletedTurns')

	def isShowAltTotalTurns(self):
		return self.getBoolean('NJAGCM_ShowAltTotalTurns')

	def isShowAltPercentComplete(self):
		return self.getBoolean('NJAGCM_ShowAltCompletedPercent')

	def isShowAltDateGA(self):
		return self.getBoolean('NJAGCM_ShowAltDate')


# The singleton BugNJAGCOptions object

__g_options = BugNJAGCOptions()
def getOptions():
	return __g_options
