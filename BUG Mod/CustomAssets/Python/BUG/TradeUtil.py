## TradeUtil
##
## Utilities for dealing with Trades and TradeData.
##
##   format(player or ID, TradeData(s))
##     Returns a plain text description of the given tradeable item(s).
##
##   Trade class
##     Can be used to create new trades.
##     (not really since implementDeal() not exposed to Python)
##
## Notes
##   - Must be initialized externally by calling init()
##
## Copyright (c) 2008 The BUG Mod.
##
## Author: EmperorFool

from CvPythonExtensions import *
import BugUtil
import PlayerUtil

gc = CyGlobalContext()

TRADE_FORMATS = {}


## Trade Class

class Trade(object):
	"""
	Encapsulates the player IDs and TradeData for a new or proposed trade.
	
	Implements the same interface as the DealUtil.Deal class.
	"""
	def __init__(self, ePlayer, eOtherPlayer):
		self.ePlayer = ePlayer
		self.eOtherPlayer = eOtherPlayer
		self.tradeList = []
		self.otherTradeList = []
	
	def isReversed(self):
		return False
	def getPlayer(self):
		return self.ePlayer
	def getOtherPlayer(self):
		return self.eOtherPlayer
	
	def getCount(self):
		return len(self.tradeList)
	def getOtherCount(self):
		return len(self.otherTradeList)
	def getTrade(self, index):
		return self.tradeList[index]
	def getOtherTrade(self, index):
		return self.otherTradeList[index]
	def trades(self):
		return self.tradeList
	def otherTrades(self):
		return self.otherTradeList
	
	def addTrade(self, trade):
		self.tradeList.append(trade)
	def addOtherTrade(self, trade):
		self.otherTradeList.append(trade)
	
	def hasType(self, type):
		return self.hasAnyType((type,))
	def hasAnyType(self, types):
		for trade in self.trades():
			if trade.ItemType in types:
				return True
		for trade in self.otherTrades():
			if trade.ItemType in types:
				return True
		return False
	def findType(self, type):
		return self.findTypes((type,))
	def findTypes(self, types):
		found = []
		for trade in self.trades():
			for type in types:
				if type == trade.ItemType:
					found.append(trade)
		for trade in self.otherTrades():
			for type in types:
				if type == trade.ItemType:
					found.append(trade)
		return found
	
	def __repr__(self):
		return ("<trade %d [%s] for %d [%s]>" % 
				(self.getPlayer(), 
				format(self.getPlayer(), self.trades()), 
				self.getOtherPlayer(), 
				format(self.getOtherPlayer(), self.otherTrades())))


## TradeData Formatting

def format(player, trade):
	"""Returns a single string containing all of the trade items separated by commas.
	
	player can be either an ID or CyPlayer and is needed when a city is being traded.
	"""
	if isinstance(trade, list) or isinstance(trade, tuple) or isinstance(trade, set):
		return ", ".join([format(player, t) for t in trade])
	elif trade.ItemType in TRADE_FORMATS:
		return TRADE_FORMATS[trade.ItemType].format(player, trade)
	else:
		BugUtil.warn("TradeUtil - unknown item type %d", trade.ItemType)
		return ""

def init():
	"""Performs one-time initialization after the game starts up."""
	addSimpleTrade("gold", TradeableItems.TRADE_GOLD, "TXT_KEY_TRADE_GOLD_NUM")
	addSimpleTrade("gold per turn", TradeableItems.TRADE_GOLD_PER_TURN, "TXT_KEY_TRADE_GOLD_PER_TURN_NUM")
	addPlainTrade("map", TradeableItems.TRADE_MAPS, "TXT_KEY_TRADE_WORLD_MAP_STRING")
	addPlainTrade("vassal", TradeableItems.TRADE_VASSAL, "TXT_KEY_TRADE_VASSAL_TREATY_STRING")
	addPlainTrade("capitulation", TradeableItems.TRADE_SURRENDER, "TXT_KEY_TRADE_CAPITULATE_STRING")
	addPlainTrade("open borders", TradeableItems.TRADE_OPEN_BORDERS, "TXT_KEY_TRADE_OPEN_BORDERS_STRING")
	addPlainTrade("defensive pact", TradeableItems.TRADE_DEFENSIVE_PACT, "TXT_KEY_TRADE_DEFENSIVE_PACT_STRING")
	addPlainTrade("alliance", TradeableItems.TRADE_PERMANENT_ALLIANCE, "TXT_KEY_TRADE_PERMANENT_ALLIANCE_STRING")
	addComplexTrade("peace treaty", TradeableItems.TRADE_PEACE_TREATY, getTradePeaceDeal)
	addComplexTrade("technology", TradeableItems.TRADE_TECHNOLOGIES, getTradeTech)
	addComplexTrade("resource", TradeableItems.TRADE_RESOURCES, getTradeBonus)
	addComplexTrade("city", TradeableItems.TRADE_CITIES, getTradeCity)
	addAppendingTrade("peace", TradeableItems.TRADE_PEACE, "TXT_KEY_TRADE_PEACE_WITH", getTradePlayer)
	addAppendingTrade("war", TradeableItems.TRADE_WAR, "TXT_KEY_TRADE_WAR_WITH", getTradePlayer)
	addAppendingTrade("trade embargo", TradeableItems.TRADE_EMBARGO, "TXT_KEY_TRADE_STOP_TRADING_WITH", getTradePlayer, " %s")
	addAppendingTrade("civic", TradeableItems.TRADE_CIVIC, "TXT_KEY_TRADE_ADOPT", getTradeCivic)
	addAppendingTrade("religion", TradeableItems.TRADE_RELIGION, "TXT_KEY_TRADE_CONVERT", getTradeReligion)

