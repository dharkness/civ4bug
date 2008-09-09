## DiplomacyUtil
##
## Utilities for handling and dispatching Diplomacy events and acquiring
## proposed trades from the (unmoddable) CyDiplomacy screen.
##
## TODO: switch to init()
##
## Notes
##   - Must be initialized externally by calling addEvents(eventManager)
##
## Copyright (c) 2008 The BUG Mod.
##
## Author: EmperorFool

from CvPythonExtensions import *
import BugUtil
import PlayerUtil
import TradeUtil

MAX_TRADE_DATA = 50  # avoid an infinite loop

gc = CyGlobalContext()
diplo = CyDiplomacy()

# comment-type -> ( event-type , trade-type )
g_eventsByCommentType = {}
g_eventManager = None


## Event Initialization

def addEvents(eventManager):
	"""Adds the diplomacy events to BugEventManager."""
	global g_eventManager
	g_eventManager = eventManager
	
	# Trade
	DiploEvent("AI_DIPLOCOMMENT_OFFER_DEAL", "DealOffered", sendTrade=True)
	DiploEvent("AI_DIPLOCOMMENT_CANCEL_DEAL", "DealCanceled", sendTrade=True)
	DiploEvent("USER_DIPLOCOMMENT_ACCEPT_OFFER", "DealAccepted", sendTrade=True)
	DiploEvent("USER_DIPLOCOMMENT_REJECT_OFFER", "DealRejected", sendTrade=True)
	
	# Free Stuff
	DiploEvent("AI_DIPLOCOMMENT_OFFER_CITY", "CityOffered", tradeType=TradeableItems.TRADE_CITIES)
	DiploEvent("AI_DIPLOCOMMENT_GIVE_HELP", "HelpOffered", sendTrade=True)
	DiploEvent("AI_DIPLOCOMMENT_OFFER_PEACE", "PeaceOffered")
	DiploEvent("AI_DIPLOCOMMENT_OFFER_VASSAL", "VassalOffered")
	
	# Ask for Help
	DiploEvent("AI_DIPLOCOMMENT_ASK_FOR_HELP", "HelpDemanded", sendTrade=True)
	DiploEvent("USER_DIPLOCOMMENT_GIVE_HELP", "HelpAccepted", sendTrade=True)
	DiploEvent("USER_DIPLOCOMMENT_REFUSE_HELP", "HelpRejected", sendTrade=True)
	
	# Demand Tribute
	DiploEvent("AI_DIPLOCOMMENT_DEMAND_TRIBUTE", "TributeDemanded", sendTrade=True)
	DiploEvent("USER_DIPLOCOMMENT_ACCEPT_DEMAND", "TributeAccepted", sendTrade=True)
	DiploEvent("USER_DIPLOCOMMENT_REJECT_DEMAND", "TributeRejected", sendTrade=True)
	
	# Religion
	DiploEvent("AI_DIPLOCOMMENT_RELIGION_PRESSURE", "ReligionDemanded", onReligionDemanded, 
			argFunc=PlayerUtil.getStateReligion)
	DiploEvent("USER_DIPLOCOMMENT_CONVERT", "ReligionAccepted", onReligionAccepted, 
			argFunc=PlayerUtil.getStateReligion)
	DiploEvent("USER_DIPLOCOMMENT_NO_CONVERT", "ReligionRejected", onReligionRejected, 
			argFunc=PlayerUtil.getStateReligion)
	
	# Civic
	DiploEvent("AI_DIPLOCOMMENT_CIVIC_PRESSURE", "CivicDemanded", onCivicDemanded,
			argFunc=PlayerUtil.getFavoriteCivic)
	DiploEvent("USER_DIPLOCOMMENT_REVOLUTION", "CivicAccepted", onCivicAccepted,
			argFunc=PlayerUtil.getFavoriteCivic)
	DiploEvent("USER_DIPLOCOMMENT_NO_REVOLUTION", "CivicRejected", onCivicRejected,
			argFunc=PlayerUtil.getFavoriteCivic)
	
	# Join War
	DiploEvent("AI_DIPLOCOMMENT_JOIN_WAR", "WarDemanded", sendData=True)
	DiploEvent("USER_DIPLOCOMMENT_JOIN_WAR", "WarAccepted", sendData=True)
	DiploEvent("USER_DIPLOCOMMENT_NO_JOIN_WAR", "WarRejected", sendData=True)
	
	# Trade Embargo
	DiploEvent("AI_DIPLOCOMMENT_STOP_TRADING", "EmbargoDemanded", sendData=True)
	DiploEvent("USER_DIPLOCOMMENT_STOP_TRADING", "EmbargoAccepted", sendData=True)
	DiploEvent("USER_DIPLOCOMMENT_NO_STOP_TRADING", "EmbargoRejected", sendData=True)

