## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005

# For Input see CvOptionsScreenCallbackInterface in Python\EntryPoints\

import CvUtil
from CvPythonExtensions import *

# RuffMod changes 1/3
import RuffModControl
RuffMod = RuffModControl.RuffModConfig()
# RuffMod Changes

# globals
gc = CyGlobalContext()
UserProfile = CyUserProfile()
localText = CyTranslator()

checkboxes = {
	'PlotList_Action': {'Section':'PlotList', 'Key':'Action', 'Default':False, 'Title':'Show Unit Action', 'Tooltip':'When checked, the unit icon will show the current action (eg Fortified, goto, Sentry, etc).'},
	'PlotList_Promo': {'Section':'PlotList', 'Key':'Promo', 'Default':False, 'Title':'Show Unit Promotion', 'Tooltip':'When checked, units with possible promotion will be highlighted.'},
	'Attitude_Icons': {'Section':'Attitude', 'Key':'Enabled', 'Default':False, 'Title':'Show Attitude Icons', 'Tooltip':'When checked, smilie faces show the AI\'s attitude.'},

	'CivSB_Hide': {'Section':'Dead Civ Scoreboard Mod', 'Key':'Hide Dead Civilizations', 'Default':False, 'Title':'Hide Dead Civilizations', 'Tooltip':'When checked, the dead civilizations will not be shown on the scoreboard.'},
	'CivSB_Grey': {'Section':'Dead Civ Scoreboard Mod', 'Key':'Grey Out Dead Civilizations', 'Default':False, 'Title':'Grey Out Dead Civilizations', 'Tooltip':'When checked, the dead civilizations will be greyed out on the scoreboard.'},
	'CivSB_Dead': {'Section':'Dead Civ Scoreboard Mod', 'Key':'Show Dead Tag', 'Default':False, 'Title':'Show Dead Tag', 'Tooltip':'When checked, a dead tag will be shown against the dead civilizations on the scoreboard.'},

	'RawCommerce': {'Section':'RawCommerce', 'Key':'Enabled', 'Default':False, 'Title':'Show Raw Commerce', 'Tooltip':'When checked, the raw commerce is shown in the city screen.\nToggling this will mix up some headings in the city screen - alt-tab to correct.'},

	'GreatPeopleTurns': {'Section':'GreatPeopleTurns', 'Key':'Enabled', 'Default':False, 'Title':'Show Turns until next Great Person', 'Tooltip':'When checked, the number of turns until the next Great Person will be shown.'},
	'CultureTurns': {'Section':'CultureTurns', 'Key':'Enabled', 'Default':False, 'Title':'Show Turns until next Cultural Expansion', 'Tooltip':'When checked, the number of turns until the next cultural expansion will be shown.'},

	'UnitName_Roman': {'Section':'UNITNAME', 'Key':'Roman', 'Default':False, 'Title':'Use Roman Numerals in Unit Naming', 'Tooltip':'When checked, roman numerals are used in the Unit Naming process.'},

	'AUTOLOG_Silent': {'Section':'AUTOLOG', 'Key':'Silent', 'Default':True, 'Title':'Silent Logging', 'Tooltip':'When checked, the logger is automatically started with no in-game echos.'},
	'AUTOLOG_ColorCoding': {'Section':'AUTOLOG', 'Key':'ColorCoding', 'Default':True, 'Title':'Color Coding', 'Tooltip':'When checked, comments are color-coded for forum posts'},
	'AUTOLOG_LOG_COMBAT': {'Section':'AUTOLOG', 'Key':'LOG_COMBAT', 'Default':True, 'Title':'Log Combat', 'Tooltip':'When checked, will log combat results involving your units'},
	'AUTOLOG_LOG_TECH': {'Section':'AUTOLOG', 'Key':'LOG_TECH', 'Default':True, 'Title':'Log Tech', 'Tooltip':'When checked, will log techs acquired and research started'},
	'AUTOLOG_LOG_COMPLETED_BUILDS': {'Section':'AUTOLOG', 'Key':'LOG_COMPLETED_BUILDS', 'Default':True, 'Title':'Log Complete Builds', 'Tooltip':'When checked, will log when a city completes a build'},
	'AUTOLOG_LOG_START_BUILDS': {'Section':'AUTOLOG', 'Key':'LOG_START_BUILDS', 'Default':True, 'Title':'Log Start Builds', 'Tooltip':'When checked, will log when a city starts a build'},
	'AUTOLOG_LOG_CITY_FOUNDED': {'Section':'AUTOLOG', 'Key':'LOG_CITY_FOUNDED', 'Default':True, 'Title':'Log City Founded', 'Tooltip':'When checked, will log when you found a city'},
	'AUTOLOG_LOG_CITY_GROWTH': {'Section':'AUTOLOG', 'Key':'LOG_CITY_GROWTH', 'Default':True, 'Title':'Log City Growth', 'Tooltip':'When checked, will log when one of your cities grows in population'},
	'AUTOLOG_LOG_CITY_RAZED': {'Section':'AUTOLOG', 'Key':'LOG_CITY_RAZED', 'Default':True, 'Title':'Log City Razed', 'Tooltip':'When checked, will log when you raze another civ\'s city or one of your cities is razed'},
	'AUTOLOG_LOG_CITY_OWNERSHIP': {'Section':'AUTOLOG', 'Key':'LOG_CITY_OWNERSHIP', 'Default':True, 'Title':'Log City Ownership', 'Tooltip':'When checked, will log when you acquire or lose a city through conquest or trade'},
	'AUTOLOG_LOG_BORDERS': {'Section':'AUTOLOG', 'Key':'LOG_BORDERS', 'Default':True, 'Title':'Log Borders', 'Tooltip':'When checked, will log when one of your city\'s borders expand'},
	'AUTOLOG_LOG_PROJECTS': {'Section':'AUTOLOG', 'Key':'LOG_PROJECTS', 'Default':True, 'Title':'Log Projects', 'Tooltip':'When checked, will log completion of projects (certain wonders are technically projects -- other wonders are treated like normal buildings)'},
	'AUTOLOG_LOG_PROMOTIONS': {'Section':'AUTOLOG', 'Key':'LOG_PROMOTIONS', 'Default':True, 'Title':'Log Promotions', 'Tooltip':'When checked, will log when one of your units is promoted'},
	'AUTOLOG_LOG_GOODIES': {'Section':'AUTOLOG', 'Key':'LOG_GOODIES', 'Default':True, 'Title':'Log Goodies', 'Tooltip':'When checked, will log results from popping tribal villages'},
	'AUTOLOG_LOG_GREAT_PEOPLE': {'Section':'AUTOLOG', 'Key':'LOG_GREAT_PEOPLE', 'Default':True, 'Title':'Log Great People', 'Tooltip':'When checked, will log the birth of great people (in your cities)'},
	'AUTOLOG_LOG_RELIGION': {'Section':'AUTOLOG', 'Key':'LOG_RELIGION', 'Default':True, 'Title':'Log Religion', 'Tooltip':'When checked, will log:\n1. When you found a religion\n2. Spread of any religion to your cities\n 3. Spread of religions whose Holy city you control to foreign cities'},
	'AUTOLOG_LOG_GOLDEN_AGE': {'Section':'AUTOLOG', 'Key':'LOG_GOLDEN_AGE', 'Default':True, 'Title':'Golden Age', 'Tooltip':'When checked, will log begin and end of your Golden Age'},
	'AUTOLOG_LOG_CONTACT': {'Section':'AUTOLOG', 'Key':'LOG_CONTACT', 'Default':True, 'Title':'Log Contact', 'Tooltip':'When checked, will log first contact with other civs'},
	'AUTOLOG_LOG_WAR': {'Section':'AUTOLOG', 'Key':'LOG_WAR', 'Default':True, 'Title':'Log War', 'Tooltip':'When checked, will log start and end of wars between CIVs know to you'},
	'AUTOLOG_LOG_CIVICS': {'Section':'AUTOLOG', 'Key':'LOG_CIVICS', 'Default':True, 'Title':'Log Civics', 'Tooltip':'When checked, will log any change in civics of CIVs know to you'},
	'AUTOLOG_LOG_ATTITUDE': {'Section':'AUTOLOG', 'Key':'LOG_ATTITUDE', 'Default':True, 'Title':'Log Attitude', 'Tooltip':'When checked, will log any change in attitude between CIVs know to you'},
	'AUTOLOG_DefaultLogFileName': {'Section':'AUTOLOG', 'Key':'DefaultLogFileName', 'Default':True, 'Title':'Default Log File', 'Tooltip':'When checked, the default (playername.txt) will be used, ignores log file name option.'},
	'AUTOLOG_4000BC': {'Section':'AUTOLOG', 'Key':'4000BC', 'Default':True, 'Title':'4000BC as Turn 0', 'Tooltip':'When checked, 4000BC is logged as turn 0, else it is logged as turn 1.'},
	'AUTOLOG_ShowIBT': {'Section':'AUTOLOG', 'Key':'ShowIBT', 'Default':True, 'Title':'Show IBT', 'Tooltip':'When checked, the logger inserts IBT (in between turns) at the end of the player\'s turn.'},

	'NJAGCM_Enabled': {'Section':'NJAGCM', 'Key':'Enabled', 'Default':True, 'Title':'Enabled', 'Tooltip':'When checked, the NJAGCM mod is enabled.'},
	'NJAGCM_AlternateText': {'Section':'NJAGCM', 'Key':'Alternate Time Text', 'Default':True, 'Title':'Alternate Text', 'Tooltip':'When checked, the time text ocelates between standard time text and the alternate time text.'},
	'NJAGCM_ShowDate': {'Section':'NJAGCM', 'Key':'Show Turns', 'Default':True, 'Title':'Show In-game Date', 'Tooltip':'When checked, the in-game date is displayed.'},
	'NJAGCM_ShowTime': {'Section':'NJAGCM', 'Key':'Show Game Clock', 'Default':True, 'Title':'Show Real Time', 'Tooltip':'When checked, the real time is displayed.'},
	'NJAGCM_ShowCompletedTurns': {'Section':'NJAGCM', 'Key':'Show Game Completed Turns', 'Default':True, 'Title':'Show Completed and Total Turns', 'Tooltip':'When checked, both the completed and total turns are displayed.'},
	'NJAGCM_ShowCompletedPercent': {'Section':'NJAGCM', 'Key':'Show Game Completed Percent', 'Default':True, 'Title':'Show Completed Percentage', 'Tooltip':'When checked, the completed percentage is displayed.'},
	'NJAGCM_AltShowDate': {'Section':'NJAGCM', 'Key':'Alternate Show Turns', 'Default':True, 'Title':'Show In-game Date in Alternate Time Text', 'Tooltip':'When checked, the in-game date is displayed in the alternate Time Text.'},
	'NJAGCM_AltShowTime': {'Section':'NJAGCM', 'Key':'Alternate Show Game Clock', 'Default':True, 'Title':'Show Real Time in Alternate Time Text', 'Tooltip':'When checked, the real time is displayed in the alternate Time Text.'},
	'NJAGCM_AltShowCompletedTurns': {'Section':'NJAGCM', 'Key':'Alternate Show Game Completed Turns', 'Default':True, 'Title':'Show Completed and Total Turns in Alternate Time Text', 'Tooltip':'When checked, both the completed and total turns are displayed in the alternate Time Text.'},
	'NJAGCM_AltShowCompletedPercent': {'Section':'NJAGCM', 'Key':'Alternate Show Game Completed Percent', 'Default':True, 'Title':'Show Completed Percentage in Alternate Time Text', 'Tooltip':'When checked, the completed percentage is displayed in the alternate Time Text.'},
	'NJAGCM_ShowEra': {'Section':'NJAGCM', 'Key':'Show Era', 'Default':True, 'Title':'Show Era Text', 'Tooltip':'When checked, the Era is displayed.'},
	'NJAGCM_ShowEraColor': {'Section':'NJAGCM', 'Key':'Show Reflect Era In Turn Color', 'Default':True, 'Title':'Show in-game date in Era related color', 'Tooltip':'When checked, in-game date is displayed in an era-color code.'},

# Civ4Alerts
	'CIV4LERTS_Enabled': {'Section':'CIV4LERTS', 'Key':'Enabled', 'Default':True, 'Title':'CIV4Lerts', 'Tooltip':'Enables use of the CIV4LERTS part of the mod'},
	'CIV4LERTS_City Pending Growth': {'Section':'CIV4LERTS', 'Key':'City Pending Growth', 'Default':False, 'Title':'City Pending Growth', 'Tooltip':'City Pending Growth'},
	'CIV4LERTS_City Pending Unhealthy': {'Section':'CIV4LERTS', 'Key':'City Pending Unhealthy', 'Default':True, 'Title':'City Pending Unhealthy', 'Tooltip':'City Pending Unhealthy'},
	'CIV4LERTS_City Pending Angry': {'Section':'CIV4LERTS', 'Key':'City Pending Angry', 'Default':True, 'Title':'City Pending Angry', 'Tooltip':'City Pending Angry'},
	'CIV4LERTS_City Growth': {'Section':'CIV4LERTS', 'Key':'City Growth', 'Default':True, 'Title':'City Growth', 'Tooltip':'City Growth'},
	'CIV4LERTS_City Growth Unhealthy': {'Section':'CIV4LERTS', 'Key':'City Growth Unhealthy', 'Default':False, 'Title':'City Growth Unhealthy', 'Tooltip':'City Growth Unhealthy'},
	'CIV4LERTS_City Growth Angry': {'Section':'CIV4LERTS', 'Key':'City Growth Angry', 'Default':False, 'Title':'City Growth Angry', 'Tooltip':'City Growth Angry'},
	'CIV4LERTS_Gold Trade': {'Section':'CIV4LERTS', 'Key':'Gold Trade', 'Default':True, 'Title':'Gold Trade', 'Tooltip':'Gold Trade'},
	'CIV4LERTS_Gold Per Turn Trade': {'Section':'CIV4LERTS', 'Key':'Gold Per Turn Trade', 'Default':True, 'Title':'Gold Per Turn Trade', 'Tooltip':'Gold Per Turn Trade'},
	'CIV4LERTS_CheckForDomPopVictory': {'Section':'CIV4LERTS', 'Key':'CheckForDomPopVictory', 'Default':True, 'Title':'Dom. Population', 'Tooltip':'Checks for Domination Population'},
	'CIV4LERTS_CheckForDomLandVictory': {'Section':'CIV4LERTS', 'Key':'CheckForDomLandVictory', 'Default':True, 'Title':'Dom. Land', 'Tooltip':'Checks for Domination Land'},
	'CIV4LERTS_CheckForCityBorderExpansion': {'Section':'CIV4LERTS', 'Key':'CheckForCityBorderExpansion', 'Default':True, 'Title':'City Expansion', 'Tooltip':'Checks for city border expansion'},
	'CIV4LERTS_CheckForNewTrades': {'Section':'CIV4LERTS', 'Key':'CheckForNewTrades', 'Default':True, 'Title':'New Trades', 'Tooltip':'Checks for new trades'},
	
# ModSpecialDomesticAdvisor
	'MSDA_Enabled': {'Section':'ModSpecialDomesticAdvisor', 'Key':'Enabled', 'Default':True, 'Title':'Enabled', 'Tooltip':'Enables use of the ModSpecialDomesticAdvisor part of the mod'},
	'MSDA_bShowOnlyAvailableBuildings': {'Section':'ModSpecialDomesticAdvisor', 'Key':'bShowOnlyAvailableBuildings', 'Default':True, 'Title':'Available Buildings', 'Tooltip':'When checked, only buildings and wonders are displayed which can be constructed by the civ\nWhen unchecked, all buildings are always displayed'},
	'MSDA_bShowCompressedSpecialists': {'Section':'ModSpecialDomesticAdvisor', 'Key':'bShowCompressedSpecialists', 'Default':True, 'Title':'Compressed Specialists', 'Tooltip':'When checked, only a single sign with a factor is displayed\n(ie "x4" if there are 4 specialists in the city. Good for low screen resolutions)\nWhen unchecked, for each specialist a single sign is displayed'},

# ExoticForeignAdvisor
	'EFA_Enabled': {'Section':'ExoticForeignAdvisor', 'Key':'Enabled', 'Default':True, 'Title':'Enabled', 'Tooltip':'Enables use of the ExoticForeignAdvisor part of the mod'},
	'EFA_RES_SHOW_EXTRA_AMOUNT': {'Section':'ExoticForeignAdvisor', 'Key':'RES_SHOW_EXTRA_AMOUNT', 'Default':True, 'Title':'Show Resource Surplus', 'Tooltip':'When checked, the amount for each surplus resource is subtracted by one. So it shows how many you can give away without losing the resource yourself. This value is not affected by any default layout.'},
	'EFA_RES_SHOW_SURPLUS_AMOUNT_ON_TOP': {'Section':'ExoticForeignAdvisor', 'Key':'RES_SHOW_SURPLUS_AMOUNT_ON_TOP', 'Default':True, 'Title':'Resource Surplus On Top', 'Tooltip':'Checked: The amounts are shown as an overlay on top of the lower left corner of the resources.\nUnchecked: The amounts are shown below the resources so you will need to use a higher value for Res. Surplus Height'},
	'EFA_RES_SHOW_IMPORT_EXPORT_HEADER': {'Section':'ExoticForeignAdvisor', 'Key':'RES_SHOW_IMPORT_EXPORT_HEADER', 'Default':True, 'Title':'Show Import/Export Header', 'Tooltip':'When checked, the resource columns are grouped as import and export'},
	'EFA_RES_SHOW_ACTIVE_TRADE': {'Section':'ExoticForeignAdvisor', 'Key':'RES_SHOW_ACTIVE_TRADE', 'Default':True, 'Title':'Show Active Trade', 'Tooltip':'When checked, two extra columns are used to display resources that are traded in active deals'},
	'EFA_TECH_USE_SMALL_ICONS': {'Section':'ExoticForeignAdvisor', 'Key':'TECH_USE_SMALL_ICONS', 'Default':True, 'Title':'Small Icons', 'Tooltip':'Checked: 32x32 icons are used\nUnchecked: 64x64 icons are used'},
	'EFA_SHOW_LEADER_NAMES': {'Section':'ExoticForeignAdvisor', 'Key':'SHOW_LEADER_NAMES', 'Default':False, 'Title':'Show Leader Names', 'Tooltip':'When checked, shows the names of the leaders'},
	'EFA_SHOW_ROW_BORDERS': {'Section':'ExoticForeignAdvisor', 'Key':'SHOW_ROW_BORDERS', 'Default':True, 'Title':'Show Row Borders', 'Tooltip':'When checked, shows a border around the rows'},
}

