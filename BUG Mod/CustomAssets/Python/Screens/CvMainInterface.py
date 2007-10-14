## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums
import CvEventInterface
import time
# BUG - Align Icons - start
import Scoreboard
# BUG - Align Icons - end

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

# BUG - Options - start
import BugNJAGCOptions
BugNJAGC = BugNJAGCOptions.getOptions()

import BugScoreOptions
BugScore = BugScoreOptions.getOptions()

import BugScreensOptions
BugScreens = BugScreensOptions.getOptions()

import BugCityScreenOptions
BugCityScreen = BugCityScreenOptions.getOptions()
# BUG - Options - end

# BUG - Reminders - start
import ReminderEventManager
# BUG - Reminders - end

g_NumEmphasizeInfos = 0
g_NumCityTabTypes = 0
g_NumHurryInfos = 0
g_NumUnitClassInfos = 0
g_NumBuildingClassInfos = 0
g_NumProjectInfos = 0
g_NumProcessInfos = 0
g_NumActionInfos = 0
g_eEndTurnButtonState = -1

MAX_SELECTED_TEXT = 5
MAX_DISPLAYABLE_BUILDINGS = 15
MAX_DISPLAYABLE_TRADE_ROUTES = 4
MAX_BONUS_ROWS = 10
MAX_CITIZEN_BUTTONS = 8

SELECTION_BUTTON_COLUMNS = 8
SELECTION_BUTTON_ROWS = 2
NUM_SELECTION_BUTTONS = SELECTION_BUTTON_ROWS * SELECTION_BUTTON_COLUMNS

g_iNumBuildingWidgets = MAX_DISPLAYABLE_BUILDINGS
g_iNumTradeRouteWidgets = MAX_DISPLAYABLE_TRADE_ROUTES

# END OF TURN BUTTON POSITIONS
######################
iEndOfTurnButtonSize = 32
iEndOfTurnPosX = 296 # distance from right
iEndOfTurnPosY = 147 # distance from bottom

# MINIMAP BUTTON POSITIONS
######################
iMinimapButtonsExtent = 228
iMinimapButtonsX = 227
iMinimapButtonsY_Regular = 160
iMinimapButtonsY_Minimal = 32
iMinimapButtonWidth = 24
iMinimapButtonHeight = 24

# Globe button
iGlobeButtonX = 48
iGlobeButtonY_Regular = 168
iGlobeButtonY_Minimal = 40
iGlobeToggleWidth = 48
iGlobeToggleHeight = 48

# GLOBE LAYER OPTION POSITIONING
######################
iGlobeLayerOptionsX  = 235
iGlobeLayerOptionsY_Regular  = 170# distance from bottom edge
iGlobeLayerOptionsY_Minimal  = 38 # distance from bottom edge
iGlobeLayerOptionsWidth = 400
iGlobeLayerOptionHeight = 24

# STACK BAR
#####################
iStackBarHeight = 27


# MULTI LIST
#####################
iMultiListXL = 318
iMultiListXR = 332


# TOP CENTER TITLE
#####################
iCityCenterRow1X = 398
iCityCenterRow1Y = 78
iCityCenterRow2X = 398
iCityCenterRow2Y = 104

iCityCenterRow1Xa = 347
iCityCenterRow2Xa = 482


g_iNumTradeRoutes = 0
g_iNumBuildings = 0
g_iNumLeftBonus = 0
g_iNumCenterBonus = 0
g_iNumRightBonus = 0

g_szTimeText = ""

# BUG - NJAGC - start
g_bShowTimeTextAlt = False
g_iTimeTextCounter = -1
# BUG - NJAGC - end

# BUG - Raw Commerce - start
g_bRawShowing = False
g_iYieldType = YieldTypes.YIELD_COMMERCE
# BUG - Raw Commerce - end

g_pSelectedUnit = 0


class CvMainInterface:
	"Main Interface Screen"
	
	def numPlotListButtons(self):
		return self.m_iNumPlotListButtons

	def interfaceScreen (self):

		# Global variables being set here
		global g_NumEmphasizeInfos
		global g_NumCityTabTypes
		global g_NumHurryInfos
		global g_NumUnitClassInfos
		global g_NumBuildingClassInfos
		global g_NumProjectInfos
		global g_NumProcessInfos
		global g_NumActionInfos
		
		global MAX_SELECTED_TEXT
		global MAX_DISPLAYABLE_BUILDINGS
		global MAX_DISPLAYABLE_TRADE_ROUTES
		global MAX_BONUS_ROWS
		global MAX_CITIZEN_BUTTONS
		
		if ( CyGame().isPitbossHost() ):
			return

		# This is the main interface screen, create it as such
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		screen.setForcedRedraw(True)

		# Find out our resolution
		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()
		self.m_iNumPlotListButtons = (xResolution - (iMultiListXL+iMultiListXR) - 68) / 34
		
		screen.setDimensions(0, 0, xResolution, yResolution)

		# Set up our global variables...
		g_NumEmphasizeInfos = gc.getNumEmphasizeInfos()
		g_NumCityTabTypes = CityTabTypes.NUM_CITYTAB_TYPES
		g_NumHurryInfos = gc.getNumHurryInfos()
		g_NumUnitClassInfos = gc.getNumUnitClassInfos()
		g_NumBuildingClassInfos = gc.getNumBuildingClassInfos()
		g_NumProjectInfos = gc.getNumProjectInfos()
		g_NumProcessInfos = gc.getNumProcessInfos()
		g_NumActionInfos = gc.getNumActionInfos()
		
		# Help Text Area
		screen.setHelpTextArea( 350, FontTypes.SMALL_FONT, 7, yResolution - 172, -0.1, False, "", True, False, CvUtil.FONT_LEFT_JUSTIFY, 150 )

		# Center Left
		screen.addPanel( "InterfaceCenterLeftBackgroundWidget", u"", u"", True, False, 0, 0, 258, yResolution-149, PanelStyles.PANEL_STYLE_STANDARD )
		screen.setStyle( "InterfaceCenterLeftBackgroundWidget", "Panel_City_Left_Style" )
		screen.hide( "InterfaceCenterLeftBackgroundWidget" )

		# Top Left
		screen.addPanel( "InterfaceTopLeftBackgroundWidget", u"", u"", True, False, 258, 0, xResolution - 516, yResolution-149, PanelStyles.PANEL_STYLE_STANDARD )
		screen.setStyle( "InterfaceTopLeftBackgroundWidget", "Panel_City_Top_Style" )
		screen.hide( "InterfaceTopLeftBackgroundWidget" )

		# Center Right
		screen.addPanel( "InterfaceCenterRightBackgroundWidget", u"", u"", True, False, xResolution - 258, 0, 258, yResolution-149, PanelStyles.PANEL_STYLE_STANDARD )
		screen.setStyle( "InterfaceCenterRightBackgroundWidget", "Panel_City_Right_Style" )
		screen.hide( "InterfaceCenterRightBackgroundWidget" )
		
		screen.addPanel( "CityScreenAdjustPanel", u"", u"", True, False, 10, 44, 238, 105, PanelStyles.PANEL_STYLE_STANDARD )
		screen.setStyle( "CityScreenAdjustPanel", "Panel_City_Info_Style" )
		screen.hide( "CityScreenAdjustPanel" )
		
		screen.addPanel( "TopCityPanelLeft", u"", u"", True, False, 260, 70, xResolution/2-260, 60, PanelStyles.PANEL_STYLE_STANDARD )
		screen.setStyle( "TopCityPanelLeft", "Panel_City_TanTL_Style" )
		screen.hide( "TopCityPanelLeft" )
		
		screen.addPanel( "TopCityPanelRight", u"", u"", True, False, xResolution/2, 70, xResolution/2-260, 60, PanelStyles.PANEL_STYLE_STANDARD )
		screen.setStyle( "TopCityPanelRight", "Panel_City_TanTR_Style" )
		screen.hide( "TopCityPanelRight" )
		
		# Top Bar

		# SF CHANGE		
		screen.addPanel( "CityScreenTopWidget", u"", u"", True, False, 0, -2, xResolution, 41, PanelStyles.PANEL_STYLE_STANDARD )

		screen.setStyle( "CityScreenTopWidget", "Panel_TopBar_Style" )
		screen.hide( "CityScreenTopWidget" )
		
		# Top Center Title
		screen.addPanel( "CityNameBackground", u"", u"", True, False, 260, 31, xResolution - (260*2), 38, PanelStyles.PANEL_STYLE_STANDARD )
		screen.setStyle( "CityNameBackground", "Panel_City_Title_Style" )
		screen.hide( "CityNameBackground" )

		# Left Background Widget
		screen.addDDSGFC( "InterfaceLeftBackgroundWidget", ArtFileMgr.getInterfaceArtInfo("INTERFACE_BOTTOM_LEFT").getPath(), 0, yResolution - 164, 304, 164, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.hide( "InterfaceLeftBackgroundWidget" )

		# Center Background Widget
		screen.addPanel( "InterfaceCenterBackgroundWidget", u"", u"", True, False, 296, yResolution - 133, xResolution - (296*2), 133, PanelStyles.PANEL_STYLE_STANDARD)
		screen.setStyle( "InterfaceCenterBackgroundWidget", "Panel_Game_HudBC_Style" )
		screen.hide( "InterfaceCenterBackgroundWidget" )

		# Left Background Widget
		screen.addPanel( "InterfaceLeftBackgroundWidget", u"", u"", True, False, 0, yResolution - 168, 304, 168, PanelStyles.PANEL_STYLE_STANDARD)
		screen.setStyle( "InterfaceLeftBackgroundWidget", "Panel_Game_HudBL_Style" )
		screen.hide( "InterfaceLeftBackgroundWidget" )

		# Right Background Widget
		screen.addPanel( "InterfaceRightBackgroundWidget", u"", u"", True, False, xResolution - 304, yResolution - 168, 304, 168, PanelStyles.PANEL_STYLE_STANDARD)
		screen.setStyle( "InterfaceRightBackgroundWidget", "Panel_Game_HudBR_Style" )
		screen.hide( "InterfaceRightBackgroundWidget" )
	
		# Top Center Background

		# SF CHANGE
		screen.addPanel( "InterfaceTopCenter", u"", u"", True, False, 257, -2, xResolution-(257*2), 48, PanelStyles.PANEL_STYLE_STANDARD)

		screen.setStyle( "InterfaceTopCenter", "Panel_Game_HudTC_Style" )
		screen.hide( "InterfaceTopCenter" )

		# Top Left Background
		screen.addPanel( "InterfaceTopLeft", u"", u"", True, False, 0, -2, 267, 60, PanelStyles.PANEL_STYLE_STANDARD)
		screen.setStyle( "InterfaceTopLeft", "Panel_Game_HudTL_Style" )
		screen.hide( "InterfaceTopLeft" )

		# Top Right Background
		screen.addPanel( "InterfaceTopRight", u"", u"", True, False, xResolution - 267, -2, 267, 60, PanelStyles.PANEL_STYLE_STANDARD)
		screen.setStyle( "InterfaceTopRight", "Panel_Game_HudTR_Style" )
		screen.hide( "InterfaceTopRight" )

		iBtnWidth	= 28
		iBtnAdvance = 25
		iBtnY = 27
		iBtnX = 27
		
		# Turn log Button
		screen.setImageButton( "TurnLogButton", "", iBtnX, iBtnY - 2, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_TURN_LOG).getActionInfoIndex(), -1 )
		screen.setStyle( "TurnLogButton", "Button_HUDLog_Style" )
		screen.hide( "TurnLogButton" )
		
		iBtnX = xResolution - 277
		
		# Advisor Buttons...
		screen.setImageButton( "DomesticAdvisorButton", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_DOMESTIC_SCREEN).getActionInfoIndex(), -1 )
		screen.setStyle( "DomesticAdvisorButton", "Button_HUDAdvisorDomestic_Style" )
		screen.hide( "DomesticAdvisorButton" )

		iBtnX += iBtnAdvance
		screen.setImageButton( "FinanceAdvisorButton", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_FINANCIAL_SCREEN).getActionInfoIndex(), -1 )
		screen.setStyle( "FinanceAdvisorButton", "Button_HUDAdvisorFinance_Style" )
		screen.hide( "FinanceAdvisorButton" )
		
		iBtnX += iBtnAdvance
		screen.setImageButton( "CivicsAdvisorButton", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_CIVICS_SCREEN).getActionInfoIndex(), -1 )
		screen.setStyle( "CivicsAdvisorButton", "Button_HUDAdvisorCivics_Style" )
		screen.hide( "CivicsAdvisorButton" )
		
		iBtnX += iBtnAdvance 
		screen.setImageButton( "ForeignAdvisorButton", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_FOREIGN_SCREEN).getActionInfoIndex(), -1 )
		screen.setStyle( "ForeignAdvisorButton", "Button_HUDAdvisorForeign_Style" )
		screen.hide( "ForeignAdvisorButton" )
		
		iBtnX += iBtnAdvance
		screen.setImageButton( "MilitaryAdvisorButton", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_MILITARY_SCREEN).getActionInfoIndex(), -1 )
		screen.setStyle( "MilitaryAdvisorButton", "Button_HUDAdvisorMilitary_Style" )
		screen.hide( "MilitaryAdvisorButton" )
		
		iBtnX += iBtnAdvance
		screen.setImageButton( "TechAdvisorButton", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_TECH_CHOOSER).getActionInfoIndex(), -1 )
		screen.setStyle( "TechAdvisorButton", "Button_HUDAdvisorTechnology_Style" )
		screen.hide( "TechAdvisorButton" )

		iBtnX += iBtnAdvance
		screen.setImageButton( "ReligiousAdvisorButton", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_RELIGION_SCREEN).getActionInfoIndex(), -1 )
		screen.setStyle( "ReligiousAdvisorButton", "Button_HUDAdvisorReligious_Style" )
		screen.hide( "ReligiousAdvisorButton" )
		
		iBtnX += iBtnAdvance
		screen.setImageButton( "CorporationAdvisorButton", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_CORPORATION_SCREEN).getActionInfoIndex(), -1 )
		screen.setStyle( "CorporationAdvisorButton", "Button_HUDAdvisorCorporation_Style" )
		screen.hide( "CorporationAdvisorButton" )
		
		iBtnX += iBtnAdvance
		screen.setImageButton( "VictoryAdvisorButton", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_VICTORY_SCREEN).getActionInfoIndex(), -1 )
		screen.setStyle( "VictoryAdvisorButton", "Button_HUDAdvisorVictory_Style" )
		screen.hide( "VictoryAdvisorButton" )
		
		iBtnX += iBtnAdvance
		screen.setImageButton( "InfoAdvisorButton", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_INFO).getActionInfoIndex(), -1 )
		screen.setStyle( "InfoAdvisorButton", "Button_HUDAdvisorRecord_Style" )
		screen.hide( "InfoAdvisorButton" )

		iBtnX += iBtnAdvance
		screen.setImageButton( "EspionageAdvisorButton", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_ESPIONAGE_SCREEN).getActionInfoIndex(), -1 )
		screen.setStyle( "EspionageAdvisorButton", "Button_HUDAdvisorEspionage_Style" )
		screen.hide( "EspionageAdvisorButton" )
		
		# City Tabs
		iBtnX = xResolution - 324
		iBtnY = yResolution - 94
		iBtnWidth = 24
		iBtnAdvance = 24

		screen.setButtonGFC( "CityTab0", "", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_CITY_TAB, 0, -1, ButtonStyles.BUTTON_STYLE_STANDARD )
		screen.setStyle( "CityTab0", "Button_HUDJumpUnit_Style" )
		screen.hide( "CityTab0" )

		iBtnY += iBtnAdvance
		screen.setButtonGFC( "CityTab1", "", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_CITY_TAB, 1, -1, ButtonStyles.BUTTON_STYLE_STANDARD )
		screen.setStyle( "CityTab1", "Button_HUDJumpBuilding_Style" )
		screen.hide( "CityTab1" )
		
		iBtnY += iBtnAdvance
		screen.setButtonGFC( "CityTab2", "", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_CITY_TAB, 2, -1, ButtonStyles.BUTTON_STYLE_STANDARD )
		screen.setStyle( "CityTab2", "Button_HUDJumpWonder_Style" )
		screen.hide( "CityTab2" )
		
		# Minimap initialization
		screen.setMainInterface(True)
		
		screen.addPanel( "MiniMapPanel", u"", u"", True, False, xResolution - 214, yResolution - 151, 208, 151, PanelStyles.PANEL_STYLE_STANDARD )
		screen.setStyle( "MiniMapPanel", "Panel_Game_HudMap_Style" )
		screen.hide( "MiniMapPanel" )

		screen.initMinimap( xResolution - 210, xResolution - 9, yResolution - 131, yResolution - 9, -0.1 )
		gc.getMap().updateMinimapColor()

		self.createMinimapButtons()
	
		# Help button (always visible)
		screen.setImageButton( "InterfaceHelpButton", ArtFileMgr.getInterfaceArtInfo("INTERFACE_GENERAL_CIVILOPEDIA_ICON").getPath(), xResolution - 28, 2, 24, 24, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_CIVILOPEDIA).getActionInfoIndex(), -1 )
		screen.hide( "InterfaceHelpButton" )

		screen.setImageButton( "MainMenuButton", ArtFileMgr.getInterfaceArtInfo("INTERFACE_GENERAL_MENU_ICON").getPath(), xResolution - 54, 2, 24, 24, WidgetTypes.WIDGET_MENU_ICON, -1, -1 )
		screen.hide( "MainMenuButton" )

		# Globeview buttons
		self.createGlobeviewButtons( )

		screen.addMultiListControlGFC( "BottomButtonContainer", u"", iMultiListXL, yResolution - 113, xResolution - (iMultiListXL+iMultiListXR), 100, 4, 48, 48, TableStyles.TABLE_STYLE_STANDARD )		
		screen.hide( "BottomButtonContainer" )

		# *********************************************************************************
		# PLOT LIST BUTTONS
		# *********************************************************************************

		for j in range(gc.getMAX_PLOT_LIST_ROWS()):
			yRow = (j - gc.getMAX_PLOT_LIST_ROWS() + 1) * 34
			yPixel = yResolution - 169 + yRow - 3
			xPixel = 315 - 3
			xWidth = self.numPlotListButtons() * 34 + 3
			yHeight = 32 + 3
		
			szStringPanel = "PlotListPanel" + str(j)
			screen.addPanel(szStringPanel, u"", u"", True, False, xPixel, yPixel, xWidth, yHeight, PanelStyles.PANEL_STYLE_EMPTY)

			for i in range(self.numPlotListButtons()):
				k = j*self.numPlotListButtons()+i
				
				xOffset = i * 34
				
				szString = "PlotListButton" + str(k)

# BUG - plot list - start
				szFileNamePromo = ArtFileMgr.getInterfaceArtInfo("OVERLAY_PROMOTION_FRAME").getPath()
				szStringPromoFrame  = szString + "PromoFrame"
				screen.addDDSGFCAt( szStringPromoFrame , szStringPanel, szFileNamePromo, xOffset +  2,  2, 34, 34, WidgetTypes.WIDGET_PLOT_LIST, k, -1, False )
				screen.hide( szStringPromoFrame  )
