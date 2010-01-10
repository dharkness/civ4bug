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
import UnitUtil

import BugCore
PleOpt = BugCore.game.PLE

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

iLeaderPromo = gc.getInfoTypeForString('PROMOTION_LEADER')
#screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )

# constants
#(sUpdateShow,
# sUpdateShowIf,
# sUpdateHide,
# sUpdateNothing,
#) = range(4)


sBupStringBase = "BUGUnitPlotString"
cBupCellSize = 34
cBupCellSpacing = 3

class BupPanel:
	def __init__(self, screen, yRes, iVanCols, iVanRows):
		self.CellSpacing = cBupCellSpacing
		self.MaxCells = iVanCols * iVanRows
		self.Rows = iVanRows
		self.Cols = iVanCols

		BugUtil.debug("BupPanel %i %i %i", yRes, iVanCols, iVanRows)

		self.screen = screen
		self.xPanel = 315 - cBupCellSpacing
		self.yPanel = yRes - 169 + (1 - iVanRows) * cBupCellSize - cBupCellSpacing
		self.wPanel = iVanCols * cBupCellSize + cBupCellSpacing
		self.hPanel = iVanRows * cBupCellSize + cBupCellSpacing
#		self.sBupPanel = sBupStringBase + "BackgroundPanel"

		BugUtil.debug("BupPanel %i %i %i %i", self.xPanel, self.yPanel, self.wPanel, self.hPanel)

#		self.screen.addPanel(self.sBupPanel, u"", u"", True, False, self.xPanel, self.yPanel, self.wPanel, self.hPanel, PanelStyles.PANEL_STYLE_MAIN)  #PanelStyles.PANEL_STYLE_EMPTY
#		self.screen.addPanel(self.sBupPanel, u"", u"", True, False, self.xPanel, self.yPanel, self.wPanel, self.hPanel, PanelStyles.PANEL_STYLE_EMPTY)
#		self.screen.hide(self.sBupPanel)

		sTexture = getArt("INTERFACE_BUTTONS_GOVERNOR")
		sHiLiteTexture = getArt("BUTTON_HILITE_SQUARE")
		sFileNamePromo = getArt("OVERLAY_PROMOTION_FRAME")

		for iIndex in range(self.MaxCells):
			szBupCell = self._getCellWidget(iIndex)
			iX = self._getX(self._getCol(iIndex))
			iY = self._getY(self._getRow(iIndex))

			BugUtil.debug("BupPanel MaxCells %i %i %i %i %i", iIndex, self._getCol(iIndex), self._getRow(iIndex), self._getX(self._getCol(iIndex)), self._getY(self._getRow(iIndex)))

			# place/init the promotion frame. Important to have it at first place within the for loop.
			szStringPromoFrame = szBupCell + "PromoFrame"
			screen.addDDSGFC(szStringPromoFrame, sFileNamePromo, iX, iY, 32, 32, WidgetTypes.WIDGET_GENERAL, iIndex, -1 )
			screen.hide(szStringPromoFrame)

#VOID addDDSGFC(STRING szName, STRING szTexture, INT iX, INT iY, INT iWidth, INT iHeight, WidgetType eWidgetType, INT iData1, INT iData2)
#VOID addDDSGFCAt(STRING szName, STRING szAttachTo, STRING szTexture, INT iX, INT iY, INT iWidth, INT iHeight, WidgetType eWidgetType, INT iData1, INT iData2, BOOL bOption)
#VOID addCheckBoxGFC(STRING szName, STRING szTexture, STRING szHiliteTexture, INT iX, INT iY, INT iWidth, INT iHeight, WidgetType eWidgetType, INT iData1, INT iData2, ButtonStyle eStyle)
#VOID addCheckBoxGFCAt(STRING szName, STRING szTexture, STRING szHiliteTexture, INT iX, INT iY, INT iWidth, INT iHeight, WidgetType eWidgetType, INT iData1, INT iData2, ButtonStyle eStyle)

			screen.addCheckBoxGFC(szBupCell, sTexture, sHiLiteTexture, iX, iY, 32, 32, WidgetTypes.WIDGET_PLOT_LIST, iIndex, -1, ButtonStyles.BUTTON_STYLE_LABEL)
			screen.hide(szBupCell)

#			screen.attachCheckBoxGFC(self.sBupPanel, szBupCell, sTexture, sHiLiteTexture, 32, 32, WidgetTypes.WIDGET_PLOT_LIST, iIndex, -1, ButtonStyles.BUTTON_STYLE_LABEL)

