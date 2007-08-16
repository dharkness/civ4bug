## Ruff autologger
## Modified from HOF MOD V1.61.001
## Modified from autolog by eotinb
## contains variables to turn on and off various extra log messages
## Alt+E is always on

import os
import os.path
import string
import BugOptions
import BugAutologOptions

BugOpt = BugOptions.getOptions()
BugAutolog = BugAutologOptions.BugAutologOptions()

class autologInstance:

	def __init__(self):
		## USER SETTINGS
		self.colorMessageFormats = [
			["%s\n", "<b><u>%s</b></u><br>\n", "[b][u]%s[/u][/b]\n"],
			["%s\n", "%s<br>\n", "%s\n"],
			["%s %s\n", "<b>%s</b> %s<br>\n", "[b]%s[/b] %s\n"],
			["%s\n", "<span style=\"color: Red\">%s</span><br>\n", "[color=\"Red\"]%s[/color]\n"],
			["%s\n", "<span style=\"color: Purple\">%s</span><br>\n", "[color=\"Purple\"]%s[/color]\n"],
			["%s\n", "<span style=\"color: RoyalBlue\">%s</span><br>\n", "[color=\"RoyalBlue\"]%s[/color]\n"],
			["%s\n", "<span style=\"color: DarkOrange\">%s</span><br>\n", "[color=\"DarkOrange\"]%s[/color]\n"],
			["%s\n", "<span style=\"color: Green\">%s</span><br>\n", "[color=\"Green\"]%s[/color]\n"],
			["%s\n", "<span style=\"color: Brown\">%s</span><br>\n", "[color=\"Brown\"]%s[/color]\n"],
			["%s\n", "<span style=\"color: DarkRed\">%s</span><br>\n", "[color=\"DarkRed\"]%s[/color]\n"],
			["%s\n", "<b>%s</b>\n", "[b]%s[/b]\n"],
			["%s\n", "<span style=\"color: SeaGreen\">%s</span><br>\n", "[color=\"SeaGreen\"]%s[/color]\n"],
			["%s\n", "<span style=\"color: Blue\">%s</span><br>\n", "[color=\"Blue\"]%s[/color]\n"]];
		self.plainMessageFormats = [
			["%s\n", "<b><u>%s</b></u><br>\n", "[b][u]%s[/u][/b]\n"],
			["%s\n", "%s<br>\n", "%s\n"],
			["%s %s\n", "<b>%s</b> %s<br>\n", "[b]%s[/b] %s\n"],
			["%s\n", "%s<br>\n", "%s\n"],
			["%s\n", "%s<br>\n", "%s\n"],
			["%s\n", "%s<br>\n", "%s\n"],
			["%s\n", "%s<br>\n", "%s\n"],
			["%s\n", "%s<br>\n", "%s\n"],
			["%s\n", "%s<br>\n", "%s\n"],
			["%s\n", "%s<br>\n", "%s\n"],
			["%s\n", "<b>%s</b>\n", "[b]%s[/b]\n"],
			["%s\n", "%s<br>\n", "%s\n"],
			["%s\n", "%s<br>\n", "%s\n"]];

	def setLogFileName(self, LogFileName):
		BugAutolog.setFileName(LogFileName)
		BugAutolog.write()

	def setLogFileEnabled(self, LogFileEnabled):
		BugAutolog.setEnabled(LogFileEnabled)
		BugAutolog.write()

	def Enabled(self):
		if BugAutolog.isEnabled():
			return True
		else:
			return False

	def writeLog(self, type, message, year = 0, turn = 0):
		self.openLog()
		## fix formatting of year
		if (year < 0):
			year = str(-year) + " BC"
		else:
			year = str(year) + " AD"
		## determine type of message
		style = BugAutolog.getFormatStyle()
		if style<0 or style>2: style=0
		if type<0 or type>12: type=3
		if BugAutolog.isColorCoding():
			format = self.colorMessageFormats[type][style]
		else:
			format = self.plainMessageFormats[type][style]
		
		if (type == 2): ## custom user comment
			logMessage = format % (BugAutolog.getPrefix(), message)
		else:
			logMessage = format % message

		self.log.write(logMessage)
		self.closeLog()

	def openLog(self):
		temppath = os.getcwd()
		os.chdir(BugAutolog.getFilePath())
		self.log = open(BugAutolog.getFileName(), 'a')
		os.chdir(temppath)
		return

	def closeLog(self):
		self.log.close()

class autologRetain:

	def __init__(self):
		bLogFileOpen = false
		bPlayerHuman = false
		Counter = 0
