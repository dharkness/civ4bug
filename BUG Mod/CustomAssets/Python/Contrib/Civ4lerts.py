## Copyright (c) 2005-2006, Gillmer J. Derge.

## This file is part of Civilization IV Alerts mod.
##
## Civilization IV Alerts mod is free software; you can redistribute
## it and/or modify it under the terms of the GNU General Public
## License as published by the Free Software Foundation; either
## version 2 of the License, or (at your option) any later version.
##
## Civilization IV Alerts mod is distributed in the hope that it will
## be useful, but WITHOUT ANY WARRANTY; without even the implied
## warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
## See the GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with Civilization IV Alerts mod; if not, write to the Free
## Software Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA
## 02110-1301 USA

__version__ = "$Revision: 1.2 $"
# $Source: /usr/local/cvsroot/Civ4lerts/src/main/python/Civ4lerts.py,v $

## Civ4lerts
## This class extends the built in event manager and overrides various
## event handlers to display alerts about important game situations.
##
## [*] = Already implemented in the Civ4lerts mod
## [o] = Partially implemented in the Civ4lerts mod
## [x] = Already implemented in CivIV
## [?] = Not sure if this applies in CivIV
## 
## Golden Age turns left
## At Year 1000 B.C. (QSC Save Submission)
## Within 10 tiles of domination limit
## There is new technology for sale
## There is a new luxury resource for sale
## There is a new strategic resource for sale
## There is a new bonus resource for sale
## We can sell a technology
## We can sell a luxury resource
## We can sell a strategic resource
## We can sell a bonus resource
## [*] Rival has lots of cash
## [*] Rival has lots of cash per turn
## [x] Rival has changed civics
## Rival has entered a new Era
## Trade deal expires next turn
## [o] Enemy at war is willing to negotiate
## [x] There are foreign units in our territory
## City is about to riot or rioting
## [*] City has grown or shrunk
## City has shrunk
## [*] City is unhealthy
## [*] City is angry
## City specialists reassigned
## [*] City is about to grow
## City is about to starve
## [*] City is about to grow into unhealthyness
## [*] City is about to grow into anger
## City is in resistance
## [?] City is wasting food
## City is working unimproved tiles
## Disconnected resources in our territory
## City is about to produce a great person
## 
## Other:
## City is under cultural pressure


class Civ4lerts:

	def __init__(self, eventManager):
		CityGrowth(eventManager)
		
		cityEvent = EndGameTurnCityEvent(eventManager)
		cityEvent.add(CityPendingGrowth())
		cityEvent.add(CityHealthiness())
		cityEvent.add(CityHappiness())
		
		CanHurryPopulation(eventManager)
		CanHurryGold(eventManager)
		GoldTrade(eventManager)
		GoldPerTurnTrade(eventManager)

from CvPythonExtensions import *

# BUG - Options - start
import BugAlertsOptions
BugAlerts = BugAlertsOptions.getOptions()
# BUG - Options - end

gc = CyGlobalContext()
localText = CyTranslator()

# Icons don't seem to be displayed anyway
HEALTHY_ICON = "Art/Interface/Buttons/General/unhealthy_person.dds"
UNHEALTHY_ICON = "Art/Interface/Buttons/General/unhealthy_person.dds"

HAPPY_ICON = "Art/Interface/mainscreen/cityscreen/angry_citizen.dds"
UNHAPPY_ICON = "Art/Interface/mainscreen/cityscreen/angry_citizen.dds"

# Displaying alerts on-screen
def addMessageNoIcon(iPlayer, message):
	"Displays an on-screen message with no popup icon."
	addMessage(iPlayer, message, None, 0, 0)

def addMessageAtCity(iPlayer, message, icon, city):
	"Displays an on-screen message with a popup icon that zooms to the given city."
	addMessage(iPlayer, message, icon, city.getX(), city.getY())

def addMessageAtPlot(iPlayer, message, icon, plot):
	"Displays an on-screen message with a popup icon that zooms to the given plot."
	addMessage(iPlayer, message, icon, plot.getX(), plot.getY())