textedits = {
	'AUTOLOG_AutoLogPath': {'Section':'AUTOLOG', 'Key':'AutoLogPath', 'Default':'Default', 'Title':'Path', 'Tooltip':'Autolog directory where log file resides - Default or use fully qualified path (i.e. C:\Folder\subfolder etc.)'},
	'AUTOLOG_LogFileName': {'Section':'AUTOLOG', 'Key':'LogFileName', 'Default':'autolog.txt', 'Title':'Filename', 'Tooltip':'name of log file -- if there is no file of this name in the directory above, one will be created'},
	'AUTOLOG_UserPrefixTag': {'Section':'AUTOLOG', 'Key':'UserPrefixTag', 'Default':'User comment:', 'Title':'User Prefix Tag', 'Tooltip':'Used as a prefix before custom user entries in the text log. If you don\'t want any prefix set this options to blank.'},
}

textdropdowns = {
	'TechSplash_Version': {'Section':'TECHSPLASH', 'Key':'Version', 'Default':1, 'Choices':['Standard','Mod (Small)','Mod (Large)'], 'Title':'Tech Splash Version', 'Tooltip':'Options for the Tech Splash screen are:\n1. Standard - shows the vanilla screen.\n2. Mod (Small) - shows the small version of the modified screen.\n3. Mod (Large) - shows the large version of the modified screen.'},
	'CivSB_LeaderCivName': {'Section':'Dead Civ Scoreboard Mod', 'Key':'Show Name', 'Default':1, 'Choices':['Leader\'s Name','Civilization Description','Both'], 'Title':'Name on Scoreboard', 'Tooltip':'Options for the Scoreboard name are:\n1. Shows the Leader\'s Name (standard).\n2. Show the Civilization\'s Description.\n3. Show Both.'},
	'AUTOLOG_FormatStyle': {'Section':'AUTOLOG', 'Key':'FormatStyle', 'Default':2, 'Choices':['None','HTML Tags','Forum Tags'], 'Title':'Format Style', 'Tooltip':'The format of the file output'},
	'UnitName_Method': {'Section':'UNITNAME', 'Key':'Method', 'Default':0, 'Choices':['Standard Civ Naming','Totally Random Names','Civ Related Random Names','1st Warrior type Names','1st Warrior of Moscow type Names','Borg Naming'], 'Title':'Unit Naming Method', 'Tooltip':'There is No tooltip.'}
}

