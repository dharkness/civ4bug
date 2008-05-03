## BugUtil
## Collection of utility functions.
##
## Copyright (c) 2008 The BUG Mod.

from CvPythonExtensions import *

localText = CyTranslator()

def getPlainText(key, default=None):
	"""
	Looks up a translated message in XML without any replacement parameters.
	If the key isn't found, the default is returned.
	"""
	text = localText.getText(key, ())
	if (text and text != key):
		return text
	else:
		return default

def getText(key, values, default=None):
	"""
	Looks up a translated message in XML with a tuple of replacement parameters.
	If the key isn't found, the default is returned.
	"""
	text = localText.getText(key, values)
	if (text and text != key):
		return text
	else:
		return default

def debug(message):
	"""
	Displays a simple message on-screen with no sound.
	"""
	CyInterface().addImmediateMessage(message, "")
	CvUtil.pyPrint(message)