def addMessage(iPlayer, szString, szIcon, iFlashX, iFlashY):
	"Displays an on-screen message."
	eventMessageTimeLong = gc.getDefineINT("EVENT_MESSAGE_TIME_LONG")
	CyInterface().addMessage(iPlayer, True, eventMessageTimeLong,
							 szString, None, 0, szIcon, ColorTypes(-1),
							 iFlashX, iFlashY, True, True)

class EndGameTurnCityEvent:
	"""
	Triggered at the end of each game turn, this event loops over all of the
	active player's cities, passing each off to a set of alert checkers.
	
	All of the alerts are reset when the game is loaded or started, too.
	"""
	def __init__(self, eventManager):
		eventManager.addEventHandler("GameStart", self.onGameStart)
		eventManager.addEventHandler("OnLoad", self.onLoadGame)
		eventManager.addEventHandler("cityAcquiredAndKept", self.onCityAcquiredAndKept)
		eventManager.addEventHandler("cityLost", self.onCityLost)
		eventManager.addEventHandler("EndGameTurn", self.onEndGameTurn)
		self.alerts = []

	def add(self, alert):
		self.alerts.append(alert)

	def onGameStart(self, argsList):
		self._reset()

	def onLoadGame(self, argsList):
		self._reset()
		return 0
	
	def onCityAcquiredAndKept(self, argsList):
		iPlayer, city = argsList
		if (iPlayer == gc.getGame().getActivePlayer()):
			self._checkCity(city)
	
	def onCityLost(self, argsList):
		'City Lost'
		city = argsList[0]
		iPlayer = gc.getGame().getActivePlayer()
		if (iPlayer == gc.getGame().getActivePlayer()):
			self._discardCity(city)
	
	def onEndGameTurn(self, argsList):
		"Loops over active player's cities, telling each to perform its check."
		iTurn = argsList[0]
		iPlayer = gc.getGame().getActivePlayer()
		player = gc.getActivePlayer()
		for iCity in range(player.getNumCities()):
			city = player.getCity(iCity)
			if (city and not city.isNone()):
				for alert in self.alerts:
					iCityID = city.getID()
					alert.check(iTurn, iCityID, city, iPlayer, player)

	def _reset(self):
		"Resets each alert."
		for alert in self.alerts:
			alert.reset()

	def _checkCity(self, city):
		"tells each alert to check the state of the given city -- no alerts are displayed."
		for alert in self.alerts:
			alert.checkCity(city)

	def _discardCity(self, city):
		"tells each alert to discard the state of the given city."
		for alert in self.alerts:
			alert.discardCity(city)

class AbstractCityAlert:
	"""
	Tracks cities from turn-to-turn and checks each at the end of every game turn
	to see if the alert should be displayed.
	"""
	def __init__(self):
		"Performs static initialization that doesn't require game data."
		pass
	
	def reset(self):
		"Clears state kept for each city."
		pass
	
	def check(self, iTurn, iCityID, city, iPlayer, player):
		"Checks the city, updates its tracked state and possibly displays an alert."
		pass
	
	def checkCity(self, city):
		"Checks the city and updates its tracked state."
		pass
	
	def discardCity(self, city):
		"Discards the tracked state of the city."
		pass


class CityPendingGrowth(AbstractCityAlert):
	"""
	Displays an alert when a city's population will grow next turn.
	State: None.
	"""
	def __init__(self):
		AbstractCityAlert.__init__(self)
	
	def check(self, iTurn, iCityID, city, iPlayer, player):
		if (not BugAlerts.isShowCityPendingGrowthAlert()):
			return
		if (city.getFoodTurnsLeft() == 1 and not city.isFoodProduction() and not city.AI_isEmphasize(5)):
			message = localText.getText(
					"TXT_KEY_CIV4LERTS_ON_CITY_PENDING_GROWTH",
					(city.getName(), city.getPopulation() + 1))
			icon = "Art/Interface/Symbols/Food/food05.dds"
			addMessageAtCity(iPlayer, message, icon, city)

class CityGrowth:
	"""
	Displays an alert when a city's population grows.
	"""
	def __init__(self, eventManager): 
		eventManager.addEventHandler("cityGrowth", self.onCityGrowth)

	def onCityGrowth(self, argsList):
		city, iPlayer = argsList
		if (iPlayer == gc.getGame().getActivePlayer() and BugAlerts.isShowCityGrowthAlert()):
			message = localText.getText(
					"TXT_KEY_CIV4LERTS_ON_CITY_GROWTH",
					(city.getName(), city.getPopulation()))
			icon = "Art/Interface/Symbols/Food/food05.dds"
			addMessageAtCity(iPlayer, message, icon, city)


