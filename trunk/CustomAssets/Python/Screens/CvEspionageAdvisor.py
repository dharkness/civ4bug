## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
## Improvements to this screen by Almightix - thanks
from CvPythonExtensions import *
from PyHelpers import PyPlayer
import CvUtil
import ScreenInput
import CvScreenEnums

# BUG - Better Espionage - start
import ColorUtil
import BugUtil
import FontUtil
import BugCore
EspionageOpt = BugCore.game.BetterEspionage
# BUG - Better Espionage - end

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

ESPIONAGE_MISSION_TAB = 0
ESPIONAGE_GLANCE_TAB = 1

CITYMISSION_CITY = 0
CITYMISSION_MISSION = 1

import SdToolKit
sdEcho			= SdToolKit.sdEcho
sdModInit		= SdToolKit.sdModInit
sdModLoad		= SdToolKit.sdModLoad
sdModSave		= SdToolKit.sdModSave
sdEntityInit	= SdToolKit.sdEntityInit
sdEntityExists	= SdToolKit.sdEntityExists
sdEntityWipe	= SdToolKit.sdEntityWipe
sdGetVal		= SdToolKit.sdGetVal
sdSetVal		= SdToolKit.sdSetVal
sdGroup			= "EspionagePoints"

class CvEspionageAdvisor:

	def __init__(self):
		self.SCREEN_NAME = "EspionageAdvisor"
		self.DEBUG_DROPDOWN_ID =  "EspionageAdvisorDropdownWidget"
		self.WIDGET_ID = "EspionageAdvisorWidget"
		self.WIDGET_HEADER = "EspionageAdvisorWidgetHeader"
		self.EXIT_ID = "EspionageAdvisorExitWidget"
		self.BACKGROUND_ID = "EspionageAdvisorBackground"
		self.X_SCREEN = 500
		self.Y_SCREEN = 396
		self.W_SCREEN = 1024
		self.H_SCREEN = 768
		self.Y_TITLE = 12
		self.BORDER_WIDTH = 4
		self.PANE_HEIGHT = 450
		self.PANE_WIDTH = 283
		self.X_SLIDERS = 50
		self.X_INCOME = 373
		self.X_EXPENSES = 696
		self.Y_TREASURY = 90
		self.H_TREASURY = 100
		self.Y_LOCATION = 230
		self.Y_SPACING = 30
		self.TEXT_MARGIN = 15
		self.Z_BACKGROUND = -2.1
		self.Z_CONTROLS = self.Z_BACKGROUND - 0.2
		self.DZ = -0.2

		self.X_EXIT = 994
		self.Y_EXIT = 726

		self.nWidgetCount = 0

		self.iDirtyBit = 0

		self.iTargetPlayer = -1

		self.iActiveCityID = -1
		self.iActiveMissionID = -1

		self.iActiveTab = ESPIONAGE_MISSION_TAB
		self.drawMissionTabConstantsDone = 0
		self.CityMissionToggle = CITYMISSION_CITY

	def getScreen(self):
		return CyGInterfaceScreen(self.SCREEN_NAME, CvScreenEnums.ESPIONAGE_ADVISOR)

	def interfaceScreen (self):

		self.iTargetPlayer = -1
		self.iActiveCityID = -1
		self.iActiveMissionID = -1
		self.iActivePlayer = CyGame().getActivePlayer()
		
		screen = self.getScreen()
		if screen.isActive():
			return
		screen.setRenderInterfaceOnly(True);
		screen.showScreen( PopupStates.POPUPSTATE_IMMEDIATE, False)

		if (self.iActiveTab < 0
		or  self.iActiveTab > 1):
			self.iActiveTab = ESPIONAGE_MISSION_TAB

		# Set the background and exit button, and show the screen
		screen.setDimensions(screen.centerX(0), screen.centerY(0), self.W_SCREEN, self.H_SCREEN)

		screen.addDDSGFC(self.BACKGROUND_ID, ArtFileMgr.getInterfaceArtInfo("SCREEN_BG_OPAQUE").getPath(), 0, 0, self.W_SCREEN, self.H_SCREEN, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addPanel( "TechTopPanel", u"", u"", True, False, 0, 0, self.W_SCREEN, 55, PanelStyles.PANEL_STYLE_TOPBAR )
		screen.addPanel( "TechBottomPanel", u"", u"", True, False, 0, 713, self.W_SCREEN, 55, PanelStyles.PANEL_STYLE_BOTTOMBAR )

		screen.showWindowBackground(False)
		screen.setText(self.EXIT_ID, "Background", u"<font=4>" + localText.getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, self.X_EXIT, self.Y_EXIT, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1 )

		# Header...
		screen.setLabel(self.WIDGET_HEADER, "Background", u"<font=4b>" + localText.getText("TXT_KEY_ESPIONAGE_SCREEN", ()).upper() + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_SCREEN, self.Y_TITLE, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		if (CyGame().isDebugMode()):
			self.iDebugDropdownID = 554
			self.szDropdownName = self.DEBUG_DROPDOWN_ID
			screen.addDropDownBoxGFC(self.szDropdownName, 22, 12, 300, WidgetTypes.WIDGET_GENERAL, self.iDebugDropdownID, -1, FontTypes.GAME_FONT)
			for j in range(gc.getMAX_PLAYERS()):
				if (gc.getPlayer(j).isAlive()):
					screen.addPullDownString(self.szDropdownName, gc.getPlayer(j).getName(), j, j, False )

		# draw the contents
		self.drawContents()

	def drawContents(self):

		self.deleteAllWidgets()

		BugUtil.debug("CvEspionage Advisor: Active Tab %i", self.iActiveTab)

		if not EspionageOpt.isEnabled():
			self.CityMissionToggle = CITYMISSION_CITY
			self.iActiveTab = ESPIONAGE_MISSION_TAB

		# draw tab details
		if self.iActiveTab == ESPIONAGE_MISSION_TAB:
			self.drawMissionTab()
			self.refreshMissionTab()
		elif self.iActiveTab == ESPIONAGE_GLANCE_TAB:
			self.drawGlanceTab()

	def drawMissionTab(self):

		screen = self.getScreen()

		BugUtil.debug("CvEspionage Advisor: drawMissionsTab")

		pActivePlayer = gc.getPlayer(self.iActivePlayer)
		pActiveTeam = gc.getTeam(pActivePlayer.getTeam())

		self.drawMissionTabConstants()

		self.szLeftPaneWidget = "LeftPane"
		screen.addPanel( self.szLeftPaneWidget, "", "", true, true,
			self.X_LEFT_PANE, self.Y_LEFT_PANE, self.W_LEFT_PANE, self.H_LEFT_PANE, PanelStyles.PANEL_STYLE_MAIN )

		self.szScrollPanel = "ScrollPanel"
		screen.addPanel( self.szScrollPanel, "", "", true, true,
			self.X_SCROLL, self.Y_SCROLL, self.W_SCROLL, self.H_SCROLL, PanelStyles.PANEL_STYLE_EMPTY)
		
		self.aiKnownPlayers = []
		self.aiUnknownPlayers = []
		self.iNumEntries= 0

		for iLoop in range(gc.getMAX_PLAYERS()):
			pPlayer = gc.getPlayer(iLoop)
			if (pPlayer.getTeam() != pActivePlayer.getTeam() and not pPlayer.isBarbarian()):
				if (pPlayer.isAlive()):
					if (pActiveTeam.isHasMet(pPlayer.getTeam())):
						self.aiKnownPlayers.append(iLoop)
						self.iNumEntries = self.iNumEntries + 1

						if (self.iTargetPlayer == -1):
							self.iTargetPlayer = iLoop

		while(self.iNumEntries < 17):
			self.iNumEntries = self.iNumEntries + 1
			self.aiUnknownPlayers.append(self.iNumEntries)

		############################
		#### Total EPs Per Turn Text
		############################

		if not EspionageOpt.isEnabled():
			self.szTotalPaneWidget = "TotalPane"
			screen.addPanel( self.szTotalPaneWidget, "", "", true, true,
				self.X_TOTAL_PANE, self.Y_TOTAL_PANE, self.W_TOTAL_PANE, self.H_TOTAL_PANE, PanelStyles.PANEL_STYLE_MAIN )

			self.szMakingText = "MakingText"
			szText = u"<font=4>" + localText.getText("TXT_KEY_ESPIONAGE_SCREEN_TOTAL_NUM_EPS", (pActivePlayer.getCommerceRate(CommerceTypes.COMMERCE_ESPIONAGE), )) + "</font>"
			screen.setLabel(self.szMakingText, "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, self.X_MAKING_TEXT, self.Y_MAKING_TEXT, self.Z_CONTROLS, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )

		############################
		#### Right Panel
		############################

		self.szRightPaneWidget = "RightPane"
		screen.addPanel( self.szRightPaneWidget, "", "", true, true,
			self.X_RIGHT_PANE, self.Y_RIGHT_PANE, self.W_RIGHT_PANE, self.H_RIGHT_PANE, PanelStyles.PANEL_STYLE_MAIN )

		if (self.iTargetPlayer != -1):
			self.szCitiesTitleText = "CitiesTitle"
			if self.CityMissionToggle == CITYMISSION_CITY:
				szText = u"<font=4>" + localText.getText("TXT_KEY_CONCEPT_CITIES", ()) + "</font>"
			else:
				szText = u"<font=4>" + localText.getText("TXT_KEY_ESPIONAGE_SCREEN_MISSIONS", ()) + "</font>"

			if EspionageOpt.isEnabled():
				szText = localText.changeTextColor(szText, gc.getInfoTypeForString("COLOR_YELLOW"))
				screen.setText(self.szCitiesTitleText, "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, self.X_CITY_LIST, self.Y_CITY_LIST - 40, self.Z_CONTROLS, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			else:
				screen.setLabel(self.szCitiesTitleText, "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, self.X_CITY_LIST, self.Y_CITY_LIST - 40, self.Z_CONTROLS, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )

			self.szEffectsTitleText = "EffectsTitle"
			szText = u"<font=4>" + localText.getText("TXT_KEY_ESPIONAGE_SCREEN_PASSIVE_EFFECTS", ()) + "</font>"
			screen.setLabel(self.szEffectsTitleText, "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, self.X_EFFECTS_LIST, self.Y_EFFECTS_LIST - 40, self.Z_CONTROLS, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )

			self.szMissionsTitleText = "MissionsTitle"
			if self.CityMissionToggle == CITYMISSION_MISSION:
				szText = u"<font=4>" + localText.getText("TXT_KEY_CONCEPT_CITIES", ()) + "</font>"
			else:
				szText = u"<font=4>" + localText.getText("TXT_KEY_ESPIONAGE_SCREEN_MISSIONS", ()) + "</font>"

			if EspionageOpt.isEnabled():
				szText = localText.changeTextColor(szText, gc.getInfoTypeForString("COLOR_YELLOW"))
				screen.setText(self.szMissionsTitleText, "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, self.X_MISSIONS_LIST, self.Y_MISSIONS_LIST - 40, self.Z_CONTROLS, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			else:
				screen.setLabel(self.szMissionsTitleText, "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, self.X_MISSIONS_LIST, self.Y_MISSIONS_LIST - 40, self.Z_CONTROLS, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )

			self.szEffectsCostTitleText = "EffectsCostTitle"
			szText = u"<font=4>" + localText.getText("TXT_KEY_ESPIONAGE_SCREEN_COST", ()) + "</font>"
			screen.setLabel(self.szEffectsCostTitleText, "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, self.X_EFFECTS_COSTS_LIST, self.Y_EFFECTS_COSTS_LIST - 40, self.Z_CONTROLS, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )

			self.szMissionsCostTitleText = "MissionsCostTitle"
			szText = u"<font=4>" + localText.getText("TXT_KEY_ESPIONAGE_SCREEN_COST", ()) + "</font>"
			screen.setLabel(self.szMissionsCostTitleText, "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, self.X_MISSIONS_COSTS_LIST, self.Y_MISSIONS_COSTS_LIST - 40, self.Z_CONTROLS, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )


			############################
			#### Left Leaders Panel
			############################

			# the left leader panel contains the following elements:

			# created / updated during drawMissionTab()
			#self.aszLeaderImages      - leader image / icon (selectable)
			#self.aszLeaderNamePanels  - leader panel
			#self.aszNameTexts         - leader name
			#self.aszPointsTexts       - current EPs player has against leader
			#self.aszIncreaseButtons   - weight increase button
			#self.aszDecreaseButtons   - weight decrease button

			# created / updated during refreshMissionTab()
			#self.aszSpendingTexts     - current weight player has assigned against leader
			#self.aszAmountTexts       - EPs per turn
			#self.aszEspionageIcons    - EP icon

			if EspionageOpt.isEnabled():
				self.drawMissionTab_LeftLeaderPanal_BUG(screen)
			else:
				self.drawMissionTab_LeftLeaderPanal(screen)



		return

	def drawMissionTabConstants(self):

		if EspionageOpt.isEnabled():
			if  self.drawMissionTabConstantsDone == 2:
				return
		else:
			if  self.drawMissionTabConstantsDone == 1:
				return

		if EspionageOpt.isEnabled():
			self.drawMissionTabConstantsDone = 2
		else:
			self.drawMissionTabConstantsDone = 1

		if EspionageOpt.isEnabled():
			for iMissionLoop in range(gc.getNumEspionageMissionInfos()):
				pMission = gc.getEspionageMissionInfo(iMissionLoop)
				if (pMission.getCost() != -1
				and pMission.isPassive()):
					if pMission.isInvestigateCity():
						self.MissionInvestigateCity = iMissionLoop
					elif pMission.isSeeDemographics():
						self.MissionSeeDemo = iMissionLoop
					elif pMission.isSeeResearch():
						self.MissionSeeResearch = iMissionLoop
					else:
						self.MissionCityVisibility = iMissionLoop

			self.X_LEFT_PANE = 25
			self.Y_LEFT_PANE = 70 - 5
			self.W_LEFT_PANE = 400 + 60
			self.H_LEFT_PANE = 620

			self.X_SCROLL = self.X_LEFT_PANE + 20
			self.Y_SCROLL= 90 - 5
			self.W_SCROLL= 360 + 60
			self.H_SCROLL= 580

			############################
			#### Right Panel
			############################

			self.X_RIGHT_PANE = self.X_LEFT_PANE + self.W_LEFT_PANE + 10
			self.Y_RIGHT_PANE = self.Y_LEFT_PANE
			self.W_RIGHT_PANE = 550 - 50
			self.H_RIGHT_PANE = self.H_LEFT_PANE

			self.X_CITY_LIST = self.X_RIGHT_PANE + 20
			self.Y_CITY_LIST = self.Y_RIGHT_PANE + 60
			self.W_CITY_LIST = 160
			self.H_CITY_LIST = self.H_RIGHT_PANE - 90

			self.X_EFFECTS_LIST = self.X_CITY_LIST + self.W_CITY_LIST + 10
			self.Y_EFFECTS_LIST = self.Y_CITY_LIST
			self.W_EFFECTS_LIST = 210
			self.H_EFFECTS_LIST = 100

			self.X_EFFECTS_COSTS_LIST = self.X_EFFECTS_LIST + self.W_EFFECTS_LIST + 10
			self.Y_EFFECTS_COSTS_LIST = self.Y_EFFECTS_LIST
			self.W_EFFECTS_COSTS_LIST = 60
			self.H_EFFECTS_COSTS_LIST = self.H_EFFECTS_LIST

			self.X_MISSIONS_LIST = self.X_CITY_LIST + self.W_CITY_LIST + 10
			self.Y_MISSIONS_LIST = self.Y_EFFECTS_LIST + self.H_EFFECTS_LIST + 50
			self.W_MISSIONS_LIST = self.W_EFFECTS_LIST
			self.H_MISSIONS_LIST = self.H_CITY_LIST -  + self.H_EFFECTS_LIST - 50

			self.X_MISSIONS_COSTS_LIST = self.X_MISSIONS_LIST + self.W_MISSIONS_LIST + 10
			self.Y_MISSIONS_COSTS_LIST = self.Y_MISSIONS_LIST
			self.W_MISSIONS_COSTS_LIST = self.W_EFFECTS_COSTS_LIST
			self.H_MISSIONS_COSTS_LIST = self.H_MISSIONS_LIST

#ruff_hi - needed for when I add the second tab
#CyInterface().determineWidth(szText)

			############################
			#### Left Leaders Panel
			############################

			self.LeaderPanelTopRow = 0
			self.LeaderPanelBottomRow = 15
			self.LeaderPanelMiddle = 6
			self.LeaderPanel_X_LeaderIcon = 21
			self.LeaderPanel_X_LeaderNamePanel = 5
			self.LeaderPanel_X_LeaderName = 55
			self.LeaderPanel_X_Multiplier = 190
			self.LeaderPanel_X_CounterEP = 220
			self.LeaderPanel_X_EPoints = 300
			self.LeaderPanel_X_PassiveMissions = 380
			self.LeaderPanel_X_WghtInc = 53
			self.LeaderPanel_X_WghtDec = 68
			self.LeaderPanel_X_Wght = 85
			self.LeaderPanel_X_EPointsTurn = self.LeaderPanel_X_EPoints + 4
			self.LeaderPanel_X_EspionageIcon = 3

			self.W_LEADER = 128
			self.H_LEADER = 128

			self.W_NAME_PANEL = 220
			self.H_NAME_PANEL = 30

		else:
			self.X_LEFT_PANE = 25
			self.Y_LEFT_PANE = 70
			self.W_LEFT_PANE = 400
			self.H_LEFT_PANE = 620

			self.X_SCROLL = self.X_LEFT_PANE + 20
			self.Y_SCROLL= 90
			self.W_SCROLL= 360
			self.H_SCROLL= 580

			############################
			#### Total EPs Per Turn Text
			############################

			self.X_TOTAL_PANE = self.X_LEFT_PANE + self.W_LEFT_PANE + 20
			self.Y_TOTAL_PANE = self.Y_LEFT_PANE
			self.W_TOTAL_PANE = 550
			self.H_TOTAL_PANE = 60

			self.X_MAKING_TEXT = 490
			self.Y_MAKING_TEXT = 85

			############################
			#### Right Panel
			############################

			self.X_RIGHT_PANE = self.X_TOTAL_PANE
			self.Y_RIGHT_PANE = self.Y_TOTAL_PANE + self.H_TOTAL_PANE + 20
			self.W_RIGHT_PANE = self.W_TOTAL_PANE
			self.H_RIGHT_PANE = self.H_LEFT_PANE - self.H_TOTAL_PANE - 20

			self.X_CITY_LIST = self.X_RIGHT_PANE + 40
			self.Y_CITY_LIST = self.Y_RIGHT_PANE + 60
			self.W_CITY_LIST = 160
			self.H_CITY_LIST = self.H_RIGHT_PANE - 90

			self.X_EFFECTS_LIST = self.X_CITY_LIST + self.W_CITY_LIST + 20
			self.Y_EFFECTS_LIST = self.Y_CITY_LIST
			self.W_EFFECTS_LIST = 210
			self.H_EFFECTS_LIST = (self.H_CITY_LIST / 3) - 50

			self.X_EFFECTS_COSTS_LIST = self.X_EFFECTS_LIST + self.W_EFFECTS_LIST + 10
			self.Y_EFFECTS_COSTS_LIST = self.Y_EFFECTS_LIST
			self.W_EFFECTS_COSTS_LIST = 60
			self.H_EFFECTS_COSTS_LIST = self.H_EFFECTS_LIST

			self.X_MISSIONS_LIST = self.X_CITY_LIST + self.W_CITY_LIST + 20
			self.Y_MISSIONS_LIST = self.Y_EFFECTS_LIST + self.H_EFFECTS_LIST + 50
			self.W_MISSIONS_LIST = self.W_EFFECTS_LIST
			self.H_MISSIONS_LIST = (self.H_CITY_LIST * 2 / 3) #- 45

			self.X_MISSIONS_COSTS_LIST = self.X_MISSIONS_LIST + self.W_MISSIONS_LIST + 10
			self.Y_MISSIONS_COSTS_LIST = self.Y_MISSIONS_LIST
			self.W_MISSIONS_COSTS_LIST = self.W_EFFECTS_COSTS_LIST
			self.H_MISSIONS_COSTS_LIST = self.H_MISSIONS_LIST

			############################
			#### Left Leaders Panel
			############################

			self.W_LEADER = 128
			self.H_LEADER = 128

			self.W_NAME_PANEL = 220
			self.H_NAME_PANEL = 30


		return



	def drawMissionTab_LeftLeaderPanal(self, screen):
		pActivePlayer = gc.getPlayer(self.iActivePlayer)
		pActiveTeam = gc.getTeam(pActivePlayer.getTeam())

		self.aszLeaderImages = []
		self.aszLeaderNamePanels = []
		self.aszNameTexts = []
		self.aszPointsTexts = []
		self.aszSpendingTexts = []
		self.aszRelativeTexts = []
		self.aszIncreaseButtons = []
		self.aszDecreaseButtons = []
		self.aszAmountTexts = []
		self.aszEspionageIcons = []

		for iPlayerID in self.aiKnownPlayers:
			pTargetPlayer = gc.getPlayer(iPlayerID)
			iTargetTeam = pTargetPlayer.getTeam()

			iX = 0
			iY = 14

			attach = "LeaderContainer%d" % (iPlayerID)

			screen.attachPanel(self.szScrollPanel, attach, "", "", True, False, PanelStyles.PANEL_STYLE_STANDARD)

			szName = "LeaderImageA%d" %(iPlayerID)
			screen.attachSeparator(attach, szName, true, 30)

			self.iLeaderImagesID = 456
			szName = "LeaderImage%d" %(iPlayerID)
			self.aszLeaderImages.append(szName)

			screen.addCheckBoxGFCAt(attach, szName, gc.getLeaderHeadInfo(gc.getPlayer(iPlayerID).getLeaderType()).getButton(), ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),
				iX +21 , iY - 14, 32, 32, WidgetTypes.WIDGET_GENERAL, self.iLeaderImagesID, iPlayerID, ButtonStyles.BUTTON_STYLE_LABEL, False)
			if (self.iTargetPlayer == iPlayerID):
				screen.setState(szName, true)
			
			szName = "LeaderNamePanel%d" %(iPlayerID)
			self.aszLeaderNamePanels.append(szName)
			screen.attachPanelAt( attach, szName, "", "", true, false, PanelStyles.PANEL_STYLE_MAIN,
				iX + 5, iY-15, self.W_NAME_PANEL, self.H_NAME_PANEL, WidgetTypes.WIDGET_GENERAL, -1, -1 )

			szName = "NameText%d" %(iPlayerID)
			self.aszNameTexts.append(szName)

			szMultiplier = self.getEspionageMultiplierText(self.iActivePlayer, iPlayerID)
			szTempBuffer = u"<color=%d,%d,%d,%d>%s (%s)</color>" %(pTargetPlayer.getPlayerTextColorR(), pTargetPlayer.getPlayerTextColorG(), pTargetPlayer.getPlayerTextColorB(), pTargetPlayer.getPlayerTextColorA(), pTargetPlayer.getName(), szMultiplier)
			szText = u"<font=2>" + szTempBuffer + "</font>"
			screen.setLabelAt( szName, attach, szText, 0, iX + 55, iY -15, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 );

			szName = "PointsText%d" %(iPlayerID)
			self.aszPointsTexts.append(szName)
			szText = u"<font=2>" + localText.getText("TXT_KEY_ESPIONAGE_NUM_EPS", (self.getPlayerEPs(self.iActivePlayer, iPlayerID), )) + "</font>"
			screen.setLabelAt( szName, attach, szText, 0, 247, iY - 14, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 );

			szName = "SpendingText%d" %(iPlayerID)
			self.aszSpendingTexts.append(szName)
			szText = u"<font=2>%s: %d</font>" %(localText.getText("TXT_KEY_ESPIONAGE_SCREEN_SPENDING_WEIGHT", ()), pActivePlayer.getEspionageSpendingWeightAgainstTeam(iTargetTeam))
			screen.setLabelAt( szName, attach, szText, 0, 85, iY - 1, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 );

			szName = "AmountText%d" %(iPlayerID)
			self.aszAmountTexts.append(szName)
			if (pActivePlayer.getEspionageSpending(iTargetTeam) > 0):
				szText = u"<font=2><color=0,255,0,0>%s</color></font>" %(localText.getText("TXT_KEY_ESPIONAGE_NUM_EPS_PER_TURN", (pActivePlayer.getEspionageSpending(iTargetTeam), )))
			else:
				szText = u"<font=2><color=192,0,0,0>%s</color></font>" %(localText.getText("TXT_KEY_ESPIONAGE_NUM_EPS_PER_TURN", (pActivePlayer.getEspionageSpending(iTargetTeam), )))

			screen.setLabelAt( szName, attach, szText, CvUtil.FONT_RIGHT_JUSTIFY, 330, iY, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 );

			szName = "SpendingIcon%d" %(iPlayerID)
			self.aszEspionageIcons.append(szName)
			if (pActivePlayer.getEspionageSpendingWeightAgainstTeam(iTargetTeam) > 0):
				szText = u"<font=2>%c</font>" %(gc.getCommerceInfo(CommerceTypes.COMMERCE_ESPIONAGE).getChar())
			else:
				szText = u""

			screen.setLabelAt( szName, attach, szText, 0, 3, iY - 9, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 );

			iSize = 16
			self.iIncreaseButtonID = 555
			szName = "IncreaseButton%d" %(iPlayerID)
			self.aszIncreaseButtons.append(szName)
			screen.setImageButtonAt( szName, attach, ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_PLUS").getPath(), 53, iY + 1, iSize, iSize, WidgetTypes.WIDGET_GENERAL, self.iIncreaseButtonID, iPlayerID );
			self.iDecreaseButtonID = 556
			szName = "DecreaseButton%d" %(iPlayerID)
			self.aszDecreaseButtons.append(szName)
			screen.setImageButtonAt( szName, attach, ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_MINUS").getPath(), 68, iY + 1, iSize, iSize, WidgetTypes.WIDGET_GENERAL, self.iDecreaseButtonID, iPlayerID );

		for iPlayerID in self.aiUnknownPlayers:
			attach = "EmptyLeaderContainer%d" % (iPlayerID)
			screen.attachPanel(self.szScrollPanel, attach, "", "", True, False, PanelStyles.PANEL_STYLE_STANDARD)
			screen.attachSeparator(attach, "EmptyLeaderImageA%d" %(iPlayerID), true, 30)

	def drawMissionTab_LeftLeaderPanal_BUG(self, screen):
		# created / updated during drawMissionTab()
		#self.aszLeaderImages      - leader image / icon (selectable)
		#self.aszLeaderNamePanels  - leader panel
		#self.aszNameTexts         - leader name
		#self.aszPointsTexts       - current EPs player has against leader
		#self.aszIncreaseButtons   - weight increase button
		#self.aszDecreaseButtons   - weight decrease button

		# created / updated during refreshMissionTab()
		#self.aszSpendingTexts     - current weight player has assigned against leader
		#self.aszAmountTexts       - EPs per turn
		#self.aszEspionageIcons    - EP icon

		pActivePlayer = gc.getPlayer(self.iActivePlayer)
		pActiveTeam = gc.getTeam(pActivePlayer.getTeam())

		self.aszLeaderImages = []
		self.aszLeaderNamePanels = []
		self.aszNameTexts = []
		self.aszPointsTexts = []
		self.aszSpendingTexts = []
		self.aszIncreaseButtons = []
		self.aszDecreaseButtons = []
		self.aszAmountTexts = []
		self.aszEspionageIcons = []

		iRatioColor = EspionageOpt.getDefaultRatioColor()
		iGoodRatioColor = EspionageOpt.getGoodRatioColor()
		iBadRatioColor = EspionageOpt.getBadRatioColor()

		for iPlayerID in self.aiKnownPlayers:
			pTargetPlayer = gc.getPlayer(iPlayerID)
			iTargetTeam = pTargetPlayer.getTeam()

			# leader panel / container
			attach = "LeaderContainer%d" % (iPlayerID)
			screen.attachPanel(self.szScrollPanel, attach, "", "", True, False, PanelStyles.PANEL_STYLE_STANDARD)

			# leader immage
			szName = "LeaderImageA%d" %(iPlayerID)
			screen.attachSeparator(attach, szName, true, 30)

			self.iLeaderImagesID = 456
			szName = "LeaderImage%d" %(iPlayerID)
			self.aszLeaderImages.append(szName)

			screen.addCheckBoxGFCAt(attach, szName, gc.getLeaderHeadInfo(gc.getPlayer(iPlayerID).getLeaderType()).getButton(), ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),
				self.LeaderPanel_X_LeaderIcon, self.LeaderPanelTopRow, 32, 32, WidgetTypes.WIDGET_GENERAL, self.iLeaderImagesID, iPlayerID, ButtonStyles.BUTTON_STYLE_LABEL, False)
			if (self.iTargetPlayer == iPlayerID):
				screen.setState(szName, true)

			# leader name
			szName = "LeaderNamePanel%d" %(iPlayerID)
			self.aszLeaderNamePanels.append(szName)
			screen.attachPanelAt( attach, szName, "", "", true, false, PanelStyles.PANEL_STYLE_MAIN,
				self.LeaderPanel_X_LeaderNamePanel, self.LeaderPanelTopRow, self.W_NAME_PANEL, self.H_NAME_PANEL, WidgetTypes.WIDGET_GENERAL, -1, -1 )

			szName = "NameText%d" %(iPlayerID)
			self.aszNameTexts.append(szName)

			szTempBuffer = u"<color=%d,%d,%d,%d>%s</color>" %(pTargetPlayer.getPlayerTextColorR(), pTargetPlayer.getPlayerTextColorG(), pTargetPlayer.getPlayerTextColorB(), pTargetPlayer.getPlayerTextColorA(), pTargetPlayer.getName())
			szText = u"<font=2>" + szTempBuffer + "</font>"
			screen.setLabelAt( szName, attach, szText, 0, self.LeaderPanel_X_LeaderName, self.LeaderPanelTopRow, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 );

			# EPoints Multiplier
			iMultiplier = self.getEspionageMultiplier(self.iActivePlayer, iPlayerID)
			szName = "MultiplerText%d" %(iPlayerID)
			szText = u"<font=2>%i%s</font>" %(iMultiplier, "%")

			if (iBadRatioColor >= 0 and iMultiplier >= EspionageOpt.getBadRatioCutoff()):
				szText = localText.changeTextColor(szText, iBadRatioColor)
			elif (iGoodRatioColor >= 0 and iMultiplier <= EspionageOpt.getGoodRatioCutoff()):
				szText = localText.changeTextColor(szText, iGoodRatioColor)
			elif (iRatioColor >= 0):
				szText = localText.changeTextColor(szText, iRatioColor)

			screen.setLabelAt( szName, attach, szText, CvUtil.FONT_RIGHT_JUSTIFY, self.LeaderPanel_X_Multiplier, self.LeaderPanelTopRow, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 );

			# EPoints Multiplier Against
			if EspionageOpt.isShowCalculatedInformation():
				iMultiplier = self.getEspionageMultiplier(iPlayerID, self.iActivePlayer)
				szName = "MultiplerAgainstText%d" %(iPlayerID)
				szText = u"<font=2>%i%s</font>" %(iMultiplier, "%")
				screen.setLabelAt( szName, attach, szText, CvUtil.FONT_RIGHT_JUSTIFY, self.LeaderPanel_X_Multiplier, self.LeaderPanelBottomRow, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 );

			# Counter Espionage
			iCounterEsp = self.getCounterEspionageTurnsLeft(self.iActivePlayer, iPlayerID)
			szName = "CounterEspionageText%d" %(iPlayerID)
			if iCounterEsp > 0:
				szText = u"<font=2>[%i]</font>" %(iCounterEsp)
			else:
				szText = u""
			screen.setLabelAt( szName, attach, szText, CvUtil.FONT_RIGHT_JUSTIFY, self.LeaderPanel_X_CounterEP, self.LeaderPanelTopRow, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 );

			# Counter Espionage Against
			iCounterEsp = self.getCounterEspionageTurnsLeft(iPlayerID, self.iActivePlayer)
			szName = "CounterEspionageAgainstText%d" %(iPlayerID)
			if iCounterEsp > 0:
				szText = u"<font=2>[%i]</font>" %(iCounterEsp)
			else:
				szText = u""
			screen.setLabelAt( szName, attach, szText, CvUtil.FONT_RIGHT_JUSTIFY, self.LeaderPanel_X_CounterEP, self.LeaderPanelBottomRow, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 );

			# EPs
			szName = "PointsText%d" %(iPlayerID)
			self.aszPointsTexts.append(szName)
			iPlayerEPs = self.getPlayerEPs(self.iActivePlayer, iPlayerID)
			szText = u"<font=2>" + localText.getText("TXT_KEY_ESPIONAGE_NUM_EPS", (iPlayerEPs ,)) + "</font>"
			screen.setLabelAt( szName, attach, szText, CvUtil.FONT_RIGHT_JUSTIFY, self.LeaderPanel_X_EPoints, self.LeaderPanelTopRow, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 );

			# EPs Against
			szName = "PointsAgainstText%d" %(iPlayerID)
			iTargetEPs = self.getPlayerEPs(iPlayerID, self.iActivePlayer)
			szText = u"<font=2>" + localText.getText("TXT_KEY_ESPIONAGE_NUM_EPS", (iTargetEPs, )) + "</font>"
			screen.setLabelAt( szName, attach, szText, CvUtil.FONT_RIGHT_JUSTIFY, self.LeaderPanel_X_EPoints, self.LeaderPanelBottomRow, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 );

			# EP Spending Against (Points per turn)
			szName = "AmountAgainstText%d" %(iPlayerID)
			zsSDKey = "%i-%i" %(iPlayerID, self.iActivePlayer)
			if (sdEntityExists(sdGroup, zsSDKey) == False): #create record if it doesn't exist
				zDic = {'Prior':0}
				sdEntityInit(sdGroup, zsSDKey, zDic)

			iPrior = sdGetVal(sdGroup, zsSDKey, "Prior")
			iSpending = iTargetEPs - iPrior
			if (iPrior > 0
			and iSpending > 0):
				szText = u"<font=2><color=0,255,0,0>(+%i)</color></font>" %(iSpending)
			else:
				szText = u""
			screen.deleteWidget(szName)
			screen.setLabelAt( szName, attach, szText, CvUtil.FONT_LEFT_JUSTIFY, self.LeaderPanel_X_EPointsTurn, self.LeaderPanelBottomRow, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 );

			# EP Weights
			iSize = 16
			self.iIncreaseButtonID = 555
			szName = "IncreaseButton%d" %(iPlayerID)
			self.aszIncreaseButtons.append(szName)
			screen.setImageButtonAt( szName, attach, ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_PLUS").getPath(), self.LeaderPanel_X_WghtInc, self.LeaderPanelBottomRow, iSize, iSize, WidgetTypes.WIDGET_GENERAL, self.iIncreaseButtonID, iPlayerID );
			self.iDecreaseButtonID = 556
			szName = "DecreaseButton%d" %(iPlayerID)
			self.aszDecreaseButtons.append(szName)
			screen.setImageButtonAt( szName, attach, ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_MINUS").getPath(), self.LeaderPanel_X_WghtDec, self.LeaderPanelBottomRow, iSize, iSize, WidgetTypes.WIDGET_GENERAL, self.iDecreaseButtonID, iPlayerID );

			# Active Player - Symbols for 'Demographics' and 'Research'
			szName = "ActivePassiveMissionIndicator%d" %(iPlayerID)
			screen.deleteWidget(szName)

			iCost = pActivePlayer.getEspionageMissionCost(self.MissionSeeDemo, iPlayerID, None, -1)
			if iPlayerEPs >= iCost:
				szText = FontUtil.getChar("ss life support")
			else:
				szText = FontUtil.getChar("space")

			iCost = pActivePlayer.getEspionageMissionCost(self.MissionSeeResearch, iPlayerID, None, -1)
			if iPlayerEPs >= iCost:
				szText += FontUtil.getChar("commerce research")
			else:
				szText += FontUtil.getChar("space")

			screen.setLabelAt( szName, attach, szText, CvUtil.FONT_LEFT_JUSTIFY, self.LeaderPanel_X_PassiveMissions, self.LeaderPanelTopRow, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 );

			# Target Player - Symbols for 'Demographics' and 'Research'
			if EspionageOpt.isShowCalculatedInformation():
				szName = "TargetPassiveMissionIndicator%d" %(iPlayerID)
				screen.deleteWidget(szName)

				iCost = pTargetPlayer.getEspionageMissionCost(self.MissionSeeDemo, self.iActivePlayer, None, -1)
				if iTargetEPs >= iCost:
					szText = FontUtil.getChar("ss life support")
				else:
					szText = FontUtil.getChar("space")

				iCost = pTargetPlayer.getEspionageMissionCost(self.MissionSeeResearch, self.iActivePlayer, None, -1)
				if iTargetEPs >= iCost:
					szText += FontUtil.getChar("commerce research")
				else:
					szText += FontUtil.getChar("space")

				screen.setLabelAt( szName, attach, szText, CvUtil.FONT_LEFT_JUSTIFY, self.LeaderPanel_X_PassiveMissions, self.LeaderPanelBottomRow, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 );

			# Espionage Icon
			szName = "SpendingIcon%d" %(iPlayerID)
			self.aszEspionageIcons.append(szName)
			if (pActivePlayer.getEspionageSpendingWeightAgainstTeam(iTargetTeam) > 0):
				szText = u"<font=2>%c</font>" %(gc.getCommerceInfo(CommerceTypes.COMMERCE_ESPIONAGE).getChar())
			else:
				szText = u""

			screen.setLabelAt( szName, attach, szText, 0, self.LeaderPanel_X_EspionageIcon, self.LeaderPanelMiddle, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 );

		for iPlayerID in self.aiUnknownPlayers:
			attach = "EmptyLeaderContainer%d" % (iPlayerID)
			screen.attachPanel(self.szScrollPanel, attach, "", "", True, False, PanelStyles.PANEL_STYLE_STANDARD)
			screen.attachSeparator(attach, "EmptyLeaderImageA%d" %(iPlayerID), true, 30)




	def drawGlanceTab(self):
		return

	def getEspionageMultiplier(self, iCurrentPlayer, iTargetPlayer):
		pCurrentPlayer = gc.getPlayer(iCurrentPlayer)
		iCurrentTeamID = pCurrentPlayer.getTeam()
		pTargetPlayer = gc.getPlayer(iTargetPlayer)
		iTargetTeamID = pTargetPlayer.getTeam()

		iMultiplier = getEspionageModifier(iCurrentTeamID, iTargetTeamID)
		return iMultiplier

	def getEspionageMultiplierText(self, iCurrentPlayer, iTargetPlayer):
		pCurrentPlayer = gc.getPlayer(iCurrentPlayer)
		iCurrentTeamID = pCurrentPlayer.getTeam()
		pTargetPlayer = gc.getPlayer(iTargetPlayer)
		iTargetTeamID = pTargetPlayer.getTeam()

		iMultiplier = getEspionageModifier(iCurrentTeamID, iTargetTeamID)
		szMultiplier = localText.getText("TXT_KEY_ESPIONAGE_COST", (iMultiplier, ))

		if self.getCounterEspionageTurnsLeft(iCurrentPlayer, iTargetPlayer) > 0:
			szMultiplier += u"*"

		if self.getCounterEspionageTurnsLeft(iTargetPlayer, iCurrentPlayer) > 0:
			szMultiplier += u"+"

		return szMultiplier

	def getCounterEspionageTurnsLeft(self, iCurrentPlayer, iTargetPlayer):
		pCurrentTeam = gc.getTeam(gc.getPlayer(iCurrentPlayer).getTeam())
		iTargetTeamID = gc.getPlayer(iTargetPlayer).getTeam()

		iCurrentCounterEsp = pCurrentTeam.getCounterespionageTurnsLeftAgainstTeam(iTargetTeamID)
		return iCurrentCounterEsp

	def refreshMissionTab(self):

		self.deleteAllWidgets()

		if (self.iTargetPlayer != -1):

			# Create a new screen, called EspionageAdvisor, using the file EspionageAdvisor.py for input
			screen = self.getScreen()
			
			pActivePlayer = gc.getPlayer(self.iActivePlayer)
			pActiveTeam = gc.getTeam(pActivePlayer.getTeam())
			
#			iPlayerLoop = 0
			
			for iPlayerID in self.aiKnownPlayers:
				if EspionageOpt.isEnabled():
					self.refreshMissionTab_LeftLeaderPanel_BUG(screen, pActivePlayer, iPlayerID)
				else:
					self.refreshMissionTab_LeftLeaderPanel(screen, pActivePlayer, iPlayerID)

			# Is there any other players which have been met?
			if (self.iTargetPlayer != -1):
				pTargetPlayer = gc.getPlayer(self.iTargetPlayer)
				pyTargetPlayer = PyPlayer(self.iTargetPlayer)

				# List of Cities
				self.szCityListBox = self.getNextWidgetName()
				screen.addListBoxGFC(self.szCityListBox, "", self.X_CITY_LIST, self.Y_CITY_LIST, self.W_CITY_LIST, self.H_CITY_LIST, TableStyles.TABLE_STYLE_STANDARD)
				screen.enableSelect(self.szCityListBox, True)
				screen.setStyle(self.szCityListBox, "Table_StandardCiv_Style")

				if self.CityMissionToggle == CITYMISSION_CITY:
					# Loop through target's cities, see which are visible and add them to the list
					apCityList = pyTargetPlayer.getCityList()

					iLoop = 0
					for pyCity in apCityList:
						pCity = pyCity.GetCy()
						szCityName = self.getCityNameText(pCity, self.iActivePlayer, self.iTargetPlayer)

						if (EspionageOpt.isEnabled()
						or (not EspionageOpt.isEnabled()
							and pCity.isRevealed(pActivePlayer.getTeam(), false))):
							screen.appendListBoxString( self.szCityListBox, szCityName, WidgetTypes.WIDGET_GENERAL, pCity.getID(), 0, CvUtil.FONT_LEFT_JUSTIFY )

							if (self.iActiveCityID == -1 or pTargetPlayer.getCity(self.iActiveCityID).isNone()):
								self.iActiveCityID = pCity.getID()

							if (self.iActiveCityID == pCity.getID()):
								screen.setSelectedListBoxStringGFC(self.szCityListBox, iLoop)

							iLoop += 1

				elif self.CityMissionToggle == CITYMISSION_MISSION:
					# active missions only
					iLoop = 0
					for iMissionLoop in range(gc.getNumEspionageMissionInfos()):
						pMission = gc.getEspionageMissionInfo(iMissionLoop)
						if (pMission.getCost() != -1):
#							if (not pMission.isPassive()):
							if pMission.isTargetsCity():
								screen.appendListBoxString( self.szCityListBox, pMission.getDescription(), WidgetTypes.WIDGET_GENERAL, iMissionLoop, 0, CvUtil.FONT_LEFT_JUSTIFY )

								if (self.iActiveMissionID == -1):
									self.iActiveMissionID = iMissionLoop

								if (self.iActiveMissionID == iMissionLoop):
									screen.setSelectedListBoxStringGFC(self.szCityListBox, iLoop)

								iLoop += 1

				self.W_TABLE_0 = self.W_EFFECTS_LIST
				self.W_TABLE_1 = 0
				self.W_TABLE_2 = self.W_EFFECTS_COSTS_LIST
				self.W_TABLE_3 = 20

				szEffectsTable = self.getNextWidgetName()
				szHelpText = localText.getText("TXT_KEY_ESPIONAGE_PASSIVE_AUTOMATIC", ())
				screen.addTableControlGFCWithHelp(szEffectsTable, 4, self.X_EFFECTS_LIST, self.Y_EFFECTS_LIST, self.W_EFFECTS_LIST + self.W_EFFECTS_COSTS_LIST + self.W_TABLE_1 + self.W_TABLE_3, self.H_EFFECTS_LIST, False, False, 32,32, TableStyles.TABLE_STYLE_STANDARD, szHelpText)
				screen.setTableColumnHeader(szEffectsTable, 0, "", self.W_TABLE_0)
				screen.setTableColumnHeader(szEffectsTable, 1, "", self.W_TABLE_1)
				screen.setTableColumnHeader(szEffectsTable, 2, "", self.W_TABLE_2)
				screen.setTableColumnHeader(szEffectsTable, 3, "", self.W_TABLE_3)

				szMissionsTable = self.getNextWidgetName()
				if self.CityMissionToggle == CITYMISSION_CITY:
					szHelpText = localText.getText("TXT_KEY_ESPIONAGE_MISSIONS_SPY", ())
				else:
					szHelpText = ""
				screen.addTableControlGFCWithHelp(szMissionsTable, 4, self.X_MISSIONS_LIST, self.Y_MISSIONS_LIST, self.W_MISSIONS_LIST + self.W_MISSIONS_COSTS_LIST + self.W_TABLE_1 + self.W_TABLE_3, self.H_MISSIONS_LIST, False, False, 32,32, TableStyles.TABLE_STYLE_STANDARD, szHelpText)
				screen.setTableColumnHeader(szMissionsTable, 0, "", self.W_TABLE_0)
				screen.setTableColumnHeader(szMissionsTable, 1, "", self.W_TABLE_1)
				screen.setTableColumnHeader(szMissionsTable, 2, "", self.W_TABLE_2)
				screen.setTableColumnHeader(szMissionsTable, 3, "", self.W_TABLE_3)

				# Loop through passive Missions
				for iMissionLoop in range(gc.getNumEspionageMissionInfos()):
					pMission = gc.getEspionageMissionInfo(iMissionLoop)
					if (pMission.getCost() != -1):
						if (pMission.isPassive()):
							if (self.CityMissionToggle == CITYMISSION_CITY
							or (self.CityMissionToggle == CITYMISSION_MISSION
							and not pMission.isTargetsCity())):
#							and (iMissionLoop == self.MissionSeeDemo
#							or iMissionLoop == self.MissionSeeResearch))):
								szTable = szEffectsTable
								szText, szCost = self.getTableTextCost(self.iActivePlayer, self.iTargetPlayer, iMissionLoop, self.iActiveCityID)
								iRow = screen.appendTableRow(szTable)
								screen.setTableText(szTable, 0, iRow, szText, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
								screen.setTableText(szTable, 2, iRow, szCost, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)

				if self.CityMissionToggle == CITYMISSION_CITY:
					# Loop through active Missions
					# Primary list is cities, secondary list is missions
					for iMissionLoop in range(gc.getNumEspionageMissionInfos()):
						pMission = gc.getEspionageMissionInfo(iMissionLoop)
						if (pMission.getCost() != -1):
							if (not pMission.isPassive()):
								szTable = szMissionsTable
								szText, szCost = self.getTableTextCost(self.iActivePlayer, self.iTargetPlayer, iMissionLoop, self.iActiveCityID)
								iRow = screen.appendTableRow(szTable)
								screen.setTableText(szTable, 0, iRow, szText, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
								screen.setTableText(szTable, 2, iRow, szCost, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)

				elif self.CityMissionToggle == CITYMISSION_MISSION:
					# Loop through target's cities, see which are visible and add them to the list
					# Primary list is missions, secondary list is cities
					apCityList = pyTargetPlayer.getCityList()

					for pyCity in apCityList:
						pCity = pyCity.GetCy()

						szTable = szMissionsTable
						szText, szCost = self.getTableTextCost(self.iActivePlayer, self.iTargetPlayer, self.iActiveMissionID, pCity.getID())
						iRow = screen.appendTableRow(szTable)
						screen.setTableText(szTable, 0, iRow, szText, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
						if (pCity.isRevealed(pActivePlayer.getTeam(), false)):
							screen.setTableText(szTable, 2, iRow, szCost, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)

					#screen.updateListBox(self.szCityListBox)

		return 0

	def refreshMissionTab_LeftLeaderPanel(self, screen, pActivePlayer, iPlayerID):
		iX = 0
		iY = 15
		
		pTargetPlayer = gc.getPlayer(iPlayerID)
		iTargetTeam = pTargetPlayer.getTeam()
		
		attach = "LeaderContainer%d" % (iPlayerID)
		
		szName = "SpendingText%d" %(iPlayerID)
		self.aszSpendingTexts.append(szName)
		szText = u"<font=2>" + localText.getText("TXT_KEY_ESPIONAGE_SCREEN_SPENDING_WEIGHT", ()) + ": %d</font>" %(pActivePlayer.getEspionageSpendingWeightAgainstTeam(iTargetTeam))
		screen.deleteWidget(szName)
		screen.setLabelAt( szName, attach, szText, 0, 85, iY, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 );
		
		szName = "AmountText%d" %(iPlayerID)

		if (pActivePlayer.getEspionageSpending(iTargetTeam) > 0):
			szText = u"<font=2><color=0,255,0,0>%s</color></font>" %(localText.getText("TXT_KEY_ESPIONAGE_NUM_EPS_PER_TURN", (pActivePlayer.getEspionageSpending(iTargetTeam), )))
		else:
			szText = u"<font=2><color=192,0,0,0>%s</color></font>" %(localText.getText("TXT_KEY_ESPIONAGE_NUM_EPS_PER_TURN", (pActivePlayer.getEspionageSpending(iTargetTeam), )))

		screen.deleteWidget(szName)
		screen.setLabelAt( szName, attach, szText, 0, 247, iY - 1, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 );

		szName = "SpendingIcon%d" %(iPlayerID)
		if (pActivePlayer.getEspionageSpendingWeightAgainstTeam(iTargetTeam) > 0):
			szText = u"<font=2>%c</font>" %(gc.getCommerceInfo(CommerceTypes.COMMERCE_ESPIONAGE).getChar())
		else:
			szText = u""

		screen.deleteWidget(szName)
		screen.setLabelAt( szName, attach, szText, 0, 3, iY - 9, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 );

	def refreshMissionTab_LeftLeaderPanel_BUG(self, screen, pActivePlayer, iPlayerID):
		pTargetPlayer = gc.getPlayer(iPlayerID)
		iTargetTeam = pTargetPlayer.getTeam()

		attach = "LeaderContainer%d" % (iPlayerID)

		# EP Weight
		szName = "SpendingText%d" %(iPlayerID)
		self.aszSpendingTexts.append(szName)
		szText = u"<font=2>" + localText.getText("TXT_KEY_ESPIONAGE_SCREEN_SPENDING_WEIGHT", ()) + ": %d</font>" %(pActivePlayer.getEspionageSpendingWeightAgainstTeam(iTargetTeam))
		screen.deleteWidget(szName)
		screen.setLabelAt( szName, attach, szText, 0, self.LeaderPanel_X_Wght, self.LeaderPanelBottomRow, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 );

		# EP Spending (Points per turn)
		szName = "AmountText%d" %(iPlayerID)
		iSpending = pActivePlayer.getEspionageSpending(iTargetTeam)
		if (iSpending > 0):
			szText = u"<font=2><color=0,255,0,0>(+%i)</color></font>" %(iSpending)
		else:
			szText = u""
		screen.deleteWidget(szName)
		screen.setLabelAt( szName, attach, szText, CvUtil.FONT_LEFT_JUSTIFY, self.LeaderPanel_X_EPointsTurn, self.LeaderPanelTopRow, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 );

	def getCityNameText(self, pCity, iActivePlayer, iTargetPlayer):
		if not EspionageOpt.isEnabled():
			return pCity.getName()

		szCityName = pCity.getName()
		iPlayerEPs = self.getPlayerEPs(iActivePlayer, iTargetPlayer)
		pActivePlayer = gc.getPlayer(iActivePlayer)
		pPlot = pCity.plot()

		if not pCity.isRevealed(pActivePlayer.getTeam(), false):
			szCityName = "-- %s --" %(szCityName)

		return szCityName

	def getPlayerEPs(self, iCurrentPlayer, iTargetPlayer):
		pCurrentPlayer = gc.getPlayer(iCurrentPlayer)
		pCurrentTeam = gc.getTeam(pCurrentPlayer.getTeam())
		pTargetPlayer = gc.getPlayer(iTargetPlayer)
		iTargetTeam = pTargetPlayer.getTeam()
		EPs = pCurrentTeam.getEspionagePointsAgainstTeam(iTargetTeam)
		return EPs

	def getTableTextCost(self, iActivePlayer, iTargetPlayer, iMission, iCity):

		pActivePlayer = gc.getPlayer(iActivePlayer)
		pActiveTeam = gc.getTeam(pActivePlayer.getTeam())
		pTargetPlayer = gc.getPlayer(iTargetPlayer)
		pMission = gc.getEspionageMissionInfo(iMission)

		szText = ""
		szCost = ""

		if pMission.getCost() == -1:
			return szText, szCost

		iTargetTeam = pTargetPlayer.getTeam()
		iPlayerEPs = self.getPlayerEPs(iActivePlayer, iTargetPlayer)
		if (EspionageOpt.isEnabled()):
			iPossibleColor = EspionageOpt.getPossibleMissionColor()
			iCloseColor = EspionageOpt.getCloseMissionColor()
			iClosePercent = EspionageOpt.getCloseMissionPercent()
		else:
			iPossibleColor = -1
			iCloseColor = -1
			iClosePercent = -1

		pPlot = None
		szCityName= ""
		bHideCost = False
		if (iCity != -1
		and pMission.isTargetsCity()):
			pActiveCity = gc.getPlayer(iTargetPlayer).getCity(iCity)
			pPlot = pActiveCity.plot()
			szCityName = pActiveCity.getName()
			szCityName = self.getCityNameText(pActiveCity, iActivePlayer, iTargetPlayer)
			if not pActiveCity.isRevealed(pActivePlayer.getTeam(), false):
				bHideCost = True

		if not bHideCost:
			iCost = pActivePlayer.getEspionageMissionCost(iMission, iTargetPlayer, pPlot, -1)
		else:
			iCost = 0

		if (self.CityMissionToggle == CITYMISSION_CITY # secondary list is mission names
		or (pMission.isPassive()
		and not pMission.isTargetsCity())):
			szTechText = ""
			if (pMission.getTechPrereq() != -1):
				szTechText = " (%s)" %(gc.getTechInfo(pMission.getTechPrereq()).getDescription())

			szText = pMission.getDescription() + szTechText
		else: # secondary list is city names
			szText = szCityName

		if iCost > 0:
			szCost = unicode(str(iCost))
			if (EspionageOpt.isEnabled()):
				if (iPossibleColor >= 0 and iPlayerEPs >= iCost):
					szCost = localText.changeTextColor(szCost, iPossibleColor)
					szText = localText.changeTextColor(szText, iPossibleColor)
				elif (iCloseColor >= 0 and iPlayerEPs >= (iCost * float(100 - iClosePercent) / 100)):
					szCost = localText.changeTextColor(szCost, iCloseColor)
					szText = localText.changeTextColor(szText, iCloseColor)

		if (pMission.getTechPrereq() != -1):
			pTeam = gc.getTeam(pActivePlayer.getTeam())
			if (not pTeam.isHasTech(pMission.getTechPrereq())):
				szText = u"<color=255,0,0,0>%s</color>" %(szText)
				return szText, szCost

		return szText, szCost

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
			
	# Will handle the input for this screen...
	def handleInput (self, inputClass):
		'Calls function mapped in EspionageAdvisorInputMap'
		
		screen = self.getScreen()
		pActivePlayer = gc.getPlayer(self.iActivePlayer)
		
		##### Debug Dropdown #####
		if (CyGame().isDebugMode()):
			if (inputClass.getFunctionName() == self.DEBUG_DROPDOWN_ID):
				iIndex = screen.getSelectedPullDownID(self.DEBUG_DROPDOWN_ID)
				self.iActivePlayer = screen.getPullDownData(self.DEBUG_DROPDOWN_ID, iIndex)
				self.drawContents()
				CyInterface().setDirty(InterfaceDirtyBits.Espionage_Advisor_DIRTY_BIT, True)
		
		if (self.iTargetPlayer != -1):

			if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED):
				if ((inputClass.getFunctionName() == self.szMissionsTitleText
				or   inputClass.getFunctionName() == self.szCitiesTitleText)
				and EspionageOpt.isEnabled()):
					if self.CityMissionToggle == CITYMISSION_MISSION:
						self.CityMissionToggle = CITYMISSION_CITY
						self.drawContents()
						return 0
					else:
						self.CityMissionToggle = CITYMISSION_MISSION
						self.drawContents()
						return 0

			##### Player Images #####
			if (inputClass.getData1() == self.iLeaderImagesID):
				self.iTargetPlayer = inputClass.getData2()

				# Loop through all images
				for iPlayerID in self.aiKnownPlayers:
					szName = "LeaderImage%d" %(iPlayerID)
					if (self.iTargetPlayer == iPlayerID):
						screen.setState(szName, true)
					else:
						screen.setState(szName, false)

					self.iActiveCityID = -1

				CyInterface().setDirty(InterfaceDirtyBits.Espionage_Advisor_DIRTY_BIT, True)
				return 0

			##### City Listbox #####
			if ("%s%d" %(inputClass.getFunctionName(), inputClass.getID()) == self.szCityListBox):
				if self.CityMissionToggle == CITYMISSION_CITY:
					iCityID = inputClass.getData1()
					self.iActiveCityID = iCityID
					CyInterface().setDirty(InterfaceDirtyBits.Espionage_Advisor_DIRTY_BIT, True)
				else:
					self.iActiveMissionID = inputClass.getData1()
					CyInterface().setDirty(InterfaceDirtyBits.Espionage_Advisor_DIRTY_BIT, True)
				return 0

			# EP spending weight adjustments
			##### Increase Button #####
			if (inputClass.getData1() == self.iIncreaseButtonID):
				iPlayerID = inputClass.getData2()
				iTargetTeam = gc.getPlayer(iPlayerID).getTeam()

				CyMessageControl().sendEspionageSpendingWeightChange(iTargetTeam, 1)
				CyInterface().setDirty(InterfaceDirtyBits.Espionage_Advisor_DIRTY_BIT, True)
				return 0

			##### Decrease Button #####
			elif (inputClass.getData1() == self.iDecreaseButtonID):
				iPlayerID = inputClass.getData2()
				iTargetTeam = gc.getPlayer(iPlayerID).getTeam()

				if (pActivePlayer.getEspionageSpendingWeightAgainstTeam(iTargetTeam) > 0):	# Can't reduce weight below 0
					CyMessageControl().sendEspionageSpendingWeightChange(iTargetTeam, -1)
					CyInterface().setDirty(InterfaceDirtyBits.Espionage_Advisor_DIRTY_BIT, True)
				return 0

		return 0

	def update(self, fDelta):
		if (CyInterface().isDirty(InterfaceDirtyBits.Espionage_Advisor_DIRTY_BIT) == True):
			CyInterface().setDirty(InterfaceDirtyBits.Espionage_Advisor_DIRTY_BIT, False)
			self.refreshMissionTab()
		return

