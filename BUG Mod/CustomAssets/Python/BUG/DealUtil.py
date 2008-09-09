## DealUtil
##
## Utilities for dealing with Deals.
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
##   - Add 'gameUpdate' event for onGameUpdate()
##   - Defines new 'DealCanceled' event
##
## Copyright (c) 2008 The BUG Mod.
##
## Author: EmperorFool

from CvPythonExtensions import *
import CvEventInterface
import BugUtil
import PlayerUtil

gc = CyGlobalContext()

g_eventManager = None
g_lastDealCount = 0

## Deal Functions

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


## Initialization and Events

def addEvents(eventManager):
	"""Defines a new 'DealCanceled' event."""
	global g_eventManager
	g_eventManager = eventManager
	g_eventManager.addEvent("DealCanceled")

def onGameUpdate(argsList):
	"""
	Fires 'DealCanceled' event during update event if the number of deals
	is less than it was during the previous call.
	"""
	global g_lastDealCount
	count = gc.getGame().getNumDeals()
	if count < g_lastDealCount:
		g_eventManager.fireEvent('DealCanceled')
		g_lastDealCount = count


## Wrapper Classes

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


## Testing

def test():
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