## BugTechScreenOptions
## Facade for accessing TechChooser options
## BUG Mod - Copyright 2007

from CvPythonExtensions import *
from BugOptions import OptionsFacade, Option, OptionList

class BugTechScreenOptions(OptionsFacade):

	def __init__(self):
		OptionsFacade.__init__(self)
		self.addOption(Option("Tech_GPPrefs",
							  "Tech", "GP Tech Prefs", False,
							  "Great Person Research",
							  "When checked, displays the technology each type of great person will research."))


	def isShowGPTechPrefs(self):
		return self.getBoolean("Tech_GPPrefs")


# The singleton BugTechScreenOptions object

__g_options = BugTechScreenOptions()
def getOptions():
	return __g_options