#VOID attachCheckBoxGFC(STRING szAttachTo, STRING szName, STRING szTexture, STRING szHiliteTexture, INT iWidth, INT iHeight, WidgetType eWidgetType, INT iData1, INT iData2, ButtonStyle eStyle)
#VOID addCheckBoxGFC(STRING szName, STRING szTexture, STRING szHiliteTexture, INT iX, INT iY, INT iWidth, INT iHeight, WidgetType eWidgetType, INT iData1, INT iData2, ButtonStyle eStyle)
#VOID addCheckBoxGFCAt(STRING szName, STRING szTexture, STRING szHiliteTexture, INT iX, INT iY, INT iWidth, INT iHeight, WidgetType eWidgetType, INT iData1, INT iData2, ButtonStyle eStyle)




		self.BupUnits = []
		self.BupUnitsPrior = []

#	def setCellSpacing(self, iSpacing):
#		self.BupCellSpacing = iSpacing

		self.bShowWoundedIndicator = True
		self.bShowGreatGeneralIndicator = True
		self.bShowPromotionIndicator = True
		self.bShowUpgradeIndicator = True
		self.bShowMissionInfo = True
		self.bShowHealthBar = True
		self.bHideHealthBarWhileFighting = True
		self.bShowMoveBar = True

	def UpdateBUGOptions(self):
		self.bShowWoundedIndicator = PleOpt.isShowWoundedIndicator()
		self.bShowGreatGeneralIndicator = PleOpt.isShowGreatGeneralIndicator()
		self.bShowPromotionIndicator = PleOpt.isShowPromotionIndicator()
		self.bShowUpgradeIndicator = PleOpt.isShowUpgradeIndicator()
		self.bShowMissionInfo = PleOpt.isShowMissionInfo()
		self.bShowHealthBar = PleOpt.isShowHealthBar()
		self.bHideHealthBarWhileFighting = PleOpt.isHideHealthFighting()
		self.bShowMoveBar = PleOpt.isShowMoveBar()

	def Draw(self):
#		self.screen.show(self.sBupPanel)

		iIndex = 0
		while iIndex <= self.MaxCells:
			szBupCell = self._getCellWidget(iIndex)
			self.screen.hide(szBupCell)
			self.screen.hide(szBupCell + "Dot")
			self.screen.hide(szBupCell + "PromoFrame")
			self.screen.hide(szBupCell + "Upgrade")
			self.screen.hide(szBupCell + "Mission")
			iIndex += 1

		iIndex = CyInterface().getPlotListOffset()
		iMaxUnits = max(len(self.BupUnits), len(self.BupUnitsPrior))
		for iUnit in range(iMaxUnits):
			if iUnit < len(self.BupUnits):
				cBupUnit = self.BupUnits[iUnit]
			else:
				cBupUnit = None
			if iUnit < len(self.BupUnitsPrior):
				pBupUnit = self.BupUnitsPrior[iUnit]
			else:
				pBupUnit = None

			szBupCell = self._getCellWidget(iIndex)
			self._drawUnitIcon(cBupUnit, pBupUnit, szBupCell)

			if (cBupUnit is not None
			and cBupUnit.Owner == gc.getGame().getActivePlayer()):
				iX = self._getX(self._getCol(iIndex))
				iY = self._getY(self._getRow(iIndex))

#		self.xPanel = 315 - cBupCellSpacing
#		self.yPanel = yRes - 169 + (1 - iVanRows) * cBupCellSize - cBupCellSpacing

#def displayUnitPlotList_Dot( self, screen, pLoopUnit, szString, iCount, x, y, bShowWoundedIndicator, bShowGreatGeneralIndicator ):

				self._drawDot(cBupUnit, pBupUnit, szBupCell, iIndex, iX, iY + 4)
				self._drawPromo(cBupUnit, pBupUnit, szBupCell)
				self._drawUpgrade(cBupUnit, pBupUnit, szBupCell, iIndex, iX, iY)
				self._drawMission(cBupUnit, pBupUnit, szBupCell, iIndex, iX, iY)

#				displayUnitPlotList_Mission( self.screen, pBupUnit, szBupCell, iIndex, iX, iY - 22, 12)




			iIndex += 1

		# save the current units for next time
		self.BupUnitsPrior = []
		for iUnit in range(len(self.BupUnits)):
			self.BupUnitsPrior.append(self.BupUnits[iUnit])






	def Hide(self):
		iIndex = 0
		while iIndex <= self.MaxCells:
			szBupCell = self._getCellWidget(iIndex)
			self.screen.hide(szBupCell)
			self.screen.hide(szBupCell + "Dot")
			self.screen.hide(szBupCell + "PromoFrame")
			self.screen.hide(szBupCell + "Upgrade")
			self.screen.hide(szBupCell + "Mission")
			iIndex += 1

	def addUnit(self, pUnit):
		self.BupUnits.append(BupUnit(pUnit))

	def clearUnits(self):
		self.BupUnits = []
		self.BupUnitsPrior = []

