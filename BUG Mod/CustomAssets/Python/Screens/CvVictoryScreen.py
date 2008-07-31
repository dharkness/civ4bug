## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
from CvPythonExtensions import *
import CvUtil
import ScreenInput
import PyHelpers
import time
import ColorUtil
import AttitudeUtils

PyPlayer = PyHelpers.PyPlayer

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

VICTORY_CONDITION_SCREEN = 0
GAME_SETTINGS_SCREEN = 1
UN_RESOLUTION_SCREEN = 2
UN_MEMBERS_SCREEN = 3

class CvVictoryScreen:
	"Keeps track of victory conditions"

	def __init__(self, screenId):
		self.screenId = screenId
		self.SCREEN_NAME = "VictoryScreen"
		self.DEBUG_DROPDOWN_ID =  "VictoryScreenDropdownWidget"
		self.INTERFACE_ART_INFO = "TECH_BG"
		self.EXIT_AREA = "EXIT"
		self.EXIT_ID = "VictoryScreenExit"
		self.BACKGROUND_ID = "VictoryScreenBackground"
		self.HEADER_ID = "VictoryScreenHeader"
		self.WIDGET_ID = "VictoryScreenWidget"
		self.VC_TAB_ID = "VictoryTabWidget"
		self.SETTINGS_TAB_ID = "SettingsTabWidget"
		self.UN_RESOLUTION_TAB_ID = "VotingTabWidget"
		self.UN_MEMBERS_TAB_ID = "MembersTabWidget"
		self.SPACESHIP_SCREEN_BUTTON = 1234
		
		self.Z_BACKGROUND = -6.1
		self.Z_CONTROLS = self.Z_BACKGROUND - 0.2
		self.DZ = -0.2

		self.X_SCREEN = 500
		self.Y_SCREEN = 396
		self.W_SCREEN = 1024
		self.H_SCREEN = 768
		self.Y_TITLE = 12
		
		self.X_EXIT = 994
		self.Y_EXIT = 726
		
		self.X_AREA = 10
		self.Y_AREA = 60
		self.W_AREA = 1010
		self.H_AREA = 650
		
		self.TABLE_WIDTH_0 = 350
		self.TABLE_WIDTH_1 = 80
		self.TABLE_WIDTH_2 = 180
		self.TABLE_WIDTH_3 = 100
		self.TABLE_WIDTH_4 = 180
		self.TABLE_WIDTH_5 = 100

		self.TABLE2_WIDTH_0 = 740
		self.TABLE2_WIDTH_1 = 265

# BUG Additions Start
		self.TABLE3_WIDTH_0 = 450
		self.TABLE3_WIDTH_1 = 80
		self.TABLE3_WIDTH_2 = 80
		self.TABLE3_WIDTH_3 = 80
		self.TABLE3_WIDTH_4 = 80
		self.TABLE3_WIDTH_5 = 200
