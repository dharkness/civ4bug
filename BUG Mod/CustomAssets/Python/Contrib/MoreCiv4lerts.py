## MoreCiv4lerts
## From HOF MOD V1.61.001
## Based upon Gillmer J. Derge's Civ4lerts.py

from CvPythonExtensions import *
import CvUtil
import PyHelpers

# BUG - Options - start
import BugAlertsOptions
BugAlerts = BugAlertsOptions.getOptions()
# BUG - Options - end

gc = CyGlobalContext()
localText = CyTranslator()
PyGame = PyHelpers.PyGame()
PyPlayer = PyHelpers.PyPlayer
PyCity = PyHelpers.PyCity
PyInfo = PyHelpers.PyInfo

class MoreCiv4lerts:

	def __init__(self, eventManager):
		## Init event handlers
		MoreCiv4lertsEvent(eventManager)

class AbstractMoreCiv4lertsEvent(object):
	
	def __init__(self, eventManager, *args, **kwargs):
			super( AbstractMoreCiv4lertsEvent, self).__init__(*args, **kwargs)

	def _addMessageNoIcon(self, player, message):
			#Displays an on-screen message with no popup icon.
			self._addMessage(player, message, None, 0, 0, False, False)

	def _addMessageAtCity(self, player, message, icon, city):
			#Displays an on-screen message with a popup icon that zooms to the given city.
			self._addMessage(player, message, icon, city.getX(), city.getY(), True, True)

	def _addMessageAtPlot(self, player, message, icon, plot):
			#Displays an on-screen message with a popup icon that zooms to the given plot.
			self._addMessage(player, message, icon, plot.getX(), plot.getY(), True, True)

	def _addMessage(self, ePlayer, szString, szIcon, iFlashX, iFlashY, bOffArrow, bOnArrow):
			#Displays an on-screen message.
			eventMessageTimeLong = gc.getDefineINT("EVENT_MESSAGE_TIME_LONG")
			CyInterface().addMessage(ePlayer, True, eventMessageTimeLong,
															 szString, None, 0, szIcon, ColorTypes(-1),
															 iFlashX, iFlashY, bOffArrow, bOnArrow)