class CityHappiness(AbstractCityAlert):
	"""
	Displays an event when a city goes from happy to angry or vice versa.
	State: set of unhappy city IDs.
	"""
	def __init__(self):
		AbstractCityAlert.__init__(self)

	def check(self, iTurn, iCityID, city, iPlayer, player):
		angry = city.angryPopulation(0) > 0
		wasAngry = iCityID in self.angryCities
		if (angry != wasAngry):
			# City switched this turn
			if (angry):
				self.angryCities.add(iCityID)
				if (BugAlerts.isShowCityHappinessAlert()):
					message = localText.getText(
							"TXT_KEY_CIV4LERTS_ON_CITY_UNHAPPY",
							(city.getName(), ))
					addMessageAtCity(iPlayer, message, UNHAPPY_ICON, city)
			else:
				self.angryCities.discard(iCityID)
				if (BugAlerts.isShowCityHappinessAlert()):
					message = localText.getText(
							"TXT_KEY_CIV4LERTS_ON_CITY_HAPPY",
							(city.getName(), ))
					addMessageAtCity(iPlayer, message, HAPPY_ICON, city)
		elif (BugAlerts.isShowCityPendingHappinessAlert()):
			# See if city will switch next turn
			if (city.getFoodTurnsLeft() == 1 and not city.isFoodProduction() 
			and not city.AI_isEmphasize(5)):
				iExtra = 1
			else:
				iExtra = 0
			iHappy = city.happyLevel()
			iUnhappy = city.unhappyLevel(iExtra)
			if (iUnhappy > 0 and city.getHurryAngerTimer() > 0 
			and city.getHurryAngerTimer() % city.flatHurryAngerLength() == 0):
				iUnhappy -= 1
			if (iUnhappy > 0 and city.getConscriptAngerTimer()
			and city.getConscriptAngerTimer() % city.flatConscriptAngerLength() == 0):
				iUnhappy -= 1
			if (iUnhappy > 0 and city.getDefyResolutionAngerTimer() > 0
			and city.getDefyResolutionAngerTimer() % city.flatDefyResolutionAngerLength() == 0):
				iUnhappy -= 1
			if (iUnhappy > 0 and city.getEspionageHappinessCounter() > 0):
				iUnhappy -= 1
			if (iHappy > 0 and city.getHappinessTimer() == 1):
				iHappy -= gc.getDefineINT("TEMP_HAPPY")
			if (iHappy < 0):
				iHappy = 0
			if (iUnhappy < 0):
				iUnhappy = 0
			if (not wasAngry and iHappy < iUnhappy):
				message = localText.getText(
						"TXT_KEY_CIV4LERTS_ON_CITY_PENDING_UNHAPPY",
						(city.getName(), ))
				addMessageAtCity(iPlayer, message, UNHAPPY_ICON, city)
			elif (wasAngry and iHappy >= iUnhappy):
				message = localText.getText(
						"TXT_KEY_CIV4LERTS_ON_CITY_PENDING_HAPPY",
						(city.getName(), ))
				addMessageAtCity(iPlayer, message, HAPPY_ICON, city)

	def reset(self):
		self.angryCities = set()
		player = gc.getActivePlayer()
		for iCity in range(player.getNumCities()):
			city = player.getCity(iCity)
			if (not city.isNone() and city.angryPopulation(0) > 0):
				self.angryCities.add(city.getID())
	
	def checkCity(self, city):
		if (city.angryPopulation(0) > 0):
			self.angryCities.add(city.getID())
	
	def discardCity(self, city):
		self.angryCities.discard(city.getID())

