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
#PLACE_HOLDER = 2

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
#		self.PLACE_HOLDER_TAB = "placeholder"

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


		self.iPlayerPower = 0
		self.iDemographicsMission = -1









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

		self.minimapInitialized = False
		self.iScreen = UNIT_LOCATION_SCREEN

		# icongrid constants
		self.IconGridActive = False

		self.SHOW_LEADER_NAMES = False
		self.SHOW_ROW_BORDERS = True
		self.MIN_TOP_BOTTOM_SPACE = 30
		self.MIN_LEFT_RIGHT_SPACE = 10
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
		
		self.unitLocationInitDone = False
		if self.iScreen == UNIT_LOCATION_SCREEN:
			self.showUnitLocation()
		elif self.iScreen == SITUATION_REPORT_SCREEN:
			self.showSituationReport()
#		elif self.iScreen == PLACE_HOLDER:
#			self.showGameSettingsScreen()

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

# dev using icongrid
	def showSituationReport(self):

		self.deleteAllWidgets()
		screen = self.getScreen()

		# get Player arrays
		iVassals = [[]] * gc.getMAX_PLAYERS()
		iDefPacks = [[]] * gc.getMAX_PLAYERS()
		bVassals = False
		bDefPacks = False
		for iLoopPlayer in range(gc.getMAX_PLAYERS()):
			pPlayer = gc.getPlayer(iLoopPlayer)

			if (pPlayer.isAlive()
			and (gc.getTeam(pPlayer.getTeam()).isHasMet(gc.getPlayer(self.iActivePlayer).getTeam())
			or gc.getGame().isDebugMode())
			and iLoopPlayer != self.iActivePlayer
			and not pPlayer.isBarbarian()
			and not pPlayer.isMinorCiv()):
				iVassals[iLoopPlayer] = self.getVassals(iLoopPlayer)
				iDefPacks[iLoopPlayer] = self.getDefPacks(iLoopPlayer)

				if len(iVassals[iLoopPlayer]) > 0:
					bVassals = True

				if len(iDefPacks[iLoopPlayer]) > 0:
					bDefPacks = True

		self.initGrid(screen, bVassals, bDefPacks)
		self.initPower()
		
		activePlayer = gc.getPlayer(self.iActivePlayer)		

		
		# Assemble the panel
#		iPANEL_X = self.SITREP_LEFT_RIGHT_SPACE
#		iPANEL_Y = self.SITREP_TOP_BOTTOM_SPACE
#		iPANEL_WIDTH = self.W_SCREEN - 2 * self.SITREP_LEFT_RIGHT_SPACE
#		iPANEL_HEIGHT = self.H_SCREEN - 2 * self.SITREP_TOP_BOTTOM_SPACE

		iPANEL_X = 5
		iPANEL_Y = 60
		iPANEL_WIDTH = self.W_SCREEN - 20
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
			pPlayer = gc.getPlayer(iLoopPlayer)

			if (pPlayer.isAlive()
			and (gc.getTeam(pPlayer.getTeam()).isHasMet(gc.getPlayer(self.iActivePlayer).getTeam())
			or gc.getGame().isDebugMode())
			and iLoopPlayer != self.iActivePlayer
			and not pPlayer.isBarbarian()
			and not pPlayer.isMinorCiv()):

				self.SitRepGrid.appendRow(pPlayer.getName(), "")

				# add leaderhead icon
				self.SitRepGrid.addIcon( iRow, self.Col_Leader
										, gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getButton()
										, WidgetTypes.WIDGET_LEADERHEAD, iLoopPlayer)

				# add worst enemy
