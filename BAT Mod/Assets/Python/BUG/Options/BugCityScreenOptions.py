## BugCityScreenOptions
## Facade for accessing City Screen options
## BUG Mod - Copyright 2007

from CvPythonExtensions import *
from BugOptions import OptionsFacade, Option, OptionList

class BugCityScreenOptions(OptionsFacade):

	def __init__(self):
		OptionsFacade.__init__(self)
		self.addOption(Option("City_RawCommerce",
							  "City Screen", "Raw Commerce", False,
							  "Raw Commerce / Production",
							  "When checked, the raw commerce and production are displayed above the trade routes.",
							  InterfaceDirtyBits.CityScreen_DIRTY_BIT))
		self.addOption(Option("City_CultureTurns",
							  "City Screen", "Culture Turns", False,
							  "Culture Turns",
							  "When checked, displays the number of turns until the city's borders expand.",
							  InterfaceDirtyBits.CityScreen_DIRTY_BIT))
		self.addOption(Option("City_GreatPersonTurns",
							  "City Screen", "Great Person Turns", False,
							  "Great Person Turns",
							  "When checked, displays the number of turns until the city will produce a Great Person.",
							  InterfaceDirtyBits.CityScreen_DIRTY_BIT))
		self.addOption(Option("City_StackSpecialists",
							  "City Screen", "Specialist Stacker", False,
							  "Stack Specialists",
							  "When checked, the specialists are displayed in a more compact form.",
							  InterfaceDirtyBits.CityScreen_DIRTY_BIT))
		self.addOption(Option("City_Anger_Counter",
							  "Screens", "Anger Counter", True,
							  "Anger Counter",
							  "When checked, puts anger countdown on city screen.",
							  InterfaceDirtyBits.MiscButtons_DIRTY_BIT))

	def isShowRawCommerce(self):
		return self.getBoolean('City_RawCommerce')

	def isShowCultureTurns(self):
		return self.getBoolean('City_CultureTurns')

	def isShowGreatPersonTurns(self):
		return self.getBoolean('City_GreatPersonTurns')

	def isStackSpecialists(self):
		return self.getBoolean('City_StackSpecialists')

	def isShowAngerCounter(self):
		return self.getBoolean('City_Anger_Counter')


# The singleton BugCityScreenOptions object

__g_options = BugCityScreenOptions()
def getOptions():
	return __g_options