class CityHealthiness(AbstractCityAlert):
	"""
	Displays an event when a city goes from healthy to sick or vice versa.
	State: set of unhealthy city IDs.
	"""
	def __init__(self):
		AbstractCityAlert.__init__(self)

	def check(self, iTurn, iCityID, city, iPlayer, player):
		sick = city.healthRate(False, 0) < 0
		wasSick = iCityID in self.sickCities
		if (sick != wasSick):
			if (sick):
				self.sickCities.add(iCityID)
				if (BugAlerts.isShowCityHealthinessAlert()):
					message = localText.getText(
							"TXT_KEY_CIV4LERTS_ON_CITY_UNHEALTHY",
							(city.getName(), ))
					addMessageAtCity(iPlayer, message, UNHEALTHY_ICON, city)
			else:
				self.sickCities.discard(iCityID)
				if (BugAlerts.isShowCityHealthinessAlert()):
					message = localText.getText(
							"TXT_KEY_CIV4LERTS_ON_CITY_HEALTHY",
							(city.getName(), ))
					addMessageAtCity(iPlayer, message, HEALTHY_ICON, city)
		elif (BugAlerts.isShowCityPendingHealthinessAlert()):
			# See if city will switch next turn
			if (city.getFoodTurnsLeft() == 1 and not city.isFoodProduction() 
			and not city.AI_isEmphasize(5)):
				iExtra = 1
			else:
				iExtra = 0
			# badHealth() doesn't take iExtra!
			iHealth = city.healthRate(False, iExtra)
			if (city.getEspionageHealthCounter() > 0):
				iHealth -= 1
			if (not wasSick and iHealth < 0):
				message = localText.getText(
						"TXT_KEY_CIV4LERTS_ON_CITY_PENDING_UNHEALTHY",
						(city.getName(), ))
				addMessageAtCity(iPlayer, message, UNHEALTHY_ICON, city)
			elif (wasSick and iHealth >= 0):
				message = localText.getText(
						"TXT_KEY_CIV4LERTS_ON_CITY_PENDING_HEALTHY",
						(city.getName(), ))
				addMessageAtCity(iPlayer, message, HEALTHY_ICON, city)

	def reset(self):
		self.sickCities = set()
		player = gc.getActivePlayer()
		for iCity in range(player.getNumCities()):
			city = player.getCity(iCity)
			if (not city.isNone() and city.healthRate(False, 0) < 0):
				self.sickCities.add(city.getID())
	
	def checkCity(self, city):
		if (city.healthRate(False, 0) < 0):
			self.sickCities.add(city.getID())
	
	def discardCity(self, city):
		self.sickCities.discard(city.getID())


class AbstractStatefulAlert:

#   Provides a base class and several convenience functions for 
#   implementing an alert that retains state information between turns.

	def __init__(self, eventManager):
		eventManager.addEventHandler("GameStart", self.onGameStart)
		eventManager.addEventHandler("OnLoad", self.onLoadGame)

	def onGameStart(self, argsList):
#	   Called at the start of the game
		self._reset()

	def onLoadGame(self, argsList):
		self._reset()
		return 0

	def _reset(self):
#	   Override this method to reset any turn state information.
		pass