class MoreCiv4lertsEvent( AbstractMoreCiv4lertsEvent):

	def __init__(self, eventManager, *args, **kwargs):
		super(MoreCiv4lertsEvent, self).__init__(eventManager, *args, **kwargs)

		eventManager.addEventHandler("BeginGameTurn", self.OnBeginGameTurn)
		eventManager.addEventHandler("cityAcquired", self.OnCityAcquired)
		eventManager.addEventHandler("cityBuilt", self.OnCityBuilt)
		eventManager.addEventHandler("cityRazed", self.OnCityRazed)
		eventManager.addEventHandler("cityLost", self.OnCityLost)

		self.eventMgr = eventManager
		self.CurrAvailTechTrades = {}
		self.PrevAvailTechTrades = {}
		self.lastDomLimitMsgTurn = 0
		self.lastPopCount = 0
		self.lastLandCount = 0

	def getCheckForDomPopVictory(self):
		return BugAlerts.isShowDomPopAlert()

	def getCheckForDomLandVictory(self):
		return BugAlerts.isShowDomLandAlert()

	def getPopThreshold(self):
		return BugAlerts.getDomPopThreshold()

	def getLandThreshold(self):
		return BugAlerts.getDomLandThreshold()

	def getCheckForCityBorderExpansion(self):
		return BugAlerts.isShowCityExpandBorderAlert()

	def getCheckForNewTrades(self):
		return BugAlerts.isShowTechTradeAlert()

	def getCheckForDomVictory(self):
		return self.getCheckForDomPopVictory() or self.getCheckForDomLandVictory()

	def getDoChecks(self):
		return self.getCheckForDomVictory() or self.getCheckForCityBorderExpansion() or self.getCheckForNewTrades()

	def OnBeginGameTurn(self, argsList):
		iGameTurn = argsList[0]
		if (not self.getDoChecks()): return
		iPlayer = gc.getGame().getActivePlayer()
		self.CheckForAlerts(iPlayer, PyPlayer(iPlayer).getTeam(), True)

	def OnCityAcquired(self, argsList):
		owner,playerType,city,bConquest,bTrade = argsList
		iPlayer = city.getOwner()
		if (not self.getCheckForDomVictory()): return
		if (iPlayer == gc.getGame().getActivePlayer()):
				self.CheckForAlerts(iPlayer, PyPlayer(iPlayer).getTeam(), False)

	def OnCityBuilt(self, argsList):
		city = argsList[0]
		iPlayer = city.getOwner()
		if (not self.getCheckForDomVictory()): return
		if (iPlayer == gc.getGame().getActivePlayer()):
				self.CheckForAlerts(iPlayer, PyPlayer(iPlayer).getTeam(), False)

	def OnCityRazed(self, argsList):
		city, iPlayer = argsList
		if (not self.getCheckForDomVictory()): return
		if (iPlayer == gc.getGame().getActivePlayer()):
				self.CheckForAlerts(iPlayer, PyPlayer(iPlayer).getTeam(), False)

	def OnCityLost(self, argsList):
		city = argsList[0]
		iPlayer = city.getOwner()
		if (not self.getCheckForDomVictory()): return
		if (iPlayer == gc.getGame().getActivePlayer()):
				self.CheckForAlerts(iPlayer, PyPlayer(iPlayer).getTeam(), False)

	def CheckForAlerts(self, iPlayer, iActiveTeam, BeginTurn):
	##Added "else: pass" code to diagnose strange results - might be related to indent issues
		ourPop = 0
		ourLand = 0
		totalPop = 0
		totalLand = 0
		LimitPop =0
		LimitLand = 0
		DomVictory = 3
		popGrowthCount = 0
		currentTurn = gc.getGame().getGameTurn()

		if (self.getCheckForDomPopVictory() or (BeginTurn and self.getCheckForCityBorderExpansion())):
			# Check for cultural expansion and population growth
			teamPlayerList = []
			teamPlayerList = PyGame.getCivTeamList(PyGame.getActiveTeam())
			teamPlayerList.append(PyPlayer(iPlayer))
			for loopPlayer in range(len(teamPlayerList)):
				lCity = []
				lCity = PyPlayer(loopPlayer).getCityList()
				for loopCity in range(len(lCity)):
					city = gc.getPlayer(loopPlayer).getCity(loopCity)
					if (city.getFoodTurnsLeft() == 1 and not city.isFoodProduction()) and not city.AI_isEmphasize(5):
						popGrowthCount = popGrowthCount + 1
					if (BeginTurn and self.getCheckForCityBorderExpansion()):
						if (city.getCultureLevel() != gc.getNumCultureLevelInfos() - 1):
							if ((city.getCulture(loopPlayer) + city.getCommerceRate(CommerceTypes.COMMERCE_CULTURE)) > city.getCultureThreshold()):
								message = localText.getText("TXT_KEY_MORECIV4LERTS_CITY_TO_EXPAND",(city.getName(),))
								icon = "Art/Interface/Buttons/General/Warning_popup.dds"
								self._addMessageAtCity(loopPlayer, message, icon, city)
							else: pass
						else: pass #expand check
					else: pass #message check
				else: pass #end city loop
			else: pass #end player loop
		else: pass # end expansion check / pop count

		# Check Domination Limit
		if (self.getCheckForDomVictory() and gc.getGame().isVictoryValid(DomVictory)):
			
			# Population Limit
			if (self.getCheckForDomPopVictory()):
				VictoryPopPercent = 0.0
				VictoryPopPercent = gc.getGame().getAdjustedPopulationPercent(DomVictory) * 1.0
				totalPop = gc.getGame().getTotalPopulation()
				LimitPop = int((totalPop * VictoryPopPercent) / 100.0)
				ourPop = iActiveTeam.getTotalPopulation()
				if (totalPop > 0):
					popPercent = (ourPop * 100.0) / totalPop
					NextpopPercent = ((ourPop + popGrowthCount) * 100.0) / totalPop
				else:
					popPercent = 0.0
					NextpopPercent = 0.0

				if (totalPop > 1 and (currentTurn <> self.lastDomLimitMsgTurn or (ourPop + popGrowthCount) <> self.lastPopCount)):
					self.lastPopCount = ourPop + popGrowthCount
					if (popPercent >= VictoryPopPercent):
						message = localText.getText("TXT_KEY_MORECIV4LERTS_POP_EXCEEDS_LIMIT",
						   		(ourPop, (u"%.2f%%" % popPercent), LimitPop, (u"%.2f%%" % VictoryPopPercent)))
						self._addMessageNoIcon(iPlayer, message)

					elif (popGrowthCount > 0 and NextpopPercent >= VictoryPopPercent):
						message = localText.getText("TXT_KEY_MORECIV4LERTS_POP_GROWTH_EXCEEDS_LIMIT",
						   		(ourPop, popGrowthCount, (u"%.2f%%" % NextpopPercent), LimitPop, (u"%.2f%%" % VictoryPopPercent)))
						self._addMessageNoIcon(iPlayer, message)

					elif (popGrowthCount > 0 and (VictoryPopPercent - NextpopPercent < self.getPopThreshold())):
						message = localText.getText("TXT_KEY_MORECIV4LERTS_POP_GROWTH_CLOSE_TO_LIMIT",
						   		(ourPop, popGrowthCount, (u"%.2f%%" % NextpopPercent), LimitPop, (u"%.2f%%" % VictoryPopPercent)))
						self._addMessageNoIcon(iPlayer, message)

