## HelpEventManager
## Opens the BUG help file when Shift-F1 is hit.
##
## Copyright (c) 2008 The BUG Mod.

from CvPythonExtensions import *
from BugPath import findIniFile
import os

class HelpEventManager:

	def __init__(self, eventManager):
		eventManager.addEventHandler("kbdEvent", self.onKbdEvent)
		self.eventMgr = eventManager

	def onKbdEvent(self, argsList):
		eventType, key, mx, my, px, py = argsList
		if eventType == self.eventMgr.EventKeyDown:
			theKey = int(key)
			# Check if Shift + F1 was hit
			if (theKey == int(InputTypes.KB_F1) and self.eventMgr.bShift):
				file = findIniFile("The BUG Mod Help.chm")
				if file:
					CyInterface().addImmediateMessage("Opening BUG Help file...", "")
					os.startfile(file)
				else:
					CyInterface().addImmediateMessage("Error: Cannot locate BUG Help file.", "")
				return 1
		return 0
