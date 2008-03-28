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
		self.addOption(OptionList("Main_GPBar_Types",
								  "Screens", "GP Progress Bar Types", 0,
								  "GP Bar Types",
								  "Determines how many GP types to display in the GP Progress Bar. The \"Maximum\" setting also displays the percent chance for each.",
								  ['None', 'One', 'Maximum'], None,
								  InterfaceDirtyBits.GameData_DIRTY_BIT))
		self.addOption(Option("Main_Combat_Counter",
							  "Screens", "Combat Counter", True,
							  "Combat Experience",
							  "When checked, displays Combat Experience to track next Great General.",
							  InterfaceDirtyBits.GameData_DIRTY_BIT))
		
		self.addOption(Option("Main_CityArrows",
							  "Screens", "City Cycle Arrows", True,
							  "City Cycle Arrows",
							  "When checked, displays arrows to cycle through cities above your civ's flag.",
							  InterfaceDirtyBits.MiscButtons_DIRTY_BIT))

		self.addOption(Option("Unit_Promo_Available",
							  "PlotList", "Promo Available", True,
							  "Promotion Available",
							  "When checked, puts blue border around units that have a promotion available.",
							  InterfaceDirtyBits.PlotListButtons_DIRTY_BIT))
		self.addOption(Option("Unit_Actions",
							  "PlotList", "Unit Actions", True,
							  "Unit Actions",
							  "When checked, puts unit actions text on unit icons.",
							  InterfaceDirtyBits.PlotListButtons_DIRTY_BIT))
		self.addOption(Option("Great_General",
							  "PlotList", "Great General", True,
							  "Great General",
							  "When checked, puts a little gold star on an Great General icon.",
							  InterfaceDirtyBits.PlotListButtons_DIRTY_BIT))

		self.addOption(Option("CDA_Enabled",
							  "Screens", "CustDomAdv", True,
							  "Customizable",
							  "When checked, uses the Customizable Domestic Advisor (requires restart)."))

		self.addOption(Option("EFA_Glance",
							  "Screens", "EFA Glance", True,
							  "Glance Tab",
							  "When checked, displays the 'Glance' tab on the Exotic Foreign Advisor screen."))
		self.addOption(Option("EFA_Glance_Smilies",
							  "Screens", "EFA Glance Smilies", True,
							  "Glance Tab Smilies",
							  "When checked, the 'Glance' tab shows Smilies (attitude icons)."))

		self.addOption(Option("Tech_GPPrefs",
							  "Screens", "GP Tech Prefs", True,
							  "Great Person Research",
							  "When checked, displays the technology each type of great person will research."))
		self.addOption(Option("TechScreen_Wide",
							  "Screens", "Wide Tech Screen", True,
							  "Wide Tech Screen",
							  "When checked, the width of the tech screen will be linked to your screen resolution (requires reload to take effect)."))

		self.addOption(Option("Sevopedia_Enabled",
							  "Screens", "Sevopedia", True,
							  "Enabled",
							  "When checked, uses the Sevopedia (requires restart)."))
		self.addOption(Option("Sevopedia_Sort",
							  "Screens", "Sevopedia Sort", True,
							  "Sort Lists",
							  "When checked, the lists of units, buildings, technologies, etc. are sorted."))

	def isShowOptionsKeyReminder(self):
		return self.getBoolean('Main_OptionsKey')

	def isShowGPProgressBar(self):
		return self.getBoolean('Main_GPBar')

	def getGPBarPercents(self):
		return self.getInt('Main_GPBar_Types')

	def isGPBarTypesNone(self):
		return self.getGPBarPercents() == 0

	def isGPBarTypesOne(self):
		return self.getGPBarPercents() == 1

	def isGPBarTypesMax(self):
		return self.getGPBarPercents() == 2

	def isShowCombatCounter(self):
		return self.getBoolean('Main_Combat_Counter')
	

	def isShowCityCycleArrows(self):
		return self.getBoolean('Main_CityArrows')
	

	def isShowUnitPromo(self):
		return self.getBoolean('Unit_Promo_Available')

	def isShowUnitActions(self):
		return self.getBoolean('Unit_Actions')

	def isShowGreatGeneral(self):
		return self.getBoolean('Great_General')


	def isCustDomAdv(self):
		return self.getBoolean('CDA_Enabled')

	
	def isShowGlance(self):
		return self.getBoolean("EFA_Glance")

	def isShowGlanceSmilies(self):
		return self.getBoolean("EFA_Glance_Smilies")


	def isShowGPTechPrefs(self):
		return self.getBoolean("Tech_GPPrefs")


	def isSevopedia(self):
		return self.getBoolean('Sevopedia_Enabled')

	def isSortSevopedia(self):
		return self.getBoolean('Sevopedia_Sort')

	def isWideTechScreen(self):
		return self.getBoolean('TechScreen_Wide')

# The singleton BugScreensOptions object

__g_options = BugScreensOptions()
def getOptions():
	return __g_options