intdropdowns = {
	'NJAGCM_AltTiming': {'Section':'NJAGCM', 'Key':'Alternating Time', 'Default':15, 'Values':[2,5,10,15,30,45,60,300,600], 'Title':'Time (in seconds) between alternating time text', 'Tooltip':'Select the time between Time Text altering.'},

	'EFA_MIN_TOP_BOTTOM_SPACE': {'Section':'ExoticForeignAdvisor', 'Key':'MIN_TOP_BOTTOM_SPACE', 'Default':60, 'Values':[30,45,60,75,90], 'Title':'Min. Vert. Border', 'Tooltip':'Minimum space at the top and bottom of the screen'},
	'EFA_MIN_LEFT_RIGHT_SPACE': {'Section':'ExoticForeignAdvisor', 'Key':'MIN_LEFT_RIGHT_SPACE', 'Default':25, 'Values':[5,10,15,20,25,30,35,40,45,50], 'Title':'Min. Horiz. Border', 'Tooltip':'Minimum space at the left and right end of the screen'},
	'EFA_GROUP_BORDER': {'Section':'ExoticForeignAdvisor', 'Key':'GROUP_BORDER', 'Default':8, 'Values':[2,4,6,8,10,12,14,16,18,20], 'Title':'Group Border', 'Tooltip':'Extra border at the left and right ends of the column groups (import/export)'},
	'EFA_GROUP_LABEL_OFFSET': {'Section':'ExoticForeignAdvisor', 'Key':'GROUP_LABEL_OFFSET', 'Default':3, 'Values':[1,2,3,4,5,6,7,8,9,10], 'Step':1, 'Title':'Group Label Offset', 'Tooltip':'Number of Extra spaces before the label of the column groups (import/export)'},
	'EFA_MIN_COLUMN_SPACE': {'Section':'ExoticForeignAdvisor', 'Key':'MIN_COLUMN_SPACE', 'Default':5, 'Values':[1,2,3,4,5,6,7,8,9,10], 'Title':'Min. Col. Space', 'Tooltip':'Minimum space between the columns'},
	'EFA_MIN_ROW_SPACE': {'Section':'ExoticForeignAdvisor', 'Key':'MIN_ROW_SPACE', 'Default':1, 'Values':[1,2,3,4,5,6,7,8,9,10], 'Title':'Min. Row Space', 'Tooltip':'Minimum space between the rows'},
	'EFA_RES_SURPLUS_HEIGHT': {'Section':'ExoticForeignAdvisor', 'Key':'RES_SURPLUS_HEIGHT', 'Default':80, 'Values':[60,65,70,75,80,85,90,95,100], 'Title':'Res. Surplus Height', 'Tooltip':'Height of the panel showing the surplus resources. If "Resource Surplus On Top" is unchecked you will need to set a higher value for this variable (110 is recommended).'},
	'EFA_RES_GOLD_COL_WIDTH': {'Section':'ExoticForeignAdvisor', 'Key':'RES_GOLD_COL_WIDTH', 'Default':25, 'Values':[5,10,20,25,30,35,40,45,50], 'Title':'Res. Gold Width', 'Tooltip':'Width of the gold column on the resource page'},
	'EFA_RES_PANEL_SPACE': {'Section':'ExoticForeignAdvisor', 'Key':'RES_PANEL_SPACE', 'Default':0, 'Values':[0,1,2,3,4,5,6,7,8,9,10], 'Title':'Res. Panel Space', 'Tooltip':'Space between the two resource panels'},
	'EFA_TECH_GOLD_COL_WITH': {'Section':'ExoticForeignAdvisor', 'Key':'TECH_GOLD_COL_WITH', 'Default':60, 'Values':[40,50,60,70,80], 'Title':'Tech Gold Width', 'Tooltip':'Width of the gold column on the tech page'},

	'CIV4LERTS_Gold Trade Threshold': {'Section':'CIV4LERTS', 'Key':'Gold Trade Threshold', 'Default':50, 'Values':[1,2,3,5,10,20,30,50,100,200,300,500,1000], 'Title':'Threshold', 'Tooltip':'Gold Trade Threshold'},
	'CIV4LERTS_Gold Per Turn Threshold': {'Section':'CIV4LERTS', 'Key':'Gold Per Turn Threshold', 'Default':5, 'Values':[1,2,3,5,10,15,20,25,30,50,100], 'Title':'Threshold', 'Tooltip':'Gold Per Turn Threshold'},
}

