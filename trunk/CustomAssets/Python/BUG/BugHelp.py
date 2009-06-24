## BugHelp
##
## Opens BUG's help file, "BUG Help.chm".
##
## TODO:
##   Move to configuration XML
##   Support multiple help files and shortcuts
##
## Copyright (c) 2008 The BUG Mod.
##
## Author: EmperorFool

from CvPythonExtensions import *
import Popup as PyPopup
import BugPath
import BugUtil
import os

def launch(argsList=None):
	"Opens the mod's help file externally if it can be found or displays an error alert"
	sLang = ["ENG", "FRA", "DEU", "ITA", "ESP"]
	name = "BUG Mod Help-%s.chm" % (sLang[CyGame().getCurrentLanguage()])
	file = BugPath.findInfoFile(name)
	if file:
		message = BugUtil.getPlainText("TXT_KEY_BUG_HELP_OPENING")
		CyInterface().addImmediateMessage(message, "")
		os.startfile(file)
		return True
	else:
		popup = PyPopup.PyPopup()
		popup.setHeaderString(BugUtil.getPlainText("TXT_KEY_BUG_HELP_MISSING_TITLE"))
		popup.setBodyString(BugUtil.getText("TXT_KEY_BUG_HELP_MISSING_BODY", (name,)))
		popup.launch()
		return False