#	def clearAllUnits(self):
#		self.BupUnits = []
#		self.BupUnitsPrior = []


	def _drawUnitIcon(self, cBupUnit, pBupUnit, szBupCell):
		if cBupUnit is not None:
			self.screen.changeImageButton(szBupCell, gc.getUnitInfo(cBupUnit.UnitType).getButton())
			self.screen.enable(szBupCell, cBupUnit.Owner == gc.getGame().getActivePlayer())
			self.screen.setState(szBupCell, cBupUnit.isSelected)
			self.screen.show(szBupCell)

	def _drawDot(self, cBupUnit, pBupUnit, szString, iCount, x, y):
		# handles the display of the colored buttons in the upper left corner of each unit icon.
		if cBupUnit is not None:
			# Units lead by a GG will get a star instead of a dot - and the location and size of star differs
			if (PleOpt.isShowGreatGeneralIndicator()
			and cBupUnit.isLeadByGreatGeneral):
				xSize = 16
				ySize = 16
				xOffset = -3
				yOffset = -3
			else:
				xSize = 12
				ySize = 12
				xOffset = 0
				yOffset = 0

			# display the colored spot icon
			self.screen.addDDSGFC(szString + "Dot", getArt(cBupUnit.DotStatus), x-3+xOffset, y-7+yOffset, xSize, ySize, WidgetTypes.WIDGET_GENERAL, iCount, -1 )

	def _drawPromo(self, cBupUnit, pBupUnit, szString):
		if (PleOpt.isShowPromotionIndicator()
		and cBupUnit.isPromotionReady):
			self.screen.show(szString + "PromoFrame")

	def _drawUpgrade(self, cBupUnit, pBupUnit, szString, iCount, x, y):
		if (cBupUnit.isCanUpgrade):
			# place the upgrade arrow
			self.screen.addDDSGFC(szString + "Upgrade", getArt("OVERLAY_UPGRADE"), x+2, y+14, 8, 16, WidgetTypes.WIDGET_GENERAL, iCount, -1 )

	def _drawMission(self, cBupUnit, pBupUnit, szString, iCount, x, y):
		if PleOpt.isShowMissionInfo():
			if cBupUnit.Mission != "":
#				sMission = getArt(cBupUnit.Mission)
				self.screen.addDDSGFC(szString + "Mission", getArt(cBupUnit.Mission), x+20, y+20, 12, 12, WidgetTypes.WIDGET_GENERAL, iCount, -1)






	def _getMaxCols(self):
		return self.Cols

	def _getMaxRows(self):
		return self.Rows

	def _getRow(self, i):
#		return self._getMaxRows() - i / self._getMaxCols() - 1
		return i / self._getMaxCols()

	def _getCol(self, i):
		return i % self._getMaxCols()

	def _getX(self, nCol):
		return nCol * cBupCellSize + self.xPanel

	def _getY(self, nRow):
		return nRow * cBupCellSize + self.yPanel

	def _getCellWidget(self, index):
		return sBupStringBase + "BackgroundCell" + str(index)

#	def _getIndex(self, nRow, nCol):
#		return ( nRow * self.getMaxCol() ) + ( nCol % self.getMaxCol() )

############## functions for visual objects (show and hide) ######################
		
	# PLE Grouping Mode Switcher 















































class BupUnit:
	def __init__(self, pUnit):
		self.pUnit = pUnit

		# unit type
		self.UnitType = pUnit.getUnitType()
		self.Owner = pUnit.getOwner()
		self.isSelected = pUnit.IsSelected()

		self.isFortified = pUnit.getTeam() != gc.getGame().getActiveTeam() or pUnit.isWaiting()
		self.isMoved = pUnit.canMove() and pUnit.hasMoved()
		self.isMove = pUnit.canMove() and not pUnit.hasMoved()
		self.isNotMove = not pUnit.canMove()
		self.isHurt = pUnit.isHurt()

		iLeaderPromo = gc.getInfoTypeForString('PROMOTION_LEADER')
		self.isLeadByGreatGeneral = iLeaderPromo != -1 and pUnit.isHasPromotion(iLeaderPromo)




		self.DotStatus = self._getDotStatus()
		self.Mission = self._getMission(pUnit)

		self.isPromotionReady = pUnit.isPromotionReady()

		if PleOpt.isShowUpgradeIndicator():
			self.isCanUpgrade = mt.checkAnyUpgrade(pUnit)
		else:
			self.isCanUpgrade = False

	def _getDotStatus(self):
		sDotStatus = ""
		if self.isFortified:  # fortified
			sDotStatus = "OVERLAY_FORTIFY"
		elif self.isMoved:  # unit moved, but some movement points are left
			sDotStatus = "OVERLAY_HASMOVED"
		elif self.isMove:  # unit did not move yet
			sDotStatus = "OVERLAY_MOVE"
		else: # unit has no movement points left
			sDotStatus = "OVERLAY_NOMOVE"

		# Wounded units will get a darker colored button.
		if (PleOpt.isShowWoundedIndicator()
		and self.isHurt):
			sDotStatus += "_INJURED"

		# Units lead by a GG will get a star instead of a dot.
		if (PleOpt.isShowGreatGeneralIndicator()
		and self.isLeadByGreatGeneral):
			sDotStatus += "_GG"

		return sDotStatus

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



