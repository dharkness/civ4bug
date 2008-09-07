## TradeUtil
##
## Utilities for dealing with Trades and Deals.
##
##   formatTrade(player or ID, TradeData(s))
##     Returns a plain text description of the given tradeable item(s).
##
##   formatDeal(CyDeal)
##     Returns a plain text description of the given deal.
##
##   findDealsByPlayerAndType(player ID, type(s))
##     Returns a data structure holding the deals for a player that match the types.
##     This should only be used with symmetrically tradeable types like open borders.
##
##   playerDeals(player ID)
##     Used to iterate over all deals that the player participates in.
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

## TradeData Formatting

def formatTrade(player, trade):
	"""Returns a single string containing all of the trade items separated by commas.
	
	player can be either an ID or CyPlayer and is needed when a city is being traded.
	"""
	if isinstance(trade, list) or isinstance(trade, tuple) or isinstance(trade, set):
		return ", ".join([formatTrade(player, t) for t in trade])
	elif trade.ItemType in TRADE_FORMATS:
		return TRADE_FORMATS[trade.ItemType].format(player, trade)
	else:
		BugUtil.debug("WARN: unknown item type %d" % trade.ItemType)
		return ""

TRADE_FORMATS = {}

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


# Functions for use as argsFunction: converting TradeData.iData into
# whatever you want to display in the formatted string.

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
	BugUtil.debug("TradeUtil - peace treaty has iData %d" % trade.iData)
	return BugUtil.getText("TXT_KEY_TRADE_PEACE_TREATY_STRING", (gc.getDefineINT("PEACE_TREATY_LENGTH"),))


# Classes for Formatting TradeData

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


# Testing

def makeTrade(type, value=-1):
	trade = TradeData()
	trade.ItemType = TradeableItems(type)
	if value != -1:
		trade.iData = value
	return trade

def testTrade(player, type, value):
	print formatTrade(player, makeTrade(type, value))

def testAllTrades():
	for i in TRADE_FORMATS.keys():
		testTrade(2, i, 1)

def testTradeList():
	print formatTrade(2, [
		makeTrade(TradeableItems.TRADE_GOLD, 53),
		makeTrade(TradeableItems.TRADE_MAPS),
		makeTrade(TradeableItems.TRADE_PEACE, 1),
		makeTrade(TradeableItems.TRADE_CITY, 1),
		makeTrade(TradeableItems.TRADE_GOLD_PER_TURN, 6),
	])


## Deals

def playerDeals(ePlayer):
	"""Generates an iterator of all PlayerDeals in which ePlayer takes part.
	
	PlayerDeal.getPlayer() always returns ePlayer.
	
	# print all open borders deals for active player
	ePlayer = gc.getGame().getActivePlayer()
	for deal in TradeUtil.playerDeals(ePlayer):
		if deal.hasType(TradeableItems.TRADE_OPEN_BORDERS):
			print deal
	"""
	if ePlayer is not None and ePlayer != -1:
		game = gc.getGame()
		for i in range(game.getIndexAfterLastDeal()):
			deal = game.getDeal(i)
			if not deal.isNone():
				if deal.getFirstPlayer() == ePlayer:
					yield Deal(deal)
				if deal.getSecondPlayer() == ePlayer:
					yield ReversedDeal(deal)

def findDealsByPlayerAndType(ePlayer, types):
	"""Returns PlayerDeals in which ePlayer takes part and that match
	one of the given types.
	
	This function only works with symmetric TradeableItem types (OB, DP, PA, PT).
	The returned dictionary maps each unique player ID to a dictionary that
	maps TradeableItem (from types) to PlayerDeal. Only players with at least
	one matching deal get added to the dictionary.
	
	Each deal can be mapped to multiple types, but each type will have at most
	one deal mapped to it per player. This is because you cannot trade open borders
	to the same player in two or more deals.
	"""
	timer = BugUtil.Timer("findDealsByPlayerAndType")
	if isinstance(types, int):
		types = (types,)
	found = {}
	for deal in playerDeals(ePlayer):
		matches = deal.findTypes(types)
		for type in matches:
			found.setdefault(deal.getOtherPlayer(), {})[type] = deal
	timer.log()
	return found


