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
        CityPendingGrowth(eventManager)
        CityPendingUnhealthy(eventManager)
        CityPendingAngry(eventManager)
        CityGrowth(eventManager)
        CityGrowthUnhealthy(eventManager)
        CityGrowthAngry(eventManager)
        CanHurryPopulation(eventManager)
        CanHurryGold(eventManager)
        GoldTrade(eventManager)
        GoldPerTurnTrade(eventManager)
    

from CvPythonExtensions import ColorTypes
from CvPythonExtensions import CyGlobalContext
from CvPythonExtensions import CyInterface
from CvPythonExtensions import CyTranslator

# BUG - Options - start
import BugAlertsOptions
BugAlerts = BugAlertsOptions.getOptions()
# BUG - Options - end

class AbstractAlert(object):

#   Provides a base class and several convenience functions for implementing an alert.

    gc = CyGlobalContext()
    localText = CyTranslator()

    def __init__(self, eventManager, *args, **kwargs):
        super(AbstractAlert, self).__init__(*args, **kwargs)

    def _addMessageNoIcon(self, player, message):
#       Displays an on-screen message with no popup icon.
        self._addMessage(player, message, None, 0, 0)

    def _addMessageAtCity(self, player, message, icon, city):
#       Displays an on-screen message with a popup icon that zooms to the given city.
        self._addMessage(player, message, icon, city.getX(), city.getY())

    def _addMessageAtPlot(self, player, message, icon, plot):
#       Displays an on-screen message with a popup icon that zooms to the given plot.
        self._addMessage(player, message, icon, plot.getX(), plot.getY())

    def _addMessage(self, ePlayer, szString, szIcon, iFlashX, iFlashY):
#       Displays an on-screen message.
        eventMessageTimeLong = self.gc.getDefineINT("EVENT_MESSAGE_TIME_LONG")
        CyInterface().addMessage(ePlayer, True, eventMessageTimeLong,
                                 szString, None, 0, szIcon, ColorTypes(-1),
                                 iFlashX, iFlashY, True, True)

class AbstractStatefulAlert(AbstractAlert):

#   Provides a base class and several convenience functions for 
#   implementing an alert that retains state information between turns.

    def __init__(self, eventManager, *args, **kwargs):
        super(AbstractStatefulAlert, self).__init__(eventManager,
                                                    *args, **kwargs)
        eventManager.addEventHandler("GameStart", self.onGameStart)
        eventManager.addEventHandler("OnLoad", self.onLoadGame)

    def onGameStart(self, argsList):
#       Called at the start of the game
        self._reset()

    def onLoadGame(self, argsList):
        self._reset()
        return 0

    def _reset(self):
#       Override this method to reset any turn state information.
        pass


class AbstractCityPendingGrowth(AbstractAlert):
#   Synthesizes an event when a city's population is about to grow.

    def __init__(self, eventManager, *args, **kwargs): 
        super(AbstractCityPendingGrowth, self).__init__(eventManager,
                                                        *args, **kwargs)
        eventManager.addEventHandler("cityDoTurn", self.onCityDoTurn)

    def onCityDoTurn(self, argsList):
        city, player = argsList
        if (city.getOwner() != self.gc.getGame().getActivePlayer()):
            return
        if (((city.getFoodTurnsLeft() == 1)
        and not city.isFoodProduction())
        and not city.AI_isEmphasize(5)):
            self.onCityPendingGrowth(city, player)

    def onCityPendingGrowth(self, city, player):
#       Override this method to perform an action when a city is about to grow.
        pass

class CityPendingGrowth(AbstractCityPendingGrowth):
#   Displays an alert when a city's population is about to grow.

    def __init__(self, eventManager, *args, **kwargs): 
        super(CityPendingGrowth, self).__init__(eventManager, *args, **kwargs)

    def onCityPendingGrowth(self, city, player):
        if (not BugAlerts.isShowCityPendingGrowthAlert()):
            return

        message = self.localText.getText(
                "TXT_KEY_CIV4LERTS_ON_CITY_PENDING_GROWTH",
                (city.getName(), city.getPopulation() + 1))
        icon = "Art/Interface/Symbols/Food/food05.dds"
        self._addMessageAtCity(player, message, icon, city)

