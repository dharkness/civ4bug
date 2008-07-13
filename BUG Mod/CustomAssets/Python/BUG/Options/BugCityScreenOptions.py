## BugCityScreenOptions
## Facade for accessing City Screen options
## BUG Mod - Copyright 2007

from CvPythonExtensions import *
from BugOptions import OptionsFacade, Option, OptionList

class BugCityScreenOptions(OptionsFacade):

	def __init__(self):
		OptionsFacade.__init__(self)
		self.addOption(Option("City_RawYields",
							  "City Screen", "Raw Yields", True,
							  "Raw Yields",
							  "When checked, the raw yields (food, production and commerce) can be displayed in the trade routes table.",
							  InterfaceDirtyBits.CityScreen_DIRTY_BIT))
		self.addOption(Option("City_WhipAssist",
							  "City Screen", "Whip Assist", True,
							  "Whip Assist",
							  "When checked, displays the population cost and overflow production for whipping and the gold cost for buying the item being produced.",
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
		self.addOption(Option("City_GreatPersonInfo",
							  "City Screen", "Great Person Info", False,
							  "Great Person Info",
							  "When checked, displays additional Great Person Information.",
							  InterfaceDirtyBits.CityScreen_DIRTY_BIT))

		self.addOption(OptionList("City_Specialists",
								  "City Screen", "City Specialists", 0,
								  "City Specialists",
								  "Determines how specialists are displayed.\n\
The \"Default\" setting shows the specialists using the vanilla BtS format. \
The \"Stacker\" setting shows the specialists stacked using the Stacked Specialist mod. \
The \"Chevron\" setting shows the specialists grouped into 5 (single cheron), 10 (capped chevron) and 20 (boxed capped chevron) format. ",
								  ['Default', 'Stacker', 'Chevron'], None,
								  InterfaceDirtyBits.CityScreen_DIRTY_BIT))

		self.addOption(Option("City_Anger_Counter",
							  "Screens", "Anger Counter", True,
							  "Anger Counter",
							  "When checked, puts anger countdown on city screen.",
							  InterfaceDirtyBits.CityScreen_DIRTY_BIT))

	def isShowRawYields(self):
		return self.getBoolean('City_RawYields')

	def isShowWhipAssist(self):
		return self.getBoolean('City_WhipAssist')

	def isShowCultureTurns(self):
		return self.getBoolean('City_CultureTurns')

	def isShowGreatPersonTurns(self):
		return self.getBoolean('City_GreatPersonTurns')

	def isShowCityGreatPersonInfo(self):
		return self.getBoolean('City_GreatPersonInfo')

	def isShowAngerCounter(self):
		return self.getBoolean('City_Anger_Counter')

	def getCitySpecialist(self):
		return self.getInt('City_Specialists')

	def isCitySpecialist_Default(self):
		return self.getCitySpecialist() == 0

	def isCitySpecialist_Stacker(self):
		return self.getCitySpecialist() == 1

	def isCitySpecialist_Chevron(self):
		return self.getCitySpecialist() == 2


# The singleton BugCityScreenOptions object

__g_options = BugCityScreenOptions()
def getOptions():
	return __g_options