class DiploEvent:
	def __init__(self, comment, event, handler=None, 
				 sendFromPlayer=True, sendToPlayer=True, 
				 sendData=False, sendArgs=False, argFunc=None, 
				 sendTrade=False, tradeType=None):
		self.comment = comment
		self.eComment = gc.getInfoTypeForString(comment)
		if self.eComment == -1:
			raise ConfigError("invalid comment type %s" % comment)
		self.event = event
		self.sendFromPlayer = sendFromPlayer
		self.sendToPlayer = sendToPlayer
		self.sendData = sendData
		self.sendArgs = sendArgs
		self.argFunc = argFunc
		self.sendTrade = sendTrade
		self.tradeType = tradeType
		if tradeType:
			BugUtil.debug("Diplomacy - mapped %s to %s with %s", 
					comment, event, str(tradeType))
		else:
			BugUtil.debug("Diplomacy - mapped %s to %s", comment, event)
		g_eventsByCommentType[self.eComment] = self
		g_eventManager.addEventHandler(event, handler)
	
	def dispatch(self, eFromPlayer, eToPlayer, args):
		data = diplo.getData()
		BugUtil.debug("Diplomacy - %s [%d] from %d to %d with %r",
				self.comment, data, eFromPlayer, eToPlayer, args)
		argList = []
		if self.sendFromPlayer:
			argList.append(eFromPlayer)
		if self.sendToPlayer:
			argList.append(eToPlayer)
		
		if self.sendData:
			argList.append(data)
		if self.sendArgs:
			argList.append(args)
		if self.argFunc:
			argList.append(self.argFunc(eFromPlayer))
		
		if self.sendTrade or self.tradeType:
			trade = getProposedTrade()
			if self.sendTrade:
				argList.append(trade)
			if self.tradeType:
				trades = trade.findType(self.tradeType)
				if trade and trades:
					iData = trades[0].iData
					BugUtil.debug("Diplomacy - firing %s with %s %d", 
							self.event, str(self.tradeType), iData)
					argList.append(iData)
				else:
					BugUtil.debug("Diplomacy - firing %s without %s", 
							self.event, str(self.tradeType))
					argList.append(-1)
#			else:
#				if self.sendTrade:
#					argList.append(Trade())
#				if self.tradeType:
#					BugUtil.debug("Diplomacy - firing %s with empty trade (no %s)", 
#							self.event, str(self.tradeType))
#					argList.append(-1)
#				else:
#					BugUtil.debug("Diplomacy - firing %s with empty trade", self.event)
		else:
			BugUtil.debug("Diplomacy - firing %s", self.event)
		g_eventManager.fireEvent(self.event, *argList)


## Event Dispatching

def handleAIComment(eComment, args):
	dispatchEvent(eComment, diplo.getWhoTradingWith(), 
			PlayerUtil.getActivePlayerID(), args)

def handleUserResponse(eComment, args):
	dispatchEvent(eComment, PlayerUtil.getActivePlayerID(), 
			diplo.getWhoTradingWith(), args)

def dispatchEvent(eComment, eFromPlayer, eToPlayer, args):
	event = g_eventsByCommentType.get(eComment, None)
	if event:
		event.dispatch(eFromPlayer, eToPlayer, args)
	else:
		key = gc.getDiplomacyInfo(eComment).getType()
		BugUtil.debug("Diplomacy - ignoring %s from %d to %d with %r", 
				key, eFromPlayer, eToPlayer, args)


## Event Handlers

def onReligionDemanded(argsList):
	ePlayer, eTargetPlayer, eReligion = argsList
	BugUtil.debug("Diplomacy - %s asks %s to convert to %s",
			PlayerUtil.getPlayer(ePlayer).getName(), 
			PlayerUtil.getPlayer(eTargetPlayer).getName(), 
			gc.getReligionInfo(eReligion).getDescription())

def onReligionAccepted(argsList):
	ePlayer, eTargetPlayer, eReligion = argsList

def onReligionRejected(argsList):
	ePlayer, eTargetPlayer, eReligion = argsList


def onCivicDemanded(argsList):
	ePlayer, eTargetPlayer, eCivic = argsList
	BugUtil.debug("Diplomacy - %s asks %s to switch to %s",
			PlayerUtil.getPlayer(ePlayer).getName(), 
			PlayerUtil.getPlayer(eTargetPlayer).getName(), 
			gc.getCivicInfo(eCivic).getDescription())

def onCivicAccepted(argsList):
	ePlayer, eTargetPlayer, eCivic = argsList

def onCivicRejected(argsList):
	ePlayer, eTargetPlayer, eCivic = argsList


## Proposed Trade Functions

def getProposedTrade():
	trade = TradeUtil.Trade(PlayerUtil.getActivePlayerID(), diplo.getWhoTradingWith())
	if not diplo.ourOfferEmpty():
		getProposedTradeData(diplo.getPlayerTradeOffer, trade.addTrade)
	if not diplo.theirOfferEmpty():
		getProposedTradeData(diplo.getTheirTradeOffer, trade.addOtherTrade)
	BugUtil.debug("getProposedTrade - %r" % trade)
	return trade

def getProposedTradeData(getFunc, addFunc):
	for index in range(MAX_TRADE_DATA):
		data = getFunc(index)
		if data:
			addFunc(data)
		else:
			break
	else:
		BugUtil.debug("WARN: reached %d items in a single trade" % MAX_TRADE_DATA)