# BUG Additions End

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
		self.bVoteTab = False

		self.iScreen = VICTORY_CONDITION_SCREEN
						
	def getScreen(self):
		return CyGInterfaceScreen(self.SCREEN_NAME, self.screenId)

	def hideScreen(self):
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
			self.iScreen = VICTORY_CONDITION_SCREEN

		# Set the background widget and exit button
		screen.addDDSGFC(self.BACKGROUND_ID, ArtFileMgr.getInterfaceArtInfo("MAINMENU_SLIDESHOW_LOAD").getPath(), 0, 0, self.W_SCREEN, self.H_SCREEN, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addPanel( "TechTopPanel", u"", u"", True, False, 0, 0, self.W_SCREEN, 55, PanelStyles.PANEL_STYLE_TOPBAR )
		screen.addPanel( "TechBottomPanel", u"", u"", True, False, 0, 713, self.W_SCREEN, 55, PanelStyles.PANEL_STYLE_BOTTOMBAR )
		screen.showWindowBackground( False )
		screen.setDimensions(screen.centerX(0), screen.centerY(0), self.W_SCREEN, self.H_SCREEN)
		screen.setText(self.EXIT_ID, "Background", u"<font=4>" + localText.getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, self.X_EXIT, self.Y_EXIT, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1 )

		# Header...
		screen.setLabel(self.HEADER_ID, "Background", u"<font=4b>" + localText.getText("TXT_KEY_VICTORY_SCREEN_TITLE", ()).upper() + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_SCREEN, self.Y_TITLE, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		if self.iScreen == VICTORY_CONDITION_SCREEN:
			self.showVictoryConditionScreen()
		elif self.iScreen == GAME_SETTINGS_SCREEN:
			self.showGameSettingsScreen()
		elif self.iScreen == UN_RESOLUTION_SCREEN:
			self.showVotingScreen()
		elif self.iScreen == UN_MEMBERS_SCREEN:
			self.showMembersScreen()

	def drawTabs(self):
	
		screen = self.getScreen()

		xLink = self.X_LINK
		if (self.iScreen != VICTORY_CONDITION_SCREEN):
			screen.setText(self.VC_TAB_ID, "", u"<font=4>" + localText.getText("TXT_KEY_MAIN_MENU_VICTORIES", ()).upper() + "</font>", CvUtil.FONT_CENTER_JUSTIFY, xLink, self.Y_LINK, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		else:
			screen.setText(self.VC_TAB_ID, "", u"<font=4>" + localText.getColorText("TXT_KEY_MAIN_MENU_VICTORIES", (), gc.getInfoTypeForString("COLOR_YELLOW")).upper() + "</font>", CvUtil.FONT_CENTER_JUSTIFY, xLink, self.Y_LINK, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		xLink += self.DX_LINK
			
		if (self.iScreen != GAME_SETTINGS_SCREEN):
			screen.setText(self.SETTINGS_TAB_ID, "", u"<font=4>" + localText.getText("TXT_KEY_MAIN_MENU_SETTINGS", ()).upper() + "</font>", CvUtil.FONT_CENTER_JUSTIFY, xLink, self.Y_LINK, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		else:
			screen.setText(self.SETTINGS_TAB_ID, "", u"<font=4>" + localText.getColorText("TXT_KEY_MAIN_MENU_SETTINGS", (), gc.getInfoTypeForString("COLOR_YELLOW")).upper() + "</font>", CvUtil.FONT_CENTER_JUSTIFY, xLink, self.Y_LINK, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		xLink += self.DX_LINK
			
		if self.bVoteTab:			
			if (self.iScreen != UN_RESOLUTION_SCREEN):
				screen.setText(self.UN_RESOLUTION_TAB_ID, "", u"<font=4>" + localText.getText("TXT_KEY_VOTING_TITLE", ()).upper() + "</font>", CvUtil.FONT_CENTER_JUSTIFY, xLink, self.Y_LINK, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			else:
				screen.setText(self.UN_RESOLUTION_TAB_ID, "", u"<font=4>" + localText.getColorText("TXT_KEY_VOTING_TITLE", (), gc.getInfoTypeForString("COLOR_YELLOW")).upper() + "</font>", CvUtil.FONT_CENTER_JUSTIFY, xLink, self.Y_LINK, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			xLink += self.DX_LINK

			if (self.iScreen != UN_MEMBERS_SCREEN):
				screen.setText(self.UN_MEMBERS_TAB_ID, "", u"<font=4>" + localText.getText("TXT_KEY_MEMBERS_TITLE", ()).upper() + "</font>", CvUtil.FONT_CENTER_JUSTIFY, xLink, self.Y_LINK, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			else:
				screen.setText(self.UN_MEMBERS_TAB_ID, "", u"<font=4>" + localText.getColorText("TXT_KEY_MEMBERS_TITLE", (), gc.getInfoTypeForString("COLOR_YELLOW")).upper() + "</font>", CvUtil.FONT_CENTER_JUSTIFY, xLink, self.Y_LINK, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			xLink += self.DX_LINK

	def showVotingScreen(self):
	
		self.deleteAllWidgets()
	
		activePlayer = gc.getPlayer(self.iActivePlayer)
		iActiveTeam = activePlayer.getTeam()
		
		aiVoteBuildingClass = []
		for i in range(gc.getNumBuildingInfos()):
			for j in range(gc.getNumVoteSourceInfos()):
				if (gc.getBuildingInfo(i).getVoteSourceType() == j):								
					iUNTeam = -1
					bUnknown = true
					for iLoopTeam in range(gc.getMAX_CIV_TEAMS()):
						if (gc.getTeam(iLoopTeam).isAlive() and not gc.getTeam(iLoopTeam).isMinorCiv() and not gc.getTeam(iLoopTeam).isBarbarian()):
							if (gc.getTeam(iLoopTeam).getBuildingClassCount(gc.getBuildingInfo(i).getBuildingClassType()) > 0):
								iUNTeam = iLoopTeam
								if (iLoopTeam == iActiveTeam or gc.getGame().isDebugMode() or gc.getTeam(activePlayer.getTeam()).isHasMet(iLoopTeam)):
									bUnknown = false		
								break
									
					aiVoteBuildingClass.append((gc.getBuildingInfo(i).getBuildingClassType(), iUNTeam, bUnknown))
				
		if (len(aiVoteBuildingClass) == 0):
			return

		screen = self.getScreen()

		screen.addPanel(self.getNextWidgetName(), "", "", False, False, self.X_AREA-10, self.Y_AREA-15, self.W_AREA+20, self.H_AREA+30, PanelStyles.PANEL_STYLE_BLUE50)
		szTable = self.getNextWidgetName()
		screen.addTableControlGFC(szTable, 2, self.X_AREA, self.Y_AREA, self.W_AREA, self.H_AREA, False, False, 32,32, TableStyles.TABLE_STYLE_STANDARD)
		screen.enableSelect(szTable, False)		
		screen.setTableColumnHeader(szTable, 0, "", self.TABLE2_WIDTH_0)
		screen.setTableColumnHeader(szTable, 1, "", self.TABLE2_WIDTH_1)

		for (iVoteBuildingClass, iUNTeam, bUnknown) in aiVoteBuildingClass:
			iRow = screen.appendTableRow(szTable)
			screen.setTableText(szTable, 0, iRow, localText.getText("TXT_KEY_VICTORY_SCREEN_ELECTION", (gc.getBuildingClassInfo(iVoteBuildingClass).getTextKey(), )), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
			if (iUNTeam != -1):
				if bUnknown:
					szName = localText.getText("TXT_KEY_TOPCIVS_UNKNOWN", ())
				else:
					szName = gc.getTeam(iUNTeam).getName()
				screen.setTableText(szTable, 1, iRow, localText.getText("TXT_KEY_VICTORY_SCREEN_BUILT", (szName, )), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
			else:
				screen.setTableText(szTable, 1, iRow, localText.getText("TXT_KEY_VICTORY_SCREEN_NOT_BUILT", ()), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

		for i in range(gc.getNumVoteSourceInfos()):
			if (gc.getGame().canHaveSecretaryGeneral(i) and -1 != gc.getGame().getSecretaryGeneral(i)):
				iRow = screen.appendTableRow(szTable)
				screen.setTableText(szTable, 0, iRow, gc.getVoteSourceInfo(i).getSecretaryGeneralText(), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
				screen.setTableText(szTable, 1, iRow, gc.getTeam(gc.getGame().getSecretaryGeneral(i)).getName(), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
	
			for iLoop in range(gc.getNumVoteInfos()):
				if gc.getGame().countPossibleVote(iLoop, i) > 0:		
					info = gc.getVoteInfo(iLoop)
					if gc.getGame().isChooseElection(iLoop):			
						iRow = screen.appendTableRow(szTable)
						screen.setTableText(szTable, 0, iRow, info.getDescription(), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
						if gc.getGame().isVotePassed(iLoop):
							screen.setTableText(szTable, 1, iRow, localText.getText("TXT_KEY_POPUP_PASSED", ()), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
						else:
							screen.setTableText(szTable, 1, iRow, localText.getText("TXT_KEY_POPUP_ELECTION_OPTION", (u"", gc.getGame().getVoteRequired(iLoop, i), gc.getGame().countPossibleVote(iLoop, i))), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
								
		self.drawTabs()


	def showMembersScreen(self):
	
		self.deleteAllWidgets()
	
		activePlayer = gc.getPlayer(self.iActivePlayer)
		iActiveTeam = activePlayer.getTeam()
		
		screen = self.getScreen()

		screen.addPanel(self.getNextWidgetName(), "", "", False, False, self.X_AREA-10, self.Y_AREA-15, self.W_AREA+20, self.H_AREA+30, PanelStyles.PANEL_STYLE_BLUE50)
		szTable = self.getNextWidgetName()
		screen.addTableControlGFC(szTable, 6, self.X_AREA, self.Y_AREA, self.W_AREA, self.H_AREA, False, False, 32,32, TableStyles.TABLE_STYLE_STANDARD)
		screen.enableSelect(szTable, False)		

# BUG Additions Start
		screen.setTableColumnHeader(szTable, 0, "", self.TABLE3_WIDTH_0)
		screen.setTableColumnHeader(szTable, 1, "", self.TABLE3_WIDTH_1)
		screen.setTableColumnHeader(szTable, 2, "", self.TABLE3_WIDTH_2)
		screen.setTableColumnHeader(szTable, 3, "", self.TABLE3_WIDTH_3)
		screen.setTableColumnHeader(szTable, 4, "", self.TABLE3_WIDTH_4)
		screen.setTableColumnHeader(szTable, 5, "", self.TABLE3_WIDTH_5)
# BUG Additions End

		for i in range(gc.getNumVoteSourceInfos()):
			if gc.getGame().isDiploVote(i):
				kVoteSource = gc.getVoteSourceInfo(i)
				iRow = screen.appendTableRow(szTable)
# BUG Additions Start
				sTableHeader = u"<font=4b>" + kVoteSource.getDescription().upper() + u"</font>"
				if (gc.getGame().getVoteSourceReligion(i) != -1):
#					screen.setTableText(szTable, 2, iRow, gc.getReligionInfo(gc.getGame().getVoteSourceReligion(i)).getDescription(), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
					sTableHeader += " (" + gc.getReligionInfo(gc.getGame().getVoteSourceReligion(i)).getDescription() + ")"
				screen.setTableText(szTable, 0, iRow, sTableHeader, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
# BUG Additions End

				iSecretaryGeneralVote = -1
				if (gc.getGame().canHaveSecretaryGeneral(i) and -1 != gc.getGame().getSecretaryGeneral(i)):		
					for j in range(gc.getNumVoteInfos()):
						print j
						if gc.getVoteInfo(j).isVoteSourceType(i):
							print "votesource"
							if gc.getVoteInfo(j).isSecretaryGeneral():
								print "secgen"
								iSecretaryGeneralVote = j
								break
				print iSecretaryGeneralVote
								
# BUG Additions Start
				lMembers = []
				for j in range(gc.getMAX_PLAYERS()):
					pPlayer = gc.getPlayer(j)
					if pPlayer.isAlive() and not pPlayer.isBarbarian() and gc.getTeam(iActiveTeam).isHasMet(pPlayer.getTeam()):
						iPlayer = j
						lPlayerName = pPlayer.getName()
						lPlayerVotes = 10000 - pPlayer.getVotes(iSecretaryGeneralVote, i)   # so that it sorts from most votes to least
						if (gc.getGame().canHaveSecretaryGeneral(i) and gc.getGame().getSecretaryGeneral(i) == pPlayer.getTeam()):
							lPlayerStatus = 0
							lPlayerLabel = gc.getVoteSourceInfo(i).getSecretaryGeneralText()
						elif (pPlayer.isFullMember(i)):
							lPlayerStatus = 1
							lPlayerLabel = localText.getText("TXT_KEY_VOTESOURCE_FULL_MEMBER", ())
						elif (pPlayer.isVotingMember(i)):
							lPlayerStatus = 2
							lPlayerLabel = localText.getText("TXT_KEY_VOTESOURCE_VOTING_MEMBER", ())
						else:
							lPlayerStatus = 3
							lPlayerLabel = localText.getText("TXT_KEY_VOTESOURCE_NON_VOTING_MEMBER", ())

						lMembers.append([lPlayerStatus, lPlayerVotes, lPlayerName, lPlayerLabel, iPlayer])

				lMembers.sort()

				# determine the two candidates, add to header
				iCandidate1 = lMembers[0][4]
				iCandidate2 = lMembers[1][4]
				iVote1 = 0
				iVote2 = 0
				screen.setTableText(szTable, 1, iRow, lMembers[0][2], "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
				screen.setTableText(szTable, 3, iRow, lMembers[1][2], "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)

				for lMember in lMembers:
					szPlayerText = lMember[2]
					if 10000 - lMember[1] > 0:
						szPlayerText += localText.getText("TXT_KEY_VICTORY_SCREEN_PLAYER_VOTES", (10000 - lMember[1], i), )
					iRow = screen.appendTableRow(szTable)
					screen.setTableText(szTable, 0, iRow, szPlayerText, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

					if lMember[4] != self.iActivePlayer:
						szText = AttitudeUtils.getAttitudeText (lMember[4], iCandidate1, True, True, False, False)
						if szText != None:
							screen.setTableText(szTable, 1, iRow, szText, "", WidgetTypes.WIDGET_LEADERHEAD, lMember[4], iCandidate1, CvUtil.FONT_CENTER_JUSTIFY)

						szText = AttitudeUtils.getAttitudeText (lMember[4], iCandidate2, True, True, False, False)
						if szText != None:
							screen.setTableText(szTable, 3, iRow, szText, "", WidgetTypes.WIDGET_LEADERHEAD, lMember[4], iCandidate2, CvUtil.FONT_CENTER_JUSTIFY)

					iVote = self.getVotesForWhichCandidate(lMember[4], iCandidate1, iCandidate2)
					if iVote == -1: #abstain
						screen.setTableText(szTable, 2, iRow, "-", "", WidgetTypes.WIDGET_LEADERHEAD, lMember[4], iCandidate2, CvUtil.FONT_CENTER_JUSTIFY)
						screen.setTableText(szTable, 4, iRow, "-", "", WidgetTypes.WIDGET_LEADERHEAD, lMember[4], iCandidate2, CvUtil.FONT_CENTER_JUSTIFY)
					elif iVote == 1: #votes for candidate 1
						iVote1 += 10000 - lMember[1]
						screen.setTableText(szTable, 2, iRow, str(10000 - lMember[1]), "", WidgetTypes.WIDGET_LEADERHEAD, lMember[4], iCandidate2, CvUtil.FONT_CENTER_JUSTIFY)
					else: # votes for candidate 2
						iVote2 += 10000 - lMember[1]
						screen.setTableText(szTable, 4, iRow, str(10000 - lMember[1]), "", WidgetTypes.WIDGET_LEADERHEAD, lMember[4], iCandidate2, CvUtil.FONT_CENTER_JUSTIFY)

					screen.setTableText(szTable, 5, iRow, lMember[3], "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)

				iRow = screen.appendTableRow(szTable)
				sTableHeader = u"<font=3b>Total</font>"
				screen.setTableText(szTable, 0, iRow, sTableHeader, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
				screen.setTableText(szTable, 2, iRow, str(iVote1), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
				screen.setTableText(szTable, 4, iRow, str(iVote2), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)

				iRow = screen.appendTableRow(szTable)
				iRow = screen.appendTableRow(szTable)
				if iVote1 > iVote2:
					sWin = lMembers[0][2]
					sLose = lMembers[1][2]
					nMargin = iVote1 - iVote2
				else:
					sWin = lMembers[1][2]
					sLose = lMembers[0][2]
					nMargin = iVote2 - iVote1

				sTableHeader = "The latest BUG poll has %s leading %s by %i votes." % (sWin, sLose, nMargin)  #(iVotelMembers[0][1], , gc.getGame().countPossibleVote(iLoop, i))
				screen.setTableText(szTable, 0, iRow, sTableHeader, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

# BUG Additions End

		self.drawTabs()


	def showGameSettingsScreen(self):
	
		self.deleteAllWidgets()	
		screen = self.getScreen()
				

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
		

	def showVictoryConditionScreen(self):
					
		activePlayer = PyHelpers.PyPlayer(self.iActivePlayer)
		iActiveTeam = gc.getPlayer(self.iActivePlayer).getTeam()
		
		# Conquest
		nRivals = -1
# BUG Additions Start
		nknown = 0
		nVassaled = 0
# BUG Additions End
		for i in range(gc.getMAX_CIV_TEAMS()):
			if (gc.getTeam(i).isAlive() and not gc.getTeam(i).isMinorCiv() and not gc.getTeam(i).isBarbarian()):
				nRivals += 1
# BUG Additions Start
				if i != iActiveTeam:
					if gc.getTeam(i).isHasMet(iActiveTeam):
						nknown += 1
					if gc.getTeam(i).isVassal(iActiveTeam):
						nVassaled += 1
# BUG Additions End

		# Population
		totalPop = gc.getGame().getTotalPopulation()
		ourPop = activePlayer.getTeam().getTotalPopulation()
		if (totalPop > 0):
			popPercent = (ourPop * 100.0) / totalPop
		else:
			popPercent = 0.0

		iBestPopTeam = -1
		bestPop = 0
		for iLoopTeam in range(gc.getMAX_CIV_TEAMS()):
			if (gc.getTeam(iLoopTeam).isAlive() and not gc.getTeam(iLoopTeam).isMinorCiv() and not gc.getTeam(iLoopTeam).isBarbarian()):
				if (iLoopTeam != iActiveTeam and (activePlayer.getTeam().isHasMet(iLoopTeam) or gc.getGame().isDebugMode())):
					teamPop = gc.getTeam(iLoopTeam).getTotalPopulation()
					if (teamPop > bestPop):
						bestPop = teamPop
						iBestPopTeam = iLoopTeam

		# Score
		ourScore = gc.getGame().getTeamScore(iActiveTeam)
			
		iBestScoreTeam = -1
		bestScore = 0
		for iLoopTeam in range(gc.getMAX_CIV_TEAMS()):
			if (gc.getTeam(iLoopTeam).isAlive() and not gc.getTeam(iLoopTeam).isMinorCiv() and not gc.getTeam(iLoopTeam).isBarbarian()):
				if (iLoopTeam != iActiveTeam and (activePlayer.getTeam().isHasMet(iLoopTeam) or gc.getGame().isDebugMode())):
					teamScore = gc.getGame().getTeamScore(iLoopTeam)
					if (teamScore > bestScore):
						bestScore = teamScore
						iBestScoreTeam = iLoopTeam

		# Land Area
		totalLand = gc.getMap().getLandPlots()
		ourLand = activePlayer.getTeam().getTotalLand()
		if (totalLand > 0):
			landPercent = (ourLand * 100.0) / totalLand
		else:
			landPercent = 0.0
			
		iBestLandTeam = -1
		bestLand = 0
		for iLoopTeam in range(gc.getMAX_CIV_TEAMS()):
			if (gc.getTeam(iLoopTeam).isAlive() and not gc.getTeam(iLoopTeam).isMinorCiv() and not gc.getTeam(iLoopTeam).isBarbarian()):
				if (iLoopTeam != iActiveTeam and (activePlayer.getTeam().isHasMet(iLoopTeam) or gc.getGame().isDebugMode())):
					teamLand = gc.getTeam(iLoopTeam).getTotalLand()
					if (teamLand > bestLand):
						bestLand = teamLand
						iBestLandTeam = iLoopTeam

		# Religion
		iOurReligion = -1
		ourReligionPercent = 0
		for iLoopReligion in range(gc.getNumReligionInfos()):
			if (activePlayer.getTeam().hasHolyCity(iLoopReligion)):
				religionPercent = gc.getGame().calculateReligionPercent(iLoopReligion)
				if (religionPercent > ourReligionPercent):
					ourReligionPercent = religionPercent
					iOurReligion = iLoopReligion

		iBestReligion = -1
		bestReligionPercent = 0
		for iLoopReligion in range(gc.getNumReligionInfos()):
			if (iLoopReligion != iOurReligion):
				religionPercent = gc.getGame().calculateReligionPercent(iLoopReligion)
				if (religionPercent > bestReligionPercent):
					bestReligionPercent = religionPercent
					iBestReligion = iLoopReligion

		# Total Culture
		ourCulture = activePlayer.getTeam().countTotalCulture()

		iBestCultureTeam = -1
		bestCulture = 0
		for iLoopTeam in range(gc.getMAX_CIV_TEAMS()):
			if (gc.getTeam(iLoopTeam).isAlive() and not gc.getTeam(iLoopTeam).isMinorCiv() and not gc.getTeam(iLoopTeam).isBarbarian()):
				if (iLoopTeam != iActiveTeam and (activePlayer.getTeam().isHasMet(iLoopTeam) or gc.getGame().isDebugMode())):
					teamCulture = gc.getTeam(iLoopTeam).countTotalCulture()
					if (teamCulture > bestCulture):
						bestCulture = teamCulture
						iBestCultureTeam = iLoopTeam

		# Vote
		aiVoteBuildingClass = []
		for i in range(gc.getNumBuildingInfos()):
			for j in range(gc.getNumVoteSourceInfos()):
				if (gc.getBuildingInfo(i).getVoteSourceType() == j):
					iUNTeam = -1
					bUnknown = true 
					for iLoopTeam in range(gc.getMAX_CIV_TEAMS()):
						if (gc.getTeam(iLoopTeam).isAlive() and not gc.getTeam(iLoopTeam).isMinorCiv() and not gc.getTeam(iLoopTeam).isBarbarian()):
							if (gc.getTeam(iLoopTeam).getBuildingClassCount(gc.getBuildingInfo(i).getBuildingClassType()) > 0):
								iUNTeam = iLoopTeam
								if (iLoopTeam == iActiveTeam or gc.getGame().isDebugMode() or activePlayer.getTeam().isHasMet(iLoopTeam)):
									bUnknown = false		
								break

					aiVoteBuildingClass.append((gc.getBuildingInfo(i).getBuildingClassType(), iUNTeam, bUnknown))

		self.bVoteTab = (len(aiVoteBuildingClass) > 0)

		self.deleteAllWidgets()	
		screen = self.getScreen()
														
		# Start filling in the table below
		screen.addPanel(self.getNextWidgetName(), "", "", False, False, self.X_AREA-10, self.Y_AREA-15, self.W_AREA+20, self.H_AREA+30, PanelStyles.PANEL_STYLE_BLUE50)
		szTable = self.getNextWidgetName()
		screen.addTableControlGFC(szTable, 6, self.X_AREA, self.Y_AREA, self.W_AREA, self.H_AREA, False, False, 32,32, TableStyles.TABLE_STYLE_STANDARD)
		screen.setTableColumnHeader(szTable, 0, "", self.TABLE_WIDTH_0)
		screen.setTableColumnHeader(szTable, 1, "", self.TABLE_WIDTH_1)
		screen.setTableColumnHeader(szTable, 2, "", self.TABLE_WIDTH_2)
		screen.setTableColumnHeader(szTable, 3, "", self.TABLE_WIDTH_3)
		screen.setTableColumnHeader(szTable, 4, "", self.TABLE_WIDTH_4)
		screen.setTableColumnHeader(szTable, 5, "", self.TABLE_WIDTH_5)
		screen.appendTableRow(szTable)
		
		for iLoopVC in range(gc.getNumVictoryInfos()):
			victory = gc.getVictoryInfo(iLoopVC)
			if gc.getGame().isVictoryValid(iLoopVC):
				
				iNumRows = screen.getTableNumRows(szTable)
				szVictoryType = u"<font=4b>" + victory.getDescription().upper() + u"</font>"
				if (victory.isEndScore() and (gc.getGame().getMaxTurns() > gc.getGame().getElapsedGameTurns())):
					szVictoryType += "    (" + localText.getText("TXT_KEY_MISC_TURNS_LEFT", (gc.getGame().getMaxTurns() - gc.getGame().getElapsedGameTurns(), )) + ")"

				iVictoryTitleRow = iNumRows - 1
				screen.setTableText(szTable, 0, iVictoryTitleRow, szVictoryType, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
				bSpaceshipFound = False
					
				bEntriesFound = False
				
				if (victory.isTargetScore() and gc.getGame().getTargetScore() != 0):
										
					iRow = screen.appendTableRow(szTable)
					screen.setTableText(szTable, 0, iRow, localText.getText("TXT_KEY_VICTORY_SCREEN_TARGET_SCORE", (gc.getGame().getTargetScore(), )), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
					screen.setTableText(szTable, 2, iRow, activePlayer.getTeam().getName() + ":", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
					screen.setTableText(szTable, 3, iRow, (u"%d" % ourScore), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
					
					if (iBestScoreTeam != -1):
						screen.setTableText(szTable, 4, iRow, gc.getTeam(iBestScoreTeam).getName() + ":", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
						screen.setTableText(szTable, 5, iRow, (u"%d" % bestScore), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
						
					bEntriesFound = True
				
				if (victory.isEndScore()):

					szText1 = localText.getText("TXT_KEY_VICTORY_SCREEN_HIGHEST_SCORE", (CyGameTextMgr().getTimeStr(gc.getGame().getStartTurn() + gc.getGame().getMaxTurns(), false), ))

					iRow = screen.appendTableRow(szTable)
					screen.setTableText(szTable, 0, iRow, szText1, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
					screen.setTableText(szTable, 2, iRow, activePlayer.getTeam().getName() + ":", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
					screen.setTableText(szTable, 3, iRow, (u"%d" % ourScore), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
					
					if (iBestScoreTeam != -1):
						screen.setTableText(szTable, 4, iRow, gc.getTeam(iBestScoreTeam).getName() + ":", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
						screen.setTableText(szTable, 5, iRow, (u"%d" % bestScore), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
						
					bEntriesFound = True
					
				if (victory.isConquest()):
					iRow = screen.appendTableRow(szTable)
					screen.setTableText(szTable, 0, iRow, localText.getText("TXT_KEY_VICTORY_SCREEN_ELIMINATE_ALL", ()), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
					screen.setTableText(szTable, 2, iRow, localText.getText("TXT_KEY_VICTORY_SCREEN_RIVALS_LEFT", ()), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
					screen.setTableText(szTable, 3, iRow, unicode(nRivals), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
					bEntriesFound = True
# BUG Additions Start
					sString = "%i vassaled" % (nVassaled)
					screen.setTableText(szTable, 4, iRow, sString, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
					sString = "%i unknown" % (nRivals - nknown)
					screen.setTableText(szTable, 5, iRow, sString, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
# BUG Additions End

				if (gc.getGame().getAdjustedPopulationPercent(iLoopVC) > 0):			
					iRow = screen.appendTableRow(szTable)
					screen.setTableText(szTable, 0, iRow, localText.getText("TXT_KEY_VICTORY_SCREEN_PERCENT_POP", (gc.getGame().getAdjustedPopulationPercent(iLoopVC), )), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
					screen.setTableText(szTable, 2, iRow, activePlayer.getTeam().getName() + ":", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
					screen.setTableText(szTable, 3, iRow, (u"%.2f%%" % popPercent), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
					if (iBestPopTeam != -1):
						screen.setTableText(szTable, 4, iRow, gc.getTeam(iBestPopTeam).getName() + ":", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
						screen.setTableText(szTable, 5, iRow, (u"%.2f%%" % (bestPop * 100 / totalPop)), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
					bEntriesFound = True


				if (gc.getGame().getAdjustedLandPercent(iLoopVC) > 0):
					iRow = screen.appendTableRow(szTable)
					screen.setTableText(szTable, 0, iRow, localText.getText("TXT_KEY_VICTORY_SCREEN_PERCENT_LAND", (gc.getGame().getAdjustedLandPercent(iLoopVC), )), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
					screen.setTableText(szTable, 2, iRow, activePlayer.getTeam().getName() + ":", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
					screen.setTableText(szTable, 3, iRow, (u"%.2f%%" % landPercent), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
					if (iBestLandTeam != -1):
						screen.setTableText(szTable, 4, iRow, gc.getTeam(iBestLandTeam).getName() + ":", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
						screen.setTableText(szTable, 5, iRow, (u"%.2f%%" % (bestLand * 100 / totalLand)), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
					bEntriesFound = True

				if (victory.getReligionPercent() > 0):			
					iRow = screen.appendTableRow(szTable)
					screen.setTableText(szTable, 0, iRow, localText.getText("TXT_KEY_VICTORY_SCREEN_PERCENT_RELIGION", (victory.getReligionPercent(), )), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
					if (iOurReligion != -1):
						screen.setTableText(szTable, 2, iRow, gc.getReligionInfo(iOurReligion).getDescription() + ":", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
						screen.setTableText(szTable, 3, iRow, (u"%d%%" % ourReligionPercent), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
					else:
						screen.setTableText(szTable, 2, iRow, activePlayer.getTeam().getName() + ":", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
						screen.setTableText(szTable, 3, iRow, u"No Holy City", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
					if (iBestReligion != -1):
						screen.setTableText(szTable, 4, iRow, gc.getReligionInfo(iBestReligion).getDescription() + ":", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
						screen.setTableText(szTable, 5, iRow, (u"%d%%" % religionPercent), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
					bEntriesFound = True
				
				if (victory.getTotalCultureRatio() > 0):			
					iRow = screen.appendTableRow(szTable)
					screen.setTableText(szTable, 0, iRow, localText.getText("TXT_KEY_VICTORY_SCREEN_PERCENT_CULTURE", (int((100.0 * bestCulture) / victory.getTotalCultureRatio()), )), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
					screen.setTableText(szTable, 2, iRow, activePlayer.getTeam().getName() + ":", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
					screen.setTableText(szTable, 3, iRow, unicode(ourCulture), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
					if (iBestLandTeam != -1):
						screen.setTableText(szTable, 4, iRow, gc.getTeam(iBestCultureTeam).getName() + ":", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
						screen.setTableText(szTable, 5, iRow, unicode(bestCulture), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
					bEntriesFound = True

				iBestBuildingTeam = -1
				bestBuilding = 0
				for iLoopTeam in range(gc.getMAX_CIV_TEAMS()):
					if (gc.getTeam(iLoopTeam).isAlive() and not gc.getTeam(iLoopTeam).isMinorCiv() and not gc.getTeam(iLoopTeam).isBarbarian()):
						if (iLoopTeam != iActiveTeam and (activePlayer.getTeam().isHasMet(iLoopTeam) or gc.getGame().isDebugMode())):
							teamBuilding = 0
							for i in range(gc.getNumBuildingClassInfos()):
								if (gc.getBuildingClassInfo(i).getVictoryThreshold(iLoopVC) > 0):					
									teamBuilding += gc.getTeam(iLoopTeam).getBuildingClassCount(i)
							if (teamBuilding > bestBuilding):
								bestBuilding = teamBuilding
								iBestBuildingTeam = iLoopTeam	
											
				for i in range(gc.getNumBuildingClassInfos()):
					if (gc.getBuildingClassInfo(i).getVictoryThreshold(iLoopVC) > 0):
						iRow = screen.appendTableRow(szTable)
						szNumber = unicode(gc.getBuildingClassInfo(i).getVictoryThreshold(iLoopVC))
						screen.setTableText(szTable, 0, iRow, localText.getText("TXT_KEY_VICTORY_SCREEN_BUILDING", (szNumber, gc.getBuildingClassInfo(i).getTextKey())), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
						screen.setTableText(szTable, 2, iRow, activePlayer.getTeam().getName() + ":", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
						screen.setTableText(szTable, 3, iRow, activePlayer.getTeam().getBuildingClassCount(i), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
						if (iBestBuildingTeam != -1):
							screen.setTableText(szTable, 4, iRow, gc.getTeam(iBestBuildingTeam).getName() + ":", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
							screen.setTableText(szTable, 5, iRow, gc.getTeam(iBestBuildingTeam).getBuildingClassCount(i), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
						bEntriesFound = True
						
				iBestProjectTeam = -1
				bestProject = 0
				for iLoopTeam in range(gc.getMAX_CIV_TEAMS()):
					if (gc.getTeam(iLoopTeam).isAlive() and not gc.getTeam(iLoopTeam).isMinorCiv() and not gc.getTeam(iLoopTeam).isBarbarian()):
						if (iLoopTeam != iActiveTeam and (activePlayer.getTeam().isHasMet(iLoopTeam) or gc.getGame().isDebugMode())):
							teamProject = 0
							for i in range(gc.getNumProjectInfos()):
								if (gc.getProjectInfo(i).getVictoryThreshold(iLoopVC) > 0):					
									teamProject += gc.getTeam(iLoopTeam).getProjectCount(i)
							if (teamProject > bestProject):
								bestProject = teamProject
								iBestProjectTeam = iLoopTeam

# BUG Additions Start
				bApolloShown = False
				for i in range(gc.getNumProjectInfos()):
					if (gc.getProjectInfo(i).getVictoryThreshold(iLoopVC) > 0):
						if not self.isApolloBuilt():
							iRow = screen.appendTableRow(szTable)
							screen.setTableText(szTable, 0, iRow, localText.getText("TXT_KEY_PROJECT_APOLLO_PROGRAM", ()), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
							screen.setTableText(szTable, 2, iRow, activePlayer.getTeam().getName() + ":", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
							screen.setTableText(szTable, 3, iRow, localText.getText("TXT_KEY_VICTORY_SCREEN_NOT_BUILT", ()), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
							bEntriesFound = True
							break
						else:
							if not bApolloShown:
								bApolloShown = True
								iRow = screen.appendTableRow(szTable)
								screen.setTableText(szTable, 0, iRow, localText.getText("TXT_KEY_PROJECT_APOLLO_PROGRAM", ()), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
								screen.setTableText(szTable, 2, iRow, localText.getText("TXT_KEY_VICTORY_SCREEN_BUILT", (activePlayer.getTeam().getName(), )), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
								if (iBestProjectTeam != -1):
									screen.setTableText(szTable, 4, iRow, localText.getText("TXT_KEY_VICTORY_SCREEN_BUILT", (gc.getTeam(iBestProjectTeam).getName(), )), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

							iRow = screen.appendTableRow(szTable)
							if (gc.getProjectInfo(i).getVictoryMinThreshold(iLoopVC) == gc.getProjectInfo(i).getVictoryThreshold(iLoopVC)):
								szNumber = unicode(gc.getProjectInfo(i).getVictoryThreshold(iLoopVC))
							else:
								szNumber = unicode(gc.getProjectInfo(i).getVictoryMinThreshold(iLoopVC)) + u"-" + unicode(gc.getProjectInfo(i).getVictoryThreshold(iLoopVC))

							iReqTech = gc.getProjectInfo(i).getTechPrereq()
							bHasTech = gc.getTeam(iActiveTeam).isHasTech(iReqTech)
							sSSPart = localText.getText("TXT_KEY_VICTORY_SCREEN_BUILDING", (szNumber, gc.getProjectInfo(i).getTextKey()))
							sSSPlayer = activePlayer.getTeam().getName() + ":"
							sSSCount = "%i (%i)" % (activePlayer.getTeam().getProjectCount(i), activePlayer.getTeam().getProjectMaking(i))

							iHasTechColor = -1
							iSSColor = 0
							if activePlayer.getTeam().getProjectCount(i) == gc.getProjectInfo(i).getVictoryThreshold(iLoopVC):
								iSSColor = ColorUtil.keyToType("COLOR_GREEN")
							elif activePlayer.getTeam().getProjectCount(i) >= gc.getProjectInfo(i).getVictoryMinThreshold(iLoopVC):
								iSSColor = ColorUtil.keyToType("COLOR_YELLOW")

							if iSSColor > 0:
								sSSPlayer = localText.changeTextColor(activePlayer.getTeam().getName() + ":", iSSColor)
								sSSCount = localText.changeTextColor(str(activePlayer.getTeam().getProjectCount(i)), iSSColor)

							screen.setTableText(szTable, 0, iRow, sSSPart, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
							screen.setTableText(szTable, 2, iRow, sSSPlayer, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
							if bHasTech:
								screen.setTableText(szTable, 3, iRow, sSSCount, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
							
# BUG Additions End
							if (gc.getProjectInfo(i).isSpaceship()):
								bSpaceshipFound = True
							
							if (iBestProjectTeam != -1):
								screen.setTableText(szTable, 4, iRow, gc.getTeam(iBestProjectTeam).getName() + ":", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
								screen.setTableText(szTable, 5, iRow, unicode(gc.getTeam(iBestProjectTeam).getProjectCount(i)), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
							bEntriesFound = True
						
				#add spaceship button
				if (bSpaceshipFound):
					screen.setButtonGFC("SpaceShipButton" + str(iLoopVC), localText.getText("TXT_KEY_GLOBELAYER_STRATEGY_VIEW", ()), "", 0, 0, 15, 10, WidgetTypes.WIDGET_GENERAL, self.SPACESHIP_SCREEN_BUTTON, -1, ButtonStyles.BUTTON_STYLE_STANDARD )
					screen.attachControlToTableCell("SpaceShipButton" + str(iLoopVC), szTable, iVictoryTitleRow, 1)
					
					victoryDelay = gc.getTeam(iActiveTeam).getVictoryCountdown(iLoopVC)
					if((victoryDelay > 0) and (gc.getGame().getGameState() != GameStateTypes.GAMESTATE_EXTENDED)):
						victoryDate = CyGameTextMgr().getTimeStr(gc.getGame().getGameTurn() + victoryDelay, false)
						screen.setTableText(szTable, 2, iVictoryTitleRow, localText.getText("TXT_KEY_SPACE_SHIP_SCREEN_ARRIVAL", ()) + ":", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
						screen.setTableText(szTable, 3, iVictoryTitleRow, victoryDate, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
						screen.setTableText(szTable, 4, iVictoryTitleRow, localText.getText("TXT_KEY_REPLAY_SCREEN_TURNS", ()) + ":", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
						screen.setTableText(szTable, 5, iVictoryTitleRow, str(victoryDelay), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
						
				if (victory.isDiploVote()):
					for (iVoteBuildingClass, iUNTeam, bUnknown) in aiVoteBuildingClass:
						iRow = screen.appendTableRow(szTable)
						screen.setTableText(szTable, 0, iRow, localText.getText("TXT_KEY_VICTORY_SCREEN_ELECTION", (gc.getBuildingClassInfo(iVoteBuildingClass).getTextKey(), )), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
						if (iUNTeam != -1):
							if bUnknown:
								szName = localText.getText("TXT_KEY_TOPCIVS_UNKNOWN", ())
							else:
								szName = gc.getTeam(iUNTeam).getName()
							screen.setTableText(szTable, 2, iRow, localText.getText("TXT_KEY_VICTORY_SCREEN_BUILT", (szName, )), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
						else:
							screen.setTableText(szTable, 2, iRow, localText.getText("TXT_KEY_VICTORY_SCREEN_NOT_BUILT", ()), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
						bEntriesFound = True
					
				if (victory.getCityCulture() != CultureLevelTypes.NO_CULTURELEVEL and victory.getNumCultureCities() > 0):
					ourBestCities = self.getListCultureCities(self.iActivePlayer, victory)[0:victory.getNumCultureCities()]
					
					iBestCulturePlayer = -1
					bestCityCulture = 0
					maxCityCulture = gc.getCultureLevelInfo(victory.getCityCulture()).getSpeedThreshold(gc.getGame().getGameSpeedType())
					for iLoopPlayer in range(gc.getMAX_PLAYERS()):
						if (gc.getPlayer(iLoopPlayer).isAlive() and not gc.getPlayer(iLoopPlayer).isMinorCiv() and not gc.getPlayer(iLoopPlayer).isBarbarian()):
							if (iLoopPlayer != self.iActivePlayer and (activePlayer.getTeam().isHasMet(gc.getPlayer(iLoopPlayer).getTeam()) or gc.getGame().isDebugMode())):
								theirBestCities = self.getListCultureCities(iLoopPlayer, victory)[0:victory.getNumCultureCities()]
								
								iTotalCulture = 0
								for loopCity in theirBestCities:
									if loopCity[0] >= maxCityCulture:
										iTotalCulture += maxCityCulture
									else:
										iTotalCulture += loopCity[0]
								
								if (iTotalCulture >= bestCityCulture):
									bestCityCulture = iTotalCulture
									iBestCulturePlayer = iLoopPlayer

					if (iBestCulturePlayer != -1):
						theirBestCities = self.getListCultureCities(iBestCulturePlayer, victory)[0:(victory.getNumCultureCities())]
					else:
						theirBestCities = []
						
					iRow = screen.appendTableRow(szTable)
					screen.setTableText(szTable, 0, iRow, localText.getText("TXT_KEY_VICTORY_SCREEN_CITY_CULTURE", (victory.getNumCultureCities(), gc.getCultureLevelInfo(victory.getCityCulture()).getTextKey())), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

					for i in range(victory.getNumCultureCities()):
						if (len(ourBestCities) > i):
							screen.setTableText(szTable, 2, iRow, ourBestCities[i][1].getName() + ":", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
# BUG Additions Start
							if ourBestCities[i][2] == -1:
								sString = "%i (-)" % (ourBestCities[i][0])
							elif ourBestCities[i][2] > 100:
								sString = "%i (100+)" % (ourBestCities[i][0])
							elif ourBestCities[i][2] < 1:
								sString = "%i (L)" % (ourBestCities[i][0])
							else:
								sString = "%i (%i)" % (ourBestCities[i][0], ourBestCities[i][2])
							screen.setTableText(szTable, 3, iRow, sString, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
# BUG Additions End

						if (len(theirBestCities) > i):
							screen.setTableText(szTable, 4, iRow, theirBestCities[i][1].getName() + ":", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

# BUG Additions Start
							if theirBestCities[i][2] == -1:
								sString = "%i (-)" % (theirBestCities[i][0])
							elif theirBestCities[i][2] > 100:
								sString = "%i (100+)" % (theirBestCities[i][0])
							elif theirBestCities[i][2] < 1:
								sString = "%i (L)" % (theirBestCities[i][0])
							else:
								sString = "%i (%i)" % (theirBestCities[i][0], theirBestCities[i][2])
							screen.setTableText(szTable, 5, iRow, sString, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
# BUG Additions End

						if (i < victory.getNumCultureCities()-1):
							iRow = screen.appendTableRow(szTable)
					bEntriesFound = True
					
				if (bEntriesFound):
					screen.appendTableRow(szTable)
					screen.appendTableRow(szTable)

		# civ picker dropdown
		if (CyGame().isDebugMode()):
			self.szDropdownName = self.DEBUG_DROPDOWN_ID
			screen.addDropDownBoxGFC(self.szDropdownName, 22, 12, 300, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
			for j in range(gc.getMAX_PLAYERS()):
				if (gc.getPlayer(j).isAlive()):
					screen.addPullDownString(self.szDropdownName, gc.getPlayer(j).getName(), j, j, False )
		
		self.drawTabs()

# BUG Additions Start
#	def getListCultureCities(self, iPlayer):
	def getListCultureCities(self, iPlayer, victory):
		maxCityCulture = gc.getCultureLevelInfo(victory.getCityCulture()).getSpeedThreshold(gc.getGame().getGameSpeedType())
# BUG Additions End

		if iPlayer >= 0:
			player = PyPlayer(iPlayer)
			if player.isAlive():
				cityList = player.getCityList()
# BUG Additions Start
#				listCultureCities = len(cityList) * [(0, 0)]
				listCultureCities = len(cityList) * [(0, 0, 0)]
# BUG Additions End
				i = 0
				for city in cityList:
# BUG Additions Start
					pCity = city.GetCy()
					iRate = pCity.getCommerceRateTimes100(CommerceTypes.COMMERCE_CULTURE)
					if iRate == 0:
						iTurns = -1
					else:
						iCultureLeftTimes100 = 100 * maxCityCulture - pCity.getCultureTimes100(city.getOwner())
						iTurns = int((iCultureLeftTimes100 + iRate - 1) / iRate)
					listCultureCities[i] = (city.getCulture(), city, iTurns)
#					listCultureCities[i] = (city.getCulture(), city)
# BUG Additions Start
					i += 1
				listCultureCities.sort()
				listCultureCities.reverse()
				return listCultureCities
		return []					

# BUG Additions Start
	def getVotesForWhichCandidate(self, iPlayer, iCand1, iCand2):
		# returns are 1 = vote for candidate 1
		#             2 = vote for candidate 2
		#            -1 = abstain

		# * AI votes for itself if it can
		# * AI votes for a team member if it can
		# * AI votes for its master, if it is a vassal
		# * if the AI attitude to one of the candidates is 'friendly' and the other is 'pleased' or less, AI votes for 'friend'
		# * if both candidates are at 'friendly' status, votes for one with highest attitude
		# * if neither candidate is at 'friendly', abstains

		# * AI votes for itself if it can
		if iPlayer == iCand1:
			return 1
		if iPlayer == iCand2:
			return 2

		# if player is human, votes for self or abstains
		if iPlayer == self.iActivePlayer:
			return -1

		iPTeam = gc.getPlayer(iPlayer).getTeam()
		iC1Team = gc.getPlayer(iCand1).getTeam()
		iC2Team = gc.getPlayer(iCand2).getTeam()

		# * AI votes for a team member if it can
		# * AI votes for its master, if it is a vassal
		if (gc.getTeam(iC1Team).isVassal(iPTeam)
		or  iC1Team == iPTeam):
			return 1

		if (gc.getTeam(iC2Team).isVassal(iPTeam)
		or  iC2Team == iPTeam):
			return 2

		# get player category (friendly) to candidates
		iC1Cat = AttitudeUtils.getAttitudeCategory(iPlayer, iCand1)
		iC2Cat = AttitudeUtils.getAttitudeCategory(iPlayer, iCand2)

		# * if neither candidate is at 'friendly', abstains
		# assumes friendly = 4, pleased = 3, etc
		if (iC1Cat < 4
		and iC2Cat < 4):
			return -1

		# * if the AI attitude to one of the candidates is 'friendly' and the other is 'pleased' or less, AI votes for 'friend'
		if (iC1Cat == 4
		and iC2Cat < 4):
			return 1

		if (iC1Cat < 4
		and iC2Cat == 4):
			return 2

		# get player attitude to candidates
		iC1Att = AttitudeUtils.getAttitudeCount(iPlayer, iCand1)
		iC2Att = AttitudeUtils.getAttitudeCount(iPlayer, iCand2)

		# * if both candidates are at 'friendly' status, votes for one with highest attitude
		if iC2Att > iC1Att: # ties go to Candidate #1
			return 1
		else:
			return 2

		return -1

	def canBuildSSComponent(self, vTeam, vComponent):
		if(not vTeam.isHasTech(vComponent.getTechPrereq())):
			return False
		else:
			for j in range(gc.getNumProjectInfos()):
				if(vTeam.getProjectCount(j) < vComponent.getProjectsNeeded(j)):
					return False
		return True

	def isApolloBuilt(self):
		activePlayer = gc.getPlayer(self.iActivePlayer)
		iActiveTeam = activePlayer.getTeam()

		# check if anyone has built the apollo project (PROJECT_APOLLO_PROGRAM)
		for iLoopTeam in range(gc.getMAX_CIV_TEAMS()):
			pLoopTeam = gc.getTeam(iLoopTeam)
			if (pLoopTeam.isAlive()
			and not pLoopTeam.isMinorCiv()
			and not pLoopTeam.isBarbarian()):
				if iLoopTeam == iActiveTeam:
					bContact = True
				elif (gc.getTeam(iActiveTeam).isHasMet(iLoopTeam)
				or gc.getGame().isDebugMode()):
					bContact = True
				else:
					bContact = False

				if bContact:
					if self.isApolloBuiltbyTeam(pLoopTeam):
						return True
		return False

	def isApolloBuiltbyTeam(self, vTeam):
		for i in range(gc.getNumProjectInfos()):
			component = gc.getProjectInfo(i)
			if (component.isSpaceship()):
				bApollo = True
				for j in range(gc.getNumProjectInfos()):
					if(vTeam.getProjectCount(j) < component.getProjectsNeeded(j)):
						bApollo = False
				if bApollo:
					return True
				break

		return False
# BUG Additions End

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

																				
	# handle the input for this screen...
	def handleInput (self, inputClass):
		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_LISTBOX_ITEM_SELECTED):
			if (inputClass.getFunctionName() == self.DEBUG_DROPDOWN_ID):
				szName = self.DEBUG_DROPDOWN_ID
				iIndex = self.getScreen().getSelectedPullDownID(szName)
				self.iActivePlayer = self.getScreen().getPullDownData(szName, iIndex)
				self.iScreen = VICTORY_CONDITION_SCREEN
				self.showVictoryConditionScreen()				
		elif (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED):
			if (inputClass.getFunctionName() == self.VC_TAB_ID):
				self.iScreen = VICTORY_CONDITION_SCREEN
				self.showVictoryConditionScreen()				
			elif (inputClass.getFunctionName() == self.SETTINGS_TAB_ID):
				self.iScreen = GAME_SETTINGS_SCREEN
				self.showGameSettingsScreen()
			elif (inputClass.getFunctionName() == self.UN_RESOLUTION_TAB_ID):
				self.iScreen = UN_RESOLUTION_SCREEN
				self.showVotingScreen()
			elif (inputClass.getFunctionName() == self.UN_MEMBERS_TAB_ID):
				self.iScreen = UN_MEMBERS_SCREEN
				self.showMembersScreen()
			elif (inputClass.getData1() == self.SPACESHIP_SCREEN_BUTTON):
				#close screen
				screen = self.getScreen()
				screen.setDying(True)
				CyInterface().clearSelectedCities()
				
				#popup spaceship screen
				popupInfo = CyPopupInfo()
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON_SCREEN)
				popupInfo.setData1(-1)
				popupInfo.setText(u"showSpaceShip")
				popupInfo.addPopup(self.iActivePlayer)

	def update(self, fDelta):
		return
