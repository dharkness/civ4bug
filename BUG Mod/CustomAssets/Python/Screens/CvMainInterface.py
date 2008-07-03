## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums
import CvEventInterface
import time

# BUG - PLE - start 			
import MonkeyTools as mt
import string
from AStarTools import *
import PyHelpers 
PyPlayer = PyHelpers.PyPlayer

import BugPleOptions
BugPle = BugPleOptions.getOptions()
# BUG - PLE - end

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

# BUG - 3.17 No Espionage - start
import BugUtil
# BUG - 3.17 No Espionage - end

# BUG - Reminders - start
import ReminderEventManager
# BUG - Reminders - end

# BUG - Great Person Bar - start
import GPUtil
GP_BAR_WIDTH = 320
# BUG - Great Person Bar - end

g_NumEmphasizeInfos = 0
g_NumCityTabTypes = 0
g_NumHurryInfos = 0
g_NumUnitClassInfos = 0
g_NumBuildingClassInfos = 0
g_NumProjectInfos = 0
g_NumProcessInfos = 0
g_NumActionInfos = 0
g_eEndTurnButtonState = -1

# BUG - city specialist - start
g_iSuperSpecialistCount = 0
g_iCitySpecialistCount = 0
g_iAngryCitizensCount = 0
SUPER_SPECIALIST_STACK_WIDTH = 15
SPECIALIST_ROW_HEIGHT = 34
SPECIALIST_ROWS = 3
MAX_SPECIALIST_BUTTON_SPACING = 30
SPECIALIST_AREA_MARGIN = 45
# BUG - city specialist - end

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
	
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
# BUG - PLE - start
	def __init__(self):
	
		self.PLOT_LIST_BUTTON_NAME 		= "MyPlotListButton"		
		self.PLOT_LIST_MINUS_NAME 		= "MyPlotListMinus"
		self.PLOT_LIST_PLUS_NAME 		= "MyPlotListPlus"
		self.PLOT_LIST_UP_NAME 			= "MyPlotListUp"
		self.PLOT_LIST_DOWN_NAME 		= "MyPlotListDown"
		self.PLOT_LIST_PROMO_NAME 		= "MyPlotListPromo"		
		self.PLOT_LIST_UPGRADE_NAME 	= "MyPlotListUpgrade"		
		
		self.PLE_VIEW_MODE 		 	   	= "PLE_VIEW_MODE1"
		self.PLE_MODE_STANDARD 			= "PLE_MODE_STANDARD1"
		self.PLE_MODE_MULTILINE 		= "PLE_MODE_MULTILINE1"
		self.PLE_MODE_STACK_VERT 		= "PLE_MODE_STACK_VERT1"
		self.PLE_MODE_STACK_HORIZ 		= "PLE_MODE_STACK_HORIZ1"
		self.PLE_VIEW_MODES = ( self.PLE_MODE_STANDARD, 
							    self.PLE_MODE_MULTILINE,
							    self.PLE_MODE_STACK_VERT,
							    self.PLE_MODE_STACK_HORIZ )
		self.PLE_VIEW_MODE_CYCLE = { self.PLE_MODE_STANDARD : self.PLE_MODE_MULTILINE,
									 self.PLE_MODE_MULTILINE : self.PLE_MODE_STACK_VERT,
									 self.PLE_MODE_STACK_VERT : self.PLE_MODE_STACK_HORIZ,
									 self.PLE_MODE_STACK_HORIZ : self.PLE_MODE_STANDARD }
		self.PLE_VIEW_MODE_ART = { self.PLE_MODE_STANDARD : "PLE_MODE_STANDARD",
									 self.PLE_MODE_MULTILINE : "PLE_MODE_MULTILINE",
									 self.PLE_MODE_STACK_VERT : "PLE_MODE_STACK_VERT",
									 self.PLE_MODE_STACK_HORIZ : "PLE_MODE_STACK_HORIZ" }
		
		self.PLE_RESET_FILTERS			= "PLE_RESET_FILTERS1"
		self.PLE_FILTER_NOTWOUND		= "PLE_FILTER_NOTWOUND1"
		self.PLE_FILTER_WOUND			= "PLE_FILTER_WOUND1"
		self.PLE_FILTER_LAND			= "PLE_FILTER_LAND1"
		self.PLE_FILTER_SEA				= "PLE_FILTER_SEA1"
		self.PLE_FILTER_AIR				= "PLE_FILTER_AIR1"
		self.PLE_FILTER_MIL				= "PLE_FILTER_MIL1"
		self.PLE_FILTER_DOM				= "PLE_FILTER_DOM1"
		self.PLE_FILTER_OWN				= "PLE_FILTER_OWN1"
		self.PLE_FILTER_FOREIGN			= "PLE_FILTER_FOREIGN1"
		self.PLE_FILTER_CANMOVE			= "PLE_FILTER_CANMOVE1"
		self.PLE_FILTER_CANTMOVE		= "PLE_FILTER_CANTMOVE1"
		
		self.PLE_PROMO_BUTTONS_UNITINFO = "PLE_PROMO_BUTTONS_UNITINFO"

		self.PLE_GRP_UNITTYPE			= "PLE_GRP_UNITTYPE1"
		self.PLE_GRP_GROUPS				= "PLE_GRP_GROUPS1"
		self.PLE_GRP_PROMO				= "PLE_GRP_PROMO1"
		self.PLE_GRP_UPGRADE			= "PLE_GRP_UPGRADE1"
		self.PLE_GROUP_MODES = ( self.PLE_GRP_UNITTYPE, 
								 self.PLE_GRP_GROUPS,
								 self.PLE_GRP_PROMO,
								 self.PLE_GRP_UPGRADE )

		self.UNIT_INFO_PANE				= "PLE_UNIT_INFO_PANE_ID"
		self.UNIT_INFO_TEXT				= "PLE_UNIT_INFO_TEXT_ID"
		self.UNIT_INFO_TEXT_SHADOW		= "PLE_UNIT_INFO_TEXT_SHADOW_ID"
		
		# filter constants
		self.nPLEFilterModeCanMove		= 0x0001
		self.nPLEFilterModeCantMove		= 0x0002
		self.nPLEFilterModeWound		= 0x0004
		self.nPLEFilterModeNotWound		= 0x0008
		self.nPLEFilterModeAir 			= 0x0010
		self.nPLEFilterModeSea 			= 0x0020
		self.nPLEFilterModeLand			= 0x0040
		self.nPLEFilterModeDom			= 0x0080
		self.nPLEFilterModeMil			= 0x0100
		self.nPLEFilterModeOwn			= 0x0200
		self.nPLEFilterModeForeign		= 0x0400
		
		self.nPLEFilterGroupHealth	    = self.nPLEFilterModeWound | self.nPLEFilterModeNotWound
		self.nPLEFilterGroupDomain	   	= self.nPLEFilterModeAir | self.nPLEFilterModeSea | self.nPLEFilterModeLand
		self.nPLEFilterGroupType        = self.nPLEFilterModeDom | self.nPLEFilterModeMil
		self.nPLEFilterGroupOwner       = self.nPLEFilterModeOwn | self.nPLEFilterModeForeign
		self.nPLEFilterGroupMove  	    = self.nPLEFilterModeCanMove | self.nPLEFilterModeCantMove
		
		self.nPLEAllFilters = self.nPLEFilterGroupHealth | self.nPLEFilterGroupDomain | self.nPLEFilterGroupType | self.nPLEFilterGroupOwner | self.nPLEFilterGroupMove

		# set all filters to active -> all units 
		self.nPLEFilter 				= self.nPLEAllFilters
		
		self.MainInterfaceInputMap = {
			self.PLOT_LIST_BUTTON_NAME		: self.getPlotListButtonName,
			self.PLOT_LIST_MINUS_NAME		: self.getPlotListMinusName,
			self.PLOT_LIST_PLUS_NAME		: self.getPlotListPlusName,
			self.PLOT_LIST_UP_NAME 			: self.getPlotListUpName,
			self.PLOT_LIST_DOWN_NAME 		: self.getPlotListDownName,
			self.PLE_VIEW_MODE   	   	    : self.onClickPLEViewMode,
			self.PLE_MODE_STANDARD			: self.onClickPLEModeStandard,
			self.PLE_MODE_MULTILINE			: self.onClickPLEModeMultiline,
			self.PLE_MODE_STACK_VERT		: self.onClickPLEModeStackVert,
			self.PLE_MODE_STACK_HORIZ		: self.onClickPLEModeStackHoriz,
			self.PLE_RESET_FILTERS   	    : self.onClickPLEResetFilters,
			self.PLE_FILTER_CANMOVE			: self.onClickPLEFilterCanMove,
			self.PLE_FILTER_CANTMOVE		: self.onClickPLEFilterCantMove,
			self.PLE_FILTER_NOTWOUND		: self.onClickPLEFilterNotWound,
			self.PLE_FILTER_WOUND			: self.onClickPLEFilterWound,
			self.PLE_FILTER_LAND			: self.onClickPLEFilterLand,
			self.PLE_FILTER_SEA				: self.onClickPLEFilterSea,
			self.PLE_FILTER_AIR				: self.onClickPLEFilterAir,
			self.PLE_FILTER_MIL				: self.onClickPLEFilterMil,
			self.PLE_FILTER_DOM				: self.onClickPLEFilterDom,
			self.PLE_FILTER_OWN				: self.onClickPLEFilterOwn,
			self.PLE_FILTER_FOREIGN			: self.onClickPLEFilterForeign,
			self.PLE_GRP_UNITTYPE			: self.onClickPLEGrpUnittype,
			self.PLE_GRP_GROUPS				: self.onClickPLEGrpGroups,
			self.PLE_GRP_PROMO				: self.onClickPLEGrpPromo,
			self.PLE_GRP_UPGRADE			: self.onClickPLEGrpUpgrade,
			self.PLOT_LIST_PROMO_NAME		: self.unitPromotion,		
			self.PLOT_LIST_UPGRADE_NAME		: self.unitUpgrade,
		}		
		
		self.iColOffset 			= 0
		self.iRowOffset 			= 0
		self.iVisibleUnits 			= 0
		self.pActPlot 				= 0
		self.pOldPlot 				= self.pActPlot
		self.sPLEMode 				= self.PLE_VIEW_MODES[BugPle.getDefaultViewMode()]
		self.iMaxPlotListIcons 		= 0
		self.nPLEGrpMode 			= self.PLE_GROUP_MODES[BugPle.getDefaultGroupMode()]
		self.nPLELastGrpMode  	    = self.nPLEGrpMode
		self.pActPlotListUnit		= 0
		self.iActPlotListGroup		= 0
		self.pLastPlotListUnit		= 0
		self.iLastPlotListGroup		= 0
	
		self.IDX_PLAYER				= 0
		self.IDX_DOMAIN 			= 1
		self.IDX_GROUPID			= 2
		self.IDX_COMBAT				= 3
		self.IDX_UNITTYPE			= 4
		self.IDX_LEVEL				= 5
		self.IDX_XP					= 6
		self.IDX_TRANSPORTID		= 7
		self.IDX_CARGOID			= 8
		self.IDX_UNITID				= 9
		self.IDX_UNIT				= 10
		
		self.lPLEUnitList 			= []
		self.lPLEUnitListTempOK		= []
		self.lPLEUnitListTempNOK	= []
		self.dPLEUnitInfo 			= {}	
		
		self.iLoopCnt 				= 0
		self.bPLEHide 				= False
		self.bUpdatePLEUnitList 	= True
		
		self.dUnitPromoList			= {}
		self.dUnitUpgradeList		= {}		
		
		self.bInit					= False
		
		self.ASMA 					= AStarMoveArea()
		
		self.tLastMousePos			= (0,0)
		self.bInfoPaneActive		= False
		self.bUnitPromoButtonsActive = False
		self.iMousePosTol			= 30
		self.iInfoPaneCnt			= 0
		self.iLastInfoPaneCnt		= -1

		self.xResolution = 0
		self.yResolution = 0

############## Basic operational functions ###################

	# Returns True if the given filter is active
	# You can pass in a filter group to see if any of its filters is active
	def isPLEFilter(self, nFilter):
		return self.nPLEFilter & nFilter != nFilter

	# Sets or toggles a specific filter button (wounded, air, etc) based on the PLE/BUG mode
	def setPLEFilter(self, nFilter, nFilterGroup):
		self.hideInfoPane()
		if (BugPle.isBugFilterBehavior()):
			bWasSelected = self.isPLEFilter(nFilter)
			# Clear all filters in group
			self.nPLEFilter |= nFilterGroup
			if (not bWasSelected):
				# Select the specified mode
				self.nPLEFilter ^= nFilter
		else:
			# Toggle the specified mode
			self.nPLEFilter ^= nFilter
		CyInterface().setDirty(InterfaceDirtyBits.PlotListButtons_DIRTY_BIT, True)
	
	def resetPLEFilters(self):
		self.nPLEFilter = self.nPLEAllFilters
		CyInterface().setDirty(InterfaceDirtyBits.PlotListButtons_DIRTY_BIT, True)

	# Sets the grouping mode (includes upgrade and promotion modes)
	def setPLEGroupMode(self, nGroupingMode):
		self.hideInfoPane()
		if (self.nPLEGrpMode != nGroupingMode):
			self.nPLEGrpMode = nGroupingMode
			self.bUpdatePLEUnitList = True
			CyInterface().setDirty(InterfaceDirtyBits.PlotListButtons_DIRTY_BIT, True)

	# Sets the view mode
	def setPLEViewMode(self, nViewMode):
		self.hideInfoPane()
		if (self.sPLEMode != nViewMode):
			self.iRowOffset = 0
			self.iColOffset = 0
			self.sPLEMode = nViewMode
			CyInterface().setDirty(InterfaceDirtyBits.PlotListButtons_DIRTY_BIT, True)

############## input handlers functions ######################

	def handleHoverPLEFilter(self, inputClass, sKey, nFilter):
		"Shows or hides the correct hover text for the given filter."
		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_ON ):
			sFullKey = "TXT_KEY_PLE_FILTER_"
			if ( BugPle.isBugFilterBehavior() ):
				sFullKey += "BUG_"
			sFullKey += sKey
			bSelected = self.isPLEFilter(nFilter)
			if ( bSelected ):
				sFullKey += "_ON"
			self.displayInfoPane(BugUtil.getPlainText(sFullKey))
			return 1
		elif ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_OFF ):
			self.hideInfoPane()
			return 1
		return 0

	def handleHoverPLEViewMode(self, inputClass, sKey, nViewMode):
		"Shows or hides the hover text for the given view mode."
		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_ON ):
			sFullKey = "TXT_KEY_PLE_MODE_" + sKey
			bSelected = self.sPLEMode == nViewMode
			#if ( bSelected ):
			#	sFullKey += "_ON"
			self.displayInfoPane(BugUtil.getPlainText(sFullKey))
			return 1
		elif ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_OFF ):
			self.hideInfoPane()
			return 1
		return 0

	def handleHoverPLEGrpMode(self, inputClass, sKey, nGrpMode):
		"Shows or hides the hover text for the given view mode."
		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_ON ):
			sFullKey = "TXT_KEY_PLE_GRP_" + sKey
			if ( sKey == "STANDARD" ):
				bSelected = self.nPLEGrpMode in (self.PLE_GRP_UNITTYPE, self.PLE_GRP_GROUPS)
			elif ( sKey == "PROMO" ):
				bSelected = self.nPLEGrpMode == self.PLE_GRP_PROMO
			elif ( sKey == "UPGRADE" ):
				bSelected = self.nPLEGrpMode == self.PLE_GRP_UPGRADE
			if ( bSelected ):
				sFullKey += "_ON"
			self.displayInfoPane(BugUtil.getPlainText(sFullKey))
			return 1
		elif ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_OFF ):
			self.hideInfoPane()
			return 1
		return 0


	# PLE Mode Switcher functions
	def onClickPLEResetFilters(self, inputClass):
		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED ):
			self.resetPLEFilters()
			return 1
		elif ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_ON ):
			sFullKey = "TXT_KEY_PLE_RESET_FILTERS"
			bSelected = self.isPLEFilter(self.nPLEAllFilters)
			if ( bSelected ):
				sFullKey += "_ON"
			self.displayInfoPane(BugUtil.getPlainText(sFullKey))
			return 1
		elif ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_OFF ):
			self.hideInfoPane()
			return 1
		return 0


	# PLE Movement Filters
	def onClickPLEFilterCanMove(self, inputClass):
		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED ):
			self.setPLEFilter(self.nPLEFilterModeCanMove, self.nPLEFilterGroupMove)
			return 1
		else:
			return self.handleHoverPLEFilter(inputClass, "CANMOVE", self.nPLEFilterModeCanMove)

	def onClickPLEFilterCantMove(self, inputClass):
		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED ):
			self.setPLEFilter(self.nPLEFilterModeCantMove, self.nPLEFilterGroupMove)
			return 1
		else:
			return self.handleHoverPLEFilter(inputClass, "CANTMOVE", self.nPLEFilterModeCantMove)
	
	
	# PLE Health Filters
	def onClickPLEFilterNotWound(self, inputClass):
		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED ):
			self.setPLEFilter(self.nPLEFilterModeNotWound, self.nPLEFilterGroupHealth)
			return 1
		else:
			return self.handleHoverPLEFilter(inputClass, "HEALTHY", self.nPLEFilterModeNotWound)
			
	def onClickPLEFilterWound(self, inputClass):
		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED ):
			self.setPLEFilter(self.nPLEFilterModeWound, self.nPLEFilterGroupHealth)
			return 1
		else:
			return self.handleHoverPLEFilter(inputClass, "WOUNDED", self.nPLEFilterModeWound)


	# PLE Domain Filters
	def onClickPLEFilterLand(self, inputClass):
		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED ):
			self.setPLEFilter(self.nPLEFilterModeLand, self.nPLEFilterGroupDomain)
			return 1
		else:
			return self.handleHoverPLEFilter(inputClass, "LAND", self.nPLEFilterModeLand)

	def onClickPLEFilterSea(self, inputClass):
		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED ):
			self.setPLEFilter(self.nPLEFilterModeSea, self.nPLEFilterGroupDomain)
			return 1
		else:
			return self.handleHoverPLEFilter(inputClass, "SEA", self.nPLEFilterModeSea)

	def onClickPLEFilterAir(self, inputClass):
		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED ):
			self.setPLEFilter(self.nPLEFilterModeAir, self.nPLEFilterGroupDomain)
			return 1
		else:
			return self.handleHoverPLEFilter(inputClass, "AIR", self.nPLEFilterModeAir)


	# PLE Domain Filters
	def onClickPLEFilterMil(self, inputClass):
		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED ):
			self.setPLEFilter(self.nPLEFilterModeMil, self.nPLEFilterGroupType)
			return 1
		else:
			return self.handleHoverPLEFilter(inputClass, "MIL", self.nPLEFilterModeMil)

	def onClickPLEFilterDom(self, inputClass):
		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED ):
			self.setPLEFilter(self.nPLEFilterModeDom, self.nPLEFilterGroupType)
			return 1
		else:
			return self.handleHoverPLEFilter(inputClass, "DOM", self.nPLEFilterModeDom)
			
	
	# PLE Ownership Filters
	def onClickPLEFilterOwn(self, inputClass):
		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED ):
			self.setPLEFilter(self.nPLEFilterModeOwn, self.nPLEFilterGroupOwner)
			return 1
		else:
			return self.handleHoverPLEFilter(inputClass, "OWN", self.nPLEFilterModeOwn)
			
	def onClickPLEFilterForeign(self, inputClass):
		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED ):
			self.setPLEFilter(self.nPLEFilterModeForeign, self.nPLEFilterGroupOwner)
			return 1
		else:
			return self.handleHoverPLEFilter(inputClass, "FOREIGN", self.nPLEFilterModeForeign)


	# PLE Grouping Modes
	def onClickPLEGrpUnittype(self, inputClass):
		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED ):
			if (self.nPLEGrpMode == self.PLE_GRP_UNITTYPE):
				self.setPLEGroupMode(self.PLE_GRP_GROUPS)
				self.nPLELastGrpMode = self.PLE_GRP_GROUPS
			elif (self.nPLEGrpMode == self.PLE_GRP_GROUPS):
				self.setPLEGroupMode(self.PLE_GRP_UNITTYPE)
				self.nPLELastGrpMode = self.PLE_GRP_UNITTYPE
			else:
				self.setPLEGroupMode(self.nPLELastGrpMode)
			return 1
		else:
			return self.handleHoverPLEGrpMode(inputClass, "STANDARD", self.PLE_GRP_UNITTYPE)

	def onClickPLEGrpGroups(self, inputClass):
		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED ):
			self.setPLEGroupMode(self.PLE_GRP_GROUPS)
			return 1
		else:
			return self.handleHoverPLEGrpMode(inputClass, "GROUPS", self.PLE_GRP_GROUPS)

	def onClickPLEGrpPromo(self, inputClass):
		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED ):
			if ( self.nPLEGrpMode == self.PLE_GRP_PROMO ):
				self.setPLEGroupMode(self.nPLELastGrpMode)
			else:
				self.setPLEGroupMode(self.PLE_GRP_PROMO)
			return 1
		else:
			return self.handleHoverPLEGrpMode(inputClass, "PROMO", self.PLE_GRP_PROMO)

	def onClickPLEGrpUpgrade(self, inputClass):
		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED ):
			if ( self.nPLEGrpMode == self.PLE_GRP_UPGRADE ):
				self.setPLEGroupMode(self.nPLELastGrpMode)
			else:
				self.setPLEGroupMode(self.PLE_GRP_UPGRADE)
			return 1
		else:
			return self.handleHoverPLEGrpMode(inputClass, "UPGRADE", self.PLE_GRP_UPGRADE)


	# PLE View Modes
	def onClickPLEViewMode(self, inputClass):
		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED ):
			if ( self.sPLEMode in self.PLE_VIEW_MODE_CYCLE ):
				self.setPLEViewMode(self.PLE_VIEW_MODE_CYCLE[self.sPLEMode])
			else:
				self.setPLEViewMode(BugPle.getDefaultViewMode())
			return 1
		elif ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_ON ):
			sFullKey = "TXT_KEY_PLE_VIEW_MODE"
			self.displayInfoPane(BugUtil.getPlainText(sFullKey))
			return 1
		elif ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_OFF ):
			self.hideInfoPane()
			return 1
		return 0
				
	def onClickPLEModeStandard(self, inputClass):
		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED ):
			self.setPLEViewMode(self.PLE_MODE_STANDARD)
			return 1
		else:
			return self.handleHoverPLEViewMode(inputClass, "STANDARD", self.PLE_MODE_STANDARD)
				
	def onClickPLEModeMultiline(self, inputClass):
		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED ):
			self.setPLEViewMode(self.PLE_MODE_MULTILINE)
			return 1
		else:
			return self.handleHoverPLEViewMode(inputClass, "MULTILINE", self.PLE_MODE_MULTILINE)

	def onClickPLEModeStackVert(self, inputClass):
		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED ):
			self.setPLEViewMode(self.PLE_MODE_STACK_VERT)
			return 1
		else:
			return self.handleHoverPLEViewMode(inputClass, "STACK_VERT", self.PLE_MODE_STACK_VERT)

	def onClickPLEModeStackHoriz(self, inputClass):
		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED ):
			self.setPLEViewMode(self.PLE_MODE_STACK_HORIZ)
			return 1
		else:
			return self.handleHoverPLEViewMode(inputClass, "STACK_HORIZ", self.PLE_MODE_STACK_HORIZ)


	# handles the unit promotion button inputs
	def unitPromotion(self, inputClass):
		id = inputClass.getID()
		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_ON ):
			if not CyInterface().isCityScreenUp():
				self.showPromoInfoPane(id)
			return 1
		elif ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_OFF ):
			self.hidePromoInfoPane()				
			return 1
		elif ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED ):
			self.doPromotion(id)
			CyInterface().setDirty(InterfaceDirtyBits.PlotListButtons_DIRTY_BIT, True)
			return 1

	# Arrow Up
	def getPlotListUpName(self, inputClass):
		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED ):
			self.iRowOffset += 1
			CyInterface().setDirty(InterfaceDirtyBits.PlotListButtons_DIRTY_BIT, True)
			return 1
		return 0
		
	# Arrow Down
	def getPlotListDownName(self, inputClass):
		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED ):
			if (self.iRowOffset > 0):
				self.iRowOffset -= 1
				CyInterface().setDirty(InterfaceDirtyBits.PlotListButtons_DIRTY_BIT, True)
				return 1
		return 0
		
	# Arrow Left
	def getPlotListMinusName(self, inputClass):
		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED ):
			if (self.iColOffset > 0):
				self.iColOffset -= 1
				CyInterface().setDirty(InterfaceDirtyBits.PlotListButtons_DIRTY_BIT, True)
				return 1
		return 0
		
	# Arrow Right
	def getPlotListPlusName(self, inputClass):
		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED ):
			self.iColOffset += 1
			CyInterface().setDirty(InterfaceDirtyBits.PlotListButtons_DIRTY_BIT, True)
			return 1
		return 0
	
	# determines the unit button
	def getPlotListButtonName(self, inputClass):
		id = inputClass.getID()
		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_ON ):
			if not CyInterface().isCityScreenUp():
				self.showUnitInfoPane(id)
			if mt.bAlt():
				self.highlightMoves(id)
			return 1
		elif ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_OFF ):
			self.hideUnitInfoPane()				
			if mt.bAlt():
				self.dehighlightMoves()
			return 1
		elif ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED ):
			# mt.debug("id:%i;p:(%i;%i)"%(id, self.pActPlot.getX(), self.pActPlot.getY()))
			if (id >= 0) and (id <= self.iMaxPlotListIcons):
				self.selectGroup( id, mt.bShift(), mt.bCtrl(), mt.bAlt())
				CyInterface().setDirty(InterfaceDirtyBits.PlotListButtons_DIRTY_BIT, True)
				return 1
		return 0

	# handles the unit upgrade button inputs
	def unitUpgrade(self, inputClass):
		id = inputClass.getID()
		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_ON ):
			if not CyInterface().isCityScreenUp():
				self.showUpgradeInfoPane(id)
			return 1
		elif ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_OFF ):
			self.hideUpgradeInfoPane()				
			return 1
		elif ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED ):