class AbstractCanHurry(AbstractStatefulAlert):
#   Displays an alert when a city can hurry the current production item.

	def __init__(self, eventManager, hurryType):
		AbstractStatefulAlert.__init__(self, eventManager)
		eventManager.addEventHandler("cityDoTurn", self.onCityDoTurn)
		eventManager.addEventHandler("cityBuildingUnit", self.onCityBuildingUnit)
		eventManager.addEventHandler("cityBuildingBuilding", self.onCityBuildingBuilding)
		self.hurryType = hurryType

	def onCityDoTurn(self, argsList):
		city, iPlayer = argsList
		if (iPlayer != gc.getGame().getActivePlayer()):
			return
		self.checkCity(city, iPlayer)
		
	def checkCity(self, city, iPlayer):
		iCityID = city.getID()
		eHurryType = gc.getInfoTypeForString(self.hurryType)
		if (city.canHurry(eHurryType, False) and not self._canHurryCity(iCityID)):
			self._addCity(iCityID)
			if (city.isProductionBuilding()):
				iType = city.getProductionBuilding()
				if (iType >= 0):
					info = gc.getBuildingInfo(iType)
					self.onCityCanHurry(city, iPlayer, info.getDescription(), eHurryType)
			elif (city.isProductionUnit()):
				iType = city.getProductionUnit()
				if (iType >= 0):
					info = gc.getUnitInfo(iType)
					self.onCityCanHurry(city, iPlayer, info.getDescription(), eHurryType)
			elif (city.isProductionProject()):
				# Can't hurry projects, but just in case
				iType = city.getProductionProject()
				if (iType >= 0):
					info = gc.getProjectInfo(iType)
					self.onCityCanHurry(city, iPlayer, info.getDescription(), eHurryType)

	def onCityCanHurry(self, city, iPlayer, item, eHurryType):
		"Override to display the alert."
		pass

	def onCityBuildingUnit(self, argsList):
		city, iUnit = argsList
		self.onItemStarted(city)

	def onCityBuildingBuilding(self, argsList):
		city, iBuilding = argsList
		self.onItemStarted(city)

	def onItemStarted(self, city):
		iPlayer = city.getOwner()
		if (iPlayer != gc.getGame().getActivePlayer()):
			return
		self._removeCity(city.getID())

	def _reset(self, *args, **kwargs):
		self.canHurryCities = set()
		eHurryType = gc.getInfoTypeForString(self.hurryType)
		player = gc.getActivePlayer()
		for iCity in range(player.getNumCities()):
			city = player.getCity(iCity)
			if (city and not city.isNone()):
				if (city.canHurry(eHurryType, False)):
					self._addCity(city.getID())

	def _canHurryCity(self, iCityID):
		return iCityID in self.canHurryCities

	def _addCity(self, iCityID):
		self.canHurryCities.add(iCityID)

	def _removeCity(self, iCityID):
		self.canHurryCities.discard(iCityID)

class CanHurryPopulation(AbstractCanHurry):
#   Displays an alert when a city can hurry using population.

	def __init__(self, eventManager): 
		AbstractCanHurry.__init__(self, eventManager, "HURRY_POPULATION")

	def onCityCanHurry(self, city, iPlayer, item, eHurryType):
		if (BugAlerts.isShowCityCanHurryPopAlert()):
			iPop = city.hurryPopulation(eHurryType)
			iOverflow = city.hurryProduction(eHurryType) - (city.getProductionNeeded() - city.getProduction())
			cPop = u"%c" % gc.getGame().getSymbolID(FontSymbols.ANGRY_POP_CHAR)
			cHammer = u"%c" % gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getChar()
			message = localText.getText("TXT_KEY_CIV4LERTS_ON_CITY_CAN_HURRY_POP", 
										(item, city.getName(), iPop, cPop, iOverflow, cHammer))
			icon = "Art/Interface/mainscreen/cityscreen/angry_citizen.dds"
			addMessageAtCity(iPlayer, message, icon, city)

class CanHurryGold(AbstractCanHurry):
#   Displays an alert when a city can hurry using gold.

	def __init__(self, eventManager): 
		AbstractCanHurry.__init__(self, eventManager, "HURRY_GOLD")

	def onCityCanHurry(self, city, iPlayer, item, eHurryType):
		if (BugAlerts.isShowCityCanHurryGoldAlert()):
			iGold = city.hurryGold(eHurryType)
			cGold = u"%c" % gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getChar()
			message = localText.getText("TXT_KEY_CIV4LERTS_ON_CITY_CAN_HURRY_GOLD", 
										(item, city.getName(), iGold, cGold))
			icon = "Art/Interface/mainscreen/cityscreen/angry_citizen.dds"
			addMessageAtCity(iPlayer, message, icon, city)