floatdropdowns = {
	'CIV4LERTS_PopThreshold': {'Section':'CIV4LERTS', 'Key':'PopThreshold', 'Default':1, 'Values':[0.01,0.02,0.05,0.1,0.2,0.5,1.0,2.0,5.0,10.0,20.0,50.0], 'FormatString':'%g%%', 'Title':'Pop Threshold', 'Tooltip':'Population Threshold'},
	'CIV4LERTS_LandThreshold': {'Section':'CIV4LERTS', 'Key':'LandThreshold', 'Default':1, 'Values':[0.01,0.02,0.05,0.1,0.2,0.5,1.0,2.0,5.0,10.0,20.0,50.0], 'FormatString':'%g%%', 'Title':'Land Threshold', 'Tooltip':'Land Threshold'},
}

class CvRuffModScreen:
	"Options Screen"
	
	def __init__(self):
		self.iScreenHeight = 50
		self.callbackIFace = "CvOptionsScreenCallbackInterface"

	def getTabControl(self):
		return self.pTabControl
		
	def getRuffModTabMiscName(self):
		return self.szRM_MiscName
	def getRuffModTabLogName(self):
		return self.szRM_LogName
	def getRuffModTabCivSBName(self):
		return self.szRM_CivSBName
	def getRuffModTabNJAGCMName(self):
		return self.szRM_NJAGCMName
	def getRuffModMSDATabName(self):
		return self.szRM_MSDAName
	def getRuffModEFATabName(self):
		return self.szEFAName
	def getRuffModAlertsTabName(self):
		return self.szAlertsName
	def getRuffModCreditsTabName(self):
		return self.szRM_CreditsName

