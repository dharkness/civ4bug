## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005

## Victory Screen shell used to build Military Advisor multi-tab display

from CvPythonExtensions import *
import CvUtil
import ScreenInput
import PyHelpers
import time
import re

# BUG - Options - start
import BugScreensOptions
BugScreens = BugScreensOptions.getOptions()
# BUG - Options - end

PyPlayer = PyHelpers.PyPlayer

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

UNIT_LOCATION_SCREEN = 0
SITUATION_REPORT_SCREEN = 1
PLACE_HOLDER = 2

# Debugging help
def BUGPrint (stuff):
	stuff = "BUG_MAdv: " + stuff
	CvUtil.pyPrint (stuff)

class CvMilitaryAdvisor:
	"Shows the BUG Version of the Military Advisor"

	def __init__(self, screenId):
		self.screenId = screenId
		self.SCREEN_NAME = "MilitaryScreen-BUG"

		self.UNIT_LOC_TAB_ID = "MilitaryUnitLocTabWidget-BUG"
		self.SIT_REP_TAB_ID = "MilitarySitRepTabWidget-BUG"
		self.PLACE_HOLDER_TAB = "placeholder"

		self.X_MAP = 20
		self.Y_MAP = 190
		self.W_MAP = 580
		self.H_MAP_MAX = 500
		self.MAP_MARGIN = 20

		self.X_TEXT = 625
		self.Y_TEXT = 190
		self.W_TEXT = 380
		self.H_TEXT = 500
						
		self.X_LEADERS = 20
		self.Y_LEADERS = 80
		self.W_LEADERS = 985
		self.H_LEADERS = 90
		self.LEADER_BUTTON_SIZE = 64
		self.LEADER_MARGIN = 12

		self.LEADER_COLUMNS = int(self.W_LEADERS / (self.LEADER_BUTTON_SIZE + self.LEADER_MARGIN))

		self.selectedLeaderList = []
		self.selectedGroupList = []
		self.selectedUnitList = []
		self.bUnitDetails = False
		self.iShiftKeyDown = 0

		self.X_GREAT_GENERAL_BAR = 0
		self.Y_GREAT_GENERAL_BAR = 0
		self.W_GREAT_GENERAL_BAR = 0
		self.H_GREAT_GENERAL_BAR = 0

		self.UNIT_BUTTON_ID = "MilitaryAdvisorUnitButton-BUG"
		self.UNIT_LIST_ID = "MilitaryAdvisorUnitList-BUG"
		self.UNIT_BUTTON_LABEL_ID = "MilitaryAdvisorUnitButtonLabel-BUG"
		self.LEADER_BUTTON_ID = "MilitaryAdvisorLeaderButton-BUG"
		self.MINIMAP_PANEL = "MilitaryMiniMapPanel-BUG"

		self.SitRep_Y = 55
		self.SitRep_Y_Offset = 10
		self.SitRep_X1 = 90
		self.SitRep_X2 = self.SitRep_X1 + 100
		self.SitRep_X3 = self.SitRep_X2 + 100
		self.SitRep_X4 = self.SitRep_X3 + 100
		self.SitRep_X5 = self.SitRep_X4 + 100
		self.SitRep_X6 = self.SitRep_X5 + 100











#		self.DEBUG_DROPDOWN_ID =  "MilitaryScreenDropdownWidget"
#		self.INTERFACE_ART_INFO = "TECH_BG"
#		self.EXIT_AREA = "EXIT"
		self.EXIT_ID = "MilitaryScreenExit-BUG"
		self.BACKGROUND_ID = "MilitaryScreenBackground-BUG"
		self.HEADER_ID = "MilitaryScreenHeader-BUG"
		self.WIDGET_ID = "MilitaryScreenWidget-BUG"
#		self.VC_TAB_ID = "VictoryTabWidget"
#		self.SETTINGS_TAB_ID = "SettingsTabWidget"
#		self.SPACESHIP_SCREEN_BUTTON = 1234

		self.Z_BACKGROUND = -6.1
		self.Z_CONTROLS = self.Z_BACKGROUND - 0.2
#		self.DZ = -0.2

		self.X_SCREEN = 500
		self.Y_SCREEN = 396
		self.W_SCREEN = 1024
		self.H_SCREEN = 768
		self.Y_TITLE = 12
		
		self.X_EXIT = 994
		self.Y_EXIT = 726
		
#		self.X_AREA = 10
#		self.Y_AREA = 60
#		self.W_AREA = 1010
#		self.H_AREA = 650
		
#		self.TABLE_WIDTH_0 = 350
#		self.TABLE_WIDTH_1 = 80
#		self.TABLE_WIDTH_2 = 180
#		self.TABLE_WIDTH_3 = 100
#		self.TABLE_WIDTH_4 = 180
#		self.TABLE_WIDTH_5 = 100

#		self.TABLE2_WIDTH_0 = 740
#		self.TABLE2_WIDTH_1 = 265

		self.X_LINK = 100
		self.DX_LINK = 220
		self.Y_LINK = 726
		self.MARGIN = 20
		
		self.SETTINGS_PANEL_X1 = 50
		self.SETTINGS_PANEL_X2 = 355
		self.SETTINGS_PANEL_X3 = 660
		self.SETTINGS_PANEL_Y = 150
		self.SETTINGS_PANEL_WIDTH = 300
		self.SETTINGS_PANEL_HEIGHT = 500
								
		self.nWidgetCount = 0
		self.iActiveLeader = -1
#		self.bVoteTab = False

		self.iScreen = UNIT_LOCATION_SCREEN
						
	def getScreen(self):
		return CyGInterfaceScreen(self.SCREEN_NAME, self.screenId)

	def hideScreen(self):
		screen = self.getScreen()
		screen.hideScreen()
										
	def interfaceScreen(self):

		self.ATTITUDE_DICT = {
			"COLOR_YELLOW": re.sub (":", "|", localText.getText ("TXT_KEY_ATTITUDE_FRIENDLY", ())),
			"COLOR_GREEN" : re.sub (":", "|", localText.getText ("TXT_KEY_ATTITUDE_PLEASED", ())),
			"COLOR_CYAN" : re.sub (":", "|", localText.getText ("TXT_KEY_ATTITUDE_ANNOYED", ())),
			"COLOR_RED" : re.sub (":", "|", localText.getText ("TXT_KEY_ATTITUDE_FURIOUS", ())),
			}

		# Create a new screen
		screen = self.getScreen()
		if screen.isActive():
			return
		screen.setRenderInterfaceOnly(True);
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)

		self.iActiveLeader = CyGame().getActivePlayer()
		if self.iScreen == -1:
			self.iScreen = UNIT_LOCATION_SCREEN

# BUG - optional sit rep - start
		if not BugScreens.isShowSitRep():
			self.iScreen = UNIT_LOCATION_SCREEN
