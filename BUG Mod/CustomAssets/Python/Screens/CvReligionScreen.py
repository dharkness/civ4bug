## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
from CvPythonExtensions import *
import PyHelpers
import CvUtil
import ScreenInput
import CvScreenEnums

#BUG: Change Graphs - start
import BugUtil
import BugCore
AdvisorOpt = BugCore.game.Advisors
#BUG: Change Graphs - end

PyPlayer = PyHelpers.PyPlayer

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

class CvReligionScreen:
	"Religion Advisor Screen"

	def __init__(self):

		self.SCREEN_NAME = "ReligionScreen"
		self.BUTTON_NAME = "ReligionScreenButton"
		self.RELIGION_NAME = "ReligionText"
		self.CONVERT_NAME = "ReligionConvertButton"
		self.CANCEL_NAME = "ReligionCancelButton"
		self.CITY_NAME = "ReligionCity"
		self.HEADER_NAME = "ReligionScreenHeader"
		self.DEBUG_DROPDOWN_ID =  "ReligionDropdownWidget"
		self.TABLE_ID =  "ReligionTableWidget"
		self.AREA1_ID =  "ReligionAreaWidget1"
		self.AREA2_ID =  "ReligionAreaWidget2"
		self.BACKGROUND_ID = "ReligionBackground"
		self.RELIGION_PANEL_ID = "ReligionPanel"
		self.RELIGION_ANARCHY_WIDGET = "ReligionAnarchyWidget"

		self.BORDER_WIDTH = 2
		self.BUTTON_SIZE = 48
		self.HIGHLIGHT_EXTRA_SIZE = 4

		self.X_SCREEN = 500
		self.Y_SCREEN = 396
		self.W_SCREEN = 1024
		self.H_SCREEN = 768
		self.Z_SCREEN = -6.1

		self.Y_TITLE = 8
		self.Z_TEXT = self.Z_SCREEN - 0.2
		self.DZ = -0.2
		self.Z_CONTROLS = self.Z_TEXT

		self.X_EXIT = 994
		self.Y_EXIT = 726

		self.X_CANCEL = 552
		self.Y_CANCEL = 726

		self.X_ANARCHY = 21
		self.Y_ANARCHY = 726

		self.LEFT_EDGE_TEXT = 10
		self.X_RELIGION_START = 180
		self.DX_RELIGION = 98
		self.Y_RELIGION = 35
		self.Y_FOUNDED = 90
		self.Y_HOLY_CITY = 115
		self.Y_INFLUENCE = 140
		self.Y_RELIGION_NAME = 58

		self.X_RELIGION_AREA = 45
		self.Y_RELIGION_AREA = 84
		self.W_RELIGION_AREA = 934
		self.H_RELIGION_AREA = 175

		self.X_CITY1_AREA = 45
		self.X_CITY2_AREA = 522
		self.Y_CITY_AREA = 282
		self.W_CITY_AREA = 457
		self.H_CITY_AREA = 395

		self.X_CITY = 10
		self.DY_CITY = 38

		self.iReligionExamined = -1
		self.iReligionSelected = -1
		self.iReligionOriginal = -1
		self.iActivePlayer = -1

		self.bScreenUp = False

		self.ReligionScreenInputMap = {
			self.RELIGION_NAME		: self.ReligionScreenButton,
			self.BUTTON_NAME		: self.ReligionScreenButton,
			self.CONVERT_NAME		: self.ReligionConvert,
			self.CANCEL_NAME		: self.ReligionCancel,
			}

		# BUG Constants
		self.bBUGConstants = False

	def getScreen(self):
		return CyGInterfaceScreen(self.SCREEN_NAME, CvScreenEnums.RELIGION_SCREEN)

	def interfaceScreen (self):

		self.SCREEN_ART = ArtFileMgr.getInterfaceArtInfo("TECH_BG").getPath()
		self.NO_STATE_BUTTON_ART = ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_CANCEL").getPath()
		self.EXIT_TEXT = u"<font=4>" + localText.getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + "</font>"
		self.CONVERT_TEXT = u"<font=4>" + localText.getText("TXT_KEY_RELIGION_CONVERT", ()).upper() + "</font>"
		self.CANCEL_TEXT = u"<font=4>" + localText.getText("TXT_KEY_SCREEN_CANCEL", ()).upper() + "</font>"

		self.iActivePlayer = gc.getGame().getActivePlayer()

		self.bScreenUp = True

		screen = self.getScreen()
		if screen.isActive():
			return
		screen.setRenderInterfaceOnly(True);
		screen.showScreen( PopupStates.POPUPSTATE_IMMEDIATE, False)

		# Set the background and exit button, and show the screen
		screen.setDimensions(screen.centerX(0), screen.centerY(0), self.W_SCREEN, self.H_SCREEN)

		screen.addDDSGFC(self.BACKGROUND_ID, ArtFileMgr.getInterfaceArtInfo("MAINMENU_SLIDESHOW_LOAD").getPath(), 0, 0, self.W_SCREEN, self.H_SCREEN, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addPanel( "TechTopPanel", u"", u"", True, False, 0, 0, self.W_SCREEN, 55, PanelStyles.PANEL_STYLE_TOPBAR )
		screen.addPanel( "TechBottomPanel", u"", u"", True, False, 0, 713, self.W_SCREEN, 55, PanelStyles.PANEL_STYLE_BOTTOMBAR )
		screen.setText(self.CANCEL_NAME, "Background", self.CANCEL_TEXT, CvUtil.FONT_CENTER_JUSTIFY, self.X_CANCEL, self.Y_CANCEL, self.Z_TEXT, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, 1, 0)

		screen.showWindowBackground(False)

		# Header...
		screen.setLabel(self.HEADER_NAME, "Background", u"<font=4b>" + localText.getText("TXT_KEY_RELIGION_SCREEN_TITLE", ()).upper() + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_SCREEN, self.Y_TITLE, self.Z_TEXT, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		# Make the scrollable areas for the city list...

		if (CyGame().isDebugMode()):
			self.szDropdownName = self.DEBUG_DROPDOWN_ID
			screen.addDropDownBoxGFC(self.szDropdownName, 22, 12, 300, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
			for j in range(gc.getMAX_PLAYERS()):
				if (gc.getPlayer(j).isAlive()):
					screen.addPullDownString(self.szDropdownName, gc.getPlayer(j).getName(), j, j, False )

		# Draw Religion info
		self.drawReligionInfo()

		self.drawCityInfo(self.iReligionSelected)

	# Draws the religion buttons and information
	def drawReligionInfo(self):

		screen = self.getScreen()

		# Put everything on a scrollable area
		szArea = self.RELIGION_PANEL_ID
		if AdvisorOpt.isReligious():
			screen.addPanel(szArea, "", "", False, True, self.X_RELIGION_AREA, self.Y_RELIGION_AREA, self.W_RELIGION_AREA, self.H_RELIGION_AREA + 40, PanelStyles.PANEL_STYLE_MAIN)
		else:
			screen.addPanel(szArea, "", "", False, True, self.X_RELIGION_AREA, self.Y_RELIGION_AREA, self.W_RELIGION_AREA, self.H_RELIGION_AREA, PanelStyles.PANEL_STYLE_MAIN)

		# Religion buttons at the top
		xLoop = self.X_RELIGION_START
		for i in range(gc.getNumReligionInfos()):
			szButtonName = self.getReligionButtonName(i)
			if gc.getGame().getReligionGameTurnFounded(i) >= 0:
				screen.addCheckBoxGFC(szButtonName, gc.getReligionInfo(i).getButton(), ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(), self.X_RELIGION_AREA + xLoop - self.BUTTON_SIZE/2, self.Y_RELIGION_AREA + self.Y_RELIGION - self.BUTTON_SIZE/2, self.BUTTON_SIZE, self.BUTTON_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1, ButtonStyles.BUTTON_STYLE_LABEL)
			else:
				screen.setImageButton(szButtonName, gc.getReligionInfo(i).getButtonDisabled(), self.X_RELIGION_AREA + xLoop - self.BUTTON_SIZE/2, self.Y_RELIGION_AREA + self.Y_RELIGION - self.BUTTON_SIZE/2, self.BUTTON_SIZE, self.BUTTON_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1)
			szName = self.getReligionTextName(i)
			szLabel = gc.getReligionInfo(i).getDescription()
#			if (self.iReligionSelected == i):
#				szLabel = localText.changeTextColor(szLabel, gc.getInfoTypeForString("COLOR_YELLOW"))
			screen.setText(szName, szArea, szLabel, CvUtil.FONT_CENTER_JUSTIFY, xLoop + self.X_RELIGION_AREA, self.Y_RELIGION_AREA + self.Y_RELIGION_NAME, 2*self.DZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			xLoop += self.DX_RELIGION

		szButtonName = self.getReligionButtonName(gc.getNumReligionInfos())
		screen.addCheckBoxGFC(szButtonName, self.NO_STATE_BUTTON_ART, ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(), self.X_RELIGION_AREA + xLoop - self.BUTTON_SIZE/2, self.Y_RELIGION_AREA + self.Y_RELIGION - self.BUTTON_SIZE/2, self.BUTTON_SIZE, self.BUTTON_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1, ButtonStyles.BUTTON_STYLE_LABEL)

		szName = self.getReligionTextName(gc.getNumReligionInfos())
		szLabel = localText.getText("TXT_KEY_RELIGION_SCREEN_NO_STATE", ())
#		if (self.iReligionSelected == gc.getNumReligionInfos()):
#			szLabel = localText.changeTextColor(szLabel, gc.getInfoTypeForString("COLOR_YELLOW"))
		screen.setText(szName, szArea, szLabel, CvUtil.FONT_CENTER_JUSTIFY, xLoop + self.X_RELIGION_AREA, self.Y_RELIGION_AREA + self.Y_RELIGION_NAME, 2*self.DZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)		

		# Founded...
		screen.setLabelAt("", szArea, localText.getText("TXT_KEY_RELIGION_SCREEN_DATE_FOUNDED", ()), CvUtil.FONT_LEFT_JUSTIFY, self.LEFT_EDGE_TEXT, self.Y_FOUNDED, self.DZ, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		# Date Founded:
		xLoop = self.X_RELIGION_START
		for i in range(gc.getNumReligionInfos()):
			if (gc.getGame().getReligionGameTurnFounded(i) < 0):
				szFounded = localText.getText("TXT_KEY_RELIGION_SCREEN_NOT_FOUNDED", ())
			else:
				szFounded = CyGameTextMgr().getTimeStr(gc.getGame().getReligionGameTurnFounded(i), false)
			screen.setLabelAt("", szArea, szFounded, CvUtil.FONT_CENTER_JUSTIFY, xLoop, self.Y_FOUNDED, self.DZ, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			xLoop += self.DX_RELIGION

		screen.setLabelAt("", szArea, "", CvUtil.FONT_CENTER_JUSTIFY, xLoop, self.Y_FOUNDED, self.DZ, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		# Holy City...
		screen.setLabelAt("", szArea, localText.getText("TXT_KEY_RELIGION_SCREEN_HOLY_CITY", ()), CvUtil.FONT_LEFT_JUSTIFY, self.LEFT_EDGE_TEXT, self.Y_HOLY_CITY, self.DZ, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		xLoop = self.X_RELIGION_START
		for i in range(gc.getNumReligionInfos()):
			pHolyCity = gc.getGame().getHolyCity(i)
			if pHolyCity.isNone():
				szFounded = localText.getText("TXT_KEY_NONE", ())
				screen.setLabelAt("", szArea, szFounded, CvUtil.FONT_CENTER_JUSTIFY, xLoop, self.Y_HOLY_CITY, self.DZ, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			elif not pHolyCity.isRevealed(gc.getPlayer(self.iActivePlayer).getTeam(), False):
				szFounded = localText.getText("TXT_KEY_UNKNOWN", ())
				screen.setLabelAt("", szArea, szFounded, CvUtil.FONT_CENTER_JUSTIFY, xLoop, self.Y_HOLY_CITY, self.DZ, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			else:
				szFounded = pHolyCity.getName()
				screen.setLabelAt("", szArea, "(%s)" % gc.getPlayer(pHolyCity.getOwner()).getCivilizationAdjective(0), CvUtil.FONT_CENTER_JUSTIFY, xLoop, self.Y_HOLY_CITY+8, self.DZ, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				screen.setLabelAt("", szArea, szFounded, CvUtil.FONT_CENTER_JUSTIFY, xLoop, self.Y_HOLY_CITY-8, self.DZ, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			xLoop += self.DX_RELIGION

		szFounded = "-"
		screen.setLabelAt("", szArea, szFounded, CvUtil.FONT_CENTER_JUSTIFY, xLoop, self.Y_HOLY_CITY, self.DZ, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		# Influence...
		screen.setLabelAt("", szArea, localText.getText("TXT_KEY_RELIGION_SCREEN_INFLUENCE", ()), CvUtil.FONT_LEFT_JUSTIFY, self.LEFT_EDGE_TEXT, self.Y_INFLUENCE, self.DZ, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		xLoop = self.X_RELIGION_START
		for i in range(gc.getNumReligionInfos()):
			if (gc.getGame().getReligionGameTurnFounded(i) < 0):
				szFounded = "0%"
			else:
				szFounded = str(gc.getGame().calculateReligionPercent(i)) + "%"
			screen.setLabelAt("", szArea, szFounded, CvUtil.FONT_CENTER_JUSTIFY, xLoop, self.Y_INFLUENCE, self.DZ, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			xLoop += self.DX_RELIGION

		szFounded = "-"
		screen.setLabelAt("", szArea, szFounded, CvUtil.FONT_CENTER_JUSTIFY, xLoop, self.Y_INFLUENCE, self.DZ, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		if AdvisorOpt.isReligious():
			# Count the number of temples and monastery
			self.BUGConstants()
			iPlayer = PyPlayer(self.iActivePlayer)
			cityList = iPlayer.getCityList()
			iTemple = [0,0,0,0,0,0,0]
			iMonastery = [0,0,0,0,0,0,0]

			for iCity in range(len(cityList)):
				pLoopCity = cityList[iCity]

				for iRel in range(gc.getNumReligionInfos()):
					iBldg = 77 + iRel * 4  # temple
					if self.calculateBuilding(pLoopCity, iBldg) == self.objectHave:
						iTemple[iRel] += 1

					iBldg = 77 + iRel * 4 + 2  # monastery
					if self.calculateBuilding(pLoopCity, iBldg) == self.objectHave:
						iMonastery[iRel] += 1

			# number of temples...
			screen.setLabelAt("", szArea, localText.getText("TXT_KEY_BUG_BUILDING_TEMPLE", ()), CvUtil.FONT_LEFT_JUSTIFY, self.LEFT_EDGE_TEXT, self.Y_INFLUENCE + 20, self.DZ, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

			xLoop = self.X_RELIGION_START
			for i in range(gc.getNumReligionInfos()):
				szFounded = "%i" % (iTemple[i])
				screen.setLabelAt("", szArea, szFounded, CvUtil.FONT_CENTER_JUSTIFY, xLoop, self.Y_INFLUENCE + 20, self.DZ, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				xLoop += self.DX_RELIGION

			# number of monasteries...
			screen.setLabelAt("", szArea, localText.getText("TXT_KEY_BUG_BUILDING_MONASTARY", ()), CvUtil.FONT_LEFT_JUSTIFY, self.LEFT_EDGE_TEXT, self.Y_INFLUENCE + 40, self.DZ, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

			xLoop = self.X_RELIGION_START
			for i in range(gc.getNumReligionInfos()):
				szFounded = "%i" % (iMonastery[i])
				screen.setLabelAt("", szArea, szFounded, CvUtil.FONT_CENTER_JUSTIFY, xLoop, self.Y_INFLUENCE + 40, self.DZ, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				xLoop += self.DX_RELIGION

		self.iReligionSelected = gc.getPlayer(self.iActivePlayer).getStateReligion()
		if (self.iReligionSelected == -1):
			self.iReligionSelected = gc.getNumReligionInfos()
		self.iReligionExamined = self.iReligionSelected
		self.iReligionOriginal = self.iReligionSelected

	# BUG constants
	def BUGConstants(self):

		if self.bBUGConstants:
			return

		# BUG additions
		self.hammerIcon = u"%c" %(gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getChar())

		# Special symbols for building, wonder and project views
		self.objectIsPresent = "x"
		self.objectIsNotPresent = "-"
		self.objectCanBeBuild = "o"
		self.objectUnderConstruction = self.hammerIcon
		
		# add the colors dependant on the statuses
		self.objectHave = localText.changeTextColor (self.objectIsPresent, gc.getInfoTypeForString("COLOR_GREEN")) #"x"
		self.objectNotPossible = localText.changeTextColor (self.objectIsNotPresent, gc.getInfoTypeForString("COLOR_RED")) #"-"
		self.objectPossible = localText.changeTextColor (self.objectCanBeBuild, gc.getInfoTypeForString("COLOR_BLUE")) #"o"
		self.objectHaveObsolete = localText.changeTextColor (self.objectIsPresent, gc.getInfoTypeForString("COLOR_WHITE")) #"x"
		self.objectNotPossibleConcurrent = localText.changeTextColor (self.objectIsNotPresent, gc.getInfoTypeForString("COLOR_YELLOW")) #"-"
		self.objectPossibleConcurrent = localText.changeTextColor (self.objectCanBeBuild, gc.getInfoTypeForString("COLOR_YELLOW")) #"o"		

		self.szTempleIcon = u"<font=2>%c</font>" %(CyGame().getSymbolID(FontSymbols.RELIGION_CHAR))
		self.szMonastaryIcon = u"<font=2>%c</font>" %(gc.getCommerceInfo(CommerceTypes.COMMERCE_RESEARCH).getChar())
		self.szCathedralIcon = u"<font=2>%c</font>" %(gc.getCommerceInfo(CommerceTypes.COMMERCE_CULTURE).getChar())
		self.szShrineIcon = u"<font=2>%c</font>" %(gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getChar())

		self.bBUGConstants = True

	# Draws the city list
	def drawCityInfo(self, iReligion):

		if (not self.bScreenUp):
			return

		screen = self.getScreen()

		if (iReligion == gc.getNumReligionInfos()):
			iLinkReligion = -1
		else:
			iLinkReligion = iReligion

		if not AdvisorOpt.isReligious():
			screen.addPanel(self.AREA1_ID, "", "", True, True, self.X_CITY1_AREA, self.Y_CITY_AREA, self.W_CITY_AREA, self.H_CITY_AREA, PanelStyles.PANEL_STYLE_MAIN)
			screen.addPanel(self.AREA2_ID, "", "", True, True, self.X_CITY2_AREA, self.Y_CITY_AREA, self.W_CITY_AREA, self.H_CITY_AREA, PanelStyles.PANEL_STYLE_MAIN)

		szArea = self.RELIGION_PANEL_ID
		for i in range(gc.getNumReligionInfos()):
			if (self.iReligionSelected == i):
				screen.setState(self.getReligionButtonName(i), True)
			else:
				screen.setState(self.getReligionButtonName(i), False)

		if (self.iReligionSelected == gc.getNumReligionInfos()):
			screen.setState(self.getReligionButtonName(gc.getNumReligionInfos()), True)
		else:
			screen.setState(self.getReligionButtonName(gc.getNumReligionInfos()), False)

		iPlayer = PyPlayer(self.iActivePlayer)
		cityList = iPlayer.getCityList()

# start of BUG indent for new code
		if AdvisorOpt.isReligious():
			# create religion table
			screen.addTableControlGFC(self.TABLE_ID, 15, self.X_RELIGION_AREA, self.Y_RELIGION_AREA + self.H_RELIGION_AREA + 40 + 10, self.W_RELIGION_AREA, self.H_CITY_AREA,
						  True, True, 24,24, TableStyles.TABLE_STYLE_STANDARD)
			screen.enableSort(self.TABLE_ID)

			zoomArt = ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_CITYSELECTION").getPath()
			sCity = localText.getText("TXT_KEY_WONDER_CITY", ())

			screen.setTableColumnHeader(self.TABLE_ID, 0, "", 30)
			screen.setTableColumnHeader(self.TABLE_ID, 1, sCity, 115)

			for i in range(gc.getNumReligionInfos()):   # columns for religous icons
				szReligionIcon = u"<font=2>%c</font>" %(gc.getReligionInfo(i).getChar())
				screen.setTableColumnHeader(self.TABLE_ID, 2+i, szReligionIcon, 25)

			# columns for temples, monastaries, cathedral, shrine
			screen.setTableColumnHeader(self.TABLE_ID, 10, self.szTempleIcon, 30)
			screen.setTableColumnHeader(self.TABLE_ID, 11, self.szCathedralIcon, 30)
			screen.setTableColumnHeader(self.TABLE_ID, 12, self.szMonastaryIcon, 30)
			screen.setTableColumnHeader(self.TABLE_ID, 13, self.szShrineIcon, 30)

			# column for religious impact
			screen.setTableColumnHeader(self.TABLE_ID, 14, "", 400)

			# Loop through the cities
			for iCity in range(len(cityList)):
				pLoopCity = cityList[iCity]

				screen.appendTableRow(self.TABLE_ID)
				screen.setTableText(self.TABLE_ID, 0, iCity, "" , zoomArt, WidgetTypes.WIDGET_ZOOM_CITY, pLoopCity.getOwner(), pLoopCity.getID(), CvUtil.FONT_LEFT_JUSTIFY)
				screen.setTableText(self.TABLE_ID, 1, iCity, pLoopCity.getName(), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

				lHolyCity = pLoopCity.getHolyCity()
				lReligions = pLoopCity.getReligions()

				for i in range(gc.getNumReligionInfos()):
					szReligionIcon = ""
					if i in lHolyCity:
						szReligionIcon = u"<font=2>%c</font>" %(gc.getReligionInfo(i).getHolyCityChar())
					elif i in lReligions:
						szReligionIcon = u"<font=2>%c</font>" %(gc.getReligionInfo(i).getChar())

					screen.setTableText(self.TABLE_ID, 2+i, iCity, szReligionIcon, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)

				if iReligion != -1:
					# check for temples, cathedral, monastaries, shrine
					for i in range(4):
						iBldg = 77 + iReligion * 4 + i
						sBldg = self.calculateBuilding(pLoopCity, iBldg)
						screen.setTableText(self.TABLE_ID, 10+i, iCity, sBldg, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)

				if (iLinkReligion == -1):
					bFirst = True
					sHelp = ""
					for iI in range(len(lReligions)):
						szTempBuffer = CyGameTextMgr().getReligionHelpCity(lReligions[iI], pLoopCity.GetCy(), False, False, False, True)
						if (szTempBuffer):
							if (not bFirst):
								sHelp += u", "
							sHelp += szTempBuffer
							bFirst = False
				else:
					sHelp = CyGameTextMgr().getReligionHelpCity(iLinkReligion, pLoopCity.GetCy(), False, False, True, False)

				screen.setTableText(self.TABLE_ID, 14, iCity, sHelp, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

# start of BUG indent of original code
		else:
			# Loop through the cities
			szLeftCities = u""
			szRightCities = u""
			for i in range(len(cityList)):

				bFirstColumn = (i % 2 == 0)

				pLoopCity = cityList[i]

				# Constructing the City name...
				szCityName = u""
				if pLoopCity.isCapital():
					szCityName += u"%c" % CyGame().getSymbolID(FontSymbols.STAR_CHAR)

				lHolyCity = pLoopCity.getHolyCity()
				if lHolyCity:
					for iI in range(len(lHolyCity)):
						szCityName += u"%c" %(gc.getReligionInfo(lHolyCity[iI]).getHolyCityChar())

				lReligions = pLoopCity.getReligions()
				if lReligions:
					for iI in range(len(lReligions)):
						if lReligions[iI] not in lHolyCity:
							szCityName += u"%c" %(gc.getReligionInfo(lReligions[iI]).getChar())

				szCityName += pLoopCity.getName()[0:17] + "  "

				if (iLinkReligion == -1):
					bFirst = True
					for iI in range(len(lReligions)):
						szTempBuffer = CyGameTextMgr().getReligionHelpCity(lReligions[iI], pLoopCity.GetCy(), False, False, False, True)
						if (szTempBuffer):
							if (not bFirst):
								szCityName += u", "
							szCityName += szTempBuffer
							bFirst = False
				else:
					szCityName += CyGameTextMgr().getReligionHelpCity(iLinkReligion, pLoopCity.GetCy(), False, False, True, False)

				if bFirstColumn:
					szLeftCities += u"<font=3>" + szCityName + u"</font>\n"
				else:
					szRightCities += u"<font=3>" + szCityName + u"</font>\n"

			screen.addMultilineText("Child" + self.AREA1_ID, szLeftCities, self.X_CITY1_AREA+5, self.Y_CITY_AREA+5, self.W_CITY_AREA-10, self.H_CITY_AREA-10, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
			screen.addMultilineText("Child" + self.AREA2_ID, szRightCities, self.X_CITY2_AREA+5, self.Y_CITY_AREA+5, self.W_CITY_AREA-10, self.H_CITY_AREA-10, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
# end of BUG indent of original code

		# Convert Button....
		iLink = 0
		if (gc.getPlayer(self.iActivePlayer).canChangeReligion()):
			iLink = 1

		if (not self.canConvert(iLinkReligion) or iLinkReligion == self.iReligionOriginal):			
			screen.setText(self.CONVERT_NAME, "Background", self.EXIT_TEXT, CvUtil.FONT_RIGHT_JUSTIFY, self.X_EXIT, self.Y_EXIT, self.Z_TEXT, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, 1, 0)
			screen.hide(self.CANCEL_NAME)
			szAnarchyTime = CyGameTextMgr().setConvertHelp(self.iActivePlayer, iLinkReligion)
		else:
			screen.setText(self.CONVERT_NAME, "Background", self.CONVERT_TEXT, CvUtil.FONT_RIGHT_JUSTIFY, self.X_EXIT, self.Y_EXIT, self.Z_TEXT, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CONVERT, iLinkReligion, 1)
			screen.show(self.CANCEL_NAME)
			szAnarchyTime = localText.getText("TXT_KEY_ANARCHY_TURNS", (gc.getPlayer(self.iActivePlayer).getReligionAnarchyLength(), ))

		# Turns of Anarchy Text...
		screen.setLabel(self.RELIGION_ANARCHY_WIDGET, "Background", u"<font=3>" + szAnarchyTime + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_ANARCHY, self.Y_ANARCHY, self.Z_TEXT, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

	def getReligionButtonName(self, iReligion):
		szName = self.BUTTON_NAME + str(iReligion)
		return szName

	def getReligionTextName(self, iReligion):
		szName = self.RELIGION_NAME + str(iReligion)
		return szName

	def canConvert(self, iReligion):
		iCurrentReligion = gc.getPlayer(self.iActivePlayer).getStateReligion()
		if (iReligion == gc.getNumReligionInfos()):
			iConvertReligion = -1
		else:
			iConvertReligion = iReligion

		return (iConvertReligion != iCurrentReligion and gc.getPlayer(self.iActivePlayer).canConvert(iConvertReligion))		

	# Will handle the input for this screen...
	def handleInput (self, inputClass):
#		BugUtil.debugInput(inputClass)

		screen = self.getScreen()

		szWidgetName = inputClass.getFunctionName()
		szFullWidgetName = szWidgetName + str(inputClass.getID())
		code = inputClass.getNotifyCode()

		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_LISTBOX_ITEM_SELECTED
		and szWidgetName != self.TABLE_ID):
			screen = self.getScreen()
			iIndex = screen.getSelectedPullDownID(self.DEBUG_DROPDOWN_ID)
			self.iActivePlayer = screen.getPullDownData(self.DEBUG_DROPDOWN_ID, iIndex)
			self.drawReligionInfo()
			self.drawCityInfo(self.iReligionSelected)
			return 1

		# BUG Zoom to City
		elif (szWidgetName == self.TABLE_ID):
			if (inputClass.getMouseX() == 0):
				screen.hideScreen()
				pPlayer = gc.getPlayer(inputClass.getData1())
				pCity = pPlayer.getCity(inputClass.getData2())
#				CyCamera().JustLookAtPlot(pCity.plot())

				CyInterface().selectCity(pCity, true);

		elif (self.ReligionScreenInputMap.has_key(inputClass.getFunctionName())):
			'Calls function mapped in ReligionScreenInputMap'
			# only get from the map if it has the key

			# get bound function from map and call it
			self.ReligionScreenInputMap.get(inputClass.getFunctionName())(inputClass)
			return 1

		return 0

	def update(self, fDelta):
		return

	# Religion Button
	def ReligionScreenButton( self, inputClass ):	
		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED ) :
			if (inputClass.getID() == gc.getNumReligionInfos() or gc.getGame().getReligionGameTurnFounded(inputClass.getID()) >= 0) :
				self.iReligionSelected = inputClass.getID()
				self.iReligionExamined = self.iReligionSelected
				self.drawCityInfo(self.iReligionSelected)
		elif ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_ON ) :
			if ( inputClass.getID() == gc.getNumReligionInfos() or gc.getGame().getReligionGameTurnFounded(inputClass.getID()) >= 0) :
				self.iReligionExamined = inputClass.getID()
				self.drawCityInfo(self.iReligionExamined)
		elif ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_OFF ) :
			self.iReligionExamined = self.iReligionSelected
			self.drawCityInfo(self.iReligionSelected)
		return 0

	def ReligionConvert(self, inputClass):
		screen = self.getScreen()
		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED) :
			screen.hideScreen()

	def ReligionCancel(self, inputClass):
		screen = self.getScreen()
		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED) :
			self.iReligionSelected = self.iReligionOriginal
			if (-1 == self.iReligionSelected):
				self.iReligionSelected = gc.getNumReligionInfos()
			self.drawCityInfo(self.iReligionSelected)

	def calculateBuilding (self, city, bldg):
		if city.getNumBuilding(bldg) > 0:
			return self.objectHave
#			if city.getNumActiveBuilding(bldg) > 0:
#				return self.objectHave
#			else:
#				return self.objectHaveObsolete
		elif city.GetCy().getFirstBuildingOrder(bldg) != -1:
			return self.objectUnderConstruction
		elif city.GetCy().canConstruct(bldg, False, False, False):
			return self.objectPossible
		elif city.GetCy().canConstruct(bldg, True, False, False):
			return self.objectPossibleConcurrent
		else:
			return self.objectNotPossible