#			mt.debug("upgrade id:"+str(id))
			self.doUpgrade(id)
			CyInterface().setDirty(InterfaceDirtyBits.PlotListButtons_DIRTY_BIT, True)
			return 1
		
############## base functions to calculate/transform the number of objects dependent on the screen resolution ######################

	def getMaxCol(self):
		return ((self.xResolution - (iMultiListXL+iMultiListXR) - 68) / 34)
		
	def getMaxRow(self):
		return ((self.yResolution - 160) / BugPle.getVerticalSpacing()) 
		
	def getRow(self, i):
		return i / self.getMaxCol()

	def getCol(self, i):
		return i % self.getMaxCol()
		
	def getX(self, nCol):
		return 315 + (nCol * BugPle.getHoriztonalSpacing())
		
	def getY(self, nRow):
		return self.yResolution - 169 - (nRow * BugPle.getVerticalSpacing())
		
	def getI(self, nRow, nCol):
		return ( nRow * self.getMaxCol() ) + ( nCol % self.getMaxCol() )

############## functions for visual objects (show and hide) ######################
		
	# PLE Grouping Mode Switcher 
	def setupPLEGroupModeButtons(self, screen):
		if (self.nPLEGrpMode == self.PLE_GRP_UNITTYPE):
			screen.changeImageButton(self.PLE_GRP_UNITTYPE, ArtFileMgr.getInterfaceArtInfo("PLE_GRP_UNITTYPE").getPath())
			screen.setState(self.PLE_GRP_UNITTYPE, True)
		elif (self.nPLEGrpMode == self.PLE_GRP_GROUPS):
			screen.changeImageButton(self.PLE_GRP_UNITTYPE, ArtFileMgr.getInterfaceArtInfo("PLE_GRP_GROUPS").getPath())
			screen.setState(self.PLE_GRP_UNITTYPE, True)
		else:
			screen.setState(self.PLE_GRP_UNITTYPE, False)
		#screen.setState(self.PLE_GRP_UNITTYPE, self.nPLEGrpMode == self.PLE_GRP_UNITTYPE or self.nPLEGrpMode == self.PLE_GRP_GROUPS)
		#screen.setState(self.PLE_GRP_GROUPS, self.nPLEGrpMode == self.PLE_GRP_GROUPS)
		screen.setState(self.PLE_GRP_PROMO, self.nPLEGrpMode == self.PLE_GRP_PROMO)
		screen.setState(self.PLE_GRP_UPGRADE, self.nPLEGrpMode == self.PLE_GRP_UPGRADE)
		
	# PLE View Mode Switcher
	def setupPLEViewModeButtons(self, screen):
		screen.changeImageButton(self.PLE_VIEW_MODE, ArtFileMgr.getInterfaceArtInfo(self.PLE_VIEW_MODE_ART[self.sPLEMode]).getPath())
#		screen.setState(self.PLE_MODE_STANDARD, self.sPLEMode == self.PLE_MODE_STANDARD)
#		screen.setState(self.PLE_MODE_MULTILINE, self.sPLEMode == self.PLE_MODE_MULTILINE)
#		screen.setState(self.PLE_MODE_STACK_VERT, self.sPLEMode == self.PLE_MODE_STACK_VERT)
#		screen.setState(self.PLE_MODE_STACK_HORIZ, self.sPLEMode == self.PLE_MODE_STACK_HORIZ)
	
	# PLE Filters
	def setupPLEFilterButtons(self, screen):
		screen.setState(self.PLE_FILTER_CANMOVE, self.isPLEFilter(self.nPLEFilterModeCanMove))
		screen.setState(self.PLE_FILTER_CANTMOVE, self.isPLEFilter(self.nPLEFilterModeCantMove))
		
		screen.setState(self.PLE_FILTER_NOTWOUND, self.isPLEFilter(self.nPLEFilterModeNotWound))
		screen.setState(self.PLE_FILTER_WOUND, self.isPLEFilter(self.nPLEFilterModeWound))
		
		screen.setState(self.PLE_FILTER_LAND, self.isPLEFilter(self.nPLEFilterModeLand))
		screen.setState(self.PLE_FILTER_SEA, self.isPLEFilter(self.nPLEFilterModeSea))
		screen.setState(self.PLE_FILTER_AIR, self.isPLEFilter(self.nPLEFilterModeAir))

		screen.setState(self.PLE_FILTER_MIL, self.isPLEFilter(self.nPLEFilterModeMil))
		screen.setState(self.PLE_FILTER_DOM, self.isPLEFilter(self.nPLEFilterModeDom))
		
		screen.setState(self.PLE_FILTER_OWN, self.isPLEFilter(self.nPLEFilterModeOwn))
		screen.setState(self.PLE_FILTER_FOREIGN, self.isPLEFilter(self.nPLEFilterModeForeign))
		
		return 0

	# Displays the plot list switches (views, filters, groupings)
	def showPlotListButtonObjects(self, screen):
		if ( BugPle.isShowButtons() and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_MINIMAP_ONLY and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_ADVANCED_START ):
			# show PLE modes switches
			self.setupPLEViewModeButtons(screen)
			screen.show(self.PLE_VIEW_MODE)
#			screen.show(self.PLE_MODE_STANDARD)
#			screen.show(self.PLE_MODE_MULTILINE)
#			screen.show(self.PLE_MODE_STACK_VERT)
#			screen.show(self.PLE_MODE_STACK_HORIZ)
			
			# show PLE filter switches
			screen.show(self.PLE_RESET_FILTERS)
			
			self.setupPLEFilterButtons(screen)
			screen.show(self.PLE_FILTER_CANMOVE)
			screen.show(self.PLE_FILTER_CANTMOVE)
			
			screen.show(self.PLE_FILTER_NOTWOUND)
			screen.show(self.PLE_FILTER_WOUND)
			
			screen.show(self.PLE_FILTER_LAND)
			screen.show(self.PLE_FILTER_SEA)
			screen.show(self.PLE_FILTER_AIR)
			
			screen.show(self.PLE_FILTER_MIL)
			screen.show(self.PLE_FILTER_DOM)
			
			screen.show(self.PLE_FILTER_OWN)
			screen.show(self.PLE_FILTER_FOREIGN)
			
			# show PLE grouping switches
			self.setupPLEGroupModeButtons(screen)
			screen.show(self.PLE_GRP_UNITTYPE)
			screen.show(self.PLE_GRP_GROUPS)
			screen.show(self.PLE_GRP_PROMO)
			screen.show(self.PLE_GRP_UPGRADE)
	
			self.bPLEHide = False


	# hides all plot list switches (views, filters, groupings) and all the other objects
	def hidePlotListButtonObjects(self, screen):
		# hides all unit button objects
		for i in range( self.iMaxPlotListIcons ):
			# hide unit button
			szString = self.PLOT_LIST_BUTTON_NAME + str(i)
			screen.hide( szString )
			# hide colored spot
			szStringIcon = szString+"Icon"
			screen.hide( szStringIcon )
			# hide health bar
			szStringHealthBar = szString+"HealthBar"
			screen.hide( szStringHealthBar )
			# hide move bar
			szStringMoveBar = szString+"MoveBar"
			screen.hide( szStringMoveBar )
			# hide promotion frame
			szStringPromoFrame = szString+"PromoFrame"
			screen.hide( szStringPromoFrame )
			# hide mission info
			szStringActionIcon = szString+"ActionIcon"
			screen.hide( szStringActionIcon )
			# hide upgrade arrow
			szStringUpgrade = szString+"Upgrade"
			screen.hide( szStringUpgrade )
			# hide GG star
			szStringUpgrade = szString+"GreatGeneral"
			screen.hide( szStringUpgrade )

		# hides all promotion and upgrade button objects
		for nCol in range(self.getMaxCol()+1):
			for nRow in range(self.getMaxRow()+1):
				# 
				szStringUnitPromo = self.PLOT_LIST_PROMO_NAME + string.zfill(str(nRow), 2) + string.zfill(str(nCol), 2)
				screen.hide( szStringUnitPromo )		
				# 
				szStringUnitUpgrade = self.PLOT_LIST_UPGRADE_NAME + string.zfill(str(nRow), 2) + string.zfill(str(nCol), 2)
				screen.hide( szStringUnitUpgrade )				
		
		# hide PLE modes switches
		screen.hide(self.PLE_VIEW_MODE)
