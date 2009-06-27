## Unit Plot List Utilities
##
## Holds the information used to display the unit plot list
##
## Copyright (c) 2007-2009 The BUG Mod.
##
## Author: Ruff_Hi

from CvPythonExtensions import *
import MonkeyTools as mt
import BugUtil

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

iLeaderPromo = gc.getInfoTypeForString('PROMOTION_LEADER')
sFileNamePromo = ArtFileMgr.getInterfaceArtInfo("OVERLAY_PROMOTION_FRAME").getPath()
screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )

# constants
sUpdateShow = "SHOW"
sUpdateShowIf = "SHOWIF"
sUpdateHide = "HIDE"
sUpdateNothing = "NOTHING"
sBupStringBase = "BUGUnitPlotString"

def updatePLEOptions():
	# Capture these for looping over the plot's units
	self.bShowWoundedIndicator = PleOpt.isShowWoundedIndicator()
	self.bShowGreatGeneralIndicator = PleOpt.isShowGreatGeneralIndicator()
	self.bShowPromotionIndicator = PleOpt.isShowPromotionIndicator()
	self.bShowUpgradeIndicator = PleOpt.isShowUpgradeIndicator()
	self.bShowMissionInfo = PleOpt.isShowMissionInfo()
	self.bShowHealthBar = PleOpt.isShowHealthBar()
	self.bHideHealthBarWhileFighting = PleOpt.isHideHealthFighting()
	self.bShowMoveBar = PleOpt.isShowMoveBar()

## Notes:
## - the vanilla BtS unit plot list has a panel for each row of icons and the units are arranged from the bottom left
## - the PLE unit plot list has no panel (drawn straight onto the screen) and counts from the top left (when in standard format)
## - the BUG unit plot list has one big panel and counts from the bottom left
##    - this means that the max'th row fills up first, then the max'th-1, etc.
## - x counts the columns across the panel, from 0 to max - 1
## - y counts the rows down the panel, from 0 to max - 1

## _getx and _gety return the number of pixels for each unitplot from the top left of the panel (not from the top left of the screen!)

class UnitList:
	def __init__(self, vScreen, vCols, vRows, yRes):
		screen = vScreen
		iCols = vCols
		iRows = vRows

		_x = 315 - 3
		_y = yRes - 169 - 3 + (1 - vRows) * 34
		_w = vCols * 34 + 3
		_h = vRows * 34 + 3
		sBupPanel = sBupStringBase + "BackgroundPanel"
		screen.addPanel(sBupPanel, u"", u"", True, False, _x, _y, _w, _h, PanelStyles.PANEL_STYLE_EMPTY)

		UnitPlots = []
		for i in range(vCols * vRows):
			UnitPlots.append(UnitPlot(sBupPanel, i, _getx(i), _gety(i)))

	def _getx(self, iIndex):
		_col = iIndex % iCols
		return _col - 1

	def _gety(self, iIndex):
		_row = iIndex / iCols
		return iRows - irow

	def _getIndex(self, x, y):
		return (iRows - y) * iCols + x - 1


#	def getMaxCol(self):
#		return ((self.xResolution - (iMultiListXL+iMultiListXR) - 68) / 34)
#		
#	def getMaxRow(self):
#		return ((self.yResolution - 160) / PleOpt.getVerticalSpacing()) 
#		
#	def getRow(self, i):
#		return i / self.getMaxCol()

#	def getCol(self, i):
#		return i % self.getMaxCol()
#		
#	def getX(self, nCol):
#		return 315 + (nCol * PleOpt.getHoriztonalSpacing())
#		
#	def getY(self, nRow):
#		return self.yResolution - 169 - (nRow * PleOpt.getVerticalSpacing())
#		
#	def getI(self, nRow, nCol):
#		return ( nRow * self.getMaxCol() ) + ( nCol % self.getMaxCol() )






## - xPixel is the number of horizontal pixels from the top left of the BUG unit plot list panel
## - yPixel is the number of vertically pixels from the top left of the BUG unit plot list panel