#########################################################################################
################################## SCREEN CONSTRUCTION ##################################
#########################################################################################
	
	def initText(self):
		
		self.szTabControlName = "Ruff Mod Options"
		
		self.szRM_MiscName = "Misc"
		self.szRM_LogName = "Log"
		self.szRM_CivSBName = "CivSB"
		self.szRM_NJAGCMName = "NJAGCM"
		self.szRM_MSDAName = "MSDA"
		self.szRM_EFAName = "EFA"
		self.szRM_AlertsName = "Alerts"
		self.szRM_CreditsName = "Credits"

	def refreshScreen (self):
		return 1		

	def interfaceScreen (self):
		"Initial creation of the screen"
		self.initText()
		
		self.pTabControl = CyGTabCtrl(self.szTabControlName, false, false)
		self.pTabControl.setModal(1)
		self.pTabControl.setSize(800,695)
		self.pTabControl.setControlsExpanding(false)
		self.pTabControl.setColumnLength(self.iScreenHeight)
		
		# Set Tabs
		self.pTabControl.attachTabItem("RM_Misc", self.szRM_MiscName)
		self.pTabControl.attachTabItem("RM_Log", self.szRM_LogName)
		self.pTabControl.attachTabItem("RM_CivSB", self.szRM_CivSBName)
		self.pTabControl.attachTabItem("RM_NJAGCM", self.szRM_NJAGCMName)
		self.pTabControl.attachTabItem("RM_MSDA", self.szRM_MSDAName)
		self.pTabControl.attachTabItem("RM_EFA", self.szRM_EFAName)
		self.pTabControl.attachTabItem("RM_Alerts", self.szRM_AlertsName)
		self.pTabControl.attachTabItem("RM_Credits", self.szRM_CreditsName)

		self.drawRM_Misc()
		self.drawRM_Log()
		self.drawRM_CivSB()
		self.drawRM_NJAGCM()
		self.drawRM_MSDA()
		self.drawRM_EFA()
		self.drawRM_Alerts()
		self.drawRM_Credits()

	def drawRM_Misc(self):
		tab = self.pTabControl
		tab.attachVBox("RM_Misc", "VBox")		

		tab.attachScrollPanel("VBox", "MasterPanel")
		tab.setLayoutFlag("MasterPanel", "LAYOUT_SIZE_HEXPANDING")
		tab.setLayoutFlag("MasterPanel", "LAYOUT_SIZE_VEXPANDING")

		tab.attachPanel("MasterPanel", "BackPanel")
		tab.setStyle("BackPanel", "Panel_Tan15_Style")
		tab.setLayoutFlag("BackPanel", "LAYOUT_SIZE_HPREFERREDEXPANDING")
		tab.setLayoutFlag("BackPanel", "LAYOUT_SIZE_VPREFERREDEXPANDING")

		tab.attachHBox("BackPanel", "HBox")
		tab.setLayoutFlag("HBox", "LAYOUT_SIZE_HPREFERREDEXPANDING")
		tab.setLayoutFlag("HBox", "LAYOUT_SIZE_VPREFERREDEXPANDING")

		tab.attachVBox("HBox", "LeftVBox")
		tab.setLayoutFlag("LeftVBox", "LAYOUT_SIZE_HMIN")
		tab.setLayoutFlag("LeftVBox", "LAYOUT_SIZE_VPREFERREDEXPANDING")
		panelName = "LeftVBox"

		tab.attachLabel(panelName, "RM_Misc", "Miscellaneous Options")
		tab.attachHSeparator(panelName, "Misc_Separator")
		self.addRM_TextDropDown(tab,panelName,"TechSplash_Version")
		self.addRM_CheckBox(tab,panelName,"PlotList_Action")
		self.addRM_CheckBox(tab,panelName,"PlotList_Promo")
		self.addRM_CheckBox(tab,panelName,"Attitude_Icons")
		self.addRM_CheckBox(tab,panelName,"RawCommerce")
		self.addRM_CheckBox(tab,panelName,"GreatPeopleTurns")
		self.addRM_CheckBox(tab,panelName,"CultureTurns")
		self.addRM_TextDropDown(tab,panelName,"UnitName_Method")
		self.addRM_CheckBox(tab,panelName,"UnitName_Roman")

		self.drawExit(tab,"VBox")

	def drawRM_Log(self):
		tab = self.pTabControl
		tab.attachVBox("RM_Log", "VBox")		

		tab.attachScrollPanel("VBox", "MasterPanel")
		tab.setLayoutFlag("MasterPanel", "LAYOUT_SIZE_HEXPANDING")
		tab.setLayoutFlag("MasterPanel", "LAYOUT_SIZE_VEXPANDING")

		tab.attachPanel("MasterPanel", "BackPanel")
		tab.setStyle("BackPanel", "Panel_Tan15_Style")
		tab.setLayoutFlag("BackPanel", "LAYOUT_SIZE_HPREFERREDEXPANDING")
		tab.setLayoutFlag("BackPanel", "LAYOUT_SIZE_VPREFERREDEXPANDING")

		tab.attachVBox("BackPanel", "TopBox")
		tab.setLayoutFlag("TopBox", "LAYOUT_SIZE_HPREFERREDEXPANDING")
		tab.setLayoutFlag("TopBox", "LAYOUT_SIZE_VMIN")
		panelName = "TopBox"

		tab.attachLabel(panelName, "RM_Log", "Logger Options")
		tab.attachHSeparator(panelName, "Log_Separator")
		self.addRM_TextEdit(tab,panelName,"AUTOLOG_AutoLogPath")
		self.addRM_TextEdit(tab,panelName,"AUTOLOG_LogFileName")
		self.addRM_TextEdit(tab,panelName,"AUTOLOG_UserPrefixTag")
		self.addRM_TextDropDown(tab,panelName,"AUTOLOG_FormatStyle")

		tab.attachHBox("BackPanel", "HBox")
		tab.setLayoutFlag("HBox", "LAYOUT_SIZE_HPREFERREDEXPANDING")
		tab.setLayoutFlag("HBox", "LAYOUT_SIZE_VPREFERREDEXPANDING")

		tab.attachVBox("HBox", "LeftVBox")
		tab.setLayoutFlag("LeftVBox", "LAYOUT_SIZE_HMIN")
		tab.setLayoutFlag("LeftVBox", "LAYOUT_SIZE_VPREFERREDEXPANDING")
		panelName = "LeftVBox"

		self.addRM_CheckBox(tab,panelName,"AUTOLOG_Silent")
		self.addRM_CheckBox(tab,panelName,"AUTOLOG_DefaultLogFileName")
		self.addRM_CheckBox(tab,panelName,"AUTOLOG_4000BC")
		self.addRM_CheckBox(tab,panelName,"AUTOLOG_ShowIBT")
		self.addRM_CheckBox(tab,panelName,"AUTOLOG_ColorCoding")
		self.addRM_CheckBox(tab,panelName,"AUTOLOG_LOG_COMBAT")
		self.addRM_CheckBox(tab,panelName,"AUTOLOG_LOG_TECH")
		self.addRM_CheckBox(tab,panelName,"AUTOLOG_LOG_COMPLETED_BUILDS")
		
		tab.attachVBox("HBox", "MiddleVBox")
		tab.setLayoutFlag("MiddleVBox", "LAYOUT_SIZE_HMIN")
		tab.setLayoutFlag("MiddleVBox", "LAYOUT_SIZE_VPREFERREDEXPANDING")
		panelName = "MiddleVBox"
		
		self.addRM_CheckBox(tab,panelName,"AUTOLOG_LOG_START_BUILDS")
		self.addRM_CheckBox(tab,panelName,"AUTOLOG_LOG_CITY_FOUNDED")
		self.addRM_CheckBox(tab,panelName,"AUTOLOG_LOG_CITY_GROWTH")
		self.addRM_CheckBox(tab,panelName,"AUTOLOG_LOG_CITY_RAZED")
		self.addRM_CheckBox(tab,panelName,"AUTOLOG_LOG_CITY_OWNERSHIP")
		self.addRM_CheckBox(tab,panelName,"AUTOLOG_LOG_BORDERS")
		self.addRM_CheckBox(tab,panelName,"AUTOLOG_LOG_PROJECTS")
		self.addRM_CheckBox(tab,panelName,"AUTOLOG_LOG_PROMOTIONS")

		tab.attachVBox("HBox", "RightVBox")
		tab.setLayoutFlag("RightVBox", "LAYOUT_SIZE_HMIN")
		tab.setLayoutFlag("RightVBox", "LAYOUT_SIZE_VPREFERREDEXPANDING")
		panelName = "RightVBox"
		
		self.addRM_CheckBox(tab,panelName,"AUTOLOG_LOG_GOODIES")
		self.addRM_CheckBox(tab,panelName,"AUTOLOG_LOG_GREAT_PEOPLE")
		self.addRM_CheckBox(tab,panelName,"AUTOLOG_LOG_RELIGION")
		self.addRM_CheckBox(tab,panelName,"AUTOLOG_LOG_GOLDEN_AGE")
		self.addRM_CheckBox(tab,panelName,"AUTOLOG_LOG_CONTACT")
		self.addRM_CheckBox(tab,panelName,"AUTOLOG_LOG_WAR")
		self.addRM_CheckBox(tab,panelName,"AUTOLOG_LOG_CIVICS")
		self.addRM_CheckBox(tab,panelName,"AUTOLOG_LOG_ATTITUDE")

		self.drawExit(tab,"VBox")

	def drawRM_CivSB(self):
		tab = self.pTabControl
		tab.attachVBox("RM_CivSB", "VBox")		

		tab.attachScrollPanel("VBox", "MasterPanel")
		tab.setLayoutFlag("MasterPanel", "LAYOUT_SIZE_HEXPANDING")
		tab.setLayoutFlag("MasterPanel", "LAYOUT_SIZE_VEXPANDING")

		tab.attachPanel("MasterPanel", "BackPanel")
		tab.setStyle("BackPanel", "Panel_Tan15_Style")
		tab.setLayoutFlag("BackPanel", "LAYOUT_SIZE_HPREFERREDEXPANDING")
		tab.setLayoutFlag("BackPanel", "LAYOUT_SIZE_VPREFERREDEXPANDING")

		tab.attachHBox("BackPanel", "HBox")
		tab.setLayoutFlag("HBox", "LAYOUT_SIZE_HPREFERREDEXPANDING")
		tab.setLayoutFlag("HBox", "LAYOUT_SIZE_VPREFERREDEXPANDING")

		tab.attachVBox("HBox", "LeftVBox")
		tab.setLayoutFlag("LeftVBox", "LAYOUT_SIZE_HMIN")
		tab.setLayoutFlag("LeftVBox", "LAYOUT_SIZE_VPREFERREDEXPANDING")
		panelName = "LeftVBox"

		tab.attachLabel(panelName, "RM_CivSB", "Dead Civilization Score Board (incl Leader Name / Civilization Description)")
		tab.attachHSeparator(panelName, "CivSB_Separator")
		self.addRM_CheckBox(tab,panelName,"CivSB_Hide")
		self.addRM_CheckBox(tab,panelName,"CivSB_Grey")
		self.addRM_CheckBox(tab,panelName,"CivSB_Dead")
		self.addRM_TextDropDown(tab,panelName,"CivSB_LeaderCivName")

		self.drawExit(tab,"VBox")

	def drawRM_NJAGCM(self):
		tab = self.pTabControl
		tab.attachVBox("RM_NJAGCM", "VBox")		

		tab.attachScrollPanel("VBox", "MasterPanel")
		tab.setLayoutFlag("MasterPanel", "LAYOUT_SIZE_HEXPANDING")
		tab.setLayoutFlag("MasterPanel", "LAYOUT_SIZE_VEXPANDING")

		tab.attachPanel("MasterPanel", "BackPanel")
		tab.setStyle("BackPanel", "Panel_Tan15_Style")
		tab.setLayoutFlag("BackPanel", "LAYOUT_SIZE_HPREFERREDEXPANDING")
		tab.setLayoutFlag("BackPanel", "LAYOUT_SIZE_VPREFERREDEXPANDING")

		tab.attachVBox("BackPanel", "TopBox")
		tab.setLayoutFlag("TopBox", "LAYOUT_SIZE_HPREFERREDEXPANDING")
		tab.setLayoutFlag("TopBox", "LAYOUT_SIZE_VMIN")
		panelName = "TopBox"

		tab.attachLabel(panelName, "RM_NJAGCM", "Not Just Another Game Clock Mod Options")
		tab.attachHSeparator(panelName, "NJAGCM_Separator")
		self.addRM_IntEdit(tab, panelName,"NJAGCM_AltTiming", true)

		tab.attachHBox("BackPanel", "HBox")
		tab.setLayoutFlag("HBox", "LAYOUT_SIZE_HPREFERREDEXPANDING")
		tab.setLayoutFlag("HBox", "LAYOUT_SIZE_VPREFERREDEXPANDING")

		tab.attachVBox("HBox", "LeftVBox")
		tab.setLayoutFlag("LeftVBox", "LAYOUT_SIZE_HMIN")
		tab.setLayoutFlag("LeftVBox", "LAYOUT_SIZE_VPREFERREDEXPANDING")
		panelName = "LeftVBox"

		self.addRM_CheckBox(tab,panelName,"NJAGCM_Enabled")
		self.addRM_CheckBox(tab,panelName,"NJAGCM_AlternateText")
		self.addRM_CheckBox(tab,panelName,"NJAGCM_ShowDate")
		self.addRM_CheckBox(tab,panelName,"NJAGCM_ShowTime")
		self.addRM_CheckBox(tab,panelName,"NJAGCM_ShowCompletedTurns")
		self.addRM_CheckBox(tab,panelName,"NJAGCM_ShowCompletedPercent")

		tab.attachVBox("HBox", "RightVBox")
		tab.setLayoutFlag("RightVBox", "LAYOUT_SIZE_HMIN")
		tab.setLayoutFlag("RightVBox", "LAYOUT_SIZE_VPREFERREDEXPANDING")
		panelName = "RightVBox"

		self.addRM_CheckBox(tab,panelName,"NJAGCM_ShowEra")
		self.addRM_CheckBox(tab,panelName,"NJAGCM_ShowEraColor")
		self.addRM_CheckBox(tab,panelName,"NJAGCM_AltShowDate")
		self.addRM_CheckBox(tab,panelName,"NJAGCM_AltShowTime")
		self.addRM_CheckBox(tab,panelName,"NJAGCM_AltShowCompletedTurns")
		self.addRM_CheckBox(tab,panelName,"NJAGCM_AltShowCompletedPercent")

		self.drawExit(tab,"VBox")

	def drawRM_MSDA(self):
		tab = self.pTabControl
		tab.attachVBox("RM_MSDA", "VBox")		

		tab.attachScrollPanel("VBox", "MasterPanel")
		tab.setLayoutFlag("MasterPanel", "LAYOUT_SIZE_HEXPANDING")
		tab.setLayoutFlag("MasterPanel", "LAYOUT_SIZE_VEXPANDING")

		tab.attachPanel("MasterPanel", "BackPanel")
		tab.setStyle("BackPanel", "Panel_Tan15_Style")
		tab.setLayoutFlag("BackPanel", "LAYOUT_SIZE_HPREFERREDEXPANDING")
		tab.setLayoutFlag("BackPanel", "LAYOUT_SIZE_VPREFERREDEXPANDING")

		tab.attachHBox("BackPanel", "HBox")
		tab.setLayoutFlag("HBox", "LAYOUT_SIZE_HPREFERREDEXPANDING")
		tab.setLayoutFlag("HBox", "LAYOUT_SIZE_VPREFERREDEXPANDING")

		tab.attachVBox("HBox", "LeftVBox")
		tab.setLayoutFlag("LeftVBox", "LAYOUT_SIZE_HMIN")
		tab.setLayoutFlag("LeftVBox", "LAYOUT_SIZE_VPREFERREDEXPANDING")
		panelName = "LeftVBox"

		tab.attachLabel(panelName, "RM_MSDA", "Mod Special Domestic Advisor Options")
		tab.attachHSeparator(panelName, "MSDA_Separator")
		self.addRM_CheckBox(tab,panelName,"MSDA_Enabled")
		self.addRM_CheckBox(tab,panelName,"MSDA_bShowOnlyAvailableBuildings")
		self.addRM_CheckBox(tab,panelName,"MSDA_bShowCompressedSpecialists")

		self.drawExit(tab,"VBox")

	def drawRM_EFA(self):
		tab = self.pTabControl
		tab.attachVBox("RM_EFA", "VBox")		

		tab.attachScrollPanel("VBox", "MasterPanel")
		tab.setLayoutFlag("MasterPanel", "LAYOUT_SIZE_HEXPANDING")
		tab.setLayoutFlag("MasterPanel", "LAYOUT_SIZE_VEXPANDING")

		tab.attachPanel("MasterPanel", "BackPanel")
		tab.setStyle("BackPanel", "Panel_Tan15_Style")
		tab.setLayoutFlag("BackPanel", "LAYOUT_SIZE_HPREFERREDEXPANDING")
		tab.setLayoutFlag("BackPanel", "LAYOUT_SIZE_VPREFERREDEXPANDING")

		tab.attachVBox("BackPanel", "TopBox")
		tab.setLayoutFlag("TopBox", "LAYOUT_SIZE_HPREFERREDEXPANDING")
		tab.setLayoutFlag("TopBox", "LAYOUT_SIZE_VMIN")
		panelName = "TopBox"

		tab.attachLabel(panelName, "RM_EFA", "Exotic Foreign Advisor Options")
		tab.attachHSeparator(panelName, "EFA_Separator")

		tab.attachHBox("BackPanel", "HBox")
		tab.setLayoutFlag("HBox", "LAYOUT_SIZE_HPREFERREDEXPANDING")
		tab.setLayoutFlag("HBox", "LAYOUT_SIZE_VPREFERREDEXPANDING")

		tab.attachVBox("HBox", "LeftVBox")
		tab.setLayoutFlag("LeftVBox", "LAYOUT_SIZE_HMIN")
		tab.setLayoutFlag("LeftVBox", "LAYOUT_SIZE_VPREFERREDEXPANDING")
		panelName = "LeftVBox"

		self.addRM_CheckBox(tab,panelName,"EFA_Enabled")
		self.addRM_CheckBox(tab,panelName,"EFA_RES_SHOW_EXTRA_AMOUNT")
		self.addRM_CheckBox(tab,panelName,"EFA_RES_SHOW_SURPLUS_AMOUNT_ON_TOP")
		self.addRM_CheckBox(tab,panelName,"EFA_RES_SHOW_IMPORT_EXPORT_HEADER")
		self.addRM_CheckBox(tab,panelName,"EFA_RES_SHOW_ACTIVE_TRADE")
		self.addRM_CheckBox(tab,panelName,"EFA_TECH_USE_SMALL_ICONS")
		self.addRM_CheckBox(tab,panelName,"EFA_SHOW_LEADER_NAMES")
		self.addRM_CheckBox(tab,panelName,"EFA_SHOW_ROW_BORDERS")

		tab.attachVBox("HBox", "RightVBox")
		tab.setLayoutFlag("RightVBox", "LAYOUT_SIZE_HMIN")
		tab.setLayoutFlag("RightVBox", "LAYOUT_SIZE_VPREFERREDEXPANDING")
		panelName = "RightVBox"

		self.addRM_IntEdit(tab,panelName,"EFA_MIN_TOP_BOTTOM_SPACE",True)
		self.addRM_IntEdit(tab,panelName,"EFA_MIN_LEFT_RIGHT_SPACE",True)
		self.addRM_IntEdit(tab,panelName,"EFA_GROUP_BORDER",True)
		self.addRM_IntEdit(tab,panelName,"EFA_GROUP_LABEL_OFFSET",True)
		self.addRM_IntEdit(tab,panelName,"EFA_MIN_COLUMN_SPACE",True)
		self.addRM_IntEdit(tab,panelName,"EFA_MIN_ROW_SPACE",True)
		self.addRM_IntEdit(tab,panelName,"EFA_RES_SURPLUS_HEIGHT",True)
		self.addRM_IntEdit(tab,panelName,"EFA_RES_GOLD_COL_WIDTH",True)
		self.addRM_IntEdit(tab,panelName,"EFA_RES_PANEL_SPACE",True)
		self.addRM_IntEdit(tab,panelName,"EFA_TECH_GOLD_COL_WITH",True)

		self.drawExit(tab,"VBox")

	def drawRM_Alerts(self):
		tab = self.pTabControl
		tab.attachVBox("RM_Alerts", "VBox")		

		tab.attachScrollPanel("VBox", "MasterPanel")
		tab.setLayoutFlag("MasterPanel", "LAYOUT_SIZE_HEXPANDING")
		tab.setLayoutFlag("MasterPanel", "LAYOUT_SIZE_VEXPANDING")

		tab.attachPanel("MasterPanel", "BackPanel")
		tab.setStyle("BackPanel", "Panel_Tan15_Style")
		tab.setLayoutFlag("BackPanel", "LAYOUT_SIZE_HPREFERREDEXPANDING")
		tab.setLayoutFlag("BackPanel", "LAYOUT_SIZE_VPREFERREDEXPANDING")

		tab.attachVBox("BackPanel", "TopBox")
		tab.setLayoutFlag("TopBox", "LAYOUT_SIZE_HPREFERREDEXPANDING")
		tab.setLayoutFlag("TopBox", "LAYOUT_SIZE_VMIN")
		panelName = "TopBox"

		tab.attachLabel(panelName, "RM_Alerts", "Civilization 4 Alerts")
		tab.attachHSeparator(panelName, "Alerts_Separator")

		tab.attachHBox("BackPanel", "HBox")
		tab.setLayoutFlag("HBox", "LAYOUT_SIZE_HPREFERREDEXPANDING")
		tab.setLayoutFlag("HBox", "LAYOUT_SIZE_VPREFERREDEXPANDING")

		tab.attachVBox("HBox", "LeftVBox")
		tab.setLayoutFlag("LeftVBox", "LAYOUT_SIZE_HMIN")
		tab.setLayoutFlag("LeftVBox", "LAYOUT_SIZE_VPREFERREDEXPANDING")
		panelName = "LeftVBox"

		self.addRM_CheckBox(tab,panelName,"CIV4LERTS_Enabled")
		self.addRM_CheckBox(tab,panelName,"CIV4LERTS_City Pending Growth")
		self.addRM_CheckBox(tab,panelName,"CIV4LERTS_City Pending Unhealthy")
		self.addRM_CheckBox(tab,panelName,"CIV4LERTS_City Pending Angry")
		self.addRM_CheckBox(tab,panelName,"CIV4LERTS_City Growth")
		self.addRM_CheckBox(tab,panelName,"CIV4LERTS_City Growth Unhealthy")
		self.addRM_CheckBox(tab,panelName,"CIV4LERTS_City Growth Angry")
		self.addRM_CheckBox(tab,panelName,"CIV4LERTS_CheckForCityBorderExpansion")
		self.addRM_CheckBox(tab,panelName,"CIV4LERTS_CheckForNewTrades")

		tab.attachVBox("HBox", "RightVBox")
		tab.setLayoutFlag("RightVBox", "LAYOUT_SIZE_HMIN")
		tab.setLayoutFlag("RightVBox", "LAYOUT_SIZE_VPREFERREDEXPANDING")
		panelName = "RightVBox"

		self.addRM_CheckBox(tab,panelName,"CIV4LERTS_Gold Trade")
		self.addRM_IntEdit(tab,panelName,"CIV4LERTS_Gold Trade Threshold",False)
		self.addRM_CheckBox(tab,panelName,"CIV4LERTS_Gold Per Turn Trade")
		self.addRM_IntEdit(tab,panelName,"CIV4LERTS_Gold Per Turn Threshold",False)
		self.addRM_CheckBox(tab,panelName,"CIV4LERTS_CheckForDomLandVictory")
		self.addRM_FloatEdit(tab,panelName,"CIV4LERTS_LandThreshold",False)
		self.addRM_CheckBox(tab,panelName,"CIV4LERTS_CheckForDomPopVictory")
		self.addRM_FloatEdit(tab,panelName,"CIV4LERTS_PopThreshold",False)

		self.drawExit(tab,"VBox")

	def drawRM_Credits(self):
		tab = self.pTabControl
		tab.attachVBox("RM_Credits", "VBox")		

		tab.attachScrollPanel("VBox", "MasterPanel")
		tab.setLayoutFlag("MasterPanel", "LAYOUT_SIZE_HEXPANDING")
		tab.setLayoutFlag("MasterPanel", "LAYOUT_SIZE_VEXPANDING")

		tab.attachPanel("MasterPanel", "BackPanel")
		tab.setStyle("BackPanel", "Panel_Tan15_Style")
		tab.setLayoutFlag("BackPanel", "LAYOUT_SIZE_HPREFERREDEXPANDING")
		tab.setLayoutFlag("BackPanel", "LAYOUT_SIZE_VPREFERREDEXPANDING")

		tab.attachHBox("BackPanel", "HBox")
		tab.setLayoutFlag("HBox", "LAYOUT_SIZE_HPREFERREDEXPANDING")
		tab.setLayoutFlag("HBox", "LAYOUT_SIZE_VPREFERREDEXPANDING")

		tab.attachVBox("HBox", "LeftVBox")
		tab.setLayoutFlag("LeftVBox", "LAYOUT_SIZE_HMIN")
		tab.setLayoutFlag("LeftVBox", "LAYOUT_SIZE_VPREFERREDEXPANDING")
		panelName = "LeftVBox"

		tab.attachLabel(panelName, "RM_Credits", "Credits - the numbers in brackets are the thread at CFC")
		tab.attachHSeparator(panelName, "Credits_Separator")
		tab.attachLabel(panelName, "credits01", "reminder by eotinb")
		tab.attachLabel(panelName, "credits02", "enhanced tech window by Roamty (158636)")
		tab.attachLabel(panelName, "credits03", "not just another clock mod by TheLopez (158137)")
		tab.attachLabel(panelName, "credits04", "logger by eotinb but extended by Ruff")
		tab.attachLabel(panelName, "credits05", "Elements of plot list enhancements by 12Monkeys")
		tab.attachLabel(panelName, "credits06", "attitude icons by Porges (167352)")
		tab.attachLabel(panelName, "credits07", "raw commerce by sevo (158002)")
		tab.attachLabel(panelName, "credits08", "Dead Civ Scoreboard Mod by TheLopez (167023)")
		tab.attachLabel(panelName, "credits09", "turns to complete GP and Culture by Chinese American")
		tab.attachLabel(panelName, "credits10", "unit naming (bits by TheLopez, sen2000, Porges and Ruff")
		tab.attachLabel(panelName, "credits11", "civ 4 alerts by Dr Elmer Jiggle (157088)")
		tab.attachLabel(panelName, "credits11", "more civ 4 alerts by HOF Crew")
		tab.attachLabel(panelName, "credits12", "civilopedia by sevo (148253)")
		tab.attachLabel(panelName, "credits13", "Modified Special domestic advisor by 12Monkeys but maintained by HOF Crew")
		tab.attachLabel(panelName, "credits14", "exotic foreign advisor by Requies but maintained by HOF Crew")
		tab.attachLabel(panelName, "credits15", "civ name / nationality in scoreboard by Ruff")
		tab.attachLabel(panelName, "credits16", "UN Resolutions with real names by Rufus T. Firefly (145587)")
		tab.attachHSeparator(panelName, "Credits_Separator")
		tab.attachLabel(panelName, "credits17", "Pls let Ruff know if the above credits are wrong or imcomplete")

		self.drawExit(tab,"VBox")

	def drawExit(self,tab,parentPanelName):
		tab.attachHSeparator(parentPanelName, "RM_ExitSeparator")
		
		tab.attachHBox(parentPanelName, "LowerHBox")
		tab.setLayoutFlag("LowerHBox", "LAYOUT_HCENTER")
		
		szOptionDesc = localText.getText("TXT_KEY_PEDIA_SCREEN_EXIT", ())
		szCallbackFunction = "handleRuffModExitButtonInput"
		szWidgetName = "RM_OptionsExitButton"
		tab.attachButton("LowerHBox", szWidgetName, szOptionDesc, self.callbackIFace, szCallbackFunction, szWidgetName)
		tab.setLayoutFlag(szWidgetName, "LAYOUT_HCENTER")

	def addRM_TextDropDown(self,tab,panelName,name):
		boxName=name+"HBox"
		labelName=name+"Label"
		editName=name+"Edit"
		tab.attachHBox(panelName, boxName)
		tab.setLayoutFlag(panelName, "LAYOUT_SIZE_HPREFERREDEXPANDING")
		tab.attachLabel(boxName, labelName, textdropdowns[name]['Title'])
		selectedIndex = RuffMod.get_int(textdropdowns[name]['Section'], textdropdowns[name]['Key'], textdropdowns[name]['Default'])
		elements = ()
		for i in range(len(textdropdowns[name]['Choices'])):
			elements += (textdropdowns[name]['Choices'][i],)
		tab.attachDropDown(boxName, editName, "Description", elements, self.callbackIFace, "handleRM_TextDropDownChange", name, selectedIndex)
		tab.setToolTip(editName, textdropdowns[name]['Tooltip'])
		tab.setLayoutFlag(editName, "LAYOUT_RIGHT")

	def addRM_CheckBox(self,tab,panelName,name):
		boxName=name+"HBox"
		editName=name+"Edit"
		value=RuffMod.get_boolean(checkboxes[name]['Section'], checkboxes[name]['Key'], checkboxes[name]['Default'])
		tab.attachVBox(panelName, boxName)
		tab.attachCheckBox(boxName, editName, checkboxes[name]['Title'], self.callbackIFace, "handleRM_CheckboxClicked", name, value)
		tab.setToolTip(editName, checkboxes[name]['Tooltip'])

	def addRM_TextEdit(self,tab,panelName,name):
		boxName=name+"HBox"
		labelName=name+"Label"
		editName=name+"Edit"
		value=RuffMod.get_str(textedits[name]['Section'], textedits[name]['Key'], textedits[name]['Default'])
		tab.attachHBox(panelName, boxName)
		tab.setLayoutFlag(panelName, "LAYOUT_SIZE_HPREFERREDEXPANDING")
		tab.attachLabel(boxName, labelName, textedits[name]['Title'])
		tab.attachEdit(boxName, editName, value, self.callbackIFace, "handleRM_TextEditChange", name)
		tab.setToolTip(editName, textedits[name]['Tooltip'])

	def addRM_IntEdit(self,tab,panelName,name,addLabel):
		boxName=name+"HBox"
		labelName=name+"Label"
		editName=name+"Edit"
		tab.attachHBox(panelName, boxName)
		tab.setLayoutFlag(panelName, "LAYOUT_SIZE_HPREFERREDEXPANDING")
		if addLabel:
			tab.attachLabel(boxName, labelName, intdropdowns[name]['Title'])

		selectedValue = RuffMod.get_int(intdropdowns[name]['Section'], intdropdowns[name]['Key'], intdropdowns[name]['Default'])
		elements = ()
		values=intdropdowns[name]['Values']
		selectedIndex=-1
		bestDistance=100000
		for i in range(len(values)):
			val=values[i]
			elements += (str(val),)
			distance=selectedValue-val
			if distance<0: distance=-distance
			if distance<bestDistance:
				selectedIndex=i
				bestDistance=distance
		tab.attachDropDown(boxName, editName, "Description", elements, self.callbackIFace, "handleRM_IntEditChange", name, selectedIndex)
		tab.setToolTip(editName, intdropdowns[name]['Tooltip'])
		tab.setLayoutFlag(editName, "LAYOUT_RIGHT")

	def addRM_FloatEdit(self,tab,panelName,name,addLabel):
		boxName=name+"HBox"
		labelName=name+"Label"
		editName=name+"Edit"
		tab.attachHBox(panelName, boxName)
		tab.setLayoutFlag(panelName, "LAYOUT_SIZE_HPREFERREDEXPANDING")
		if addLabel:
			tab.attachLabel(boxName, labelName, floatdropdowns[name]['Title'])

		selectedValue = RuffMod.get_float(floatdropdowns[name]['Section'], floatdropdowns[name]['Key'], floatdropdowns[name]['Default'])
		formatString = floatdropdowns[name]['FormatString']
		elements = ()
		values=floatdropdowns[name]['Values']
		selectedIndex=-1
		bestDistance=100000
		for i in range(len(values)):
			val=values[i]
			elements += (formatString%val,)
			distance=selectedValue-val
			if distance<0: distance=-distance
			if distance<bestDistance:
				selectedIndex=i
				bestDistance=distance
		tab.attachDropDown(boxName, editName, "Description", elements, self.callbackIFace, "handleRM_FloatEditChange", name, selectedIndex)
		tab.setToolTip(editName, floatdropdowns[name]['Tooltip'])
		tab.setLayoutFlag(editName, "LAYOUT_RIGHT")
