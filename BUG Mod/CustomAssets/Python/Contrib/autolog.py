## Ruff autologger
## Modified from HOF MOD V1.61.001
## Modified from autolog by eotinb
## contains variables to turn on and off various extra log messages
## Alt+E is always on

import codecs
import os
import os.path
import string
import CvPath
import BugOptions
import BugAutologOptions

BugOpt = BugOptions.getOptions()
BugAutolog = BugAutologOptions.BugAutologOptions()

class autologInstance:

#	def __init__(self):

	def setLogFileName(self, LogFileName):
		BugAutolog.setFileName(LogFileName)
		BugAutolog.write()

#	def setLogFileEnabled(self, LogFileEnabled):
#		BugAutolog.setEnabled(LogFileEnabled)
#		BugAutolog.write()

#	def Enabled(self):
#		if BugAutolog.isEnabled():
#			return True
#		else:
#			return False

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
#		temppath = os.getcwd()
#		os.chdir(BugAutolog.getFilePath())
		szPath = BugAutolog.getFilePath()
		if (not szPath or szPath == "Default"):
			if (os.path.isdir(CvPath.userDir)):
				szPath = os.path.join(CvPath.userDir, "AutoLog")
		if (not os.path.isdir(szPath)):
			os.makedirs(szPath)
		self.log = codecs.open(os.path.join(szPath, BugAutolog.getFileName()), 'a', 'utf-8')
#		os.chdir(temppath)

	def closeLog(self):
		self.log.close()

	def RuffEcho(self, echoString, printToScr, printToLog):
		printToScr = False
		printToLog = False

		szMessage = "%s" % (echoString)
		if (printToScr):
			CyInterface().addMessage(CyGame().getActivePlayer(), True, 10, szMessage, "", 2, None, ColorTypes(8), 0, 0, False, False)
		if (printToLog):
			CvUtil.pyPrint(szMessage)
		return 0

class autologRetain:

	def __init__(self):
		bLogFileOpen = False
		bPlayerHuman = False
		Counter = 0