#		self.bSelected = pUnit.IsSelected()
#		self.eUnit = pUnit.getUnitType()
#		self.sDotState, self.iDotxSize, self.iDotySize, self.iDotxOffset, self.iDotyOffset = _getDOTInfo(pUnit)
#		self.sMission = _getMission(pUnit)
#		self.bPromo = pUnit.isPromotionReady()
#		self.bGG = iLeaderPromo != -1 and pUnit.isHasPromotion(iLeaderPromo)
#		self.bUpgrade = mt.checkAnyUpgrade(pUnit)
#		self.icurrHitPoints = pUnit.currHitPoints()
#		self.imaxHitPoints = pUnit.maxHitPoints()
#		self.iMovesLeft = pUnit.movesLeft()
#		self.iMoves = pUnit.getMoves()






def displayUnitPlotList_Promo( self, screen, pLoopUnit, szString ):
	if (self.bShowPromotionIndicator):
		# can unit be promoted ?
		if (pLoopUnit.isPromotionReady()):
			# place the promotion frame
			szStringPromoFrame = szString+"PromoFrame"
			screen.show( szStringPromoFrame )

	return 0

def displayUnitPlotList_Upgrade( self, screen, pLoopUnit, szString, iCount, x, y ):
	if (self.bShowUpgradeIndicator):
		# can unit be upgraded ?
		if (mt.checkAnyUpgrade(pLoopUnit)):
			# place the upgrade arrow
			szStringUpgrade = szString+"Upgrade"
			szFileNameUpgrade = ArtFileMgr.getInterfaceArtInfo("OVERLAY_UPGRADE").getPath()	
			screen.addDDSGFC( szStringUpgrade, szFileNameUpgrade, x+2, y+14, 8, 16, WidgetTypes.WIDGET_GENERAL, iCount, -1 )
			screen.show( szStringUpgrade )

	return 0

def displayUnitPlotList_HealthBar( self, screen, pLoopUnit, szString ):
	if (self.bShowHealthBar and pLoopUnit.maxHitPoints()
	and not (pLoopUnit.isFighting() and self.bHideHealthBarWhileFighting)):
		# place the health bar
		szStringHealthBar = szString+"HealthBar"
		screen.setBarPercentage( szStringHealthBar, InfoBarTypes.INFOBAR_STORED, float( pLoopUnit.currHitPoints() ) / float( pLoopUnit.maxHitPoints() ) )
		screen.setBarPercentage( szStringHealthBar, InfoBarTypes.INFOBAR_RATE, float(1.0) )
		screen.show( szStringHealthBar )

	return 0

def displayUnitPlotList_MoveBar( self, screen, pLoopUnit, szString ):
	if (self.bShowMoveBar):
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

	return 0

def displayUnitPlotList_Mission( self, screen, pLoopUnit, szString, iCount, x, y, iSize ):
	# display the mission or activity info
	if (self.bShowMissionInfo): 
		# TODO: Switch to UnitUtil.getOrder()
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
			eMissionType = pLoopUnit.getGroup().getMissionType(0)
			# is the mission to build an improvement
			if (eMissionType == MissionTypes.MISSION_BUILD):
				szFileNameAction = ArtFileMgr.getInterfaceArtInfo("OVERLAY_ACTION_BUILD").getPath()
			# is the mission a "move to" mission
			elif (eMissionType in UnitUtil.MOVE_TO_MISSIONS):
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
			screen.addDDSGFC( szStringActionIcon, szFileNameAction, x+20, y+20, iSize, iSize, WidgetTypes.WIDGET_GENERAL, iCount, -1 )
			screen.show( szStringActionIcon )

	return 0

def getArt(sArt):
	return ArtFileMgr.getInterfaceArtInfo(sArt).getPath()

















#		UnitPlots = []
#		for i in range(vCols * vRows):
#			UnitPlots.append(UnitPlot(sBupPanel, i, _getx(i), _gety(i)))

#	def _getx(self, iIndex):
#		_col = iIndex % iCols
#		return _col - 1

#	def _gety(self, iIndex):
#		_row = iIndex / iCols
#		return iRows - irow

#	def _getIndex(self, x, y):
#		return (iRows - y) * iCols + x - 1
