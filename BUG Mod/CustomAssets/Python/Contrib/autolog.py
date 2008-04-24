## Ruff autologger
## Modified from HOF MOD V1.61.001
## Modified from autolog by eotinb
## contains variables to turn on and off various extra log messages
## Alt+E is always on

import codecs
import os
import os.path
import string
import BugPath
import BugConfigTracker
import BugAutologOptions

BugAutolog = BugAutologOptions.BugAutologOptions()

class autologInstance:

#	def __init__(self):

	def setLogFileName(self, LogFileName):
		BugAutolog.setFileName(LogFileName)
		BugAutolog.write()

	def writeLog(self, vMsg, vColor = "Black", vBold = False, vUnderline = False, vPrefix = ""):
		self.openLog()

		if vPrefix != "":
			zMsg = "%s %s" % (vPrefix, vMsg)
		else:
			zMsg = vMsg

		## determine type of message
		zStyle = BugAutolog.getFormatStyle()
		if (zStyle < 0
		or zStyle > 3): zStyle=0

		if zStyle == 0: # no formatting so do nothing
			zMsg = zMsg

		elif zStyle == 1:  # html formatting
			if vBold:
				zMsg = "<b>%s</b>" % (zMsg)
			if vUnderline:
				zMsg = "<u>%s</u>" % (zMsg)
			if (vColor != "Black"
			and BugAutolog.isColorCoding()):
				zMsg = "<span style=\"color: %s\">%s</span>" % (vColor, zMsg)

			zMsg = "%s<br>" % (zMsg)

		else: # forum formatting
			if vBold:
				zMsg = "[b]%s[/b]" % (zMsg)
			if vUnderline:
				zMsg = "[u]%s[/u]" % (zMsg)
			if (vColor != "Black"
			and BugAutolog.isColorCoding()):
				if zStyle == 2:  # color coding with "
					zMsg = "[color=\"%s\"]%s[/color]" % (vColor, zMsg)
				else:  # color coding without "
					zMsg = "[color=%s]%s[/color]" % (vColor, zMsg)

		zMsg = "%s\r\n" % (zMsg)

		self.log.write(zMsg)
		self.closeLog()

	def openLog(self):
		szPath = BugAutolog.getFilePath()
		if (not szPath or szPath == "Default"):
			szPath = BugPath.findOrMakeDir("Autolog")
		if (not os.path.isdir(szPath)):
			os.makedirs(szPath)
		szFile = os.path.join(szPath, BugAutolog.getFileName())
		self.log = codecs.open(szFile, 'a', 'utf-8')
		BugConfigTracker.add("Autolog_Log", szFile)

	def closeLog(self):
		self.log.close()

class autologRetain:

	def __init__(self):
		bLogFileOpen = False
		bPlayerHuman = False
		Counter = 0
