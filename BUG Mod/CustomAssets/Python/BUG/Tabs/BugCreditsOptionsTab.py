## BugCreditsOptionsTab
## Tab for the BUG Scoreboard Options
## BUG Mod - Copyright 2007

import BugOptionsTab
import CvModName

credits = [ "BUG Team",
		    "Alerum68 - Release, Testing",
		    "EmperorFool - Coding",
		    "Massimo \"Cammagno\" Maccagno - Documentation",
		    "Ruff_Hi - Coding, Testing",
		    "-",
		    "Mod Authors",
		    "12monkeys - Plot List Enhancements",
		    "Almightix - Better Espionage Screen",
		    "asioasioasio - Wide City Bar",
		    "Chinese American - Culture Turns, Great Person Turns",
		    "Dr. Elmer Jiggles - Civ4lerts, Custom Event Manager, MoreCiv4lerts",
		    "EmperorFool - Advanced Scoreboard, GP Tech Prefs, Options Core, Power Ratio, Raw Production",
		    " -    (extended BES, Civ4lerts, CDA, Raw Commerce, Reminders)",
		    "Eotinb - Autolog, Reminders",
		    "Impaler[WrG] - Great Person Progress Bar",
		    "NeverMind - Great General Combat Experience Counter",
		    "Porges - Attitude Icons",
		    "Requies - Exotic Foreign Advisor",
		    "Ruff_Hi - Generic Unit Naming",
		    " -    (extended AutoLog, Reminders, Promo/Actions in PLE, Smilies in EFA)",
		    "Sevo - Raw Commerce, Sevopedia",
		    "SimCutie - Attitudes in Score, City Cycle Arrows, Extended Color Table",
		    "Taelis - Customizable Domestic Advisor",
		    "TheLopez - Dead Civ Scoreboard, Not Just Another Game Clock",
		    "-",
		    "Translators",
		    "Ludwig II - German",
		    "Massimo \"Cammagno\" Maccagno - Italian"
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
		first = True
		for line in credits:
			if line == "-":
				pass
			else:
				pos = line.find(" - ")
				if pos == -1:
					# Header
					if not first:
						label = "CreditsSpacerLabel%d" % labelNum
						screen.attachLabel(column, label, " ")
						labelNum += 1
					else:
						first = False
					label = "CreditsHeaderLabel%d" % labelNum
					screen.attachLabel(column, label, line)
					#screen.setLayoutFlag(label, "LAYOUT_CENTER")
					#screen.setLayoutFlag(label, "LAYOUT_SIZE_HPREFERREDEXPANDING")
					labelNum += 1
					screen.attachHSeparator(column, column + "Sep%d" % sepNum)
					sepNum += 1
					box = "CreditsBox%d" % boxNum
					left, right = self.addTwoColumnLayout(screen, column, box)
					screen.setLayoutFlag(box + "HBox", "LAYOUT_CENTER")
					boxNum += 1
				else:
					# Person - Task
					leftLabel = "CreditsLabelLeft%d" % labelNum
					rightLabel = "CreditsLabelRight%d" % labelNum
					leftText = line[0:pos] + "   "
					rightText = line[pos+3:]
					screen.attachLabel(left, leftLabel, leftText)
					screen.setLayoutFlag(leftLabel, "LAYOUT_RIGHT")
					#screen.setLayoutFlag(leftLabel, "LAYOUT_SIZE_HPREFERREDEXPANDING")
					screen.attachLabel(right, rightLabel, rightText)
					labelNum += 1