#				self.Grid_WorstEnemy(iRow, iLoopLeader)

				# add strategic differences
				self.Grid_Strategic_Resources(iRow, iLoopPlayer)

				# add current war opponents
				self.bCurrentWar = False
				iActiveWars = self.GetActiveWars(iRow, iLoopPlayer)
				if len(iActiveWars) > 0:
					self.bCurrentWar = True
					
				for iLoopPlayer2 in iActiveWars:
					self.SitRepGrid.addIcon(iRow, self.Col_Curr_Wars, 
											gc.getLeaderHeadInfo (gc.getPlayer(iLoopPlayer2).getLeaderType()).getButton(), 
											WidgetTypes.WIDGET_LEADERHEAD, iLoopPlayer2)

				# show vassals
				if bVassals:
					for iLoopPlayer2 in iVassals[iLoopPlayer]:
						self.SitRepGrid.addIcon(iRow, self.Col_Vassals, 
												gc.getLeaderHeadInfo (gc.getPlayer(iLoopPlayer2).getLeaderType()).getButton(), 
												WidgetTypes.WIDGET_LEADERHEAD, iLoopPlayer2)

				# show defensive packs
				if bDefPacks:
					for iLoopPlayer2 in iDefPacks[iLoopPlayer]:
						self.SitRepGrid.addIcon(iRow, self.Col_DefPacks, 
												gc.getLeaderHeadInfo (gc.getPlayer(iLoopPlayer2).getLeaderType()).getButton(), 
												WidgetTypes.WIDGET_LEADERHEAD, iLoopPlayer2)

				# show players that the current player will declare on
				self.bWHEOOH = False
				iActiveWars = self.GetDeclareWar(iRow, iLoopPlayer)
				for iLoopPlayer2 in iActiveWars:
					self.SitRepGrid.addIcon(iRow, self.Col_WillDeclareOn, 
											gc.getLeaderHeadInfo (gc.getPlayer(iLoopPlayer2).getLeaderType()).getButton(), 
											WidgetTypes.WIDGET_LEADERHEAD, iLoopPlayer2)
				# WHEOOH
				if self.bWHEOOH:
					sWHEOOH = u" %c" % CyGame().getSymbolID(FontSymbols.OCCUPATION_CHAR)
				else:
					sWHEOOH = ""

				self.SitRepGrid.setText(iRow, self.Col_WHEOOH, sWHEOOH)

				# add the threat index
				self.Grid_ThreatIndex(iRow, iLoopPlayer)

				iRow += 1

		self.SitRepGrid.refresh()

		self.drawTabs()

		return















	def initGrid(self, screen, bVassals, bDefPacks):
		
		self.Col_Leader = 0
		self.Col_WHEOOH = 1
		self.Col_Threat = 2
		self.Col_Curr_Wars = 6
		self.Col_StratResPos = 3
		self.Col_StratResNeg = 4
		self.Col_WillDeclareOn = 5
		self.Col_Vassals = 7
		self.Col_DefPacks = 8

		if (not bVassals and not bDefPacks):
			columns = ( IconGrid_BUG.GRID_ICON_COLUMN,
						IconGrid_BUG.GRID_TEXT_COLUMN,
						IconGrid_BUG.GRID_STACKEDBAR_COLUMN,
						IconGrid_BUG.GRID_MULTI_LIST_COLUMN,
						IconGrid_BUG.GRID_MULTI_LIST_COLUMN,
						IconGrid_BUG.GRID_MULTI_LIST_COLUMN,
						IconGrid_BUG.GRID_MULTI_LIST_COLUMN)
		if (bVassals and bDefPacks):
			columns = ( IconGrid_BUG.GRID_ICON_COLUMN,
						IconGrid_BUG.GRID_TEXT_COLUMN,
						IconGrid_BUG.GRID_STACKEDBAR_COLUMN,
						IconGrid_BUG.GRID_MULTI_LIST_COLUMN,
						IconGrid_BUG.GRID_MULTI_LIST_COLUMN,
						IconGrid_BUG.GRID_MULTI_LIST_COLUMN,
						IconGrid_BUG.GRID_MULTI_LIST_COLUMN,
						IconGrid_BUG.GRID_MULTI_LIST_COLUMN,
						IconGrid_BUG.GRID_MULTI_LIST_COLUMN)
		else:
			columns = ( IconGrid_BUG.GRID_ICON_COLUMN,
						IconGrid_BUG.GRID_TEXT_COLUMN,
						IconGrid_BUG.GRID_STACKEDBAR_COLUMN,
						IconGrid_BUG.GRID_MULTI_LIST_COLUMN,
						IconGrid_BUG.GRID_MULTI_LIST_COLUMN,
						IconGrid_BUG.GRID_MULTI_LIST_COLUMN,
						IconGrid_BUG.GRID_MULTI_LIST_COLUMN,
						IconGrid_BUG.GRID_MULTI_LIST_COLUMN)

		gridX = self.MIN_LEFT_RIGHT_SPACE + 10
		gridY = self.MIN_TOP_BOTTOM_SPACE + self.SITREP_PANEL_SPACE + self.TABLE_CONTROL_HEIGHT + self.TITLE_HEIGHT + 10
		gridWidth = self.W_SCREEN - 10 # - self.MIN_LEFT_RIGHT_SPACE * 2 - 20
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
		self.SitRepGrid.setHeader(self.Col_WHEOOH, "")