class UnitPlot:
	def __init__(self, vBupPanel, iIndex, x, y):
		sBupString = sBupStringBase + str(iIndex)
		xPixel = _getxPixel(x)
		yPixel = _getyPixel(x)

		# add promo frame
		screen.addDDSGFCAt(sBupString + "PromoFrame", vBupPanel, sFileNamePromo, xPixel + 2, yPixel + 2, 32, 32, WidgetTypes.WIDGET_PLOT_LIST, iIndex, -1, False )
		screen.hide(sBupString + "PromoFrame")


	def _getxPixel(self, x):
		return x * 34 + 3

	def _getyPixel(self, y):
		return y * 34 + 3

#		_updatePromo(sBupString + "PromoFrame", None, None, sUpdateNew)



#				szStringPromoFrame  = szString + "PromoFrame"









#		for i in range( self.iMaxPlotListIcons ):
#			szString = self.PLOT_LIST_BUTTON_NAME + str(i)
#			screen.hide( szString )
#			screen.hide( szString + "Icon" )
#			screen.hide( szString + "HealthBar" )
#			screen.hide( szString + "MoveBar" )
#			screen.hide( szString + "PromoFrame" )
#			screen.hide( szString + "ActionIcon" )
#			screen.hide( szString + "Upgrade" )



	def update(self, pUnit):
		pPrevUnit = pCurrUnit
		pCurrUnit = UnitDisplay(pUnit)

		# Unit Plot
		if pCurrUnit == None:
			if pPrevUnit != None:
				# current unit is blank, previous unit was not blank
				_updatePromo(sBupString + "PromoFrame", pCurrUnit, pPrevUnit, sUpdateHide)
			else:
				# current unit is blank, previous unit was blank
				_updatePromo(sBupString + "PromoFrame", pCurrUnit, pPrevUnit, sUpdateNothing)
		else:
			if pPrevUnit != None:
				# current unit is not blank, previous unit was not blank
				_updatePromo(sBupString + "PromoFrame", pCurrUnit, pPrevUnit, sUpdateShowIf)
			else:
				# current unit is not blank, previous unit was blank
				_updatePromo(sBupString + "PromoFrame", pCurrUnit, pPrevUnit, sUpdateShow)








	def _updatePromo(self, vString, pCurrUnit, pPrevUnit, sUpdate):
		if sUpdate == sUpdateNothing:
			return

		if sUpdate == sUpdateHide:
			screen.hide(vString)
			return

		if sUpdate == sUpdateShow:
			screen.show(vString)
			return

		if pCurrUnit.bPromo == None:
			if pPrevUnit.bPromo != None:
				_updatePromo(vString, pCurrUnit, pPrevUnit, sUpdateHide)
				return
			else:
				_updatePromo(vString, pCurrUnit, pPrevUnit, sUpdateNothing)
				return
		else:
			if pPrevUnit.bPromo != None:
				#_updatePromo(vString, pCurrUnit, pPrevUnit, sUpdateShowIf)
				return
			else:
				_updatePromo(vString, pCurrUnit, pPrevUnit, sUpdateShow)
				return



