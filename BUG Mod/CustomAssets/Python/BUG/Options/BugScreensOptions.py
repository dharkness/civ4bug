## BugScreensOptions
## Facade for accessing Customizable Domestic Advisor options
## BUG Mod - Copyright 2007

from BugOptions import OptionsFacade, Option, OptionList

class BugScreensOptions(OptionsFacade):

	def __init__(self):
		OptionsFacade.__init__(self)
		self.addOption(Option("Screens_CDA",
							  "Screens", "CustDomAdv", False,
							  "Customizable Domestic Advisor",
							  "When checked, uses the Customizable Domestic Advisor (requires restart)."))
		self.addOption(Option("Screens_Espionage",
							  "Screens", "BetterEspionage", False,
							  "Compact Espionage List",
							  "When checked, uses the Better Espionage Advisor."))

	def isCustDomAdv(self):
		return self.getBoolean('Screens_CDA')

	def isBetterEspionage(self):
		return self.getBoolean('Screens_Espionage')


# The singleton BugScreensOptions object

__g_options = BugScreensOptions()
def getOptions():
	return __g_options
