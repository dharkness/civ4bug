## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005

## Victory Screen shell used to build Military Advisor multi-tab display

from CvPythonExtensions import *
import CvUtil
import ScreenInput
import PyHelpers
import time
import re

import IconGrid_BUG

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
		self.iActivePlayer = -1
#		self.bVoteTab = False

		self.iScreen = UNIT_LOCATION_SCREEN

		# icongrid constants
		self.IconGridActive = False

		self.SHOW_LEADER_NAMES = False
		self.SHOW_ROW_BORDERS = True
		self.MIN_TOP_BOTTOM_SPACE = 60
		self.MIN_LEFT_RIGHT_SPACE = 25
		self.GROUP_BORDER = 8
		self.GROUP_LABEL_OFFSET = "   "
		self.MIN_COLUMN_SPACE = 5
		self.MIN_ROW_SPACE = 1

		# sit rep constants
		self.SITREP_PANEL_SPACE = 50
		self.TITLE_HEIGHT = 0
		self.TABLE_CONTROL_HEIGHT = 0
#		self.RESOURCE_ICON_SIZE = 34
		self.SCROLL_TABLE_UP = 1
		self.SCROLL_TABLE_DOWN = 2

		self.bWHEOOH = False
		self.bCurrentWar = False

						
	def getScreen(self):
		return CyGInterfaceScreen(self.SCREEN_NAME, self.screenId)

	def hideScreen(self):
		self.IconGridActive = False
		screen = self.getScreen()
		screen.hideScreen()
										
	def interfaceScreen(self):

		# Create a new screen
		screen = self.getScreen()
		if screen.isActive():
			return
		screen.setRenderInterfaceOnly(True);
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)

		self.iActivePlayer = CyGame().getActivePlayer()
		if self.iScreen == -1:
			self.iScreen = UNIT_LOCATION_SCREEN

# BUG - optional sit rep - start
#		if not BugScreens.isShowSitRep():
#			self.iScreen = UNIT_LOCATION_SCREEN
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
			self.showUnitLocation(True)
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

		self.drawTabs()

		#return
	
		#self.BUGPrint "tjp1"
		sColor = ["COLOR_PLAYER_BLACK", 
					"COLOR_PLAYER_BROWN", 
					"COLOR_PLAYER_CYAN", 
					"COLOR_PLAYER_GRAY", 
					"COLOR_PLAYER_PURPLE", 
					"COLOR_PLAYER_WHITE", 
					"COLOR_PLAYER_PEACH", 
					"COLOR_PLAYER_DARK_BLUE", 
					"COLOR_PLAYER_DARK_CYAN", 
					"COLOR_PLAYER_PINK", 
					"COLOR_PLAYER_DARK_YELLOW", 
					"COLOR_PLAYER_DARK_PINK", 
					"COLOR_PLAYER_DARK_PURPLE", 
					"COLOR_PLAYER_DARK_RED", 
					"COLOR_PLAYER_DARK_GREEN", 
					"COLOR_PLAYER_GREEN", 
					"COLOR_PLAYER_BLUE", 
					"COLOR_PLAYER_YELLOW",
					"COLOR_PLAYER_ORANGE", 
					"COLOR_PLAYER_RED"]

		#self.BUGPrint "tjp2"

# File "CvBUGMilitaryAdvisor", line 283, in showGameSettingsScreen
#
#ArgumentError: Python argument types in
#    CyGInterfaceScreen.addStackedBarGFCAt(CyGInterfaceScreen, str, CyGInterfaceScreen, int, int, int, int, CvPythonExtensions.InfoBarTypes, CvPythonExtensions.WidgetTypes, int, int)
#did not match C++ signature:
#    addStackedBarGFCAt(class CyGInterfaceScreen {lvalue}, char const *, char const *, int, int, int, int, int, enum WidgetTypes, int, int)
#ERR: Python function handleInput failed, module CvScreensInterface

