## BugScreensOptions
## Facade for accessing various screen options
## BUG Mod - Copyright 2007

from CvPythonExtensions import *
from BugOptions import OptionsFacade, Option, OptionList

class BugScreensOptions(OptionsFacade):

	def __init__(self):
		OptionsFacade.__init__(self)
		self.addOption(Option("Main_OptionsKey",
							  "Screens", "Options Shortcut Reminder", True,
							  "Options Shortcut Reminder",
							  "When checked, displays a message about Ctrl-Alt-O when a game is started or loaded.",
							  InterfaceDirtyBits.GameData_DIRTY_BIT))
		self.addOption(Option("Main_GPBar",
							  "Screens", "GP Progress Bar", True,
							  "Great Person Progress Bar",
							  "When checked, displays the progress and city of the next Great Person.",
							  InterfaceDirtyBits.GameData_DIRTY_BIT))
		self.addOption(Option("Main_CityArrows",
							  "Screens", "City Cycle Arrows", True,
							  "City Cycle Arrows",
							  "When checked, displays arrows to cycle through cities above your civ's flag.",
							  InterfaceDirtyBits.MiscButtons_DIRTY_BIT))
		
		self.addOption(Option("CDA_Enabled",
							  "Screens", "CustDomAdv", True,
							  "Domestic: Customizable Domestic Advisor",
							  "When checked, uses the Customizable Domestic Advisor (requires restart)."))

		self.addOption(Option("Sevopedia_Enabled",
							  "Screens", "Sevopedia", True,
							  "Sevopedia",
							  "When checked, uses the Sevopedia (requires restart)."))
		self.addOption(Option("Sevopedia_Sort",
							  "Screens", "Sevopedia Sort", True,
							  "Sort Lists",
							  "When checked, the lists of units, buildings, technologies, etc. are sorted."))

		self.addOption(Option("Tech_GPPrefs",
							  "Screens", "GP Tech Prefs", True,
							  "Tech: Great Person Research",
							  "When checked, displays the technology each type of great person will research."))

		self.addOption(Option("EFA_Glance",
							  "Screens", "EFA Glance", True,
							  "Foreign: Glance Tab",
							  "When checked, displays the 'Glance' tab on the Exotic Foreign Advisor screen."))


	def isShowOptionsKeyReminder(self):
		return self.getBoolean('Main_OptionsKey')

	def isShowGPProgressBar(self):
		return self.getBoolean('Main_GPBar')

	def isShowCityCycleArrows(self):
		return self.getBoolean('Main_CityArrows')


	def isCustDomAdv(self):
		return self.getBoolean('CDA_Enabled')

	def isSevopedia(self):
		return self.getBoolean('Sevopedia_Enabled')

	def isSortSevopedia(self):
		return self.getBoolean('Sevopedia_Sort')

	def isShowGPTechPrefs(self):
		return self.getBoolean("Tech_GPPrefs")


	def isShowGlance(self):
		return self.getBoolean("EFA_Glance")


# The singleton BugScreensOptions object

__g_options = BugScreensOptions()
def getOptions():
	return __g_options
