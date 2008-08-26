## Ruff autologger
## Modified from HOF MOD V1.61.001
## Modified from autolog by eotinb
## contains variables to turn on and off various extra log messages
## Alt+E is always on

import codecs
import os
import os.path
import string
import BugCore
import BugOptions
import BugPath
import BugConfigTracker

BugAutolog = BugCore.game.Autolog

class autologInstance:


	def __init__(self):
		self.MsgStore = []

	def setLogFileName(self, LogFileName):
		BugAutolog.setFileName(LogFileName)
		# TODO: do we need to save this?
		BugOptions.write()
		
	def isLogging(self):
		return BugAutolog.isLoggingOn()

	def writeLog(self, vMsg, vColor = "Black", vBold = False, vUnderline = False, vPrefix = ""):

		if len(self.MsgStore) > 0:
			self.openLog()
			for sMsg in self.MsgStore:
				self.log.write(sMsg)
			self.closeLog()
			self.writeLog_pending_flush()

		zMsg = self.buildMsg(vMsg, vColor, vBold, vUnderline, vPrefix)

		self.openLog()
		self.log.write(zMsg)
		self.closeLog()

	def writeLog_pending(self, vMsg, vColor = "Black", vBold = False, vUnderline = False, vPrefix = ""):
		zMsg = self.buildMsg(vMsg, vColor, vBold, vUnderline, vPrefix)
		self.MsgStore.append (zMsg)

	def writeLog_pending_flush(self):
		self.MsgStore = []

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

	def buildMsg(self, vMsg, vColor, vBold, vUnderline, vPrefix):
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

		return "%s\r\n" % (zMsg)

# EF: What is this unused class for?
class autologRetain:

	def __init__(self):
		bLogFileOpen = False
		bPlayerHuman = False
		Counter = 0