#				screen.addStackedBarGFCAt( szStringHealth, szStringPanel, xOffset + 3, 26, 32, 11, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_GENERAL, k, -1 )

		self.tradePanel = self.getNextWidgetName()
		screen.addPanel("AA", "", "", True, True, 200, 100, 800, 600, PanelStyles.PANEL_STYLE_MAIN )


		for i in range(0, 15, 1):
			szBar_ID = self.getNextWidgetName()
			screen.addStackedBarGFCAt(szBar_ID, "AA", 200, 10 + i * 25, 100, 20, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			screen.setBarPercentage(szBar_ID, InfoBarTypes.INFOBAR_STORED, float( 100 ) / float( 100 ) )
			screen.setStackedBarColors(szBar_ID, InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString(sColor[i]))

			szTxt_ID = self.getNextWidgetName()
			screen.setTextAt (szTxt_ID, "AA", sColor[i], CvUtil.FONT_CENTER_JUSTIFY, 320, 10 + i * 25, -0.1, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		for i in range(15, 20, 1):
			szBar_ID = self.getNextWidgetName()
			screen.addStackedBarGFCAt(szBar_ID, "AA", 200, 40 + i * 25, 100, 20, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			screen.setBarPercentage(szBar_ID, InfoBarTypes.INFOBAR_STORED, float( 100 ) / float( 100 ) )
			screen.setStackedBarColors(szBar_ID, InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString(sColor[i]))

			szTxt_ID = self.getNextWidgetName()
			screen.setTextAt (szTxt_ID, "AA", sColor[i], CvUtil.FONT_CENTER_JUSTIFY, 320, 40 + i * 25, -0.1, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		#self.BUGPrint "tjp3"
		
		return










		activePlayer = gc.getPlayer(self.iActivePlayer)		

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
			if (player.isEverAlive() and iLoopPlayer != self.iActivePlayer and (gc.getTeam(player.getTeam()).isHasMet(activePlayer.getTeam()) or gc.getGame().isDebugMode()) and not player.isBarbarian() and not player.isMinorCiv()):
				screen.appendListBoxStringNoUpdate(szCivsTable, localText.getText("TXT_KEY_LEADER_CIV_DESCRIPTION", (player.getNameKey(), player.getCivilizationShortDescriptionKey())), WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
				screen.appendListBoxStringNoUpdate(szCivsTable, u"     (" + CyGameTextMgr().parseLeaderTraits(player.getLeaderType(), player.getCivilizationType(), True, False) + ")", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
				screen.appendListBoxStringNoUpdate(szCivsTable, " ", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )

		screen.updateListBox(szCivsTable)

		self.drawTabs()







# dev using icongrid
	def showSituationReport(self):

		self.deleteAllWidgets()
		screen = self.getScreen()
		self.initGrid(screen)
		
		activePlayer = gc.getPlayer(self.iActivePlayer)		

		# Assemble the panel
#		iPANEL_X = self.SITREP_LEFT_RIGHT_SPACE
#		iPANEL_Y = self.SITREP_TOP_BOTTOM_SPACE
#		iPANEL_WIDTH = self.W_SCREEN - 2 * self.SITREP_LEFT_RIGHT_SPACE
#		iPANEL_HEIGHT = self.H_SCREEN - 2 * self.SITREP_TOP_BOTTOM_SPACE

		iPANEL_X = 20
		iPANEL_Y = 60
		iPANEL_WIDTH = self.W_SCREEN - 40
		iPANEL_HEIGHT = self.H_SCREEN - 120

		#self.X_SCREEN = 500
		#s#elf.Y_SCREEN = 396
		#self.W_SCREEN = 1024
		#self.H_SCREEN = 768


		self.tradePanel = self.getNextWidgetName()
		screen.addPanel(self.tradePanel, "", "", True, True, iPANEL_X, iPANEL_Y, iPANEL_WIDTH, iPANEL_HEIGHT, PanelStyles.PANEL_STYLE_MAIN )
		
		self.SitRepGrid.createGrid()
		self.SitRepGrid.clearData()

		iRow = 0
		for iLoopPlayer in range(gc.getMAX_PLAYERS()):
			iLeader = gc.getPlayer(iLoopPlayer)

			if (iLeader.isAlive()
			and (gc.getTeam(iLeader.getTeam()).isHasMet(gc.getPlayer(self.iActivePlayer).getTeam())
			or gc.getGame().isDebugMode())
			and iLoopPlayer != self.iActivePlayer
			and not iLeader.isBarbarian()
			and not iLeader.isMinorCiv()):

				self.SitRepGrid.appendRow(iLeader.getName(), "")

				self.SitRepGrid.addIcon( iRow, self.Col_Leader
										, gc.getLeaderHeadInfo(iLeader.getLeaderType()).getButton()
										, WidgetTypes.WIDGET_LEADERHEAD, iLoopPlayer)

				# add attitude
#				szRel = self.SR_calculateRelations (iLoopLeader, self.iActivePlayer)
#				szText = self.SR_LRow_getAttitudeText (szRel, self.iActivePlayer, iLoopLeader)
#				self.SitRepGrid.setText(iRow, self.Col_Attitude, szText)

				# add worst enemy
#				self.Grid_WorstEnemy(iRow, iLoopLeader)

				# add current war opponents
				self.bCurrentWar = False
				self.Grid_CurrentWars(iRow, iLoopPlayer)

				self.SitRepGrid.addIcon( iRow, self.Col_StratRes
										, gc.getLeaderHeadInfo(iLeader.getLeaderType()).getButton()
										, WidgetTypes.WIDGET_LEADERHEAD, iLoopPlayer)

				self.bWHEOOH = False
				self.Grid_DeclareWar(iRow, iLoopPlayer)

#				if (self.bWHEOOH
#				and not self.bCurrentWar = True):
				if self.bWHEOOH:
					self.SitRepGrid.addStackedBar(iRow, self.Col_Threat, 75, "COLOR_PLAYER_RED", "red")
				else:
					self.SitRepGrid.addStackedBar(iRow, self.Col_Threat, 75, "COLOR_PLAYER_YELLOW", "yellow")

				iRow += 1

		self.SitRepGrid.refresh()

		self.drawTabs()

		return
















	def initGrid(self, screen):
		
		# columns are: leader, attitude, worse enemy, threat index, active wars, stategic resources, will declare

#		self.Col_Leader = 0
#		self.Col_Attitude = 1
#		self.Col_WEnemy = 2
#		self.Col_Threat = 3
#		self.Col_Curr_Wars = 4
#		self.Col_StratRes = 5
#		self.Col_WillDeclare = 6

#		columns = ( IconGrid_BUG.GRID_ICON_COLUMN,
#					IconGrid_BUG.GRID_TEXT_COLUMN,
#					IconGrid_BUG.GRID_ICON_COLUMN,
#					IconGrid_BUG.GRID_TEXT_COLUMN,
#					IconGrid_BUG.GRID_MULTI_LIST_COLUMN,
#					IconGrid_BUG.GRID_MULTI_LIST_COLUMN,
#					IconGrid_BUG.GRID_TEXT_COLUMN )

		self.Col_Leader = 0
		self.Col_Threat = 1
		self.Col_Curr_Wars = 2
		self.Col_StratRes = 3
		self.Col_WillDeclareOn = 4
		self.Col_WarDenial = 5

		columns = ( IconGrid_BUG.GRID_ICON_COLUMN,
					IconGrid_BUG.GRID_STACKEDBAR_COLUMN,
					IconGrid_BUG.GRID_MULTI_LIST_COLUMN,
					IconGrid_BUG.GRID_MULTI_LIST_COLUMN,
					IconGrid_BUG.GRID_MULTI_LIST_COLUMN,
					IconGrid_BUG.GRID_TEXT_COLUMN )

#		self.NUM_RESOURCE_COLUMNS = len(columns) - 1
		
		gridX = self.MIN_LEFT_RIGHT_SPACE + 10
		gridY = self.MIN_TOP_BOTTOM_SPACE + self.SITREP_PANEL_SPACE + self.TABLE_CONTROL_HEIGHT + self.TITLE_HEIGHT + 10
		gridWidth = self.W_SCREEN - self.MIN_LEFT_RIGHT_SPACE * 2 - 20
		gridHeight = self.H_SCREEN - self.MIN_TOP_BOTTOM_SPACE * 2 - self.SITREP_PANEL_SPACE - self.TITLE_HEIGHT - 20
		
#		self.resIconGridName = self.getNextWidgetName()
#class IconGrid:  def __init__(self, sWidgetId, screen, iX, iY, iWidth, iHeight, columns, bUseSmallIcons, bShowRowHeader, bShowRowBorder):


		self.SitRepGrid = IconGrid_BUG.IconGrid_BUG(self.getNextWidgetName(), screen, gridX, gridY, gridWidth, gridHeight,
													columns, True, self.SHOW_LEADER_NAMES, self.SHOW_ROW_BORDERS)

		# set constants
		self.SitRepGrid.setGroupBorder(self.GROUP_BORDER)
		self.SitRepGrid.setGroupLabelOffset(self.GROUP_LABEL_OFFSET)
		self.SitRepGrid.setMinColumnSpace(self.MIN_COLUMN_SPACE)
		self.SitRepGrid.setMinRowSpace(self.MIN_ROW_SPACE)

		# set headings
		self.SitRepGrid.setHeader(self.Col_Leader, "")
#		self.SitRepGrid.setHeader(self.Col_Attitude, localText.getText("TXT_KEY_MILITARY_SITREP_RELATIONSHIP", ()))
#		self.SitRepGrid.setHeader(self.Col_WEnemy, localText.getText("TXT_KEY_MILITARY_SITREP_WORSE_ENEMY", ()))
		self.SitRepGrid.setHeader(self.Col_Threat, localText.getText("TXT_KEY_MILITARY_SITREP_THREAD_INDEX", ()))
		self.SitRepGrid.setHeader(self.Col_Curr_Wars, localText.getText("TXT_KEY_MILITARY_SITREP_ACTIVE_WARS", ()))
		self.SitRepGrid.setHeader(self.Col_StratRes, localText.getText("TXT_KEY_MILITARY_SITREP_STRATEGIC_RESOURCES", ()))
		self.SitRepGrid.setHeader(self.Col_WillDeclareOn, localText.getText("TXT_KEY_MILITARY_SITREP_WILL_DECLARE", ()))
		self.SitRepGrid.setHeader(self.Col_WarDenial, localText.getText("TXT_KEY_MILITARY_SITREP_WAR_DENIAL", ()))

#		self.SitRepGrid.setTextColWidth(self.Col_Attitude, 100)
		self.SitRepGrid.setStackedBarColWidth(self.Col_Threat, 100)
		self.SitRepGrid.setTextColWidth(self.Col_WarDenial, 200)
		
		
		gridWidth = self.SitRepGrid.getPrefferedWidth()
		gridHeight = self.SitRepGrid.getPrefferedHeight()
		self.SITREP_LEFT_RIGHT_SPACE = (self.W_SCREEN - gridWidth - 20) / 2
		self.SITREP_TOP_BOTTOM_SPACE = (self.H_SCREEN - gridHeight - 20) / 2
		gridX = self.SITREP_LEFT_RIGHT_SPACE + 10
		gridY = self.SITREP_TOP_BOTTOM_SPACE + 10

		self.SitRepGrid.setPosition(gridX, gridY)
		self.SitRepGrid.setSize(gridWidth, gridHeight)

		self.IconGridActive = True		


	def Grid_WorstEnemy(self, iRow, iLeader):
		szWEnemyName = gc.getPlayer(iLeader).getWorstEnemyName()

		if szWEnemyName == "":
			self.SitRepGrid.addIcon(iRow, self.Col_WEnemy,
									ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_CANCEL").getPath(),
									WidgetTypes.WIDGET_LEADERHEAD, -1)
		else:
			for iLoopEnemy in range(gc.getMAX_PLAYERS()):
				if gc.getPlayer(iLoopEnemy).getName() == szWEnemyName:
					iWEnemy = iLoopEnemy
					break

			self.SitRepGrid.addIcon(iRow, self.Col_WEnemy,
									gc.getLeaderHeadInfo(gc.getPlayer(iWEnemy).getLeaderType()).getButton(), 
									WidgetTypes.WIDGET_LEADERHEAD, iLoopEnemy)
		return

	def Grid_CurrentWars(self, iRow, iLeader):
		iLeaderWars = []

		for iLoopPlayer in range(gc.getMAX_PLAYERS()):
			gcLoopLeader = gc.getPlayer(iLoopPlayer)
			if (gcLoopLeader.isAlive()
			and (gc.getTeam(gcLoopLeader.getTeam()).isHasMet(gc.getPlayer(self.iActivePlayer).getTeam())
			or gc.getGame().isDebugMode())
			and not gcLoopLeader.isBarbarian()
			and not gcLoopLeader.isMinorCiv()):
				if gc.getTeam(gc.getPlayer(iLeader).getTeam()).isAtWar(gcLoopLeader.getTeam()):
					iLeaderWars.append(iLoopPlayer)

		for iLoopPlayer in iLeaderWars:
			self.bCurrentWar = True
			self.SitRepGrid.addIcon(iRow, self.Col_Curr_Wars, 
									gc.getLeaderHeadInfo (gc.getPlayer(iLoopPlayer).getLeaderType()).getButton(), 
									WidgetTypes.WIDGET_LEADERHEAD, iLoopPlayer)
		return

	

	def Grid_DeclareWar(self, iRow, iPlayer):
		# this module will check if the iPlayer will declare war
		# on the other leaders.  We cannot check if the iPlayer, the iActivePlayer
		# and the iTargetPlayer don't all know each other.
		# However, the code wouldn't have got this far if the iPlayer didn't know the iActivePlayer
		# so we only need to check if the iPlayer and the iActivePlayer both know the iTargetPlayer.

		# also need to check on vassal state - will do that later

		iLeaderWars = []
		szWarDenial = ""

#		sReturn = ("", False, DenialTypes.NO_DENIAL)

		tradeData = TradeData()
		tradeData.ItemType = TradeableItems.TRADE_WAR

		pPlayer = gc.getPlayer(iPlayer)

		szPlayerName = gc.getPlayer(iPlayer).getName() + "/" + gc.getPlayer(iPlayer).getCivilizationShortDescription(0)
#		print "start: %s" % (szPlayerName)

		for iTargetPlayer in range(gc.getMAX_PLAYERS()):
			pTargetPlayer = gc.getPlayer(iTargetPlayer)
			
			if (pTargetPlayer.isAlive()
			and (gc.getTeam(pTargetPlayer.getTeam()).isHasMet(gc.getPlayer(self.iActivePlayer).getTeam())
			and  gc.getTeam(pTargetPlayer.getTeam()).isHasMet(gc.getPlayer(iPlayer).getTeam())
			or   gc.getGame().isDebugMode())
			and not iTargetPlayer == self.iActivePlayer
			and not iTargetPlayer == iPlayer
			and not gc.getTeam(pPlayer.getTeam()).isAtWar(pTargetPlayer.getTeam())
			and not pTargetPlayer.isBarbarian()
			and not pTargetPlayer.isMinorCiv()):

				szPlayerName = gc.getPlayer(iTargetPlayer).getName() + "/" + gc.getPlayer(iTargetPlayer).getCivilizationShortDescription(0)
#				print "TargetPlayer: %s" % (szPlayerName)

				tradeData.iData = iTargetPlayer
				if (pPlayer.canTradeItem(self.iActivePlayer, tradeData, False)):
#					print "trade is possible"
					WarDenial = pPlayer.getTradeDenial(self.iActivePlayer, tradeData)
					if WarDenial == DenialTypes.NO_DENIAL:
						iLeaderWars.append(iTargetPlayer)
					elif szWarDenial == "":
						szWarDenial = gc.getDenialInfo(WarDenial).getDescription()
#						print WarDenial

					if WarDenial == DenialTypes.DENIAL_TOO_MANY_WARS:
						self.bWHEOOH = True

#					if szWillTradeWar == "":
#						szWillTradeWar = "YES"
#					elif szWillTradeWar == "NO":
#						szWillTradeWar = "MIXED"
#				else:
#					print "no trade is possible"
#					if szWillTradeWar == "":
#						szWillTradeWar = "NO"
#					elif szWillTradeWar == "YES":
#						szWillTradeWar = "MIXED"

		#			if sReturn[1] == False:
		#				sReturn[1] = True
		#				sReturn[2] = pPlayer.getTradeDenial(self.iActivePlayer, tradeData)
		#				print "denial %i" % (sReturn[2])

		#print sReturn

#		self.Grid_DeclareWar(iRow, iLoopLeader)
#		if sDeclare[1] == -1:
#		self.SitRepGrid.setText(iRow, self.Col_WillDeclare, szWillTradeWar)
#		else:
#			self.SitRepGrid.setText(iRow, self.Col_WillDeclare, sDeclare[0] + " [")   # + gc.getDenialInfo(sDeclare[1]).getDescription + "]")
				
#		if szWillTradeWar == "":
#			szWillTradeWar = "NOO"

		for iLoopPlayer in iLeaderWars:
			self.SitRepGrid.addIcon(iRow, self.Col_WillDeclareOn, 
									gc.getLeaderHeadInfo (gc.getPlayer(iLoopPlayer).getLeaderType()).getButton(), 
									WidgetTypes.WIDGET_LEADERHEAD, iLoopPlayer)

		if szWarDenial != "":
			self.SitRepGrid.setText(iRow, self.Col_WarDenial, szWarDenial)

		return


		

# code here to check if iLeader will trade war with iLoopLeader to iActiveLeader

#		return sReturn

#			if (iLeader.isAlive()
#			and (gc.getTeam(iLeader.getTeam()).isHasMet(gc.getPlayer(self.iActivePlayer).getTeam())
#			or gc.getGame().isDebugMode())
#			and iLoopLeader != self.iActivePlayer
#			and not iLeader.isBarbarian()
#			and not iLeader.isMinorCiv()):





#			loopLeader = gc.getPlayer(iLoopLeaderID)
#			iLoopTeamID = loopPlayer.getTeam()
#			loopTeam = gc.getTeam(iLoopTeamID)
#			if (loopPlayer.isBarbarian()
#			or loopPlayer.isMinorCiv()
#			or not loopPlayer.isAlive()
#			or ):
#				continue
	


	def getWarDeclarationTrades(self, activePlayer, activeTeam):
		iActivePlayerID = activePlayer.getID()
		iActiveTeamID = activeTeam.getID()
		tradeData = TradeData()
		tradeData.ItemType = TradeableItems.TRADE_WAR
		currentTrades = set()
		
		for iLoopPlayerID in range(gc.getMAX_PLAYERS()):
			loopPlayer = gc.getPlayer(iLoopPlayerID)
			iLoopTeamID = loopPlayer.getTeam()
			loopTeam = gc.getTeam(iLoopTeamID)
			if (loopPlayer.isBarbarian() or loopPlayer.isMinorCiv() or not loopPlayer.isAlive()):
				continue
			if (iLoopPlayerID != iActivePlayerID and loopTeam.isHasMet(iActiveTeamID)):
#				if (activeTeam.isOpenBorders(iLoopTeamID) or loopTeam.isOpenBorders(iActiveTeamID)):
#					continue
#				if (activeTeam.isOpenBordersTrading() or loopTeam.isOpenBordersTrading()):
#					#tradeData.iData = None
				if (loopPlayer.canTradeItem(iActivePlayerID, tradeData, False)):
					if (loopPlayer.getTradeDenial(iActivePlayerID, tradeData) == DenialTypes.NO_DENIAL): # will trade
						currentTrades.add(iLoopPlayerID)
		return currentTrades


		








#		for iLoopPlayer in range(nCount + 1, 9):
#			self.SR_drawLeaderRows(screen, szMainPanel_ID, -1, nCount)

#		self.SR_drawLeaderRows(screen, szMainPanel_ID, iLoopPlayer)
#		self.SR_drawLeaderRows(screen, szMainPanel_ID, iLoopPlayer)

#		zsRowsPanel_ID = self.getNextWidgetName()
#		screen.addPanel(zsRowsPanel_ID, "", "", True, True, 0, 104, self.W_SCREEN, self.H_SCREEN - 155, PanelStyles.PANEL_STYLE_MAIN)

#		self.drawGlanceRows (screen, zsRowsPanel_ID, self.iSelectedLeader != self.iActivePlayer, self.iSelectedLeader)





# HEADER
# LEADER BARS [ICON, RELATIONSHIP (FROM GLANCE), THREAD INDEX, ACTIVE WARS (SMALL LEADER ICONS), STRATEGIC RESOURCES, WILL DECLARE WAR (PLUS REASON WHY NOT)]

# REASONS WHY NOT ... http://civilization4.net/files/modding/PythonAPI/Types/DenialTypes.html
# TRADABLE ITEMS ... http://civilization4.net/files/modding/PythonAPI/Types/TradeableItems.html
# STRATEGIC RESOURCES ... copper, iron, aluminimium, oil, uranium






















	def SR_LRow_ThreatIndex(self, screen, sPanel, iLeader, nCount):

		iThreatIndex = 20 + nCount * 15



		if iThreatIndex <= 20:
			szColor = "COLOR_GREEN"
			szText = localText.getText("TXT_KEY_MILITARY_THREAD_INDEX_NIL", ())
		elif iThreatIndex <= 40:
			szColor = "COLOR_PLAYER_BROWN"
			szText = localText.getText("TXT_KEY_MILITARY_THREAD_INDEX_LOW", ())
		elif iThreatIndex <= 60:
			szColor = "COLOR_YELLOW"
			szText = localText.getText("TXT_KEY_MILITARY_THREAD_INDEX_MODERATE", ())
		elif iThreatIndex <= 75:
			szColor = "COLOR_PLAYER_ORANGE"
			szText = localText.getText("TXT_KEY_MILITARY_THREAD_INDEX_HIGH", ())
		else:
			szColor = "COLOR_RED"
			szText = localText.getText("TXT_KEY_MILITARY_THREAD_INDEX_EXTREME", ())


		szBar_ID = self.getNextWidgetName()
		screen.addStackedBarGFCAt(szBar_ID, sPanel, self.SitRep_X3, self.Y_Text_Offset + self.SitRep_Y_Offset - 3, 100, 26, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.setBarPercentage(szBar_ID, InfoBarTypes.INFOBAR_STORED, float( iThreatIndex ) / float( 100 ) )
		screen.setStackedBarColors(szBar_ID, InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString(szColor))
		#screen.setStackedBarColors(szStringHealth, InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_RED"))
		#screen.show(szPanel_ID)

		szTxt_ID = self.getNextWidgetName()
		screen.setTextAt (szTxt_ID, sPanel, szText, CvUtil.FONT_CENTER_JUSTIFY, self.SitRep_X3+50, self.Y_Text_Offset + self.SitRep_Y_Offset, -0.1, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

#		szText = "Threat"

#		szPanel_ID = self.getNextWidgetName()
#		screen.setTextAt (szPanel_ID, sPanel, szText, CvUtil.FONT_CENTER_JUSTIFY, self.SitRep_X3, self.Y_Text_Offset + self.SitRep_Y_Offset, -0.1, FontTypes.GAME_FONT, WidgetTypes.WIDGET_LEADERHEAD, iLeader, self.iActivePlayer)


		#szBar_ID = self.getNextWidgetName()
		#szTxt_ID = self.getNextWidgetName()

#		screen.addStackedBarGFC(szGGBar_ID, self.X_GREAT_GENERAL_BAR, self.Y_GREAT_GENERAL_BAR, self.W_GREAT_GENERAL_BAR, self.H_GREAT_GENERAL_BAR,
#								InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_HELP_GREAT_GENERAL, -1, -1)
#		screen.setStackedBarColors(szGGBar_ID, InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_GREAT_PEOPLE_STORED"))
#		screen.setStackedBarColors(szGGBar_ID, InfoBarTypes.INFOBAR_RATE, gc.getInfoTypeForString("COLOR_GREAT_PEOPLE_RATE"))
#		screen.setStackedBarColors(szGGBar_ID, InfoBarTypes.INFOBAR_RATE_EXTRA, gc.getInfoTypeForString("COLOR_EMPTY"))
#		screen.setStackedBarColors(szGGBar_ID, InfoBarTypes.INFOBAR_EMPTY, gc.getInfoTypeForString("COLOR_EMPTY"))
#		screen.setBarPercentage(szGGBar_ID, InfoBarTypes.INFOBAR_STORED, float(iExperience) / float(gc.getPlayer(self.iActivePlayer).greatPeopleThreshold(true)))

#		screen.setLabel(szGGTxt_ID, "", localText.getText("TXT_KEY_MISC_COMBAT_EXPERIENCE", ()), CvUtil.FONT_CENTER_JUSTIFY, self.X_GREAT_GENERAL_BAR + self.W_GREAT_GENERAL_BAR/2, self.Y_GREAT_GENERAL_BAR + 6, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_HELP_GREAT_GENERAL, -1, -1)

		#self.Z_CONTROLS = -6.3
		#screen.addStackedBar(zsBar_ID, sPanel, 2, 2, 100, 30, self.Z_CONTROLS, 2, WidgetTypes.WIDGET_LEADERHEAD, -1, -1)
		#screen.setStackedBarColors(zsBar_ID, InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_GREAT_PEOPLE_STORED"))
		#screen.setBarPercentage(zsBar_ID, InfoBarTypes.INFOBAR_STORED, float(45) / float(100))











	def SR_LRow_StratResources(self, screen, sPanel, iLeader, nCount):

		activePlayer = gc.getPlayer(self.iActivePlayer)		

		iBUTTON_SIZE = 32
		screen.attachMultiListControlGFC(sPanel, "StratRes" + sPanel, "", 1, iBUTTON_SIZE, iBUTTON_SIZE, TableStyles.TABLE_STYLE_STANDARD)

		if (not activePlayer.canTradeNetworkWith(iLeader) and not gc.getGame().isDebugMode()):
			screen.appendMultiListButton("StratRes" + sPanel, ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_CANCEL").getPath(), 0, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
		else:
			StratRes = []

			tradeData = TradeData()
			tradeData.ItemType = TradeableItems.TRADE_RESOURCES

			# copper
			tradeData.iData = gc.getInfoTypeForString("BONUS_COPPER")
			if (gc.getPlayer(iLeader).canTradeItem(self.iActivePlayer, tradeData, False)):
				StratRes.append(tradeData.iData)

			# iron
			tradeData.iData = gc.getInfoTypeForString("BONUS_IRON")
			if (gc.getPlayer(iLeader).canTradeItem(self.iActivePlayer, tradeData, False)):
				StratRes.append(tradeData.iData)

			# horse
			tradeData.iData = gc.getInfoTypeForString("BONUS_HORSE")
			if (gc.getPlayer(iLeader).canTradeItem(self.iActivePlayer, tradeData, False)):
				StratRes.append(tradeData.iData)

			# ivory
			tradeData.iData = gc.getInfoTypeForString("BONUS_IVORY")
			if (gc.getPlayer(iLeader).canTradeItem(self.iActivePlayer, tradeData, False)):
				StratRes.append(tradeData.iData)

			# aluminum
			tradeData.iData = gc.getInfoTypeForString("BONUS_ALUMINUM")
			if (gc.getPlayer(iLeader).canTradeItem(self.iActivePlayer, tradeData, False)):
				StratRes.append(tradeData.iData)

			# oil
			tradeData.iData = gc.getInfoTypeForString("BONUS_OIL")
			if (gc.getPlayer(iLeader).canTradeItem(self.iActivePlayer, tradeData, False)):
				StratRes.append(tradeData.iData)

			# unanium
			tradeData.iData = gc.getInfoTypeForString("BONUS_URANIUM")
			if (gc.getPlayer(iLeader).canTradeItem(self.iActivePlayer, tradeData, False)):
				StratRes.append(tradeData.iData)

			for iLoopBonus in StratRes:
				screen.appendMultiListButton("StratRes" + sPanel, gc.getBonusInfo(iLoopBonus).getButton(), 0, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, iLoopBonus, -1, False)

#gc.getBonusInfo(iLoopBonus).getTechReveal()

# amount of resources in a circle ...
		# add the circles behind the amounts

#		if (self.RES_SHOW_SURPLUS_AMOUNT_ON_TOP):
#			for iIndex in range(len(listSurplus)):
#				screen.addDDSGFC( self.availableTable + "Circle" + str(iIndex)
#								 , ArtFileMgr.getInterfaceArtInfo("WHITE_CIRCLE_40").getPath()
#								 , self.SURPLUS_CIRCLE_X_START + iIndex * self.RESOURCE_ICON_SIZE, self.SURPLUS_CIRCLE_Y
#								 , 16, 16, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
		# add the table showing the amounts

#		screen.addTableControlGFC( self.availableTable, len(listSurplus)
#							     , self.SURPLUS_TABLE_X, self.SURPLUS_TABLE_Y
#							     , len(listSurplus) * self.RESOURCE_ICON_SIZE, self.TABLE_CONTROL_HEIGHT
#							     , False, False, 16, 16, TableStyles.TABLE_STYLE_EMPTY )
		
		# Add the bonuses to the surplus panel with their amount

#		for iIndex in range(len(listSurplus)):
#			screen.appendMultiListButton( self.availableMultiList, gc.getBonusInfo(listSurplus[iIndex]).getButton(), 0
#										, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, listSurplus[iIndex], -1, False )
#			screen.setTableColumnHeader( self.availableTable, iIndex, u"", self.RESOURCE_ICON_SIZE )
			
#			amount = activePlayer.getNumTradeableBonuses(listSurplus[iIndex])
#			if (self.RES_SHOW_EXTRA_AMOUNT):
#				amount = amount - 1
			
#			if (self.RES_SHOW_SURPLUS_AMOUNT_ON_TOP):
#				amountStr = u"<font=2>" + localText.changeTextColor(str(amount), gc.getInfoTypeForString("COLOR_YELLOW")) + "</font>"
#			else:
#				amountStr = u"<font=3>" + str(amount) + "</font>"
#			screen.setTableText( self.availableTable, iIndex, 0, amountStr, "", WidgetTypes.WIDGET_GENERAL, -1, -1, 0 )





#			for iLoopBonus in range(gc.getNumBonusInfos()):
#				tradeData.iData = iLoopBonus
#				if (gc.getPlayer(iLoopPlayer).canTradeItem(self.iActivePlayer, tradeData, False)):
#					if (gc.getPlayer(iLoopPlayer).getTradeDenial(self.iActivePlayer, tradeData) == DenialTypes.NO_DENIAL):
#						listTradeable.append(iLoopBonus)
#					else:
#						listUntradeable.append(iLoopBonus)
						
#						if len(listTradeable) > 0:
#							screen.attachLabel(currentPlayerPanelName, "", u"<font=4>" + localText.getText("TXT_KEY_FOREIGN_ADVISOR_FOR_TRADE", ()) + u"</font>")
							
#			screen.attachMultiListControlGFC(currentPlayerPanelName, "ChildTrade" + currentPlayerPanelName, "", 1, self.BUTTON_SIZE, self.BUTTON_SIZE, TableStyles.TABLE_STYLE_STANDARD)
#			for iLoopBonus in listTradeable:
#				screen.appendMultiListButton("ChildTrade" + currentPlayerPanelName, gc.getBonusInfo(iLoopBonus).getButton(), 0, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, iLoopBonus, -1, False)





























	def showUnitLocation(self, bReload):

		self.deleteAllWidgets()	
		screen = self.getScreen()

		activePlayer = PyHelpers.PyPlayer(self.iActivePlayer)
		iActiveTeam = gc.getPlayer(self.iActivePlayer).getTeam()
		
		self.unitsList = [(0, 0, [], 0)] * gc.getNumUnitInfos()
		self.selectedUnitList = []
		self.selectedLeaderList.append(self.iActivePlayer)

		if bReload:
			self.UL_initMinimap(screen)

		self.drawCombatExperience()

		# refresh the unit location
		self.UL_refresh(true)

		self.drawTabs()




	def UL_initMinimap(self, iScreen):
		# Minimap initialization
		iMap_W = CyMap().getGridWidth()
		iMap_H = CyMap().getGridHeight()
		self.H_MAP = (self.W_MAP * iMap_H) / iMap_W
		if (self.H_MAP > self.H_MAP_MAX):
			self.W_MAP = (self.H_MAP_MAX * iMap_W) / iMap_H
			self.H_MAP = self.H_MAP_MAX

		szPanel_ID = self.MINIMAP_PANEL
		iScreen.addPanel(szPanel_ID, u"", "", False, False, self.X_MAP, self.Y_MAP, self.W_MAP, self.H_MAP, PanelStyles.PANEL_STYLE_MAIN)
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
	
		if (self.iActivePlayer < 0):
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
			if (player.isAlive() and (gc.getTeam(player.getTeam()).isHasMet(gc.getPlayer(self.iActivePlayer).getTeam()) or gc.getGame().isDebugMode())):
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
				szText = localText.getText("TXT_KEY_MILITARY_ADVISOR_UNIT_TOGGLE_OFF", ())
				screen.setButtonGFC(self.UNIT_BUTTON_ID, u"", "", iBtn_X, iBtn_Y, 20, 20, WidgetTypes.WIDGET_GENERAL, -1, -1, ButtonStyles.BUTTON_STYLE_CITY_MINUS )
				screen.setLabel(self.UNIT_BUTTON_LABEL_ID, "", szText, CvUtil.FONT_LEFT_JUSTIFY, iTxt_X, iTxt_Y, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			else:
				szText = localText.getText("TXT_KEY_MILITARY_ADVISOR_UNIT_TOGGLE_ON", ())
				screen.setButtonGFC(self.UNIT_BUTTON_ID, u"", "", iBtn_X, iBtn_Y, 20, 20, WidgetTypes.WIDGET_GENERAL, -1, -1, ButtonStyles.BUTTON_STYLE_CITY_PLUS )
				screen.setLabel(self.UNIT_BUTTON_LABEL_ID, "", szText, CvUtil.FONT_LEFT_JUSTIFY, iTxt_X, iTxt_Y, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

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
							bVisible = plot.isVisible(gc.getPlayer(self.iActivePlayer).getTeam(), False) and not loopUnit.isInvisible(gc.getPlayer(self.iActivePlayer).getTeam(), False)

						if unitType >= 0 and unitType < gc.getNumUnitInfos() and bVisible:
							iNumUnits = self.unitsList[unitType][3]
							if (iPlayer == self.iActivePlayer):
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
						
						if (player.getTeam().isAtWar(gc.getPlayer(self.iActivePlayer).getTeam())):
							iColor = gc.getInfoTypeForString("COLOR_RED")
						elif (gc.getPlayer(iPlayer).getTeam() != gc.getPlayer(self.iActivePlayer).getTeam()):
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
	
		if (gc.getPlayer(self.iActivePlayer).greatPeopleThreshold(true) > 0):

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

			iExperience = gc.getPlayer(self.iActivePlayer).getCombatExperience()
			
			szGGBar_ID = self.getNextWidgetName()
			szGGTxt_ID = self.getNextWidgetName()

			screen.addStackedBarGFC(szGGBar_ID, self.X_GREAT_GENERAL_BAR, self.Y_GREAT_GENERAL_BAR, self.W_GREAT_GENERAL_BAR, self.H_GREAT_GENERAL_BAR, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_HELP_GREAT_GENERAL, -1, -1)
			screen.setStackedBarColors(szGGBar_ID, InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_GREAT_PEOPLE_STORED"))
			screen.setStackedBarColors(szGGBar_ID, InfoBarTypes.INFOBAR_RATE, gc.getInfoTypeForString("COLOR_GREAT_PEOPLE_RATE"))
			screen.setStackedBarColors(szGGBar_ID, InfoBarTypes.INFOBAR_RATE_EXTRA, gc.getInfoTypeForString("COLOR_EMPTY"))
			screen.setStackedBarColors(szGGBar_ID, InfoBarTypes.INFOBAR_EMPTY, gc.getInfoTypeForString("COLOR_EMPTY"))
			screen.setBarPercentage(szGGBar_ID, InfoBarTypes.INFOBAR_STORED, float(iExperience) / float(gc.getPlayer(self.iActivePlayer).greatPeopleThreshold(true)))

			screen.setLabel(szGGTxt_ID, "", localText.getText("TXT_KEY_MISC_COMBAT_EXPERIENCE", ()), CvUtil.FONT_CENTER_JUSTIFY, self.X_GREAT_GENERAL_BAR + self.W_GREAT_GENERAL_BAR/2, self.Y_GREAT_GENERAL_BAR + 6, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_HELP_GREAT_GENERAL, -1, -1)







	def minimapClicked(self):
		self.hideScreen()
						



	def getLeaderButtonWidget(self, iPlayer):
		szName = self.LEADER_BUTTON_ID + str(iPlayer)
		return szName


	def scrollGrid_Up(self):
		if self.iScreen == SITUATION_REPORT_SCREEN:
			self.SitRepGrid.scrollUp()

	def scrollGrid_Down(self):
		if self.iScreen == SITUATION_REPORT_SCREEN:
			self.SitRepGrid.scrollDown()



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
		#screen.hide(self.MINIMAP_PANEL)

		for iLoopPlayer in range(gc.getMAX_PLAYERS()):
			screen.deleteWidget(self.getLeaderButtonWidget(iLoopPlayer))

		# hide the mini-map
		#self.UL_SetMinimapVisibility(screen, false)

		# clear the grid
		if self.IconGridActive:
			self.SitRepGrid.hideGrid()
			self.IconGridActive = False


																				
	# handle the input for this screen...
	def handleInput (self, inputClass):
		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED):
			if (inputClass.getFunctionName() == self.UNIT_LOC_TAB_ID):
				self.iScreen = UNIT_LOCATION_SCREEN
				self.showUnitLocation(False)

			elif (inputClass.getFunctionName() == self.SIT_REP_TAB_ID):
				self.iScreen = SITUATION_REPORT_SCREEN
				self.showSituationReport()

			elif (inputClass.getFunctionName() == self.PLACE_HOLDER_TAB):
				self.iScreen = PLACE_HOLDER
				self.showGameSettingsScreen()

			elif (inputClass.getFunctionName() == self.UNIT_BUTTON_ID):
				self.bUnitDetails = not self.bUnitDetails
				self.UL_refreshUnitSelection(True)

			elif (inputClass.getButtonType() == WidgetTypes.WIDGET_GENERAL):
				if (inputClass.getData1() == self.SCROLL_TABLE_UP):
					print "scroll up"
					self.scrollGrid_Up()
				elif (inputClass.getData1() == self.SCROLL_TABLE_DOWN):
					print "scroll down"
					self.scrollGrid_Down()

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