class CityPendingUnhealthy(AbstractCityPendingGrowth):
#   Displays an alert when a city's population is about to grow and become unhealthy.

    def __init__(self, eventManager, *args, **kwargs): 
        super(CityPendingUnhealthy, self).__init__(eventManager,
                                                   *args, **kwargs)

    def onCityPendingGrowth(self, city, player):
        if (not BugAlerts.isShowCityPendingUnhealthyAlert()):
            return

        if (city.goodHealth() <= city.badHealth(False)):
            message = self.localText.getText(
                    "TXT_KEY_CIV4LERTS_ON_CITY_PENDING_UNHEALTHY",
                    (city.getName(), city.getPopulation()))
            icon = "Art/Interface/Interface/Buttons/General/unhealthy_person.dds"
            self._addMessageAtCity(player, message, icon, city)

class CityPendingAngry(AbstractCityPendingGrowth):
#   Displays an alert when a city's population is about to grow and become angry.

    def __init__(self, eventManager, *args, **kwargs): 
        super(CityPendingAngry, self).__init__(eventManager, *args, **kwargs)

    def onCityPendingGrowth(self, city, player):
        if (not BugAlerts.isShowCityPendingAngryAlert()):
            return

        if (city.happyLevel() <= city.unhappyLevel(0)):
            message = self.localText.getText(
                    "TXT_KEY_CIV4LERTS_ON_CITY_PENDING_ANGRY",
                    (city.getName(), city.getPopulation()))
            icon = "Art/Interface/mainscreen/cityscreen/angry_citizen.dds"
            self._addMessageAtCity(player, message, icon, city)


class CityGrowth(AbstractAlert):
#   Displays an alert when a city's population grows."""

    def __init__(self, eventManager, *args, **kwargs): 
        super(CityGrowth, self).__init__(eventManager, *args, **kwargs)
        eventManager.addEventHandler("cityGrowth", self.onCityGrowth)

    def onCityGrowth(self, argsList):
        if (not BugAlerts.isShowCityGrowthAlert()):
            return

        city, player = argsList
        if (city.getOwner() != self.gc.getGame().getActivePlayer()):
            return
        message = self.localText.getText(
                "TXT_KEY_CIV4LERTS_ON_CITY_GROWTH",
                (city.getName(), city.getPopulation()))
        icon = "Art/Interface/Symbols/Food/food05.dds"
        self._addMessageAtCity(player, message, icon, city)

class CityGrowthUnhealthy(AbstractAlert):
#   Displays an alert when a city's population grows and becomes unhealthy.

    def __init__(self, eventManager, *args, **kwargs): 
        super(CityGrowthUnhealthy, self).__init__(eventManager,
                                                  *args, **kwargs)
        eventManager.addEventHandler("cityGrowth", self.onCityGrowth)

    def onCityGrowth(self, argsList):
        if (not BugAlerts.isShowCityGrowthUnhealthyAlert()):
            return

        city, player = argsList
        if (city.getOwner() != self.gc.getGame().getActivePlayer()):
            return
        if (city.healthRate(False, 0) < 0):
            message = self.localText.getText(
                    "TXT_KEY_CIV4LERTS_ON_CITY_UNHEALTHY",
                    (city.getName(), city.getPopulation()))
            icon = "Art/Interface/Interface/Buttons/General/unhealthy_person.dds"
            self._addMessageAtCity(player, message, icon, city)

class CityGrowthAngry(AbstractAlert):
#   Displays an alert when a city's population grows and becomes angry.

    def __init__(self, eventManager, *args, **kwargs): 
        super(CityGrowthAngry, self).__init__(eventManager, *args, **kwargs)
        eventManager.addEventHandler("cityGrowth", self.onCityGrowth)

    def onCityGrowth(self, argsList):
        if (not BugAlerts.isShowCityGrowthAngryAlert()):
            return

        city, player = argsList
        if (city.getOwner() != self.gc.getGame().getActivePlayer()):
            return
        if (city.angryPopulation(0) > 0):
            message = self.localText.getText(
                    "TXT_KEY_CIV4LERTS_ON_CITY_ANGRY",
                    (city.getName(), city.getPopulation()))
            icon = "Art/Interface/mainscreen/cityscreen/angry_citizen.dds"
            self._addMessageAtCity(player, message, icon, city)


