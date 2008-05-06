## BugHelp
## Opens the mod's help file, "<mod> Help.chm".
##
## Copyright (c) 2008 The BUG Mod.

from CvPythonExtensions import *
import Popup as PyPopup
import CvModName
from BugPath import findIniFile
import BugUtil
import os

def launch():
	"Opens the mod's help file externally if it can be found or displays an error alert"
	name = "%s Help.chm" % CvModName.getName()
	file = findIniFile(name)
	if file:
		message = BugUtil.getPlainText("TXT_KEY_BUG_HELP_OPENING")
		CyInterface().addImmediateMessage(message, "")
		os.startfile(file)
		return True
	else:
		title = BugUtil.getPlainText("TXT_KEY_BUG_HELP_MISSING_TITLE")
		body = BugUtil.getText("TXT_KEY_BUG_HELP_MISSING_BODY", (name,))
		popup = PyPopup.PyPopup()
		popup.setHeaderString(title)
		popup.setBodyString(body)
		popup.launch()
		return False
