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
		self.sBupPanel = sBupStringBase + "BackgroundPanel"

		BugUtil.debug("BupPanel %s %i %i %i %i", self.sBupPanel, self.xPanel, self.yPanel, self.wPanel, self.hPanel)

#		screen.addPanel(sBupPanel, u"", u"", True, False, _x, _y, _w, _h, PanelStyles.PANEL_STYLE_EMPTY)
		self.screen.addPanel(self.sBupPanel, u"", u"", True, False, self.xPanel, self.yPanel, self.wPanel, self.hPanel, PanelStyles.PANEL_STYLE_MAIN)
		self.screen.hide(self.sBupPanel)

		sTexture = ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_GOVERNOR").getPath()
		sHiLiteTexture = ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath()
		for iIndex in range(self.MaxCells):
			szBupCell = self._getCellWidget(iIndex)
			iX = self._getX(self._getCol(iIndex))
			iY = self._getY(self._getRow(iIndex))

			BugUtil.debug("BupPanel MaxCells %i %i %i %i %i", iIndex, self._getCol(iIndex), self._getRow(iIndex), self._getX(self._getCol(iIndex)), self._getY(self._getRow(iIndex)))


#			screen.addCheckBoxGFCAt(szStringPanel, szString, ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_GOVERNOR").getPath(), ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(), xOffset + 3, 3, 32, 32, WidgetTypes.WIDGET_PLOT_LIST, k, -1, ButtonStyles.BUTTON_STYLE_LABEL, True )
			screen.addCheckBoxGFCAt(self.sBupPanel, szBupCell, sTexture, sHiLiteTexture, iX, iY, 32, 32, WidgetTypes.WIDGET_PLOT_LIST, iIndex, -1, ButtonStyles.BUTTON_STYLE_LABEL, True)
			screen.hide(szBupCell)

#			screen.attachCheckBoxGFC(self.sBupPanel, szBupCell, sTexture, sHiLiteTexture, 32, 32, WidgetTypes.WIDGET_PLOT_LIST, iIndex, -1, ButtonStyles.BUTTON_STYLE_LABEL)

#VOID attachCheckBoxGFC(STRING szAttachTo, STRING szName, STRING szTexture, STRING szHiliteTexture, INT iWidth, INT iHeight, WidgetType eWidgetType, INT iData1, INT iData2, ButtonStyle eStyle)
#VOID addCheckBoxGFC(STRING szName, STRING szTexture, STRING szHiliteTexture, INT iX, INT iY, INT iWidth, INT iHeight, WidgetType eWidgetType, INT iData1, INT iData2, ButtonStyle eStyle)
#VOID addCheckBoxGFCAt(STRING szName, STRING szTexture, STRING szHiliteTexture, INT iX, INT iY, INT iWidth, INT iHeight, WidgetType eWidgetType, INT iData1, INT iData2, ButtonStyle eStyle)




		self.sFileNamePromo = ArtFileMgr.getInterfaceArtInfo("OVERLAY_PROMOTION_FRAME").getPath()
		self.iLeaderPromo = gc.getInfoTypeForString('PROMOTION_LEADER')
		self.BupUnits = []

#	def setCellSpacing(self, iSpacing):
#		self.BupCellSpacing = iSpacing

	def Draw(self):
		self.screen.show(self.sBupPanel)

		iIndex = 0
		for pBupUnit in self.BupUnits:
			szBupCell = self._getCellWidget(iIndex)
			self.screen.changeImageButton(szBupCell, gc.getUnitInfo(pBupUnit.pUnit.getUnitType()).getButton())
			self.screen.enable(szBupCell, pBupUnit.pUnit.getOwner() == gc.getGame().getActivePlayer())
			self.screen.setState(szBupCell, pBupUnit.pUnit.IsSelected())
			self.screen.show(szBupCell)
			iIndex += 1

		while iIndex <= self.MaxCells:
			szBupCell = self._getCellWidget(iIndex)
			self.screen.hide(szBupCell)
			iIndex += 1


#					szString = "PlotListButton" + str(iCount)
#					screen.changeImageButton( szString, gc.getUnitInfo(pLoopUnit.getUnitType()).getButton() )
#					if ( pLoopUnit.getOwner() == gc.getGame().getActivePlayer() ):
#						bEnable = True
#					else:
#						bEnable = False
#					screen.enable(szString, bEnable)

#					if (pLoopUnit.IsSelected()):
#						screen.setState(szString, True)
#					else:
#						screen.setState(szString, False)
#					screen.show( szString )




	def Hide(self):
		self.screen.hide(self.sBupPanel)

	def addUnit(self, pUnit):
		self.BupUnits.append(BupUnit(pUnit))

	def flushUnits(self):
		self.BupUnits = []




	def _getMaxCols(self):
		return self.Cols

	def _getMaxRows(self):
		return self.Rows

	def _getRow(self, i):
		return i / self._getMaxCols()

	def _getCol(self, i):
		return i % self._getMaxCols()

	def _getX(self, nCol):
		return nCol * cBupCellSize

	def _getY(self, nRow):
		return nRow * cBupCellSize

	def _getCellWidget(self, index):
		return sBupStringBase + "BackgroundCell" + str(index)

#	def _getIndex(self, nRow, nCol):
#		return ( nRow * self.getMaxCol() ) + ( nCol % self.getMaxCol() )

############## functions for visual objects (show and hide) ######################
		
	# PLE Grouping Mode Switcher 















































class BupUnit:
	def __init__(self, pUnit):
		self.pUnit = pUnit
		self.bSelected = pUnit.IsSelected()
		self.eUnit = pUnit.getUnitType()
#		self.sDotState, self.iDotxSize, self.iDotySize, self.iDotxOffset, self.iDotyOffset = _getDOTInfo(pUnit)
#		self.sMission = _getMission(pUnit)
		self.bPromo = pUnit.isPromotionReady()
		self.bGG = iLeaderPromo != -1 and pUnit.isHasPromotion(iLeaderPromo)
#		self.bUpgrade = mt.checkAnyUpgrade(pUnit)
		self.icurrHitPoints = pUnit.currHitPoints()
		self.imaxHitPoints = pUnit.maxHitPoints()
		self.iMovesLeft = pUnit.movesLeft()
		self.iMoves = pUnit.getMoves()





















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
