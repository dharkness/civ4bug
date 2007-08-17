## BugAutologOptions
## Facade for accessing NJAGC options
## BUG Mod - Copyright 2007

from BugOptions import OptionsFacade, Option, OptionList

class BugAutologOptions(OptionsFacade):

	def __init__(self):
		OptionsFacade.__init__(self)
		self.addOption(Option("Autolog_Enabled",
						 "Autolog", "Enabled", False,
						 "Enable Logging",
						 "When checked, various game events are logged to a text file using eotinb's AutoLog mod."))
		self.addOption(Option("Autolog_Silent",
						 "Autolog", "Silent", True,
						 "Silent Start",
						 "When checked, the logger is automatically started with no in-game message."))
		
		# Log file
		self.addOption(Option("Autolog_DefaultFileName",
						 "Autolog", "Default File Name", True,
						 "Use Default File Name",
						 "When checked, the default (playername.txt) will be used, ignores log file name option."))
		self.addOption(Option("Autolog_FilePath",
						 "Autolog", "File Path", '',
						 "Path",
						 "Directory where log file resides (fully qualified path, i.e. C:\folder\subfolder or blank)."))
		self.addOption(Option("Autolog_FileName",
						 "Autolog", "File Name", 'autolog.txt',
						 "File",
						 "Name of log file. If there is no file of this name in the directory above, one will be created."))
		
		# Log format
		self.addOption(OptionList("Autolog_Format",
							 "Autolog", "Format Style", 2,
							 "Format Style",
							 "The format of the log output.",
							 ['Plain', 'HTML Tags', 'Forum Tags']))
		self.addOption(Option("Autolog_ColorCoding",
						 "Autolog", "", True,
						 "Color Coding",
						 "When checked, comments are color-coded for forum posts."))
		self.addOption(OptionList("Autolog_4000BC",
								  "Autolog", "4000BC", 1,
								  "4000BC is Turn",
								  "Select which turn number 4000BC should be.",
								  [0, 1]))
		self.addOption(Option("Autolog_IBT",
						 "Autolog", "Show IBT", True,
						 "Show IBT",
						 "When checked, the logger inserts IBT (in between turns) at the end of the player\'s turn."))
		self.addOption(Option("Autolog_Prefix",
						 "Autolog", "Prefix", 'Player Comment',
						 "Prefix",
						 "Used as a prefix before user entries in the log (use ALT-E), e.g. your nick."))
		
		# Events to log
		# Research and Builds
		self.addOption(Option("Autolog_LogTech",
						 "Autolog", "Tech", True,
						 "Technologies",
						 "When checked, will log techs acquired and research started."))
		self.addOption(Option("Autolog_LogBuildStarted",
						 "Autolog", "Build Started", True,
						 "Builds Started",
						 "When checked, will log when a city starts a build."))
		self.addOption(Option("Autolog_LogBuildCompleted",
						 "Autolog", "Build Completed", True,
						 "Builds Completed",
						 "When checked, will log when a city completes a build."))
		self.addOption(Option("Autolog_LogProjects",
						 "Autolog", "Project Completed", True,
						 "Projects Completed",
						 "When checked, will log completion of projects (certain wonders are technically projects -- other wonders are treated like normal buildings)."))
		self.addOption(Option("Autolog_LogImprovements",
						 "Autolog", "Improvements", True,
						 "Improvements",
						 "When checked, will log when your improvements are built or destroyed by you."))
		
		# Cities
		self.addOption(Option("Autolog_LogCityFounded",
						 "Autolog", "City Founded", True,
						 "City Founded",
						 "When checked, will log when you found a city."))
		self.addOption(Option("Autolog_LogCityGrowth",
						 "Autolog", "City Growth", True,
						 "City Growth",
						 "When checked, will log when one of your cities grows in population."))
		self.addOption(Option("Autolog_LogCityBorders",
						 "Autolog", "City Borders", True,
						 "City Borders",
						 "When checked, will log when one of your city\'s borders expand."))
		self.addOption(Option("Autolog_LogCityOwner",
						 "Autolog", "City Ownership", True,
						 "City Ownership",
						 "When checked, will log when you acquire or lose a city through conquest or trade."))
		self.addOption(Option("Autolog_LogCityRazed",
						 "Autolog", "City Razed", True,
						 "City Razed",
						 "When checked, will log when you raze another civ\'s city or one of your cities is razed."))
		
		# Events
		self.addOption(Option("Autolog_LogGoodies",
						 "Autolog", "Goodies", True,
						 "Tribal Villages",
						 "When checked, will log results from popping tribal villages."))
		self.addOption(Option("Autolog_LogReligion",
						 "Autolog", "Religion", True,
						 "Religion",
						 "When checked, will log\n1. When you found a religion\n2. Spread of any religion to your cities\n 3. Spread of religions whose Holy city you control to foreign cities"))
		self.addOption(Option("Autolog_LogGP",
						 "Autolog", "Great People", True,
						 "Great People",
						 "When checked, will log the birth of great people (in your cities)."))
		self.addOption(Option("Autolog_LogGA",
						 "Autolog", "Golden Age", True,
						 "Golden Age",
						 "When checked, will log begin and end of your Golden Ages."))
		self.addOption(Option("Autolog_LogEvents",
						 "Autolog", "Events", True,
						 "Events and Quests",
						 "When checked, will log events and quests."))
		
		# Politics
		self.addOption(Option("Autolog_LogContact",
						 "Autolog", "Contact", True,
						 "Contact",
						 "When checked, will log first contact with other civs."))
		self.addOption(Option("Autolog_LogAttitude",
						 "Autolog", "Attitude", True,
						 "Attitude",
						 "When checked, will log any change in attitude between civs known to you."))
		self.addOption(Option("Autolog_LogWar",
						 "Autolog", "War", True,
						 "War",
						 "When checked, will log start and end of wars between civs known to you."))
		self.addOption(Option("Autolog_LogVassals",
						 "Autolog", "Vassals", True,
						 "Vassal States",
						 "When checked, will log when any civ becomes a vassal state of or frees itself from another."))
		self.addOption(Option("Autolog_LogCivics",
						 "Autolog", "Civics", True,
						 "Civics",
						 "When checked, will log any change in civics of civs known to you."))
		
		# Combat
		self.addOption(Option("Autolog_LogCombat",
						 "Autolog", "Combat", True,
						 "Combat",
						 "When checked, will log combat results involving your units."))
		self.addOption(Option("Autolog_LogPromotions",
						 "Autolog", "Promotions", True,
						 "Promotions",
						 "When checked, will log when you promote one of your units."))
		self.addOption(Option("Autolog_LogPillage",
						 "Autolog", "Pillage", True,
						 "Pillaging",
						 "When checked, will log when you pillage or your improvements are pillaged."))
		

	def isEnabled(self):
		return self.getBoolean('Autolog_Enabled')

	def setEnabled(self, value):
		self.setValue('Autolog_Enabled', value)

	def enable(self):
		self.setEnabled(True)

	def disable(self):
		self.setEnabled(False)

	def isSilent(self):
		return self.getBoolean('Autolog_Silent')


	# Log File
	
	def isUseDefaultFileName(self):
		return self.getBoolean('Autolog_DefaultFileName')
	
	def getFilePath(self):
		return self.getString('Autolog_FilePath')
	
	def getFileName(self):
		return self.getString('Autolog_FileName')
	
	def setFileName(self, name):
		self.setValue('Autolog_FileName', name)
	

	# Log Format
	
	def getFormatStyle(self):
		return self.getInt('Autolog_Format')
	
	def get4000BCTurn(self):
		return self.getInt('Autolog_4000BC')
	
	def isColorCoding(self):
		return self.getBoolean('Autolog_ColorCoding')
	
	def isShowIBT(self):
		return self.getBoolean('Autolog_IBT')
	
	def getPrefix(self):
		return self.getString('Autolog_Prefix')


	# Events to log

	# Research and Builds

	def isLogTechnology(self):
		return self.getBoolean('Autolog_LogTech')
	
	def isLogBuildStarted(self):
		return self.getBoolean('Autolog_LogBuildStarted')
	
	def isLogBuildCompleted(self):
		return self.getBoolean('Autolog_LogBuildCompleted')
	
	def isLogProjectCompleted(self):
		return self.getBoolean('Autolog_LogProjects')
	
	def isLogImprovements(self):
		return self.getBoolean('Autolog_LogImprovements')

	# Cities

	def isLogCityFounded(self):
		return self.getBoolean('Autolog_LogCityFounded')
	
	def isLogCityGrowth(self):
		return self.getBoolean('Autolog_LogCityGrowth')
	
	def isLogCityBorders(self):
		return self.getBoolean('Autolog_LogCityBorders')
	
	def isLogCityOwner(self):
		return self.getBoolean('Autolog_LogCityOwner')
	
	def isLogCityRazed(self):
		return self.getBoolean('Autolog_LogCityRazed')
	
	# Events

	def isLogTribalVillage(self):
		return self.getBoolean('Autolog_LogGoodies')
	
	def isLogReligion(self):
		return self.getBoolean('Autolog_LogReligion')
	
	def isLogGreatPeople(self):
		return self.getBoolean('Autolog_LogGP')
	
	def isLogGoldenAge(self):
		return self.getBoolean('Autolog_LogGA')
	
	def isLogEvents(self):
		return self.getBoolean('Autolog_LogEvents')

	# Politics

	def isLogContact(self):
		return self.getBoolean('Autolog_LogContact')
	
	def isLogAttitude(self):
		return self.getBoolean('Autolog_LogAttitude')
	
	def isLogWar(self):
		return self.getBoolean('Autolog_LogWar')
	
	def isLogVassals(self):
		return self.getBoolean('Autolog_LogVassals')
	
	def isLogCivics(self):
		return self.getBoolean('Autolog_LogCivics')
	
	# Combat

	def isLogCombat(self):
		return self.getBoolean('Autolog_LogCombat')
	
	def isLogPromotion(self):
		return self.getBoolean('Autolog_LogPromotions')
	
	def isLogPillage(self):
		return self.getBoolean('Autolog_LogPillage')


# The singleton BugAutologOptions object

__g_options = BugAutologOptions()
def getOptions():
	return __g_options