def addPlainTrade(name, type, key):
	"""Creates a trade using an unparameterized XML <text> tag."""
	return addTrade(type, PlainTradeFormat(name, type, key))

def addSimpleTrade(name, type, key):
	"""Creates a trade using an XML <text> tag with a int placeholder for iData."""
	return addTrade(type, SimpleTradeFormat(name, type, key))

def addAppendingTrade(name, type, key, argsFunction, text="%s"):
	"""Creates a trade using an XML <text> tag with a single appended string placeholder."""
	format = addTrade(type, AppendingTradeFormat(name, type, key, text))
	if argsFunction is not None:
		format.getParameters = lambda player, trade: argsFunction(player, trade)
	return format

def addComplexTrade(name, type, argsFunction, textFunction=None):
	"""Creates a trade using an XML <text> tag with any number of placeholders."""
	format = addTrade(type, ComplexTradeFormat(name, type))
	if argsFunction is not None:
		format.getParameters = lambda player, trade: argsFunction(player, trade)
	if textFunction is not None:
		format.getText = lambda player, trade: textFunction(player, trade)
	return format

def addTrade(type, format):
	TRADE_FORMATS[type] = format
	return format


## Functions for use as argsFunction: converting TradeData.iData into
## whatever you want to display in the formatted string.

def getTradeTech(player, trade):
	return gc.getTechInfo(trade.iData).getDescription()

def getTradeBonus(player, trade):
	return gc.getBonusInfo(trade.iData).getDescription()

def getTradeCity(player, trade):
	return PlayerUtil.getPlayer(player).getCity(trade.iData).getName()

def getTradeCivic(player, trade):
	return gc.getCivicInfo(trade.iData).getDescription()

def getTradeReligion(player, trade):
	return gc.getReligionInfo(trade.iData).getDescription()

def getTradePlayer(player, trade):
	return PlayerUtil.getPlayer(trade.iData).getName()

def getTradePeaceDeal(player, trade):
	BugUtil.debug("TradeUtil - peace treaty has iData %d", trade.iData)
	return BugUtil.getText("TXT_KEY_TRADE_PEACE_TREATY_STRING", (gc.getDefineINT("PEACE_TREATY_LENGTH"),))


## Classes for Formatting TradeData

class BaseTradeFormat(object):
	def __init__(self, name, type):
		self.name = name
		self.type = type
	def format(self, player, trade):
		pass

class PlainTradeFormat(BaseTradeFormat):
	def __init__(self, name, type, key):
		super(PlainTradeFormat, self).__init__(name, type)
		self.key = key
	def format(self, player, trade):
		return BugUtil.getPlainText(self.key)

class SimpleTradeFormat(BaseTradeFormat):
	def __init__(self, name, type, key):
		super(SimpleTradeFormat, self).__init__(name, type)
		self.key = key
	def format(self, player, trade):
		return BugUtil.getText(self.key, (self.getParameters(player, trade),))
	def getParameters(self, player, trade):
		return trade.iData

class AppendingTradeFormat(BaseTradeFormat):
	def __init__(self, name, type, key, text="%s"):
		super(AppendingTradeFormat, self).__init__(name, type)
		self.key = key
		self.text = text
	def format(self, player, trade):
		return self.getText(player, trade) % (self.getParameters(player, trade),)
	def getText(self, player, trade):
		return BugUtil.getPlainText(self.key) + self.text
	def getParameters(self, player, trade):
		return trade.iData

class ComplexTradeFormat(BaseTradeFormat):
	def __init__(self, name, type):
		super(ComplexTradeFormat, self).__init__(name, type)
	def format(self, player, trade):
		return self.getText(player, trade) % (self.getParameters(player, trade),)
	def getText(self, player, trade):
		return "%s"
	def getParameters(self, player, trade):
		return trade.iData


## Testing

def makeTrade(type, value=-1):
	trade = TradeData()
	trade.ItemType = TradeableItems(type)
	if value != -1:
		trade.iData = value
	return trade

def test(player, type, value):
	print format(player, makeTrade(type, value))

def testAll():
	for i in TRADE_FORMATS.keys():
		test(2, i, 1)

def testList():
	print format(2, [
		makeTrade(TradeableItems.TRADE_GOLD, 53),
		makeTrade(TradeableItems.TRADE_MAPS),
		makeTrade(TradeableItems.TRADE_PEACE, 1),
		makeTrade(TradeableItems.TRADE_CITY, 1),
		makeTrade(TradeableItems.TRADE_GOLD_PER_TURN, 6),
	])