#		self.SitRepGrid.setHeader(self.Col_WEnemy, localText.getText("TXT_KEY_MILITARY_SITREP_WORSE_ENEMY", ()))
		self.SitRepGrid.setHeader(self.Col_Threat, localText.getText("TXT_KEY_MILITARY_SITREP_THREAT_INDEX", ()))
		self.SitRepGrid.setHeader(self.Col_Curr_Wars, localText.getText("TXT_KEY_MILITARY_SITREP_ACTIVE_WARS", ()))
		self.SitRepGrid.setHeader(self.Col_StratResPos, "Ours")
		self.SitRepGrid.setHeader(self.Col_StratResNeg, "Theirs")
		self.SitRepGrid.setHeader(self.Col_WillDeclareOn, localText.getText("TXT_KEY_MILITARY_SITREP_WILL_DECLARE", ()))

		if bVassals:
			self.SitRepGrid.setHeader(self.Col_Vassals, "Vassals")

		if bDefPacks:
			self.SitRepGrid.setHeader(self.Col_DefPacks, "DefPacks")

		self.SitRepGrid.createColumnGroup("", 1)
		self.SitRepGrid.createColumnGroup("", 1)
		self.SitRepGrid.createColumnGroup("", 1)
		self.SitRepGrid.createColumnGroup("Strategic Advantage", 2)

		self.SitRepGrid.setTextColWidth(self.Col_WHEOOH, 25)
		self.SitRepGrid.setStackedBarColWidth(self.Col_Threat, 120)
				
		gridWidth = self.SitRepGrid.getPrefferedWidth()
		gridHeight = self.SitRepGrid.getPrefferedHeight()
		self.SITREP_LEFT_RIGHT_SPACE = (self.W_SCREEN - gridWidth - 20) / 2
		self.SITREP_TOP_BOTTOM_SPACE = (self.H_SCREEN - gridHeight - 20) / 2
		gridX = self.SITREP_LEFT_RIGHT_SPACE + 10
		gridY = self.SITREP_TOP_BOTTOM_SPACE + 10

		self.SitRepGrid.setPosition(gridX, gridY)
		self.SitRepGrid.setSize(gridWidth, gridHeight)

		self.IconGridActive = True		


	def initPower(self):
		# active player power
		self.iPlayerPower = gc.getActivePlayer().getPower()

		# see demographics?		
		self.iDemographicsMission = -1
		for iMissionLoop in range(gc.getNumEspionageMissionInfos()):
			if (gc.getEspionageMissionInfo(iMissionLoop).isSeeDemographics()):
				self.iDemographicsMission = iMissionLoop
				break

		return






























	def Grid_ThreatIndex(self, iRow, iPlayer):

		pPlayer = gc.getPlayer(iPlayer)

		# no threat index if active player cannot see the demographics
		if not gc.getActivePlayer().canDoEspionageMission(self.iDemographicsMission, iPlayer, None, -1):
			return

		if gc.getTeam(pPlayer.getTeam()).isAVassal():
			self.SitRepGrid.addStackedBar(iRow, self.Col_Threat, -1, "", "Vassal")
			return

		# initialize threat index
		iThreat = 0

		# add attitude threat value
		iRel = self.calculateRelations(iPlayer, self.iActivePlayer)
		fRel_Threat = float(38) * float(15 - iRel) / float(30)
		if fRel_Threat < 0:
			fRel_Threat = 0.0
		elif fRel_Threat > 38:
			fRel_Threat = 38.0

		# calculate the power threat value
		fPwr_Threat = 0
		iPower = pPlayer.getPower()
		if (iPower > 0): # avoid divide by zero
			fPowerRatio = float(self.iPlayerPower) / float(iPower)
			fPwr_Threat = float(38) * float(1.5 - fPowerRatio)
			if fPwr_Threat < 0:
				fPwr_Threat = 0.0
			elif fPwr_Threat > 38:
				fPwr_Threat = 38.0


		# total threat, pre WHEOOH adjustment
		fThreat = fRel_Threat + fPwr_Threat

		# WHEOOH adjustment
		if (self.bWHEOOH
		and not self.bCurrentWar):
			fThreat = fThreat * 1.3

		# reduce the threat if the current player is in a defensive pact with the active player
		if gc.getTeam(pPlayer.getTeam()).isDefensivePact(gc.getPlayer(self.iActivePlayer).getTeam()):
			fThreat = fThreat * 0.2