#		screen.hide(self.PLE_MODE_STANDARD)
#		screen.hide(self.PLE_MODE_MULTILINE)
#		screen.hide(self.PLE_MODE_STACK_VERT)
#		screen.hide(self.PLE_MODE_STACK_HORIZ)
		# hide horizontal scroll buttons
		screen.hide( self.PLOT_LIST_MINUS_NAME )
		screen.hide( self.PLOT_LIST_PLUS_NAME )
		# hide vertical scroll buttons
		screen.hide( self.PLOT_LIST_UP_NAME )
		screen.hide( self.PLOT_LIST_DOWN_NAME )
		# hide reset all filters button
		screen.hide(self.PLE_RESET_FILTERS)
		# hide PLE filter switches
		screen.hide(self.PLE_FILTER_CANMOVE)
		screen.hide(self.PLE_FILTER_CANTMOVE)
		screen.hide(self.PLE_FILTER_NOTWOUND)
		screen.hide(self.PLE_FILTER_WOUND)
		screen.hide(self.PLE_FILTER_LAND)
		screen.hide(self.PLE_FILTER_SEA)
		screen.hide(self.PLE_FILTER_AIR)
		screen.hide(self.PLE_FILTER_MIL)	
		screen.hide(self.PLE_FILTER_DOM)
		screen.hide(self.PLE_FILTER_OWN)	
		screen.hide(self.PLE_FILTER_FOREIGN)	
		# hide PLE group switches
		screen.hide(self.PLE_GRP_UNITTYPE)	
		screen.hide(self.PLE_GRP_GROUPS)	
		screen.hide(self.PLE_GRP_PROMO)	
		screen.hide(self.PLE_GRP_UPGRADE)	
		
		self.bPLEHide = True
		
	# prepares the display of the mode, view, grouping, filter  switches
	def preparePlotListObjects(self, screen):
		xResolution = self.xResolution
		yResolution = self.yResolution
	
		nYOff	= 130 + 4
		nXOff	= 290 - 12
		nSize	= 24
		nDist	= 22
		nGap    = 10
		nNum	= 0
		
		# place the PLE mode switches
		nXOff += nDist
		szString = self.PLE_VIEW_MODE
		screen.addCheckBoxGFC( szString, ArtFileMgr.getInterfaceArtInfo("PLE_MODE_STANDARD").getPath(), "", nXOff, yResolution - nYOff, nSize, nSize, WidgetTypes.WIDGET_GENERAL, 1, -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.hide( szString )
		
#		nXOff += nDist
#		szString = self.PLE_MODE_STANDARD
#		screen.addCheckBoxGFC( szString, ArtFileMgr.getInterfaceArtInfo("PLE_MODE_STANDARD").getPath(), ArtFileMgr.getInterfaceArtInfo("PLE_BUTTON_HILITE").getPath(), nXOff, yResolution - nYOff, nSize, nSize, WidgetTypes.WIDGET_GENERAL, 1, -1, ButtonStyles.BUTTON_STYLE_LABEL )
#		screen.hide( szString )
#		
#		nXOff += nDist
#		szString = self.PLE_MODE_MULTILINE
#		screen.addCheckBoxGFC( szString, ArtFileMgr.getInterfaceArtInfo("PLE_MODE_MULTILINE").getPath(), ArtFileMgr.getInterfaceArtInfo("PLE_BUTTON_HILITE").getPath(), nXOff, yResolution - nYOff, nSize, nSize, WidgetTypes.WIDGET_GENERAL, 2, -1, ButtonStyles.BUTTON_STYLE_LABEL )
#		screen.hide( szString )
#		
#		nXOff += nDist
#		szString = self.PLE_MODE_STACK_VERT
#		screen.addCheckBoxGFC( szString, ArtFileMgr.getInterfaceArtInfo("PLE_MODE_STACK_VERT").getPath(), ArtFileMgr.getInterfaceArtInfo("PLE_BUTTON_HILITE").getPath(), nXOff, yResolution - nYOff, nSize, nSize, WidgetTypes.WIDGET_GENERAL, 3, -1, ButtonStyles.BUTTON_STYLE_LABEL )
#		screen.hide( szString )
#		
#		nXOff += nDist
#		szString = self.PLE_MODE_STACK_HORIZ
#		screen.addCheckBoxGFC( szString, ArtFileMgr.getInterfaceArtInfo("PLE_MODE_STACK_HORIZ").getPath(), ArtFileMgr.getInterfaceArtInfo("PLE_BUTTON_HILITE").getPath(), nXOff, yResolution - nYOff, nSize, nSize, WidgetTypes.WIDGET_GENERAL, 4, -1, ButtonStyles.BUTTON_STYLE_LABEL )
#		screen.hide( szString )
		
		# place the PLE grouping mode switches
		nXOff += nDist + nGap
		szString = self.PLE_GRP_UNITTYPE
		screen.addCheckBoxGFC( szString, ArtFileMgr.getInterfaceArtInfo("PLE_GRP_UNITTYPE").getPath(), ArtFileMgr.getInterfaceArtInfo("PLE_BUTTON_HILITE").getPath(), nXOff, yResolution - nYOff, nSize, nSize, WidgetTypes.WIDGET_GENERAL, 1, -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.hide( szString )
		
#		nXOff += nDist
#		szString = self.PLE_GRP_GROUPS
#		screen.addCheckBoxGFC( szString, ArtFileMgr.getInterfaceArtInfo("PLE_GRP_GROUPS").getPath(), ArtFileMgr.getInterfaceArtInfo("PLE_BUTTON_HILITE").getPath(), nXOff, yResolution - nYOff, nSize, nSize, WidgetTypes.WIDGET_GENERAL, 1, -1, ButtonStyles.BUTTON_STYLE_LABEL )
#		screen.hide( szString )
		
		# place the promotion and upgrades mode switches
		nXOff += nDist
		szString = self.PLE_GRP_PROMO
		screen.addCheckBoxGFC( szString, ArtFileMgr.getInterfaceArtInfo("PLE_GRP_PROMO").getPath(), ArtFileMgr.getInterfaceArtInfo("PLE_BUTTON_HILITE").getPath(), nXOff, yResolution - nYOff, nSize, nSize, WidgetTypes.WIDGET_GENERAL, 1, -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.hide( szString )
		
		nXOff += nDist
		szString = self.PLE_GRP_UPGRADE
		screen.addCheckBoxGFC( szString, ArtFileMgr.getInterfaceArtInfo("PLE_GRP_UPGRADE").getPath(), ArtFileMgr.getInterfaceArtInfo("PLE_BUTTON_HILITE").getPath(), nXOff, yResolution - nYOff, nSize, nSize, WidgetTypes.WIDGET_GENERAL, 1, -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.hide( szString )
		
		# place the PLE reset filter button
		nXOff += nDist + nGap
		szString = self.PLE_RESET_FILTERS
		screen.addCheckBoxGFC( szString, ArtFileMgr.getInterfaceArtInfo("PLE_RESET_FILTERS").getPath(), "", nXOff, yResolution - nYOff, nSize, nSize, WidgetTypes.WIDGET_GENERAL, -1, -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.hide( szString )

		# place the PLE movement filter switches
		nXOff += nDist + nGap
		szString = self.PLE_FILTER_CANMOVE
		screen.addCheckBoxGFC( szString, ArtFileMgr.getInterfaceArtInfo("PLE_FILTER_CANMOVE").getPath(), ArtFileMgr.getInterfaceArtInfo("PLE_BUTTON_HILITE").getPath(), nXOff, yResolution - nYOff, nSize, nSize, WidgetTypes.WIDGET_GENERAL, 1, -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.hide( szString )
		
		nXOff += nDist
		szString = self.PLE_FILTER_CANTMOVE
		screen.addCheckBoxGFC( szString, ArtFileMgr.getInterfaceArtInfo("PLE_FILTER_CANTMOVE").getPath(), ArtFileMgr.getInterfaceArtInfo("PLE_BUTTON_HILITE").getPath(), nXOff, yResolution - nYOff, nSize, nSize, WidgetTypes.WIDGET_GENERAL, 1, -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.hide( szString )

		# place the PLE health filter switches
		nXOff += nDist + nGap
		szString = self.PLE_FILTER_NOTWOUND
		screen.addCheckBoxGFC( szString, ArtFileMgr.getInterfaceArtInfo("PLE_FILTER_NOTWOUND").getPath(), ArtFileMgr.getInterfaceArtInfo("PLE_BUTTON_HILITE").getPath(), nXOff, yResolution - nYOff, nSize, nSize, WidgetTypes.WIDGET_GENERAL, 1, -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.hide( szString )

		nXOff += nDist
		szString = self.PLE_FILTER_WOUND
		screen.addCheckBoxGFC( szString, ArtFileMgr.getInterfaceArtInfo("PLE_FILTER_WOUND").getPath(), ArtFileMgr.getInterfaceArtInfo("PLE_BUTTON_HILITE").getPath(), nXOff, yResolution - nYOff, nSize, nSize, WidgetTypes.WIDGET_GENERAL, 1, -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.hide( szString )

		# place the PLE domain filter switches
		nXOff += nDist + nGap
		szString = self.PLE_FILTER_LAND
		screen.addCheckBoxGFC( szString, ArtFileMgr.getInterfaceArtInfo("PLE_FILTER_LAND").getPath(), ArtFileMgr.getInterfaceArtInfo("PLE_BUTTON_HILITE").getPath(), nXOff, yResolution - nYOff, nSize, nSize, WidgetTypes.WIDGET_GENERAL, 1, -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.hide( szString )

		nXOff += nDist
		szString = self.PLE_FILTER_SEA
		screen.addCheckBoxGFC( szString, ArtFileMgr.getInterfaceArtInfo("PLE_FILTER_SEA").getPath(), ArtFileMgr.getInterfaceArtInfo("PLE_BUTTON_HILITE").getPath(), nXOff, yResolution - nYOff, nSize, nSize, WidgetTypes.WIDGET_GENERAL, 1, -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.hide( szString )

		nXOff += nDist
		szString = self.PLE_FILTER_AIR
		screen.addCheckBoxGFC( szString, ArtFileMgr.getInterfaceArtInfo("PLE_FILTER_AIR").getPath(), ArtFileMgr.getInterfaceArtInfo("PLE_BUTTON_HILITE").getPath(), nXOff, yResolution - nYOff, nSize, nSize, WidgetTypes.WIDGET_GENERAL, 1, -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.hide( szString )

		# place the PLE civilian/military filter switches
		nXOff += nDist + nGap
		szString = self.PLE_FILTER_MIL
		screen.addCheckBoxGFC( szString, ArtFileMgr.getInterfaceArtInfo("PLE_FILTER_MIL").getPath(), ArtFileMgr.getInterfaceArtInfo("PLE_BUTTON_HILITE").getPath(), nXOff, yResolution - nYOff, nSize, nSize, WidgetTypes.WIDGET_GENERAL, 1, -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.hide( szString )
		
		nXOff += nDist
		szString = self.PLE_FILTER_DOM
		screen.addCheckBoxGFC( szString, ArtFileMgr.getInterfaceArtInfo("PLE_FILTER_DOM").getPath(), ArtFileMgr.getInterfaceArtInfo("PLE_BUTTON_HILITE").getPath(), nXOff, yResolution - nYOff, nSize, nSize, WidgetTypes.WIDGET_GENERAL, 1, -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.hide( szString )
				
		# place the PLE owner filter switches
		nXOff += nDist + nGap
		szString = self.PLE_FILTER_OWN
		screen.addCheckBoxGFC( szString, ArtFileMgr.getInterfaceArtInfo("PLE_FILTER_OWN").getPath(), ArtFileMgr.getInterfaceArtInfo("PLE_BUTTON_HILITE").getPath(), nXOff, yResolution - nYOff, nSize, nSize, WidgetTypes.WIDGET_GENERAL, 1, -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.hide( szString )
		
		nXOff += nDist
		szString = self.PLE_FILTER_FOREIGN
		screen.addCheckBoxGFC( szString, ArtFileMgr.getInterfaceArtInfo("PLE_FILTER_FOREIGN").getPath(), ArtFileMgr.getInterfaceArtInfo("PLE_BUTTON_HILITE").getPath(), nXOff, yResolution - nYOff, nSize, nSize, WidgetTypes.WIDGET_GENERAL, 1, -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.hide( szString )
				
################ functions for normal/shift/ctrl/alt unit selection within the plot list itself #################

	# deselects all units in the plot list
	def deselectAll(self):
		for i in range(len(self.lPLEUnitList)):
			pUnit = self.getInterfacePlotUnit(i)
			if (pUnit.IsSelected()):
				CyInterface().selectUnit(pUnit, False, True, False)	
	
	# function saves all units not matching actual filter criteria in a temp list by type
	def saveFilteredUnitsByType(self, pCompareUnit, bShift):
		self.lPLEUnitListTempOK = []
		self.lPLEUnitListTempNOK = []
		# save unit type for comparision
		pCompareUnitType = pCompareUnit.getUnitType()
		for i in range(len(self.lPLEUnitList)):
			pLoopUnit = self.getInterfacePlotUnit(i)
			# has the unit the correct type and does the unit NOT match the filter parameters
			if (pLoopUnit.getUnitType() == pCompareUnitType) and (not (self.checkDisplayFilter(pLoopUnit))):
				# unit has to be moved
				self.lPLEUnitListTempNOK.append(pLoopUnit)
			else:
				# unit has to be displayed
				self.lPLEUnitListTempOK.append(pLoopUnit)
		# loop to find all the cargo of units in the OK list. They don't have to be moved away.
		lTempNOK 	= self.lPLEUnitListTempNOK[:]
		lTempOK 	= self.lPLEUnitListTempOK[:]
		for pLoopUnitNOK in lTempNOK:
			# check if unit is cargo
			if pLoopUnitNOK.isCargo():
				# check if the units transport unit is a to be displayed unit
				for pLoopUnitOK in lTempOK:
					if pLoopUnitOK.getID() == pLoopUnitNOK.getTransportUnit().getID():
						# remove cargo unit from NOK array and append it to OK array
						self.lPLEUnitListTempNOK.remove(pLoopUnitNOK)
						self.lPLEUnitListTempOK.append(pLoopUnitNOK)
		# if Shift is pressed, we also have to keep the already selected units 
		if bShift:
			lTempNOK 	= self.lPLEUnitListTempNOK[:]
			lTempOK 	= self.lPLEUnitListTempOK[:]
			for i in range(len(self.lPLEUnitList)):
				pLoopUnit = self.getInterfacePlotUnit(i)
				if (pLoopUnit.IsSelected()):
					if pLoopUnit in lTempNOK:
						self.lPLEUnitListTempNOK.remove(pLoopUnitNOK)
						self.lPLEUnitListTempOK.append(pLoopUnitNOK)
						
					
	# function saves all units not matching actual filter criteria in a temp list by domain
	def saveFilteredUnitsByDomain(self, pCompareUnit):
		self.lPLEUnitListTempOK = []
		self.lPLEUnitListTempNOK = []
		# save unit type for comparision
		pUnitTypeInfo = gc.getUnitInfo(pCompareUnit.getUnitType())
		eCompareDomain = pUnitTypeInfo.getDomainType()
		for i in range(len(self.lPLEUnitList)):
			pLoopUnit = self.getInterfacePlotUnit(i)
			pUnitTypeInfo = gc.getUnitInfo(pLoopUnit.getUnitType())
			eDomainType = pUnitTypeInfo.getDomainType()
			# has the unit the correct domain and ismatching the current filter criteria
			if (eDomainType == eCompareDomain) and (self.checkDisplayFilter(pLoopUnit)):					
				# unit has to be displayed
				self.lPLEUnitListTempOK.append(pLoopUnit)
			else:
				# unit has to be moved
				self.lPLEUnitListTempNOK.append(pLoopUnit)
		# loop to find all the cargo of units in the OK list. They don't have to be moved away.
		lTempNOK 	= self.lPLEUnitListTempNOK[:]
		lTempOK 	= self.lPLEUnitListTempOK[:]
		for pLoopUnitNOK in lTempNOK:
			# check if unit is cargo
			if pLoopUnitNOK.isCargo():
				# check if the units transport unit is a to be displayed unit
				for pLoopUnitOK in lTempOK:
					if pLoopUnitOK.getID() == pLoopUnitNOK.getTransportUnit().getID():
						# remove cargo unit from NOK array and append it to OK array
						self.lPLEUnitListTempNOK.remove(pLoopUnitNOK)
						self.lPLEUnitListTempOK.append(pLoopUnitNOK)
	
	# finds plots where we can temporarily park some units.
	# the "parking" is needed to avoid that the units are selected by the CyInterface.selectGroup() function.
	def getTempPlot(self):
		# first try : put them into another city
		pPlayer = gc.getActivePlayer()
		iPlayer = CyGame().getActivePlayer()
		lCity = PyPlayer(iPlayer).getCityList()
		pPlot = CyMap().plot(0,0)
		dPlotList = {}
		if not (self.pActPlot.isCity()):
			# if actual plot is not a city -> use first available city to park units
			pPlot = lCity[0].plot()
			for d in range(DomainTypes.NUM_DOMAIN_TYPES):	
				dPlotList[d] = pPlot
		elif (pPlayer.getNumCities() > 1):
			# if actual plot is a city -> use next available city to park units
			for i in range(pPlayer.getNumCities()):
				pPlot =  lCity[i].plot()
				if (pPlot.getX() != self.pActPlot.getX()) or (pPlot.getY() != self.pActPlot.getY()):
					break
			for d in range(DomainTypes.NUM_DOMAIN_TYPES):	
				dPlotList[d] = pPlot
		else:
			# no city available -> place units around the capital. There is the smallest chance to reveal a plot.
			lList = []
			pCapital = PyPlayer(iPlayer).getCapitalCity()
			for dx in range(-1, 2):
				for dy in range(-1, 2):
					if dx != 0 and dy != 0:
						pPlot = CyMap().plot(pCapital.getX()+dx, pCapital.getY()+dy)
						lList.append(pPlot)
			for d in range(DomainTypes.NUM_DOMAIN_TYPES):	
				dPlotList[d] = lList[d]				
		return dPlotList
			
	# temporarily moves a unit away, so that the select group works well.
	def tempMove(self, iMode):
		if iMode == 0:
			dTempPlots = self.getTempPlot()
		for i in range(len(self.lPLEUnitListTempNOK)):
			pLoopUnit = self.lPLEUnitListTempNOK[i]
			eDomainType = gc.getUnitInfo(pLoopUnit.getUnitType()).getDomainType()
			# move unit to temp plot. 
			if iMode == 0:				
				pTempPlot = dTempPlots[eDomainType]
				pLoopUnit.setXY( pTempPlot.getX(), pTempPlot.getY())
			else:
				pLoopUnit.setXY( self.pActPlot.getX(), self.pActPlot.getY() )

	# replacement of the civ 4 version
	def selectGroup(self, iID, bShift, bCtrl, bAlt):
		pUnit = self.listPLEButtons[iID][0]
		# check if the unit has been selected from the city screen
		bCityUp = CyInterface().isCityScreenUp()		
		if not (self.pActPlotListUnit):
			self.pActPlotListUnit = CyInterface().getHeadSelectedUnit()
			self.pActPlotListGroup = self.pActPlotListUnit.getGroupID()
		if (not (bShift or bCtrl or bAlt)):
#			# save prev selections
#			self.pLastPlotListUnit = self.pActPlotListUnit
#			self.iLastPlotListGroup = self.pActPlotListUnit.getGroupID()
			# save act selection
			self.pActPlotListUnit = pUnit
			self.iActPlotListGroup = pUnit.getGroupID()		
			CyInterface().selectGroup( self.pActPlotListUnit, false, false, false )
#			# check if the group has been changed 
#			if (self.iLastPlotListGroup != self.iActPlotListGroup):
#				self.deselectAll()
#			# deselect last selected unit
#			elif (self.pLastPlotListUnit):
#				if (self.pLastPlotListUnit.IsSelected()):
#					CyInterface().selectUnit(self.pLastPlotListUnit, false, true, false)
#			# check if the group has not been changed and the unit is selected again -> deselect all other units of the group
#			if (self.iLastPlotListGroup == self.iActPlotListGroup):
#				CyInterface().selectUnit(self.pActPlotListUnit, true, true, true)
#			else:
#				CyInterface().selectUnit(self.pActPlotListUnit, false, true, true)
		elif bShift and (not (bCtrl or bAlt)):
			self.pActPlotListUnit = pUnit
			self.iActPlotListGroup = pUnit.getGroupID()
#			CyInterface().selectUnit(self.pActPlotListUnit, false, true, true)
			CyInterface().selectGroup( self.pActPlotListUnit, true, false, false )
		elif bCtrl and (not (bShift or bAlt)):
			self.deselectAll()
			self.pActPlotListUnit = pUnit
			self.iActPlotListGroup = pUnit.getGroupID()
			self.saveFilteredUnitsByType(self.pActPlotListUnit, false)
			self.tempMove(0)
			CyInterface().selectGroup( self.pActPlotListUnit, false, true, false )
			self.tempMove(1)
			self.bUpdatePLEUnitList = true
		elif bCtrl and bShift and (not bAlt):
#			# self.deselectAll()
			self.pActPlotListUnit = pUnit
			self.iActPlotListGroup = pUnit.getGroupID()
			self.saveFilteredUnitsByType(self.pActPlotListUnit, true)
			self.tempMove(0)
			CyInterface().selectGroup( self.pActPlotListUnit, true, true, false )
			self.tempMove(1)
			self.bUpdatePLEUnitList = true
		elif bAlt and (not (bCtrl or bShift)):
			self.deselectAll()
			self.pActPlotListUnit = pUnit
			self.iActPlotListGroup = pUnit.getGroupID()
			self.saveFilteredUnitsByDomain(self.pActPlotListUnit)
			self.tempMove(0)
			CyInterface().selectGroup( self.pActPlotListUnit, false, false, true )
			self.tempMove(1)
			self.bUpdatePLEUnitList = true		
		# if we came from city screen -> focus view on the selected unit
		if bCityUp:
			CyCamera().JustLookAtPlot(self.pActPlot)

################## general PLE functions ##################

	# displays a single unit icon in the plot list with all its decorations
	def displayUnitPlotListObjects( self, screen, pLoopUnit, nRow, nCol ):
		iCount = self.getI(nRow, nCol)	
		self.listPLEButtons[iCount] = ( pLoopUnit, nRow, nCol )
		self.bPLEHide = False
		
		# create the button name 
		szString = self.PLOT_LIST_BUTTON_NAME + str(iCount)
		
		# set unit button image
		screen.changeImageButton( szString, gc.getUnitInfo(pLoopUnit.getUnitType()).getButton() )
		
		# check if it is an player unit or not
		if ( pLoopUnit.getOwner() == gc.getGame().getActivePlayer() ):
			bEnable = True
		else:
			bEnable = False
		# if player unit enable button (->visible, but not selectable)
		screen.enable(szString, bEnable)
		
		# check if the units is selected
		if (pLoopUnit.IsSelected()):
			screen.setState(szString, True)
		else:
			screen.setState(szString, False)
		# set select state of the unit button
		screen.show( szString )
		
		# this if statement and everything inside, handles the display of the colored buttons in the upper left corner of each unit icon.
		xSize = 12
		ySize = 12
		xOffset = 0
		yOffset = 0
		if ((pLoopUnit.getTeam() != gc.getGame().getActiveTeam()) or pLoopUnit.isWaiting()):
			# fortified
			szDotState = "OVERLAY_FORTIFY"								
		elif (pLoopUnit.canMove()):
			if (pLoopUnit.hasMoved()):
				# unit moved, but some movement points are left
				szDotState = "OVERLAY_HASMOVED"
			else:
				# unit did not move yet
				szDotState = "OVERLAY_MOVE"
		else:
			# unit has no movement points left
			szDotState = "OVERLAY_NOMOVE"
		
		# Wounded units will get a darker colored button.
		if (self.bShowWoundedIndicator) and (pLoopUnit.isHurt()):
			szDotState += "_INJURED"
		
		# Units lead by a GG will get a star instead of a dot.
		if (self.bShowGreatGeneralIndicator):
			# is unit lead by a GG?
			iLeaderPromo = gc.getInfoTypeForString('PROMOTION_LEADER')
			if (iLeaderPromo != -1 and pLoopUnit.isHasPromotion(iLeaderPromo)):
				szDotState += "_GG"
				xSize = 16
				ySize = 16
				xOffset = -3
				yOffset = -3
		
		szFileNameState = ArtFileMgr.getInterfaceArtInfo(szDotState).getPath()
		
		if (bEnable and self.bShowPromotionIndicator):
			# can unit be promoted ?
			if (pLoopUnit.isPromotionReady()):
				# place the promotion frame
				szStringPromoFrame = szString+"PromoFrame"
				screen.show( szStringPromoFrame )

		x = self.getX( nCol )
		y = self.getY( nRow )

		if (bEnable and self.bShowUpgradeIndicator):
			# can unit be upgraded ?
			if (mt.checkAnyUpgrade(pLoopUnit)):
				# place the upgrade arrow
				szStringUpgrade = szString+"Upgrade"
				szFileNameUpgrade = ArtFileMgr.getInterfaceArtInfo("OVERLAY_UPGRADE").getPath()	
				screen.addDDSGFC( szStringUpgrade, szFileNameUpgrade, x+2, y+14, 8, 16, WidgetTypes.WIDGET_GENERAL, iCount, -1 )
				screen.show( szStringUpgrade )

		if (self.bShowHealthBar and pLoopUnit.maxHitPoints() and not (pLoopUnit.isFighting() and self.bHideHealthBarWhileFighting)):
			# place the health bar
			szStringHealthBar = szString+"HealthBar"
			screen.setBarPercentage( szStringHealthBar, InfoBarTypes.INFOBAR_STORED, float( pLoopUnit.currHitPoints() ) / float( pLoopUnit.maxHitPoints() ) )
			screen.setBarPercentage( szStringHealthBar, InfoBarTypes.INFOBAR_RATE, float(1.0) )

			# EF: Colors are set by user instead
			#if (pLoopUnit.getDamage() >= ((pLoopUnit.maxHitPoints() * 2) / 3)):
			#	screen.setStackedBarColors(szStringHealthBar, InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_RED"))
			#elif (pLoopUnit.getDamage() >= (pLoopUnit.maxHitPoints() / 3)):
			#	screen.setStackedBarColors(szStringHealthBar, InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_YELLOW"))
			#else:
			#	screen.setStackedBarColors(szStringHealthBar, InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_GREEN"))	
													
			screen.show( szStringHealthBar )

		if (bEnable and self.bShowMoveBar):
			# place the move bar
			szStringMoveBar = szString+"MoveBar"
			if (pLoopUnit.movesLeft() == 0 or pLoopUnit.baseMoves() == 0):
				screen.setBarPercentage( szStringMoveBar, InfoBarTypes.INFOBAR_STORED, 0.0 )
				screen.setBarPercentage( szStringMoveBar, InfoBarTypes.INFOBAR_RATE, 0.0 )
				screen.setBarPercentage( szStringMoveBar, InfoBarTypes.INFOBAR_EMPTY, 1.0 )
			else:
				fMaxMoves = float(pLoopUnit.baseMoves())
				#fCurrMoves = fMaxMoves - (pLoopUnit.getMoves() / float(gc.getMOVE_DENOMINATOR())) 
				fCurrMoves = float(pLoopUnit.movesLeft()) / float(gc.getMOVE_DENOMINATOR()) 
				# mt.debug("c/m/r:%f/%f/%f"%(fCurrMoves, fMaxMoves, float( fCurrMoves ) / float( fMaxMoves ) ))
				if (fMaxMoves):
					screen.setBarPercentage( szStringMoveBar, InfoBarTypes.INFOBAR_STORED, fCurrMoves / fMaxMoves )
				else:
					screen.setBarPercentage( szStringMoveBar, InfoBarTypes.INFOBAR_STORED, 1.0 )
				screen.setBarPercentage( szStringMoveBar, InfoBarTypes.INFOBAR_RATE, 1.0 )
				screen.setBarPercentage( szStringMoveBar, InfoBarTypes.INFOBAR_EMPTY, 1.0 )
			screen.show( szStringMoveBar )
		
		# display the mission or activity info
		if (self.bShowMissionInfo): 
			
			# place the activity info below the unit icon.
			szFileNameAction = ""						
			eActivityType = pLoopUnit.getGroup().getActivityType()
			eAutomationType = pLoopUnit.getGroup().getAutomateType()
			
			# is unit on air intercept mission
			if (eActivityType == ActivityTypes.ACTIVITY_INTERCEPT):
				szFileNameAction = ArtFileMgr.getInterfaceArtInfo("OVERLAY_ACTION_INTERCEPT").getPath()
			# is unit on boat patrol coast mission
			elif (eActivityType == ActivityTypes.ACTIVITY_PATROL):
				szFileNameAction = ArtFileMgr.getInterfaceArtInfo("OVERLAY_ACTION_PATROL").getPath()
			# is unit on boat blockade mission
			elif (eActivityType == ActivityTypes.ACTIVITY_PLUNDER):
				szFileNameAction = ArtFileMgr.getInterfaceArtInfo("OVERLAY_ACTION_PLUNDER").getPath()
			# is unit fortified for healing (wake up when healed)
			elif (eActivityType == ActivityTypes.ACTIVITY_HEAL):
				szFileNameAction = ArtFileMgr.getInterfaceArtInfo("OVERLAY_ACTION_HEAL").getPath()
			# is unit sentry (wake up when enemy in sight)
			elif (eActivityType == ActivityTypes.ACTIVITY_SENTRY):
				szFileNameAction = ArtFileMgr.getInterfaceArtInfo("OVERLAY_ACTION_SENTRY").getPath()
			# is the turn for this unit skipped (wake up next turn)
			elif (eActivityType == ActivityTypes.ACTIVITY_HOLD):
				szFileNameAction = ArtFileMgr.getInterfaceArtInfo("OVERLAY_ACTION_SKIP").getPath()
			# has unit exploration mission
			elif (eAutomationType == AutomateTypes.AUTOMATE_EXPLORE):
				szFileNameAction = ArtFileMgr.getInterfaceArtInfo("OVERLAY_ACTION_EXPLORE").getPath()
			# is unit automated generally (only worker units)
			elif (eAutomationType == AutomateTypes.AUTOMATE_BUILD):
				szFileNameAction = ArtFileMgr.getInterfaceArtInfo("OVERLAY_ACTION_AUTO_BUILD").getPath()
			# is unit automated for nearest city (only worker units)
			elif (eAutomationType == AutomateTypes.AUTOMATE_CITY):
				szFileNameAction = ArtFileMgr.getInterfaceArtInfo("OVERLAY_ACTION_AUTO_CITY").getPath()
			# is unit automated for network (only worker units)
			elif (eAutomationType == AutomateTypes.AUTOMATE_NETWORK):
				szFileNameAction = ArtFileMgr.getInterfaceArtInfo("OVERLAY_ACTION_AUTO_NETWORK").getPath()
			# is unit automated spread religion (only missionary units)
			elif (eAutomationType == AutomateTypes.AUTOMATE_RELIGION):
				szFileNameAction = ArtFileMgr.getInterfaceArtInfo("OVERLAY_ACTION_AUTO_RELIGION").getPath()
			# has unit a mission
			elif (pLoopUnit.getGroup().getLengthMissionQueue() > 0):
				# is the mission a "move to" mission
				eMissionType = pLoopUnit.getGroup().getMissionType(0)
				if ( (eMissionType == MissionTypes.MISSION_MOVE_TO) or \
					 (eMissionType == MissionTypes.MISSION_MOVE_TO_UNIT) ):
					szFileNameAction = ArtFileMgr.getInterfaceArtInfo("OVERLAY_ACTION_GOTO").getPath()
			# if nothing of above, but unit is waiting -> unit is fortified
			elif (pLoopUnit.isWaiting()):
				if (pLoopUnit.isFortifyable()):
					szFileNameAction = ArtFileMgr.getInterfaceArtInfo("OVERLAY_ACTION_FORTIFY").getPath()
				else:
					szFileNameAction = ArtFileMgr.getInterfaceArtInfo("OVERLAY_ACTION_SLEEP").getPath()
						
			# display the mission icon
			if (szFileNameAction != ""):
				szStringActionIcon = szString+"ActionIcon"
				screen.addDDSGFC( szStringActionIcon, szFileNameAction, x+20, y+20, 16, 16, WidgetTypes.WIDGET_GENERAL, iCount, -1 )
				screen.show( szStringActionIcon )
			
		# display the colored spot icon
		szStringIcon = szString+"Icon"
		screen.addDDSGFC( szStringIcon, szFileNameState, x-3+xOffset, y-7+yOffset, xSize, ySize, WidgetTypes.WIDGET_GENERAL, iCount, -1 )
		screen.show( szStringIcon )
	
	# checks if the unit matches actual filter conditions
	def checkDisplayFilter(self, pUnit):

		# in case of Promotion or Upgrade Display 
		if (self.nPLEGrpMode == self.PLE_GRP_PROMO):
			# if unit is not promotion ready -> return
			if not pUnit.isPromotionReady():
				return False
		elif (self.nPLEGrpMode == self.PLE_GRP_UPGRADE):
			# if unit is not upgrade ready -> return
			if not mt.checkAnyUpgrade(pUnit):
				return False
		elif pUnit.isCargo():
			# in case the unit is a cargo unit, the decision is made by the tranporting unit. 
			# that ensures, that cargo is always displayed or not displayed together with its tranporting unit
			return self.checkDisplayFilter(pUnit.getTransportUnit())
		
		if (self.isPLEFilter(self.nPLEAllFilters)):
			# At least one filter is active
			if (BugPle.isPleFilterBehavior()):
				# unit can move and filter active
				if (self.isPLEFilter(self.nPLEFilterModeCanMove)):
					if (pUnit.movesLeft()):
						return False
				# unit cannot move and filter active
				if (self.isPLEFilter(self.nPLEFilterModeCantMove)):
					if (not pUnit.movesLeft()):
						return False
				
				# unit not wounded and filter active
				if (self.isPLEFilter(self.nPLEFilterModeNotWound)):
					if (not pUnit.isHurt()):
						return False
				# unit wounded and filter active
				if (self.isPLEFilter(self.nPLEFilterModeWound)):
					if (pUnit.isHurt()):
						return False
				
				pUnitTypeInfo = gc.getUnitInfo(pUnit.getUnitType())
				# is unit a land unit (or ICBM) and filter active
				if (self.isPLEFilter(self.nPLEFilterModeLand)):
					if (pUnitTypeInfo.getDomainType() == DomainTypes.DOMAIN_LAND) or (pUnitTypeInfo.getDomainType() == DomainTypes.DOMAIN_IMMOBILE):
						return False
				# is unit a sea unit and filter active
				if (self.isPLEFilter(self.nPLEFilterModeSea)):
					if (pUnitTypeInfo.getDomainType() == DomainTypes.DOMAIN_SEA):
						return False
				# is unit a air unit and filter active
				if (self.isPLEFilter(self.nPLEFilterModeAir)):
					if (pUnitTypeInfo.getDomainType() == DomainTypes.DOMAIN_AIR):
						return False
				
				# is unit a combat unit and filter active (combat means -> Combat or AirCombat values > 0!
				if (self.isPLEFilter(self.nPLEFilterModeMil)):
					if ((pUnitTypeInfo.getCombat() > 0) or (pUnitTypeInfo.getAirCombat() > 0)):
						return False
				# is unit a domestic unit and filter active (domestic means -> no Combat or AirCombat values!
				if (self.isPLEFilter(self.nPLEFilterModeDom)):
					if ((pUnitTypeInfo.getCombat() == 0) and (pUnitTypeInfo.getAirCombat() == 0)):
						return False
				
				# is the units owner the active player
				if (self.isPLEFilter(self.nPLEFilterModeOwn)):
					if ( pUnit.getOwner() == gc.getGame().getActivePlayer() ):
						return False
				# # is the units owner another player
				if (self.isPLEFilter(self.nPLEFilterModeForeign)):
					if ( not ( pUnit.getOwner() == gc.getGame().getActivePlayer() )):
						return False
			else:
				# BUG Filter Mode
				if (self.isPLEFilter(self.nPLEFilterModeCanMove)):
					if (not pUnit.movesLeft()):
						return False
				elif (self.isPLEFilter(self.nPLEFilterModeCantMove)):
					if (pUnit.movesLeft()):
						return False
				
				if (self.isPLEFilter(self.nPLEFilterModeNotWound)):
					if (pUnit.isHurt()):
						return False
				elif (self.isPLEFilter(self.nPLEFilterModeWound)):
					if (not pUnit.isHurt()):
						return False
				
				pUnitTypeInfo = gc.getUnitInfo(pUnit.getUnitType())
				if (self.isPLEFilter(self.nPLEFilterModeLand)):
					if (pUnitTypeInfo.getDomainType() != DomainTypes.DOMAIN_LAND) and (gc.getUnitInfo(pUnit.getUnitType()).getDomainType() != DomainTypes.DOMAIN_IMMOBILE):
						return False
				elif (self.isPLEFilter(self.nPLEFilterModeSea)):
					if (pUnitTypeInfo.getDomainType() != DomainTypes.DOMAIN_SEA):
						return False
				elif (self.isPLEFilter(self.nPLEFilterModeAir)):
					if (pUnitTypeInfo.getDomainType() != DomainTypes.DOMAIN_AIR):
						return False
				
				if (self.isPLEFilter(self.nPLEFilterModeMil)):
					if ((pUnitTypeInfo.getCombat() == 0) and (pUnitTypeInfo.getAirCombat() == 0)):
						return False
				elif (self.isPLEFilter(self.nPLEFilterModeDom)):
					if ((pUnitTypeInfo.getCombat() > 0) or (pUnitTypeInfo.getAirCombat() > 0)):
						return False
				
				if (self.isPLEFilter(self.nPLEFilterModeOwn)):
					if ( pUnit.getOwner() != gc.getGame().getActivePlayer() ):
						return False
				elif (self.isPLEFilter(self.nPLEFilterModeForeign)):
					if ( pUnit.getOwner() == gc.getGame().getActivePlayer() ):
						return False
		
		return True
		
	# create an info set for each unit. This set is used to determine the order of the plot list buttons.
	def getPLEUnitInfo(self, pUnit):
		if pUnit.isCargo() and (self.nPLEGrpMode != self.PLE_GRP_PROMO) and (self.nPLEGrpMode != self.PLE_GRP_UPGRADE):
			# if unit is cargo, we do retrieve the transport units characteristics to insert the cargo unit behind the transport unit in the sort list.
			pTransportUnit = pUnit.getTransportUnit()
			setUnit = self.getPLEUnitInfo(pTransportUnit)
			tReturn = (setUnit[self.IDX_PLAYER], setUnit[self.IDX_DOMAIN], setUnit[self.IDX_GROUPID], setUnit[self.IDX_COMBAT], setUnit[self.IDX_UNITTYPE], setUnit[self.IDX_LEVEL], setUnit[self.IDX_XP], pTransportUnit.getID(), pUnit.getID(), pUnit.getID(), pUnit)
			return tReturn
		else:
			# retrieve player info
			iPlayer = pUnit.getOwner()
			# get gproup id of the unit. only when display mode = group
			if (self.nPLEGrpMode == self.PLE_GRP_GROUPS):
				if (pUnit.getGroup().getNumUnits() > 1):
					iGroupID = pUnit.getGroupID()
				else:
					iGroupID = 0
			else:
				iGroupID = 0
			# retrieve domain info
			pUnitTypeInfo = gc.getUnitInfo(pUnit.getUnitType())
			eDomainType = pUnitTypeInfo.getDomainType()
			# retrieve combat strength :
			# - baseCombat is only set for ground units
			# - airBaseCombat is set used for ait units
			# - bombardRate is only set for Artillery 
			# - bombRate is only set for Bombers
			# the following calculation makes artillery/bombers listed before tanks/fighters
			iCombatStr = pUnit.baseCombatStr() + 100 * pUnit.bombardRate() + pUnit.airBaseCombatStr() + 100 * pUnitTypeInfo.getBombRate()
			# retrieve Unit type info
			eUnitType = pUnit.getUnitType()
			# retrieve unit level
			iLevel = pUnit.getLevel()
			# retrieve unit experience
			iXP = pUnit.getExperience()	
			# if unit has cargo...
			if pUnit.cargoSpace() > 0:
				iTransportUnit = pUnit.getID()
			else:
				iTransportUnit = 0
			# in case of promotion view, do not consider combat strngth, unit level and unit experience. Otherise the sorting will change during promotion process
			if (self.nPLEGrpMode == self.PLE_GRP_PROMO):
				# return negatives for some elements for descending sorting of related column.			
				tReturn = (iPlayer, eDomainType, -iGroupID, 0, -eUnitType, 0, 0, iTransportUnit, 0, pUnit.getID(), pUnit)
			else:
				# return negatives for some elements for descending sorting of related column.			
				tReturn = (iPlayer, eDomainType, -iGroupID, -iCombatStr, -eUnitType, -iLevel, -iXP, iTransportUnit, 0, pUnit.getID(), pUnit)
			return tReturn
			
	# creates a sorted unit list of the plot depending on the current grouping
	def getUnitList(self, pPlot):
		# local list to store unit order
		self.lPLEUnitList = []
		# loop for all units on the actual plot
		for i in range(pPlot.getNumUnits()):
			# retrieve single unit
			pUnit = pPlot.getUnit(i)
			# only units which are visible for the player 
			if not pUnit.isInvisible(gc.getPlayer(gc.getGame().getActivePlayer()).getTeam(), true):
				# check if the unit is loaded into any tranporter
				# append empty list element. Each element stores the following information in given order :
				lUnitInfo = self.getPLEUnitInfo(pUnit)
				self.lPLEUnitList.append( lUnitInfo )
				self.dPLEUnitInfo[ pUnit.getID() ] = lUnitInfo
		# sort list
		self.lPLEUnitList.sort()			
		
	# replaces the buggy civ 4 version.
	def getInterfacePlotUnit(self, i):
		return self.lPLEUnitList[i][self.IDX_UNIT]
	
	# displays all the possible promotion buttons for a unit 
	def displayUnitPromos(self, screen, pUnit, nRow, nCol):
		lPromos = mt.getPossiblePromos(pUnit)
		# remove the 'Lead by Warlord' promotion, if any
		for i in range(len(lPromos)):
			if (gc.getPromotionInfo(lPromos[i]).getType() == 'PROMOTION_LEADER'):
				lPromos.pop(i)
				break
		# determine which dimension is the unit and which the promotion
		if (self.sPLEMode == self.PLE_MODE_STACK_HORIZ):
			iU = nRow
		else:
			iU = nCol
		# display the promotions
		for i in range(len(lPromos)):
			if (self.sPLEMode == self.PLE_MODE_STACK_HORIZ):
				nCol += 1
			else:
				nRow += 1
			x = self.getX( nCol )
			y = self.getY( nRow )
			if (self.sPLEMode == self.PLE_MODE_STACK_HORIZ):
				iP = nCol
			else:
				iP = nRow
			iPromo = lPromos[i]
			sID = string.zfill(str(iU), 2) + string.zfill(str(iP), 2)
			szStringUnitPromo = self.PLOT_LIST_PROMO_NAME + sID
			szFileNamePromo = gc.getPromotionInfo(iPromo).getButton()
			screen.setImageButton( szStringUnitPromo, szFileNamePromo, x, y, 32, 32, WidgetTypes.WIDGET_GENERAL, gc.getPromotionInfo(iPromo).getActionInfoIndex(), -1 )
			screen.show( szStringUnitPromo )
		self.dUnitPromoList[iU] = lPromos
		return

	# performs the units promotion
	def doPromotion(self, id):
		idPromo		= id % 100
		idUnit		= id / 100
		pUnit 		= self.listPLEButtons[idUnit][0]
		iPromo		= self.dUnitPromoList[idUnit][idPromo-1]
		pUnit.promote(iPromo, -1)
		
		
	# displays all the possible upgrade buttons for a unit 
	def displayUnitUpgrades(self, screen, pUnit, nRow, nCol):
		lUpgrades 	= []
		lUnits		= []
		
		# reading all upgrades
		lUpgrades = mt.getPossibleUpgrades(pUnit)
		
		# determine which dimension is the unit and which the upgrade
		if (self.sPLEMode == self.PLE_MODE_STACK_HORIZ):
			iU = nRow
		else:
			iU = nCol
		
		# displaying the results
		for i in range(len(lUpgrades)):
			if (self.sPLEMode == self.PLE_MODE_STACK_HORIZ):
				nCol += 1
			else:
				nRow += 1
			x = self.getX( nCol )
			y = self.getY( nRow )
			if (self.sPLEMode == self.PLE_MODE_STACK_HORIZ):
				iP = nCol
			else:
				iP = nRow
			iUnitIndex = lUpgrades[i]
			lUnits.append(iUnitIndex)
			sID = string.zfill(str(iU), 2) + string.zfill(str(iP), 2)
			szStringUnitUpgrade = self.PLOT_LIST_UPGRADE_NAME + sID
			szFileNameUpgrade = gc.getUnitInfo(iUnitIndex).getButton()
			screen.setImageButton( szStringUnitUpgrade, szFileNameUpgrade, x, y, 34, 34, WidgetTypes.WIDGET_GENERAL, iUnitIndex, -1 )
			if pUnit.canUpgrade(iUnitIndex, false):
				screen.enable(szStringUnitUpgrade, true)
			else:
				screen.enable(szStringUnitUpgrade, false)
			screen.show( szStringUnitUpgrade )
		self.dUnitUpgradeList[iU] = lUnits
		return
			
	# performs the unit upgrades
	def doUpgrade(self, id):
		idUpgrade		= id % 100
		idUnit			= id / 100
		pUnit 			= self.listPLEButtons[idUnit][0]
		iUnitType		= self.dUnitUpgradeList[idUnit][idUpgrade-1]		
		if mt.bCtrl():
			pPlot = pUnit.plot()
			iCompUnitType = pUnit.getUnitType()
			for i in range(pPlot.getNumUnits()):
				pLoopUnit = pPlot.getUnit(i)
				if (pLoopUnit.getUnitType() == iCompUnitType):
					pLoopUnit.doCommand(CommandTypes.COMMAND_UPGRADE, iUnitType, 0)
		elif mt.bAlt():
			pActPlayer = gc.getActivePlayer()
			iCompUnitType = pUnit.getUnitType()
			for i in range(pActPlayer.getNumUnits()):
				pLoopUnit = pActPlayer.getUnit(i)
				if (pLoopUnit.getUnitType() == iCompUnitType):
					pLoopUnit.doCommand(CommandTypes.COMMAND_UPGRADE, iUnitType, 0)
		else:
			pUnit.doCommand(CommandTypes.COMMAND_UPGRADE, iUnitType, 0)		

##################### info pane (mouse over) functions ########################
		
	# handles display of the promotion button info pane
	def showPromoInfoPane(self, id):
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		idPromo		= id % 100
		idUnit		= id / 100
		pUnit 		= self.listPLEButtons[idUnit][0]
		iPromo		= self.dUnitPromoList[idUnit][idPromo-1]
		
		# promo info
		szPromoInfo = u"<font=2>" + mt.removeLinks(CyGameTextMgr().getPromotionHelp(iPromo, false)) + u"</font>\n"
		
		# unit level 
		iLevel = pUnit.getLevel()
		iMaxLevel = mt.GetPossiblePromotions(pUnit.experienceNeeded(), pUnit.getExperience())
		if iMaxLevel <> iLevel:
			# actual / available (= number of possible promotions)
			szLevel = u"<font=2>" + localText.getText("INTERFACE_PANE_LEVEL", ()) + u"%i / %i" % (iLevel, (iMaxLevel+iLevel)) + u"</font>\n"
		else:
			# actual 
			szLevel = u"<font=2>" + localText.getText("INTERFACE_PANE_LEVEL", ()) + u"%i" % iLevel + u"</font>\n"

		# unit experience (actual / needed)
		iExperience = pUnit.getExperience()
		if (iExperience > 0):
			szExperience = u"<font=2>" + localText.getText("INTERFACE_PANE_EXPERIENCE", ()) + u": %i / %i" %(iExperience, pUnit.experienceNeeded()) + u"</font>\n"
		else:
			szExperience = u""
			
		szText = szPromoInfo + szLevel + szExperience
			
		# display the info pane
		self.displayInfoPane(szText)
		
	def hidePromoInfoPane(self):
		self.hideInfoPane()

	# handles display of the promotion bottun info pane
	def showUpgradeInfoPane(self, id):
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		idUpgrade		= id % 100
		idUnit			= id / 100
		pUnit 			= self.listPLEButtons[idUnit][0]
		iUnitType		= self.dUnitUpgradeList[idUnit][idUpgrade-1]		
		pUnitTypeInfo 	= gc.getUnitInfo(iUnitType)		
		
		# reading attributes
		szUnitName 		= localText.changeTextColor(pUnitTypeInfo.getDescription(), gc.getInfoTypeForString(BugPle.getUnitNameColor())) + u"\n"
		if pUnitTypeInfo.getUnitCombatType() != -1:
			szCombatType	= gc.getUnitCombatInfo(pUnitTypeInfo.getUnitCombatType()).getDescription() + u"\n"
		else:
			szCombatType = u""
		if (pUnitTypeInfo.getAirCombat() > 0):
			iStrength = pUnitTypeInfo.getAirCombat()
		else:
			iStrength = pUnitTypeInfo.getCombat()
		szStrength = u"%i "%iStrength + u"%c" % CyGame().getSymbolID( FontSymbols.STRENGTH_CHAR )
		szMovement = u", %i "%pUnitTypeInfo.getMoves()+ u"%c" % CyGame().getSymbolID(FontSymbols.MOVES_CHAR)
		if (pUnitTypeInfo.getAirRange() > 0):
			szRange = u", " + localText.getText("TXT_KEY_UNIT_AIR_RANGE", ( pUnitTypeInfo.getAirRange(), ) ) + u"\n"
		else:
			szRange = u"\n"
		szSpecialText = mt.removeLinks(CyGameTextMgr().getUnitHelp( iUnitType, True, False, False, None )[1:]) + "\n"
			
		# determining the unit upgrade price
		iUpgradePriceSingle 	= mt.getUpgradePrice(pUnit, iUnitType, 0)
#		iUpgradePriceGrp 		= mt.getUpgradePrice(pUnit, iUnitType, 1)
		iUpgradePricePlot 		= mt.getUpgradePrice(pUnit, iUnitType, 2)
		iUpgradePriceAll 		= mt.getUpgradePrice(pUnit, iUnitType, 3)
		
		iGold = gc.getActivePlayer().getGold()	
		if iUpgradePriceSingle > iGold:
			szUpgradePriceSingle = localText.changeTextColor(u"%i"%iUpgradePriceSingle, gc.getInfoTypeForString(BugPle.getUpgradeNotPossibleColor()))
		else:
			szUpgradePriceSingle = localText.changeTextColor(u"%i"%iUpgradePriceSingle, gc.getInfoTypeForString(BugPle.getUpgradePossibleColor()))
		if iUpgradePricePlot > iGold:
			szUpgradePricePlot = localText.changeTextColor(u"%i"%iUpgradePricePlot, gc.getInfoTypeForString(BugPle.getUpgradeNotPossibleColor()))
		else:
			szUpgradePricePlot = localText.changeTextColor(u"%i"%iUpgradePricePlot, gc.getInfoTypeForString(BugPle.getUpgradePossibleColor()))
		if iUpgradePriceAll > iGold:
			szUpgradePriceAll = localText.changeTextColor(u"%i"%iUpgradePriceAll, gc.getInfoTypeForString(BugPle.getUpgradeNotPossibleColor()))
		else:
			szUpgradePriceAll = localText.changeTextColor(u"%i"%iUpgradePriceAll, gc.getInfoTypeForString(BugPle.getUpgradePossibleColor()))
		
		szUpgradePrice = szUpgradePriceSingle + u" / " + szUpgradePricePlot + u" / " + szUpgradePriceAll+ u" %c" %  gc.getYieldInfo(YieldTypes.YIELD_COMMERCE).getChar() + u"\n"
		
		szUpgradeHelp = localText.getText("TXT_KEY_PLE_UPGRADE_HELP", () )		

		szText 		= u"<font=2>" + szUnitName + \
						szCombatType  + \
						szStrength  + \
						szMovement + \
						szRange  + \
						szSpecialText + \
						szUpgradePrice + \
						szUpgradeHelp + \
					u"</font>"
					
		# display the info pane
		self.displayInfoPane(szText)
				
	def hideUpgradeInfoPane(self):
		self.hideInfoPane()
				
	# handles the display of the unit's info pane
	def showUnitInfoPane(self, id):
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )

		pUnit 			= self.listPLEButtons[id][0]
		iUnitType 		= pUnit.getUnitType()
		pUnitTypeInfo 	= gc.getUnitInfo(iUnitType)
		eUnitDomain 	= pUnitTypeInfo.getDomainType()
	
		#mt.debug("id:%i; iUnit:%i"%(id, iUnit))
		
		# get units owner name if its not a player unit
		if (pUnit.getOwner() != gc.getGame().getActivePlayer()):
			pOwner = gc.getPlayer(pUnit.getOwner())
			szOwner = u"<font=2> [" + localText.changeTextColor(pOwner.getName(), pOwner.getPlayerColor()) + u"]</font>"
		else:
			szOwner = u""
				
		# unit type description + unit name (if given)
		szUnitName = u"<font=2>" + localText.changeTextColor(pUnit.getName(), gc.getInfoTypeForString(BugPle.getUnitNameColor())) + szOwner + u"</font>\n"
			
		# strength 
		if (eUnitDomain == DomainTypes.DOMAIN_AIR):
			fCurrStrength 	= float(pUnit.airCurrCombatStr()*0.01)
			fMaxStrength 	= float(pUnit.airMaxCombatStr()*0.01)
		else:
			fCurrStrength 	= float(pUnit.baseCombatStr())*float(1.0-pUnit.getDamage()*0.01)
			fMaxStrength 	= float(pUnit.baseCombatStr())
		if fCurrStrength != fMaxStrength:
			if float(fMaxStrength*float(mt.getPlotHealFactor(pUnit))*0.01) == 0:
				iTurnsToHeal = 999
			else:
				iTurnsToHeal 		= int((fMaxStrength-fCurrStrength)/float(fMaxStrength*float(mt.getPlotHealFactor(pUnit))*0.01)+0.999) # force to round upwards
			szCurrStrength 		= u" %.1f" % fCurrStrength
			szMaxStrength 		= u" / %i" % fMaxStrength
			if mt.getPlotHealFactor(pUnit) != 0:
				szTurnsToHeal 		= u" (%i)" % iTurnsToHeal
			else:
				szTurnsToHeal = u" (Not Healing)"
		else: 
			iTurnsToHeal 		= 0
			szCurrStrength 		= u" %i" % fCurrStrength
			szMaxStrength 		= u""		
			szTurnsToHeal 		= u""
		szStrength = u"<font=2>" + szCurrStrength + szMaxStrength + szTurnsToHeal + u"%c" % CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR) + u"</font>\n" 
			
		# movement
		fMaxMoves = float(pUnit.baseMoves())
		fCurrMoves = (float(fMaxMoves)-float(pUnit.getMoves()/60.0))
		if (eUnitDomain == DomainTypes.DOMAIN_AIR):
			szAirRange 		= u", " + localText.getText("TXT_KEY_UNIT_AIR_RANGE", ( pUnit.airRange(), ) ) 
		else:
			szAirRange 		= u""
		if fCurrMoves != 0:
			szCurrMoves = u" %.1f" % fCurrMoves
			szMaxMoves 	= u" / %i" % fMaxMoves
		else:
			szCurrMoves = u" %i" % fMaxMoves
			szMaxMoves 	= u""
		szMovement = u"<font=2>" + szCurrMoves + szMaxMoves + u"%c"%(CyGame().getSymbolID(FontSymbols.MOVES_CHAR)) + szAirRange + u"</font>\n"

		# compressed display for standard display
		szStrengthMovement = u"<font=2>" + szCurrStrength + szMaxStrength + szTurnsToHeal + u"%c" % CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR) + ", " + \
							szCurrMoves + szMaxMoves + u"%c"%(CyGame().getSymbolID(FontSymbols.MOVES_CHAR)) + szAirRange + u"</font>\n"
							
		# civilization type
		szCiv = u""
#		iCiv = pUnit.getCivilizationType()
#		for i in range(gc.getMAX_PLAYERS()):
#			pLoopPlayer = gc.getPlayer(i)
#			if pLoopPlayer.getCivilizationType() == iCiv:
#				break
#		szCiv = u"<font=2>100% " + localText.changeTextColor(pLoopPlayer.getCivilizationAdjective(0), pLoopPlayer.getPlayerColor()) + u"</font>\n"
	
		# unit level
		iLevel = pUnit.getLevel()
		iMaxLevel = mt.GetPossiblePromotions(pUnit.experienceNeeded(), pUnit.getExperience())
		if (iMaxLevel > 0) or (iLevel > 1):
			if iMaxLevel <> iLevel:
				szLevel = u"<font=2>" + localText.getText("INTERFACE_PANE_LEVEL", ()) + u" %i / %i" % (iLevel, (iMaxLevel+iLevel)) + u"</font>\n"
			else:
				szLevel = u"<font=2>" + localText.getText("INTERFACE_PANE_LEVEL", ()) + u" %i" % iLevel + u"</font>\n"
		else:
			szLevel = u""

		# unit experience (actual / needed (possible promos))
		iExperience = pUnit.getExperience()
		if (iExperience > 0):
			szExperience = u"<font=2>" + localText.getText("INTERFACE_PANE_EXPERIENCE", ()) + u": %i / %i" %(iExperience, pUnit.experienceNeeded()) + u"</font>\n"
		else:
			szExperience = u""

		# cargo space
		iCargoSpace = pUnit.cargoSpace()
		if iCargoSpace > 0:
			iCargo = pUnit.getCargo()
			szCargo = u"<font=2>" + localText.getText("TXT_KEY_UNIT_HELP_CARGO_SPACE", (iCargo, iCargoSpace ) ) + u"</font>\n"
		else:
			szCargo = u""
				
		# fortify bonus
		szFortifyBonus = u"" 
		iFortifyBonus = pUnit.fortifyModifier()
		if iFortifyBonus > 0:
			szFortifyBonus = u"<font=2>" + localText.getText("TXT_KEY_UNIT_HELP_FORTIFY_BONUS", (iFortifyBonus, )) + u"\n" + u"</font>"
	
		# unit type specialities 
		szSpecialText 	= u"<font=2>" + localText.getText("TXT_KEY_PEDIA_SPECIAL_ABILITIES", ()) + u":\n" + CyGameTextMgr().getUnitHelp( iUnitType, true, false, false, None )[1:] + u"</font>"
		szSpecialText = localText.changeTextColor(szSpecialText, gc.getInfoTypeForString(BugPle.getUnitTypeSpecialtiesColor()))
		
		if iLevel > 1:
			szSpecialText += "\n" + localText.changeTextColor(mt.getPromotionInfoText(pUnit), gc.getInfoTypeForString(BugPle.getPromotionSpecialtiesColor()))
		szSpecialText = mt.removeLinks(szSpecialText)

		# count the promotions
		szPromotion = u""
		iPromotionCount = 0
		for i in range(gc.getNumPromotionInfos()):
			if pUnit.isHasPromotion(i):
				iPromotionCount += 1
		if iPromotionCount > 0:
			szPromotion = u"\n"*((iPromotionCount/self.CFG_INFOPANE_BUTTON_PER_LINE)+1)

		# build text
		szText 	= szUnitName + \
				szPromotion + \
				szStrengthMovement + \
				szLevel + \
				szExperience + \
				szCargo + \
				szCiv + \
				szFortifyBonus + \
				szSpecialText

		# display the info pane
		dy = self.displayInfoPane(szText)
					
		# show promotion buttons
		iTemp = 0
		for i in range(gc.getNumPromotionInfos()):
			if pUnit.isHasPromotion(i):
				szName = self.PLE_PROMO_BUTTONS_UNITINFO + str(i)
				self.displayUnitInfoPromoButtonPos( szName, iTemp, dy-1*self.CFG_INFOPANE_PIX_PER_LINE_1 )
				screen.show( szName )
				iTemp += 1
							
	def hideUnitInfoPane(self):
		self.hideUnitInfoPromoButtons()
		self.hideInfoPane()
		
	def hideUnitInfoPromoButtons(self):
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		for i in range(gc.getNumPromotionInfos()):
			szName = self.PLE_PROMO_BUTTONS_UNITINFO + str(i)
			screen.hide( szName )
		self.bUnitPromoButtonsActive = false
	
	# displays the unit's promotion buttons in the info pane. They are not part of the info pane.
	def displayUnitInfoPromoButtonPos( self, szName, iPromotionCount, yOffset ):
		self.bUnitPromoButtonsActive = true
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		if ( CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW ):
			y = self.CFG_INFOPANE_Y
		else:
			y = self.CFG_INFOPANE_Y2
		screen.moveItem( szName, BugPle.getInfoPaneX() + 4 + (self.CFG_INFOPANE_BUTTON_SIZE * (iPromotionCount % self.CFG_INFOPANE_BUTTON_PER_LINE)), \
								 y + 4 - yOffset + (self.CFG_INFOPANE_BUTTON_SIZE * (iPromotionCount / self.CFG_INFOPANE_BUTTON_PER_LINE)), -0.3 )
		screen.moveToFront( szName )

	# calculates the height of a text in pixels
	def getTextLines(self, szText):
		szText = mt.removeFonts(szText)
		szText = mt.removeColor(szText)
		szText = mt.removeLinks(szText)
		iNormalLines = 0
		iBulletLines = 0
		lChapters = szText.split('\n')
		sComp = u"%c"%CyGame().getSymbolID(FontSymbols.BULLET_CHAR)
		for i in range(len(lChapters)):
			iLen = len(lChapters[i])
			iWidth = CyInterface().determineWidth(lChapters[i])/(self.CFG_INFOPANE_DX-3)+1
			if (lChapters[i].find(sComp) != -1):
				iBulletLines += iWidth
			else:
				iNormalLines += iWidth
		dy = iNormalLines*self.CFG_INFOPANE_PIX_PER_LINE_1 + (iBulletLines)*self.CFG_INFOPANE_PIX_PER_LINE_2 + 20
		return dy
		
	# base function to display a self sizing info pane
	def displayInfoPane(self, szText):

		self.bInfoPaneActive 	= True
		self.iInfoPaneCnt  		+= 1
		self.tLastMousePos 		= (CyInterface().getMousePos().x, CyInterface().getMousePos().y)

		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		
		# calculate text size
		dy = self.getTextLines(szText)
		
		# draw panel
		if ( CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW ):
			y = self.CFG_INFOPANE_Y
		else:
			y = self.CFG_INFOPANE_Y2
		screen.addPanel( self.UNIT_INFO_PANE, u"", u"", True, True, \
						BugPle.getInfoPaneX(), y - dy, self.CFG_INFOPANE_DX, dy, \
						PanelStyles.PANEL_STYLE_HUD_HELP )
		
		# create shadow text
		szTextBlack = localText.changeTextColor(mt.removeColor(szText), gc.getInfoTypeForString("COLOR_BLACK"))
		
		# display shadow text
		screen.addMultilineText( self.UNIT_INFO_TEXT_SHADOW, szTextBlack, \
								BugPle.getInfoPaneX() + 5, y - dy + 5, \
								self.CFG_INFOPANE_DX - 3, dy - 3, \
								WidgetTypes.WIDGET_GENERAL, -1, -1, \
								CvUtil.FONT_LEFT_JUSTIFY)
		# display text
		screen.addMultilineText( self.UNIT_INFO_TEXT, szText, \
								BugPle.getInfoPaneX() + 4, y - dy + 4, \
								self.CFG_INFOPANE_DX - 3, dy - 3, \
								WidgetTypes.WIDGET_GENERAL, -1, -1, \
								CvUtil.FONT_LEFT_JUSTIFY)
					
		return dy
	
	# hides the info pane
	def hideInfoPane(self):
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		screen.hide(self.UNIT_INFO_TEXT)
		screen.hide(self.UNIT_INFO_TEXT_SHADOW)
		screen.hide(self.UNIT_INFO_PANE)
		self.bInfoPaneActive = False
		self.iLastInfoPaneCnt = self.iInfoPaneCnt

#################### functions for a units move area #######################
		
	# highlights the move area
	def highlightMoves(self, id):
		if BugPle.isShowMoveHighlighter():
			pUnit = self.listPLEButtons[id][0]
			self.ASMA.highlightMoveArea(pUnit)

	# hides the move area
	def dehighlightMoves(self):
		if BugPle.isShowMoveHighlighter():
			self.ASMA.dehighlightMoveArea()
		
# BUG - PLE- end
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################

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
# BUG - PLE- begin
#		xResolution = screen.getXResolution()
#		yResolution = screen.getYResolution()
#		self.m_iNumPlotListButtons = (xResolution - (iMultiListXL+iMultiListXR) - 68) / 34
#		
#		screen.setDimensions(0, 0, xResolution, yResolution)

		self.pOldPlot = 0

		self.xResolution = screen.getXResolution()
		self.yResolution = screen.getYResolution()
		
		# this is only to prevent changing all variables in the code. 
		xResolution = self.xResolution
		yResolution = self.yResolution
		self.m_iNumPlotListButtons = (self.xResolution - (iMultiListXL+iMultiListXR) - 68) / 34
		screen.setDimensions(0, 0, self.xResolution, self.yResolution)
		
		self.CFG_INFOPANE_PIX_PER_LINE_1 			= 24
		self.CFG_INFOPANE_PIX_PER_LINE_2 			= 19
		self.CFG_INFOPANE_DX 					    = 290
		
		self.CFG_INFOPANE_Y		 			= yResolution - BugPle.getInfoPaneY()
		self.CFG_INFOPANE_BUTTON_SIZE		= self.CFG_INFOPANE_PIX_PER_LINE_1 - 2
		self.CFG_INFOPANE_BUTTON_PER_LINE	= self.CFG_INFOPANE_DX / self.CFG_INFOPANE_BUTTON_SIZE
		self.CFG_INFOPANE_Y2				= self.CFG_INFOPANE_Y + 105
				
# BUG - PLE- end

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

# BUG - 3.17 No Espionage - start
		if not BugUtil.isNoEspionage():
			iBtnX += iBtnAdvance
			screen.setImageButton( "EspionageAdvisorButton", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_ESPIONAGE_SCREEN).getActionInfoIndex(), -1 )
			screen.setStyle( "EspionageAdvisorButton", "Button_HUDAdvisorEspionage_Style" )
			screen.hide( "EspionageAdvisorButton" )
# BUG - 3.17 No Espionage - end
		
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

# BUG - PLE- begin
#		for j in range(gc.getMAX_PLOT_LIST_ROWS()):
#			yRow = (j - gc.getMAX_PLOT_LIST_ROWS() + 1) * 34
#			yPixel = yResolution - 169 + yRow - 3
#			xPixel = 315 - 3
#			xWidth = self.numPlotListButtons() * 34 + 3
#			yHeight = 32 + 3
#		
#			szStringPanel = "PlotListPanel" + str(j)
#			screen.addPanel(szStringPanel, u"", u"", True, False, xPixel, yPixel, xWidth, yHeight, PanelStyles.PANEL_STYLE_EMPTY)
#
#			for i in range(self.numPlotListButtons()):
#				k = j*self.numPlotListButtons()+i
#				
#				xOffset = i * 34
#				
#				szString = "PlotListButton" + str(k)
#				screen.addCheckBoxGFCAt(szStringPanel, szString, ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_GOVERNOR").getPath(), ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(), xOffset + 3, 3, 32, 32, WidgetTypes.WIDGET_PLOT_LIST, k, -1, ButtonStyles.BUTTON_STYLE_LABEL, True )
#				screen.hide( szString )
#				
#				szStringHealth = szString + "Health"
#				screen.addStackedBarGFCAt( szStringHealth, szStringPanel, xOffset + 3, 26, 32, 11, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_GENERAL, k, -1 )
#				screen.hide( szStringHealth )
#				
#				szStringIcon = szString + "Icon"
#				szFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_MOVE").getPath()
#				screen.addDDSGFCAt( szStringIcon, szStringPanel, szFileName, xOffset, 0, 12, 12, WidgetTypes.WIDGET_PLOT_LIST, k, -1, False )
#				screen.hide( szStringIcon )

		self.iMaxPlotListIcons = self.getMaxCol() * self.getMaxRow()
		szHealthyColor = BugPle.getHealthyColor()
		szWoundedColor = BugPle.getWoundedColor()
		szMovementColor = BugPle.getFullMovementColor()
		szHasMovedColor = BugPle.getHasMovedColor()
		szNoMovementColor = BugPle.getNoMovementColor()
		
		szFileNamePromo = ArtFileMgr.getInterfaceArtInfo("OVERLAY_PROMOTION_FRAME").getPath()
		szFileNameGovernor = ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_GOVERNOR").getPath()
		szFileNameHilite = ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath()
		for i in range( self.iMaxPlotListIcons ):		
			# create button name
			szString = self.PLOT_LIST_BUTTON_NAME + str(i)
				
			x = self.getX( self.getCol( i ) )
			y = self.getY( self.getRow( i ) )
			
			# place/init the promotion frame. Important to have it at first place within the for loop.
			szStringPromoFrame = szString + "PromoFrame"
			screen.addDDSGFC( szStringPromoFrame, szFileNamePromo, x, y, 32, 32, WidgetTypes.WIDGET_GENERAL, i, -1 )
			screen.hide( szStringPromoFrame )

			# place the plot list unit button
			screen.addCheckBoxGFC( szString, szFileNameGovernor, szFileNameHilite, x, y, 32, 32, WidgetTypes.WIDGET_GENERAL, i, -1, ButtonStyles.BUTTON_STYLE_LABEL )
			screen.hide( szString )
	
			# place/init the health bar. Important to have it at last place within the for loop.
			szStringHealthBar = szString + "HealthBar"
#			screen.addStackedBarGFC( szStringHealthBar, x+7, y-7, 25, 14, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			screen.addStackedBarGFC( szStringHealthBar, x+5, y-9, 29, 11, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_GENERAL, i, -1 )
			screen.setStackedBarColors( szStringHealthBar, InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString(szHealthyColor) )
			screen.setStackedBarColors( szStringHealthBar, InfoBarTypes.INFOBAR_RATE, gc.getInfoTypeForString(szWoundedColor) )
			screen.hide( szStringHealthBar )

			# place/init the movement bar. Important to have it at last place within the for loop.
			szStringMoveBar = szString + "MoveBar"
			screen.addStackedBarGFC( szStringMoveBar, x+5, y-5, 29, 11, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_GENERAL, i, -1 )
			screen.setStackedBarColors( szStringMoveBar, InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString(szMovementColor) )
			screen.setStackedBarColors( szStringMoveBar, InfoBarTypes.INFOBAR_RATE, gc.getInfoTypeForString(szHasMovedColor) )
			screen.setStackedBarColors( szStringMoveBar, InfoBarTypes.INFOBAR_EMPTY, gc.getInfoTypeForString(szNoMovementColor) )
			screen.hide( szStringMoveBar )

		self.preparePlotListObjects(screen)
# BUG - PLE - end


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

# BUG - city specialist - start
		screen.addPanel( "SpecialistBackground", u"", u"", True, False, xResolution - 243, yResolution - 423, 230, 30, PanelStyles.PANEL_STYLE_STANDARD )
		screen.setStyle( "SpecialistBackground", "Panel_City_Header_Style" )
		screen.hide( "SpecialistBackground" )
		screen.setLabel( "SpecialistLabel", "Background", "Specialists", CvUtil.FONT_CENTER_JUSTIFY, xResolution - 128, yResolution - 415, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.hide( "SpecialistLabel" )
# BUG - city specialist - end

		# **********************************************************
		# GAME DATA STRINGS
		# **********************************************************

		szGameDataList = []

		xCoord = 268 + (xResolution - 1024) / 2
		screen.addStackedBarGFC( "ResearchBar", xCoord, 2, 487, iStackBarHeight, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_RESEARCH, -1, -1 )
		screen.setStackedBarColors( "ResearchBar", InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_RESEARCH_STORED") )
		screen.setStackedBarColors( "ResearchBar", InfoBarTypes.INFOBAR_RATE, gc.getInfoTypeForString("COLOR_RESEARCH_RATE") )
		screen.setStackedBarColors( "ResearchBar", InfoBarTypes.INFOBAR_RATE_EXTRA, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.setStackedBarColors( "ResearchBar", InfoBarTypes.INFOBAR_EMPTY, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.hide( "ResearchBar" )

# BUG - Great General Bar - start
		screen.addStackedBarGFC( "GreatGeneralBar", xCoord, 27, 100, iStackBarHeight, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_HELP_GREAT_GENERAL, -1, -1 )
		screen.setStackedBarColors( "GreatGeneralBar", InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_NEGATIVE_RATE") ) #gc.getInfoTypeForString("COLOR_GREAT_PEOPLE_STORED") )
		screen.setStackedBarColors( "GreatGeneralBar", InfoBarTypes.INFOBAR_RATE, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.setStackedBarColors( "GreatGeneralBar", InfoBarTypes.INFOBAR_RATE_EXTRA, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.setStackedBarColors( "GreatGeneralBar", InfoBarTypes.INFOBAR_EMPTY, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.hide( "GreatGeneralBar" )
# BUG - Great General Bar - end

# BUG - Great Person Bar - start
		xCoord += 7 + 100
		screen.addStackedBarGFC( "GreatPersonBar", xCoord, 27, 380, iStackBarHeight, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.setStackedBarColors( "GreatPersonBar", InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_GREAT_PEOPLE_STORED") )
		screen.setStackedBarColors( "GreatPersonBar", InfoBarTypes.INFOBAR_RATE, gc.getInfoTypeForString("COLOR_GREAT_PEOPLE_RATE") )
		screen.setStackedBarColors( "GreatPersonBar", InfoBarTypes.INFOBAR_RATE_EXTRA, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.setStackedBarColors( "GreatPersonBar", InfoBarTypes.INFOBAR_EMPTY, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.hide( "GreatPersonBar" )
# BUG - Great Person Bar - end

# BUG - Bars on single line for higher resolution screens - start
		xCoord = 268 + (xResolution - 1440) / 2
		screen.addStackedBarGFC( "GreatGeneralBar-w", xCoord, 2, 84, iStackBarHeight, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_HELP_GREAT_GENERAL, -1, -1 )
		screen.setStackedBarColors( "GreatGeneralBar-w", InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_NEGATIVE_RATE") ) #gc.getInfoTypeForString("COLOR_GREAT_PEOPLE_STORED") )
		screen.setStackedBarColors( "GreatGeneralBar-w", InfoBarTypes.INFOBAR_RATE, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.setStackedBarColors( "GreatGeneralBar-w", InfoBarTypes.INFOBAR_RATE_EXTRA, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.setStackedBarColors( "GreatGeneralBar-w", InfoBarTypes.INFOBAR_EMPTY, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.hide( "GreatGeneralBar-w" )

		xCoord += 6 + 84
		screen.addStackedBarGFC( "ResearchBar-w", xCoord, 2, 487, iStackBarHeight, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_RESEARCH, -1, -1 )
		screen.setStackedBarColors( "ResearchBar-w", InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_RESEARCH_STORED") )
		screen.setStackedBarColors( "ResearchBar-w", InfoBarTypes.INFOBAR_RATE, gc.getInfoTypeForString("COLOR_RESEARCH_RATE") )
		screen.setStackedBarColors( "ResearchBar-w", InfoBarTypes.INFOBAR_RATE_EXTRA, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.setStackedBarColors( "ResearchBar-w", InfoBarTypes.INFOBAR_EMPTY, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.hide( "ResearchBar-w" )

		xCoord += 6 + 487
		screen.addStackedBarGFC( "GreatPersonBar-w", xCoord, 2, 320, iStackBarHeight, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.setStackedBarColors( "GreatPersonBar-w", InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_GREAT_PEOPLE_STORED") )
		screen.setStackedBarColors( "GreatPersonBar-w", InfoBarTypes.INFOBAR_RATE, gc.getInfoTypeForString("COLOR_GREAT_PEOPLE_RATE") )
		screen.setStackedBarColors( "GreatPersonBar-w", InfoBarTypes.INFOBAR_RATE_EXTRA, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.setStackedBarColors( "GreatPersonBar-w", InfoBarTypes.INFOBAR_EMPTY, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.hide( "GreatPersonBar-w" )
# BUG - Bars on single line for higher resolution screens - end

		
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

# BUG - PLE- begin
#		screen.setButtonGFC( "PlotListMinus", u"", "", 315 + ( xResolution - (iMultiListXL+iMultiListXR) - 68 ), yResolution - 171, 32, 32, WidgetTypes.WIDGET_PLOT_LIST_SHIFT, -1, -1, ButtonStyles.BUTTON_STYLE_ARROW_LEFT )
#		screen.hide( "PlotListMinus" )
#
#		screen.setButtonGFC( "PlotListPlus", u"", "", 298 + ( xResolution - (iMultiListXL+iMultiListXR) - 34 ), yResolution - 171, 32, 32, WidgetTypes.WIDGET_PLOT_LIST_SHIFT, 1, -1, ButtonStyles.BUTTON_STYLE_ARROW_RIGHT )
#		screen.hide( "PlotListPlus" )
		
		screen.setButtonGFC( self.PLOT_LIST_MINUS_NAME, u"", "", 315 + ( xResolution - (iMultiListXL+iMultiListXR) - 68 ), yResolution - 171, 32, 32, WidgetTypes.WIDGET_GENERAL, -1, -1, ButtonStyles.BUTTON_STYLE_ARROW_LEFT )
		screen.hide( self.PLOT_LIST_MINUS_NAME )
		screen.setButtonGFC( self.PLOT_LIST_PLUS_NAME, u"", "", 298 + ( xResolution - (iMultiListXL+iMultiListXR) - 34 ), yResolution - 171, 32, 32, WidgetTypes.WIDGET_GENERAL, 1, -1, ButtonStyles.BUTTON_STYLE_ARROW_RIGHT )
		screen.hide( self.PLOT_LIST_PLUS_NAME )

		screen.setImageButton( self.PLOT_LIST_UP_NAME, ArtFileMgr.getInterfaceArtInfo("PLE_ARROW_UP").getPath(), 315 + ( xResolution - (iMultiListXL+iMultiListXR) - 68 ) + 5, yResolution - 171 + 5, 20, 20, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.hide( self.PLOT_LIST_UP_NAME )
		screen.setImageButton( self.PLOT_LIST_DOWN_NAME, ArtFileMgr.getInterfaceArtInfo("PLE_ARROW_DOWN").getPath(), 298 + ( xResolution - (iMultiListXL+iMultiListXR) - 34 ) + 5, yResolution - 171 + 5, 20, 20, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.hide( self.PLOT_LIST_DOWN_NAME )

# BUG - PLE- end

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

# BUG - PLE- begin
			szName = self.PLE_PROMO_BUTTONS_UNITINFO + str(i)
			screen.addDDSGFC( szName, gc.getPromotionInfo(i).getButton(), \
								180, yResolution - 18, \
								self.CFG_INFOPANE_BUTTON_SIZE, self.CFG_INFOPANE_BUTTON_SIZE, \
								WidgetTypes.WIDGET_ACTION, gc.getPromotionInfo(i).getActionInfoIndex(), -1 )
			screen.hide( szName )
# BUG - PLE- end
			
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

# BUG - PLE - start 			
		# this ensures that the info pane is closed after a greater mouse pos change
		if self.bInfoPaneActive and (self.iInfoPaneCnt == (self.iLastInfoPaneCnt+1)): 
			tMousePos = CyInterface().getMousePos()
			if (tMousePos.x < self.tLastMousePos[0]-self.iMousePosTol) or \
				(tMousePos.x > self.tLastMousePos[0]+self.iMousePosTol) or \
				(tMousePos.y < self.tLastMousePos[1]-self.iMousePosTol) or \
				(tMousePos.y > self.tLastMousePos[1]+self.iMousePosTol):
				self.hideInfoPane()
				if self.bUnitPromoButtonsActive:
					self.hideUnitInfoPromoButtons()
# BUG - PLE - end

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

# BUG - city specialist - start
			self.updateCitizenButtons_hide()
			if (BugCityScreen.isCitySpecialist_Stacker()):
				self.updateCitizenButtons_Stacker()
			elif (BugCityScreen.isCitySpecialist_Chevron()):
				self.updateCitizenButtons_Chevron()
			else:
				self.updateCitizenButtons()
# BUG - city specialist - end
			
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

# BUG - Great Person Bar - start
		self.updateGreatPersonBar(screen)
# BUG - Great Person Bar - end

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

# BUG - PLE- begin
##		xResolution = screen.getXResolution()
##		yResolution = screen.getYResolution()

		self.hideInfoPane()
		self.xResolution = screen.getXResolution()
		self.yResolution = screen.getYResolution()
		
		# Capture these for looping over the plot's units
		self.bShowWoundedIndicator = BugPle.isShowWoundedIndicator()
		self.bShowGreatGeneralIndicator = BugPle.isShowGreatGeneralIndicator()
		self.bShowPromotionIndicator = BugPle.isShowPromotionIndicator()
		self.bShowUpgradeIndicator = BugPle.isShowUpgradeIndicator()
		self.bShowMissionInfo = BugPle.isShowMissionInfo()
		
		self.bShowHealthBar = BugPle.isShowHealthBar()
		self.bHideHealthBarWhileFighting = BugPle.isHideHealthFighting()
		self.bShowMoveBar = BugPle.isShowMoveBar()
		
		xResolution = self.xResolution
		yResolution = self.yResolution
# BUG - PLE- end

		bHandled = False
		if ( CyInterface().shouldDisplayUnitModel() and not CyEngine().isGlobeviewUp() and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL ):
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
			
# BUG - PLE- begin
#		pPlot = CyInterface().getSelectionPlot()
		
		self.iLoopCnt += 1
		
		self.pActPlot = CyInterface().getSelectionPlot()
		# if the plot changed, reset plot list offset
		if (self.pOldPlot):
			# check if plot has changed
			if (self.pOldPlot.getX() != self.pActPlot.getX()) or (self.pOldPlot.getY() != self.pActPlot.getY()):
				self.pOldPlot = self.pActPlot
				self.iColOffset = 0		
				self.iRowOffset = 0		
				self.bUpdatePLEUnitList = True
				# mt.debug("update plot:"+str(self.iLoopCnt))
		else:
			# initialization
			self.pOldPlot = self.pActPlot
			self.bUpdatePLEUnitList = True
			# mt.debug("update init:"+str(self.iLoopCnt))

			
		# check if the current unit has changed (eg. when it is unloaded). 
		# if so, do a reinit PLE Unit List
		pHeadSelectedUnit = CyInterface().getHeadSelectedUnit()
		try:
			id = pHeadSelectedUnit.getID()
			# mt.debug("Sel Unit:"+str(id))
			if (id in self.dPLEUnitInfo):
				lActUnitInfo = self.getPLEUnitInfo( pHeadSelectedUnit ) 	
				if (lActUnitInfo <> self.dPLEUnitInfo[ id ]):
					self.bUpdatePLEUnitList = True
					# mt.debug("update unload:"+str(self.iLoopCnt))
		except:
			# mt.debug("Sel Unit: <fail>")
			pass

		if (self.bUpdatePLEUnitList):
			self.getUnitList(self.pActPlot)
			self.bUpdatePLEUnitList = False
			# mt.debug("Sel Unit: UPDATE!")

		self.listPLEButtons = [(0,0,0)] * self.iMaxPlotListIcons
			
# BUG - PLE- end

		for i in range(gc.getNumPromotionInfos()):
			szName = "PromotionButton" + str(i)
			screen.moveToFront( szName )
		
# BUG - PLE- begin
#		screen.hide( "PlotListMinus" )
#		screen.hide( "PlotListPlus" )
#		
#		for j in range(gc.getMAX_PLOT_LIST_ROWS()):
#			#szStringPanel = "PlotListPanel" + str(j)
#			#screen.hide(szStringPanel)
#			
#			for i in range(self.numPlotListButtons()):
#				szString = "PlotListButton" + str(j*self.numPlotListButtons()+i)
#				screen.hide( szString )
#				
#				szStringHealth = szString + "Health"
#				screen.hide( szStringHealth )
#
#				szStringIcon = szString + "Icon"
#				screen.hide( szStringIcon )
#
#		if ( pPlot and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL and CyEngine().isGlobeviewUp() == False):
#
#			iVisibleUnits = CyInterface().getNumVisibleUnits()
#			iCount = -(CyInterface().getPlotListColumn())

		# hide all buttons
		if (not self.bPLEHide):
			self.hidePlotListButtonObjects(screen)		
				
		if ( self.pActPlot and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL and CyEngine().isGlobeviewUp() == False):

			nRow = 0
			nCol = 0		
			self.iVisibleUnits = CyInterface().getNumVisibleUnits()
			
			if self.sPLEMode == self.PLE_MODE_STANDARD:
				iCount = -self.iColOffset
				nNumUnits = self.getMaxCol()
			elif self.sPLEMode == self.PLE_MODE_MULTILINE:
				iCount = 0
				nNumUnits = self.iVisibleUnits
			elif self.sPLEMode == self.PLE_MODE_STACK_VERT:
				iCount = 0
				nCol = -self.iColOffset
				nNumUnits = self.iVisibleUnits
			elif self.sPLEMode == self.PLE_MODE_STACK_HORIZ:
				iCount = 0
				nRow = -self.iRowOffset
				nNumUnits = self.iVisibleUnits
				
			bUpArrow = False
			bDownArrow = False
			bFirstLoop = True
			
# BUG - PLE - end

			bLeftArrow = False
			bRightArrow = False
			
# BUG - PLE - start 			
#			if (CyInterface().isCityScreenUp()):
#				iMaxRows = 1
#				iSkipped = (gc.getMAX_PLOT_LIST_ROWS() - 1) * self.numPlotListButtons()
#				iCount += iSkipped
#			else:
#				iMaxRows = gc.getMAX_PLOT_LIST_ROWS()
#				iCount += CyInterface().getPlotListOffset()
#				iSkipped = 0
#
#			CyInterface().cacheInterfacePlotUnits(pPlot)
#			for i in range(CyInterface().getNumCachedInterfacePlotUnits()):
#				pLoopUnit = CyInterface().getCachedInterfacePlotUnit(i)
#				if (pLoopUnit):
#
#					if ((iCount == 0) and (CyInterface().getPlotListColumn() > 0)):
#						bLeftArrow = True
#					elif ((iCount == (gc.getMAX_PLOT_LIST_ROWS() * self.numPlotListButtons() - 1)) and ((iVisibleUnits - iCount - CyInterface().getPlotListColumn() + iSkipped) > 1)):
#						bRightArrow = True
#						
#					if ((iCount >= 0) and (iCount <  self.numPlotListButtons() * gc.getMAX_PLOT_LIST_ROWS())):
#						if ((pLoopUnit.getTeam() != gc.getGame().getActiveTeam()) or pLoopUnit.isWaiting()):
#							szFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_FORTIFY").getPath()
#							
#						elif (pLoopUnit.canMove()):
#							if (pLoopUnit.hasMoved()):
#								szFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_HASMOVED").getPath()
#							else:
#								szFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_MOVE").getPath()
#						else:
#							szFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_NOMOVE").getPath()
#
#						szString = "PlotListButton" + str(iCount)
#						screen.changeImageButton( szString, gc.getUnitInfo(pLoopUnit.getUnitType()).getButton() )
#						if ( pLoopUnit.getOwner() == gc.getGame().getActivePlayer() ):
#							bEnable = True
#						else:
#							bEnable = False
#						screen.enable(szString, bEnable)
#
#						if (pLoopUnit.IsSelected()):
#							screen.setState(szString, True)
#						else:
#							screen.setState(szString, False)
#						screen.show( szString )
#						
#						# place the health bar
#						if (pLoopUnit.isFighting()):
#							bShowHealth = False
#						elif (pLoopUnit.getDomainType() == DomainTypes.DOMAIN_AIR):
#							bShowHealth = pLoopUnit.canAirAttack()
#						else:
#							bShowHealth = pLoopUnit.canFight()
#						
#						if bShowHealth:
#							szStringHealth = szString + "Health"
#							screen.setBarPercentage( szStringHealth, InfoBarTypes.INFOBAR_STORED, float( pLoopUnit.currHitPoints() ) / float( pLoopUnit.maxHitPoints() ) )
#							if (pLoopUnit.getDamage() >= ((pLoopUnit.maxHitPoints() * 2) / 3)):
#								screen.setStackedBarColors(szStringHealth, InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_RED"))
#							elif (pLoopUnit.getDamage() >= (pLoopUnit.maxHitPoints() / 3)):
#								screen.setStackedBarColors(szStringHealth, InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_YELLOW"))
#							else:
#								screen.setStackedBarColors(szStringHealth, InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_GREEN"))
#							screen.show( szStringHealth )
#						
#						# Adds the overlay first
#						szStringIcon = szString + "Icon"
#						screen.changeDDSGFC( szStringIcon, szFileName )
#						screen.show( szStringIcon )
#
#					iCount = iCount + 1
#
#			if (iVisibleUnits > self.numPlotListButtons() * iMaxRows):
#				screen.enable("PlotListMinus", bLeftArrow)
#				screen.show( "PlotListMinus" )
#	
#				screen.enable("PlotListPlus", bRightArrow)
#				screen.show( "PlotListPlus" )
			
			iLastUnitType = UnitTypes.NO_UNIT
			iLastGroupID  = 0
			# loop for all units on the plot
			for i in range(len(self.lPLEUnitList)):
			
				pLoopUnit = self.getInterfacePlotUnit(i)
				
				if (pLoopUnit):
					
					# checks if the units matches actual filters
					if (self.checkDisplayFilter(pLoopUnit)):
													
						if not pLoopUnit.isCargo():
							iActUnitType = pLoopUnit.getUnitType()
							iActGroupID  = pLoopUnit.getGroupID()
							
						# standard view with scroll arrows
						if (self.sPLEMode == self.PLE_MODE_STANDARD):
						
							if (self.iColOffset > 0):
								bLeftArrow = True
							if ((self.iVisibleUnits - self.getMaxCol() - self.iColOffset) > 0):
								bRightArrow = True
								
							if ((iCount >= 0) and (iCount < nNumUnits )):
								nCol = iCount
								nRow = 0
								self.displayUnitPlotListObjects(screen, pLoopUnit, nRow, nCol)

						# multiline view
						elif (self.sPLEMode == self.PLE_MODE_MULTILINE):						

							if (self.iRowOffset > 0):
								bDownArrow = True
							if ((nRow >= self.getMaxRow()) > 0):
								bUpArrow = True
								
							nCol = self.getCol( iCount ) 
							nRow = self.getRow( iCount ) - self.iRowOffset
							if ((nRow >= 0) and (iCount < nNumUnits ) and (nRow < self.getMaxRow())):
								self.displayUnitPlotListObjects(screen, pLoopUnit, nRow, nCol)
								
						# vertical stack view
						elif (self.sPLEMode == self.PLE_MODE_STACK_VERT):

							if (self.iColOffset > 0):
								bLeftArrow = True
							if (nCol >= self.getMaxCol()):
								bRightArrow = True
								
							if (self.nPLEGrpMode == self.PLE_GRP_UNITTYPE):				
								if (iLastUnitType != UnitTypes.NO_UNIT):
									if (iActUnitType != iLastUnitType):
										nCol += 1
										nRow = 0
									else:
										nRow += 1
										if (nRow >= self.getMaxRow()):										
											nRow = 0
											nCol += 1								
							elif (self.nPLEGrpMode == self.PLE_GRP_GROUPS):
								if (iLastGroupID != 0):
									if (iActGroupID != iLastGroupID):
										nCol += 1
										nRow = 0
									else:
										nRow += 1
										if (nRow >= self.getMaxRow()):										
											nRow = 0
											nCol += 1								
							elif (self.nPLEGrpMode == self.PLE_GRP_PROMO):
								nRow = 0
								if not bFirstLoop:
									nCol += 1
							elif (self.nPLEGrpMode == self.PLE_GRP_UPGRADE):
								nRow = 0
								if not bFirstLoop:
									nCol += 1

							if ((nCol >= 0) and (iCount < nNumUnits ) and (nCol < self.getMaxCol())):
								self.displayUnitPlotListObjects(screen, pLoopUnit, nRow, nCol)
								if (self.nPLEGrpMode == self.PLE_GRP_PROMO):
									self.displayUnitPromos(screen, pLoopUnit, nRow, nCol)
								elif (self.nPLEGrpMode == self.PLE_GRP_UPGRADE):
									self.displayUnitUpgrades(screen, pLoopUnit, nRow, nCol)

						# horizontal stack view
						elif (self.sPLEMode == self.PLE_MODE_STACK_HORIZ):

							if (self.iRowOffset > 0):
								bDownArrow = True
							if ((nRow >= self.getMaxRow()) > 0):
								bUpArrow = True
								
							if (self.nPLEGrpMode == self.PLE_GRP_UNITTYPE):
								if ((iLastUnitType != UnitTypes.NO_UNIT)):
									if (iActUnitType != iLastUnitType):
										nRow += 1
										nCol = 0
									else:
										nCol += 1
										if (nCol >= self.getMaxCol()):										
											nCol = 0
											nRow += 1
							elif (self.nPLEGrpMode == self.PLE_GRP_GROUPS):
								if (iLastGroupID != 0):
									if (iActGroupID != iLastGroupID):
										nRow += 1
										nCol = 0
									else:
										nCol += 1
										if (nCol >= self.getMaxCol()):										
											nCol = 0
											nRow += 1
							elif (self.nPLEGrpMode == self.PLE_GRP_PROMO):
								nCol= 0
								if not bFirstLoop:
									nRow += 1
							elif (self.nPLEGrpMode == self.PLE_GRP_UPGRADE):
								nCol= 0
								if not bFirstLoop:
									nRow += 1

							if ((nRow >= 0) and (iCount < nNumUnits ) and (nRow < self.getMaxRow())):
								self.displayUnitPlotListObjects(screen, pLoopUnit, nRow, nCol)
								if (self.nPLEGrpMode == self.PLE_GRP_PROMO):
									self.displayUnitPromos(screen, pLoopUnit, nRow, nCol)
								elif (self.nPLEGrpMode == self.PLE_GRP_UPGRADE):
									self.displayUnitUpgrades(screen, pLoopUnit, nRow, nCol)

						iCount += 1
						
						iLastUnitType 	= iActUnitType
						iLastGroupID  	= iActGroupID
						bFirstLoop 		= false

			# left/right scroll buttons
			if 	( ( self.sPLEMode == self.PLE_MODE_STANDARD ) and ( self.iVisibleUnits > self.getMaxCol() ) ) or \
				( ( self.sPLEMode == self.PLE_MODE_STACK_VERT ) and ( ( nCol >= self.getMaxCol() or ( self.iColOffset > 0 ) ) ) ):
				screen.enable( self.PLOT_LIST_MINUS_NAME, bLeftArrow )
				screen.show( self.PLOT_LIST_MINUS_NAME )
				screen.enable( self.PLOT_LIST_PLUS_NAME, bRightArrow )
				screen.show( self.PLOT_LIST_PLUS_NAME )
				
			# up/Down scroll buttons
			if 	( ( self.sPLEMode == self.PLE_MODE_MULTILINE ) and ( ( nRow >= self.getMaxRow() or ( self.iRowOffset > 0 ) ) ) ) or \
				( ( self.sPLEMode == self.PLE_MODE_STACK_HORIZ ) and ( ( nRow >= self.getMaxRow() or ( self.iRowOffset > 0 ) ) ) ):
				screen.enable(self.PLOT_LIST_UP_NAME, bUpArrow )
				screen.show( self.PLOT_LIST_UP_NAME )
				screen.enable( self.PLOT_LIST_DOWN_NAME, bDownArrow )
				screen.show( self.PLOT_LIST_DOWN_NAME )
				
			self.showPlotListButtonObjects(screen)
			
		else:
			if (not self.bPLEHide):
				self.hidePlotListButtonObjects(screen)		
# BUG - PLE - end

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
		
# BUG - city specialist - start
	def updateCitizenButtons_hide( self ):

		global MAX_CITIZEN_BUTTONS
		
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
				szName = "CitizenChevron" + str((i * 100) + j)
				screen.hide( szName )

				szName = "IncresseCitizenButton" + str((i * 100) + j)
				screen.hide( szName )
				szName = "IncresseCitizenBanner" + str((i * 100) + j)
				screen.hide( szName )
				szName = "DecresseCitizenButton" + str((i * 100) + j)
				screen.hide( szName )
				szName = "CitizenButtonHighlight" + str((i * 100) + j)
				screen.hide( szName )

		global g_iSuperSpecialistCount
		global g_iCitySpecialistCount
		global g_iAngryCitizensCount

		screen.hide( "SpecialistBackground" )
		screen.hide( "SpecialistLabel" )

		for i in range( g_iSuperSpecialistCount ):
			szName = "FreeSpecialist" + str(i)
			screen.hide( szName )
		for i in range( g_iAngryCitizensCount ):
			szName = "AngryCitizen" + str(i)
			screen.hide( szName )

		for i in range( gc.getNumSpecialistInfos() ):
			for k in range( g_iCitySpecialistCount ):
				szName = "IncresseCitizenBanner" + str((i * 100) + k)					
				screen.hide( szName )
				szName = "IncresseCitizenButton" + str((i * 100) + k)					
				screen.hide( szName )
				szName = "DecresseCitizenButton" + str((i * 100) + k)					
				screen.hide( szName )

		return 0
# BUG - city specialist - end


	# Will update the citizen buttons
	def updateCitizenButtons( self ):

		if not CyInterface().isCityScreenUp(): return 0

		pHeadSelectedCity = CyInterface().getHeadSelectedCity()
		if not (pHeadSelectedCity and CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW): return 0
	
		global MAX_CITIZEN_BUTTONS
		
		bHandled = False
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )

		# Find out our resolution
		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()

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

# BUG - city specialist - start
	def updateCitizenButtons_Stacker( self ):
	
		if not CyInterface().isCityScreenUp(): return 0

		pHeadSelectedCity = CyInterface().getHeadSelectedCity()
		if not (pHeadSelectedCity and CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW): return 0

		global g_iSuperSpecialistCount
		global g_iCitySpecialistCount
		global g_iAngryCitizensCount
		
		bHandled = False
	
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )

		# Find out our resolution
		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()

		pHeadSelectedCity = CyInterface().getHeadSelectedCity()

		currentAngryCitizenCount = pHeadSelectedCity.angryPopulation(0)
		
		if(currentAngryCitizenCount > 0):
			stackWidth = 220 / currentAngryCitizenCount
			if (stackWidth > MAX_SPECIALIST_BUTTON_SPACING):
				stackWidth = MAX_SPECIALIST_BUTTON_SPACING

		for i in range(currentAngryCitizenCount):
			bHandled = True
			szName = "AngryCitizen" + str(i)
			screen.setImageButton( szName, ArtFileMgr.getInterfaceArtInfo("INTERFACE_ANGRYCITIZEN_TEXTURE").getPath(), xResolution - SPECIALIST_AREA_MARGIN - (stackWidth * i), yResolution - (282- SPECIALIST_ROW_HEIGHT), 30, 30, WidgetTypes.WIDGET_ANGRY_CITIZEN, -1, -1 )
			screen.show( szName )
			
		# update the max ever citizen counts
		if g_iAngryCitizensCount < currentAngryCitizenCount:
			g_iAngryCitizensCount = currentAngryCitizenCount

		iCount = 0
		bHandled = False
		currentSuperSpecialistCount = 0

		for i in range(gc.getNumSpecialistInfos()):
			if(pHeadSelectedCity.getFreeSpecialistCount(i) > 0):
				currentSuperSpecialistCount = currentSuperSpecialistCount + pHeadSelectedCity.getFreeSpecialistCount(i)

		if(currentSuperSpecialistCount > 0):
			stackWidth = 220 / currentSuperSpecialistCount 
			if (stackWidth > MAX_SPECIALIST_BUTTON_SPACING):
				stackWidth = MAX_SPECIALIST_BUTTON_SPACING

		for i in range(gc.getNumSpecialistInfos()):
			for j in range( pHeadSelectedCity.getFreeSpecialistCount(i) ):

				szName = "FreeSpecialist" + str(iCount)
				screen.setImageButton( szName, gc.getSpecialistInfo(i).getTexture(), (xResolution - SPECIALIST_AREA_MARGIN  - (stackWidth * iCount)), yResolution - (282 - SPECIALIST_ROW_HEIGHT * 2), 30, 30, WidgetTypes.WIDGET_FREE_CITIZEN, i, 1 )
				screen.show( szName )
				bHandled = true

				iCount = iCount + 1

		# update the max ever citizen counts
		if g_iSuperSpecialistCount < iCount:
			g_iSuperSpecialistCount = iCount

		iXShiftVal = 0
		iYShiftVal = 0
		iSpecialistCount = 0

		for i in range( gc.getNumSpecialistInfos() ):
		
			bHandled = False
			if( iSpecialistCount > SPECIALIST_ROWS ):
				iXShiftVal = 115
				iYShiftVal = (iSpecialistCount % SPECIALIST_ROWS) + 1
			else:
				iYShiftVal = iSpecialistCount

			if (gc.getSpecialistInfo(i).isVisible()):
				iSpecialistCount = iSpecialistCount + 1					
				
			if (gc.getPlayer(pHeadSelectedCity.getOwner()).isSpecialistValid(i) or i == 0):
				iCount = (pHeadSelectedCity.getPopulation() - pHeadSelectedCity.angryPopulation(0)) +  pHeadSelectedCity.totalFreeSpecialists()
			else:
				iCount = pHeadSelectedCity.getMaxSpecialistCount(i)

			# update the max ever citizen counts
			if g_iCitySpecialistCount < iCount:
				g_iCitySpecialistCount = iCount

			RowLength = 110
			if (i == 0):
			#if (i == gc.getInfoTypeForString(gc.getDefineSTRING("DEFAULT_SPECIALIST"))):
				RowLength *= 2
			
			HorizontalSpacing = MAX_SPECIALIST_BUTTON_SPACING	
			if (iCount > 0):
				HorizontalSpacing = RowLength / iCount
			if (HorizontalSpacing > MAX_SPECIALIST_BUTTON_SPACING):
				HorizontalSpacing = MAX_SPECIALIST_BUTTON_SPACING
									
			for k in range (iCount):
				if (k  >= pHeadSelectedCity.getSpecialistCount(i)):
					szName = "IncresseCitizenBanner" + str((i * 100) + k)					
					screen.addCheckBoxGFC( szName, gc.getSpecialistInfo(i).getTexture(), "", xResolution - (SPECIALIST_AREA_MARGIN + iXShiftVal) - (HorizontalSpacing * k), (yResolution - 282 - (SPECIALIST_ROW_HEIGHT * iYShiftVal)), 30, 30, WidgetTypes.WIDGET_CHANGE_SPECIALIST, i, 1, ButtonStyles.BUTTON_STYLE_LABEL )
					screen.enable( szName, False )
					screen.show( szName )
					
					szName = "IncresseCitizenButton" + str((i * 100) + k)					
					screen.addCheckBoxGFC( szName, "", "", xResolution - (SPECIALIST_AREA_MARGIN + iXShiftVal) - (HorizontalSpacing * k), (yResolution - 282 - (SPECIALIST_ROW_HEIGHT * iYShiftVal)), 30, 30, WidgetTypes.WIDGET_CHANGE_SPECIALIST, i, 1, ButtonStyles.BUTTON_STYLE_LABEL )					
					screen.show( szName )

				else:
					szName = "DecresseCitizenButton" + str((i * 100) + k)					
					screen.addCheckBoxGFC( szName, gc.getSpecialistInfo(i).getTexture(), "", xResolution - (SPECIALIST_AREA_MARGIN + iXShiftVal) - (HorizontalSpacing * k), (yResolution - 282 - (SPECIALIST_ROW_HEIGHT * iYShiftVal)), 30, 30, WidgetTypes.WIDGET_CHANGE_SPECIALIST, i, -1, ButtonStyles.BUTTON_STYLE_LABEL )
					screen.show( szName )
					
		screen.show( "SpecialistBackground" )
		screen.show( "SpecialistLabel" )
	
		return 0
# BUG - city specialist - end

# BUG - city specialist - start
	def updateCitizenButtons_Chevron( self ):
	
		if not CyInterface().isCityScreenUp(): return 0

		pHeadSelectedCity = CyInterface().getHeadSelectedCity()
		if not (pHeadSelectedCity and CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW): return 0

		global MAX_CITIZEN_BUTTONS
		
		bHandled = False
	
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )

		# Find out our resolution
		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()


		pHeadSelectedCity = CyInterface().getHeadSelectedCity()

		iCount = pHeadSelectedCity.angryPopulation(0)

		j = 0
		while (iCount > 0):
			bHandled = True
			szName = "AngryCitizen" + str(j)
			screen.show( szName )

			xCoord = xResolution - 74 - (26 * j)
			yCoord = yResolution - 238

			szName = "AngryCitizenChevron" + str(j)
			if iCount >= 20:
				szFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_CHEVRON20").getPath()
				iCount -= 20
			elif iCount >= 10:
				szFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_CHEVRON10").getPath()
				iCount -= 10
			elif iCount >= 5:
				szFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_CHEVRON5").getPath()
				iCount -= 5
			else:
				szFileName = ""
				iCount -= 1

			if (szFileName != ""):
				screen.addDDSGFC( szName , szFileName, xCoord, yCoord, 10, 10, WidgetTypes.WIDGET_CITIZEN, j, False )
				screen.show( szName )

			j += 1

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
						bHandled = True
					iCount += 1
					
		else:				
			for i in range(gc.getNumSpecialistInfos()):
				for j in range( pHeadSelectedCity.getFreeSpecialistCount(i) ):
					if (iCount < MAX_CITIZEN_BUTTONS):
						szName = "FreeSpecialist" + str(iCount)
						screen.setImageButton( szName, gc.getSpecialistInfo(i).getTexture(), (xResolution - 74  - (26 * iCount)), yResolution - 206, 24, 24, WidgetTypes.WIDGET_FREE_CITIZEN, i, -1 )
						screen.show( szName )
						bHandled = True

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
					
			iCount = pHeadSelectedCity.getSpecialistCount(i)

			j = 0
			while (iCount > 0):
				bHandled = True

				xCoord = xResolution - 74 - (26 * j)
				yCoord = yResolution - 272 - (26 * i)

				szName = "CitizenButton" + str((i * 100) + j)
				screen.addCheckBoxGFC( szName, gc.getSpecialistInfo(i).getTexture(), "", xCoord, yCoord, 24, 24, WidgetTypes.WIDGET_CITIZEN, i, j, ButtonStyles.BUTTON_STYLE_LABEL )
				screen.show( szName )

				szName = "CitizenChevron" + str((i * 100) + j)
				if iCount >= 20:
					szFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_CHEVRON20").getPath()
					iCount -= 20
				elif iCount >= 10:
					szFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_CHEVRON10").getPath()
					iCount -= 10
				elif iCount >= 5:
					szFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_CHEVRON5").getPath()
					iCount -= 5
				else:
					szFileName = ""
					iCount -= 1

				if (szFileName != ""):
					screen.addDDSGFC( szName , szFileName, xCoord, yCoord, 10, 10, WidgetTypes.WIDGET_CITIZEN, i, False )
					screen.show( szName )

				j += 1

			if ( not bHandled ):
				szName = "CitizenDisabledButton" + str(i)
				screen.show( szName )

		return 0
# BUG - city specialist - end

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

# BUG - Great General Bar - start
		screen.hide( "GreatGeneralBar" )
		screen.hide( "GreatGeneralBarText" )
# BUG - Great General Bar - end

# BUG - Bars on single line for higher resolution screens - start
		screen.hide( "GreatGeneralBar-w" )
		screen.hide( "ResearchBar-w" )
		screen.hide( "GreatPersonBar-w" )
# BUG - Bars on single line for higher resolution screens - end

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
				if (BugNJAGC.isEnabled()
				and BugNJAGC.isShowEra()):
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
				
				if (gc.getPlayer(ePlayer).isAnarchy()):
				
# BUG - Bars on single line for higher resolution screens - start
					if (xResolution >= 1440
					and (BugScreens.isShowCombatCounter() or BugScreens.isShowGPProgressBar())):
						xCoord = 268 + (xResolution - 1440) / 2 + 84 + 6 + 487 / 2
					else:
						xCoord = screen.centerX(512)

					yCoord = 3
					szText = localText.getText("INTERFACE_ANARCHY", (gc.getPlayer(ePlayer).getAnarchyTurns(), ))
					screen.setText( "ResearchText", "Background", szText, CvUtil.FONT_CENTER_JUSTIFY, xCoord, yCoord, -0.4, FontTypes.GAME_FONT, WidgetTypes.WIDGET_RESEARCH, -1, -1 )
# BUG - Bars on single line for higher resolution screens - end

					if ( gc.getPlayer(ePlayer).getCurrentResearch() != -1 ):
						screen.show( "ResearchText" )
					else:
						screen.hide( "ResearchText" )
					
				elif (gc.getPlayer(ePlayer).getCurrentResearch() != -1):

					szText = CyGameTextMgr().getResearchStr(ePlayer)

# BUG - Bars on single line for higher resolution screens - start
					if (xResolution >= 1440
					and (BugScreens.isShowCombatCounter() or BugScreens.isShowGPProgressBar())):
						szResearchBar = "ResearchBar-w"
						xCoord = 268 + (xResolution - 1440) / 2 + 84 + 6 + 487 / 2
					else:
						szResearchBar = "ResearchBar"
						xCoord = screen.centerX(512)

					yCoord = 3
					screen.setText( "ResearchText", "Background", szText, CvUtil.FONT_CENTER_JUSTIFY, xCoord, yCoord, -0.4, FontTypes.GAME_FONT, WidgetTypes.WIDGET_RESEARCH, -1, -1 )
					screen.show( "ResearchText" )
# BUG - Bars on single line for higher resolution screens - end

					researchProgress = gc.getTeam(gc.getPlayer(ePlayer).getTeam()).getResearchProgress(gc.getPlayer(ePlayer).getCurrentResearch())
					overflowResearch = (gc.getPlayer(ePlayer).getOverflowResearch() * gc.getPlayer(ePlayer).calculateResearchModifier(gc.getPlayer(ePlayer).getCurrentResearch()))/100
					researchCost = gc.getTeam(gc.getPlayer(ePlayer).getTeam()).getResearchCost(gc.getPlayer(ePlayer).getCurrentResearch())
					researchRate = gc.getPlayer(ePlayer).calculateResearchRate(-1)
					
					iFirst = float(researchProgress + overflowResearch) / float(researchCost)
					screen.setBarPercentage( szResearchBar, InfoBarTypes.INFOBAR_STORED, iFirst )
					if ( iFirst == 1 ):
						screen.setBarPercentage( szResearchBar, InfoBarTypes.INFOBAR_RATE, ( float(researchRate) / float(researchCost) ) )
					else:
						screen.setBarPercentage( szResearchBar, InfoBarTypes.INFOBAR_RATE, ( ( float(researchRate) / float(researchCost) ) ) / ( 1 - iFirst ) )

					screen.show( szResearchBar )
					
# BUG - Great Person Bar - start
				self.updateGreatPersonBar(screen)
# BUG - Great Person Bar - end

# BUG - Great General Bar - start
				self.updateGreatGeneralBar(screen)
# BUG - Great General Bar - end
					
		return 0
		
# BUG - Great Person Bar - start
	def updateGreatPersonBar(self, screen):
		if (not CyInterface().isCityScreenUp() and BugScreens.isShowGPProgressBar()):
			pHeadSelectedCity = CyInterface().getHeadSelectedCity()
			if (pHeadSelectedCity and pHeadSelectedCity.getOwner() == gc.getGame().getActivePlayer()):
				pGPCity = pHeadSelectedCity
				iGPTurns = GPUtil.getCityTurns(pGPCity)
			else:
				pGPCity, iGPTurns = GPUtil.findNextCity()
				if (not pGPCity):
					pGPCity, iGPP = GPUtil.findMaxCity()
			szText = GPUtil.getGreatPeopleText(pGPCity, iGPTurns, GP_BAR_WIDTH, BugScreens.isGPBarTypesNone(), BugScreens.isGPBarTypesOne(), True)
			szText = u"<font=2>%s</font>" % (szText)
			if (pGPCity):
				iCityID = pGPCity.getID()
			else:
				iCityID = -1
				
# BUG - Bars on single line for higher resolution screens - start
			xResolution = screen.getXResolution()
			if (xResolution >= 1440):
				szGreatPersonBar = "GreatPersonBar-w"
				xCoord = 268 + (xResolution - 1440) / 2 + 84 + 6 + 487 + 6 + 320 / 2
				yCoord = 5
			else:
				szGreatPersonBar = "GreatPersonBar"
				xCoord = 268 + (xResolution - 1024) / 2 + 100 + 7 + 380 / 2
				yCoord = 30

			screen.setText( "GreatPersonBarText", "Background", szText, CvUtil.FONT_CENTER_JUSTIFY, xCoord, yCoord, -0.4, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, iCityID, -1 )
			if (not pGPCity):
				screen.setHitTest( "GreatPersonBarText", HitTestTypes.HITTEST_NOHIT )
			screen.show( "GreatPersonBarText" )
# BUG - Bars on single line for higher resolution screens - end
			
			if (pGPCity):
				fThreshold = float(gc.getPlayer( pGPCity.getOwner() ).greatPeopleThreshold(False))
				fRate = float(pGPCity.getGreatPeopleRate())
				fFirst = float(pGPCity.getGreatPeopleProgress()) / fThreshold

				screen.setBarPercentage( szGreatPersonBar, InfoBarTypes.INFOBAR_STORED, fFirst )
				if ( fFirst == 1 ):
					screen.setBarPercentage( szGreatPersonBar, InfoBarTypes.INFOBAR_RATE, fRate / fThreshold )
				else:
					screen.setBarPercentage( szGreatPersonBar, InfoBarTypes.INFOBAR_RATE, fRate / fThreshold / ( 1 - fFirst ) )
			else:
				screen.setBarPercentage( szGreatPersonBar, InfoBarTypes.INFOBAR_STORED, 0 )
				screen.setBarPercentage( szGreatPersonBar, InfoBarTypes.INFOBAR_RATE, 0 )

			screen.show( szGreatPersonBar )
# BUG - Great Person Bar - end

# BUG - Great General Bar - start
	def updateGreatGeneralBar(self, screen):
		if (not CyInterface().isCityScreenUp() and BugScreens.isShowCombatCounter()):
			ePlayer = gc.getGame().getActivePlayer()
			iCombatExp = gc.getPlayer(ePlayer).getCombatExperience()
			iThresholdExp = gc.getPlayer(ePlayer).greatPeopleThreshold(True)
			iNeededExp = iThresholdExp - iCombatExp
			
			szText = localText.getText("INTERFACE_NEXT_GREAT_GENERAL_XP", (iNeededExp,))
			szText = u"<font=2>%s</font>" %(szText)

# BUG - Bars on single line for higher resolution screens - start
			xResolution = screen.getXResolution()
			if (xResolution >= 1440):
				szGreatGeneralBar = "GreatGeneralBar-w"
				xCoord = 268 + (xResolution - 1440) / 2 + 84 / 2
				yCoord = 5
			else:
				szGreatGeneralBar = "GreatGeneralBar"
				xCoord = 268 + (xResolution - 1024) / 2 + 100 / 2
				yCoord = 32

			screen.show( "GreatGeneralBarText" )
			screen.setLabel( "GreatGeneralBarText", "Background", szText, CvUtil.FONT_CENTER_JUSTIFY, xCoord, yCoord, -0.4, FontTypes.GAME_FONT, WidgetTypes.WIDGET_HELP_GREAT_GENERAL, -1, -1 )
# BUG - Bars on single line for higher resolution screens - end

			fProgress = float(iCombatExp) / float(iThresholdExp)
			screen.setBarPercentage( szGreatGeneralBar, InfoBarTypes.INFOBAR_STORED, fProgress )
			screen.show( szGreatGeneralBar )
# BUG - Great General Bar - end
					
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

# BUG - Anger Display - start
				bShowAngerCounter = False
# BUG - Anger Display - end
				if ((pHeadSelectedCity.happyLevel() >= 0) or (pHeadSelectedCity.unhappyLevel(0) > 0)):
					if (pHeadSelectedCity.isDisorder()):
						szBuffer = u"%d%c" %(pHeadSelectedCity.angryPopulation(0), CyGame().getSymbolID(FontSymbols.ANGRY_POP_CHAR))
					elif (pHeadSelectedCity.angryPopulation(0) > 0):
						szBuffer = localText.getText("INTERFACE_CITY_UNHAPPY", (pHeadSelectedCity.happyLevel(), pHeadSelectedCity.unhappyLevel(0), pHeadSelectedCity.angryPopulation(0)))
# BUG - Anger Display - start
						bShowAngerCounter = True
# BUG - Anger Display - end
					elif (pHeadSelectedCity.unhappyLevel(0) > 0):
						szBuffer = localText.getText("INTERFACE_CITY_HAPPY", (pHeadSelectedCity.happyLevel(), pHeadSelectedCity.unhappyLevel(0)))
# BUG - Anger Display - start
						bShowAngerCounter = True
# BUG - Anger Display - end
					else:
						szBuffer = localText.getText("INTERFACE_CITY_HAPPY_NO_UNHAPPY", (pHeadSelectedCity.happyLevel(), ))

# BUG - Anger Display - start
					if (BugCityScreen.isShowAngerCounter()
					and bShowAngerCounter):
						iAngerTimer = pHeadSelectedCity.getHurryAngerTimer()
						if iAngerTimer < pHeadSelectedCity.getConscriptAngerTimer():
							iAngerTimer = pHeadSelectedCity.getConscriptAngerTimer()

						if iAngerTimer != 0:
							szAnger = u"(%i)" %(iAngerTimer)
						else:
							szAnger = ""
#						szAnger = pHeadSelectedCity.flatHurryAngerLength()
						szBuffer = u"%s %s" %(szBuffer, szAnger)
# BUG - Anger Display - end

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
						lYieldLabels = [ localText.getText("TXT_KEY_RAW_PRODCOM_TILES", ()),
									   	 localText.getText("TXT_KEY_RAW_PRODCOM_SPECIALISTS", ()),
									   	 localText.getText("TXT_KEY_RAW_PRODCOM_BUILDINGS_CORPS", ()),
									   	 localText.getText("TXT_KEY_RAW_PRODCOM_TOTAL", ()) ]
						cYieldChar = PRODUCTION_CHAR
					else:
						lYieldLabels = [ localText.getText("TXT_KEY_RAW_PRODCOM_TILES", ()),
									   	 localText.getText("TXT_KEY_RAW_PRODCOM_TRADE", ()),
									   	 localText.getText("TXT_KEY_RAW_PRODCOM_BUILDINGS", ()),
									   	 localText.getText("TXT_KEY_RAW_PRODCOM_TOTAL", ()) ]
						cYieldChar = COMMERCE_CHAR
					
					iSpecialistsYield = 0
					for iSpec in range(gc.getNumSpecialistInfos()):
						iSpecialistsYield += gc.getActivePlayer().specialistYield(iSpec, g_iYieldType) * (pHeadSelectedCity.getSpecialistCount(iSpec) + pHeadSelectedCity.getFreeSpecialistCount(iSpec))
					
					iCorporationsYield = 0
					for iCorp in range(gc.getNumCorporationInfos()):
						if (pHeadSelectedCity.isHasCorporation(iCorp)):
							iCorporationsYield += pHeadSelectedCity.getCorporationYieldByCorporation(g_iYieldType, iCorp)
					
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
						szBuffer = u"%d%c" %( iCityBaseYield - iSpecialistsYield - iBuildingsProdYield - iCorporationsYield, cYieldChar )
					screen.setLabel( "RawWorkedPlotsText", "Background", szBuffer, CvUtil.FONT_RIGHT_JUSTIFY, 240, 160, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
					screen.show( "RawWorkedPlotsText" )
					
					# Trade Routes / Specialists
					if (g_iYieldType == YieldTypes.YIELD_COMMERCE):
						szBuffer = u"%d%c" %( iNetTradeYield, cYieldChar )
					else:
						szBuffer = u"%d%c" %( iSpecialistsYield, cYieldChar )
					screen.setLabel( "RawTradeRoutesSpecsText", "Background", szBuffer, CvUtil.FONT_RIGHT_JUSTIFY, 240, 180, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
					screen.show( "RawTradeRoutesSpecsText" )
					
					# Buildings
					if (g_iYieldType == YieldTypes.YIELD_COMMERCE):
						szBuffer = u"%d%c" %( iBuildingsYield + iSpecialistsYield, cYieldChar )
					else:
						szBuffer = u"%d%c" %( iBuildingsProdYield + iCorporationsYield, cYieldChar )
					screen.setLabel( "RawBuildingsText", "Background", szBuffer, CvUtil.FONT_RIGHT_JUSTIFY, 240, 200, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
					screen.show( "RawBuildingsText" )
					
					# Base Commerce (excludes modifiers like +50% Capital)
					if (iCityYieldDelta != 0):
						szBuffer = u"<color=205,180,55,255>%d%c + %d%c = %d%c</color>" %( iCityBaseYield, cYieldChar, iCityYieldDelta, cYieldChar, iCityTotalYield, cYieldChar )
					else:
						szBuffer = u"<color=205,180,55,255>%d</color>%c" %( iCityBaseYield, cYieldChar )
					screen.setLabel( "RawTotalText", "Background", szBuffer, CvUtil.FONT_RIGHT_JUSTIFY, 240, 220, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
					screen.show( "RawTotalText" )
					
					# Toggle Button
					if (g_iYieldType == YieldTypes.YIELD_COMMERCE):
						szBuffer = u"<font=2>%c</font><font=3>%c</font>" %( PRODUCTION_CHAR, COMMERCE_CHAR )
					else:
						szBuffer = u"<font=3>%c</font><font=2>%c</font>" %( PRODUCTION_CHAR, COMMERCE_CHAR )
					screen.setText( "RawToggleButton", "Background", szBuffer, CvUtil.FONT_CENTER_JUSTIFY, 165, 168, -0.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, g_iYieldType, -1 )
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
# BUG - Great Person Turns - start
					iRate = pHeadSelectedCity.getGreatPeopleRate()
					if BugCityScreen.isShowCityGreatPersonInfo():
						iGPTurns = GPUtil.getCityTurns(pHeadSelectedCity)
						szBuffer = GPUtil.getGreatPeopleText(pHeadSelectedCity, iGPTurns, 194, BugScreens.isGPBarTypesNone(), BugScreens.isGPBarTypesOne(), False)
					else:
						szBuffer = localText.getText("INTERFACE_CITY_GREATPEOPLE_RATE", (CyGame().getSymbolID(FontSymbols.GREAT_PEOPLE_CHAR), pHeadSelectedCity.getGreatPeopleRate()))
						if BugCityScreen.isShowGreatPersonTurns() and iRate > 0:
							iGPTurns = GPUtil.getCityTurns(pHeadSelectedCity)
							szBuffer += u" " + localText.getText("INTERFACE_CITY_TURNS", (iGPTurns, ))
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

# BUG - 3.17 No Espionage - start
				bNoEspionage = BugUtil.isNoEspionage()
# BUG - 3.17 No Espionage - end

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
					
					if (not bNoEspionage):
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
#
#										if (gc.getGame().isGameMultiPlayer()):
#											if (not (gc.getPlayer(ePlayer).isTurnActive())):
#												szBuffer = szBuffer + "*"
#												if (bAlignIcons):
#													scores.setActive()
#
# BUG - Dead Civs - start
										if (BugScore.isShowBothNames()):
											szPlayerName = gc.getPlayer(ePlayer).getName() + "/" + gc.getPlayer(ePlayer).getCivilizationShortDescription(0)
										elif (BugScore.isShowLeaderName()):
											szPlayerName = gc.getPlayer(ePlayer).getName()
										else:
											szPlayerName = gc.getPlayer(ePlayer).getCivilizationShortDescription(0)
									
#BUG - Scoreboard (AIMackey Multiplayer Fix) - Start
										if (gc.getGame().isGameMultiPlayer()):
											if (not gc.getPlayer(ePlayer).isTurnActive()):
												szPlayerName = "*" + szPlayerName	
												if (bAlignIcons):
													scores.setActive()
#BUG - Scoreboard (AIMackey Multiplayer Fix) - End
													
										if (not gc.getPlayer(ePlayer).isAlive() and BugScore.isShowDeadTag()):
											# BUG-TODO: localize
											szPlayerScore = localText.getText("TXT_KEY_BUG_DEAD_CIV", ())
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
												elif (gc.getTeam(gc.getGame().getActiveTeam()).isForcePeace(eTeam)):
													if (bAlignIcons):
														scores.setPeace()
												elif (gc.getTeam(eTeam).isAVassal()):
													for iOwnerTeam in range(gc.getMAX_TEAMS()):
														if (gc.getTeam(eTeam).isVassal(iOwnerTeam) and gc.getTeam(gc.getGame().getActiveTeam()).isForcePeace(iOwnerTeam)):
															if (bAlignIcons):
																scores.setPeace()
															break
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
											if (not bNoEspionage):
												for iMissionLoop in range(gc.getNumEspionageMissionInfos()):
													if (gc.getEspionageMissionInfo(iMissionLoop).isSeeResearch()):
														bEspionageCanSeeResearch = gc.getActivePlayer().canDoEspionageMission(iMissionLoop, ePlayer, None, -1)
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
													 and (bNoEspionage or gc.getActivePlayer().canDoEspionageMission(iDemographicsMission, ePlayer, None, -1)))):
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

# BUG - Worst Enemy - start
										if (BugScore.isShowWorstEnemy()):
											if (not gc.getPlayer(ePlayer).isHuman() and gc.getGame().getActivePlayer() != ePlayer):
												szWorstEnemy = gc.getPlayer(ePlayer).getWorstEnemyName()
												if (szWorstEnemy and gc.getActivePlayer().getName() == szWorstEnemy):
													cWorstEnemy =  u"%c" %(CyGame().getSymbolID(FontSymbols.ANGRY_POP_CHAR))
													szBuffer += cWorstEnemy
													if (bAlignIcons):
														scores.setWorstEnemy()
# BUG - Worst Enemy - end

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

# BUG - Bars on single line for higher resolution screens - start
		if (xResolution >= 1440
		and (BugScreens.isShowCombatCounter() or BugScreens.isShowGPProgressBar())):
			xCoord = 268 + (xResolution - 1440) / 2
			xCoord += 6 + 84
			screen.moveItem( szButtonID, 264 + ( ( xResolution - 1024 ) / 2 ) + ( 34 * ( iCount % 15 ) ), 0 + ( 34 * ( iCount / 15 ) ), -0.3 )
		else:
			xCoord = 264 + ( ( xResolution - 1024 ) / 2 )

		screen.moveItem( szButtonID, xCoord + ( 34 * ( iCount % 15 ) ), 0 + ( 34 * ( iCount / 15 ) ), -0.3 )
# BUG - Bars on single line for higher resolution screens - end

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
# BUG - PLE - start
		if  (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_ON) or \
			(inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_OFF) or \
			(inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED):
			if (self.MainInterfaceInputMap.has_key(inputClass.getFunctionName())):	
				return self.MainInterfaceInputMap.get(inputClass.getFunctionName())(inputClass)
			if (self.MainInterfaceInputMap.has_key(inputClass.getFunctionName() + "1")):	
				return self.MainInterfaceInputMap.get(inputClass.getFunctionName() + "1")(inputClass)
# BUG - PLE - end

# BUG - Raw Commerce - start
		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED):
			if (inputClass.getFunctionName() == "RawToggleButton"):
				global g_iYieldType
				if (g_iYieldType == YieldTypes.YIELD_COMMERCE):
					g_iYieldType = YieldTypes.YIELD_PRODUCTION
				else:
					g_iYieldType = YieldTypes.YIELD_COMMERCE
				CyInterface().setDirty(InterfaceDirtyBits.CityScreen_DIRTY_BIT, True)
				return 1
# BUG - Raw Commerce - end
		
# BUG - Great Person Bar - start
			elif (inputClass.getFunctionName() == "GreatPersonBar" or inputClass.getFunctionName() == "GreatPersonBarText"):
				# Zoom to next GP city
				iCity = inputClass.getData1()
				if (iCity == -1):
					pCity, _ = GPUtil.findNextCity()
				else:
					pCity = gc.getActivePlayer().getCity(iCity)
				CyInterface().selectCity(pCity, False)
				return 1
# BUG - Great Person Bar - end
		
		return 0
	
	def update(self, fDelta):
		return
