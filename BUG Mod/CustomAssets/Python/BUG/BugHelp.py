## BugHelp
## Opens the BUG help file.
##
## Copyright (c) 2008 The BUG Mod.

from CvPythonExtensions import *
import Popup as PyPopup
from BugPath import findIniFile
import os

def launch():
	"Opens the BUG help file externally if it can be found or displays an error alert"
	file = findIniFile("The BUG Mod Help.chm")
	if file:
		message = getText("TXT_KEY_BUG_HELP_OPENING", "Opening the BUG Mod help file...")
		CyInterface().addImmediateMessage(message, "")
		os.startfile(file)
		return True
	else:
		title = getText("TXT_KEY_BUG_HELP_MISSING_TITLE", "Help File Not Found")
		body = getText("TXT_KEY_BUG_HELP_MISSING_BODY", "Could not find the file \"The BUG Mod Help.chm\" in the search paths. See the Config tab on the BUG Options screen (Ctrl-Alt-O) for details.")
		popup = PyPopup.PyPopup()
		popup.setHeaderString(title)
		popup.setBodyString(body)
		popup.launch()
		return False

localText = CyTranslator()
def getText(key, default=None):
	text = localText.getText(key, ())
	if not text or text == key:
		return "XML key %s not found" % key
	else:
		return text
