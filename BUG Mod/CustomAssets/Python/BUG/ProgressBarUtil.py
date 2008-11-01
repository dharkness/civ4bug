## Progress Bar Utilities
##
## Holds the information used to display tick marks on progress bars
## Also draws the tick marks
##
## Copyright (c) 2007-2008 The BUG Mod.
##
## Author: Ruff_Hi

from CvPythonExtensions import *
import BugUtil
import CvUtil

# Globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
SOLID_MARKS = 0
TICK_MARKS = 1

# Constants
#BG = ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTON_NULL").getPath()

class ProgressBar:
	def __init__(self, id, x, y, w, h, color, marks):
		self.id = id
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.color = color
		self.marks = marks

		self.BG = ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTON_NULL").getPath()

		if self.marks == TICK_MARKS:
			self.m_y1 = 4
			self.m_y2 = 4 + (self.h - 8) / 3
			self.m_y3 = 5 + 2 * (self.h - 8) / 3
			self.m_y4 = self.h - 4
		else:
			self.m_y1 = 4
			self.m_y2 = self.h - 4
			self.m_y3 = -1
			self.m_y4 = -1

		self.line_cnt = 0
		self.bVisible = False

	def _setLineCount(self, i):
		self.line_cnt = i

	def _resetLineCount(self):
		self.line_cnt = 0

	def _getNextLineName(self):
		self.line_cnt += 1
		return self.id + "-Tick-" + str(self.line_cnt - 1)

	def _setVisible(self, bValue):
		self.bVisible = bValue

	def _deleteCanvas(self, screen):
		if self.bVisible:
			screen.deleteWidget(self.id)
			self._resetLineCount()
			self._setVisible(False)


	def hide(self, screen):
		screen.hide(self.id)

	def drawTickMarks(self, screen, iCurr, iTotal, iRate):
		if iRate <= 0:
			return

		self._deleteCanvas(screen)

		screen.addDrawControl(self.id, self.BG, self.x, self.y, self.w, self.h, WidgetTypes.WIDGET_GENERAL, -1, -1)
		self._setVisible(True)

		i = 0
		iXPrev = self.w * (iCurr + iRate) / iTotal
		while True:
			iX = self.w * (iCurr + (2 + i) * iRate) / iTotal

			if (iX > self.w
			or  iX - iXPrev < 5): break

			screen.addLineGFC(self.id, self._getNextLineName(), iX, self.m_y1, iX, self.m_y2, self.color)
			if self.marks == TICK_MARKS:
				screen.addLineGFC(self.id, self._getNextLineName(), iX, self.m_y3, iX, self.m_y4, self.color)

			i += 1
			iXPrev = iX