class AbstractCanHurry(AbstractStatefulAlert):
#   Displays an alert when a city can hurry the current production item.

    def __init__(self, eventManager, hurryType, *args, **kwargs): 
        super(AbstractCanHurry, self).__init__(eventManager, *args, **kwargs)
        eventManager.addEventHandler("cityDoTurn", self.onCityDoTurn)
        eventManager.addEventHandler("cityBuildingUnit", self.onCityBuildingUnit)
        eventManager.addEventHandler("cityBuildingBuilding", self.onCityBuildingBuilding)
        self.hurryType = hurryType

    def onCityDoTurn(self, argsList):
        city, iPlayer = argsList
        if (iPlayer != self.gc.getGame().getActivePlayer()):
            return
        iCity = city.getID()
        
        eHurryType = self.gc.getInfoTypeForString(self.hurryType)
        if (city.canHurry(eHurryType, False) and not self._canHurryCity(iCity)):
            self._addCity(iCity)
            if (city.isProductionBuilding()):
                iType = city.getProductionBuilding()
                if (iType >= 0):
                    info = self.gc.getBuildingInfo(iType)
                    self.onCityCanHurry(city, iPlayer, info.getDescription(), eHurryType)
            elif (city.isProductionUnit()):
                iType = city.getProductionUnit()
                if (iType >= 0):
                    info = self.gc.getUnitInfo(iType)
                    self.onCityCanHurry(city, iPlayer, info.getDescription(), eHurryType)
            elif (city.isProductionProject()):
                # Can't hurry projects, but just in case
                iType = city.getProductionProject()
                if (iType >= 0):
                    info = self.gc.getProjectInfo(iType)
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
        if (city.getOwner() != self.gc.getGame().getActivePlayer()):
            return
        self._removeCity(city.getID())

    def _reset(self, *args, **kwargs):
        super(AbstractCanHurry, self)._reset(*args, **kwargs)
        self.canHurryCities = set()

    def _canHurryCity(self, iCity):
        return iCity in self.canHurryCities

    def _addCity(self, iCity):
        self.canHurryCities.add(iCity)

    def _removeCity(self, iCity):
        self.canHurryCities.discard(iCity)

class CanHurryPopulation(AbstractCanHurry):
#   Displays an alert when a city can hurry using population.

    def __init__(self, eventManager, *args, **kwargs): 
        super(CanHurryPopulation, self).__init__(eventManager, "HURRY_POPULATION", *args, **kwargs)

    def onCityCanHurry(self, city, iPlayer, item, eHurryType):
        iPop = city.hurryPopulation(eHurryType)
        message = self.localText.getText("TXT_KEY_CIV4LERTS_ON_CITY_CAN_HURRY_POP", 
                                         (item, city.getName(), iPop))
        icon = "Art/Interface/mainscreen/cityscreen/angry_citizen.dds"
        self._addMessageAtCity(iPlayer, message, icon, city)

class CanHurryGold(AbstractCanHurry):
#   Displays an alert when a city can hurry using gold.

    def __init__(self, eventManager, *args, **kwargs): 
        super(CanHurryGold, self).__init__(eventManager, "HURRY_GOLD", *args, **kwargs)

    def onCityCanHurry(self, city, iPlayer, item, eHurryType):
        iGold = city.hurryGold(eHurryType)
        message = self.localText.getText("TXT_KEY_CIV4LERTS_ON_CITY_CAN_HURRY_GOLD", 
                                         (item, city.getName(), iGold))
        icon = "Art/Interface/mainscreen/cityscreen/angry_citizen.dds"
        self._addMessageAtCity(iPlayer, message, icon, city)