# BUG - plot list - end

				screen.addCheckBoxGFCAt(szStringPanel, szString, ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_GOVERNOR").getPath(), ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(), xOffset + 3, 3, 32, 32, WidgetTypes.WIDGET_PLOT_LIST, k, -1, ButtonStyles.BUTTON_STYLE_LABEL, True )
				screen.hide( szString )
				
				szStringHealth = szString + "Health"
				screen.addStackedBarGFCAt( szStringHealth, szStringPanel, xOffset + 3, 26, 32, 11, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_GENERAL, k, -1 )
				screen.hide( szStringHealth )
				
				szStringIcon = szString + "Icon"
				szFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_MOVE").getPath()
				screen.addDDSGFCAt( szStringIcon, szStringPanel, szFileName, xOffset, 0, 12, 12, WidgetTypes.WIDGET_PLOT_LIST, k, -1, False )
				screen.hide( szStringIcon )

		# End Turn Text		
		screen.setLabel( "EndTurnText", "Background", u"", CvUtil.FONT_CENTER_JUSTIFY, 0, yResolution - 188, -0.1, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.setHitTest( "EndTurnText", HitTestTypes.HITTEST_NOHIT )

		# Three states for end turn button...
		screen.setImageButton( "EndTurnButton", "", xResolution - (iEndOfTurnButtonSize/2) - iEndOfTurnPosX, yResolution - (iEndOfTurnButtonSize/2) - iEndOfTurnPosY, iEndOfTurnButtonSize, iEndOfTurnButtonSize, WidgetTypes.WIDGET_END_TURN, -1, -1 )
		screen.setStyle( "EndTurnButton", "Button_HUDEndTurn_Style" )
		screen.setEndTurnState( "EndTurnButton", "Red" )
		screen.hide( "EndTurnButton" )

		# *********************************************************************************
		# RESEARCH BUTTONS
		# *********************************************************************************

		i = 0
		for i in range( gc.getNumTechInfos() ):
			szName = "ResearchButton" + str(i)
			screen.setImageButton( szName, gc.getTechInfo(i).getButton(), 0, 0, 32, 32, WidgetTypes.WIDGET_RESEARCH, i, -1 )
			screen.hide( szName )

		i = 0
		for i in range(gc.getNumReligionInfos()):
			szName = "ReligionButton" + str(i)
			if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_PICK_RELIGION):
				szButton = gc.getReligionInfo(i).getGenericTechButton()
			else:
				szButton = gc.getReligionInfo(i).getTechButton()
			screen.setImageButton( szName, szButton, 0, 0, 32, 32, WidgetTypes.WIDGET_RESEARCH, gc.getReligionInfo(i).getTechPrereq(), -1 )
			screen.hide( szName )
		
		# *********************************************************************************
		# CITIZEN BUTTONS
		# *********************************************************************************

		szHideCitizenList = []

		# Angry Citizens
		i = 0
		for i in range(MAX_CITIZEN_BUTTONS):
			szName = "AngryCitizen" + str(i)
			screen.setImageButton( szName, ArtFileMgr.getInterfaceArtInfo("INTERFACE_ANGRYCITIZEN_TEXTURE").getPath(), xResolution - 74 - (26 * i), yResolution - 238, 24, 24, WidgetTypes.WIDGET_ANGRY_CITIZEN, -1, -1 )
			screen.hide( szName )
			
		iCount = 0

		# Increase Specialists...
		i = 0
		for i in range( gc.getNumSpecialistInfos() ):
			if (gc.getSpecialistInfo(i).isVisible()):
				szName = "IncreaseSpecialist" + str(i)
				screen.setButtonGFC( szName, u"", "", xResolution - 46, (yResolution - 270 - (26 * iCount)), 20, 20, WidgetTypes.WIDGET_CHANGE_SPECIALIST, i, 1, ButtonStyles.BUTTON_STYLE_CITY_PLUS )
				screen.hide( szName )

				iCount = iCount + 1

		iCount = 0

		# Decrease specialists
		i = 0
		for i in range( gc.getNumSpecialistInfos() ):
			if (gc.getSpecialistInfo(i).isVisible()):
				szName = "DecreaseSpecialist" + str(i)
				screen.setButtonGFC( szName, u"", "", xResolution - 24, (yResolution - 270 - (26 * iCount)), 20, 20, WidgetTypes.WIDGET_CHANGE_SPECIALIST, i, -1, ButtonStyles.BUTTON_STYLE_CITY_MINUS )
				screen.hide( szName )

				iCount = iCount + 1

		iCount = 0

		# Citizen Buttons
		i = 0
		for i in range( gc.getNumSpecialistInfos() ):
		
			if (gc.getSpecialistInfo(i).isVisible()):
			
				szName = "CitizenDisabledButton" + str(i)
				screen.setImageButton( szName, gc.getSpecialistInfo(i).getTexture(), xResolution - 74, (yResolution - 272 - (26 * i)), 24, 24, WidgetTypes.WIDGET_DISABLED_CITIZEN, i, -1 )
				screen.enable( szName, False )
				screen.hide( szName )

				for j in range(MAX_CITIZEN_BUTTONS):
					szName = "CitizenButton" + str((i * 100) + j)
					screen.addCheckBoxGFC( szName, gc.getSpecialistInfo(i).getTexture(), "", xResolution - 74 - (26 * j), (yResolution - 272 - (26 * i)), 24, 24, WidgetTypes.WIDGET_CITIZEN, i, j, ButtonStyles.BUTTON_STYLE_LABEL )
					screen.hide( szName )

		# **********************************************************
		# GAME DATA STRINGS
		# **********************************************************

		szGameDataList = []
		
		screen.addStackedBarGFC( "ResearchBar", 268 + ( (xResolution - 1024) / 2 ), 2, 487, iStackBarHeight, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_RESEARCH, -1, -1 )
		screen.setStackedBarColors( "ResearchBar", InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_RESEARCH_STORED") )
		screen.setStackedBarColors( "ResearchBar", InfoBarTypes.INFOBAR_RATE, gc.getInfoTypeForString("COLOR_RESEARCH_RATE") )
		screen.setStackedBarColors( "ResearchBar", InfoBarTypes.INFOBAR_RATE_EXTRA, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.setStackedBarColors( "ResearchBar", InfoBarTypes.INFOBAR_EMPTY, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.hide( "ResearchBar" )
		
# BUG - Great Person Bar - start
		screen.addStackedBarGFC( "GreatPersonBar", 328 + ( (xResolution - 1024) / 2 ), 27, 367, iStackBarHeight, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.setStackedBarColors( "GreatPersonBar", InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_GREAT_PEOPLE_STORED") )
		screen.setStackedBarColors( "GreatPersonBar", InfoBarTypes.INFOBAR_RATE, gc.getInfoTypeForString("COLOR_GREAT_PEOPLE_RATE") )
		screen.setStackedBarColors( "GreatPersonBar", InfoBarTypes.INFOBAR_RATE_EXTRA, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.setStackedBarColors( "GreatPersonBar", InfoBarTypes.INFOBAR_EMPTY, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.hide( "GreatPersonBar" )
# BUG - Great Person Bar - end
		
		# *********************************************************************************
		# SELECTION DATA BUTTONS/STRINGS
		# *********************************************************************************

		szHideSelectionDataList = []

		screen.addStackedBarGFC( "PopulationBar", iCityCenterRow1X, iCityCenterRow1Y-4, xResolution - (iCityCenterRow1X*2), iStackBarHeight, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_HELP_POPULATION, -1, -1 )
		screen.setStackedBarColors( "PopulationBar", InfoBarTypes.INFOBAR_STORED, gc.getYieldInfo(YieldTypes.YIELD_FOOD).getColorType() )
		screen.setStackedBarColorsAlpha( "PopulationBar", InfoBarTypes.INFOBAR_RATE, gc.getYieldInfo(YieldTypes.YIELD_FOOD).getColorType(), 0.8 )
		screen.setStackedBarColors( "PopulationBar", InfoBarTypes.INFOBAR_RATE_EXTRA, gc.getInfoTypeForString("COLOR_NEGATIVE_RATE") )
		screen.setStackedBarColors( "PopulationBar", InfoBarTypes.INFOBAR_EMPTY, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.hide( "PopulationBar" )
		
		screen.addStackedBarGFC( "ProductionBar", iCityCenterRow2X, iCityCenterRow2Y-4, xResolution - (iCityCenterRow2X*2), iStackBarHeight, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_HELP_PRODUCTION, -1, -1 )
		screen.setStackedBarColors( "ProductionBar", InfoBarTypes.INFOBAR_STORED, gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getColorType() )
		screen.setStackedBarColorsAlpha( "ProductionBar", InfoBarTypes.INFOBAR_RATE, gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getColorType(), 0.8 )
		screen.setStackedBarColors( "ProductionBar", InfoBarTypes.INFOBAR_RATE_EXTRA, gc.getYieldInfo(YieldTypes.YIELD_FOOD).getColorType() )
		screen.setStackedBarColors( "ProductionBar", InfoBarTypes.INFOBAR_EMPTY, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.hide( "ProductionBar" )
		
		screen.addStackedBarGFC( "GreatPeopleBar", xResolution - 246, yResolution - 180, 194, iStackBarHeight, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_HELP_GREAT_PEOPLE, -1, -1 )
		screen.setStackedBarColors( "GreatPeopleBar", InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_GREAT_PEOPLE_STORED") )
		screen.setStackedBarColors( "GreatPeopleBar", InfoBarTypes.INFOBAR_RATE, gc.getInfoTypeForString("COLOR_GREAT_PEOPLE_RATE") )
		screen.setStackedBarColors( "GreatPeopleBar", InfoBarTypes.INFOBAR_RATE_EXTRA, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.setStackedBarColors( "GreatPeopleBar", InfoBarTypes.INFOBAR_EMPTY, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.hide( "GreatPeopleBar" )
		
		screen.addStackedBarGFC( "CultureBar", 16, yResolution - 188, 220, iStackBarHeight, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_HELP_CULTURE, -1, -1 )
		screen.setStackedBarColors( "CultureBar", InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_CULTURE_STORED") )
		screen.setStackedBarColors( "CultureBar", InfoBarTypes.INFOBAR_RATE, gc.getInfoTypeForString("COLOR_CULTURE_RATE") )
		screen.setStackedBarColors( "CultureBar", InfoBarTypes.INFOBAR_RATE_EXTRA, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.setStackedBarColors( "CultureBar", InfoBarTypes.INFOBAR_EMPTY, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.hide( "CultureBar" )

		# Holy City Overlay
		for i in range( gc.getNumReligionInfos() ):
			xCoord = xResolution - 242 + (i * 34)
			yCoord = 42
			szName = "ReligionHolyCityDDS" + str(i)
			screen.addDDSGFC( szName, ArtFileMgr.getInterfaceArtInfo("INTERFACE_HOLYCITY_OVERLAY").getPath(), xCoord, yCoord, 24, 24, WidgetTypes.WIDGET_HELP_RELIGION_CITY, i, -1 )
			screen.hide( szName )

		for i in range( gc.getNumCorporationInfos() ):
			xCoord = xResolution - 242 + (i * 34)
			yCoord = 66
			szName = "CorporationHeadquarterDDS" + str(i)
			screen.addDDSGFC( szName, ArtFileMgr.getInterfaceArtInfo("INTERFACE_HOLYCITY_OVERLAY").getPath(), xCoord, yCoord, 24, 24, WidgetTypes.WIDGET_HELP_CORPORATION_CITY, i, -1 )
			screen.hide( szName )

		screen.addStackedBarGFC( "NationalityBar", 16, yResolution - 214, 220, iStackBarHeight, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_HELP_NATIONALITY, -1, -1 )
		screen.hide( "NationalityBar" )

		screen.setButtonGFC( "CityScrollMinus", u"", "", 274, 32, 32, 32, WidgetTypes.WIDGET_CITY_SCROLL, -1, -1, ButtonStyles.BUTTON_STYLE_ARROW_LEFT )
		screen.hide( "CityScrollMinus" )

		screen.setButtonGFC( "CityScrollPlus", u"", "", 288, 32, 32, 32, WidgetTypes.WIDGET_CITY_SCROLL, 1, -1, ButtonStyles.BUTTON_STYLE_ARROW_RIGHT )
		screen.hide( "CityScrollPlus" )
		
# BUG - City Arrows - start
		screen.setButtonGFC( "MainCityScrollMinus", u"", "", xResolution - 275, yResolution - 165, 32, 32, WidgetTypes.WIDGET_CITY_SCROLL, -1, -1, ButtonStyles.BUTTON_STYLE_ARROW_LEFT )
		screen.hide( "MainCityScrollMinus" )

		screen.setButtonGFC( "MainCityScrollPlus", u"", "", xResolution - 255, yResolution - 165, 32, 32, WidgetTypes.WIDGET_CITY_SCROLL, 1, -1, ButtonStyles.BUTTON_STYLE_ARROW_RIGHT )
		screen.hide( "MainCityScrollPlus" )
# BUG - City Arrows - end		

# BUG - Combat Counter - start
		screen.setLabel( "CombatXPButton", "Background", u"", CvUtil.FONT_RIGHT_JUSTIFY, 220, 50, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.hide( "CombatXPButton" )

		screen.setLabel( "CombatXPText", "Background", u"", CvUtil.FONT_LEFT_JUSTIFY, 220, 50, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.hide( "CombatXPText" )
# BUG - Combat Counter - end

		screen.setButtonGFC( "PlotListMinus", u"", "", 315 + ( xResolution - (iMultiListXL+iMultiListXR) - 68 ), yResolution - 171, 32, 32, WidgetTypes.WIDGET_PLOT_LIST_SHIFT, -1, -1, ButtonStyles.BUTTON_STYLE_ARROW_LEFT )
		screen.hide( "PlotListMinus" )

		screen.setButtonGFC( "PlotListPlus", u"", "", 298 + ( xResolution - (iMultiListXL+iMultiListXR) - 34 ), yResolution - 171, 32, 32, WidgetTypes.WIDGET_PLOT_LIST_SHIFT, 1, -1, ButtonStyles.BUTTON_STYLE_ARROW_RIGHT )
		screen.hide( "PlotListPlus" )

# BUG - Raw Commerce - start
		iRawCommerceTop = 154
		iRawCommerceHeight = 90
		screen.addPanel( "RawCommercePanel", u"", u"", True, False, 10, iRawCommerceTop, 238, iRawCommerceHeight, PanelStyles.PANEL_STYLE_STANDARD )
		screen.setStyle( "RawCommercePanel", "Panel_City_Info_Style" )
		screen.hide( "RawCommercePanel" )

		if (BugCityScreen.isShowRawCommerce()):
			iTradeRouteListTop = iRawCommerceTop + iRawCommerceHeight + 5
			iBuildingListTop = iTradeRouteListTop + 130
		else:
			iTradeRouteListTop = 157
			iBuildingListTop = 287

		screen.addPanel( "TradeRouteListBackground", u"", u"", True, False, 10, iTradeRouteListTop, 238, 30, PanelStyles.PANEL_STYLE_STANDARD )
		screen.setStyle( "TradeRouteListBackground", "Panel_City_Header_Style" )
		screen.hide( "TradeRouteListBackground" )

		screen.setLabel( "TradeRouteListLabel", "Background", localText.getText("TXT_KEY_HEADING_TRADEROUTE_LIST", ()), CvUtil.FONT_CENTER_JUSTIFY, 129, iTradeRouteListTop + 8, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.hide( "TradeRouteListLabel" )

		screen.addPanel( "BuildingListBackground", u"", u"", True, False, 10, iBuildingListTop, 238, 30, PanelStyles.PANEL_STYLE_STANDARD )
		screen.setStyle( "BuildingListBackground", "Panel_City_Header_Style" )
		screen.hide( "BuildingListBackground" )

		screen.setLabel( "BuildingListLabel", "Background", localText.getText("TXT_KEY_CONCEPT_BUILDINGS", ()), CvUtil.FONT_CENTER_JUSTIFY, 129, iBuildingListTop + 8, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.hide( "BuildingListLabel" )
# BUG - Raw Commerce - end

		# *********************************************************************************
		# UNIT INFO ELEMENTS
		# *********************************************************************************

		i = 0
		for i in range(gc.getNumPromotionInfos()):
			szName = "PromotionButton" + str(i)
			screen.addDDSGFC( szName, gc.getPromotionInfo(i).getButton(), 180, yResolution - 18, 24, 24, WidgetTypes.WIDGET_ACTION, gc.getPromotionInfo(i).getActionInfoIndex(), -1 )
			screen.hide( szName )
			
		# *********************************************************************************
		# SCORES
		# *********************************************************************************
		
		screen.addPanel( "ScoreBackground", u"", u"", True, False, 0, 0, 0, 0, PanelStyles.PANEL_STYLE_HUD_HELP )
		screen.hide( "ScoreBackground" )

		for i in range( gc.getMAX_PLAYERS() ):
			szName = "ScoreText" + str(i)
			screen.setText( szName, "Background", u"", CvUtil.FONT_RIGHT_JUSTIFY, 996, 622, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_CONTACT_CIV, i, -1 )
			screen.hide( szName )
			
		# This should be a forced redraw screen
		screen.setForcedRedraw( True )
		
		# This should show the screen immidiately and pass input to the game
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, True)
		
		szHideList = []
		
		szHideList.append( "CreateGroup" )
		szHideList.append( "DeleteGroup" )

		# City Tabs
		for i in range( g_NumCityTabTypes ):
			szButtonID = "CityTab" + str(i)
			szHideList.append( szButtonID )
					
		for i in range( g_NumHurryInfos ):
			szButtonID = "Hurry" + str(i)
			szHideList.append( szButtonID )

		szHideList.append( "Hurry0" )
		szHideList.append( "Hurry1" )
		
		screen.registerHideList( szHideList, len(szHideList), 0 )

		return 0

	# Will update the screen (every 250 MS)
	def updateScreen(self):
		
		global g_szTimeText
		global g_iTimeTextCounter
# BUG - NJAGC - start
		global g_bShowTimeTextAlt
# BUG - NJAGC - end

		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		
		# Find out our resolution
		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()
		self.m_iNumPlotListButtons = (xResolution - (iMultiListXL+iMultiListXR) - 68) / 34
		
		# This should recreate the minimap on load games and returns if already exists -JW
		screen.initMinimap( xResolution - 210, xResolution - 9, yResolution - 131, yResolution - 9, -0.1 )

		messageControl = CyMessageControl()
		
		bShow = False
		
		# Hide all interface widgets		
		#screen.hide( "EndTurnText" )

		if ( CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_MINIMAP_ONLY ):
			if (gc.getGame().isPaused()):
				# Pause overrides other messages
				acOutput = localText.getText("SYSTEM_GAME_PAUSED", (gc.getPlayer(gc.getGame().getPausePlayer()).getNameKey(), ))
				#screen.modifyLabel( "EndTurnText", acOutput, CvUtil.FONT_CENTER_JUSTIFY )
				screen.setEndTurnState( "EndTurnText", acOutput )
				bShow = True
			elif (messageControl.GetFirstBadConnection() != -1):
				# Waiting on a bad connection to resolve
				if (messageControl.GetConnState(messageControl.GetFirstBadConnection()) == 1):
					if (gc.getGame().isMPOption(MultiplayerOptionTypes.MPOPTION_ANONYMOUS)):
						acOutput = localText.getText("SYSTEM_WAITING_FOR_PLAYER", (gc.getPlayer(messageControl.GetFirstBadConnection()).getNameKey(), 0))
					else:
						acOutput = localText.getText("SYSTEM_WAITING_FOR_PLAYER", (gc.getPlayer(messageControl.GetFirstBadConnection()).getNameKey(), (messageControl.GetFirstBadConnection() + 1)))
					#screen.modifyLabel( "EndTurnText", acOutput, CvUtil.FONT_CENTER_JUSTIFY )
					screen.setEndTurnState( "EndTurnText", acOutput )
					bShow = True
				elif (messageControl.GetConnState(messageControl.GetFirstBadConnection()) == 2):
					if (gc.getGame().isMPOption(MultiplayerOptionTypes.MPOPTION_ANONYMOUS)):
						acOutput = localText.getText("SYSTEM_PLAYER_JOINING", (gc.getPlayer(messageControl.GetFirstBadConnection()).getNameKey(), 0))
					else:
						acOutput = localText.getText("SYSTEM_PLAYER_JOINING", (gc.getPlayer(messageControl.GetFirstBadConnection()).getNameKey(), (messageControl.GetFirstBadConnection() + 1)))
					#screen.modifyLabel( "EndTurnText", acOutput, CvUtil.FONT_CENTER_JUSTIFY )
					screen.setEndTurnState( "EndTurnText", acOutput )
					bShow = True
			else:
				# Flash select messages if no popups are present
				if ( CyInterface().shouldDisplayReturn() ):
					acOutput = localText.getText("SYSTEM_RETURN", ())
					#screen.modifyLabel( "EndTurnText", acOutput, CvUtil.FONT_CENTER_JUSTIFY )
					screen.setEndTurnState( "EndTurnText", acOutput )
					bShow = True
				elif ( CyInterface().shouldDisplayWaitingOthers() ):
					acOutput = localText.getText("SYSTEM_WAITING", ())
					#screen.modifyLabel( "EndTurnText", acOutput, CvUtil.FONT_CENTER_JUSTIFY )
					screen.setEndTurnState( "EndTurnText", acOutput )
					bShow = True
				elif ( CyInterface().shouldDisplayEndTurn() ):
# BUG - Reminders - start
					if ( ReminderEventManager.g_turnReminderTexts ):
						acOutput = u"%s" % ReminderEventManager.g_turnReminderTexts
					else:
						acOutput = localText.getText("SYSTEM_END_TURN", ())
# BUG - Reminders - end
					#screen.modifyLabel( "EndTurnText", acOutput, CvUtil.FONT_CENTER_JUSTIFY )
					screen.setEndTurnState( "EndTurnText", acOutput )
					bShow = True
				elif ( CyInterface().shouldDisplayWaitingYou() ):
					acOutput = localText.getText("SYSTEM_WAITING_FOR_YOU", ())
					#screen.modifyLabel( "EndTurnText", acOutput, CvUtil.FONT_CENTER_JUSTIFY )
					screen.setEndTurnState( "EndTurnText", acOutput )
					bShow = True
# BUG - Options - start
				elif ( BugScreens.isShowOptionsKeyReminder() ):
					acOutput = localText.getText("TXT_KEY_BUG_OPTIONS_KEY_REMINDER", ())
					#screen.modifyLabel( "EndTurnText", acOutput, CvUtil.FONT_CENTER_JUSTIFY )
					screen.setEndTurnState( "EndTurnText", acOutput )
					bShow = True
# BUG - Options - end

		if ( bShow ):
			screen.showEndTurn( "EndTurnText" )
			if ( CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW or CyInterface().isCityScreenUp() ):
				screen.moveItem( "EndTurnText", 0, yResolution - 194, -0.1 )
			else:
				screen.moveItem( "EndTurnText", 0, yResolution - 86, -0.1 )
		else:
			screen.hideEndTurn( "EndTurnText" )

		self.updateEndTurnButton()

# BUG - NJAGC - start
		if (CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_ADVANCED_START):
			if (BugNJAGC.isEnabled()):
				if (BugNJAGC.isShowEra()):
					screen.show( "EraText" )
				else:
					screen.hide( "EraText" )
				
				if (BugNJAGC.isAlternateTimeText()):
					#global g_iTimeTextCounter (already done above)
					if (CyUserProfile().wasClockJustTurnedOn() or g_iTimeTextCounter <= 0):
						# reset timer, display primary
						g_bShowTimeTextAlt = False
						g_iTimeTextCounter = BugNJAGC.getAlternatePeriod() * 1000
						CyUserProfile().setClockJustTurnedOn(False)
					else:
						# countdown timer
						g_iTimeTextCounter -= 250
						if (g_iTimeTextCounter <= 0):
							# timer elapsed, toggle between primary and alternate
							g_iTimeTextCounter = BugNJAGC.getAlternatePeriod() * 1000
							g_bShowTimeTextAlt = not g_bShowTimeTextAlt
				else:
					g_bShowTimeTextAlt = False
				
				self.updateTimeText()
				screen.setLabel( "TimeText", "Background", g_szTimeText, CvUtil.FONT_RIGHT_JUSTIFY, xResolution - 56, 6, -0.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
				screen.show( "TimeText" )
			else:
				screen.hide( "EraText" )
				self.updateTimeText()
				screen.setLabel( "TimeText", "Background", g_szTimeText, CvUtil.FONT_RIGHT_JUSTIFY, xResolution - 56, 6, -0.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
				screen.show( "TimeText" )
		else:
			screen.hide( "TimeText" )
			screen.hide( "EraText" )
# BUG - NJAGC - end

		return 0

	# Will redraw the interface
	def redraw( self ):

		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )

		# Check Dirty Bits, see what we need to redraw...
		if (CyInterface().isDirty(InterfaceDirtyBits.PercentButtons_DIRTY_BIT) == True):
			# Percent Buttons
			self.updatePercentButtons()
			CyInterface().setDirty(InterfaceDirtyBits.PercentButtons_DIRTY_BIT, False)
		if (CyInterface().isDirty(InterfaceDirtyBits.Flag_DIRTY_BIT) == True):
			# Percent Buttons
			self.updateFlag()
			CyInterface().setDirty(InterfaceDirtyBits.Flag_DIRTY_BIT, False)
		if ( CyInterface().isDirty(InterfaceDirtyBits.MiscButtons_DIRTY_BIT) == True ):
			# Miscellaneous buttons (civics screen, etc)
			self.updateMiscButtons()
			CyInterface().setDirty(InterfaceDirtyBits.MiscButtons_DIRTY_BIT, False)
		if ( CyInterface().isDirty(InterfaceDirtyBits.InfoPane_DIRTY_BIT) == True ):
			# Info Pane Dirty Bit
			# This must come before updatePlotListButtons so that the entity widget appears in front of the stats
			self.updateInfoPaneStrings()
			CyInterface().setDirty(InterfaceDirtyBits.InfoPane_DIRTY_BIT, False)
		if ( CyInterface().isDirty(InterfaceDirtyBits.PlotListButtons_DIRTY_BIT) == True ):
			# Plot List Buttons Dirty
			self.updatePlotListButtons()
			CyInterface().setDirty(InterfaceDirtyBits.PlotListButtons_DIRTY_BIT, False)
		if ( CyInterface().isDirty(InterfaceDirtyBits.SelectionButtons_DIRTY_BIT) == True ):
			# Selection Buttons Dirty
			self.updateSelectionButtons()
			CyInterface().setDirty(InterfaceDirtyBits.SelectionButtons_DIRTY_BIT, False)
		if ( CyInterface().isDirty(InterfaceDirtyBits.ResearchButtons_DIRTY_BIT) == True ):
			# Research Buttons Dirty
			self.updateResearchButtons()
			CyInterface().setDirty(InterfaceDirtyBits.ResearchButtons_DIRTY_BIT, False)
		if ( CyInterface().isDirty(InterfaceDirtyBits.CitizenButtons_DIRTY_BIT) == True ):
			# Citizen Buttons Dirty
			self.updateCitizenButtons()
			CyInterface().setDirty(InterfaceDirtyBits.CitizenButtons_DIRTY_BIT, False)
		if ( CyInterface().isDirty(InterfaceDirtyBits.GameData_DIRTY_BIT) == True ):
			# Game Data Strings Dirty
			self.updateGameDataStrings()
			CyInterface().setDirty(InterfaceDirtyBits.GameData_DIRTY_BIT, False)
		if ( CyInterface().isDirty(InterfaceDirtyBits.Help_DIRTY_BIT) == True ):
			# Help Dirty bit
			self.updateHelpStrings()
			CyInterface().setDirty(InterfaceDirtyBits.Help_DIRTY_BIT, False)
		if ( CyInterface().isDirty(InterfaceDirtyBits.CityScreen_DIRTY_BIT) == True ):
			# Selection Data Dirty Bit
			self.updateCityScreen()
			CyInterface().setDirty(InterfaceDirtyBits.Domestic_Advisor_DIRTY_BIT, True)
			CyInterface().setDirty(InterfaceDirtyBits.CityScreen_DIRTY_BIT, False)
		if ( CyInterface().isDirty(InterfaceDirtyBits.Score_DIRTY_BIT) == True or CyInterface().checkFlashUpdate() ):
			# Scores!
			self.updateScoreStrings()
			CyInterface().setDirty(InterfaceDirtyBits.Score_DIRTY_BIT, False)
		if ( CyInterface().isDirty(InterfaceDirtyBits.GlobeInfo_DIRTY_BIT) == True ):
			# Globeview and Globelayer buttons
			CyInterface().setDirty(InterfaceDirtyBits.GlobeInfo_DIRTY_BIT, False)
			self.updateGlobeviewButtons()
		
		return 0

	# Will update the percent buttons
	def updatePercentButtons( self ):

		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )

		for iI in range( CommerceTypes.NUM_COMMERCE_TYPES ):
			szString = "IncreasePercent" + str(iI)
			screen.hide( szString )
			szString = "DecreasePercent" + str(iI)
			screen.hide( szString )

		pHeadSelectedCity = CyInterface().getHeadSelectedCity()

		if ( not CyInterface().isCityScreenUp() or ( pHeadSelectedCity.getOwner() == gc.getGame().getActivePlayer() ) or gc.getGame().isDebugMode() ):
			iCount = 0

			if ( CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_MINIMAP_ONLY and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_ADVANCED_START):
				for iI in range( CommerceTypes.NUM_COMMERCE_TYPES ):
					# Intentional offset...
					eCommerce = (iI + 1) % CommerceTypes.NUM_COMMERCE_TYPES
										
					if (gc.getActivePlayer().isCommerceFlexible(eCommerce) or (CyInterface().isCityScreenUp() and (eCommerce == CommerceTypes.COMMERCE_GOLD))):
						szString1 = "IncreasePercent" + str(eCommerce)
						screen.setButtonGFC( szString1, u"", "", 70, 50 + (19 * iCount), 20, 20, WidgetTypes.WIDGET_CHANGE_PERCENT, eCommerce, gc.getDefineINT("COMMERCE_PERCENT_CHANGE_INCREMENTS"), ButtonStyles.BUTTON_STYLE_CITY_PLUS )
						screen.show( szString1 )
						szString2 = "DecreasePercent" + str(eCommerce)
						screen.setButtonGFC( szString2, u"", "", 90, 50 + (19 * iCount), 20, 20, WidgetTypes.WIDGET_CHANGE_PERCENT, eCommerce, -gc.getDefineINT("COMMERCE_PERCENT_CHANGE_INCREMENTS"), ButtonStyles.BUTTON_STYLE_CITY_MINUS )
						screen.show( szString2 )

						iCount = iCount + 1

						if (gc.getActivePlayer().isCommerceFlexible(eCommerce)):
							screen.enable( szString1, True )
							screen.enable( szString2, True )
						else:
							screen.enable( szString1, False )
							screen.enable( szString2, False )
							
		return 0

	# Will update the end Turn Button
	def updateEndTurnButton( self ):

		global g_eEndTurnButtonState
		
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )

		if ( CyInterface().shouldDisplayEndTurnButton() and CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW ):
		
			eState = CyInterface().getEndTurnState()
			
			bShow = False
			
			if ( eState == EndTurnButtonStates.END_TURN_OVER_HIGHLIGHT ):
				screen.setEndTurnState( "EndTurnButton", u"Red" )
				bShow = True
			elif ( eState == EndTurnButtonStates.END_TURN_OVER_DARK ):
				screen.setEndTurnState( "EndTurnButton", u"Red" )
				bShow = True
			elif ( eState == EndTurnButtonStates.END_TURN_GO ):
				screen.setEndTurnState( "EndTurnButton", u"Green" )
				bShow = True
			
			if ( bShow ):
				screen.showEndTurn( "EndTurnButton" )
			else:
				screen.hideEndTurn( "EndTurnButton" )
			
			if ( g_eEndTurnButtonState == eState ):
				return
				
			g_eEndTurnButtonState = eState
			
		else:
			screen.hideEndTurn( "EndTurnButton" )

		return 0

	# Update the miscellaneous buttons
	def updateMiscButtons( self ):
	
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		
		xResolution = screen.getXResolution()

		if ( CyInterface().shouldDisplayFlag() and CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW ):
			screen.show( "CivilizationFlag" )
			screen.show( "InterfaceHelpButton" )
			screen.show( "MainMenuButton" )
		else:
			screen.hide( "CivilizationFlag" )
			screen.hide( "InterfaceHelpButton" )
			screen.hide( "MainMenuButton" )

		if ( CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_HIDE_ALL or CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_MINIMAP_ONLY ):
			screen.hide( "InterfaceLeftBackgroundWidget" )
			screen.hide( "InterfaceTopBackgroundWidget" )
			screen.hide( "InterfaceCenterBackgroundWidget" )
			screen.hide( "InterfaceRightBackgroundWidget" )
			screen.hide( "MiniMapPanel" )
			screen.hide( "InterfaceTopLeft" )
			screen.hide( "InterfaceTopCenter" )
			screen.hide( "InterfaceTopRight" )
			screen.hide( "TurnLogButton" )
			screen.hide( "EspionageAdvisorButton" )
			screen.hide( "DomesticAdvisorButton" )
			screen.hide( "ForeignAdvisorButton" )
			screen.hide( "TechAdvisorButton" )
			screen.hide( "CivicsAdvisorButton" )
			screen.hide( "ReligiousAdvisorButton" )
			screen.hide( "CorporationAdvisorButton" )
			screen.hide( "FinanceAdvisorButton" )
			screen.hide( "MilitaryAdvisorButton" )
			screen.hide( "VictoryAdvisorButton" )
			screen.hide( "InfoAdvisorButton" )
# BUG - NJAGC - start
			screen.hide( "EraText" )
# BUG - NJAGC - end
# BUG - City Arrows - start
			screen.hide( "MainCityScrollMinus" )
			screen.hide( "MainCityScrollPlus" )
# BUG - City Arrows - end			
# BUG - Combat Counter - start
			screen.hide( "CombatXPButton" )
			screen.hide( "CombatXPText" )
# BUG - Combat Counter - end
		
		elif ( CyInterface().isCityScreenUp() ):
			screen.show( "InterfaceLeftBackgroundWidget" )
			screen.show( "InterfaceTopBackgroundWidget" )
			screen.show( "InterfaceCenterBackgroundWidget" )
			screen.show( "InterfaceRightBackgroundWidget" )
			screen.show( "MiniMapPanel" )
			screen.hide( "InterfaceTopLeft" )
			screen.hide( "InterfaceTopCenter" )
			screen.hide( "InterfaceTopRight" )
			screen.hide( "TurnLogButton" )
			screen.hide( "EspionageAdvisorButton" )
			screen.hide( "DomesticAdvisorButton" )
			screen.hide( "ForeignAdvisorButton" )
			screen.hide( "TechAdvisorButton" )
			screen.hide( "CivicsAdvisorButton" )
			screen.hide( "ReligiousAdvisorButton" )
			screen.hide( "CorporationAdvisorButton" )
			screen.hide( "FinanceAdvisorButton" )
			screen.hide( "MilitaryAdvisorButton" )
			screen.hide( "VictoryAdvisorButton" )
			screen.hide( "InfoAdvisorButton" )
# BUG - City Arrows - start
			screen.hide( "MainCityScrollMinus" )
			screen.hide( "MainCityScrollPlus" )
# BUG - City Arrows - end
# BUG - Combat Counter - start
			screen.hide( "CombatXPButton" )
			screen.hide( "CombatXPText" )
# BUG - Combat Counter - end
	
		elif ( CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_HIDE):
			screen.hide( "InterfaceLeftBackgroundWidget" )
			screen.show( "InterfaceTopBackgroundWidget" )
			screen.hide( "InterfaceCenterBackgroundWidget" )
			screen.hide( "InterfaceRightBackgroundWidget" )
			screen.hide( "MiniMapPanel" )
			screen.show( "InterfaceTopLeft" )
			screen.show( "InterfaceTopCenter" )
			screen.show( "InterfaceTopRight" )
			screen.show( "TurnLogButton" )
			screen.show( "EspionageAdvisorButton" )
			screen.show( "DomesticAdvisorButton" )
			screen.show( "ForeignAdvisorButton" )
			screen.show( "TechAdvisorButton" )
			screen.show( "CivicsAdvisorButton" )
			screen.show( "ReligiousAdvisorButton" )
			screen.show( "CorporationAdvisorButton" )
			screen.show( "FinanceAdvisorButton" )
			screen.show( "MilitaryAdvisorButton" )
			screen.show( "VictoryAdvisorButton" )
			screen.show( "InfoAdvisorButton" )
# BUG - City Arrows - start
			screen.hide( "MainCityScrollMinus" )
			screen.hide( "MainCityScrollPlus" )			
# BUG - City Arrows - end
# BUG - Combat Counter - start
			screen.hide( "CombatXPButton" )
			screen.hide( "CombatXPText" )
# BUG - Combat Counter - end

			screen.moveToFront( "TurnLogButton" )
			screen.moveToFront( "EspionageAdvisorButton" )
			screen.moveToFront( "DomesticAdvisorButton" )
			screen.moveToFront( "ForeignAdvisorButton" )
			screen.moveToFront( "TechAdvisorButton" )
			screen.moveToFront( "CivicsAdvisorButton" )
			screen.moveToFront( "ReligiousAdvisorButton" )
			screen.moveToFront( "CorporationAdvisorButton" )
			screen.moveToFront( "FinanceAdvisorButton" )
			screen.moveToFront( "MilitaryAdvisorButton" )
			screen.moveToFront( "VictoryAdvisorButton" )
			screen.moveToFront( "InfoAdvisorButton" )

		elif (CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_ADVANCED_START):		
			screen.hide( "InterfaceLeftBackgroundWidget" )
			screen.hide( "InterfaceTopBackgroundWidget" )
			screen.hide( "InterfaceCenterBackgroundWidget" )
			screen.hide( "InterfaceRightBackgroundWidget" )
			screen.show( "MiniMapPanel" )
			screen.hide( "InterfaceTopLeft" )
			screen.hide( "InterfaceTopCenter" )
			screen.hide( "InterfaceTopRight" )
			screen.hide( "TurnLogButton" )
			screen.hide( "EspionageAdvisorButton" )
			screen.hide( "DomesticAdvisorButton" )
			screen.hide( "ForeignAdvisorButton" )
			screen.hide( "TechAdvisorButton" )
			screen.hide( "CivicsAdvisorButton" )
			screen.hide( "ReligiousAdvisorButton" )
			screen.hide( "CorporationAdvisorButton" )
			screen.hide( "FinanceAdvisorButton" )
			screen.hide( "MilitaryAdvisorButton" )
			screen.hide( "VictoryAdvisorButton" )
			screen.hide( "InfoAdvisorButton" )
# BUG - City Arrows - start
			screen.hide( "MainCityScrollMinus" )
			screen.hide( "MainCityScrollPlus" )
# BUG - City Arrows - end
# BUG - Combat Counter - start
			screen.hide( "CombatXPButton" )
			screen.hide( "CombatXPText" )
# BUG - Combat Counter - end

		elif ( CyEngine().isGlobeviewUp() ):
			screen.hide( "InterfaceLeftBackgroundWidget" )
			screen.hide( "InterfaceTopBackgroundWidget" )
			screen.hide( "InterfaceCenterBackgroundWidget" )
			screen.show( "InterfaceRightBackgroundWidget" )
			screen.show( "MiniMapPanel" )
			screen.show( "InterfaceTopLeft" )
			screen.show( "InterfaceTopCenter" )
			screen.show( "InterfaceTopRight" )
			screen.show( "TurnLogButton" )
			screen.show( "EspionageAdvisorButton" )
			screen.show( "DomesticAdvisorButton" )
			screen.show( "ForeignAdvisorButton" )
			screen.show( "TechAdvisorButton" )
			screen.show( "CivicsAdvisorButton" )
			screen.show( "ReligiousAdvisorButton" )
			screen.show( "CorporationAdvisorButton" )
			screen.show( "FinanceAdvisorButton" )
			screen.show( "MilitaryAdvisorButton" )
			screen.show( "VictoryAdvisorButton" )
			screen.show( "InfoAdvisorButton" )			
# BUG - City Arrows - start
			screen.hide( "MainCityScrollMinus" )
			screen.hide( "MainCityScrollPlus" )
# BUG - City Arrows - end
# BUG - Combat Counter - start
			screen.hide( "CombatXPButton" )
			screen.hide( "CombatXPText" )
# BUG - Combat Counter - end

			screen.moveToFront( "TurnLogButton" )
			screen.moveToFront( "EspionageAdvisorButton" )
			screen.moveToFront( "DomesticAdvisorButton" )
			screen.moveToFront( "ForeignAdvisorButton" )
			screen.moveToFront( "TechAdvisorButton" )
			screen.moveToFront( "CivicsAdvisorButton" )
			screen.moveToFront( "ReligiousAdvisorButton" )
			screen.moveToFront( "CorporationAdvisorButton" )
			screen.moveToFront( "FinanceAdvisorButton" )
			screen.moveToFront( "MilitaryAdvisorButton" )
			screen.moveToFront( "VictoryAdvisorButton" )
			screen.moveToFront( "InfoAdvisorButton" )
			
		else:
			screen.show( "InterfaceLeftBackgroundWidget" )
			screen.show( "InterfaceTopBackgroundWidget" )
			screen.show( "InterfaceCenterBackgroundWidget" )
			screen.show( "InterfaceRightBackgroundWidget" )
			screen.show( "MiniMapPanel" )
			screen.show( "InterfaceTopLeft" )
			screen.show( "InterfaceTopCenter" )
			screen.show( "InterfaceTopRight" )
			screen.show( "TurnLogButton" )
			screen.show( "EspionageAdvisorButton" )
			screen.show( "DomesticAdvisorButton" )
			screen.show( "ForeignAdvisorButton" )
			screen.show( "TechAdvisorButton" )
			screen.show( "CivicsAdvisorButton" )
			screen.show( "ReligiousAdvisorButton" )
			screen.show( "CorporationAdvisorButton" )
			screen.show( "FinanceAdvisorButton" )
			screen.show( "MilitaryAdvisorButton" )
			screen.show( "VictoryAdvisorButton" )
			screen.show( "InfoAdvisorButton" )
# BUG - City Arrows - start
			if (BugScreens.isShowCityCycleArrows()):
				screen.show( "MainCityScrollMinus" )
				screen.show( "MainCityScrollPlus" )
			else:
				screen.hide( "MainCityScrollMinus" )
				screen.hide( "MainCityScrollPlus" )
# BUG - City Arrows - end
# BUG - Combat Counter - start
			if BugScreens.isShowCombatCounter():
				screen.show( "CombatXPButton" )
				screen.show( "CombatXPText" )
			else:
				screen.hide( "CombatXPButton" )
				screen.hide( "CombatXPText" )
# BUG - Combat Counter - end

			screen.moveToFront( "TurnLogButton" )
			screen.moveToFront( "EspionageAdvisorButton" )
			screen.moveToFront( "DomesticAdvisorButton" )
			screen.moveToFront( "ForeignAdvisorButton" )
			screen.moveToFront( "TechAdvisorButton" )
			screen.moveToFront( "CivicsAdvisorButton" )
			screen.moveToFront( "ReligiousAdvisorButton" )
			screen.moveToFront( "CorporationAdvisorButton" )
			screen.moveToFront( "FinanceAdvisorButton" )
			screen.moveToFront( "MilitaryAdvisorButton" )
			screen.moveToFront( "VictoryAdvisorButton" )
			screen.moveToFront( "InfoAdvisorButton" )
			
		screen.updateMinimapVisibility()

		return 0

	# Update plot List Buttons
	def updatePlotListButtons( self ):

		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )

		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()

		bHandled = False
		if ( CyInterface().shouldDisplayUnitModel() and CyEngine().isGlobeviewUp() == false and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL ):
			if ( CyInterface().isCitySelection() ):

				iOrders = CyInterface().getNumOrdersQueued()

				for i in range( iOrders ):
					if ( bHandled == False ):
						eOrderNodeType = CyInterface().getOrderNodeType(i)
						if (eOrderNodeType  == OrderTypes.ORDER_TRAIN ):
							screen.addUnitGraphicGFC( "InterfaceUnitModel", CyInterface().getOrderNodeData1(i), 175, yResolution - 138, 123, 132, WidgetTypes.WIDGET_HELP_SELECTED, 0, -1,  -20, 30, 1, False )
							bHandled = True
						elif ( eOrderNodeType == OrderTypes.ORDER_CONSTRUCT ):
							screen.addBuildingGraphicGFC( "InterfaceUnitModel", CyInterface().getOrderNodeData1(i), 175, yResolution - 138, 123, 132, WidgetTypes.WIDGET_HELP_SELECTED, 0, -1,  -20, 30, 0.8, False )
							bHandled = True
						elif ( eOrderNodeType == OrderTypes.ORDER_CREATE ):
							if(gc.getProjectInfo(CyInterface().getOrderNodeData1(i)).isSpaceship()):
								modelType = 0
								screen.addSpaceShipWidgetGFC("InterfaceUnitModel", 175, yResolution - 138, 123, 132, CyInterface().getOrderNodeData1(i), modelType, WidgetTypes.WIDGET_HELP_SELECTED, 0, -1)
							else:
								screen.hide( "InterfaceUnitModel" )
							bHandled = True
						elif ( eOrderNodeType == OrderTypes.ORDER_MAINTAIN ):
							screen.hide( "InterfaceUnitModel" )
							bHandled = True
							
				if ( not bHandled ):
					screen.hide( "InterfaceUnitModel" )
					bHandled = True

				screen.moveToFront("SelectedCityText")

			elif ( CyInterface().getHeadSelectedUnit() ):
				screen.addUnitGraphicGFC( "InterfaceUnitModel", CyInterface().getHeadSelectedUnit().getUnitType(), 175, yResolution - 138, 123, 132, WidgetTypes.WIDGET_UNIT_MODEL, CyInterface().getHeadSelectedUnit().getUnitType(), -1,  -20, 30, 1, False )
				screen.moveToFront("SelectedUnitText")
			else:
				screen.hide( "InterfaceUnitModel" )
		else:
			screen.hide( "InterfaceUnitModel" )
			
		pPlot = CyInterface().getSelectionPlot()

		for i in range(gc.getNumPromotionInfos()):
			szName = "PromotionButton" + str(i)
			screen.moveToFront( szName )
		
		screen.hide( "PlotListMinus" )
		screen.hide( "PlotListPlus" )
		
		for j in range(gc.getMAX_PLOT_LIST_ROWS()):
			#szStringPanel = "PlotListPanel" + str(j)
			#screen.hide(szStringPanel)
			
			for i in range(self.numPlotListButtons()):
				szString = "PlotListButton" + str(j*self.numPlotListButtons()+i)
				screen.hide( szString )

# BUG - plot list - start
				# hide promo frame
				szStringPromoFrame  = szString+"PromoFrame"
				screen.hide( szStringPromoFrame )

				# hide mission info
				szStringActionIcon = szString+"ActionIcon"
				screen.hide( szStringActionIcon )			
# BUG - plot list - end
				
				szStringHealth = szString + "Health"
				screen.hide( szStringHealth )

				szStringIcon = szString + "Icon"
				screen.hide( szStringIcon )

		if ( pPlot and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL and CyEngine().isGlobeviewUp() == False):

			iVisibleUnits = CyInterface().getNumVisibleUnits()
			iCount = -(CyInterface().getPlotListColumn())
				

			bLeftArrow = False
			bRightArrow = False
			
			if (CyInterface().isCityScreenUp()):
				iMaxRows = 1
				iSkipped = (gc.getMAX_PLOT_LIST_ROWS() - 1) * self.numPlotListButtons()
				iCount += iSkipped
			else:
				iMaxRows = gc.getMAX_PLOT_LIST_ROWS()
				iCount += CyInterface().getPlotListOffset()
				iSkipped = 0

			CyInterface().cacheInterfacePlotUnits(pPlot)
			for i in range(CyInterface().getNumCachedInterfacePlotUnits()):
				pLoopUnit = CyInterface().getCachedInterfacePlotUnit(i)
				if (pLoopUnit):

					if ((iCount == 0) and (CyInterface().getPlotListColumn() > 0)):
						bLeftArrow = True
					elif ((iCount == (gc.getMAX_PLOT_LIST_ROWS() * self.numPlotListButtons() - 1)) and ((iVisibleUnits - iCount - CyInterface().getPlotListColumn() + iSkipped) > 1)):
						bRightArrow = True
						
					if ((iCount >= 0) and (iCount <  self.numPlotListButtons() * gc.getMAX_PLOT_LIST_ROWS())):
						if ((pLoopUnit.getTeam() != gc.getGame().getActiveTeam()) or pLoopUnit.isWaiting()):
							szFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_FORTIFY").getPath()
							
						elif (pLoopUnit.canMove()):
							if (pLoopUnit.hasMoved()):
								szFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_HASMOVED").getPath()
							else:
								szFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_MOVE").getPath()
						else:
							szFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_NOMOVE").getPath()

						szString = "PlotListButton" + str(iCount)
						screen.changeImageButton( szString, pLoopUnit.getButton() )
						if ( pLoopUnit.getOwner() == gc.getGame().getActivePlayer() ):
							bEnable = True
						else:
							bEnable = False
						screen.enable(szString, bEnable)

						if (pLoopUnit.IsSelected()):
							screen.setState(szString, True)
						else:
							screen.setState(szString, False)
						screen.show( szString )

# BUG - plot list - start
						if (BugScreens.isShowUnitPromo()
						and pLoopUnit.getOwner() == gc.getGame().getActivePlayer()							
						and pLoopUnit.isPromotionReady()):
							szStringPromoFrame = szString+"PromoFrame"
							screen.show( szStringPromoFrame )

						if (BugScreens.isShowUnitActions()
						and pLoopUnit.getOwner() == gc.getGame().getActivePlayer()):
							# place the activity info below the unit icon.
							szFileNameAction = ""						
							eActivityType = pLoopUnit.getGroup().getActivityType()
							eAutomationType = pLoopUnit.getGroup().getAutomateType()

							# is unit on air patrol/intercept mission
							if (eActivityType == ActivityTypes.ACTIVITY_INTERCEPT):
								# place "PAT" icon
								szFileNameAction = ArtFileMgr.getInterfaceArtInfo("OVERLAY_ACTION_PATROL").getPath()
								iOffset = 14
							# is unit fortified for healing (wake up when healed)
							elif (eActivityType == ActivityTypes.ACTIVITY_HEAL):
								# place "HEAL" icon
								szFileNameAction = ArtFileMgr.getInterfaceArtInfo("OVERLAY_ACTION_HEAL").getPath()
								iOffset = 10
							# is unit sentry (wake up when enemy in sight)
							elif (eActivityType == ActivityTypes.ACTIVITY_SENTRY):
								# place "SEN" icon
								szFileNameAction = ArtFileMgr.getInterfaceArtInfo("OVERLAY_ACTION_SENTRY").getPath()
								iOffset = 13
							# is the turn for this unit skipped (wake up next turn)
							elif (eActivityType == ActivityTypes.ACTIVITY_HOLD):
								# place "SKIP" icon
								szFileNameAction = ArtFileMgr.getInterfaceArtInfo("OVERLAY_ACTION_SKIP").getPath()
								iOffset = 13
							# has unit explaration mission
							elif (eAutomationType == AutomateTypes.AUTOMATE_EXPLORE):
								# place "EXP" icon
								szFileNameAction = ArtFileMgr.getInterfaceArtInfo("OVERLAY_ACTION_EXPLORE").getPath()
								iOffset = 14
							# is unit automated generally (only worker units)
							elif (eAutomationType == AutomateTypes.AUTOMATE_BUILD):
								# place "AUT-B" icon
								szFileNameAction = ArtFileMgr.getInterfaceArtInfo("OVERLAY_ACTION_AUTO_BUILD").getPath()
								iOffset = 8
							# is unit automated for nearest city (only worker units)
							elif (eAutomationType == AutomateTypes.AUTOMATE_CITY):
								# place "AUT-C" icon
								szFileNameAction = ArtFileMgr.getInterfaceArtInfo("OVERLAY_ACTION_AUTO_CITY").getPath()
								iOffset = 8
							# is unit automated for network(only worker units)
							elif (eAutomationType == AutomateTypes.AUTOMATE_NETWORK):
								# place "AUT-N" icon
								szFileNameAction = ArtFileMgr.getInterfaceArtInfo("OVERLAY_ACTION_AUTO_NETWORK").getPath()
								iOffset = 8
							# has unit a mission
							elif (pLoopUnit.getGroup().getLengthMissionQueue() > 0):
								# is the mission a "move to" mission
								eMissionType = pLoopUnit.getGroup().getMissionType(0)
								if ( (eMissionType == MissionTypes.MISSION_MOVE_TO) or \
									 (eMissionType == MissionTypes.MISSION_MOVE_TO_UNIT) ):
									# place "GOTO" icon
									szFileNameAction = ArtFileMgr.getInterfaceArtInfo("OVERLAY_ACTION_GOTO").getPath()
									iOffset = 6
							# if nothing of above, but unit is waiting -> unit is fortified
							elif (pLoopUnit.isWaiting()):
								# place "FORT" icon
								szFileNameAction = ArtFileMgr.getInterfaceArtInfo("OVERLAY_ACTION_FORTIFY").getPath()
								iOffset = 8
										
							# display the mission icon
							if (szFileNameAction != ""):
								x = 315 + ((iCount % self.numPlotListButtons()) * 34)
								y = yResolution - 169 + (iCount / self.numPlotListButtons() - gc.getMAX_PLOT_LIST_ROWS() + 1) * 34
								szStringActionIcon = szString+"ActionIcon"
								screen.addDDSGFC( szStringActionIcon, szFileNameAction, x+iOffset-3, y+29, 32, 8, WidgetTypes.WIDGET_GENERAL, iCount, -1 )
								screen.show( szStringActionIcon )
# BUG - plot list - end

						# place the health bar
						if (pLoopUnit.isFighting()):
							bShowHealth = False
						elif (pLoopUnit.getDomainType() == DomainTypes.DOMAIN_AIR):
							bShowHealth = pLoopUnit.canAirAttack()
						else:
							bShowHealth = pLoopUnit.canFight()

						if bShowHealth:
							szStringHealth = szString + "Health"
							screen.setBarPercentage( szStringHealth, InfoBarTypes.INFOBAR_STORED, float( pLoopUnit.currHitPoints() ) / float( pLoopUnit.maxHitPoints() ) )
							if (pLoopUnit.getDamage() >= ((pLoopUnit.maxHitPoints() * 2) / 3)):
								screen.setStackedBarColors(szStringHealth, InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_RED"))
							elif (pLoopUnit.getDamage() >= (pLoopUnit.maxHitPoints() / 3)):
								screen.setStackedBarColors(szStringHealth, InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_YELLOW"))
							else:
								screen.setStackedBarColors(szStringHealth, InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_GREEN"))
							screen.show( szStringHealth )
						
						# Adds the overlay first
						szStringIcon = szString + "Icon"
						screen.changeDDSGFC( szStringIcon, szFileName )
						screen.show( szStringIcon )

					iCount = iCount + 1

			if (iVisibleUnits > self.numPlotListButtons() * iMaxRows):
				screen.enable("PlotListMinus", bLeftArrow)
				screen.show( "PlotListMinus" )
	
				screen.enable("PlotListPlus", bRightArrow)
				screen.show( "PlotListPlus" )

		return 0
		
	# This will update the flag widget for SP hotseat and dbeugging
	def updateFlag( self ):

		if ( CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_MINIMAP_ONLY and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_ADVANCED_START ):
			screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
			xResolution = screen.getXResolution()
			yResolution = screen.getYResolution()
			screen.addFlagWidgetGFC( "CivilizationFlag", xResolution - 288, yResolution - 138, 68, 250, gc.getGame().getActivePlayer(), WidgetTypes.WIDGET_FLAG, gc.getGame().getActivePlayer(), -1)
		
	# Will hide and show the selection buttons and their associated buttons
	def updateSelectionButtons( self ):
	
		global SELECTION_BUTTON_COLUMNS
		global MAX_SELECTION_BUTTONS
		global g_pSelectedUnit

		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		
		pHeadSelectedCity = CyInterface().getHeadSelectedCity()
		pHeadSelectedUnit = CyInterface().getHeadSelectedUnit()
		
		global g_NumEmphasizeInfos
		global g_NumCityTabTypes
		global g_NumHurryInfos
		global g_NumUnitClassInfos
		global g_NumBuildingClassInfos
		global g_NumProjectInfos
		global g_NumProcessInfos
		global g_NumActionInfos
		
		# Find out our resolution
		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()
		
		screen.addMultiListControlGFC( "BottomButtonContainer", u"", iMultiListXL, yResolution - 113, xResolution - (iMultiListXL+iMultiListXR), 100, 4, 48, 48, TableStyles.TABLE_STYLE_STANDARD )
		screen.clearMultiList( "BottomButtonContainer" )
		screen.hide( "BottomButtonContainer" )
		
		# All of the hides...	
		self.setMinimapButtonVisibility(False)

		screen.hideList( 0 )

		for i in range (g_NumEmphasizeInfos):
			szButtonID = "Emphasize" + str(i)
			screen.hide( szButtonID )

		# Hurry button show...
		for i in range( g_NumHurryInfos ):
			szButtonID = "Hurry" + str(i)
			screen.hide( szButtonID )

		# Conscript Button Show
		screen.hide( "Conscript" )
		#screen.hide( "Liberate" )
		screen.hide( "AutomateProduction" )
		screen.hide( "AutomateCitizens" )

		if (not CyEngine().isGlobeviewUp() and pHeadSelectedCity):
		
			self.setMinimapButtonVisibility(True)

			if ((pHeadSelectedCity.getOwner() == gc.getGame().getActivePlayer()) or gc.getGame().isDebugMode()):
			
				iBtnX = xResolution - 284
				iBtnY = yResolution - 177
				iBtnW = 64
				iBtnH = 30

				# Liberate button
				#szText = "<font=1>" + localText.getText("TXT_KEY_LIBERATE_CITY", ()) + "</font>"
				#screen.setButtonGFC( "Liberate", szText, "", iBtnX, iBtnY, iBtnW, iBtnH, WidgetTypes.WIDGET_LIBERATE_CITY, -1, -1, ButtonStyles.BUTTON_STYLE_STANDARD )
				#screen.setStyle( "Liberate", "Button_CityT1_Style" )
				#screen.hide( "Liberate" )

				iBtnSX = xResolution - 284
				
				iBtnX = iBtnSX
				iBtnY = yResolution - 140
				iBtnW = 64
				iBtnH = 30

				# Conscript button
				szText = "<font=1>" + localText.getText("TXT_KEY_DRAFT", ()) + "</font>"
				screen.setButtonGFC( "Conscript", szText, "", iBtnX, iBtnY, iBtnW, iBtnH, WidgetTypes.WIDGET_CONSCRIPT, -1, -1, ButtonStyles.BUTTON_STYLE_STANDARD )
				screen.setStyle( "Conscript", "Button_CityT1_Style" )
				screen.hide( "Conscript" )

				iBtnY += iBtnH
				iBtnW = 32
				iBtnH = 28
				
				# Hurry Buttons		
				screen.setButtonGFC( "Hurry0", "", "", iBtnX, iBtnY, iBtnW, iBtnH, WidgetTypes.WIDGET_HURRY, 0, -1, ButtonStyles.BUTTON_STYLE_STANDARD )
				screen.setStyle( "Hurry0", "Button_CityC1_Style" )
				screen.hide( "Hurry0" )

				iBtnX += iBtnW

				screen.setButtonGFC( "Hurry1", "", "", iBtnX, iBtnY, iBtnW, iBtnH, WidgetTypes.WIDGET_HURRY, 1, -1, ButtonStyles.BUTTON_STYLE_STANDARD )
				screen.setStyle( "Hurry1", "Button_CityC2_Style" )
				screen.hide( "Hurry1" )
			
				iBtnX = iBtnSX
				iBtnY += iBtnH
			
				# Automate Production Button
				screen.addCheckBoxGFC( "AutomateProduction", "", "", iBtnX, iBtnY, iBtnW, iBtnH, WidgetTypes.WIDGET_AUTOMATE_PRODUCTION, -1, -1, ButtonStyles.BUTTON_STYLE_STANDARD )
				screen.setStyle( "AutomateProduction", "Button_CityC3_Style" )

				iBtnX += iBtnW

				# Automate Citizens Button
				screen.addCheckBoxGFC( "AutomateCitizens", "", "", iBtnX, iBtnY, iBtnW, iBtnH, WidgetTypes.WIDGET_AUTOMATE_CITIZENS, -1, -1, ButtonStyles.BUTTON_STYLE_STANDARD )
				screen.setStyle( "AutomateCitizens", "Button_CityC4_Style" )

				iBtnY += iBtnH
				iBtnX = iBtnSX

				iBtnW	= 22
				iBtnWa	= 20
				iBtnH	= 24
				iBtnHa	= 27
			
				# Set Emphasize buttons
				i = 0
				szButtonID = "Emphasize" + str(i)
				screen.addCheckBoxGFC( szButtonID, "", "", iBtnX, iBtnY, iBtnW, iBtnH, WidgetTypes.WIDGET_EMPHASIZE, i, -1, ButtonStyles.BUTTON_STYLE_LABEL )
				szStyle = "Button_CityB" + str(i+1) + "_Style"
				screen.setStyle( szButtonID, szStyle )
				screen.hide( szButtonID )

				i+=1
				szButtonID = "Emphasize" + str(i)
				screen.addCheckBoxGFC( szButtonID, "", "", iBtnX+iBtnW, iBtnY, iBtnWa, iBtnH, WidgetTypes.WIDGET_EMPHASIZE, i, -1, ButtonStyles.BUTTON_STYLE_LABEL )
				szStyle = "Button_CityB" + str(i+1) + "_Style"
				screen.setStyle( szButtonID, szStyle )
				screen.hide( szButtonID )

				i+=1
				szButtonID = "Emphasize" + str(i)
				screen.addCheckBoxGFC( szButtonID, "", "", iBtnX+iBtnW+iBtnWa, iBtnY, iBtnW, iBtnH, WidgetTypes.WIDGET_EMPHASIZE, i, -1, ButtonStyles.BUTTON_STYLE_LABEL )
				szStyle = "Button_CityB" + str(i+1) + "_Style"
				screen.setStyle( szButtonID, szStyle )
				screen.hide( szButtonID )

				iBtnY += iBtnH
				
				i+=1
				szButtonID = "Emphasize" + str(i)
				screen.addCheckBoxGFC( szButtonID, "", "", iBtnX, iBtnY, iBtnW, iBtnHa, WidgetTypes.WIDGET_EMPHASIZE, i, -1, ButtonStyles.BUTTON_STYLE_LABEL )
				szStyle = "Button_CityB" + str(i+1) + "_Style"
				screen.setStyle( szButtonID, szStyle )
				screen.hide( szButtonID )

				i+=1
				szButtonID = "Emphasize" + str(i)
				screen.addCheckBoxGFC( szButtonID, "", "", iBtnX+iBtnW, iBtnY, iBtnWa, iBtnHa, WidgetTypes.WIDGET_EMPHASIZE, i, -1, ButtonStyles.BUTTON_STYLE_LABEL )
				szStyle = "Button_CityB" + str(i+1) + "_Style"
				screen.setStyle( szButtonID, szStyle )
				screen.hide( szButtonID )

				i+=1
				szButtonID = "Emphasize" + str(i)
				screen.addCheckBoxGFC( szButtonID, "", "", iBtnX+iBtnW+iBtnWa, iBtnY, iBtnW, iBtnHa, WidgetTypes.WIDGET_EMPHASIZE, i, -1, ButtonStyles.BUTTON_STYLE_LABEL )
				szStyle = "Button_CityB" + str(i+1) + "_Style"
				screen.setStyle( szButtonID, szStyle )
				screen.hide( szButtonID )
				
				g_pSelectedUnit = 0
				screen.setState( "AutomateCitizens", pHeadSelectedCity.isCitizensAutomated() )
				screen.setState( "AutomateProduction", pHeadSelectedCity.isProductionAutomated() )
				
				for i in range (g_NumEmphasizeInfos):
					szButtonID = "Emphasize" + str(i)
					screen.show( szButtonID )
					if ( pHeadSelectedCity.AI_isEmphasize(i) ):
						screen.setState( szButtonID, True )
					else:
						screen.setState( szButtonID, False )

				# City Tabs
				for i in range( g_NumCityTabTypes ):
					szButtonID = "CityTab" + str(i)
					screen.show( szButtonID )

				# Hurry button show...
				for i in range( g_NumHurryInfos ):
					szButtonID = "Hurry" + str(i)
					screen.show( szButtonID )
					screen.enable( szButtonID, pHeadSelectedCity.canHurry(i, False) )

				# Conscript Button Show
				screen.show( "Conscript" )
				if (pHeadSelectedCity.canConscript()):
					screen.enable( "Conscript", True )
				else:
					screen.enable( "Conscript", False )

				# Liberate Button Show
				#screen.show( "Liberate" )
				#if (-1 != pHeadSelectedCity.getLiberationPlayer()):
				#	screen.enable( "Liberate", True )
				#else:
				#	screen.enable( "Liberate", False )

				iCount = 0
				iRow = 0
				bFound = False

				# Units to construct
				for i in range ( g_NumUnitClassInfos ):
					eLoopUnit = gc.getCivilizationInfo(pHeadSelectedCity.getCivilizationType()).getCivilizationUnits(i)

					if (pHeadSelectedCity.canTrain(eLoopUnit, False, True)):
						szButton = gc.getPlayer(pHeadSelectedCity.getOwner()).getUnitButton(eLoopUnit)
						screen.appendMultiListButton( "BottomButtonContainer", szButton, iRow, WidgetTypes.WIDGET_TRAIN, i, -1, False )
						screen.show( "BottomButtonContainer" )
						
						if ( not pHeadSelectedCity.canTrain(eLoopUnit, False, False) ):
							screen.disableMultiListButton( "BottomButtonContainer", iRow, iCount, szButton)
						
						iCount = iCount + 1
						bFound = True

				iCount = 0
				if (bFound):
					iRow = iRow + 1
				bFound = False

				# Buildings to construct
				for i in range ( g_NumBuildingClassInfos ):
					if (not isLimitedWonderClass(i)):
						eLoopBuilding = gc.getCivilizationInfo(pHeadSelectedCity.getCivilizationType()).getCivilizationBuildings(i)

						if (pHeadSelectedCity.canConstruct(eLoopBuilding, False, True, False)):
							screen.appendMultiListButton( "BottomButtonContainer", gc.getBuildingInfo(eLoopBuilding).getButton(), iRow, WidgetTypes.WIDGET_CONSTRUCT, i, -1, False )
							screen.show( "BottomButtonContainer" )
							
							if ( not pHeadSelectedCity.canConstruct(eLoopBuilding, False, False, False) ):
								screen.disableMultiListButton( "BottomButtonContainer", iRow, iCount, gc.getBuildingInfo(eLoopBuilding).getButton() )

							iCount = iCount + 1
							bFound = True

				iCount = 0
				if (bFound):
					iRow = iRow + 1
				bFound = False

				# Wonders to construct
				i = 0
				for i in range( g_NumBuildingClassInfos ):
					if (isLimitedWonderClass(i)):
						eLoopBuilding = gc.getCivilizationInfo(pHeadSelectedCity.getCivilizationType()).getCivilizationBuildings(i)

						if (pHeadSelectedCity.canConstruct(eLoopBuilding, False, True, False)):
							screen.appendMultiListButton( "BottomButtonContainer", gc.getBuildingInfo(eLoopBuilding).getButton(), iRow, WidgetTypes.WIDGET_CONSTRUCT, i, -1, False )
							screen.show( "BottomButtonContainer" )
							
							if ( not pHeadSelectedCity.canConstruct(eLoopBuilding, False, False, False) ):
								screen.disableMultiListButton( "BottomButtonContainer", iRow, iCount, gc.getBuildingInfo(eLoopBuilding).getButton() )

							iCount = iCount + 1
							bFound = True

				iCount = 0
				if (bFound):
					iRow = iRow + 1
				bFound = False

				# Projects
				i = 0
				for i in range( g_NumProjectInfos ):
					if (pHeadSelectedCity.canCreate(i, False, True)):
						screen.appendMultiListButton( "BottomButtonContainer", gc.getProjectInfo(i).getButton(), iRow, WidgetTypes.WIDGET_CREATE, i, -1, False )
						screen.show( "BottomButtonContainer" )
						
						if ( not pHeadSelectedCity.canCreate(i, False, False) ):
							screen.disableMultiListButton( "BottomButtonContainer", iRow, iCount, gc.getProjectInfo(i).getButton() )
						
						iCount = iCount + 1
						bFound = True

				# Processes
				i = 0
				for i in range( g_NumProcessInfos ):
					if (pHeadSelectedCity.canMaintain(i, False)):
						screen.appendMultiListButton( "BottomButtonContainer", gc.getProcessInfo(i).getButton(), iRow, WidgetTypes.WIDGET_MAINTAIN, i, -1, False )
						screen.show( "BottomButtonContainer" )
						
						iCount = iCount + 1
						bFound = True

				screen.selectMultiList( "BottomButtonContainer", CyInterface().getCityTabSelectionRow() )
							
		elif (not CyEngine().isGlobeviewUp() and pHeadSelectedUnit and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_MINIMAP_ONLY):

			self.setMinimapButtonVisibility(True)

			if (CyInterface().getInterfaceMode() == InterfaceModeTypes.INTERFACEMODE_SELECTION):
			
				if ( pHeadSelectedUnit.getOwner() == gc.getGame().getActivePlayer() and g_pSelectedUnit != pHeadSelectedUnit ):
				
					g_pSelectedUnit = pHeadSelectedUnit
					
					iCount = 0

					actions = CyInterface().getActionsToShow()
					for i in actions:
						screen.appendMultiListButton( "BottomButtonContainer", gc.getActionInfo(i).getButton(), 0, WidgetTypes.WIDGET_ACTION, i, -1, False )
						screen.show( "BottomButtonContainer" )
				
						if ( not CyInterface().canHandleAction(i, False) ):
							screen.disableMultiListButton( "BottomButtonContainer", 0, iCount, gc.getActionInfo(i).getButton() )
							
						if ( pHeadSelectedUnit.isActionRecommended(i) ):#or gc.getActionInfo(i).getCommandType() == CommandTypes.COMMAND_PROMOTION ):
							screen.enableMultiListPulse( "BottomButtonContainer", True, 0, iCount )
						else:
							screen.enableMultiListPulse( "BottomButtonContainer", False, 0, iCount )

						iCount = iCount + 1

					if (CyInterface().canCreateGroup()):
						screen.appendMultiListButton( "BottomButtonContainer", ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_CREATEGROUP").getPath(), 0, WidgetTypes.WIDGET_CREATE_GROUP, -1, -1, False )
						screen.show( "BottomButtonContainer" )
						
						iCount = iCount + 1

					if (CyInterface().canDeleteGroup()):
						screen.appendMultiListButton( "BottomButtonContainer", ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_SPLITGROUP").getPath(), 0, WidgetTypes.WIDGET_DELETE_GROUP, -1, -1, False )
						screen.show( "BottomButtonContainer" )
						
						iCount = iCount + 1

		elif (CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_MINIMAP_ONLY):
		
			self.setMinimapButtonVisibility(True)

		return 0
		
	# Will update the research buttons
	def updateResearchButtons( self ):
	
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )

		for i in range( gc.getNumTechInfos() ):
			szName = "ResearchButton" + str(i)
			screen.hide( szName )

		# Find out our resolution
		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()

		#screen.hide( "InterfaceOrnamentLeftLow" )
		#screen.hide( "InterfaceOrnamentRightLow" )
			
		for i in range(gc.getNumReligionInfos()):
			szName = "ReligionButton" + str(i)
			screen.hide( szName )

		i = 0
		if ( CyInterface().shouldShowResearchButtons() and CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW ):
			iCount = 0
			
			for i in range( gc.getNumTechInfos() ):
				if (gc.getActivePlayer().canResearch(i, False)):
					if (iCount < 20):
						szName = "ResearchButton" + str(i)

						bDone = False
						for j in range( gc.getNumReligionInfos() ):
							if ( not bDone ):
								if (gc.getReligionInfo(j).getTechPrereq() == i):
									if not (gc.getGame().isReligionSlotTaken(j)):
										szName = "ReligionButton" + str(j)
										bDone = True

						screen.show( szName )
						self.setResearchButtonPosition(szName, iCount)

					iCount = iCount + 1
					
		return 0
		
	# Will update the citizen buttons
	def updateCitizenButtons( self ):
	
		global MAX_CITIZEN_BUTTONS
		
		bHandled = False
	
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )

		# Find out our resolution
		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()

		for i in range( MAX_CITIZEN_BUTTONS ):
			szName = "FreeSpecialist" + str(i)
			screen.hide( szName )
			szName = "AngryCitizen" + str(i)
			screen.hide( szName )
			
		for i in range( gc.getNumSpecialistInfos() ):
			szName = "IncreaseSpecialist" + str(i)
			screen.hide( szName )
			szName = "DecreaseSpecialist" + str(i)
			screen.hide( szName )
			szName = "CitizenDisabledButton" + str(i)
			screen.hide( szName )
			for j in range(MAX_CITIZEN_BUTTONS):
				szName = "CitizenButton" + str((i * 100) + j)
				screen.hide( szName )
				szName = "CitizenButtonHighlight" + str((i * 100) + j)
				screen.hide( szName )

		pHeadSelectedCity = CyInterface().getHeadSelectedCity()

		if ( CyInterface().isCityScreenUp() ):
			if (pHeadSelectedCity and CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW):
				if ( pHeadSelectedCity.angryPopulation(0) < MAX_CITIZEN_BUTTONS ):
					iCount = pHeadSelectedCity.angryPopulation(0)
				else:
					iCount = MAX_CITIZEN_BUTTONS

				for i in range(iCount):
					bHandled = True
					szName = "AngryCitizen" + str(i)
					screen.show( szName )

				iFreeSpecialistCount = 0
				for i in range(gc.getNumSpecialistInfos()):
					iFreeSpecialistCount += pHeadSelectedCity.getFreeSpecialistCount(i)

				iCount = 0

				bHandled = False
				
				if (iFreeSpecialistCount > MAX_CITIZEN_BUTTONS):
					for i in range(gc.getNumSpecialistInfos()):
						if (pHeadSelectedCity.getFreeSpecialistCount(i) > 0):
							if (iCount < MAX_CITIZEN_BUTTONS):
								szName = "FreeSpecialist" + str(iCount)
								screen.setImageButton( szName, gc.getSpecialistInfo(i).getTexture(), (xResolution - 74  - (26 * iCount)), yResolution - 206, 24, 24, WidgetTypes.WIDGET_FREE_CITIZEN, i, 1 )
								screen.show( szName )
								bHandled = true
							iCount += 1
							
				else:				
					for i in range(gc.getNumSpecialistInfos()):
						for j in range( pHeadSelectedCity.getFreeSpecialistCount(i) ):
							if (iCount < MAX_CITIZEN_BUTTONS):
								szName = "FreeSpecialist" + str(iCount)
								screen.setImageButton( szName, gc.getSpecialistInfo(i).getTexture(), (xResolution - 74  - (26 * iCount)), yResolution - 206, 24, 24, WidgetTypes.WIDGET_FREE_CITIZEN, i, -1 )
								screen.show( szName )
								bHandled = true

							iCount = iCount + 1

				for i in range( gc.getNumSpecialistInfos() ):
				
					bHandled = False

					if (pHeadSelectedCity.getOwner() == gc.getGame().getActivePlayer() or gc.getGame().isDebugMode()):
					
						if (pHeadSelectedCity.isCitizensAutomated()):
							iSpecialistCount = max(pHeadSelectedCity.getSpecialistCount(i), pHeadSelectedCity.getForceSpecialistCount(i))
						else:
							iSpecialistCount = pHeadSelectedCity.getSpecialistCount(i)
					
						if (pHeadSelectedCity.isSpecialistValid(i, 1) and (pHeadSelectedCity.isCitizensAutomated() or iSpecialistCount < (pHeadSelectedCity.getPopulation() + pHeadSelectedCity.totalFreeSpecialists()))):
							szName = "IncreaseSpecialist" + str(i)
							screen.show( szName )
							szName = "CitizenDisabledButton" + str(i)
							screen.show( szName )

						if iSpecialistCount > 0:
							szName = "CitizenDisabledButton" + str(i)
							screen.hide( szName )
							szName = "DecreaseSpecialist" + str(i)
							screen.show( szName )
							
					if (pHeadSelectedCity.getSpecialistCount(i) < MAX_CITIZEN_BUTTONS):
						iCount = pHeadSelectedCity.getSpecialistCount(i)
					else:
						iCount = MAX_CITIZEN_BUTTONS

					j = 0
					for j in range( iCount ):
						bHandled = True
						szName = "CitizenButton" + str((i * 100) + j)
						screen.addCheckBoxGFC( szName, gc.getSpecialistInfo(i).getTexture(), "", xResolution - 74 - (26 * j), (yResolution - 272 - (26 * i)), 24, 24, WidgetTypes.WIDGET_CITIZEN, i, j, ButtonStyles.BUTTON_STYLE_LABEL )
						screen.show( szName )
						szName = "CitizenButtonHighlight" + str((i * 100) + j)
						screen.addDDSGFC( szName, ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(), xResolution - 74 - (26 * j), (yResolution - 272 - (26 * i)), 24, 24, WidgetTypes.WIDGET_CITIZEN, i, j )
						if ( pHeadSelectedCity.getForceSpecialistCount(i) > j ):
							screen.show( szName )
						else:
							screen.hide( szName )
						
					if ( not bHandled ):
						szName = "CitizenDisabledButton" + str(i)
						screen.show( szName )

		return 0
			
	# Will update the game data strings
	def updateGameDataStrings( self ):
	
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )

		screen.hide( "ResearchText" )
		screen.hide( "GoldText" )
		screen.hide( "TimeText" )
		screen.hide( "ResearchBar" )
		
# BUG - NJAGC - start
		screen.hide( "EraText" )
# BUG - NJAGC - end

# BUG - Great Person Bar - start
		screen.hide( "GreatPersonBar" )
		screen.hide( "GreatPersonBarText" )
# BUG - Great Person Bar - end

		bShift = CyInterface().shiftKey()
		
		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()

		pHeadSelectedCity = CyInterface().getHeadSelectedCity()

		if (pHeadSelectedCity):
			ePlayer = pHeadSelectedCity.getOwner()
		else:
			ePlayer = gc.getGame().getActivePlayer()

		if ( ePlayer < 0 or ePlayer >= gc.getMAX_PLAYERS() ):
			return 0

		for iI in range(CommerceTypes.NUM_COMMERCE_TYPES):
			szString = "PercentText" + str(iI)
			screen.hide(szString)
			szString = "RateText" + str(iI)
			screen.hide(szString)

		if ( CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_MINIMAP_ONLY  and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_ADVANCED_START):

			# Percent of commerce
			if (gc.getPlayer(ePlayer).isAlive()):
				iCount = 0
				for iI in range( CommerceTypes.NUM_COMMERCE_TYPES ):
					eCommerce = (iI + 1) % CommerceTypes.NUM_COMMERCE_TYPES
					if (gc.getPlayer(ePlayer).isCommerceFlexible(eCommerce) or (CyInterface().isCityScreenUp() and (eCommerce == CommerceTypes.COMMERCE_GOLD))):
						szOutText = u"<font=2>%c:%d%%</font>" %(gc.getCommerceInfo(eCommerce).getChar(), gc.getPlayer(ePlayer).getCommercePercent(eCommerce))
						szString = "PercentText" + str(iI)
						screen.setLabel( szString, "Background", szOutText, CvUtil.FONT_LEFT_JUSTIFY, 14, 50 + (iCount * 19), -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
						screen.show( szString )

						if not CyInterface().isCityScreenUp():
							szOutText = u"<font=2>" + localText.getText("TXT_KEY_MISC_POS_GOLD_PER_TURN", (gc.getPlayer(ePlayer).getCommerceRate(CommerceTypes(eCommerce)), )) + u"</font>"
							szString = "RateText" + str(iI)
							screen.setLabel( szString, "Background", szOutText, CvUtil.FONT_LEFT_JUSTIFY, 112, 50 + (iCount * 19), -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
							screen.show( szString )

						iCount = iCount + 1;

			self.updateTimeText()
			screen.setLabel( "TimeText", "Background", g_szTimeText, CvUtil.FONT_RIGHT_JUSTIFY, xResolution - 56, 6, -0.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			screen.show( "TimeText" )
			
			if (gc.getPlayer(ePlayer).isAlive()):
				
				szText = CyGameTextMgr().getGoldStr(ePlayer)
				screen.setLabel( "GoldText", "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, 12, 6, -0.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
				screen.show( "GoldText" )
				
				if (((gc.getPlayer(ePlayer).calculateGoldRate() != 0) and not (gc.getPlayer(ePlayer).isAnarchy())) or (gc.getPlayer(ePlayer).getGold() != 0)):
					screen.show( "GoldText" )

# BUG - NJAGC - start
				if (BugNJAGC.isShowEra()):
					# BUG-TODO: Create text key for "Era"
					szText = gc.getEraInfo(gc.getPlayer(ePlayer).getCurrentEra()).getDescription() + " Era"
					if(BugNJAGC.isUseEraColor()):
						eraColor = BugNJAGC.getEraColor(gc.getEraInfo(gc.getPlayer(ePlayer).getCurrentEra()).getType())
						if (eraColor):
							iColorType = gc.getInfoTypeForString(eraColor)
							if (iColorType >= 0):
								szText = localText.changeTextColor(szText, iColorType)
					screen.setLabel( "EraText", "Background", szText, CvUtil.FONT_RIGHT_JUSTIFY, 250, 6, -0.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
					screen.show( "EraText" )
# BUG - NJAGC - emd
				
# BUG - Combat Counter - start
				if (BugScreens.isShowCombatCounter()
				and not CyInterface().isCityScreenUp()):
					eCombatXPButton = u"<font=2>%c</font>" %(CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR))
					eCombatXPText = ": " + unicode(gc.getPlayer(ePlayer).getCombatExperience()) + "/" + unicode(gc.getPlayer(ePlayer).greatPeopleThreshold(true))
					screen.setLabel( "CombatXPButton", "Background", eCombatXPButton, CvUtil.FONT_RIGHT_JUSTIFY, 220, 50, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
					screen.setLabel( "CombatXPText", "Background", eCombatXPText, CvUtil.FONT_LEFT_JUSTIFY, 220, 50, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
					screen.show( "CombatXPButton" )
					screen.show( "CombatXPText" )
				else:
					screen.hide( "CombatXPButton" )
					screen.hide( "CombatXPText" )
# BUG - Combat Counter - end

				if (gc.getPlayer(ePlayer).isAnarchy()):
				
					szText = localText.getText("INTERFACE_ANARCHY", (gc.getPlayer(ePlayer).getAnarchyTurns(), ))
					screen.setText( "ResearchText", "Background", szText, CvUtil.FONT_CENTER_JUSTIFY, screen.centerX(512), 3, -0.4, FontTypes.GAME_FONT, WidgetTypes.WIDGET_RESEARCH, -1, -1 )
					if ( gc.getPlayer(ePlayer).getCurrentResearch() != -1 ):
						screen.show( "ResearchText" )
					else:
						screen.hide( "ResearchText" )
					
				elif (gc.getPlayer(ePlayer).getCurrentResearch() != -1):

					szText = CyGameTextMgr().getResearchStr(ePlayer)
					screen.setText( "ResearchText", "Background", szText, CvUtil.FONT_CENTER_JUSTIFY, screen.centerX(512), 3, -0.4, FontTypes.GAME_FONT, WidgetTypes.WIDGET_RESEARCH, -1, -1 )
					screen.show( "ResearchText" )

					researchProgress = gc.getTeam(gc.getPlayer(ePlayer).getTeam()).getResearchProgress(gc.getPlayer(ePlayer).getCurrentResearch())
					overflowResearch = (gc.getPlayer(ePlayer).getOverflowResearch() * gc.getPlayer(ePlayer).calculateResearchModifier(gc.getPlayer(ePlayer).getCurrentResearch()))/100
					researchCost = gc.getTeam(gc.getPlayer(ePlayer).getTeam()).getResearchCost(gc.getPlayer(ePlayer).getCurrentResearch())
					researchRate = gc.getPlayer(ePlayer).calculateResearchRate(-1)
					
					iFirst = float(researchProgress + overflowResearch) / float(researchCost)
					screen.setBarPercentage( "ResearchBar", InfoBarTypes.INFOBAR_STORED, iFirst )
					if ( iFirst == 1 ):
						screen.setBarPercentage( "ResearchBar", InfoBarTypes.INFOBAR_RATE, ( float(researchRate) / float(researchCost) ) )
					else:
						screen.setBarPercentage( "ResearchBar", InfoBarTypes.INFOBAR_RATE, ( ( float(researchRate) / float(researchCost) ) ) / ( 1 - iFirst ) )

					screen.show( "ResearchBar" )
					
# BUG - Great Person Bar - start
				if (not CyInterface().isCityScreenUp() and BugScreens.isShowGPProgressBar()):				
					pGreatPersonCity, iGPTurns = self.getNextGPCity()
					if (iGPTurns < 10000000 and pGreatPersonCity):
						szText = localText.getText("INTERFACE_NEXT_GREATPERSON_CITY_TURNS", (pGreatPersonCity.getName(), iGPTurns))
						screen.setText( "GreatPersonBarText", "Background", szText, CvUtil.FONT_CENTER_JUSTIFY, screen.centerX(512), 28, -0.4, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, pGreatPersonCity.getID(), -1 )
#						screen.setHitTest( "GreatPersonBarText", HitTestTypes.HITTEST_NOHIT )
						screen.show( "GreatPersonBarText" )
						
						iFirst = float(pGreatPersonCity.getGreatPeopleProgress()) / float( gc.getPlayer( pGreatPersonCity.getOwner() ).greatPeopleThreshold(false) )
						screen.setBarPercentage( "GreatPersonBar", InfoBarTypes.INFOBAR_STORED, iFirst )
						if ( iFirst == 1 ):
							screen.setBarPercentage( "GreatPersonBar", InfoBarTypes.INFOBAR_RATE, ( float(pGreatPersonCity.getGreatPeopleRate()) / float( gc.getPlayer( pGreatPersonCity.getOwner() ).greatPeopleThreshold(false) ) ) )
						else:
							screen.setBarPercentage( "GreatPersonBar", InfoBarTypes.INFOBAR_RATE, ( ( float(pGreatPersonCity.getGreatPeopleRate()) / float( gc.getPlayer( pGreatPersonCity.getOwner() ).greatPeopleThreshold(false) ) ) ) / ( 1 - iFirst ) )				
						screen.show( "GreatPersonBar" )
					else:	
						screen.hide( "GreatPersonBar" )
						screen.hide( "GreatPersonBarText" )
# BUG - Great Person Bar - end
					
		return 0
								
# BUG - Great Person Bar - start
	def getNextGPCity( self ):
	
		iFastestPerson = 10000000
		iGPTurns = 0
		pPlayer = gc.getPlayer(gc.getGame().getActivePlayer())
		iGPNext = pPlayer.greatPeopleThreshold(false)
		pFastestCity = CyInterface().getHeadSelectedCity()
		
		for icity in range(pPlayer.getNumCities()):
			pCity = pPlayer.getCity(icity)
			if (pCity):
				iGPRate = pCity.getGreatPeopleRate()
				if (iGPRate > 0):
					iGPNow = pCity.getGreatPeopleProgress()
					iGPTurns = (iGPNext - iGPNow + iGPRate - 1) / iGPRate
					if (iGPTurns < iFastestPerson):
						iFastestPerson = iGPTurns
						pFastestCity = pCity
		
		return (pFastestCity, iFastestPerson)
# BUG - Great Person Bar - end
		
	def updateTimeText( self ):
		
		global g_szTimeText
		
		ePlayer = gc.getGame().getActivePlayer()
		
# BUG - NJAGC - start
		if (BugNJAGC.isEnabled()):
			"""
			Format: Time - GameTurn/Total Percent - GA (TurnsLeft) Date
			
			Ex: 10:37 - 220/660 33% - GA (3) 1925
			"""
			if (g_bShowTimeTextAlt):
				bShowTime = BugNJAGC.isShowAltTime()
				bShowGameTurn = BugNJAGC.isShowAltGameTurn()
				bShowTotalTurns = BugNJAGC.isShowAltTotalTurns()
				bShowPercentComplete = BugNJAGC.isShowAltPercentComplete()
				bShowDateGA = BugNJAGC.isShowAltDateGA()
			else:
				bShowTime = BugNJAGC.isShowTime()
				bShowGameTurn = BugNJAGC.isShowGameTurn()
				bShowTotalTurns = BugNJAGC.isShowTotalTurns()
				bShowPercentComplete = BugNJAGC.isShowPercentComplete()
				bShowDateGA = BugNJAGC.isShowDateGA()
			
			if (not gc.getGame().getMaxTurns() > 0):
				bShowTotalTurns = False
				bShowPercentComplete = False
			
			bFirst = True
			g_szTimeText = ""
			
			if (bShowTime):
				bFirst = False
				g_szTimeText += getClockText()
			
			if (bShowGameTurn):
				if (bFirst):
					bFirst = False
				else:
					g_szTimeText += u" - "
				g_szTimeText += u"%d" %( gc.getGame().getElapsedGameTurns() )
				if (bShowTotalTurns):
					g_szTimeText += u"/%d" %( gc.getGame().getMaxTurns() )
			
			if (bShowPercentComplete):
				if (bFirst):
					bFirst = False
				else:
					if (not bShowGameTurn):
						g_szTimeText += u" - "
					else:
						g_szTimeText += u" "
				g_szTimeText += u"%2.2f%%" %( 100 *(float(gc.getGame().getElapsedGameTurns()) / float(gc.getGame().getMaxTurns())) )
			
			if (bShowDateGA):
				if (bFirst):
					bFirst = False
				else:
					g_szTimeText += u" - "
				szDateGA = unicode(CyGameTextMgr().getInterfaceTimeStr(ePlayer))
				if(BugNJAGC.isUseEraColor()):
					eraColor = BugNJAGC.getEraColor(gc.getEraInfo(gc.getPlayer(ePlayer).getCurrentEra()).getType())
					if (eraColor):
						iColorType = gc.getInfoTypeForString(eraColor)
						if (iColorType >= 0):
							szDateGA = localText.changeTextColor(szDateGA, iColorType)
				g_szTimeText += szDateGA
		else:
			"""
			Original Clock
			Format: Time - 'Turn' GameTurn - GA (TurnsLeft) Date
			
			Ex: 10:37 - Turn 220 - GA (3) 1925
			"""
			g_szTimeText = localText.getText("TXT_KEY_TIME_TURN", (CyGame().getGameTurn(), )) + u" - " + unicode(CyGameTextMgr().getInterfaceTimeStr(ePlayer))
			if (CyUserProfile().isClockOn()):
				g_szTimeText = getClockText() + u" - " + g_szTimeText
# BUG - NJAGC - end
		
	# Will update the selection Data Strings
	def updateCityScreen( self ):
	
		global MAX_DISPLAYABLE_BUILDINGS
		global MAX_DISPLAYABLE_TRADE_ROUTES
		global MAX_BONUS_ROWS
		
		global g_iNumTradeRoutes
		global g_iNumBuildings
		global g_iNumLeftBonus
		global g_iNumCenterBonus
		global g_iNumRightBonus
	
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )

		pHeadSelectedCity = CyInterface().getHeadSelectedCity()

		# Find out our resolution
		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()

		bShift = CyInterface().shiftKey()

		screen.hide( "PopulationBar" )
		screen.hide( "ProductionBar" )
		screen.hide( "GreatPeopleBar" )
		screen.hide( "CultureBar" )
		screen.hide( "MaintenanceText" )
		screen.hide( "MaintenanceAmountText" )
		
# BUG - Raw Commerce - start
		screen.hide( "RawWorkedPlotsLabel" )
		screen.hide( "RawTradeRoutesSpecsLabel" )
		screen.hide( "RawBuildingsLabel" )
		screen.hide( "RawTotalLabel" )
		screen.hide( "RawToggleButton" )
		screen.hide( "RawWorkedPlotsText" )
		screen.hide( "RawTradeRoutesSpecsText" )
		screen.hide( "RawBuildingsText" )
		screen.hide( "RawTotalText" )
# BUG - Raw Commerce - end
		
		screen.hide( "NationalityText" )
		screen.hide( "NationalityBar" )
		screen.hide( "DefenseText" )
		screen.hide( "CityScrollMinus" )
		screen.hide( "CityScrollPlus" )
		screen.hide( "CityNameText" )
		screen.hide( "PopulationText" )
		screen.hide( "PopulationInputText" )
		screen.hide( "HealthText" )
		screen.hide( "ProductionText" )
		screen.hide( "ProductionInputText" )
		screen.hide( "HappinessText" )
		screen.hide( "CultureText" )
		screen.hide( "GreatPeopleText" )

		for i in range( gc.getNumReligionInfos() ):
			szName = "ReligionHolyCityDDS" + str(i)
			screen.hide( szName )
			szName = "ReligionDDS" + str(i)
			screen.hide( szName )
			
		for i in range( gc.getNumCorporationInfos() ):
			szName = "CorporationHeadquarterDDS" + str(i)
			screen.hide( szName )
			szName = "CorporationDDS" + str(i)
			screen.hide( szName )
			
		for i in range(CommerceTypes.NUM_COMMERCE_TYPES):
			szName = "CityPercentText" + str(i)
			screen.hide( szName )

		screen.addPanel( "BonusPane0", u"", u"", True, False, xResolution - 244, 94, 57, yResolution - 520, PanelStyles.PANEL_STYLE_CITY_COLUMNL )
		screen.hide( "BonusPane0" )
		screen.addScrollPanel( "BonusBack0", u"", xResolution - 242, 94, 157, yResolution - 536, PanelStyles.PANEL_STYLE_EXTERNAL )
		screen.hide( "BonusBack0" )

		screen.addPanel( "BonusPane1", u"", u"", True, False, xResolution - 187, 94, 68, yResolution - 520, PanelStyles.PANEL_STYLE_CITY_COLUMNC )
		screen.hide( "BonusPane1" )
		screen.addScrollPanel( "BonusBack1", u"", xResolution - 191, 94, 184, yResolution - 536, PanelStyles.PANEL_STYLE_EXTERNAL )
		screen.hide( "BonusBack1" )

		screen.addPanel( "BonusPane2", u"", u"", True, False, xResolution - 119, 94, 107, yResolution - 520, PanelStyles.PANEL_STYLE_CITY_COLUMNR )
		screen.hide( "BonusPane2" )
		screen.addScrollPanel( "BonusBack2", u"", xResolution - 125, 94, 205, yResolution - 536, PanelStyles.PANEL_STYLE_EXTERNAL )
		screen.hide( "BonusBack2" )

		screen.hide( "TradeRouteTable" )
		screen.hide( "BuildingListTable" )
		
		screen.hide( "BuildingListBackground" )
		screen.hide( "TradeRouteListBackground" )
		screen.hide( "BuildingListLabel" )
		screen.hide( "TradeRouteListLabel" )

		i = 0
		for i in range( g_iNumLeftBonus ):
			szName = "LeftBonusItem" + str(i)
			screen.hide( szName )
		
		i = 0
		for i in range( g_iNumCenterBonus ):
			szName = "CenterBonusItemLeft" + str(i)
			screen.hide( szName )
			szName = "CenterBonusItemRight" + str(i)
			screen.hide( szName )
		
		i = 0
		for i in range( g_iNumRightBonus ):
			szName = "RightBonusItemLeft" + str(i)
			screen.hide( szName )
			szName = "RightBonusItemRight" + str(i)
			screen.hide( szName )
			
		i = 0
		for i in range( 3 ):
			szName = "BonusPane" + str(i)
			screen.hide( szName )
			szName = "BonusBack" + str(i)
			screen.hide( szName )

		i = 0
		if ( CyInterface().isCityScreenUp() ):
			if ( pHeadSelectedCity ):
			
				screen.show( "InterfaceTopLeftBackgroundWidget" )
				screen.show( "InterfaceTopRightBackgroundWidget" )
				screen.show( "InterfaceCenterLeftBackgroundWidget" )
				screen.show( "CityScreenTopWidget" )
				screen.show( "CityNameBackground" )
				screen.show( "TopCityPanelLeft" )
				screen.show( "TopCityPanelRight" )
				screen.show( "CityScreenAdjustPanel" )
				screen.show( "InterfaceCenterRightBackgroundWidget" )
				
				if ( pHeadSelectedCity.getTeam() == gc.getGame().getActiveTeam() ):
					if ( gc.getActivePlayer().getNumCities() > 1 ):
						screen.show( "CityScrollMinus" )
						screen.show( "CityScrollPlus" )
				
				# Help Text Area
				screen.setHelpTextArea( 390, FontTypes.SMALL_FONT, 0, 0, -2.2, True, ArtFileMgr.getInterfaceArtInfo("POPUPS_BACKGROUND_TRANSPARENT").getPath(), True, True, CvUtil.FONT_LEFT_JUSTIFY, 0 )

				iFoodDifference = pHeadSelectedCity.foodDifference(True)
				iProductionDiffNoFood = pHeadSelectedCity.getCurrentProductionDifference(True, True)
				iProductionDiffJustFood = (pHeadSelectedCity.getCurrentProductionDifference(False, True) - iProductionDiffNoFood)

				szBuffer = u"<font=4>"
				
				if (pHeadSelectedCity.isCapital()):
					szBuffer += u"%c" %(CyGame().getSymbolID(FontSymbols.STAR_CHAR))
				elif (pHeadSelectedCity.isGovernmentCenter()):
					szBuffer += u"%c" %(CyGame().getSymbolID(FontSymbols.SILVER_STAR_CHAR))

				if (pHeadSelectedCity.isPower()):
					szBuffer += u"%c" %(CyGame().getSymbolID(FontSymbols.POWER_CHAR))
					
				szBuffer += u"%s: %d" %(pHeadSelectedCity.getName(), pHeadSelectedCity.getPopulation())

				if (pHeadSelectedCity.isOccupation()):
					szBuffer += u" (%c:%d)" %(CyGame().getSymbolID(FontSymbols.OCCUPATION_CHAR), pHeadSelectedCity.getOccupationTimer())

				szBuffer += u"</font>"

				screen.setText( "CityNameText", "Background", szBuffer, CvUtil.FONT_CENTER_JUSTIFY, screen.centerX(512), 32, -0.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_CITY_NAME, -1, -1 )
				screen.setStyle( "CityNameText", "Button_Stone_Style" )
				screen.show( "CityNameText" )

				if ( (iFoodDifference != 0) or not (pHeadSelectedCity.isFoodProduction() ) ):
					if (iFoodDifference > 0):
						szBuffer = localText.getText("INTERFACE_CITY_GROWING", (pHeadSelectedCity.getFoodTurnsLeft(), ))	
					elif (iFoodDifference < 0):
						szBuffer = localText.getText("INTERFACE_CITY_STARVING", ())	
					else:
						szBuffer = localText.getText("INTERFACE_CITY_STAGNANT", ())	

					screen.setLabel( "PopulationText", "Background", szBuffer, CvUtil.FONT_CENTER_JUSTIFY, screen.centerX(512), iCityCenterRow1Y, -1.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
					screen.setHitTest( "PopulationText", HitTestTypes.HITTEST_NOHIT )
					screen.show( "PopulationText" )

				if (not pHeadSelectedCity.isDisorder() and not pHeadSelectedCity.isFoodProduction()):
				
					szBuffer = u"%d%c - %d%c" %(pHeadSelectedCity.getYieldRate(YieldTypes.YIELD_FOOD), gc.getYieldInfo(YieldTypes.YIELD_FOOD).getChar(), pHeadSelectedCity.foodConsumption(False, 0), CyGame().getSymbolID(FontSymbols.EATEN_FOOD_CHAR))
					screen.setLabel( "PopulationInputText", "Background", szBuffer, CvUtil.FONT_RIGHT_JUSTIFY, iCityCenterRow1X - 6, iCityCenterRow1Y, -0.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
					screen.show( "PopulationInputText" )
					
				else:
				
					szBuffer = u"%d%c" %(iFoodDifference, gc.getYieldInfo(YieldTypes.YIELD_FOOD).getChar())
					screen.setLabel( "PopulationInputText", "Background", szBuffer, CvUtil.FONT_RIGHT_JUSTIFY, iCityCenterRow1X - 6, iCityCenterRow1Y, -0.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
					screen.show( "PopulationInputText" )

				if ((pHeadSelectedCity.badHealth(False) > 0) or (pHeadSelectedCity.goodHealth() >= 0)):
					if (pHeadSelectedCity.healthRate(False, 0) < 0):
						szBuffer = localText.getText("INTERFACE_CITY_HEALTH_BAD", (pHeadSelectedCity.goodHealth(), pHeadSelectedCity.badHealth(False), pHeadSelectedCity.healthRate(False, 0)))
					elif (pHeadSelectedCity.badHealth(False) > 0):
						szBuffer = localText.getText("INTERFACE_CITY_HEALTH_GOOD", (pHeadSelectedCity.goodHealth(), pHeadSelectedCity.badHealth(False)))
					else:
						szBuffer = localText.getText("INTERFACE_CITY_HEALTH_GOOD_NO_BAD", (pHeadSelectedCity.goodHealth(), ))
						
					screen.setLabel( "HealthText", "Background", szBuffer, CvUtil.FONT_LEFT_JUSTIFY, xResolution - iCityCenterRow1X + 6, iCityCenterRow1Y, -0.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_HELP_HEALTH, -1, -1 )
					screen.show( "HealthText" )

				if (iFoodDifference < 0):

					if ( pHeadSelectedCity.getFood() + iFoodDifference > 0 ):
						iDeltaFood = pHeadSelectedCity.getFood() + iFoodDifference
					else:
						iDeltaFood = 0
					if ( -iFoodDifference < pHeadSelectedCity.getFood() ):
						iExtraFood = -iFoodDifference
					else:
						iExtraFood = pHeadSelectedCity.getFood()
					iFirst = float(iDeltaFood) / float(pHeadSelectedCity.growthThreshold())
					screen.setBarPercentage( "PopulationBar", InfoBarTypes.INFOBAR_STORED, iFirst )
					screen.setBarPercentage( "PopulationBar", InfoBarTypes.INFOBAR_RATE, 0.0 )
					if ( iFirst == 1 ):
						screen.setBarPercentage( "PopulationBar", InfoBarTypes.INFOBAR_RATE_EXTRA, ( float(iExtraFood) / float(pHeadSelectedCity.growthThreshold()) ) )
					else:
						screen.setBarPercentage( "PopulationBar", InfoBarTypes.INFOBAR_RATE_EXTRA, ( ( float(iExtraFood) / float(pHeadSelectedCity.growthThreshold()) ) ) / ( 1 - iFirst ) )
					
				else:

					iFirst = float(pHeadSelectedCity.getFood()) / float(pHeadSelectedCity.growthThreshold())
					screen.setBarPercentage( "PopulationBar", InfoBarTypes.INFOBAR_STORED, iFirst )
					if ( iFirst == 1 ):
						screen.setBarPercentage( "PopulationBar", InfoBarTypes.INFOBAR_RATE, ( float(iFoodDifference) / float(pHeadSelectedCity.growthThreshold()) ) )
					else:
						screen.setBarPercentage( "PopulationBar", InfoBarTypes.INFOBAR_RATE, ( ( float(iFoodDifference) / float(pHeadSelectedCity.growthThreshold()) ) ) / ( 1 - iFirst ) )
					screen.setBarPercentage( "PopulationBar", InfoBarTypes.INFOBAR_RATE_EXTRA, 0.0 )
					
				screen.show( "PopulationBar" )

# BUG - Whip Assist - start

				if (pHeadSelectedCity.getOrderQueueLength() > 0):
					if (pHeadSelectedCity.isProductionProcess()):
						szBuffer = pHeadSelectedCity.getProductionName()
					else:
						szBuffer = localText.getText("INTERFACE_CITY_PRODUCTION", (pHeadSelectedCity.getProductionNameKey(), pHeadSelectedCity.getProductionTurnsLeft()))

					screen.setLabel( "ProductionText", "Background", szBuffer, CvUtil.FONT_CENTER_JUSTIFY, screen.centerX(512), iCityCenterRow2Y, -1.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
					screen.setHitTest( "ProductionText", HitTestTypes.HITTEST_NOHIT )
					screen.show( "ProductionText" )
				
				if (pHeadSelectedCity.isProductionProcess()):
					szBuffer = u"%d%c" %(pHeadSelectedCity.getYieldRate(YieldTypes.YIELD_PRODUCTION), gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getChar())
				elif (pHeadSelectedCity.isFoodProduction() and (iProductionDiffJustFood > 0)):
					szBuffer = u"%d%c + %d%c" %(iProductionDiffJustFood, gc.getYieldInfo(YieldTypes.YIELD_FOOD).getChar(), iProductionDiffNoFood, gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getChar())
				else:
					szBuffer = u"%d%c" %(iProductionDiffNoFood, gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getChar())
					
				screen.setLabel( "ProductionInputText", "Background", szBuffer, CvUtil.FONT_RIGHT_JUSTIFY, iCityCenterRow1X - 6, iCityCenterRow2Y, -0.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_PRODUCTION_MOD_HELP, -1, -1 )
				screen.show( "ProductionInputText" )

				if ((pHeadSelectedCity.happyLevel() >= 0) or (pHeadSelectedCity.unhappyLevel(0) > 0)):
					if (pHeadSelectedCity.isDisorder()):
						szBuffer = u"%d%c" %(pHeadSelectedCity.angryPopulation(0), CyGame().getSymbolID(FontSymbols.ANGRY_POP_CHAR))
					elif (pHeadSelectedCity.angryPopulation(0) > 0):
						szBuffer = localText.getText("INTERFACE_CITY_UNHAPPY", (pHeadSelectedCity.happyLevel(), pHeadSelectedCity.unhappyLevel(0), pHeadSelectedCity.angryPopulation(0)))
					elif (pHeadSelectedCity.unhappyLevel(0) > 0):
						szBuffer = localText.getText("INTERFACE_CITY_HAPPY", (pHeadSelectedCity.happyLevel(), pHeadSelectedCity.unhappyLevel(0)))
					else:
						szBuffer = localText.getText("INTERFACE_CITY_HAPPY_NO_UNHAPPY", (pHeadSelectedCity.happyLevel(), ))

					screen.setLabel( "HappinessText", "Background", szBuffer, CvUtil.FONT_LEFT_JUSTIFY, xResolution - iCityCenterRow1X + 6, iCityCenterRow2Y, -0.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_HELP_HAPPINESS, -1, -1 )
					screen.show( "HappinessText" )

				if (not(pHeadSelectedCity.isProductionProcess())):
				
					iFirst = ((float(pHeadSelectedCity.getProduction())) / (float(pHeadSelectedCity.getProductionNeeded())))
					screen.setBarPercentage( "ProductionBar", InfoBarTypes.INFOBAR_STORED, iFirst )
					if ( iFirst == 1 ):
						iSecond = ( ((float(iProductionDiffNoFood)) / (float(pHeadSelectedCity.getProductionNeeded()))) )
					else:
						iSecond = ( ((float(iProductionDiffNoFood)) / (float(pHeadSelectedCity.getProductionNeeded()))) ) / ( 1 - iFirst )
					screen.setBarPercentage( "ProductionBar", InfoBarTypes.INFOBAR_RATE, iSecond )
					if ( iFirst + iSecond == 1 ):
						screen.setBarPercentage( "ProductionBar", InfoBarTypes.INFOBAR_RATE_EXTRA, ( ((float(iProductionDiffJustFood)) / (float(pHeadSelectedCity.getProductionNeeded()))) ) )
					else:
						screen.setBarPercentage( "ProductionBar", InfoBarTypes.INFOBAR_RATE_EXTRA, ( ( ((float(iProductionDiffJustFood)) / (float(pHeadSelectedCity.getProductionNeeded()))) ) ) / ( 1 - ( iFirst + iSecond ) ) )

					screen.show( "ProductionBar" )

				iCount = 0

				for i in range(CommerceTypes.NUM_COMMERCE_TYPES):
					eCommerce = (i + 1) % CommerceTypes.NUM_COMMERCE_TYPES

					if ((gc.getPlayer(pHeadSelectedCity.getOwner()).isCommerceFlexible(eCommerce)) or (eCommerce == CommerceTypes.COMMERCE_GOLD)):
						szBuffer = u"%d.%02d %c" %(pHeadSelectedCity.getCommerceRate(eCommerce), pHeadSelectedCity.getCommerceRateTimes100(eCommerce)%100, gc.getCommerceInfo(eCommerce).getChar())

						iHappiness = pHeadSelectedCity.getCommerceHappinessByType(eCommerce)

						if (iHappiness != 0):
							if ( iHappiness > 0 ):
								szTempBuffer = u", %d%c" %(iHappiness, CyGame().getSymbolID(FontSymbols.HAPPY_CHAR))
							else:
								szTempBuffer = u", %d%c" %(-iHappiness, CyGame().getSymbolID(FontSymbols.UNHAPPY_CHAR))
							szBuffer = szBuffer + szTempBuffer

						szName = "CityPercentText" + str(iCount)
						screen.setLabel( szName, "Background", szBuffer, CvUtil.FONT_RIGHT_JUSTIFY, 220, 45 + (19 * iCount) + 4, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_COMMERCE_MOD_HELP, eCommerce, -1 )
						screen.show( szName )
						iCount = iCount + 1

				iCount = 0

# BUG - Raw Commerce - start
				iLabelHeight = 30
				bShowRawCommerce = BugCityScreen.isShowRawCommerce()
				if (bShowRawCommerce):
					screen.show( "RawCommercePanel" )
					iRawCommerceTop = 154 # from above
					iRawCommerceHeight = 90
					iTradeRouteTableTop = iRawCommerceTop + iRawCommerceHeight + 5 + iLabelHeight
					iBuildingListTableTop = iTradeRouteTableTop + 130
				else:
					iTradeRouteTableTop = 157 + iLabelHeight
					iBuildingListTableTop = 287 + iLabelHeight
					
				screen.addTableControlGFC( "TradeRouteTable", 3, 10, iTradeRouteTableTop, 238, 98, False, False, 32, 32, TableStyles.TABLE_STYLE_STANDARD )
				screen.setStyle( "TradeRouteTable", "Table_City_Style" )
				screen.addTableControlGFC( "BuildingListTable", 3, 10, iBuildingListTableTop, 238, yResolution - iBuildingListTableTop - 214, False, False, 32, 32, TableStyles.TABLE_STYLE_STANDARD )
				screen.setStyle( "BuildingListTable", "Table_City_Style" )
# BUG - Raw Commerce - end
				
				screen.setTableColumnHeader( "TradeRouteTable", 0, u"", 108 )
				screen.setTableColumnHeader( "TradeRouteTable", 1, u"", 118 )
				screen.setTableColumnHeader( "TradeRouteTable", 2, u"", 10 )
				screen.setTableColumnRightJustify( "TradeRouteTable", 1 )

				screen.setTableColumnHeader( "BuildingListTable", 0, u"", 108 )
				screen.setTableColumnHeader( "BuildingListTable", 1, u"", 118 )
				screen.setTableColumnHeader( "BuildingListTable", 2, u"", 10 )
				screen.setTableColumnRightJustify( "BuildingListTable", 1 )

# BUG - Raw Commerce - start
				iRawCommerceTop = 154
				iRawCommerceHeight = 90

				if (bShowRawCommerce):
					iTradeRouteListTop = iRawCommerceTop + iRawCommerceHeight + 5
					iBuildingListTop = iTradeRouteListTop + 130
				else:
					iTradeRouteListTop = 157
					iBuildingListTop = 287

				screen.addPanel( "TradeRouteListBackground", u"", u"", True, False, 10, iTradeRouteListTop, 238, 30, PanelStyles.PANEL_STYLE_STANDARD )
				screen.setStyle( "TradeRouteListBackground", "Panel_City_Header_Style" )

				screen.setLabel( "TradeRouteListLabel", "Background", localText.getText("TXT_KEY_HEADING_TRADEROUTE_LIST", ()), CvUtil.FONT_CENTER_JUSTIFY, 129, iTradeRouteListTop + 8, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )

				screen.addPanel( "BuildingListBackground", u"", u"", True, False, 10, iBuildingListTop, 238, 30, PanelStyles.PANEL_STYLE_STANDARD )
				screen.setStyle( "BuildingListBackground", "Panel_City_Header_Style" )

				screen.setLabel( "BuildingListLabel", "Background", localText.getText("TXT_KEY_CONCEPT_BUILDINGS", ()), CvUtil.FONT_CENTER_JUSTIFY, 129, iBuildingListTop + 8, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
# BUG - Raw Commerce - end

				screen.show( "BuildingListBackground" )
				screen.show( "TradeRouteListBackground" )
				screen.show( "BuildingListLabel" )
				screen.show( "TradeRouteListLabel" )
				
				for i in range( 3 ):
					szName = "BonusPane" + str(i)
					screen.show( szName )
					szName = "BonusBack" + str(i)
					screen.show( szName )

				i = 0
				iNumBuildings = 0
# BUG - Raw Commerce - start
				iBuildingsYield = 0
				iBuildingsProdYield = 0
# BUG - Raw Commerce - end
				for i in range( gc.getNumBuildingInfos() ):
					if (pHeadSelectedCity.getNumBuilding(i) > 0):

						for k in range(pHeadSelectedCity.getNumBuilding(i)):
							
							szLeftBuffer = gc.getBuildingInfo(i).getDescription()
							szRightBuffer = u""
							bFirst = True
							
							if (pHeadSelectedCity.getNumActiveBuilding(i) > 0):
								iHealth = pHeadSelectedCity.getBuildingHealth(i)

								if (iHealth != 0):
									if ( bFirst == False ):
										szRightBuffer = szRightBuffer + ", "
									else:
										bFirst = False
										
									if ( iHealth > 0 ):
										szTempBuffer = u"+%d%c" %( iHealth, CyGame().getSymbolID(FontSymbols.HEALTHY_CHAR) )
										szRightBuffer = szRightBuffer + szTempBuffer
									else:
										szTempBuffer = u"+%d%c" %( -(iHealth), CyGame().getSymbolID(FontSymbols.UNHEALTHY_CHAR) )
										szRightBuffer = szRightBuffer + szTempBuffer

								iHappiness = pHeadSelectedCity.getBuildingHappiness(i)

								if (iHappiness != 0):
									if ( bFirst == False ):
										szRightBuffer = szRightBuffer + ", "
									else:
										bFirst = False
										
									if ( iHappiness > 0 ):
										szTempBuffer = u"+%d%c" %(iHappiness, CyGame().getSymbolID(FontSymbols.HAPPY_CHAR) )
										szRightBuffer = szRightBuffer + szTempBuffer
									else:
										szTempBuffer = u"+%d%c" %( -(iHappiness), CyGame().getSymbolID(FontSymbols.UNHAPPY_CHAR) )
										szRightBuffer = szRightBuffer + szTempBuffer

								for j in range( YieldTypes.NUM_YIELD_TYPES):
									iYield = gc.getBuildingInfo(i).getYieldChange(j) + pHeadSelectedCity.getNumBuilding(i) * pHeadSelectedCity.getBuildingYieldChange(gc.getBuildingInfo(i).getBuildingClassType(), j)

									if (iYield != 0):
										if ( bFirst == False ):
											szRightBuffer = szRightBuffer + ", "
										else:
											bFirst = False
											
										if ( iYield > 0 ):
											szTempBuffer = u"%s%d%c" %( "+", iYield, gc.getYieldInfo(j).getChar() )
											szRightBuffer = szRightBuffer + szTempBuffer
										else:
											szTempBuffer = u"%s%d%c" %( "", iYield, gc.getYieldInfo(j).getChar() )
											szRightBuffer = szRightBuffer + szTempBuffer
										
# BUG - Raw Commerce - start
										if (j == YieldTypes.YIELD_COMMERCE):
											iBuildingsYield += iYield
										elif (j == YieldTypes.YIELD_PRODUCTION):
											iBuildingsProdYield += iYield
# BUG - Raw Commerce - end

							for j in range(CommerceTypes.NUM_COMMERCE_TYPES):
								iCommerce = pHeadSelectedCity.getBuildingCommerceByBuilding(j, i) / pHeadSelectedCity.getNumBuilding(i)
	
								if (iCommerce != 0):
									if ( bFirst == False ):
										szRightBuffer = szRightBuffer + ", "
									else:
										bFirst = False
										
									if ( iCommerce > 0 ):
										szTempBuffer = u"%s%d%c" %( "+", iCommerce, gc.getCommerceInfo(j).getChar() )
										szRightBuffer = szRightBuffer + szTempBuffer
									else:
										szTempBuffer = u"%s%d%c" %( "", iCommerce, gc.getCommerceInfo(j).getChar() )
										szRightBuffer = szRightBuffer + szTempBuffer
	
							szBuffer = szLeftBuffer + "  " + szRightBuffer
							
							screen.appendTableRow( "BuildingListTable" )
							screen.setTableText( "BuildingListTable", 0, iNumBuildings, "<font=1>" + szLeftBuffer + "</font>", "", WidgetTypes.WIDGET_HELP_BUILDING, i, -1, CvUtil.FONT_LEFT_JUSTIFY )
							screen.setTableText( "BuildingListTable", 1, iNumBuildings, "<font=1>" + szRightBuffer + "</font>", "", WidgetTypes.WIDGET_HELP_BUILDING, i, -1, CvUtil.FONT_RIGHT_JUSTIFY )
							
							iNumBuildings = iNumBuildings + 1
						
				if ( iNumBuildings > g_iNumBuildings ):
					g_iNumBuildings = iNumBuildings
					
				iNumTradeRoutes = 0
# BUG - Raw Commerce - start
				iNetTradeYield = 0
# BUG - Raw Commerce - end
				
				for i in range(gc.getDefineINT("MAX_TRADE_ROUTES")):
					pLoopCity = pHeadSelectedCity.getTradeCity(i)

					if (pLoopCity and pLoopCity.getOwner() >= 0):
						player = gc.getPlayer(pLoopCity.getOwner())
						szLeftBuffer = u"<color=%d,%d,%d,%d>%s</color>" %(player.getPlayerTextColorR(), player.getPlayerTextColorG(), player.getPlayerTextColorB(), player.getPlayerTextColorA(), pLoopCity.getName() )
						szRightBuffer = u""

						for j in range( YieldTypes.NUM_YIELD_TYPES ):
							iTradeProfit = pHeadSelectedCity.calculateTradeYield(j, pHeadSelectedCity.calculateTradeProfit(pLoopCity))

							if (iTradeProfit != 0):
								if ( iTradeProfit > 0 ):
									szTempBuffer = u"%s%d%c" %( "+", iTradeProfit, gc.getYieldInfo(j).getChar() )
									szRightBuffer = szRightBuffer + szTempBuffer
								else:
									szTempBuffer = u"%s%d%c" %( "", iTradeProfit, gc.getYieldInfo(j).getChar() )
									szRightBuffer = szRightBuffer + szTempBuffer

						screen.appendTableRow( "TradeRouteTable" )
						screen.setTableText( "TradeRouteTable", 0, iNumTradeRoutes, "<font=1>" + szLeftBuffer + "</font>", "", WidgetTypes.WIDGET_HELP_TRADE_ROUTE_CITY, i, -1, CvUtil.FONT_LEFT_JUSTIFY )
						screen.setTableText( "TradeRouteTable", 1, iNumTradeRoutes, "<font=1>" + szRightBuffer + "</font>", "", WidgetTypes.WIDGET_HELP_TRADE_ROUTE_CITY, i, -1, CvUtil.FONT_RIGHT_JUSTIFY )
						
						iNumTradeRoutes = iNumTradeRoutes + 1
# BUG - Raw Commerce - start
						iNetTradeYield += iTradeProfit
# BUG - Raw Commerce - end
						
				if ( iNumTradeRoutes > g_iNumTradeRoutes ):
					g_iNumTradeRoutes = iNumTradeRoutes

				i = 0  
				iLeftCount = 0
				iCenterCount = 0
				iRightCount = 0

				for i in range( gc.getNumBonusInfos() ):
					bHandled = False
					if ( pHeadSelectedCity.hasBonus(i) ):

						iHealth = pHeadSelectedCity.getBonusHealth(i)
						iHappiness = pHeadSelectedCity.getBonusHappiness(i)
						
						szBuffer = u""
						szLeadBuffer = u""

						szTempBuffer = u"<font=1>%c" %( gc.getBonusInfo(i).getChar() )
						szLeadBuffer = szLeadBuffer + szTempBuffer
						
						if (pHeadSelectedCity.getNumBonuses(i) > 1):
							szTempBuffer = u"(%d)" %( pHeadSelectedCity.getNumBonuses(i) )
							szLeadBuffer = szLeadBuffer + szTempBuffer

						szLeadBuffer = szLeadBuffer + "</font>"
						
						if (iHappiness != 0):
							if ( iHappiness > 0 ):
								szTempBuffer = u"<font=1>+%d%c</font>" %(iHappiness, CyGame().getSymbolID(FontSymbols.HAPPY_CHAR) )
							else:
								szTempBuffer = u"<font=1>+%d%c</font>" %( -iHappiness, CyGame().getSymbolID(FontSymbols.UNHAPPY_CHAR) )

							if ( iHealth > 0 ):
								szTempBuffer += u"<font=1>, +%d%c</font>" %( iHealth, CyGame().getSymbolID( FontSymbols.HEALTHY_CHAR ) )

							szName = "RightBonusItemLeft" + str(iRightCount)
							screen.setLabelAt( szName, "BonusBack2", szLeadBuffer, CvUtil.FONT_LEFT_JUSTIFY, 0, (iRightCount * 20) + 4, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, i, -1 )
							szName = "RightBonusItemRight" + str(iRightCount)
							screen.setLabelAt( szName, "BonusBack2", szTempBuffer, CvUtil.FONT_RIGHT_JUSTIFY, 102, (iRightCount * 20) + 4, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, i, -1 )
							
							iRightCount = iRightCount + 1

							bHandled = True

						if (iHealth != 0 and bHandled == False):
							if ( iHealth > 0 ):
								szTempBuffer = u"<font=1>+%d%c</font>" %( iHealth, CyGame().getSymbolID( FontSymbols.HEALTHY_CHAR ) )
							else:
								szTempBuffer = u"<font=1>+%d%c</font>" %( -iHealth, CyGame().getSymbolID(FontSymbols.UNHEALTHY_CHAR) )
								
							szName = "CenterBonusItemLeft" + str(iCenterCount)
							screen.setLabelAt( szName, "BonusBack1", szLeadBuffer, CvUtil.FONT_LEFT_JUSTIFY, 0, (iCenterCount * 20) + 4, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, i, -1 )
							szName = "CenterBonusItemRight" + str(iCenterCount)
							screen.setLabelAt( szName, "BonusBack1", szTempBuffer, CvUtil.FONT_RIGHT_JUSTIFY, 62, (iCenterCount * 20) + 4, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, i, -1 )
							
							iCenterCount = iCenterCount + 1

							bHandled = True

						szBuffer = u""
						if ( not bHandled ):
						
							szName = "LeftBonusItem" + str(iLeftCount)
							screen.setLabelAt( szName, "BonusBack0", szLeadBuffer, CvUtil.FONT_LEFT_JUSTIFY, 0, (iLeftCount * 20) + 4, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, i, -1 )
							
							iLeftCount = iLeftCount + 1

							bHandled = True

				g_iNumLeftBonus = iLeftCount
				g_iNumCenterBonus = iCenterCount
				g_iNumRightBonus = iRightCount
				
				iMaintenance = pHeadSelectedCity.getMaintenanceTimes100()

				szBuffer = localText.getText("INTERFACE_CITY_MAINTENANCE", ())
				
				screen.setLabel( "MaintenanceText", "Background", szBuffer, CvUtil.FONT_LEFT_JUSTIFY, 15, 126, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_HELP_MAINTENANCE, -1, -1 )
				screen.show( "MaintenanceText" )
				
				szBuffer = u"-%d.%02d %c" %(iMaintenance/100, iMaintenance%100, gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getChar())
				screen.setLabel( "MaintenanceAmountText", "Background", szBuffer, CvUtil.FONT_RIGHT_JUSTIFY, 220, 125, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_HELP_MAINTENANCE, -1, -1 )
				screen.show( "MaintenanceAmountText" )
				
# BUG - Raw Commerce - start
				if (bShowRawCommerce):
					PRODUCTION_CHAR = gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getChar()
					COMMERCE_CHAR = gc.getYieldInfo(YieldTypes.YIELD_COMMERCE).getChar()
					
					if (g_iYieldType == YieldTypes.YIELD_PRODUCTION):
						lYieldLabels = [ "Worked Tiles", "Specialists", "Buildings", "Total" ]
						cYieldChar = PRODUCTION_CHAR
					else:
						lYieldLabels = [ "Worked Tiles", "Trade Routes", "Buildings", "Total" ]
						cYieldChar = COMMERCE_CHAR
					
					iSpecialistsYield = 0
					for iSpec in range(gc.getNumSpecialistInfos()):
						iSpecialistsYield += gc.getActivePlayer().specialistYield(iSpec, g_iYieldType) * (pHeadSelectedCity.getSpecialistCount(iSpec) + pHeadSelectedCity.getFreeSpecialistCount(iSpec))
					
					iCityBaseYield = pHeadSelectedCity.getBaseYieldRate(g_iYieldType)
					iCityTotalYield = pHeadSelectedCity.getYieldRate(g_iYieldType)
					
					# Labels
					szBuffer = lYieldLabels[0] #"Worked Tiles:"
					screen.setLabel( "RawWorkedPlotsLabel", "Background", szBuffer, CvUtil.FONT_LEFT_JUSTIFY, 15, 160, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
					screen.show( "RawWorkedPlotsLabel" )
					
					szBuffer = lYieldLabels[1] #"Trade Routes:"
					screen.setLabel( "RawTradeRoutesSpecsLabel", "Background", szBuffer, CvUtil.FONT_LEFT_JUSTIFY, 15, 180, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
					screen.show( "RawTradeRoutesSpecsLabel" )
					
					szBuffer = lYieldLabels[2] #"Buildings and Specialists:"
					screen.setLabel( "RawBuildingsLabel", "Background", szBuffer, CvUtil.FONT_LEFT_JUSTIFY, 15, 200, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
					screen.show( "RawBuildingsLabel" )
					
					# Include modifier in total
					#   (+50% for Capital) 69C
					# Show added amount instead of percentage?
					#   (+23C for Capital) 69C
					# Remove from total?
					#   (+50% for Capital) 46C
					#   (+23C for Capital) 46C
					
					# Percentage, included
					#iYieldRateModifier = pHeadSelectedCity.getBaseYieldRateModifier(YieldTypes.YIELD_COMMERCE, 0)
					#if (iYieldRateModifier != 100):
					#	szBuffer = u"<color=205,180,55,255>Total (%+d%% for Capital):</color>" %(iYieldRateModifier - 100)
					
					# Commerce, not included
					iCityYieldDelta = iCityTotalYield - iCityBaseYield
#					if (iCityYieldDelta != 0):
#						szBuffer = u"<color=205,180,55,255>Total (%+d %c for Capital):</color>" %(iCityYieldDelta, COMMERCE_CHAR)
#					else:
					szBuffer = "<color=205,180,55,255>" + lYieldLabels[3] + "</color>"
					screen.setLabel( "RawTotalLabel", "Background", szBuffer, CvUtil.FONT_LEFT_JUSTIFY, 15, 220, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
					screen.show( "RawTotalLabel" )
					
					# Values
					# Worked Plots
					if (g_iYieldType == YieldTypes.YIELD_COMMERCE):
						szBuffer = u"%d%c" %( iCityBaseYield - iBuildingsYield - iSpecialistsYield - iNetTradeYield, cYieldChar )
					else:
						szBuffer = u"%d%c" %( iCityBaseYield - iBuildingsProdYield - iSpecialistsYield, cYieldChar )
					screen.setLabel( "RawWorkedPlotsText", "Background", szBuffer, CvUtil.FONT_RIGHT_JUSTIFY, 225, 160, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
					screen.show( "RawWorkedPlotsText" )
					
					# Trade Routes / Specialists
					if (g_iYieldType == YieldTypes.YIELD_COMMERCE):
						szBuffer = u"%d%c" %( iNetTradeYield, cYieldChar )
					else:
						szBuffer = u"%d%c" %( iSpecialistsYield, cYieldChar )
					screen.setLabel( "RawTradeRoutesSpecsText", "Background", szBuffer, CvUtil.FONT_RIGHT_JUSTIFY, 225, 180, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
					screen.show( "RawTradeRoutesSpecsText" )
					
					# Buildings
					if (g_iYieldType == YieldTypes.YIELD_COMMERCE):
						szBuffer = u"%d%c" %( iBuildingsYield + iSpecialistsYield, cYieldChar )
					else:
						szBuffer = u"%d%c" %( iBuildingsProdYield, cYieldChar )
					screen.setLabel( "RawBuildingsText", "Background", szBuffer, CvUtil.FONT_RIGHT_JUSTIFY, 225, 200, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
					screen.show( "RawBuildingsText" )
					
					# Base Commerce (excludes modifiers like +50% Capital)
					if (iCityYieldDelta != 0):
						szBuffer = u"<color=205,180,55,255>%d%c + %d%c = %d%c</color>" %( iCityBaseYield, cYieldChar, iCityYieldDelta, cYieldChar, iCityTotalYield, cYieldChar )
					else:
						szBuffer = u"<color=205,180,55,255>%d</color>%c" %( iCityBaseYield, cYieldChar )
					screen.setLabel( "RawTotalText", "Background", szBuffer, CvUtil.FONT_RIGHT_JUSTIFY, 225, 220, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
					screen.show( "RawTotalText" )
					
					# Toggle Button
					if (g_iYieldType == YieldTypes.YIELD_COMMERCE):
						szBuffer = u"%c" %( PRODUCTION_CHAR )
					else:
						szBuffer = u"%c" %( COMMERCE_CHAR )
					screen.setText( "RawToggleButton", "Background", szBuffer, CvUtil.FONT_CENTER_JUSTIFY, 140, 170, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, g_iYieldType, -1 )
					screen.show( "RawToggleButton" )
# BUG - Raw Commerce - end

				szBuffer = u""

				for i in range(gc.getNumReligionInfos()):
					xCoord = xResolution - 242 + (i * 34)
					yCoord = 42
					
					bEnable = True
						
					if (pHeadSelectedCity.isHasReligion(i)):
						if (pHeadSelectedCity.isHolyCityByType(i)):
							szTempBuffer = u"%c" %(gc.getReligionInfo(i).getHolyCityChar())
							szName = "ReligionHolyCityDDS" + str(i)
							screen.show( szName )
						else:
							szTempBuffer = u"%c" %(gc.getReligionInfo(i).getChar())
						szBuffer = szBuffer + szTempBuffer

						j = 0
						for j in range(CommerceTypes.NUM_COMMERCE_TYPES):
							iCommerce = pHeadSelectedCity.getReligionCommerceByReligion(j, i)

							if (iCommerce != 0):
								if ( iCommerce > 0 ):
									szTempBuffer = u",%s%d%c" %("+", iCommerce, gc.getCommerceInfo(j).getChar() )
									szBuffer = szBuffer + szTempBuffer
								else:
									szTempBuffer = u",%s%d%c" %( "", iCommerce, gc.getCommerceInfo(j).getChar() )
									szBuffer = szBuffer + szTempBuffer

						iHappiness = pHeadSelectedCity.getReligionHappiness(i)

						if (iHappiness != 0):
							if ( iHappiness > 0 ):
								szTempBuffer = u",+%d%c" %(iHappiness, CyGame().getSymbolID(FontSymbols.HAPPY_CHAR) )
								szBuffer = szBuffer + szTempBuffer
							else:
								szTempBuffer = u",+%d%c" %(-(iHappiness), CyGame().getSymbolID(FontSymbols.UNHAPPY_CHAR) )
								szBuffer = szBuffer + szTempBuffer

						szBuffer = szBuffer + " "
						
						szButton = gc.getReligionInfo(i).getButton()
					
					else:
					
						bEnable = False
						szButton = gc.getReligionInfo(i).getButton()

					szName = "ReligionDDS" + str(i)
					screen.setImageButton( szName, szButton, xCoord, yCoord, 24, 24, WidgetTypes.WIDGET_HELP_RELIGION_CITY, i, -1 )
					screen.enable( szName, bEnable )
					screen.show( szName )

				for i in range(gc.getNumCorporationInfos()):
					xCoord = xResolution - 242 + (i * 34)
					yCoord = 66
					
					bEnable = True
						
					if (pHeadSelectedCity.isHasCorporation(i)):
						if (pHeadSelectedCity.isHeadquartersByType(i)):
							szTempBuffer = u"%c" %(gc.getCorporationInfo(i).getHeadquarterChar())
							szName = "CorporationHeadquarterDDS" + str(i)
							screen.show( szName )
						else:
							szTempBuffer = u"%c" %(gc.getCorporationInfo(i).getChar())
						szBuffer = szBuffer + szTempBuffer

						for j in range(YieldTypes.NUM_YIELD_TYPES):
							iYield = pHeadSelectedCity.getCorporationYieldByCorporation(j, i)

							if (iYield != 0):
								if ( iYield > 0 ):
									szTempBuffer = u",%s%d%c" %("+", iYield, gc.getYieldInfo(j).getChar() )
									szBuffer = szBuffer + szTempBuffer
								else:
									szTempBuffer = u",%s%d%c" %( "", iYield, gc.getYieldInfo(j).getChar() )
									szBuffer = szBuffer + szTempBuffer
						
						for j in range(CommerceTypes.NUM_COMMERCE_TYPES):
							iCommerce = pHeadSelectedCity.getCorporationCommerceByCorporation(j, i)

							if (iCommerce != 0):
								if ( iCommerce > 0 ):
									szTempBuffer = u",%s%d%c" %("+", iCommerce, gc.getCommerceInfo(j).getChar() )
									szBuffer = szBuffer + szTempBuffer
								else:
									szTempBuffer = u",%s%d%c" %( "", iCommerce, gc.getCommerceInfo(j).getChar() )
									szBuffer = szBuffer + szTempBuffer

						szBuffer += " "
						
						szButton = gc.getCorporationInfo(i).getButton()
					
					else:
					
						bEnable = False
						szButton = gc.getCorporationInfo(i).getButton()

					szName = "CorporationDDS" + str(i)
					screen.setImageButton( szName, szButton, xCoord, yCoord, 24, 24, WidgetTypes.WIDGET_HELP_CORPORATION_CITY, i, -1 )
					screen.enable( szName, bEnable )
					screen.show( szName )

				szBuffer = u"%d%% %s" %(pHeadSelectedCity.plot().calculateCulturePercent(pHeadSelectedCity.getOwner()), gc.getPlayer(pHeadSelectedCity.getOwner()).getCivilizationAdjective(0) )
				screen.setLabel( "NationalityText", "Background", szBuffer, CvUtil.FONT_CENTER_JUSTIFY, 125, yResolution - 210, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
				screen.setHitTest( "NationalityText", HitTestTypes.HITTEST_NOHIT )
				screen.show( "NationalityText" )
				iRemainder = 0
				iWhichBar = 0
				for h in range( gc.getMAX_PLAYERS() ):
					if ( gc.getPlayer(h).isAlive() ):
						fPercent = pHeadSelectedCity.plot().calculateCulturePercent(h)
						if ( fPercent != 0 ):
							fPercent = fPercent / 100.0
							screen.setStackedBarColorsRGB( "NationalityBar", iWhichBar, gc.getPlayer(h).getPlayerTextColorR(), gc.getPlayer(h).getPlayerTextColorG(), gc.getPlayer(h).getPlayerTextColorB(), gc.getPlayer(h).getPlayerTextColorA() )
							if ( iRemainder == 1 ):
								screen.setBarPercentage( "NationalityBar", iWhichBar, fPercent )
							else:
								screen.setBarPercentage( "NationalityBar", iWhichBar, fPercent / ( 1 - iRemainder ) )
							iRemainder += fPercent
							iWhichBar += 1
				screen.show( "NationalityBar" )

				iDefenseModifier = pHeadSelectedCity.getDefenseModifier(False)

				if (iDefenseModifier != 0):
					szBuffer = localText.getText("TXT_KEY_MAIN_CITY_DEFENSE", (CyGame().getSymbolID(FontSymbols.DEFENSE_CHAR), iDefenseModifier))
					
					if (pHeadSelectedCity.getDefenseDamage() > 0):
						szTempBuffer = u" (%d%%)" %( ( ( gc.getMAX_CITY_DEFENSE_DAMAGE() - pHeadSelectedCity.getDefenseDamage() ) * 100 ) / gc.getMAX_CITY_DEFENSE_DAMAGE() )
						szBuffer = szBuffer + szTempBuffer
					szNewBuffer = "<font=4>"
					szNewBuffer = szNewBuffer + szBuffer
					szNewBuffer = szNewBuffer + "</font>"
					screen.setLabel( "DefenseText", "Background", szBuffer, CvUtil.FONT_RIGHT_JUSTIFY, xResolution - 270, 40, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_HELP_DEFENSE, -1, -1 )
					screen.show( "DefenseText" )

				if ( pHeadSelectedCity.getCultureLevel != CultureLevelTypes.NO_CULTURELEVEL ):
					iRate = pHeadSelectedCity.getCommerceRateTimes100(CommerceTypes.COMMERCE_CULTURE)
					if (iRate%100 == 0):
						szBuffer = localText.getText("INTERFACE_CITY_COMMERCE_RATE", (gc.getCommerceInfo(CommerceTypes.COMMERCE_CULTURE).getChar(), gc.getCultureLevelInfo(pHeadSelectedCity.getCultureLevel()).getTextKey(), iRate/100))
					else:
						szRate = u"+%d.%02d" % (iRate/100, iRate%100)
						szBuffer = localText.getText("INTERFACE_CITY_COMMERCE_RATE_FLOAT", (gc.getCommerceInfo(CommerceTypes.COMMERCE_CULTURE).getChar(), gc.getCultureLevelInfo(pHeadSelectedCity.getCultureLevel()).getTextKey(), szRate))
						
# BUG - Culture Turns - start
					if BugCityScreen.isShowCultureTurns() and iRate > 0:
						iCultureTimes100 = pHeadSelectedCity.getCultureTimes100(pHeadSelectedCity.getOwner())
						iCultureLeftTimes100 = 100 * pHeadSelectedCity.getCultureThreshold() - iCultureTimes100
						szBuffer += u" " + localText.getText("INTERFACE_CITY_TURNS", (((iCultureLeftTimes100 + iRate - 1) / iRate),))
# BUG - Culture Turns - end

					screen.setLabel( "CultureText", "Background", szBuffer, CvUtil.FONT_CENTER_JUSTIFY, 125, yResolution - 184, -1.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
					screen.setHitTest( "CultureText", HitTestTypes.HITTEST_NOHIT )
					screen.show( "CultureText" )

				if ((pHeadSelectedCity.getGreatPeopleProgress() > 0) or (pHeadSelectedCity.getGreatPeopleRate() > 0)):
					szBuffer = localText.getText("INTERFACE_CITY_GREATPEOPLE_RATE", (CyGame().getSymbolID(FontSymbols.GREAT_PEOPLE_CHAR), pHeadSelectedCity.getGreatPeopleRate()))

# BUG - Great Person Turns - start
					iRate = pHeadSelectedCity.getGreatPeopleRate()
					if BugCityScreen.isShowGreatPersonTurns() and iRate > 0:
						iGPPLeft = gc.getPlayer(pHeadSelectedCity.getOwner()).greatPeopleThreshold(False) - pHeadSelectedCity.getGreatPeopleProgress()
						szBuffer += u" " + localText.getText("INTERFACE_CITY_TURNS", (((iGPPLeft + iRate - 1) / iRate),))
# BUG - Great Person Turns - end

					screen.setLabel( "GreatPeopleText", "Background", szBuffer, CvUtil.FONT_CENTER_JUSTIFY, xResolution - 146, yResolution - 176, -1.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
					screen.setHitTest( "GreatPeopleText", HitTestTypes.HITTEST_NOHIT )
					screen.show( "GreatPeopleText" )

					iFirst = float(pHeadSelectedCity.getGreatPeopleProgress()) / float( gc.getPlayer( pHeadSelectedCity.getOwner() ).greatPeopleThreshold(false) )
					screen.setBarPercentage( "GreatPeopleBar", InfoBarTypes.INFOBAR_STORED, iFirst )
					if ( iFirst == 1 ):
						screen.setBarPercentage( "GreatPeopleBar", InfoBarTypes.INFOBAR_RATE, ( float(pHeadSelectedCity.getGreatPeopleRate()) / float( gc.getPlayer( pHeadSelectedCity.getOwner() ).greatPeopleThreshold(false) ) ) )
					else:
						screen.setBarPercentage( "GreatPeopleBar", InfoBarTypes.INFOBAR_RATE, ( ( float(pHeadSelectedCity.getGreatPeopleRate()) / float( gc.getPlayer( pHeadSelectedCity.getOwner() ).greatPeopleThreshold(false) ) ) ) / ( 1 - iFirst ) )
					screen.show( "GreatPeopleBar" )

				iFirst = float(pHeadSelectedCity.getCultureTimes100(pHeadSelectedCity.getOwner())) / float(100 * pHeadSelectedCity.getCultureThreshold())
				screen.setBarPercentage( "CultureBar", InfoBarTypes.INFOBAR_STORED, iFirst )
				if ( iFirst == 1 ):
					screen.setBarPercentage( "CultureBar", InfoBarTypes.INFOBAR_RATE, ( float(pHeadSelectedCity.getCommerceRate(CommerceTypes.COMMERCE_CULTURE)) / float(pHeadSelectedCity.getCultureThreshold()) ) )
				else:
					screen.setBarPercentage( "CultureBar", InfoBarTypes.INFOBAR_RATE, ( ( float(pHeadSelectedCity.getCommerceRate(CommerceTypes.COMMERCE_CULTURE)) / float(pHeadSelectedCity.getCultureThreshold()) ) ) / ( 1 - iFirst ) )
				screen.show( "CultureBar" )
				
		else:
		
			# Help Text Area
			if ( CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW ):
				screen.setHelpTextArea( 350, FontTypes.SMALL_FONT, 7, yResolution - 172, -0.1, False, "", True, False, CvUtil.FONT_LEFT_JUSTIFY, 150 )
			else:
				screen.setHelpTextArea( 350, FontTypes.SMALL_FONT, 7, yResolution - 50, -0.1, False, "", True, False, CvUtil.FONT_LEFT_JUSTIFY, 150 )

			screen.hide( "InterfaceTopLeftBackgroundWidget" )
			screen.hide( "InterfaceTopRightBackgroundWidget" )
			screen.hide( "InterfaceCenterLeftBackgroundWidget" )
			screen.hide( "CityScreenTopWidget" )
			screen.hide( "CityNameBackground" )
			screen.hide( "TopCityPanelLeft" )
			screen.hide( "TopCityPanelRight" )
			screen.hide( "CityScreenAdjustPanel" )
# BUG - Raw Commerce - start
			screen.hide( "RawCommercePanel" )
# BUG - Raw Commerce - end
			screen.hide( "InterfaceCenterRightBackgroundWidget" )
			
			if ( CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW ):
				self.setMinimapButtonVisibility(True)

		return 0
		
	# Will update the info pane strings
	def updateInfoPaneStrings( self ):
	
		iRow = 0
	
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )

		pHeadSelectedCity = CyInterface().getHeadSelectedCity()
		pHeadSelectedUnit = CyInterface().getHeadSelectedUnit()
		
		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()

		bShift = CyInterface().shiftKey()

		screen.addPanel( "SelectedUnitPanel", u"", u"", True, False, 8, yResolution - 140, 280, 130, PanelStyles.PANEL_STYLE_STANDARD )
		screen.setStyle( "SelectedUnitPanel", "Panel_Game_HudStat_Style" )
		screen.hide( "SelectedUnitPanel" )

		screen.addTableControlGFC( "SelectedUnitText", 3, 10, yResolution - 109, 183, 102, False, False, 32, 32, TableStyles.TABLE_STYLE_STANDARD )
		screen.setStyle( "SelectedUnitText", "Table_EmptyScroll_Style" )
		screen.hide( "SelectedUnitText" )
		screen.hide( "SelectedUnitLabel" )
		
		screen.addTableControlGFC( "SelectedCityText", 3, 10, yResolution - 139, 183, 128, False, False, 32, 32, TableStyles.TABLE_STYLE_STANDARD )
		screen.setStyle( "SelectedCityText", "Table_EmptyScroll_Style" )
		screen.hide( "SelectedCityText" )
		
		for i in range(gc.getNumPromotionInfos()):
			szName = "PromotionButton" + str(i)
			screen.hide( szName )
		
		if CyEngine().isGlobeviewUp():
			return

		if (pHeadSelectedCity):
		
			iOrders = CyInterface().getNumOrdersQueued()

			screen.setTableColumnHeader( "SelectedCityText", 0, u"", 121 )
			screen.setTableColumnHeader( "SelectedCityText", 1, u"", 54 )
			screen.setTableColumnHeader( "SelectedCityText", 2, u"", 10 )
			screen.setTableColumnRightJustify( "SelectedCityText", 1 )
			
			for i in range( iOrders ):
				
				szLeftBuffer = u""
				szRightBuffer = u""
				
				if ( CyInterface().getOrderNodeType(i) == OrderTypes.ORDER_TRAIN ):
					szLeftBuffer = gc.getUnitInfo(CyInterface().getOrderNodeData1(i)).getDescription()
					szRightBuffer = "(" + str(pHeadSelectedCity.getUnitProductionTurnsLeft(CyInterface().getOrderNodeData1(i), i)) + ")"

					if (CyInterface().getOrderNodeSave(i)):
						szLeftBuffer = u"*" + szLeftBuffer

				elif ( CyInterface().getOrderNodeType(i) == OrderTypes.ORDER_CONSTRUCT ):
					szLeftBuffer = gc.getBuildingInfo(CyInterface().getOrderNodeData1(i)).getDescription()
					szRightBuffer = "(" + str(pHeadSelectedCity.getBuildingProductionTurnsLeft(CyInterface().getOrderNodeData1(i), i)) + ")"

				elif ( CyInterface().getOrderNodeType(i) == OrderTypes.ORDER_CREATE ):
					szLeftBuffer = gc.getProjectInfo(CyInterface().getOrderNodeData1(i)).getDescription()
					szRightBuffer = "(" + str(pHeadSelectedCity.getProjectProductionTurnsLeft(CyInterface().getOrderNodeData1(i), i)) + ")"

				elif ( CyInterface().getOrderNodeType(i) == OrderTypes.ORDER_MAINTAIN ):
					szLeftBuffer = gc.getProcessInfo(CyInterface().getOrderNodeData1(i)).getDescription()

				screen.appendTableRow( "SelectedCityText" )
				screen.setTableText( "SelectedCityText", 0, iRow, szLeftBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, i, -1, CvUtil.FONT_LEFT_JUSTIFY )
				screen.setTableText( "SelectedCityText", 1, iRow, szRightBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, i, -1, CvUtil.FONT_RIGHT_JUSTIFY )
				screen.show( "SelectedCityText" )
				screen.show( "SelectedUnitPanel" )
				iRow += 1

		elif (pHeadSelectedUnit and CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW):
		
			screen.setTableColumnHeader( "SelectedUnitText", 0, u"", 100 )
			screen.setTableColumnHeader( "SelectedUnitText", 1, u"", 75 )
			screen.setTableColumnHeader( "SelectedUnitText", 2, u"", 10 )
			screen.setTableColumnRightJustify( "SelectedUnitText", 1 )
			
			if (CyInterface().mirrorsSelectionGroup()):
				pSelectedGroup = pHeadSelectedUnit.getGroup()
			else:
				pSelectedGroup = 0

			if (CyInterface().getLengthSelectionList() > 1):
			
				screen.setText( "SelectedUnitLabel", "Background", localText.getText("TXT_KEY_UNIT_STACK", (CyInterface().getLengthSelectionList(), )), CvUtil.FONT_LEFT_JUSTIFY, 18, yResolution - 137, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_UNIT_NAME, -1, -1 )
				
				if ((pSelectedGroup == 0) or (pSelectedGroup.getLengthMissionQueue() <= 1)):
					if (pHeadSelectedUnit):
						for i in range(gc.getNumUnitInfos()):
							iCount = CyInterface().countEntities(i)

							if (iCount > 0):
								szRightBuffer = u""
								
								szLeftBuffer = gc.getUnitInfo(i).getDescription()

								if (iCount > 1):
									szRightBuffer = u"(" + str(iCount) + u")"

								szBuffer = szLeftBuffer + u"  " + szRightBuffer
								screen.appendTableRow( "SelectedUnitText" )
								screen.setTableText( "SelectedUnitText", 0, iRow, szLeftBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, i, -1, CvUtil.FONT_LEFT_JUSTIFY )
								screen.setTableText( "SelectedUnitText", 1, iRow, szRightBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, i, -1, CvUtil.FONT_RIGHT_JUSTIFY )
								screen.show( "SelectedUnitText" )
								screen.show( "SelectedUnitPanel" )
								iRow += 1
			else:
			
				if (pHeadSelectedUnit.getHotKeyNumber() == -1):
					szBuffer = localText.getText("INTERFACE_PANE_UNIT_NAME", (pHeadSelectedUnit.getName(), ))
				else:
					szBuffer = localText.getText("INTERFACE_PANE_UNIT_NAME_HOT_KEY", (pHeadSelectedUnit.getHotKeyNumber(), pHeadSelectedUnit.getName()))
				if (len(szBuffer) > 60):
					szBuffer = "<font=2>" + szBuffer + "</font>"
				screen.setText( "SelectedUnitLabel", "Background", szBuffer, CvUtil.FONT_LEFT_JUSTIFY, 18, yResolution - 137, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_UNIT_NAME, -1, -1 )
			
				if ((pSelectedGroup == 0) or (pSelectedGroup.getLengthMissionQueue() <= 1)):
					screen.show( "SelectedUnitText" )
					screen.show( "SelectedUnitPanel" )

					szBuffer = u""

					szLeftBuffer = u""
					szRightBuffer = u""
					
					if (pHeadSelectedUnit.getDomainType() == DomainTypes.DOMAIN_AIR):
						if (pHeadSelectedUnit.airBaseCombatStr() > 0):
							szLeftBuffer = localText.getText("INTERFACE_PANE_AIR_STRENGTH", ())
							if (pHeadSelectedUnit.isFighting()):
								szRightBuffer = u"?/%d%c" %(pHeadSelectedUnit.airBaseCombatStr(), CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR))
							elif (pHeadSelectedUnit.isHurt()):
								szRightBuffer = u"%.1f/%d%c" %(((float(pHeadSelectedUnit.airBaseCombatStr() * pHeadSelectedUnit.currHitPoints())) / (float(pHeadSelectedUnit.maxHitPoints()))), pHeadSelectedUnit.airBaseCombatStr(), CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR))
							else:
								szRightBuffer = u"%d%c" %(pHeadSelectedUnit.airBaseCombatStr(), CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR))
					else:
						if (pHeadSelectedUnit.canFight()):
							szLeftBuffer = localText.getText("INTERFACE_PANE_STRENGTH", ())
							if (pHeadSelectedUnit.isFighting()):
								szRightBuffer = u"?/%d%c" %(pHeadSelectedUnit.baseCombatStr(), CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR))
							elif (pHeadSelectedUnit.isHurt()):
								szRightBuffer = u"%.1f/%d%c" %(((float(pHeadSelectedUnit.baseCombatStr() * pHeadSelectedUnit.currHitPoints())) / (float(pHeadSelectedUnit.maxHitPoints()))), pHeadSelectedUnit.baseCombatStr(), CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR))
							else:
								szRightBuffer = u"%d%c" %(pHeadSelectedUnit.baseCombatStr(), CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR))

					szBuffer = szLeftBuffer + szRightBuffer
					if ( szBuffer ):
						screen.appendTableRow( "SelectedUnitText" )
						screen.setTableText( "SelectedUnitText", 0, iRow, szLeftBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
						screen.setTableText( "SelectedUnitText", 1, iRow, szRightBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY )
						screen.show( "SelectedUnitText" )
						screen.show( "SelectedUnitPanel" )
						iRow += 1

					szLeftBuffer = u""
					szRightBuffer = u""
				
					if ( (pHeadSelectedUnit.movesLeft() % gc.getMOVE_DENOMINATOR()) > 0 ):
						iDenom = 1
					else:
						iDenom = 0
					iCurrMoves = ((pHeadSelectedUnit.movesLeft() / gc.getMOVE_DENOMINATOR()) + iDenom )
					szLeftBuffer = localText.getText("INTERFACE_PANE_MOVEMENT", ())
					if (pHeadSelectedUnit.baseMoves() == iCurrMoves):
						szRightBuffer = u"%d%c" %(pHeadSelectedUnit.baseMoves(), CyGame().getSymbolID(FontSymbols.MOVES_CHAR) )
					else:
						szRightBuffer = u"%d/%d%c" %(iCurrMoves, pHeadSelectedUnit.baseMoves(), CyGame().getSymbolID(FontSymbols.MOVES_CHAR) )

					szBuffer = szLeftBuffer + "  " + szRightBuffer
					screen.appendTableRow( "SelectedUnitText" )
					screen.setTableText( "SelectedUnitText", 0, iRow, szLeftBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
					screen.setTableText( "SelectedUnitText", 1, iRow, szRightBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY )
					screen.show( "SelectedUnitText" )
					screen.show( "SelectedUnitPanel" )
					iRow += 1

					if (pHeadSelectedUnit.getLevel() > 0):
					
						szLeftBuffer = localText.getText("INTERFACE_PANE_LEVEL", ())
						szRightBuffer = u"%d" %(pHeadSelectedUnit.getLevel())
						
						szBuffer = szLeftBuffer + "  " + szRightBuffer
						screen.appendTableRow( "SelectedUnitText" )
						screen.setTableText( "SelectedUnitText", 0, iRow, szLeftBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
						screen.setTableText( "SelectedUnitText", 1, iRow, szRightBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY )
						screen.show( "SelectedUnitText" )
						screen.show( "SelectedUnitPanel" )
						iRow += 1

					if ((pHeadSelectedUnit.getExperience() > 0) and not pHeadSelectedUnit.isFighting()):
						szLeftBuffer = localText.getText("INTERFACE_PANE_EXPERIENCE", ())
						szRightBuffer = u"(%d/%d)" %(pHeadSelectedUnit.getExperience(), pHeadSelectedUnit.experienceNeeded())
						szBuffer = szLeftBuffer + "  " + szRightBuffer
						screen.appendTableRow( "SelectedUnitText" )
						screen.setTableText( "SelectedUnitText", 0, iRow, szLeftBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
						screen.setTableText( "SelectedUnitText", 1, iRow, szRightBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY )
						screen.show( "SelectedUnitText" )
						screen.show( "SelectedUnitPanel" )
						iRow += 1

					iPromotionCount = 0
					i = 0
					for i in range(gc.getNumPromotionInfos()):
						if (pHeadSelectedUnit.isHasPromotion(i)):
							szName = "PromotionButton" + str(i)
							self.setPromotionButtonPosition( szName, iPromotionCount )
							screen.moveToFront( szName )
							screen.show( szName )

							iPromotionCount = iPromotionCount + 1

			if (pSelectedGroup):
			
				iNodeCount = pSelectedGroup.getLengthMissionQueue()

				if (iNodeCount > 1):
					for i in range( iNodeCount ):
						szLeftBuffer = u""
						szRightBuffer = u""
					
						if (gc.getMissionInfo(pSelectedGroup.getMissionType(i)).isBuild()):
							if (i == 0):
								szLeftBuffer = gc.getBuildInfo(pSelectedGroup.getMissionData1(i)).getDescription()
								szRightBuffer = localText.getText("INTERFACE_CITY_TURNS", (pSelectedGroup.plot().getBuildTurnsLeft(pSelectedGroup.getMissionData1(i), 0, 0), ))								
							else:
								szLeftBuffer = u"%s..." %(gc.getBuildInfo(pSelectedGroup.getMissionData1(i)).getDescription())
						else:
							szLeftBuffer = u"%s..." %(gc.getMissionInfo(pSelectedGroup.getMissionType(i)).getDescription())

						szBuffer = szLeftBuffer + "  " + szRightBuffer
						screen.appendTableRow( "SelectedUnitText" )
						screen.setTableText( "SelectedUnitText", 0, iRow, szLeftBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, i, -1, CvUtil.FONT_LEFT_JUSTIFY )
						screen.setTableText( "SelectedUnitText", 1, iRow, szRightBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, i, -1, CvUtil.FONT_RIGHT_JUSTIFY )
						screen.show( "SelectedUnitText" )
						screen.show( "SelectedUnitPanel" )
						iRow += 1

		return 0
		
	# Will update the scores
	def updateScoreStrings( self ):
	
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )

		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()
		
		screen.hide( "ScoreBackground" )
		
# BUG - Align Icons - start
		for i in range( gc.getMAX_PLAYERS() ):
			szName = "ScoreText" + str(i)
			screen.hide( szName )
			szName = "ScoreTech" + str(i)
			screen.hide( szName )
			for j in range( Scoreboard.SCORE, Scoreboard.NUM_PARTS ):
				szName = "ScoreText%d-%d" %( i, j )
				screen.hide( szName )
# BUG - Align Icons - end

		iWidth = 0
		iCount = 0
		iBtnHeight = 22
		
		if ((CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_MINIMAP_ONLY)):
			if (CyInterface().isScoresVisible() and not CyInterface().isCityScreenUp() and CyEngine().isGlobeviewUp() == false):

# BUG - Align Icons - start
				bAlignIcons = BugScore.isAlignIcons()
				if (bAlignIcons):
					scores = Scoreboard.Scoreboard()
# BUG - Align Icons - end

# BUG - Power Rating - start
				bShowPower = BugScore.isShowPower()
				if (bShowPower):
					iPlayerPower = gc.getActivePlayer().getPower()
					szPowerColor = BugScore.getPowerColor()
					if (szPowerColor):
						iPowerColor = gc.getInfoTypeForString(szPowerColor)
					szPowerColor = BugScore.getGoodPowerColor()
					if (szPowerColor):
						iGoodPowerColor = gc.getInfoTypeForString(szPowerColor)
					szPowerColor = BugScore.getBadPowerColor()
					if (szPowerColor):
						iBadPowerColor = gc.getInfoTypeForString(szPowerColor)
							
					iDemographicsMission = -1
					for iMissionLoop in range(gc.getNumEspionageMissionInfos()):
						if (gc.getEspionageMissionInfo(iMissionLoop).isSeeDemographics()):
							iDemographicsMission = iMissionLoop
							break
					if (iDemographicsMission == -1):
						bShowPower = False
# BUG - Power Rating - end

				i = gc.getMAX_CIV_TEAMS() - 1
				while (i > -1):
					eTeam = gc.getGame().getRankTeam(i)

					if (gc.getTeam(gc.getGame().getActiveTeam()).isHasMet(eTeam) or gc.getTeam(eTeam).isHuman() or gc.getGame().isDebugMode()):
						j = gc.getMAX_CIV_PLAYERS() - 1
						while (j > -1):
							ePlayer = gc.getGame().getRankPlayer(j)

							if (not CyInterface().isScoresMinimized() or gc.getGame().getActivePlayer() == ePlayer):
# BUG - Dead Civs - start
								if (gc.getPlayer(ePlayer).isEverAlive() and not gc.getPlayer(ePlayer).isMinorCiv()
									and (gc.getPlayer(ePlayer).isAlive() or BugScore.isShowDeadCivs())):
# BUG - Dead Civs - end
									if (gc.getPlayer(ePlayer).getTeam() == eTeam):
										szBuffer = u"<font=2>"
# BUG - Align Icons - start
										if (bAlignIcons):
											scores.addPlayer(ePlayer)
											# BUG: Align Icons continues throughout -- if (bAlignIcons): scores.setFoo(foo)
# BUG - Align Icons - end

										if (gc.getGame().isGameMultiPlayer()):
											if (not (gc.getPlayer(ePlayer).isTurnActive())):
												szBuffer = szBuffer + "*"
												if (bAlignIcons):
													scores.setActive()

# BUG - Dead Civs - start
										if (BugScore.isShowBothNames()):
											szPlayerName = gc.getPlayer(ePlayer).getName() + "/" + gc.getPlayer(ePlayer).getCivilizationShortDescription(0)
										elif (BugScore.isShowLeaderName()):
											szPlayerName = gc.getPlayer(ePlayer).getName()
										else:
											szPlayerName = gc.getPlayer(ePlayer).getCivilizationShortDescription(0)

										if (not gc.getPlayer(ePlayer).isAlive() and BugScore.isShowDeadTag()):
											# BUG-TODO: localize
											szPlayerScore = "Dead"
										else:
											szPlayerScore = str(gc.getGame().getPlayerScore(ePlayer))
										
										if (not CyInterface().isFlashingPlayer(ePlayer) or CyInterface().shouldFlash(ePlayer)):
											if (ePlayer == gc.getGame().getActivePlayer()):
												szPlayerName = u"[<color=%d,%d,%d,%d>%s</color>]" %(gc.getPlayer(ePlayer).getPlayerTextColorR(), gc.getPlayer(ePlayer).getPlayerTextColorG(), gc.getPlayer(ePlayer).getPlayerTextColorB(), gc.getPlayer(ePlayer).getPlayerTextColorA(), szPlayerName)
											else:
												if (not gc.getPlayer(ePlayer).isAlive() and BugScore.isGreyOutDeadCivs()):
													szPlayerName = u"<color=%d,%d,%d,%d>%s</color>" %(175, 175, 175, gc.getPlayer(ePlayer).getPlayerTextColorA(), szPlayerName)
												else:
													szPlayerName = u"<color=%d,%d,%d,%d>%s</color>" %(gc.getPlayer(ePlayer).getPlayerTextColorR(), gc.getPlayer(ePlayer).getPlayerTextColorG(), gc.getPlayer(ePlayer).getPlayerTextColorB(), gc.getPlayer(ePlayer).getPlayerTextColorA(), szPlayerName)
										szTempBuffer = u"%s: %s" %(szPlayerScore, szPlayerName)
										szBuffer = szBuffer + szTempBuffer
										if (bAlignIcons):
											scores.setScore(szPlayerScore + u" ")
											scores.setName(szPlayerName + u" ")
										
										if (gc.getPlayer(ePlayer).isAlive()):
											if (bAlignIcons):
												scores.setAlive()
											# BUG: Rest of Dead Civs change is merely indentation by 1 level ...
											if (gc.getTeam(eTeam).isAlive()):
												if ( not (gc.getTeam(gc.getGame().getActiveTeam()).isHasMet(eTeam)) ):
													szBuffer = szBuffer + (" ?")
													if (bAlignIcons):
														scores.setNotMet()
												if (gc.getTeam(eTeam).isAtWar(gc.getGame().getActiveTeam())):
													szBuffer = szBuffer + "("  + localText.getColorText("TXT_KEY_CONCEPT_WAR", (), gc.getInfoTypeForString("COLOR_RED")).upper() + ")"
													if (bAlignIcons):
														scores.setWar()
												if (gc.getPlayer(ePlayer).canTradeNetworkWith(gc.getGame().getActivePlayer()) and (ePlayer != gc.getGame().getActivePlayer())):
													szTempBuffer = u"%c" %(CyGame().getSymbolID(FontSymbols.TRADE_CHAR))
													szBuffer = szBuffer + szTempBuffer
													if (bAlignIcons):
														scores.setTrade()
												if (gc.getTeam(eTeam).isOpenBorders(gc.getGame().getActiveTeam())):
													szTempBuffer = u"%c" %(CyGame().getSymbolID(FontSymbols.OPEN_BORDERS_CHAR))
													szBuffer = szBuffer + szTempBuffer
													if (bAlignIcons):
														scores.setBorders()
												if (gc.getTeam(eTeam).isDefensivePact(gc.getGame().getActiveTeam())):
													szTempBuffer = u"%c" %(CyGame().getSymbolID(FontSymbols.DEFENSIVE_PACT_CHAR))
													szBuffer = szBuffer + szTempBuffer
													if (bAlignIcons):
														scores.setPact()
												if (gc.getPlayer(ePlayer).getStateReligion() != -1):
													if (gc.getPlayer(ePlayer).hasHolyCity(gc.getPlayer(ePlayer).getStateReligion())):
														szTempBuffer = u"%c" %(gc.getReligionInfo(gc.getPlayer(ePlayer).getStateReligion()).getHolyCityChar())
													else:
														szTempBuffer = u"%c" %(gc.getReligionInfo(gc.getPlayer(ePlayer).getStateReligion()).getChar())
													szBuffer = szBuffer + szTempBuffer
													if (bAlignIcons):
														scores.setReligion(szTempBuffer)
												
												if (gc.getTeam(eTeam).getEspionagePointsAgainstTeam(gc.getGame().getActiveTeam()) < gc.getTeam(gc.getGame().getActiveTeam()).getEspionagePointsAgainstTeam(eTeam)):
													szTempBuffer = u"%c" %(gc.getCommerceInfo(CommerceTypes.COMMERCE_ESPIONAGE).getChar())
													szBuffer = szBuffer + szTempBuffer
													if (bAlignIcons):
														scores.setEspionage()
											
											bEspionageCanSeeResearch = False
											for iMissionLoop in range(gc.getNumEspionageMissionInfos()):
												if (gc.getEspionageMissionInfo(iMissionLoop).isSeeResearch()):
													bEspionageCanSeeResearch = gc.getPlayer(gc.getGame().getActivePlayer()).canDoEspionageMission(iMissionLoop, ePlayer, None, -1)
													break
											
											if (((gc.getPlayer(ePlayer).getTeam() == gc.getGame().getActiveTeam()) and (gc.getTeam(gc.getGame().getActiveTeam()).getNumMembers() > 1)) or (gc.getTeam(gc.getPlayer(ePlayer).getTeam()).isVassal(gc.getGame().getActiveTeam())) or gc.getGame().isDebugMode() or bEspionageCanSeeResearch):
												if (gc.getPlayer(ePlayer).getCurrentResearch() != -1):
													szTempBuffer = u"-%s (%d)" %(gc.getTechInfo(gc.getPlayer(ePlayer).getCurrentResearch()).getDescription(), gc.getPlayer(ePlayer).getResearchTurnsLeft(gc.getPlayer(ePlayer).getCurrentResearch(), True))
													szBuffer = szBuffer + szTempBuffer
													if (bAlignIcons):
														scores.setResearch(gc.getPlayer(ePlayer).getCurrentResearch(), gc.getPlayer(ePlayer).getResearchTurnsLeft(gc.getPlayer(ePlayer).getCurrentResearch(), True))
											
# BUG - Power Rating - start
											# if on, show according to espionage "see demographics" mission
											if (bShowPower 
												and (gc.getGame().getActivePlayer() != ePlayer
													 and gc.getActivePlayer().canDoEspionageMission(iDemographicsMission, ePlayer, None, -1))):
												iPower = gc.getPlayer(ePlayer).getPower()
												if (iPower > 0): # avoid divide by zero
													fPowerRatio = float(iPlayerPower) / float(iPower)
													cPower = gc.getGame().getSymbolID(FontSymbols.STRENGTH_CHAR)
													szTempBuffer = u"%.1f%c" %(fPowerRatio, cPower)
													if (iGoodPowerColor >= 0 and fPowerRatio >= BugScore.getGoodPowerRatio()):
														szTempBuffer = localText.changeTextColor(szTempBuffer, iGoodPowerColor)
													elif (iBadPowerColor >= 0 and fPowerRatio <= BugScore.getBadPowerRatio()):
														szTempBuffer = localText.changeTextColor(szTempBuffer, iBadPowerColor)
													elif (iPowerColor >= 0):
														szTempBuffer = localText.changeTextColor(szTempBuffer, iPowerColor)
													szBuffer = szBuffer + u" " + szTempBuffer
													if (bAlignIcons):
														scores.setPower(szTempBuffer)
# BUG - Power Rating - end
											# BUG: ...end of indentation
# BUG - Dead Civs - end

# BUG - Attitude Icons - start
										if (BugScore.isShowAttitude()):
											if (not gc.getPlayer(ePlayer).isHuman()):
												iAtt = gc.getPlayer(ePlayer).AI_getAttitude(gc.getGame().getActivePlayer())
												cAtt =  unichr(ord(unichr(CyGame().getSymbolID(FontSymbols.POWER_CHAR) + 4)) + iAtt)
												szBuffer += cAtt
												if (bAlignIcons):
													scores.setAttitude(cAtt)
# BUG - Attitude Icons - end

										if (CyGame().isNetworkMultiPlayer()):
											szTempBuffer = CyGameTextMgr().getNetStats(ePlayer)
											szBuffer = szBuffer + szTempBuffer
											if (bAlignIcons):
												scores.setNetStats(szTempBuffer)
										
										if (gc.getPlayer(ePlayer).isHuman() and CyInterface().isOOSVisible()):
											szTempBuffer = u" <color=255,0,0>* %s *</color>" %(CyGameTextMgr().getOOSSeeds(ePlayer))
											szBuffer = szBuffer + szTempBuffer
											if (bAlignIcons):
												scores.setNetStats(szTempBuffer)
											
										szBuffer = szBuffer + "</font>"

# BUG - Align Icons - start
										if (not bAlignIcons):
											if ( CyInterface().determineWidth( szBuffer ) > iWidth ):
												iWidth = CyInterface().determineWidth( szBuffer )
	
											szName = "ScoreText" + str(ePlayer)
											if ( CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW or CyInterface().isInAdvancedStart()):
												yCoord = yResolution - 206
											else:
												yCoord = yResolution - 88
	
# BUG - Dead Civs - start
											# Don't try to contact dead civs
											if (gc.getPlayer(ePlayer).isAlive()):
												iWidgetType = WidgetTypes.WIDGET_CONTACT_CIV
												iPlayer = ePlayer
											else:
												iWidgetType = WidgetTypes.WIDGET_GENERAL
												iPlayer = -1
											screen.setText( szName, "Background", szBuffer, CvUtil.FONT_RIGHT_JUSTIFY, xResolution - 12, yCoord - (iCount * iBtnHeight), -0.3, FontTypes.SMALL_FONT, iWidgetType, iPlayer, -1 )
# BUG - Dead Civs - end
											screen.show( szName )
											
											CyInterface().checkFlashReset(ePlayer)
	
											iCount = iCount + 1
# BUG - Align Icons - end
							j = j - 1
					i = i - 1

# BUG - Align Icons - start
				if (bAlignIcons):
					scores.draw(screen)
				else:
					if ( CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW or CyInterface().isInAdvancedStart()):
						yCoord = yResolution - 186
					else:
						yCoord = yResolution - 68
					screen.setPanelSize( "ScoreBackground", xResolution - 21 - iWidth, yCoord - (iBtnHeight * iCount) - 4, iWidth + 12, (iBtnHeight * iCount) + 8 )
					screen.show( "ScoreBackground" )
# BUG - Align Icons - end

	# Will update the help Strings
	def updateHelpStrings( self ):
	
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )

		if ( CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_HIDE_ALL ):
			screen.setHelpTextString( "" )
		else:
			screen.setHelpTextString( CyInterface().getHelpString() )
		
		return 0
		
	# Will set the promotion button position
	def setPromotionButtonPosition( self, szName, iPromotionCount ):
		
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		
		# Find out our resolution
		yResolution = screen.getYResolution()

		if ( CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW ):
			screen.moveItem( szName, 266 - (24 * (iPromotionCount / 6)), yResolution - 144 + (24 * (iPromotionCount % 6)), -0.3 )

	# Will set the selection button position
	def setResearchButtonPosition( self, szButtonID, iCount ):
		
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		xResolution = screen.getXResolution()
		screen.moveItem( szButtonID, 264 + ( ( xResolution - 1024 ) / 2 ) + ( 34 * ( iCount % 15 ) ), 0 + ( 34 * ( iCount / 15 ) ), -0.3 )
							
	# Will set the selection button position
	def setScoreTextPosition( self, szButtonID, iWhichLine ):
		
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		yResolution = screen.getYResolution()
		if ( CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW ):
			yCoord = yResolution - 180
		else:
			yCoord = yResolution - 88
		screen.moveItem( szButtonID, 996, yCoord - (iWhichLine * 18), -0.3 )

	# Will build the globeview UI
	def updateGlobeviewButtons( self ):
		kInterface = CyInterface()
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()

		kEngine = CyEngine()
		kGLM = CyGlobeLayerManager()
		iNumLayers = kGLM.getNumLayers()
		iCurrentLayerID = kGLM.getCurrentLayerID()
		
		# Positioning things based on the visibility of the globe
		if kEngine.isGlobeviewUp():
			screen.setHelpTextArea( 350, FontTypes.SMALL_FONT, 7, yResolution - 50, -0.1, False, "", True, False, CvUtil.FONT_LEFT_JUSTIFY, 150 )
		else:
			if ( CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW ):
				screen.setHelpTextArea( 350, FontTypes.SMALL_FONT, 7, yResolution - 172, -0.1, False, "", True, False, CvUtil.FONT_LEFT_JUSTIFY, 150 )
			else:
				screen.setHelpTextArea( 350, FontTypes.SMALL_FONT, 7, yResolution - 50, -0.1, False, "", True, False, CvUtil.FONT_LEFT_JUSTIFY, 150 )

		
		# Set base Y position for the LayerOptions, if we find them	
		if CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_HIDE:
			iY = yResolution - iGlobeLayerOptionsY_Minimal
		else:
			iY = yResolution - iGlobeLayerOptionsY_Regular

		# Hide the layer options ... all of them
		for i in range (20):
			szName = "GlobeLayerOption" + str(i)
			screen.hide(szName)

		# Setup the GlobeLayer panel
		iNumLayers = kGLM.getNumLayers()
		if kEngine.isGlobeviewUp() and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL:
			# set up panel
			if iCurrentLayerID != -1 and kGLM.getLayer(iCurrentLayerID).getNumOptions() != 0:
				bHasOptions = True		
			else:
				bHasOptions = False
				screen.hide( "ScoreBackground" )

			# set up toggle button
			screen.setState("GlobeToggle", True)

			# Set GlobeLayer indicators correctly
			for i in range(kGLM.getNumLayers()):
				szButtonID = "GlobeLayer" + str(i)
				screen.setState( szButtonID, iCurrentLayerID == i )
				
			# Set up options pane
			if bHasOptions:
				kLayer = kGLM.getLayer(iCurrentLayerID)

				iCurY = iY
				iNumOptions = kLayer.getNumOptions()
				iCurOption = kLayer.getCurrentOption()
				iMaxTextWidth = -1
				for iTmp in range(iNumOptions):
					iOption = iTmp # iNumOptions - iTmp - 1
					szName = "GlobeLayerOption" + str(iOption)
					szCaption = kLayer.getOptionName(iOption)			
					if(iOption == iCurOption):
						szBuffer = "  <color=0,255,0>%s</color>  " % (szCaption)
					else:
						szBuffer = "  %s  " % (szCaption)
					iTextWidth = CyInterface().determineWidth( szBuffer )

					screen.setText( szName, "Background", szBuffer, CvUtil.FONT_LEFT_JUSTIFY, xResolution - 9 - iTextWidth, iCurY-iGlobeLayerOptionHeight-10, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GLOBELAYER_OPTION, iOption, -1 )
					screen.show( szName )

					iCurY -= iGlobeLayerOptionHeight

					if iTextWidth > iMaxTextWidth:
						iMaxTextWidth = iTextWidth

				#make extra space
				iCurY -= iGlobeLayerOptionHeight;
				iPanelWidth = iMaxTextWidth + 32
				iPanelHeight = iY - iCurY
				iPanelX = xResolution - 14 - iPanelWidth
				iPanelY = iCurY
				screen.setPanelSize( "ScoreBackground", iPanelX, iPanelY, iPanelWidth, iPanelHeight )
				screen.show( "ScoreBackground" )

		else:
			if iCurrentLayerID != -1:
				kLayer = kGLM.getLayer(iCurrentLayerID)
				if kLayer.getName() == "RESOURCES":
					screen.setState("ResourceIcons", True)
				else:
					screen.setState("ResourceIcons", False)

				if kLayer.getName() == "UNITS":
					screen.setState("UnitIcons", True)
				else:
					screen.setState("UnitIcons", False)
			else:
				screen.setState("ResourceIcons", False)
				screen.setState("UnitIcons", False)
				
			screen.setState("Grid", CyUserProfile().getGrid())
			screen.setState("BareMap", CyUserProfile().getMap())
			screen.setState("Yields", CyUserProfile().getYields())
			screen.setState("ScoresVisible", CyUserProfile().getScores())

			screen.hide( "InterfaceGlobeLayerPanel" )
			screen.setState("GlobeToggle", False )

	# Update minimap buttons
	def setMinimapButtonVisibility( self, bVisible):
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		kInterface = CyInterface()
		kGLM = CyGlobeLayerManager()
		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()

		if ( CyInterface().isCityScreenUp() ):
			bVisible = False
		
		kMainButtons = ["UnitIcons", "Grid", "BareMap", "Yields", "ScoresVisible", "ResourceIcons"]
		kGlobeButtons = []
		for i in range(kGLM.getNumLayers()):
			szButtonID = "GlobeLayer" + str(i)
			kGlobeButtons.append(szButtonID)
		
		if bVisible:
			if CyEngine().isGlobeviewUp():
				kHide = kMainButtons
				kShow = kGlobeButtons
			else:
				kHide = kGlobeButtons
				kShow = kMainButtons
			screen.show( "GlobeToggle" )
			
		else:
			kHide = kMainButtons + kGlobeButtons
			kShow = []
			screen.hide( "GlobeToggle" )
		
		for szButton in kHide:
			screen.hide(szButton)
		
		if CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_HIDE:
			iY = yResolution - iMinimapButtonsY_Minimal
			iGlobeY = yResolution - iGlobeButtonY_Minimal 
		else:
			iY = yResolution - iMinimapButtonsY_Regular
			iGlobeY = yResolution - iGlobeButtonY_Regular
			
		iBtnX = xResolution - 39
		screen.moveItem("GlobeToggle", iBtnX, iGlobeY, 0.0)
		
		iBtnAdvance = 28
		iBtnX = iBtnX - len(kShow)*iBtnAdvance - 10
		if len(kShow) > 0:		
			i = 0
			for szButton in kShow:
				screen.moveItem(szButton, iBtnX, iY, 0.0)
				screen.moveToFront(szButton)
				screen.show(szButton)
				iBtnX += iBtnAdvance
				i += 1
				
	
	def createGlobeviewButtons( self ):
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		
		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()
		
		kEngine = CyEngine()
		kGLM = CyGlobeLayerManager()
		iNumLayers = kGLM.getNumLayers()

		for i in range (kGLM.getNumLayers()):
			szButtonID = "GlobeLayer" + str(i)

			kLayer = kGLM.getLayer(i)
			szStyle = kLayer.getButtonStyle()
			
			if szStyle == 0 or szStyle == "":
				szStyle = "Button_HUDSmall_Style"
			
			screen.addCheckBoxGFC( szButtonID, "", "", 0, 0, 28, 28, WidgetTypes.WIDGET_GLOBELAYER, i, -1, ButtonStyles.BUTTON_STYLE_LABEL )
			screen.setStyle( szButtonID, szStyle )
			screen.hide( szButtonID )
				
			
	def createMinimapButtons( self ):
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()

		screen.addCheckBoxGFC( "UnitIcons", "", "", 0, 0, 28, 28, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_UNIT_ICONS).getActionInfoIndex(), -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.setStyle( "UnitIcons", "Button_HUDGlobeUnit_Style" )
		screen.setState( "UnitIcons", False )
		screen.hide( "UnitIcons" )

		screen.addCheckBoxGFC( "Grid", "", "", 0, 0, 28, 28, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_GRID).getActionInfoIndex(), -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.setStyle( "Grid", "Button_HUDBtnGrid_Style" )
		screen.setState( "Grid", False )
		screen.hide( "Grid" )

		screen.addCheckBoxGFC( "BareMap", "", "", 0, 0, 28, 28, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_BARE_MAP).getActionInfoIndex(), -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.setStyle( "BareMap", "Button_HUDBtnClearMap_Style" )
		screen.setState( "BareMap", False )
		screen.hide( "BareMap" )

		screen.addCheckBoxGFC( "Yields", "", "", 0, 0, 28, 28, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_YIELDS).getActionInfoIndex(), -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.setStyle( "Yields", "Button_HUDBtnTileAssets_Style" )
		screen.setState( "Yields", False )
		screen.hide( "Yields" )

		screen.addCheckBoxGFC( "ScoresVisible", "", "", 0, 0, 28, 28, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_SCORES).getActionInfoIndex(), -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.setStyle( "ScoresVisible", "Button_HUDBtnRank_Style" )
		screen.setState( "ScoresVisible", True )
		screen.hide( "ScoresVisible" )

		screen.addCheckBoxGFC( "ResourceIcons", "", "", 0, 0, 28, 28, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_RESOURCE_ALL).getActionInfoIndex(), -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.setStyle( "ResourceIcons", "Button_HUDBtnResources_Style" )
		screen.setState( "ResourceIcons", False )
		screen.hide( "ResourceIcons" )
		
		screen.addCheckBoxGFC( "GlobeToggle", "", "", -1, -1, 36, 36, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_GLOBELAYER).getActionInfoIndex(), -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.setStyle( "GlobeToggle", "Button_HUDZoom_Style" )
		screen.setState( "GlobeToggle", False )
		screen.hide( "GlobeToggle" )

	# Will handle the input for this screen...
	def handleInput (self, inputClass):
# BUG - Raw Commerce - start
		global g_iYieldType
		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED):
			if (inputClass.getFunctionName() == "RawToggleButton"):
				if (g_iYieldType == YieldTypes.YIELD_COMMERCE):
					g_iYieldType = YieldTypes.YIELD_PRODUCTION
				else:
					g_iYieldType = YieldTypes.YIELD_COMMERCE
				CyInterface().setDirty(InterfaceDirtyBits.CityScreen_DIRTY_BIT, True)
				#self.updateCityScreen()
				return 1
# BUG - Raw Commerce - end
		
# BUG - Great Person Bar - start
			elif (inputClass.getFunctionName() == "GreatPersonBarText"):
				CyInterface().selectCity(gc.getActivePlayer().getCity(inputClass.getData1()), False)
				return 1
# BUG - Great Person Bar - end
		
		return 0
	
	def update(self, fDelta):
		return
