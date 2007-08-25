## BugScreensOptions
## Facade for accessing various screen options
## BUG Mod - Copyright 2007

from CvPythonExtensions import *
from BugOptions import OptionsFacade, Option, OptionList

class BugScreensOptions(OptionsFacade):

	def __init__(self):
		OptionsFacade.__init__(self)
		self.addOption(Option("CDA_Enabled",
							  "Screens", "CustDomAdv", False,
							  "Customizable Domestic Advisor",
							  "When checked, uses the Customizable Domestic Advisor (requires restart)."))

		self.addOption(Option("Tech_GPPrefs",
							  "Screens", "GP Tech Prefs", False,
							  "Great Person Research",
							  "When checked, displays the technology each type of great person will research."))


	def isCustDomAdv(self):
		return self.getBoolean('CDA_Enabled')


	def isShowGPTechPrefs(self):
		return self.getBoolean("Tech_GPPrefs")


# The singleton BugScreensOptions object

__g_options = BugScreensOptions()
def getOptions():
	return __g_options
