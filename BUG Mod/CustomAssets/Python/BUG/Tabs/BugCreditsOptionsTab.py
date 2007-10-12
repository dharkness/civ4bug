## BugCreditsOptionsTab
## Tab for the BUG Scoreboard Options
## BUG Mod - Copyright 2007

import BugOptionsTab
import CvModName

credits = [ "BUG Team:",
		    "Alerum68 - Release, Testing",
		    "Massimo \"Cammagno\" Maccagno - Documentation",
		    "EmperorFool - Coding",
		    "Ruff_Hi - Coding, Testing",
		    "-",
		    "Mod Authors:",
		    "12monkeys - Plot List Enhancements",
		    "Almightix - Better Espionage Screen",
		    "asioasioasio - Wide City Bar",
		    "Chinese American - Culture Turns, Great Person Turns",
		    "Dr. Elmer Jiggles - Civ4lerts, Custom Event Manager, MoreCiv4lerts",
		    "EmperorFool - Advanced Scoreboard, Great Person Tech Prefs, Options Framework, Power Ratio in Score, Raw Production "
		        "(extended Better Espionage Screen, Civ4lerts, Customizable Domestic Advisor, Reminders)",
		    "Eotinb - Autolog, Reminders",
		    "Impaler[WrG] - Great Person Progress Bar",
		    "NeverMind - Great General Combat Experience Counter",
		    "Porges - Attitude Icons",
		    "Requies - Exotic Foreign Advisor",
		    "Ruff_Hi - Generic Unit Naming (extended AutoLog, Reminders, Promotion/Action Indicators in PLE, Smilies in GLANCE tab)",
		    "Sevo - Raw Commerce, Sevopedia",
		    "SimCutie - Attitudes in Score, City Cycle Arrows, Extended Color Table",
		    "Taelis - Customizable Domestic Advisor",
		    "TheLopez - Dead Civ Scoreboard, Not Just Another Game Clock",
		    "-",
		    "Translators:",
		    "Massimo \"Cammagno\" Maccagno - Italian",
		    "Ludwig II - German"
		    ]

class BugCreditsOptionsTab(BugOptionsTab.BugOptionsTab):
	"BUG Credits Options Screen Tab"
	
	def __init__(self, screen):
		BugOptionsTab.BugOptionsTab.__init__(self, "Credits", "Credits")

	def create(self, screen):
		tab = self.createTab(screen)
		panel = self.createMainPanel(screen)
		column = self.addOneColumnLayout(screen, panel)
		
		labelNum = 0
		sepNum = 0
		boxNum = 0
		inBox = False
		for line in credits:
			if line == "-":
				screen.attachHSeparator(column, column + "Sep%d" % sepNum)
				sepNum += 1
				inBox = False
			else:
				# Make sure a box exists
				if not inBox:
					box = "CreditsBox%d" % boxNum
					left, right = self.addTwoColumnLayout(screen, column, box)
					boxNum += 1
					inBox = True
				leftLabel = "CreditsLabelLeft%d" % labelNum
				rightLabel = "CreditsLabelRight%d" % labelNum
				pos = line.find(" - ")
				if pos != -1:
					# Person - Task
					leftText = line[0:pos] + "   "
					rightText = line[pos+3:]
				else:
					# Header
					leftText = line
					rightText = " "
				screen.attachLabel(left, leftLabel, leftText)
				screen.attachLabel(right, rightLabel, rightText)
				labelNum += 1