# BUG - optional sit rep - end

		# Set the background widget and exit button
		screen.addDDSGFC(self.BACKGROUND_ID, ArtFileMgr.getInterfaceArtInfo("MAINMENU_SLIDESHOW_LOAD").getPath(), 0, 0, self.W_SCREEN, self.H_SCREEN, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addPanel( "TechTopPanel", u"", u"", True, False, 0, 0, self.W_SCREEN, 55, PanelStyles.PANEL_STYLE_TOPBAR )
		screen.addPanel( "TechBottomPanel", u"", u"", True, False, 0, 713, self.W_SCREEN, 55, PanelStyles.PANEL_STYLE_BOTTOMBAR )
		screen.showWindowBackground( False )
		screen.setDimensions(screen.centerX(0), screen.centerY(0), self.W_SCREEN, self.H_SCREEN)
		screen.setText(self.EXIT_ID, "Background", u"<font=4>" + localText.getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, self.X_EXIT, self.Y_EXIT, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1 )

		# Header...
		screen.setLabel(self.HEADER_ID, "Background", u"<font=4b>" + localText.getText("TXT_KEY_MILITARY_ADVISOR_TITLE", ()).upper() + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_SCREEN, self.Y_TITLE, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		if self.iScreen == UNIT_LOCATION_SCREEN:
			self.showUnitLocation()		
		elif self.iScreen == SITUATION_REPORT_SCREEN:
			self.showSituationReport()
		elif self.iScreen == PLACE_HOLDER:
			self.showGameSettingsScreen()

	def drawTabs(self):
	
		screen = self.getScreen()

		xLink = self.X_LINK
		if (self.iScreen != UNIT_LOCATION_SCREEN):
			screen.setText(self.UNIT_LOC_TAB_ID, "", u"<font=4>" + localText.getText("TXT_KEY_MILITARY_UNIT_LOCATION", ()).upper() + "</font>", CvUtil.FONT_CENTER_JUSTIFY, xLink, self.Y_LINK, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		else:
			screen.setText(self.UNIT_LOC_TAB_ID, "", u"<font=4>" + localText.getColorText("TXT_KEY_MILITARY_UNIT_LOCATION", (), gc.getInfoTypeForString("COLOR_YELLOW")).upper() + "</font>", CvUtil.FONT_CENTER_JUSTIFY, xLink, self.Y_LINK, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		xLink += self.DX_LINK

# BUG - optional sit rep - start
		if BugScreens.isShowSitRep():
# BUG - optional sit rep - end, next 5 lines indented once
			if (self.iScreen != SITUATION_REPORT_SCREEN):
				screen.setText(self.SIT_REP_TAB_ID, "", u"<font=4>" + localText.getText("TXT_KEY_MILITARY_SITUATION_REPORT", ()).upper() + "</font>", CvUtil.FONT_CENTER_JUSTIFY, xLink, self.Y_LINK, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			else:
				screen.setText(self.SIT_REP_TAB_ID, "", u"<font=4>" + localText.getColorText("TXT_KEY_MILITARY_SITUATION_REPORT", (), gc.getInfoTypeForString("COLOR_YELLOW")).upper() + "</font>", CvUtil.FONT_CENTER_JUSTIFY, xLink, self.Y_LINK, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			xLink += self.DX_LINK

# remove when finished with BUG Military			
		if (self.iScreen != PLACE_HOLDER):
			screen.setText(self.PLACE_HOLDER_TAB, "", u"<font=4>" + localText.getText("TXT_KEY_MAIN_MENU_SETTINGS", ()).upper() + "</font>", CvUtil.FONT_CENTER_JUSTIFY, xLink, self.Y_LINK, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		else:
			screen.setText(self.PLACE_HOLDER_TAB, "", u"<font=4>" + localText.getColorText("TXT_KEY_MAIN_MENU_SETTINGS", (), gc.getInfoTypeForString("COLOR_YELLOW")).upper() + "</font>", CvUtil.FONT_CENTER_JUSTIFY, xLink, self.Y_LINK, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		xLink += self.DX_LINK
			


	def showGameSettingsScreen(self):
	
		self.deleteAllWidgets()	
		screen = self.getScreen()
				

		activePlayer = gc.getPlayer(self.iActiveLeader)		

		szSettingsPanel = self.getNextWidgetName()
		screen.addPanel(szSettingsPanel, localText.getText("TXT_KEY_MAIN_MENU_SETTINGS", ()).upper(), "", True, True, self.SETTINGS_PANEL_X1, self.SETTINGS_PANEL_Y - 10, self.SETTINGS_PANEL_WIDTH, self.SETTINGS_PANEL_HEIGHT, PanelStyles.PANEL_STYLE_MAIN)
		szSettingsTable = self.getNextWidgetName()
		screen.addListBoxGFC(szSettingsTable, "", self.SETTINGS_PANEL_X1 + self.MARGIN, self.SETTINGS_PANEL_Y + self.MARGIN, self.SETTINGS_PANEL_WIDTH - 2*self.MARGIN, self.SETTINGS_PANEL_HEIGHT - 2*self.MARGIN, TableStyles.TABLE_STYLE_EMPTY)
		screen.enableSelect(szSettingsTable, False)
		
		screen.appendListBoxStringNoUpdate(szSettingsTable, localText.getText("TXT_KEY_LEADER_CIV_DESCRIPTION", (activePlayer.getNameKey(), activePlayer.getCivilizationShortDescriptionKey())), WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
		screen.appendListBoxStringNoUpdate(szSettingsTable, u"     (" + CyGameTextMgr().parseLeaderTraits(activePlayer.getLeaderType(), activePlayer.getCivilizationType(), True, False) + ")", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
		screen.appendListBoxStringNoUpdate(szSettingsTable, " ", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
		screen.appendListBoxStringNoUpdate(szSettingsTable, localText.getText("TXT_KEY_SETTINGS_DIFFICULTY", (gc.getHandicapInfo(activePlayer.getHandicapType()).getTextKey(), )), WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
		screen.appendListBoxStringNoUpdate(szSettingsTable, " ", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
		screen.appendListBoxStringNoUpdate(szSettingsTable, gc.getMap().getMapScriptName(), WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
		screen.appendListBoxStringNoUpdate(szSettingsTable, localText.getText("TXT_KEY_SETTINGS_MAP_SIZE", (gc.getWorldInfo(gc.getMap().getWorldSize()).getTextKey(), )), WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
		screen.appendListBoxStringNoUpdate(szSettingsTable, localText.getText("TXT_KEY_SETTINGS_CLIMATE", (gc.getClimateInfo(gc.getMap().getClimate()).getTextKey(), )), WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
		screen.appendListBoxStringNoUpdate(szSettingsTable, localText.getText("TXT_KEY_SETTINGS_SEA_LEVEL", (gc.getSeaLevelInfo(gc.getMap().getSeaLevel()).getTextKey(), )), WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
		screen.appendListBoxStringNoUpdate(szSettingsTable, " ", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
		screen.appendListBoxStringNoUpdate(szSettingsTable, localText.getText("TXT_KEY_SETTINGS_STARTING_ERA", (gc.getEraInfo(gc.getGame().getStartEra()).getTextKey(), )), WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
		screen.appendListBoxStringNoUpdate(szSettingsTable, localText.getText("TXT_KEY_SETTINGS_GAME_SPEED", (gc.getGameSpeedInfo(gc.getGame().getGameSpeedType()).getTextKey(), )), WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
		
		screen.updateListBox(szSettingsTable)
		
		szOptionsPanel = self.getNextWidgetName()
		screen.addPanel(szOptionsPanel, localText.getText("TXT_KEY_MAIN_MENU_CUSTOM_SETUP_OPTIONS", ()).upper(), "", True, True, self.SETTINGS_PANEL_X2, self.SETTINGS_PANEL_Y - 10, self.SETTINGS_PANEL_WIDTH, self.SETTINGS_PANEL_HEIGHT, PanelStyles.PANEL_STYLE_MAIN)
		szOptionsTable = self.getNextWidgetName()
		screen.addListBoxGFC(szOptionsTable, "", self.SETTINGS_PANEL_X2 + self.MARGIN, self.SETTINGS_PANEL_Y + self.MARGIN, self.SETTINGS_PANEL_WIDTH - 2*self.MARGIN, self.SETTINGS_PANEL_HEIGHT - 2*self.MARGIN, TableStyles.TABLE_STYLE_EMPTY)
		screen.enableSelect(szOptionsTable, False)

		for i in range(GameOptionTypes.NUM_GAMEOPTION_TYPES):
			if gc.getGame().isOption(i):
				screen.appendListBoxStringNoUpdate(szOptionsTable, gc.getGameOptionInfo(i).getDescription(), WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)		

		if (gc.getGame().isOption(GameOptionTypes.GAMEOPTION_ADVANCED_START)):
			szNumPoints = u"%s %d" % (localText.getText("TXT_KEY_ADVANCED_START_POINTS", ()), gc.getGame().getNumAdvancedStartPoints())
			screen.appendListBoxStringNoUpdate(szOptionsTable, szNumPoints, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)		

		if (gc.getGame().isGameMultiPlayer()):
			for i in range(gc.getNumMPOptionInfos()):
				if (gc.getGame().isMPOption(i)):
					screen.appendListBoxStringNoUpdate(szOptionsTable, gc.getMPOptionInfo(i).getDescription(), WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		
			if (gc.getGame().getMaxTurns() > 0):
				szMaxTurns = u"%s %d" % (localText.getText("TXT_KEY_TURN_LIMIT_TAG", ()), gc.getGame().getMaxTurns())
				screen.appendListBoxStringNoUpdate(szOptionsTable, szMaxTurns, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)		
				
			if (gc.getGame().getMaxCityElimination() > 0):
				szMaxCityElimination = u"%s %d" % (localText.getText("TXT_KEY_CITY_ELIM_TAG", ()), gc.getGame().getMaxCityElimination())
				screen.appendListBoxStringNoUpdate(szOptionsTable, szMaxCityElimination, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)		

		if (gc.getGame().hasSkippedSaveChecksum()):
			screen.appendListBoxStringNoUpdate(szOptionsTable, "Skipped Checksum", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)		
			
		screen.updateListBox(szOptionsTable)

		szCivsPanel = self.getNextWidgetName()
		screen.addPanel(szCivsPanel, localText.getText("TXT_KEY_RIVALS_MET", ()).upper(), "", True, True, self.SETTINGS_PANEL_X3, self.SETTINGS_PANEL_Y - 10, self.SETTINGS_PANEL_WIDTH, self.SETTINGS_PANEL_HEIGHT, PanelStyles.PANEL_STYLE_MAIN)

		szCivsTable = self.getNextWidgetName()
		screen.addListBoxGFC(szCivsTable, "", self.SETTINGS_PANEL_X3 + self.MARGIN, self.SETTINGS_PANEL_Y + self.MARGIN, self.SETTINGS_PANEL_WIDTH - 2*self.MARGIN, self.SETTINGS_PANEL_HEIGHT - 2*self.MARGIN, TableStyles.TABLE_STYLE_EMPTY)
		screen.enableSelect(szCivsTable, False)

		for iLoopPlayer in range(gc.getMAX_CIV_PLAYERS()):
			player = gc.getPlayer(iLoopPlayer)
			if (player.isEverAlive() and iLoopPlayer != self.iActiveLeader and (gc.getTeam(player.getTeam()).isHasMet(activePlayer.getTeam()) or gc.getGame().isDebugMode()) and not player.isBarbarian() and not player.isMinorCiv()):
				screen.appendListBoxStringNoUpdate(szCivsTable, localText.getText("TXT_KEY_LEADER_CIV_DESCRIPTION", (player.getNameKey(), player.getCivilizationShortDescriptionKey())), WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
				screen.appendListBoxStringNoUpdate(szCivsTable, u"     (" + CyGameTextMgr().parseLeaderTraits(player.getLeaderType(), player.getCivilizationType(), True, False) + ")", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
				screen.appendListBoxStringNoUpdate(szCivsTable, " ", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )

		screen.updateListBox(szCivsTable)

		self.drawTabs()




	def showSituationReport(self):		

		self.deleteAllWidgets()	
		screen = self.getScreen()

		activePlayer = gc.getPlayer(self.iActiveLeader)		

		# title panel
#		zsTitlePanel_ID = self.getNextWidgetName()
#		screen.addPanel(zsTitlePanel_ID, "", "", True, True, 0, 50, self.W_SCREEN, 50, PanelStyles.PANEL_STYLE_TOPBAR)

#		zsText = localText.getText("TXT_KEY_MILITARY_SITUATION_REPORT_TITLE", ())
#		zsText = u"<font=4b>" + localText.getText("TXT_KEY_MILITARY_SITUATION_REPORT_TITLE", ()).upper() + u"</font>"
#		screen.setLabel(self.getNextWidgetName(), zsTitlePanel_ID, zsText, CvUtil.FONT_CENTER_JUSTIFY, self.X_SCREEN, self.Y_TITLE + 50, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
#		screen.setLabel(self.HEADER_ID, "Background", u"<font=4b>" + localText.getText("TXT_KEY_MILITARY_ADVISOR_TITLE", ()).upper() + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_SCREEN, self.Y_TITLE, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		# Put everything inside a main panel, so we get vertical scrolling
		zsHeadingPanel_ID = self.getNextWidgetName()
		screen.addPanel(zsHeadingPanel_ID, "", "", True, True, 0, 50, self.W_SCREEN, 45, PanelStyles.PANEL_STYLE_TOPBAR)

		# Put everything inside a main panel, so we get vertical scrolling
		zsMainPanel_ID = self.getNextWidgetName()
		screen.addPanel(zsMainPanel_ID, "", "", True, True, 0, 90, self.W_SCREEN, self.H_SCREEN - 143, PanelStyles.PANEL_STYLE_EMPTY)

		self.SR_initialize()

		self.SR_drawHeader(screen, zsHeadingPanel_ID)

		nCount = 0
		for iLoopPlayer in range(gc.getMAX_PLAYERS()):

			if (gc.getPlayer(iLoopPlayer).isAlive()
			and (gc.getTeam(gc.getPlayer(iLoopPlayer).getTeam()).isHasMet(gc.getPlayer(self.iActiveLeader).getTeam())
			or gc.getGame().isDebugMode())
			and iLoopPlayer != self.iActiveLeader
			and not gc.getPlayer(iLoopPlayer).isBarbarian()
			and not gc.getPlayer(iLoopPlayer).isMinorCiv()):
				self.SR_drawLeaderRows(screen, zsMainPanel_ID, iLoopPlayer, nCount)

				nCount += 1

#		self.SR_drawLeaderRows(screen, zsMainPanel_ID, iLoopPlayer)
#		self.SR_drawLeaderRows(screen, zsMainPanel_ID, iLoopPlayer)

#		zsRowsPanel_ID = self.getNextWidgetName()
#		screen.addPanel(zsRowsPanel_ID, "", "", True, True, 0, 104, self.W_SCREEN, self.H_SCREEN - 155, PanelStyles.PANEL_STYLE_MAIN)

#		self.drawGlanceRows (screen, zsRowsPanel_ID, self.iSelectedLeader != self.iActiveLeader, self.iSelectedLeader)





# HEADER
# LEADER BARS [ICON, RELATIONSHIP (FROM GLANCE), THREAD INDEX, ACTIVE WARS (SMALL LEADER ICONS), STRATEGIC RESOURCES, WILL DECLARE WAR (PLUS REASON WHY NOT)]

# REASONS WHY NOT ... http://civilization4.net/files/modding/PythonAPI/Types/DenialTypes.html
# TRADABLE ITEMS ... http://civilization4.net/files/modding/PythonAPI/Types/TradeableItems.html
# STRATEGIC RESOURCES ... copper, iron, aluminimium, oil, uranium




		self.drawTabs()






















	def SR_initialize(self):
		self.nCount = 0
		self.ltPlayerRel = [0] * gc.getMAX_PLAYERS()
		self.ltPlayerMet = [False] * gc.getMAX_PLAYERS()

		for iLoopPlayer in range(gc.getMAX_PLAYERS()):
			if (gc.getPlayer(iLoopPlayer).isAlive()
			and (gc.getTeam(gc.getPlayer(iLoopPlayer).getTeam()).isHasMet(gc.getPlayer(self.iActiveLeader).getTeam())
			or gc.getGame().isDebugMode())
			and not gc.getPlayer(iLoopPlayer).isBarbarian()
			and not gc.getPlayer(iLoopPlayer).isMinorCiv()):

				BUGPrint ("Player = %d" % iLoopPlayer)
				self.ltPlayerMet [iLoopPlayer] = True
				self.ltPlayerRel [iLoopPlayer] = self.SR_calculateRelations (iLoopPlayer, self.iActiveLeader)

				# Player panel
				self.nCount += 1

		self.X_Spread = (self.W_SCREEN - 20) / self.nCount
		if self.X_Spread < 58: self.X_Spread = 58

		self.Y_Spread = (self.H_SCREEN - 50) / (self.nCount + 2)
		self.Y_Text_Offset = (self.Y_Spread - 36) / 2
		if self.Y_Text_Offset < 0: self.Y_Text_Offset = 0

	def SR_calculateRelations (self, nPlayer, nTarget):
		if (nPlayer != nTarget and gc.getTeam(gc.getPlayer(nPlayer).getTeam()).isHasMet(gc.getPlayer(nTarget).getTeam())):
			nAttitude = 0
			szAttitude = CyGameTextMgr().getAttitudeString(nPlayer, nTarget)
			ltPlusAndMinuses = re.findall ("[-+][0-9]+", szAttitude)
			for i in range (len (ltPlusAndMinuses)):
				nAttitude += int (ltPlusAndMinuses[i])

			BUGPrint (("%d toward %d" % (nPlayer, nTarget)) + str(szAttitude))
			BUGPrint ("Length: %d" % len (ltPlusAndMinuses))
			BUGPrint ("Attitude: %d" % nAttitude)
		else:
			return None

		return nAttitude

	def SR_drawHeader (self, screen, panel_ID):

# RELATIONSHIP (FROM GLANCE), THREAD INDEX, ACTIVE WARS (SMALL LEADER ICONS), STRATEGIC RESOURCES, WILL DECLARE WAR (PLUS REASON WHY NOT)]

#		zsLeaderPanel_ID = self.getNextWidgetName()
#		screen.attachPanel(panel_ID, zsLeaderPanel_ID, "", "", False, True, PanelStyles.PANEL_STYLE_MAIN)

#VOID attachPanelAt(STRING szAttachTo, STRING szName, STRING title, STRING helpText, BOOL bVerticalLayout,
#	BOOL bScrollable, PanelStyle eStyle, INT iX, INT iY, INT iWidth, INT iHeight, WidgetType eWidgetType, INT iData1, INT iData2)

		zsText = localText.getText("TXT_KEY_MILITARY_SITREP_RELATIONSHIP", ())
		screen.setText(self.getNextWidgetName(), panel_ID, zsText, CvUtil.FONT_LEFT_JUSTIFY, self.SitRep_X1, self.SitRep_Y, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		zsText = localText.getText("TXT_KEY_MILITARY_SITREP_WORSE_ENEMY", ())
		screen.setText(self.getNextWidgetName(), panel_ID, zsText, CvUtil.FONT_LEFT_JUSTIFY, self.SitRep_X2, self.SitRep_Y, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		zsText = localText.getText("TXT_KEY_MILITARY_SITREP_THREAD_INDEX", ())
		screen.setText(self.getNextWidgetName(), panel_ID, zsText, CvUtil.FONT_LEFT_JUSTIFY, self.SitRep_X3, self.SitRep_Y, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		zsText = localText.getText("TXT_KEY_MILITARY_SITREP_ACTIVE_WARS", ())
		screen.setText(self.getNextWidgetName(), panel_ID, zsText, CvUtil.FONT_LEFT_JUSTIFY, self.SitRep_X4, self.SitRep_Y, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		zsText = localText.getText("TXT_KEY_MILITARY_SITREP_STRATEGIC_RESOURCES", ())
		screen.setText(self.getNextWidgetName(), panel_ID, zsText, CvUtil.FONT_LEFT_JUSTIFY, self.SitRep_X5, self.SitRep_Y, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		zsText = localText.getText("TXT_KEY_MILITARY_SITREP_WILL_DECLARE", ())
		screen.setText(self.getNextWidgetName(), panel_ID, zsText, CvUtil.FONT_LEFT_JUSTIFY, self.SitRep_X6, self.SitRep_Y, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

	def SR_drawLeaderRows (self, screen, panel_ID, iLeader, nCount):

		zsLeaderPanel_ID = self.getNextWidgetName()
		screen.attachPanel(panel_ID, zsLeaderPanel_ID, "", "", False, True, PanelStyles.PANEL_STYLE_IN)

		screen.attachLabel(zsLeaderPanel_ID, "", "   ")

		objLeaderHead = gc.getLeaderHeadInfo (gc.getPlayer(iLeader).getLeaderType())
		screen.attachImageButton(zsLeaderPanel_ID, "", objLeaderHead.getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_LEADERHEAD, iLeader, -1, False)

		# add attitude
		self.SR_LRow_Attitude(screen, zsLeaderPanel_ID, iLeader, nCount)

		# add worst enemy
		self.SR_LRow_WorseEnemy(screen, zsLeaderPanel_ID, iLeader, nCount)

		# thread index
		self.SR_LRow_ThreadIndex(screen, zsLeaderPanel_ID, iLeader, nCount)

		# active wars
		self.SR_LRow_ActiveWars(screen, zsLeaderPanel_ID, iLeader, nCount)

		# strategic resources
		self.SR_LRow_StratResources(screen, zsLeaderPanel_ID, iLeader, nCount)

		# will declare war?		
		self.SR_LRow_WillDeclare(screen, zsLeaderPanel_ID, iLeader, nCount)







	def SR_LRow_Attitude (self, screen, sPanel, iLeader, nCount):
		zsRel = self.SR_calculateRelations (iLeader, self.iActiveLeader)
		zsText = self.SR_LRow_getAttitudeText (zsRel, self.iActiveLeader, iLeader)

		szPanel_ID = self.getNextWidgetName()
		screen.setTextAt (szPanel_ID, sPanel, zsText, CvUtil.FONT_CENTER_JUSTIFY, self.SitRep_X1, self.Y_Text_Offset + self.SitRep_Y_Offset, -0.1, FontTypes.GAME_FONT, WidgetTypes.WIDGET_LEADERHEAD, iLeader, self.iActiveLeader)
#		screen.setTextAt (szPanel_ID, sPanel, szText, CvUtil.FONT_CENTER_JUSTIFY, self.X_GLANCE_OFFSET - 2 + (self.X_Spread * nCount), self.Y_GLANCE_OFFSET + self.Y_Text_Offset, -0.1, FontTypes.GAME_FONT, WidgetTypes.WIDGET_LEADERHEAD, iLeader, self.iActiveLeader)

	def SR_LRow_WorseEnemy (self, screen, sPanel, iLeader, nCount):
		zsText = gc.getPlayer(iLeader).getWorstEnemyName()
		if zsText == "":
			zsText = "None"

		szPanel_ID = self.getNextWidgetName()
		screen.setTextAt (szPanel_ID, sPanel, zsText, CvUtil.FONT_CENTER_JUSTIFY, self.SitRep_X2, self.Y_Text_Offset + self.SitRep_Y_Offset, -0.1, FontTypes.GAME_FONT, WidgetTypes.WIDGET_LEADERHEAD, iLeader, self.iActiveLeader)

	def SR_LRow_ThreadIndex(self, screen, sPanel, iLeader, nCount):
		zsText = "Thread"

		szPanel_ID = self.getNextWidgetName()
		screen.setTextAt (szPanel_ID, sPanel, zsText, CvUtil.FONT_CENTER_JUSTIFY, self.SitRep_X3, self.Y_Text_Offset + self.SitRep_Y_Offset, -0.1, FontTypes.GAME_FONT, WidgetTypes.WIDGET_LEADERHEAD, iLeader, self.iActiveLeader)

	def SR_LRow_ActiveWars(self, screen, sPanel, iLeader, nCount):
		zsText = "Active Wars"

		szPanel_ID = self.getNextWidgetName()
		screen.setTextAt (szPanel_ID, sPanel, zsText, CvUtil.FONT_CENTER_JUSTIFY, self.SitRep_X4, self.Y_Text_Offset + self.SitRep_Y_Offset, -0.1, FontTypes.GAME_FONT, WidgetTypes.WIDGET_LEADERHEAD, iLeader, self.iActiveLeader)

	def SR_LRow_StratResources(self, screen, sPanel, iLeader, nCount):
		zsText = "Strat Res"

		szPanel_ID = self.getNextWidgetName()
		screen.setTextAt (szPanel_ID, sPanel, zsText, CvUtil.FONT_CENTER_JUSTIFY, self.SitRep_X5, self.Y_Text_Offset + self.SitRep_Y_Offset, -0.1, FontTypes.GAME_FONT, WidgetTypes.WIDGET_LEADERHEAD, iLeader, self.iActiveLeader)

	def SR_LRow_WillDeclare(self, screen, sPanel, iLeader, nCount):
		zsText = "will declare"

		szPanel_ID = self.getNextWidgetName()
		screen.setTextAt (szPanel_ID, sPanel, zsText, CvUtil.FONT_CENTER_JUSTIFY, self.SitRep_X6, self.Y_Text_Offset + self.SitRep_Y_Offset, -0.1, FontTypes.GAME_FONT, WidgetTypes.WIDGET_LEADERHEAD, iLeader, self.iActiveLeader)








	def SR_LRow_getAttitudeText (self, nAttitude, nPlayer, nTarget):
		szText = str (nAttitude)
		szAttitude = CyGameTextMgr().getAttitudeString(nPlayer, nTarget)
		if nAttitude > 0:
			szText = "+" + szText

		if BugScreens.isShowGlanceSmilies():
			szText = "[" + szText + "]"
		else:
			szText = "<font=3>   " + szText + "</font>"

#		ExoticForPrint ("Attitude String = %s" % szAttitude)
		for szColor, szSearchString in self.ATTITUDE_DICT.items():
			if re.search (szSearchString, szAttitude):
				color = gc.getInfoTypeForString(szColor)
				szText = localText.changeTextColor (szText, color)

		if BugScreens.isShowGlanceSmilies():
			iAtt = gc.getPlayer(nPlayer).AI_getAttitude(nTarget)

			BUGPrint ("iAtt: %d" % (iAtt))

			szSmilie =  unichr(ord(unichr(CyGame().getSymbolID(FontSymbols.POWER_CHAR) + 4)) + iAtt)
			szText = szSmilie + " " + szText
		
		if gc.getTeam(gc.getPlayer(nPlayer).getTeam()).isAtWar(gc.getPlayer(nTarget).getTeam()):
			szText += u" %c" % CyGame().getSymbolID(FontSymbols.OCCUPATION_CHAR)

		return szText







#							szStringHealth = szString + "Health"
#							screen.setBarPercentage( szStringHealth, InfoBarTypes.INFOBAR_STORED, float( pLoopUnit.currHitPoints() ) / float( pLoopUnit.maxHitPoints() ) )
#							if (pLoopUnit.getDamage() >= ((pLoopUnit.maxHitPoints() * 2) / 3)):
#								screen.setStackedBarColors(szStringHealth, InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_RED"))
#							elif (pLoopUnit.getDamage() >= (pLoopUnit.maxHitPoints() / 3)):
#								screen.setStackedBarColors(szStringHealth, InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_YELLOW"))
#							else:
#								screen.setStackedBarColors(szStringHealth, InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_GREEN"))
#							screen.show( szStringHealth )


# thread index  (progress bar, 0 to 100 with colors as follows)
# overlay words: NIL, LOW, MODERATE, HIGH, EXTREME

# COLOR_PLAYER_GREEN	0 - 20
# COLOR_PLAYER_BROWN	20 to 40
# COLOR_PLAYER_YELLOW	40 to 60
# COLOR_PLAYER_ORANGE	60 to 75
# COLOR_PLAYER_RED		75 to 100

# 25 pts for ATTITUDE ... -15 to +15 = 25 to 0
# 25 pts for STR ... -50% to +50% = 25 to 0    (str = us / them - 1)
# 20 pts for close borders or ocean exposure (us) and them with knowledge of astronomy
# 30 pts if they are WHEOOH





				# Player panel
#		playerPanel_ID = self.getNextWidgetName()
#				screen.attachPanel(mainPanelName, playerPanelName, gc.getPlayer(iLoopPlayer).getName(), "", False, True, PanelStyles.PANEL_STYLE_MAIN)







	def showUnitLocation(self):

		self.deleteAllWidgets()	
		screen = self.getScreen()

		activePlayer = PyHelpers.PyPlayer(self.iActiveLeader)
		iActiveTeam = gc.getPlayer(self.iActiveLeader).getTeam()
		
		self.UL_DrawMinimap(screen)

		self.unitsList = [(0, 0, [], 0)] * gc.getNumUnitInfos()
		self.selectedUnitList = []
		self.selectedLeaderList.append(self.iActiveLeader)

		self.drawCombatExperience()

		# refresh the unit location
		self.UL_refresh(true)

		self.drawTabs()




	def UL_DrawMinimap(self, iScreen):
		# Minimap initialization
		iMap_W = CyMap().getGridWidth()
		iMap_H = CyMap().getGridHeight()
		self.H_MAP = (self.W_MAP * iMap_H) / iMap_W
		if (self.H_MAP > self.H_MAP_MAX):
			self.W_MAP = (self.H_MAP_MAX * iMap_W) / iMap_H
			self.H_MAP = self.H_MAP_MAX

		szPanel_ID = self.MINIMAP_PANEL
#		iScreen.addPanel(szPanel_ID, u"", "", False, False, self.X_MAP, self.Y_MAP, self.W_MAP, self.H_MAP, PanelStyles.PANEL_STYLE_MAIN)
		iScreen.initMinimap(self.X_MAP + self.MAP_MARGIN, self.X_MAP + self.W_MAP - self.MAP_MARGIN, self.Y_MAP + self.MAP_MARGIN, self.Y_MAP + self.H_MAP - self.MAP_MARGIN, self.Z_CONTROLS)
		iScreen.updateMinimapSection(False, False)
		iScreen.updateMinimapColorFromMap(MinimapModeTypes.MINIMAPMODE_TERRITORY, 0.3)
		iScreen.setMinimapMode(MinimapModeTypes.MINIMAPMODE_MILITARY)

		self.UL_SetMinimapVisibility(iScreen, true)
		iScreen.bringMinimapToFront()

	def UL_SetMinimapVisibility(self, iScreen, bVisibile):
		iOldMode = CyInterface().getShowInterface()

		if bVisibile:
			CyInterface().setShowInterface(InterfaceVisibility.INTERFACE_MINIMAP_ONLY)
		else:
			CyInterface().setShowInterface(InterfaceVisibility.INTERFACE_HIDE)
			
		iScreen.updateMinimapVisibility()
		CyInterface().setShowInterface(iOldMode)

	def UL_refresh(self, bReload):
	
		if (self.iActiveLeader < 0):
			return
						
		screen = self.getScreen()
				
		if (bReload):
			# Set scrollable area for unit buttons
			szPanel_ID = self.getNextWidgetName()
			screen.addPanel(szPanel_ID, "", "", True, True, self.X_TEXT, self.Y_TEXT, self.W_TEXT, self.H_TEXT, PanelStyles.PANEL_STYLE_MAIN)
			
			# Set scrollable area for leaders
			szPanel_ID = self.getNextWidgetName()
			screen.addPanel(szPanel_ID, "", "", False, True, self.X_LEADERS, self.Y_LEADERS, self.W_LEADERS, self.H_LEADERS, PanelStyles.PANEL_STYLE_MAIN)

		listLeaders = []
		for iLoopPlayer in range(gc.getMAX_PLAYERS()):
			player = gc.getPlayer(iLoopPlayer)
			if (player.isAlive() and (gc.getTeam(player.getTeam()).isHasMet(gc.getPlayer(self.iActiveLeader).getTeam()) or gc.getGame().isDebugMode())):
				listLeaders.append(iLoopPlayer)
				
		iNumLeaders = len(listLeaders)
		if iNumLeaders >= self.LEADER_COLUMNS:
			iButtonSize = self.LEADER_BUTTON_SIZE / 2
		else:
			iButtonSize = self.LEADER_BUTTON_SIZE

		iColumns = int(self.W_LEADERS / (iButtonSize + self.LEADER_MARGIN))

		# loop through all players and display leaderheads
		for iIndex in range(iNumLeaders):
			iLoopPlayer = listLeaders[iIndex]
			player = gc.getPlayer(iLoopPlayer)
			
			x = self.X_LEADERS + self.LEADER_MARGIN + (iIndex % iColumns) * (iButtonSize + self.LEADER_MARGIN)
			y = self.Y_LEADERS + self.LEADER_MARGIN + (iIndex // iColumns) * (iButtonSize + self.LEADER_MARGIN)

			if (bReload):
				if player.isBarbarian():
					szButton = "Art/Interface/Buttons/Civilizations/Barbarian.dds"
				else:
					szButton = gc.getLeaderHeadInfo(gc.getPlayer(iLoopPlayer).getLeaderType()).getButton()

				szLeaderButton = self.getLeaderButtonWidget(iLoopPlayer)              #self.getNextWidgetName()
				screen.addCheckBoxGFC(szLeaderButton, szButton, ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(), x, y, iButtonSize, iButtonSize, WidgetTypes.WIDGET_MINIMAP_HIGHLIGHT, 2, iLoopPlayer, ButtonStyles.BUTTON_STYLE_LABEL)
				screen.setState(szLeaderButton, (iLoopPlayer in self.selectedLeaderList))				
		
		self.UL_refreshUnitSelection(bReload)

	def UL_refreshUnitSelection(self, bReload):
		screen = self.getScreen()
		
		screen.minimapClearAllFlashingTiles()

		if (bReload):
			iBtn_X = self.X_TEXT + self.MAP_MARGIN
			iBtn_Y = self.Y_TEXT + self.MAP_MARGIN/2
			iTxt_X = iBtn_X + 22
			iTxt_Y = iBtn_Y + 2
			if (self.bUnitDetails):
				zsText = localText.getText("TXT_KEY_MILITARY_ADVISOR_UNIT_TOGGLE_OFF", ())
				screen.setButtonGFC(self.UNIT_BUTTON_ID, u"", "", iBtn_X, iBtn_Y, 20, 20, WidgetTypes.WIDGET_GENERAL, -1, -1, ButtonStyles.BUTTON_STYLE_CITY_MINUS )
				screen.setLabel(self.UNIT_BUTTON_LABEL_ID, "", zsText, CvUtil.FONT_LEFT_JUSTIFY, iTxt_X, iTxt_Y, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			else:
				zsText = localText.getText("TXT_KEY_MILITARY_ADVISOR_UNIT_TOGGLE_ON", ())
				screen.setButtonGFC(self.UNIT_BUTTON_ID, u"", "", iBtn_X, iBtn_Y, 20, 20, WidgetTypes.WIDGET_GENERAL, -1, -1, ButtonStyles.BUTTON_STYLE_CITY_PLUS )
				screen.setLabel(self.UNIT_BUTTON_LABEL_ID, "", zsText, CvUtil.FONT_LEFT_JUSTIFY, iTxt_X, iTxt_Y, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		# self.unitsList[iUnit][0] is the UnitCombatGroup (e.g. Melee)
		# self.unitsList[iUnit][1] is the unit type (e.g. Warrior)
		# self.unitsList[iUnit][2] is a list of the active player's actual units
		# self.unitsList[iUnit][3] is the total number of those units seen by the active player (not only his own)
		
		if bReload:
			for iUnit in range(gc.getNumUnitInfos()):
				self.unitsList[iUnit] = (gc.getUnitInfo(iUnit).getUnitCombatType(), iUnit, [], 0)

			for iPlayer in range(gc.getMAX_PLAYERS()):			
				player = PyPlayer(iPlayer)
				if (player.isAlive()):
					unitList = player.getUnitList()
					for loopUnit in unitList:
						unitType = loopUnit.getUnitType()
						
						bVisible = False
						plot = loopUnit.plot()
						if (not plot.isNone()):
							bVisible = plot.isVisible(gc.getPlayer(self.iActiveLeader).getTeam(), False) and not loopUnit.isInvisible(gc.getPlayer(self.iActiveLeader).getTeam(), False)

						if unitType >= 0 and unitType < gc.getNumUnitInfos() and bVisible:
							iNumUnits = self.unitsList[unitType][3]
							if (iPlayer == self.iActiveLeader):
								iNumUnits += 1
							if loopUnit.getVisualOwner() in self.selectedLeaderList:
								self.unitsList[unitType][2].append(loopUnit)							
							
							self.unitsList[unitType] = (self.unitsList[unitType][0], self.unitsList[unitType][1], self.unitsList[unitType][2], iNumUnits)

			# sort by unit combat type
			self.unitsList.sort()
		
		szText = localText.getText("TXT_KEY_PEDIA_ALL_UNITS", ()).upper()
		if (-1 in self.selectedGroupList):
			szText = localText.changeTextColor(u"<u>" + szText + u"</u>", gc.getInfoTypeForString("COLOR_YELLOW"))
		if (bReload):
			screen.addListBoxGFC(self.UNIT_LIST_ID, "", self.X_TEXT+self.MAP_MARGIN, self.Y_TEXT+self.MAP_MARGIN+15, self.W_TEXT-2*self.MAP_MARGIN, self.H_TEXT-2*self.MAP_MARGIN-15, TableStyles.TABLE_STYLE_STANDARD)
			screen.enableSelect(self.UNIT_LIST_ID, False)
			screen.setStyle(self.UNIT_LIST_ID, "Table_StandardCiv_Style")
			screen.appendListBoxString(self.UNIT_LIST_ID, szText, WidgetTypes.WIDGET_MINIMAP_HIGHLIGHT, 1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		else:		
			screen.setListBoxStringGFC(self.UNIT_LIST_ID, 0, szText, WidgetTypes.WIDGET_MINIMAP_HIGHLIGHT, 1, -1, CvUtil.FONT_LEFT_JUSTIFY)

		iPrevUnitCombat = -2
		iItem = 1
		for iUnit in range(gc.getNumUnitInfos()):
			if (len(self.unitsList[iUnit][2]) > 0):
				if (iPrevUnitCombat != self.unitsList[iUnit][0] and self.unitsList[iUnit][0] != -1):
					iPrevUnitCombat = self.unitsList[iUnit][0]
					szDescription = gc.getUnitCombatInfo(self.unitsList[iUnit][0]).getDescription().upper()
					if (self.UL_isSelectedGroup(self.unitsList[iUnit][0], False)):
						szDescription = u"   <u>" + szDescription + u"</u>"
					else:
						szDescription = u"   " + szDescription
					if (self.UL_isSelectedGroup(self.unitsList[iUnit][0], True)):
						szDescription = localText.changeTextColor(szDescription, gc.getInfoTypeForString("COLOR_YELLOW"))
					if (bReload):
						screen.appendListBoxString(self.UNIT_LIST_ID, szDescription, WidgetTypes.WIDGET_MINIMAP_HIGHLIGHT, 1, self.unitsList[iUnit][0] + gc.getNumUnitInfos(), CvUtil.FONT_LEFT_JUSTIFY)
					else:
						screen.setListBoxStringGFC(self.UNIT_LIST_ID, iItem, szDescription, WidgetTypes.WIDGET_MINIMAP_HIGHLIGHT, 1, self.unitsList[iUnit][0] + gc.getNumUnitInfos(), CvUtil.FONT_LEFT_JUSTIFY)
					iItem += 1
				
				szDescription = gc.getUnitInfo(self.unitsList[iUnit][1]).getDescription() + u" (" + unicode(len(self.unitsList[iUnit][2])) + u")"
				if (self.UL_isSelectedUnitType(self.unitsList[iUnit][1], False)):
					szDescription = u"      <u>" + szDescription + u"</u>"
				else:
					szDescription = u"      " + szDescription
				if (self.UL_isSelectedUnitType(self.unitsList[iUnit][1], True)):
					szDescription = localText.changeTextColor(szDescription, gc.getInfoTypeForString("COLOR_YELLOW"))
				if (bReload):
					screen.appendListBoxString(self.UNIT_LIST_ID, szDescription, WidgetTypes.WIDGET_MINIMAP_HIGHLIGHT, 1, self.unitsList[iUnit][1], CvUtil.FONT_LEFT_JUSTIFY)
				else:
					screen.setListBoxStringGFC(self.UNIT_LIST_ID, iItem, szDescription, WidgetTypes.WIDGET_MINIMAP_HIGHLIGHT, 1, self.unitsList[iUnit][1], CvUtil.FONT_LEFT_JUSTIFY)
				iItem += 1
				
				for loopUnit in self.unitsList[iUnit][2]:
				
					if (self.bUnitDetails):
						szDescription = CyGameTextMgr().getSpecificUnitHelp(loopUnit, true, false)

						listMatches = re.findall("<.*?color.*?>", szDescription)	
						for szMatch in listMatches:
							szDescription = szDescription.replace(szMatch, u"")
						
						if (loopUnit.isWaiting()):
							szDescription = '*' + szDescription
							
						if (self.UL_isSelectedUnit(loopUnit.getOwner(), loopUnit.getID(), False)):
							szDescription = u"         <u>" + szDescription + u"</u>"
						else:
							szDescription = u"         " + szDescription

						if (self.UL_isSelectedUnit(loopUnit.getOwner(), loopUnit.getID(), True)):
							szDescription = localText.changeTextColor(szDescription, gc.getInfoTypeForString("COLOR_YELLOW"))

						if (bReload):
							screen.appendListBoxString(self.UNIT_LIST_ID, szDescription, WidgetTypes.WIDGET_MINIMAP_HIGHLIGHT, -loopUnit.getOwner(), loopUnit.getID(), CvUtil.FONT_LEFT_JUSTIFY)
						else:
							screen.setListBoxStringGFC(self.UNIT_LIST_ID, iItem, szDescription, WidgetTypes.WIDGET_MINIMAP_HIGHLIGHT, -loopUnit.getOwner(), loopUnit.getID(), CvUtil.FONT_LEFT_JUSTIFY)
						iItem += 1

					iPlayer = loopUnit.getVisualOwner()
					player = PyPlayer(iPlayer)
					iColor = gc.getPlayerColorInfo(gc.getPlayer(iPlayer).getPlayerColor()).getColorTypePrimary()
					screen.setMinimapColor(MinimapModeTypes.MINIMAPMODE_MILITARY, loopUnit.getX(), loopUnit.getY(), iColor, 0.6)
					if (self.UL_isSelectedUnit(loopUnit.getOwner(), loopUnit.getID(), True) and (iPlayer in self.selectedLeaderList)):
						
						if (player.getTeam().isAtWar(gc.getPlayer(self.iActiveLeader).getTeam())):
							iColor = gc.getInfoTypeForString("COLOR_RED")
						elif (gc.getPlayer(iPlayer).getTeam() != gc.getPlayer(self.iActiveLeader).getTeam()):
							iColor = gc.getInfoTypeForString("COLOR_YELLOW")
						else:
							iColor = gc.getInfoTypeForString("COLOR_WHITE")
						screen.minimapFlashPlot(loopUnit.getX(), loopUnit.getY(), iColor, -1)

	def refreshSelectedGroup(self, iSelected):
		if (iSelected in self.selectedGroupList):
			self.selectedGroupList.remove(iSelected)
		else:
			self.selectedGroupList.append(iSelected)
		self.UL_refreshUnitSelection(false)
			
	def refreshSelectedUnit(self, iPlayer, iUnitId):
		selectedUnit = (iPlayer, iUnitId)
		if (selectedUnit in self.selectedUnitList):
			self.selectedUnitList.remove(selectedUnit)
		else:
			self.selectedUnitList.append(selectedUnit)
		self.UL_refreshUnitSelection(false)		

	def refreshSelectedLeader(self, iPlayer):
		if self.iShiftKeyDown == 1:
			if (iPlayer in self.selectedLeaderList):
				self.selectedLeaderList.remove(iPlayer)
			else:
				self.selectedLeaderList.append(iPlayer)
		else:
			self.selectedLeaderList = []
			self.selectedLeaderList.append(iPlayer)	
	
		self.UL_refresh(True)



	def UL_isSelectedGroup(self, iGroup, bIndirect):
		if (bIndirect):
			if -1 in self.selectedGroupList:
				return True
			if iGroup == -1:
				return False
		return ((iGroup + gc.getNumUnitInfos()) in self.selectedGroupList)
				
	def UL_isSelectedUnitType(self, iUnit, bIndirect):
		if (bIndirect):
			if -1 in self.selectedGroupList:
				return True
			if self.UL_isSelectedGroup(gc.getUnitInfo(iUnit).getUnitCombatType(), True):
				return True
		return (iUnit in self.selectedGroupList)
		
	def UL_isSelectedUnit(self, iPlayer, iUnitId, bIndirect):
		if (bIndirect):
			if -1 in self.selectedGroupList:
				return True
			unit = gc.getPlayer(iPlayer).getUnit(iUnitId)
			if self.UL_isSelectedGroup(gc.getUnitInfo(unit.getUnitType()).getUnitCombatType(), True):
				return True
			if self.UL_isSelectedUnitType(unit.getUnitType(), True):
				return True
		return ((iPlayer, iUnitId) in self.selectedUnitList)




	def drawCombatExperience(self):
	
		if (gc.getPlayer(self.iActiveLeader).greatPeopleThreshold(true) > 0):

			screen = self.getScreen()

			# set the location of the great general bar - just below the map
			iPanel_X = self.X_MAP
			iPanel_Y = self.Y_MAP + self.H_MAP
			iPanel_W = self.W_MAP
			iPanel_H = 30 + 2 * self.MAP_MARGIN
					
			szPanel_ID = self.getNextWidgetName()
			screen.addPanel(szPanel_ID, u"", "", False, False, iPanel_X, iPanel_Y, iPanel_W, iPanel_H, PanelStyles.PANEL_STYLE_MAIN)

			self.X_GREAT_GENERAL_BAR = iPanel_X + self.MAP_MARGIN
			self.Y_GREAT_GENERAL_BAR = iPanel_Y + self.MAP_MARGIN
			self.W_GREAT_GENERAL_BAR = iPanel_W - iPanel_X - self.MAP_MARGIN
			self.H_GREAT_GENERAL_BAR = 30

			iExperience = gc.getPlayer(self.iActiveLeader).getCombatExperience()
			
			szGGBar_ID = self.getNextWidgetName()
			szGGTxt_ID = self.getNextWidgetName()

			screen.addStackedBarGFC(szGGBar_ID, self.X_GREAT_GENERAL_BAR, self.Y_GREAT_GENERAL_BAR, self.W_GREAT_GENERAL_BAR, self.H_GREAT_GENERAL_BAR, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_HELP_GREAT_GENERAL, -1, -1)
			screen.setStackedBarColors(szGGBar_ID, InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_GREAT_PEOPLE_STORED"))
			screen.setStackedBarColors(szGGBar_ID, InfoBarTypes.INFOBAR_RATE, gc.getInfoTypeForString("COLOR_GREAT_PEOPLE_RATE"))
			screen.setStackedBarColors(szGGBar_ID, InfoBarTypes.INFOBAR_RATE_EXTRA, gc.getInfoTypeForString("COLOR_EMPTY"))
			screen.setStackedBarColors(szGGBar_ID, InfoBarTypes.INFOBAR_EMPTY, gc.getInfoTypeForString("COLOR_EMPTY"))
			screen.setBarPercentage(szGGBar_ID, InfoBarTypes.INFOBAR_STORED, float(iExperience) / float(gc.getPlayer(self.iActiveLeader).greatPeopleThreshold(true)))

			screen.setLabel(szGGTxt_ID, "", localText.getText("TXT_KEY_MISC_COMBAT_EXPERIENCE", ()), CvUtil.FONT_CENTER_JUSTIFY, self.X_GREAT_GENERAL_BAR + self.W_GREAT_GENERAL_BAR/2, self.Y_GREAT_GENERAL_BAR + 6, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_HELP_GREAT_GENERAL, -1, -1)







	def minimapClicked(self):
		self.hideScreen()
						



	def getLeaderButtonWidget(self, iPlayer):
		szName = self.LEADER_BUTTON_ID + str(iPlayer)
		return szName





	# returns a unique ID for a widget in this screen
	def getNextWidgetName(self):
		szName = self.WIDGET_ID + str(self.nWidgetCount)
		self.nWidgetCount += 1
		return szName
	
	def deleteAllWidgets(self):
		screen = self.getScreen()
		i = self.nWidgetCount - 1
		while (i >= 0):
			self.nWidgetCount = i
			screen.deleteWidget(self.getNextWidgetName())
			i -= 1

		self.nWidgetCount = 0		

		# delete widgets with pre-defined names
		screen.deleteWidget(self.UNIT_BUTTON_ID)
		screen.deleteWidget(self.UNIT_LIST_ID)
		screen.deleteWidget(self.UNIT_BUTTON_LABEL_ID)
		screen.deleteWidget(self.MINIMAP_PANEL)

		for iLoopPlayer in range(gc.getMAX_PLAYERS()):
			screen.deleteWidget(self.getLeaderButtonWidget(iLoopPlayer))

		# hide the mini-map
		self.UL_SetMinimapVisibility(screen, false)

																				
	# handle the input for this screen...
	def handleInput (self, inputClass):
		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED):
			if (inputClass.getFunctionName() == self.UNIT_LOC_TAB_ID):
				self.iScreen = UNIT_LOCATION_SCREEN
				self.showUnitLocation()

			elif (inputClass.getFunctionName() == self.SIT_REP_TAB_ID):
				self.iScreen = SITUATION_REPORT_SCREEN
				self.showSituationReport()

			elif (inputClass.getFunctionName() == self.PLACE_HOLDER_TAB):
				self.iScreen = PLACE_HOLDER
				self.showGameSettingsScreen()

			elif (inputClass.getFunctionName() == self.UNIT_BUTTON_ID):
				self.bUnitDetails = not self.bUnitDetails
				self.UL_refreshUnitSelection(True)

		elif (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CHARACTER):
			if (inputClass.getData() == int(InputTypes.KB_LSHIFT)
			or  inputClass.getData() == int(InputTypes.KB_RSHIFT)):
				self.iShiftKeyDown = inputClass.getID() 

#		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED and inputClass.getFunctionName() == self.UNIT_BUTTON_ID) :
#			self.bUnitDetails = not self.bUnitDetails
#			self.refreshUnitSelection(True)
#		elif (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CHARACTER):
#			if (inputClass.getData() == int(InputTypes.KB_LSHIFT) or inputClass.getData() == int(InputTypes.KB_RSHIFT)):
#				self.iShiftKeyDown = inputClass.getID() 
		
		return 0


	def update(self, fDelta):
		return
