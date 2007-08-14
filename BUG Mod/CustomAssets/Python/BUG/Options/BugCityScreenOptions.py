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
		self.addOption(Option("City_StackSpecialists",
							  "City Screen", "SpecialistStacker", False,
							  "Stack Specialists",
							  "When checked, the specialists are displayed in a more compact form.",
							  InterfaceDirtyBits.CityScreen_DIRTY_BIT))

	def isShowRawCommerce(self):
		return self.getBoolean('City_RawCommerce')

	def isStackSpecialists(self):
		return self.getBoolean('City_StackSpecialists')


# The singleton BugCityScreenOptions object

__g_options = BugCityScreenOptions()
def getOptions():
	return __g_options