class GoldTrade(AbstractStatefulAlert):
#   Displays an alert when a civilization has a significant increase
#	in gold available for trade since the last alert.

	def __init__(self, eventManager):
		AbstractStatefulAlert.__init__(self, eventManager)
		eventManager.addEventHandler("BeginGameTurn", self.onBeginGameTurn)

	def onBeginGameTurn(self, argsList):
		if (not BugAlerts.isShowGoldTradeAlert()):
			return

		turn = argsList[0]
		player = gc.getGame().getActivePlayer()
		team = gc.getTeam(gc.getPlayer(player).getTeam())
		for rival in range(gc.getMAX_PLAYERS()):
			if (rival == player): continue
			rivalPlayer = gc.getPlayer(rival)
			rivalTeam = gc.getTeam(rivalPlayer.getTeam())
			# TODO: does this need to check for war or trade denial?
			if (team.isHasMet(rivalPlayer.getTeam())
				and (team.isGoldTrading() or rivalTeam.isGoldTrading())):
				oldMaxGoldTrade = self._getMaxGoldTrade(player, rival)
				newMaxGoldTrade = rivalPlayer.AI_maxGoldTrade(player)
				deltaMaxGoldTrade = newMaxGoldTrade - oldMaxGoldTrade
				if (deltaMaxGoldTrade >= BugAlerts.getGoldTradeThreshold()):
					message = localText.getText(
							"TXT_KEY_CIV4LERTS_ON_GOLD_TRADE",
							(gc.getTeam(rival).getName(),
							 newMaxGoldTrade))
					addMessageNoIcon(player, message)
					self._setMaxGoldTrade(player, rival, newMaxGoldTrade)
				else:
					maxGoldTrade = min(oldMaxGoldTrade, newMaxGoldTrade)
					self._setMaxGoldTrade(player, rival, maxGoldTrade)

	def _reset(self):
		self.maxGoldTrade = {}
		for player in range(gc.getMAX_PLAYERS()):
			self.maxGoldTrade[player] = {}
			for rival in range(gc.getMAX_PLAYERS()):
				self._setMaxGoldTrade(player, rival, 0)

	def _getMaxGoldTrade(self, player, rival):
		return self.maxGoldTrade[player][rival]
	
	def _setMaxGoldTrade(self, player, rival, value):
		self.maxGoldTrade[player][rival] = value

class GoldPerTurnTrade(AbstractStatefulAlert):
#   Displays an alert when a civilization has a significant increase
#   in gold per turn available for trade since the last alert.

	def __init__(self, eventManager):
		AbstractStatefulAlert.__init__(self, eventManager)
		eventManager.addEventHandler("BeginGameTurn", self.onBeginGameTurn)

	def onBeginGameTurn(self, argsList):
		if (not BugAlerts.isShowGoldPerTurnTradeAlert()):
			return

		turn = argsList[0]
		player = gc.getGame().getActivePlayer()
		team = gc.getTeam(gc.getPlayer(player).getTeam())
		for rival in range(gc.getMAX_PLAYERS()):
			if (rival == player): continue
			rivalPlayer = gc.getPlayer(rival)
			rivalTeam = gc.getTeam(rivalPlayer.getTeam())
			# TODO: does this need to check for war or trade denial?
			if (team.isHasMet(rivalPlayer.getTeam())
				and (team.isGoldTrading() or rivalTeam.isGoldTrading())):
				oldMaxGoldPerTurnTrade = self._getMaxGoldPerTurnTrade(player, rival)
				newMaxGoldPerTurnTrade = rivalPlayer.AI_maxGoldPerTurnTrade(player)
				deltaMaxGoldPerTurnTrade = newMaxGoldPerTurnTrade - oldMaxGoldPerTurnTrade
				if (deltaMaxGoldPerTurnTrade >= BugAlerts.getGoldPerTurnTradeThreshold()):
					message = localText.getText(
							"TXT_KEY_CIV4LERTS_ON_GOLD_PER_TURN_TRADE",
							(gc.getTeam(rival).getName(),
							 newMaxGoldPerTurnTrade))
					addMessageNoIcon(player, message)
					self._setMaxGoldPerTurnTrade(player, rival, newMaxGoldPerTurnTrade)
				else:
					maxGoldPerTurnTrade = min(oldMaxGoldPerTurnTrade, newMaxGoldPerTurnTrade)
					self._setMaxGoldPerTurnTrade(player, rival, maxGoldPerTurnTrade)

	def _reset(self):
		self.maxGoldPerTurnTrade = {}
		for player in range(gc.getMAX_PLAYERS()):
			self.maxGoldPerTurnTrade[player] = {}
			for rival in range(gc.getMAX_PLAYERS()):
				self._setMaxGoldPerTurnTrade(player, rival, 0)

	def _getMaxGoldPerTurnTrade(self, player, rival):
		return self.maxGoldPerTurnTrade[player][rival]
	
	def _setMaxGoldPerTurnTrade(self, player, rival, value):
		self.maxGoldPerTurnTrade[player][rival] = value