#		if gc.getTeam(pLoopPlayer.getTeam()).isDefensivePact(iPlayer.getTeam()):

		
		if fThreat < 15:
			sColour = "COLOR_PLAYER_GREEN"
			sThreat = "Low"
		elif  fThreat < 35:
			sColour = "COLOR_PLAYER_BLUE"
			sThreat = "Guarded"
		elif  fThreat < 55:
			sColour = "COLOR_PLAYER_YELLOW"
			sThreat = "Elevated"
		elif  fThreat < 75:
			sColour = "COLOR_PLAYER_ORANGE"
			sThreat = "High"
		else:
			sColour = "COLOR_PLAYER_RED"
			sThreat = "Severe"

		self.SitRepGrid.addStackedBar(iRow, self.Col_Threat, fThreat, sColour, sThreat)

	def calculateRelations (self, nPlayer, nTarget):
		if (nPlayer != nTarget
		and gc.getTeam(gc.getPlayer(nPlayer).getTeam()).isHasMet(gc.getPlayer(nTarget).getTeam())):
			nAttitude = 0
			szAttitude = CyGameTextMgr().getAttitudeString(nPlayer, nTarget)
#			ExoticForPrint (("%d toward %d" % (nPlayer, nTarget)) + str(szAttitude))
			ltPlusAndMinuses = re.findall ("[-+][0-9]+", szAttitude)
#			ExoticForPrint ("Length: %d" % len (ltPlusAndMinuses))
			for i in range (len (ltPlusAndMinuses)):
				nAttitude += int (ltPlusAndMinuses[i])
#			ExoticForPrint ("Attitude: %d" % nAttitude)
		else:
			return None
		return nAttitude

	def getAttitudeText (self, nAttitude, nPlayer, nTarget):
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
			szSmilie =  unichr(ord(unichr(CyGame().getSymbolID(FontSymbols.POWER_CHAR) + 4)) + iAtt)
			szText = szSmilie + " " + szText
		
		if gc.getTeam(gc.getPlayer(nPlayer).getTeam()).isAtWar(gc.getPlayer(nTarget).getTeam()):
			szText += u" %c" % CyGame().getSymbolID(FontSymbols.OCCUPATION_CHAR)

		return szText

































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

	def GetActiveWars(self, iRow, iLeader):
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

		return iLeaderWars

	def getVassals(self, iPlayer):
		iVassals = []
		pPlayer = gc.getPlayer(iPlayer)

		for iLoopPlayer in range(gc.getMAX_PLAYERS()):
			pLoopPlayer = gc.getPlayer(iLoopPlayer)
			if (pLoopPlayer.isAlive()
			and (gc.getTeam(pLoopPlayer.getTeam()).isHasMet(gc.getPlayer(self.iActivePlayer).getTeam())
			or gc.getGame().isDebugMode())
			and not pLoopPlayer.isBarbarian()
			and not pLoopPlayer.isMinorCiv()
			and iPlayer != iLoopPlayer):
				if gc.getTeam(pLoopPlayer.getTeam()).isVassal(pPlayer.getTeam()):
					iVassals.append(iLoopPlayer)
		return iVassals

	def getDefPacks(self, iPlayer):
		iDefPacks = []
		pPlayer = gc.getPlayer(iPlayer)

		for iLoopPlayer in range(gc.getMAX_PLAYERS()):
			pLoopPlayer = gc.getPlayer(iLoopPlayer)
			if (pLoopPlayer.isAlive()
			and (gc.getTeam(pLoopPlayer.getTeam()).isHasMet(gc.getPlayer(self.iActivePlayer).getTeam())
			or gc.getGame().isDebugMode())
			and not pLoopPlayer.isBarbarian()
			and not pLoopPlayer.isMinorCiv()
			and iPlayer != iLoopPlayer):
				if gc.getTeam(pLoopPlayer.getTeam()).isDefensivePact(pPlayer.getTeam()):
					iDefPacks.append(iLoopPlayer)
		return iDefPacks





	def Grid_Strategic_Resources(self, iRow, iPlayer):
		pPlayer = gc.getPlayer(iPlayer)
		pActivePlayer = gc.getPlayer(self.iActivePlayer)

		iPlayerUnits = self.getCanTrainUnits(iPlayer)
		iActiveUnits = self.getCanTrainUnits(self.iActivePlayer)

		# remove units that the active player does not know about
		for iUnit in iPlayerUnits:
			iDiscoverTech = gc.getUnitInfo(iUnit).getPrereqAndTech()
			if not (gc.getTeam(pActivePlayer.getTeam()).isHasTech(iDiscoverTech)
			or  pActivePlayer.canResearch(iDiscoverTech, False)):
				iPlayerUnits.remove(iUnit)

		# determine units that active player can build that player cannot
		for iUnit in iActiveUnits:
			if (iUnit not in iPlayerUnits):
				szButton = gc.getUnitInfo(iUnit).getButton()
				self.SitRepGrid.addIcon(iRow, self.Col_StratResPos, szButton, WidgetTypes.WIDGET_GENERAL, -1)

		# determine units that player can build that active player cannot
		for iUnit in iPlayerUnits:
			if (iUnit not in iActiveUnits):
				szButton = gc.getUnitInfo(iUnit).getButton()
				self.SitRepGrid.addIcon(iRow, self.Col_StratResNeg, szButton, WidgetTypes.WIDGET_GENERAL, -1)






				
