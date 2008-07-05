## RawYields
##
## Calculates the raw yields of food, production and commerce for a city
## and displays them in the trade table when enabled.
##
## Copyright (c) 2008 BUG Mod.

from CvPythonExtensions import *
import CvUtil

gc = CyGlobalContext()
localText = CyTranslator()

# Types
WORKED_TILES = 0
CITY_TILES = 1
OWNED_TILES = 2
ALL_TILES = 3

BUILDINGS = 4
TRADE = 5
SPECIALISTS = 6
CORPORATIONS = 7
MULTIPLIERS = 8    # Holds the percent, not the yield value

NUM_TYPES = 9

# Yields
YIELDS = (YieldTypes.YIELD_FOOD, YieldTypes.YIELD_PRODUCTION, YieldTypes.YIELD_COMMERCE)

# Tiles
TILES = (WORKED_TILES, CITY_TILES, OWNED_TILES, ALL_TILES)

# Table
HEADING_COLUMN = 0
VALUE_COLUMN = 1

class Tracker:
	
	def __init__(self):
		"Creates a table to hold all of the tracked values for each yield type."
		self.values = {}
		for eYield in range(YieldTypes.NUM_YIELD_TYPES):
			self.values[eYield] = {}
			for eType in range(NUM_TYPES):
				self.values[eYield][eType] = 0
	
	
	def getYield(self, eYield, eType):
		return self.values[eYield][eType]
	
	def _addYield(self, eYield, eType, iValue):
		"Adds the given yield value to the given type in the table."
		self.values[eYield][eType] += iValue
	
	
	def addBuilding(self, eYield, iValue):
		self._addYield(eYield, BUILDINGS, iValue)
	
	def addTrade(self, iValue):
		self._addYield(YieldTypes.YIELD_COMMERCE, TRADE, iValue)
	
	def processCity(self, pCity):
		"""
		Calculates the yields for the given city's tiles, specialists, corporations and multipliers.
		The building and trade yields are calculated by CvMainInterface.
		"""
		self.calculateTiles(pCity)
		self.calculateSpecialists(pCity)
		self.calculateCorporations(pCity)
		self.calculateMultipliers(pCity)
	
	def calculateTiles(self, pCity):
		"Calculates the yields for all tiles of the given CyCity."
		for i in range(gc.getNUM_CITY_PLOTS()):
			pPlot = pCity.getCityIndexPlot(i)
			if pPlot and not pPlot.isNone() and pPlot.hasYield():
				if pCity.isWorkingPlot(pPlot):
					self._addTile(WORKED_TILES, pPlot)
				elif pCity.canWork(pPlot):
					self._addTile(CITY_TILES, pPlot)
				elif pPlot.getOwner() == pCity.getOwner():
					self._addTile(OWNED_TILES, pPlot)
				else:
					self._addTile(ALL_TILES, pPlot)
	
	def _addTile(self, eFirstTileType, pPlot):
		for eYield in YIELDS:
			iValue = pPlot.getYield(eYield)
			for eType in range(eFirstTileType, ALL_TILES + 1):
				self._addYield(eYield, eType, iValue)
	
	def calculateSpecialists(self, pCity):
		pPlayer = gc.getPlayer(pCity.getOwner())
		for eYield in range(YieldTypes.NUM_YIELD_TYPES):
			iValue = 0
			for eSpec in range(gc.getNumSpecialistInfos()):
				iValue += pPlayer.specialistYield(eSpec, eYield) * (pCity.getSpecialistCount(eSpec) + pCity.getFreeSpecialistCount(eSpec))
			self.addSpecialist(eYield, iValue)
	
	def addSpecialist(self, eYield, iValue):
		self._addYield(eYield, SPECIALISTS, iValue)
		
	def calculateCorporations(self, pCity):
		for eYield in range(YieldTypes.NUM_YIELD_TYPES):
			iValue = 0
			for eCorp in range(gc.getNumCorporationInfos()):
				if (pCity.isHasCorporation(eCorp)):
					iValue += pCity.getCorporationYieldByCorporation(eYield, eCorp)
			self.addCorporation(eYield, iValue)
	
	def addCorporation(self, eYield, iValue):
		self._addYield(eYield, CORPORATIONS, iValue)
	
	def calculateMultipliers(self, pCity):
		for eYield in range(YieldTypes.NUM_YIELD_TYPES):
			iValue = pCity.getBaseYieldRateModifier(eYield, 0)
			self.addMultiplier(eYield, iValue)
	
	def addMultiplier(self, eYield, iPercent):
		self._addYield(eYield, MULTIPLIERS, iPercent)
	
	
	def fillTable(self, screen, table, eYield, eTileType):
		"Fills the given GFC table control with the chosen yield values."
		self.iRow = 0
		# Tiles
		iTotal = self.getYield(eYield, eTileType)
		self.appendTable(screen, table, False, "Tiles", eYield, iTotal)
		
		# Other types
		for eType in range(BUILDINGS, MULTIPLIERS):
			iValue = self.getYield(eYield, eType)
			if iValue != 0:
				iTotal += iValue
				self.appendTable(screen, table, False, "Value", eYield, iValue)
		
		# Subtotal and Multipliers if not 100%
		iPercent = self.getYield(eYield, MULTIPLIERS)
		if iPercent > 100:
			# Subtotal
			self.appendTable(screen, table, True, "Subtotal", eYield, iTotal)
			# Multipliers
			iMultipliers = (iTotal * iPercent // 100) - iTotal
			iTotal += iMultipliers
			self.appendTable(screen, table, False, "Multipliers", eYield, iMultipliers)
		
		# Total
		self.appendTable(screen, table, True, "Total", eYield, iTotal)
	
	def appendTable(self, screen, table, bTotal, heading, eYield, iValue):
		"""
		Appends the given yield value to the table control.
		If bTotal is True, the heading is colored yellow and there's no + sign on the value.
		"""
		cYield = gc.getYieldInfo(eYield).getChar()
		screen.appendTableRow(table)
		if bTotal:
			heading = u"<color=205,180,55,255>%s</color>" % heading
			value = u"<color=205,180,55,255>%d</color>" % iValue
		else:
			value = u"%+d" % iValue
		screen.setTableText(table, HEADING_COLUMN, self.iRow, u"<font=1>%s</font>" % (heading), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setTableText(table, VALUE_COLUMN, self.iRow, u"<font=1>%s%c</font>" % (value, cYield), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
		self.iRow += 1