## .005 			elif (VictoryPopPercent - popPercent < self.getPopThreshold()):
					elif (popGrowthCount > 0 and (VictoryPopPercent - popPercent < self.getPopThreshold())):
						message = localText.getText("TXT_KEY_MORECIV4LERTS_POP_CLOSE_TO_LIMIT",
						   		(ourPop, (u"%.2f%%" % popPercent), LimitPop, (u"%.2f%%" % VictoryPopPercent)))
						self._addMessageNoIcon(iPlayer, message)
					else: pass #end elif
				else: pass #end totalPop if
			else: pass #end pop limit if

			# Land Limit
			if (self.getCheckForDomLandVictory()):
				VictoryLandPercent = 0.0
				VictoryLandPercent = gc.getGame().getAdjustedLandPercent(DomVictory) * 1.0
				totalLand = gc.getMap().getLandPlots()
				LimitLand = int((totalLand * VictoryLandPercent) / 100.0)
				ourLand = iActiveTeam.getTotalLand()
				if (totalLand > 0):
					landPercent = (ourLand * 100.0) / totalLand
				else:
					landPercent = 0.0
				if (currentTurn <> self.lastDomLimitMsgTurn or ourLand <> self.lastLandCount):
					self.lastLandCount = ourLand
					if (landPercent > VictoryLandPercent):
						message = localText.getText("TXT_KEY_MORECIV4LERTS_LAND_EXCEEDS_LIMIT",
								(ourLand, (u"%.2f%%" % landPercent), LimitLand, (u"%.2f%%" % VictoryLandPercent)))
						self._addMessageNoIcon(iPlayer, message)
					elif (VictoryLandPercent - landPercent < self.getLandThreshold()):
						message = localText.getText("TXT_KEY_MORECIV4LERTS_LAND_CLOSE_TO_LIMIT",
								(ourLand, (u"%.2f%%" % landPercent), LimitLand, (u"%.2f%%" % VictoryLandPercent)))
						self._addMessageNoIcon(iPlayer, message)
					else: pass #end elif
				else: pass #end currentTurn if
			else: pass #end land limit if
		else: pass #end dom limt if
	
		#save turn num
		if (self.getCheckForDomVictory()):
		    self.lastDomLimitMsgTurn = currentTurn

		# new trades
		if (BeginTurn and self.getCheckForNewTrades()):
			CurrTechCanTrade = []
			PrevTechCanTrade = []
			PlayerHasTech = ""
			self.getTechForTrade(gc.getPlayer(iPlayer), iActiveTeam)
			for iLoopPlayer, CurrTechCanTrade in self.CurrAvailTechTrades.iteritems():
				#Did he have trades avail last turn
				if (self.PrevAvailTechTrades.has_key(iLoopPlayer)):
					PrevTechCanTrade = []
					PrevTechCanTrade = self.PrevAvailTechTrades.get(iLoopPlayer)
					#Any trades this turn?
					if (CurrTechCanTrade):
						if (PrevTechCanTrade):
							#compare this turn's vs last turn's trades
							for iTech in CurrTechCanTrade:
								if (iTech not in PrevTechCanTrade):
									if (PlayerHasTech != ""):
										PlayerHasTech = PlayerHasTech + ", "
									else: pass
									PlayerHasTech = PlayerHasTech + PyPlayer(iLoopPlayer).getName()
									break
								else: pass
						else:
							if (PlayerHasTech != ""):
								PlayerHasTech = PlayerHasTech + ", "
							else: pass
							PlayerHasTech = PlayerHasTech + PyPlayer(iLoopPlayer).getName()
					else: pass #end (no current trades)
				#nothing last turn, how about this turn?
				elif (CurrTechCanTrade):
					if (PlayerHasTech != ""):
						PlayerHasTech = PlayerHasTech + ", "
					else: pass
					PlayerHasTech = PlayerHasTech + PyPlayer(iLoopPlayer).getName()
				else: pass #end elif
			
				#save curr trades for next time
				self.PrevAvailTechTrades[iLoopPlayer] = CurrTechCanTrade

			else: pass #end player loop

			if (PlayerHasTech != ""):
				message = localText.getText("TXT_KEY_MORECIV4LERTS_NEW_TECH_AVAIL",	(PlayerHasTech,))
				self._addMessageNoIcon(iPlayer, message)
			else: pass

		else: pass #end new trades if


	def getTechForTrade(self, iPlayer, iActiveTeam):
		iActiveTeamID = iActiveTeam.getID()
		tradeData = TradeData()
		tradeData.ItemType = TradeableItems.TRADE_TECHNOLOGIES
		self.CurrAvailTechTrades.clear
		TechCanTrade = []

		for iLoopPlayer in range(gc.getMAX_PLAYERS()):
			currentPlayer = gc.getPlayer(iLoopPlayer)
			currentTeam = currentPlayer.getTeam()

			TechCanTrade = []
			if (currentPlayer.isBarbarian()): return
			if (currentPlayer.isMinorCiv()): return
			if (iLoopPlayer != iPlayer.getID()):
				if (gc.getTeam(currentTeam).isHasMet(iActiveTeamID)):
					if (currentPlayer.isAlive()):
						if (iActiveTeam.isTechTrading() or gc.getTeam(currentTeam).isTechTrading()):
							for iLoopTech in range(gc.getNumTechInfos()):
								tradeData.iData = iLoopTech
								if (currentPlayer.canTradeItem(iPlayer.getID(), tradeData, False)):
									if (currentPlayer.getTradeDenial(iPlayer.getID(), tradeData) == DenialTypes.NO_DENIAL): # will trade
										TechCanTrade.append(iLoopTech)
									else: pass
								else: pass
						else: pass
						self.CurrAvailTechTrades[iLoopPlayer] = TechCanTrade
					else: pass
				else: pass
			else: pass
		return