class UnitDisplay:
	def __init__(self, pUnit):
		self.bSelected = pUnit.IsSelected()
		self.eUnit = pUnit.getUnitType()
		self.sDotState, self.iDotxSize, self.iDotySize, self.iDotxOffset, self.iDotyOffset = _getDOTInfo(pUnit)
		self.sMission = _getMission(pUnit)
		self.bPromo = pUnit.isPromotionReady()
		self.bGG = iLeaderPromo != -1 and pUnit.isHasPromotion(iLeaderPromo)
		self.bUpgrade = mt.checkAnyUpgrade(pUnit)
		self.icurrHitPoints = pUnit.currHitPoints()
		self.imaxHitPoints = pUnit.maxHitPoints()
		self.iMovesLeft = pUnit.movesLeft()
		self.iMoves = pUnit.getMoves()

	def _getDOTInfo(self, pUnit):
		xSize = 12
		ySize = 12
		xOffset = 0
		yOffset = 0

		if ((pUnit.getTeam() != gc.getGame().getActiveTeam()) or pUnit.isWaiting()):
			# fortified
			szDotState = "OVERLAY_FORTIFY"
		elif (pUnit.canMove()):
			if (pUnit.hasMoved()):
				# unit moved, but some movement points are left
				szDotState = "OVERLAY_HASMOVED"
			else:
				# unit did not move yet
				szDotState = "OVERLAY_MOVE"
		else:
			# unit has no movement points left
			szDotState = "OVERLAY_NOMOVE"

		# Wounded units will get a darker colored button.
		if (self.bShowWoundedIndicator) and (pUnit.isHurt()):
			szDotState += "_INJURED"

		# Units lead by a GG will get a star instead of a dot.
		if (self.bShowGreatGeneralIndicator):
			# is unit lead by a GG?
			if (iLeaderPromo != -1 and pUnit.isHasPromotion(iLeaderPromo)):
				szDotState += "_GG"
				xSize = 16
				ySize = 16
				xOffset = -3
				yOffset = -3

		return szDotState, xSize, ySize, xOffset, yOffset

	def _getMission(self, pUnit):
		eActivityType = pUnit.getGroup().getActivityType()
		eAutomationType = pUnit.getGroup().getAutomateType()

		# is unit on air intercept mission
		if (eActivityType == ActivityTypes.ACTIVITY_INTERCEPT):
			return "OVERLAY_ACTION_INTERCEPT"
		# is unit on boat patrol coast mission
		elif (eActivityType == ActivityTypes.ACTIVITY_PATROL):
			return "OVERLAY_ACTION_PATROL"
		# is unit on boat blockade mission
		elif (eActivityType == ActivityTypes.ACTIVITY_PLUNDER):
			return "OVERLAY_ACTION_PLUNDER"
		# is unit fortified for healing (wake up when healed)
		elif (eActivityType == ActivityTypes.ACTIVITY_HEAL):
			return "OVERLAY_ACTION_HEAL"
		# is unit sentry (wake up when enemy in sight)
		elif (eActivityType == ActivityTypes.ACTIVITY_SENTRY):
			return "OVERLAY_ACTION_SENTRY"
		# is the turn for this unit skipped (wake up next turn)
		elif (eActivityType == ActivityTypes.ACTIVITY_HOLD):
			return "OVERLAY_ACTION_SKIP"
		# has unit exploration mission
		elif (eAutomationType == AutomateTypes.AUTOMATE_EXPLORE):
			return "OVERLAY_ACTION_EXPLORE"
		# is unit automated generally (only worker units)
		elif (eAutomationType == AutomateTypes.AUTOMATE_BUILD):
			return "OVERLAY_ACTION_AUTO_BUILD"
		# is unit automated for nearest city (only worker units)
		elif (eAutomationType == AutomateTypes.AUTOMATE_CITY):
			return "OVERLAY_ACTION_AUTO_CITY"
		# is unit automated for network (only worker units)
		elif (eAutomationType == AutomateTypes.AUTOMATE_NETWORK):
			return "OVERLAY_ACTION_AUTO_NETWORK"
		# is unit automated spread religion (only missionary units)
		elif (eAutomationType == AutomateTypes.AUTOMATE_RELIGION):
			return "OVERLAY_ACTION_AUTO_RELIGION"
		# has unit a mission
		elif (pUnit.getGroup().getLengthMissionQueue() > 0):
			eMissionType = pUnit.getGroup().getMissionType(0)
			# is the mission to build an improvement
			if (eMissionType == MissionTypes.MISSION_BUILD):
				return "OVERLAY_ACTION_BUILD"
			# is the mission a "move to" mission
			elif (eMissionType in UnitUtil.MOVE_TO_MISSIONS):
				return "OVERLAY_ACTION_GOTO"
		# if nothing of above, but unit is waiting -> unit is fortified
		elif (pUnit.isWaiting()):
			if (pUnit.isFortifyable()):
				return "OVERLAY_ACTION_FORTIFY"
			else:
				return "OVERLAY_ACTION_SLEEP"

		return ""