#				if (PlayerHasTech != ""):



#				szButton = gc.getPlayer(pHeadSelectedCity.getOwner()).getUnitButton(eLoopUnit)
#						screen.appendMultiListButton( "BottomButtonContainer", szButton, iRow, WidgetTypes.WIDGET_TRAIN, i, -1, False )
#		self.SitRepGrid.addIcon( iRow, self.Col_StratResPos
#								, gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getButton()
#								, WidgetTypes.WIDGET_LEADERHEAD, iPlayer)


#units.getDiscoveryTech()
#						elif currentPlayer.canResearch(iLoopTech, False):

		# Go through all the techs
#		for i in range(gc.getNumTechInfos()):
		
#			abChanged.append(0)
		
#			if ( gc.getTeam(gc.getPlayer(self.iCivSelected).getTeam()).isHasTech(i) ):








#		self.SitRepGrid.addIcon( iRow, self.Col_StratResPos
#								, gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getButton()
#								, WidgetTypes.WIDGET_LEADERHEAD, iPlayer)

#		self.SitRepGrid.addIcon( iRow, self.Col_StratResNeg
#								, gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getButton()
#								, WidgetTypes.WIDGET_LEADERHEAD, iPlayer)



		return


	def getCanTrainUnits(self, iPlayer):
		pPlayer = gc.getPlayer(iPlayer)
		pCity = pPlayer.getCity(0)   # capital

		iUnits = []
		for i in range (gc.getNumUnitClassInfos()):
			iUnit = gc.getCivilizationInfo(pPlayer.getCivilizationType()).getCivilizationUnits(i)
			if (gc.getUnitInfo(iUnit).getUnitCombatType() > 0 # ie, not settler, worker, missionary, etc
			and pCity.canTrain(iUnit, False, False)):
				iUnits.append(iUnit)

		return iUnits

























	

	def GetDeclareWar(self, iRow, iPlayer):
		# this module will check if the iPlayer will declare war
		# on the other leaders.  We cannot check if the iPlayer, the iActivePlayer
		# and the iTargetPlayer don't all know each other.
		# However, the code wouldn't have got this far if the iPlayer didn't know the iActivePlayer
		# so we only need to check if the iPlayer and the iActivePlayer both know the iTargetPlayer.

		# also need to check on vassal state - will do that later

		iLeaderWars = []
		szWarDenial = ""

		tradeData = TradeData()
		tradeData.ItemType = TradeableItems.TRADE_WAR

		pPlayer = gc.getPlayer(iPlayer)

		szPlayerName = gc.getPlayer(iPlayer).getName() + "/" + gc.getPlayer(iPlayer).getCivilizationShortDescription(0)

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

				tradeData.iData = iTargetPlayer
				if (pPlayer.canTradeItem(self.iActivePlayer, tradeData, False)):
					WarDenial = pPlayer.getTradeDenial(self.iActivePlayer, tradeData)
					if WarDenial == DenialTypes.NO_DENIAL:
						iLeaderWars.append(iTargetPlayer)
					elif szWarDenial == "":
						szWarDenial = gc.getDenialInfo(WarDenial).getDescription()

					if WarDenial == DenialTypes.DENIAL_TOO_MANY_WARS:
						self.bWHEOOH = True

		return iLeaderWars

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
				if (loopPlayer.canTradeItem(iActivePlayerID, tradeData, False)):
					if (loopPlayer.getTradeDenial(iActivePlayerID, tradeData) == DenialTypes.NO_DENIAL): # will trade
						currentTrades.add(iLoopPlayerID)
		return currentTrades




























	def showUnitLocation(self):

		self.deleteAllWidgets()	
		screen = self.getScreen()

		activePlayer = PyHelpers.PyPlayer(self.iActivePlayer)
		iActiveTeam = gc.getPlayer(self.iActivePlayer).getTeam()
		
		if not self.unitLocationInitDone:
			self.unitsList = [(0, 0, [], 0)] * gc.getNumUnitInfos() * 2
			self.selectedUnitList = []
			self.selectedLeaderList = [self.iActivePlayer]
			self.UL_initMinimap(screen)
			self.unitLocationInitDone = True
			self.UL_refresh(True, True)
		else:
			self.UL_refresh(False, True)

		self.drawCombatExperience()
		self.drawTabs()




	def UL_initMinimap(self, screen):
		# Minimap initialization
		iMap_W = CyMap().getGridWidth()
		iMap_H = CyMap().getGridHeight()
		self.H_MAP = (self.W_MAP * iMap_H) / iMap_W
		if (self.H_MAP > self.H_MAP_MAX):
			self.W_MAP = (self.H_MAP_MAX * iMap_W) / iMap_H
			self.H_MAP = self.H_MAP_MAX

		szPanel_ID = self.MINIMAP_PANEL
		screen.addPanel(szPanel_ID, u"", "", False, False, self.X_MAP, self.Y_MAP, self.W_MAP, self.H_MAP, PanelStyles.PANEL_STYLE_MAIN)
		screen.initMinimap(self.X_MAP + self.MAP_MARGIN, self.X_MAP + self.W_MAP - self.MAP_MARGIN, self.Y_MAP + self.MAP_MARGIN, self.Y_MAP + self.H_MAP - self.MAP_MARGIN, self.Z_CONTROLS)
		screen.updateMinimapSection(False, False)
		screen.updateMinimapColorFromMap(MinimapModeTypes.MINIMAPMODE_TERRITORY, 0.3)
		screen.setMinimapMode(MinimapModeTypes.MINIMAPMODE_MILITARY)

		self.UL_SetMinimapVisibility(screen, true)
		screen.bringMinimapToFront()

	def UL_SetMinimapVisibility(self, screen, bVisibile):
		iOldMode = CyInterface().getShowInterface()

		if bVisibile:
			CyInterface().setShowInterface(InterfaceVisibility.INTERFACE_MINIMAP_ONLY)
		else:
			CyInterface().setShowInterface(InterfaceVisibility.INTERFACE_HIDE)
			
		screen.updateMinimapVisibility()
		CyInterface().setShowInterface(iOldMode)

	def UL_refresh(self, bReload, bRedraw):
	
		if (self.iActivePlayer < 0):
			return
						
		screen = self.getScreen()
		
		if bRedraw:
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
	
				if player.isBarbarian():
					szButton = "Art/Interface/Buttons/Civilizations/Barbarian.dds"
				else:
					szButton = gc.getLeaderHeadInfo(gc.getPlayer(iLoopPlayer).getLeaderType()).getButton()
	
				szLeaderButton = self.getLeaderButtonWidget(iLoopPlayer)              #self.getNextWidgetName()
				screen.addCheckBoxGFC(szLeaderButton, szButton, ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(), x, y, iButtonSize, iButtonSize, WidgetTypes.WIDGET_MINIMAP_HIGHLIGHT, 2, iLoopPlayer, ButtonStyles.BUTTON_STYLE_LABEL)
				screen.setState(szLeaderButton, (iLoopPlayer in self.selectedLeaderList))				
		
		self.UL_refreshUnitSelection(bReload, bRedraw)

	def UL_refreshUnitSelection(self, bReload, bRedraw):
		screen = self.getScreen()
		
		screen.minimapClearAllFlashingTiles()

		if (bRedraw):
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
		
		NUM_UNIT_INFOS = gc.getNumUnitInfos()
		GG_COMBAT_TYPE = -1
		if bReload:
			for iUnit in range(NUM_UNIT_INFOS):
				iUnitCombat = gc.getUnitInfo(iUnit).getUnitCombatType()
				if (iUnitCombat <= GG_COMBAT_TYPE):
					# non-combat type: -1 -> -2 because lead-by-GG becomes -1
					iUnitCombat -= 1
				self.unitsList[iUnit] = (iUnitCombat, iUnit, [], 0)
				self.unitsList[NUM_UNIT_INFOS + iUnit] = (GG_COMBAT_TYPE, iUnit, [], 0)

			GG_PROMO = gc.getInfoTypeForString("PROMOTION_LEADER")
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

						if unitType >= 0 and unitType < NUM_UNIT_INFOS and bVisible:
							# unused
							iNumUnits = self.unitsList[unitType][3]
							if (iPlayer == self.iActivePlayer):
								iNumUnits += 1
							if loopUnit.getVisualOwner() in self.selectedLeaderList:
								self.unitsList[unitType][2].append(loopUnit)
							
							self.unitsList[unitType] = (self.unitsList[unitType][0], self.unitsList[unitType][1], self.unitsList[unitType][2], iNumUnits)
							
							if loopUnit.isHasPromotion(GG_PROMO):
								unitType += NUM_UNIT_INFOS
								iNumUnits = self.unitsList[unitType][3]
								if (iPlayer == self.iActivePlayer):
									iNumUnits += 1
								if loopUnit.getVisualOwner() in self.selectedLeaderList:
									self.unitsList[unitType][2].append(loopUnit)
								
								self.unitsList[unitType] = (self.unitsList[unitType][0], self.unitsList[unitType][1], self.unitsList[unitType][2], iNumUnits)
								
			# sort by unit combat type
			self.unitsList.sort()
		
		szText = localText.getText("TXT_KEY_PEDIA_ALL_UNITS", ()).upper()
		if (-2 in self.selectedGroupList):
			szText = localText.changeTextColor(u"<u>" + szText + u"</u>", gc.getInfoTypeForString("COLOR_YELLOW"))
		if (bRedraw):
			screen.addListBoxGFC(self.UNIT_LIST_ID, "", self.X_TEXT+self.MAP_MARGIN, self.Y_TEXT+self.MAP_MARGIN+15, self.W_TEXT-2*self.MAP_MARGIN, self.H_TEXT-2*self.MAP_MARGIN-15, TableStyles.TABLE_STYLE_STANDARD)
			screen.enableSelect(self.UNIT_LIST_ID, False)
			screen.setStyle(self.UNIT_LIST_ID, "Table_StandardCiv_Style")
			screen.appendListBoxString(self.UNIT_LIST_ID, szText, WidgetTypes.WIDGET_MINIMAP_HIGHLIGHT, 1, -2, CvUtil.FONT_LEFT_JUSTIFY)
		else:		
			screen.setListBoxStringGFC(self.UNIT_LIST_ID, 0, szText, WidgetTypes.WIDGET_MINIMAP_HIGHLIGHT, 1, -2, CvUtil.FONT_LEFT_JUSTIFY)

		iPrevUnitCombat = -2
		iItem = 1
		for iUnit in range(2 * NUM_UNIT_INFOS):
			if (len(self.unitsList[iUnit][2]) > 0):
				iUnitCombat = self.unitsList[iUnit][0]
				if (iPrevUnitCombat != iUnitCombat and iUnitCombat != -2):
					iPrevUnitCombat = iUnitCombat
					if (iUnitCombat == GG_COMBAT_TYPE):
						szDescription = localText.getText("TXT_KEY_PROMOTION_GREAT_GENERAL", ()).upper()
					elif (iUnitCombat < GG_COMBAT_TYPE):
						szDescription = gc.getUnitCombatInfo(iUnitCombat + 1).getDescription().upper()
					else:
						szDescription = gc.getUnitCombatInfo(iUnitCombat).getDescription().upper()
					if (self.UL_isSelectedGroup(iUnitCombat, False)):
						szDescription = u"   <u>" + szDescription + u"</u>"
					else:
						szDescription = u"   " + szDescription
					if (self.UL_isSelectedGroup(iUnitCombat, True)):
						szDescription = localText.changeTextColor(szDescription, gc.getInfoTypeForString("COLOR_YELLOW"))
					if (bRedraw):
						screen.appendListBoxString(self.UNIT_LIST_ID, szDescription, WidgetTypes.WIDGET_MINIMAP_HIGHLIGHT, 1, NUM_UNIT_INFOS + iUnitCombat + 2, CvUtil.FONT_LEFT_JUSTIFY)
					else:
						screen.setListBoxStringGFC(self.UNIT_LIST_ID, iItem, szDescription, WidgetTypes.WIDGET_MINIMAP_HIGHLIGHT, 1, NUM_UNIT_INFOS + iUnitCombat + 2, CvUtil.FONT_LEFT_JUSTIFY)
					iItem += 1
				
				iUnitType = self.unitsList[iUnit][1]
				szDescription = gc.getUnitInfo(iUnitType).getDescription() + u" (" + unicode(len(self.unitsList[iUnit][2])) + u")"
				iUnitTypeSelector = iUnitType
				if (iUnitCombat == GG_COMBAT_TYPE):
					iUnitTypeSelector -= NUM_UNIT_INFOS + 2
				if (self.UL_isSelectedUnitType(iUnitTypeSelector, False)):
					szDescription = u"      <u>" + szDescription + u"</u>"
				else:
					szDescription = u"      " + szDescription
				bTypeSelected = self.UL_isSelectedUnitType(iUnitTypeSelector, True)
				if (bTypeSelected):
					szDescription = localText.changeTextColor(szDescription, gc.getInfoTypeForString("COLOR_YELLOW"))
				if (bRedraw):
					screen.appendListBoxString(self.UNIT_LIST_ID, szDescription, WidgetTypes.WIDGET_MINIMAP_HIGHLIGHT, 1, iUnitTypeSelector, CvUtil.FONT_LEFT_JUSTIFY)
				else:
					screen.setListBoxStringGFC(self.UNIT_LIST_ID, iItem, szDescription, WidgetTypes.WIDGET_MINIMAP_HIGHLIGHT, 1, iUnitTypeSelector, CvUtil.FONT_LEFT_JUSTIFY)
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

						if (bTypeSelected or self.UL_isSelectedUnit(loopUnit.getOwner(), loopUnit.getID(), True)):
							szDescription = localText.changeTextColor(szDescription, gc.getInfoTypeForString("COLOR_YELLOW"))

						if (bRedraw):
							screen.appendListBoxString(self.UNIT_LIST_ID, szDescription, WidgetTypes.WIDGET_MINIMAP_HIGHLIGHT, -loopUnit.getOwner(), loopUnit.getID(), CvUtil.FONT_LEFT_JUSTIFY)
						else:
							screen.setListBoxStringGFC(self.UNIT_LIST_ID, iItem, szDescription, WidgetTypes.WIDGET_MINIMAP_HIGHLIGHT, -loopUnit.getOwner(), loopUnit.getID(), CvUtil.FONT_LEFT_JUSTIFY)
						iItem += 1

					iPlayer = loopUnit.getVisualOwner()
					player = PyPlayer(iPlayer)
					iColor = gc.getPlayerColorInfo(gc.getPlayer(iPlayer).getPlayerColor()).getColorTypePrimary()
					screen.setMinimapColor(MinimapModeTypes.MINIMAPMODE_MILITARY, loopUnit.getX(), loopUnit.getY(), iColor, 0.6)
					if ((bTypeSelected or self.UL_isSelectedUnit(loopUnit.getOwner(), loopUnit.getID(), True)) and (iPlayer in self.selectedLeaderList)):
						
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
		self.UL_refreshUnitSelection(False, False)
			
	def refreshSelectedUnit(self, iPlayer, iUnitId):
		selectedUnit = (iPlayer, iUnitId)
		if (selectedUnit in self.selectedUnitList):
			self.selectedUnitList.remove(selectedUnit)
		else:
			self.selectedUnitList.append(selectedUnit)
		self.UL_refreshUnitSelection(False, False)		

	def refreshSelectedLeader(self, iPlayer):
		if self.iShiftKeyDown == 1:
			if (iPlayer in self.selectedLeaderList):
				self.selectedLeaderList.remove(iPlayer)
			else:
				self.selectedLeaderList.append(iPlayer)
		else:
			self.selectedLeaderList = [iPlayer]	
	
		self.UL_refresh(True, True)



	def UL_isSelectedGroup(self, iGroup, bIndirect):
		if (bIndirect):
			if -2 in self.selectedGroupList:
				return True
			if iGroup == -2:
				return False
		return ((iGroup + gc.getNumUnitInfos() + 2) in self.selectedGroupList)
				
	def UL_isSelectedUnitType(self, iUnit, bIndirect):
		if (bIndirect):
			if -2 in self.selectedGroupList:
				return True
			iActualUnit = iUnit
			if iActualUnit < -2:
				iActualUnit += gc.getNumUnitInfos() + 2
			unitInfo = gc.getUnitInfo(iActualUnit)
			iCombatType = unitInfo.getUnitCombatType()
			if iCombatType == -1:
				iCombatType = -2
			if self.UL_isSelectedGroup(iCombatType, True):
				return True
			if iUnit < -2:
				if iActualUnit in self.selectedGroupList or self.UL_isSelectedGroup(-1, True):
					return True
		return (iUnit in self.selectedGroupList)
		
	def UL_isSelectedUnit(self, iPlayer, iUnitId, bIndirect):
		if (bIndirect):
			if -2 in self.selectedGroupList:
				return True
			unit = gc.getPlayer(iPlayer).getUnit(iUnitId)
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
				self.showUnitLocation()

			elif (inputClass.getFunctionName() == self.SIT_REP_TAB_ID):
				self.iScreen = SITUATION_REPORT_SCREEN
				self.showSituationReport()

#			elif (inputClass.getFunctionName() == self.PLACE_HOLDER_TAB):
#				self.iScreen = PLACE_HOLDER
#				self.showGameSettingsScreen()

			elif (inputClass.getFunctionName() == self.UNIT_BUTTON_ID):
				self.bUnitDetails = not self.bUnitDetails
				self.UL_refreshUnitSelection(True, True)

			elif (inputClass.getButtonType() == WidgetTypes.WIDGET_GENERAL):
				if (inputClass.getData1() == self.SCROLL_TABLE_UP):
					self.scrollGrid_Up()
				elif (inputClass.getData1() == self.SCROLL_TABLE_DOWN):
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