# Deal Wrapper Classes

class Deal(object):
	"""Wraps a CyDeal where either the first or second player is the focus.
	
	All CyDeal functions are provided either directly or mapped to basic and
	'Other' versions. In the main class, the basic functions map to the 'First'
	functions and the 'Other' functions map to 'Second' functions. This is reversed
	in the ReversedDeal subclass.
	
	For example, normally getCount() returns getLengthFirstTrades() and
	getOtherCount() returns getLengthSecondTrades(). The same method applies to
	getPlayer() and getTrade().
	
	hasType() and hasAnyType() search only the focused player's TradeData.ItemType,
	so they work only for symmetric TradeableItems (peace treaty, open borders, 
	and defensive pact).
	"""
	def __init__(self, deal):
		self.deal = deal
	def getID(self):
		return self.deal.getID()
	def isNone(self):
		return self.deal.isNone()
	def getInitialGameTurn(self):
		return self.deal.getInitialGameTurn()
	def kill(self):
		self.deal.kill()
	
	def isReversed(self):
		return False
	def getPlayer(self):
		return self.deal.getFirstPlayer()
	def getOtherPlayer(self):
		return self.deal.getSecondPlayer()
	def getCount(self):
		return self.deal.getLengthFirstTrades()
	def getOtherCount(self):
		return self.deal.getLengthSecondTrades()
	def getTrade(self, index):
		return self.deal.getFirstTrade(index)
	def getOtherTrade(self, index):
		return self.deal.getSecondTrade(index)
	
	def trades(self):
		for i in range(self.getCount()):
			yield self.getTrade(i)
	def otherTrades(self):
		for i in range(self.getOtherCount()):
			yield self.getOtherTrade(i)
	def hasType(self, type):
		return self.hasAnyType((type,))
	def hasAnyType(self, types):
		for trade in self.trades():
			if trade.ItemType in types:
				return True
		return False
	def findTypes(self, types):
		found = []
		for trade in self.trades():
			for type in types:
				if type == trade.ItemType:
					found.append(type)
		return found
	
	def __repr__(self):
		return ("<deal %d [trades %d %s] [trades %d %s]>" % 
				(self.getID(), 
				self.getPlayer(), 
				formatTrade(self.getPlayer(), [t for t in self.trades()]), 
				self.getOtherPlayer(), 
				formatTrade(self.getOtherPlayer(), [t for t in self.otherTrades()])))

class ReversedDeal(Deal):
	"""A Deal where the basic and 'Other' functions are reversed."""
	def __init__(self, deal):
		super(ReversedDeal, self).__init__(deal)
	def isReversed(self):
		return True
	def getPlayer(self):
		return self.deal.getSecondPlayer()
	def getOtherPlayer(self):
		return self.deal.getFirstPlayer()
	def getCount(self):
		return self.deal.getLengthSecondTrades()
	def getOtherCount(self):
		return self.deal.getLengthFirstTrades()
	def getTrade(self, index):
		return self.deal.getSecondTrade(index)
	def getOtherTrade(self, index):
		return self.deal.getFirstTrade(index)


# Testing

def testDeals():
	allDeals = findDealsByPlayerAndType(0, 
			(
				TradeableItems.TRADE_PEACE_TREATY,
				TradeableItems.TRADE_OPEN_BORDERS,
				TradeableItems.TRADE_DEFENSIVE_PACT,
				TradeableItems.TRADE_RESOURCES,
				TradeableItems.TRADE_GOLD_PER_TURN,
			))
	for player, deals in allDeals.iteritems():
		print PlayerUtil.getPlayer(player).getName()
		for type, deal in deals.iteritems():
			print "%s: %r" % (TRADE_FORMATS[type].name, deal)