class GoldTrade(AbstractStatefulAlert):
#   Displays an alert when a civilization has a significant increase
#    in gold available for trade since the last alert.

    def __init__(self, eventManager, *args, **kwargs): 
        super(GoldTrade, self).__init__(eventManager, *args, **kwargs)
        eventManager.addEventHandler("BeginGameTurn", self.onBeginGameTurn)

    def onBeginGameTurn(self, argsList):
        if (not BugAlerts.isShowGoldTradeAlert()):
            return

        turn = argsList[0]
        player = self.gc.getGame().getActivePlayer()
        team = self.gc.getTeam(self.gc.getPlayer(player).getTeam())
        for rival in range(self.gc.getMAX_PLAYERS()):
            if (rival == player): continue
            rivalPlayer = self.gc.getPlayer(rival)
            rivalTeam = self.gc.getTeam(rivalPlayer.getTeam())
            # TODO: does this need to check for war or trade denial?
            if (team.isHasMet(rivalPlayer.getTeam())
                and (team.isGoldTrading() or rivalTeam.isGoldTrading())):
                oldMaxGoldTrade = self._getMaxGoldTrade(player, rival)
                newMaxGoldTrade = rivalPlayer.AI_maxGoldTrade(player)
                deltaMaxGoldTrade = newMaxGoldTrade - oldMaxGoldTrade
                if (deltaMaxGoldTrade >= BugAlerts.getGoldTradeThreshold()):
                    message = self.localText.getText(
                            "TXT_KEY_CIV4LERTS_ON_GOLD_TRADE",
                            (self.gc.getTeam(rival).getName(),
                             newMaxGoldTrade))
                    self._addMessageNoIcon(player, message)
                    self._setMaxGoldTrade(player, rival, newMaxGoldTrade)
                else:
                    maxGoldTrade = min(oldMaxGoldTrade, newMaxGoldTrade)
                    self._setMaxGoldTrade(player, rival, maxGoldTrade)

    def _reset(self, *args, **kwargs):
        super(GoldTrade, self)._reset(*args, **kwargs)
        self.maxGoldTrade = {}
        for player in range(self.gc.getMAX_PLAYERS()):
            self.maxGoldTrade[player] = {}
            for rival in range(self.gc.getMAX_PLAYERS()):
                self._setMaxGoldTrade(player, rival, 0)

    def _getMaxGoldTrade(self, player, rival):
        return self.maxGoldTrade[player][rival]
    
    def _setMaxGoldTrade(self, player, rival, value):
        self.maxGoldTrade[player][rival] = value

class GoldPerTurnTrade(AbstractStatefulAlert):
#   Displays an alert when a civilization has a significant increase
#   in gold per turn available for trade since the last alert.

    def __init__(self, eventManager, *args, **kwargs): 
        super(GoldPerTurnTrade, self).__init__(eventManager, *args, **kwargs)
        eventManager.addEventHandler("BeginGameTurn", self.onBeginGameTurn)

    def onBeginGameTurn(self, argsList):
        if (not BugAlerts.isShowGoldPerTurnTradeAlert()):
            return

        turn = argsList[0]
        player = self.gc.getGame().getActivePlayer()
        team = self.gc.getTeam(self.gc.getPlayer(player).getTeam())
        for rival in range(self.gc.getMAX_PLAYERS()):
            if (rival == player): continue
            rivalPlayer = self.gc.getPlayer(rival)
            rivalTeam = self.gc.getTeam(rivalPlayer.getTeam())
            # TODO: does this need to check for war or trade denial?
            if (team.isHasMet(rivalPlayer.getTeam())
                and (team.isGoldTrading() or rivalTeam.isGoldTrading())):
                oldMaxGoldPerTurnTrade = self._getMaxGoldPerTurnTrade(player, rival)
                newMaxGoldPerTurnTrade = rivalPlayer.AI_maxGoldPerTurnTrade(player)
                deltaMaxGoldPerTurnTrade = newMaxGoldPerTurnTrade - oldMaxGoldPerTurnTrade
                if (deltaMaxGoldPerTurnTrade >= BugAlerts.getGoldPerTurnTradeThreshold()):
                    message = self.localText.getText(
                            "TXT_KEY_CIV4LERTS_ON_GOLD_PER_TURN_TRADE",
                            (self.gc.getTeam(rival).getName(),
                             newMaxGoldPerTurnTrade))
                    self._addMessageNoIcon(player, message)
                    self._setMaxGoldPerTurnTrade(player, rival, newMaxGoldPerTurnTrade)
                else:
                    maxGoldPerTurnTrade = min(oldMaxGoldPerTurnTrade, newMaxGoldPerTurnTrade)
                    self._setMaxGoldPerTurnTrade(player, rival, maxGoldPerTurnTrade)

    def _reset(self, *args, **kwargs):
        super(GoldPerTurnTrade, self)._reset(*args, **kwargs)
        self.maxGoldPerTurnTrade = {}
        for player in range(self.gc.getMAX_PLAYERS()):
            self.maxGoldPerTurnTrade[player] = {}
            for rival in range(self.gc.getMAX_PLAYERS()):
                self._setMaxGoldPerTurnTrade(player, rival, 0)

    def _getMaxGoldPerTurnTrade(self, player, rival):
        return self.maxGoldPerTurnTrade[player][rival]
    
    def _setMaxGoldPerTurnTrade(self, player, rival, value):
        self.maxGoldPerTurnTrade[player][rival] = value
