## BugAutologOptions						
## Facade for accessing NJAGC options						
## BUG Mod - Copyright 2007						
						
from BugOptions import OptionsFacade, Option, OptionList						
localText = CyTranslator()
						
class BugAutologOptions(OptionsFacade):						
						
	def __init__(self):					
		OptionsFacade.__init__(self)				
						
		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_AUTOLOG_ENABLED_TEXT", ())				
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_AUTOLOG_ENABLED_HOVER", ())				
		self.addOption(Option("Autolog_Enabled", "Autolog", "Enabled", False, zs_Text, zsHover))

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_AUTOLOG_SILENT_TEXT", ())				
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_AUTOLOG_SILENT_HOVER", ())				
		self.addOption(Option("Autolog_Silent", "Autolog", "Silent", True, zs_Text, zsHover))

		# Log file				
		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_AUTOLOG_DEFAULTFILENAME_TEXT", ())				
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_AUTOLOG_DEFAULTFILENAME_HOVER", ())				
		self.addOption(Option("Autolog_DefaultFileName", "Autolog", "Default File Name", True, zs_Text, zsHover))

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_AUTOLOG_FILEPATH_TEXT", ())				
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_AUTOLOG_FILEPATH_HOVER", ())				
		self.addOption(Option("Autolog_FilePath", "Autolog", "File Path", '', zs_Text, zsHover))

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_AUTOLOG_FILENAME_TEXT", ())				
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_AUTOLOG_FILENAME_HOVER", ())				
		self.addOption(Option("Autolog_FileName", "Autolog", "File Name", 'autolog.txt', zs_Text, zsHover))

		# Log format				
		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_AUTOLOG_FORMAT_TEXT", ())				
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_AUTOLOG_FORMAT_HOVER", ())				
		self.addOption(OptionList("Autolog_Format", "Autolog", "Format Style", 2, zs_Text, zsHover,	
							 ['Plain', 'HTML Tags', 'Forum Tags, With " around color codes', 'Forum Tags, No " around color codes']))	

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_AUTOLOG_COLORCODING_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_AUTOLOG_COLORCODING_HOVER", ())						
		self.addOption(Option("Autolog_ColorCoding", "Autolog", "", True, zs_Text, zsHover))		

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_AUTOLOG_4000BC_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_AUTOLOG_4000BC_HOVER", ())						
		self.addOption(OptionList("Autolog_4000BC", "Autolog", "4000BC", 0, zs_Text, zsHover,
								  [0, 1]))

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_AUTOLOG_IBT_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_AUTOLOG_IBT_HOVER", ())				
		self.addOption(Option("Autolog_IBT", "Autolog", "Show IBT", True, zs_Text, zsHover))

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_AUTOLOG_PREFIX_TEXT", ())				
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_AUTOLOG_PREFIX_HOVER", ())				
		self.addOption(Option("Autolog_Prefix", "Autolog", "Prefix", 'Player Comment', zs_Text, zsHover))

		# Events to log				
		# Research and Builds				
		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_AUTOLOG_LOGTECH_TEXT", ())				
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_AUTOLOG_LOGTECH_HOVER", ())				
		self.addOption(Option("Autolog_LogTech", "Autolog", "Tech", True, zs_Text, zsHover))

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_AUTOLOG_LOGBUILDSTARTED_TEXT", ())				
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_AUTOLOG_LOGBUILDSTARTED_HOVER", ())				
		self.addOption(Option("Autolog_LogBuildStarted", "Autolog", "Build Started", True, zs_Text, zsHover))

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_AUTOLOG_LOGBUILDCOMPLETED_TEXT", ())				
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_AUTOLOG_LOGBUILDCOMPLETED_HOVER", ())				
		self.addOption(Option("Autolog_LogBuildCompleted", "Autolog", "Build Completed", True, zs_Text, zsHover))

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_AUTOLOG_LOGPROJECTS_TEXT", ())				
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_AUTOLOG_LOGPROJECTS_HOVER", ())				
		self.addOption(Option("Autolog_LogProjects", "Autolog", "Project Completed", True, zs_Text, zsHover))

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_AUTOLOG_LOGIMPROVEMENTS_TEXT", ())				
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_AUTOLOG_LOGIMPROVEMENTS_HOVER", ())				
		self.addOption(Option("Autolog_LogImprovements", "Autolog", "Improvements", True, zs_Text, zsHover))

		# Cities				
		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_AUTOLOG_LOGCITYFOUNDED_TEXT", ())				
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_AUTOLOG_LOGCITYFOUNDED_HOVER", ())				
		self.addOption(Option("Autolog_LogCityFounded", "Autolog", "City Founded", True, zs_Text, zsHover))

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_AUTOLOG_LOGCITYGROWTH_TEXT", ())				
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_AUTOLOG_LOGCITYGROWTH_HOVER", ())				
		self.addOption(Option("Autolog_LogCityGrowth", "Autolog", "City Growth", True, zs_Text, zsHover))

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_AUTOLOG_LOGCITYBORDERS_TEXT", ())				
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_AUTOLOG_LOGCITYBORDERS_HOVER", ())				
		self.addOption(Option("Autolog_LogCityBorders", "Autolog", "City Borders", True, zs_Text, zsHover))

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_AUTOLOG_LOGCITYOWNER_TEXT", ())				
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_AUTOLOG_LOGCITYOWNER_HOVER", ())				
		self.addOption(Option("Autolog_LogCityOwner", "Autolog", "City Ownership", True, zs_Text, zsHover))

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_AUTOLOG_LOGCITYRAZED_TEXT", ())				
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_AUTOLOG_LOGCITYRAZED_HOVER", ())				
		self.addOption(Option("Autolog_LogCityRazed", "Autolog", "City Razed", True, zs_Text, zsHover))

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_AUTOLOG_LOGCITYWHIPSTATUS_TEXT", ())				
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_AUTOLOG_LOGCITYWHIPSTATUS_HOVER", ())				
		self.addOption(Option("Autolog_LogCityWhipStatus", "Autolog", "City Whip", True, zs_Text, zsHover))

		# Events				
		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_AUTOLOG_LOGGOODIES_TEXT", ())				
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_AUTOLOG_LOGGOODIES_HOVER", ())				
		self.addOption(Option("Autolog_LogGoodies", "Autolog", "Goodies", True, zs_Text, zsHover))

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_AUTOLOG_LOGRELIGION_TEXT", ())				
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_AUTOLOG_LOGRELIGION_HOVER", ())				
		self.addOption(Option("Autolog_LogReligion", "Autolog", "Religion", True, zs_Text, zsHover))

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_AUTOLOG_LOGCORPORATION_TEXT", ())				
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_AUTOLOG_LOGCORPORATION_HOVER", ())				
		self.addOption(Option("Autolog_LogCorporation", "Autolog", "Corporation", True, zs_Text, zsHover))

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_AUTOLOG_LOGGP_TEXT", ())				
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_AUTOLOG_LOGGP_HOVER", ())				
		self.addOption(Option("Autolog_LogGP", "Autolog", "Great People", True, zs_Text, zsHover))

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_AUTOLOG_LOGGA_TEXT", ())				
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_AUTOLOG_LOGGA_HOVER", ())				
		self.addOption(Option("Autolog_LogGA", "Autolog", "Golden Age", True, zs_Text, zsHover))

		# Politics
		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_AUTOLOG_LOGCONTACT_TEXT", ())				
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_AUTOLOG_LOGCONTACT_HOVER", ())				
		self.addOption(Option("Autolog_LogContact", "Autolog", "Contact", True, zs_Text, zsHover))

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_AUTOLOG_LOGATTITUDE_TEXT", ())				
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_AUTOLOG_LOGATTITUDE_HOVER", ())				
		self.addOption(Option("Autolog_LogAttitude", "Autolog", "Attitude", True, zs_Text, zsHover))

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_AUTOLOG_LOGWAR_TEXT", ())				
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_AUTOLOG_LOGWAR_HOVER", ())				
		self.addOption(Option("Autolog_LogWar", "Autolog", "War", True, zs_Text, zsHover))

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_AUTOLOG_LOGVASSALS_TEXT", ())				
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_AUTOLOG_LOGVASSALS_HOVER", ())				
		self.addOption(Option("Autolog_LogVassals", "Autolog", "Vassals", True, zs_Text, zsHover))

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_AUTOLOG_LOGCIVICS_TEXT", ())				
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_AUTOLOG_LOGCIVICS_HOVER", ())				
		self.addOption(Option("Autolog_LogCivics", "Autolog", "Civics", True, zs_Text, zsHover))

		# Combat				
		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_AUTOLOG_LOGCOMBAT_TEXT", ())				
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_AUTOLOG_LOGCOMBAT_HOVER", ())				
		self.addOption(Option("Autolog_LogCombat", "Autolog", "Combat", True, zs_Text, zsHover))

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_AUTOLOG_LOGPROMOTIONS_TEXT", ())				
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_AUTOLOG_LOGPROMOTIONS_HOVER", ())				
		self.addOption(Option("Autolog_LogPromotions", "Autolog", "Promotions", True, zs_Text, zsHover))

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_AUTOLOG_LOGPILLAGE_TEXT", ())				
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_AUTOLOG_LOGPILLAGE_HOVER", ())				
		self.addOption(Option("Autolog_LogPillage", "Autolog", "Pillage", True, zs_Text, zsHover))

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

	def isLogCityWhipStatus(self):	
		return self.getBoolean('Autolog_LogCityWhipStatus')

	# Events	

	def isLogTribalVillage(self):	
		return self.getBoolean('Autolog_LogGoodies')

	def isLogReligion(self):	
		return self.getBoolean('Autolog_LogReligion')

	def isLogCorporation(self):	
		return self.getBoolean('Autolog_LogCorporation')

	def isLogGreatPeople(self):	
		return self.getBoolean('Autolog_LogGP')

	def isLogGoldenAge(self):	
		return self.getBoolean('Autolog_LogGA')

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
