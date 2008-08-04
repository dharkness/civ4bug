## autologger
## Modified from Ruff Mod 2w
## Modified from HOF MOD V1.61.001
## Modified from autolog by eotinb
## autolog's subclass of CvEventManager
## by eotinb
##-------------------------------------------------------------------
## Reorganized to work via CvCustomEventManager
## using Civ4lerts as template.
## CvCustomEventManager & Civ4lerts by Gillmer J. Derge
##-------------------------------------------------------------------
##
## TODO:
## - Use onPlayerChangeStateReligion event

from CvPythonExtensions import *
import CvUtil
import Popup as PyPopup
import PyHelpers
import autolog
import time
import BugAutologOptions
import BugUtil
import CvModName

BugAutolog = BugAutologOptions.BugAutologOptions()

gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer
PyInfo = PyHelpers.PyInfo

Logger = autolog.autologInstance()
lPercent = "%"

def StartLogger(vsFileName):

	if (BugAutolog.isUseDefaultFileName()
		or BugAutolog.isSilent()
		or not vsFileName):
		ePlayer = gc.getGame().getActivePlayer()
		szfileName = gc.getPlayer(ePlayer).getName()
	else:
		szfileName = vsFileName

	ziStyle = BugAutolog.getFormatStyle()
#	' valid styles are plain (0), html (1), forum with " for color(2) or forum without " for color(3)'
	if (ziStyle == 1):
		if not (szfileName.endswith(".html")):
			szfileName = szfileName + ".html"
	else:
		if not (szfileName.endswith(".txt")):
			szfileName = szfileName + ".txt"

	Logger.setLogFileName(szfileName)
	Logger.writeLog("")
	Logger.writeLog("Logging by " + CvModName.getNameAndVersion() + " (" + CvModName.getCivNameAndVersion() + ")")
	Logger.writeLog("------------------------------------------------")
	
	zcurrturn = gc.getGame().getElapsedGameTurns() + BugAutolog.get4000BCTurn()
	zmaxturn = gc.getGame().getMaxTurns()
	zyear = gc.getGame().getGameTurnYear()
	if (zyear < 0):
		zyear = str(-zyear) + " BC"
	else:
		zyear = str(zyear) + " AD"
	zCurrDateTime = time.strftime("%d-%b-%Y %H:%M:%S")

	if (zmaxturn == 0):
		zsTurn = "%i" % (zcurrturn)
	else:
		zsTurn = "%i/%i" % (zcurrturn, zmaxturn)
				
	message = BugUtil.getText("TXT_KEY_AUTOLOG_TURN", (zsTurn, zyear, zCurrDateTime))
	
	Logger.writeLog(message, vBold=True, vUnderline=True)

	if (not BugAutolog.isSilent()):
		message = "Logging Game to File: %s" % (szfileName)
		CyInterface().addMessage(CyGame().getActivePlayer(), True, 10, message, None, 2, None, ColorTypes(8), 0, 0, False, False)

class autologEventManager:

	def __init__(self, eventManager):

		AutoLogEvent(eventManager)

		# additions to self.Events
		moreEvents = {
			CvUtil.EventLogOpen : ('LogOpenPopup', self.__eventLogOpenApply, self.__eventLogOpenBegin),
			CvUtil.EventCustomLogEntry : ('', self.__eventCustomLogEntryApply, self.__eventCustomLogEntryBegin),
		}
		eventManager.Events.update(moreEvents)

	def __eventLogOpenBegin(self, argsList):
		popup = PyPopup.PyPopup(CvUtil.EventLogOpen, EventContextTypes.EVENTCONTEXT_SELF)

		if (BugAutolog.isUseDefaultFileName()):
			popup.setHeaderString("Do you want to log this game?")
			popup.setBodyString("OK for YES, Cancel for NO")
		else:
			popup.setHeaderString("Enter new or existing log file name")
			popup.createEditBox(BugAutolog.getFileName())
			popup.setEditBoxMaxCharCount( 30 )

		popup.addButton("OK")
		popup.addButton("Cancel")
		popup.launch(False, PopupStates.POPUPSTATE_IMMEDIATE)

	def __eventLogOpenApply(self, playerID, userData, popupReturn):
		if (popupReturn.getButtonClicked() != 1):
			BugAutolog.setLoggingOn(True)
			StartLogger(popupReturn.getEditBoxString(0))
		else:
			BugAutolog.setLoggingOn(False)
			message = "No Logging of this Game"
			CyInterface().addMessage(CyGame().getActivePlayer(), True, 10, message, None, 2, None, ColorTypes(8), 0, 0, False, False)

	def __eventCustomLogEntryBegin(self, argsList):
		if BugAutolog.isLoggingOn():
			popup = PyPopup.PyPopup(CvUtil.EventCustomLogEntry, EventContextTypes.EVENTCONTEXT_SELF)
			popup.setHeaderString("Enter custom log entry")
			popup.createEditBox("")
			popup.addButton("OK")
			popup.addButton("Cancel")
			popup.launch(False, PopupStates.POPUPSTATE_IMMEDIATE)

	def __eventCustomLogEntryApply(self, playerID, userData, popupReturn):
		if BugAutolog.isLoggingOn():
			message = popupReturn.getEditBoxString(0)
			if (popupReturn.getButtonClicked() != 1):
				Logger.writeLog(message, vPrefix=BugAutolog.getPrefix())

				if (not BugAutolog.isSilent()):
					CyInterface().addMessage(CyGame().getActivePlayer(), True, 10, message, None, 2, None, ColorTypes(8), 0, 0, False, False)

class AbstractAutoLogEvent(object):

	def __init__(self, eventManager, *args, **kwargs):
		super(AbstractAutoLogEvent, self).__init__(*args, **kwargs)

class AutoLogEvent(AbstractAutoLogEvent):

	def __init__(self, eventManager, *args, **kwargs):
		super(AutoLogEvent, self).__init__(eventManager, *args, **kwargs)

		eventManager.addEventHandler("kbdEvent", self.onKbdEvent)
		eventManager.addEventHandler("OnLoad", self.onLoadGame)
		eventManager.addEventHandler("GameStart", self.onGameStart)
		eventManager.addEventHandler("GameEnd", self.onGameEnd)
		eventManager.addEventHandler("EndGameTurn", self.onEndGameTurn)
		eventManager.addEventHandler("BeginPlayerTurn", self.onBeginPlayerTurn)
		eventManager.addEventHandler("EndPlayerTurn", self.onEndPlayerTurn)
		eventManager.addEventHandler("firstContact", self.onFirstContact)
		eventManager.addEventHandler("combatLogCalc", self.onCombatLogCalc)
		eventManager.addEventHandler("combatResult", self.onCombatResult)
		eventManager.addEventHandler("combatLogHit", self.onCombatLogHit)
		eventManager.addEventHandler("buildingBuilt", self.onBuildingBuilt)
		eventManager.addEventHandler("projectBuilt", self.onProjectBuilt)
		eventManager.addEventHandler("unitBuilt", self.onUnitBuilt)
		eventManager.addEventHandler("unitPromoted", self.onUnitPromoted)
		eventManager.addEventHandler("goodyReceived", self.onGoodyReceived)
		eventManager.addEventHandler("greatPersonBorn", self.onGreatPersonBorn)
		eventManager.addEventHandler("techAcquired", self.onTechAcquired)
		eventManager.addEventHandler("techSelected", self.onTechSelected)
		eventManager.addEventHandler("religionFounded", self.onReligionFounded)
		eventManager.addEventHandler("religionSpread", self.onReligionSpread)
		eventManager.addEventHandler("religionRemove", self.onReligionRemove)
		eventManager.addEventHandler("corporationFounded", self.onCorporationFounded)
		eventManager.addEventHandler("corporationSpread", self.onCorporationSpread)
		eventManager.addEventHandler("corporationRemove", self.onCorporationRemove)
		eventManager.addEventHandler("goldenAge", self.onGoldenAge)
		eventManager.addEventHandler("endGoldenAge", self.onEndGoldenAge)
		eventManager.addEventHandler("changeWar", self.onChangeWar)
		eventManager.addEventHandler("setPlayerAlive", self.onSetPlayerAlive)
		eventManager.addEventHandler("cityBuilt", self.onCityBuilt)
		eventManager.addEventHandler("cityRazed", self.onCityRazed)
		eventManager.addEventHandler("cityAcquired", self.onCityAcquired)
		eventManager.addEventHandler("cityLost", self.onCityLost)
		eventManager.addEventHandler("cultureExpansion", self.onCultureExpansion)
		eventManager.addEventHandler("cityGrowth", self.onCityGrowth)
		eventManager.addEventHandler("cityBuildingUnit", self.onCityBuildingUnit)
		eventManager.addEventHandler("cityBuildingBuilding", self.onCityBuildingBuilding)
		eventManager.addEventHandler("improvementBuilt", self.onImprovementBuilt)
		eventManager.addEventHandler("improvementDestroyed", self.onImprovementDestroyed)
		eventManager.addEventHandler("unitPillage", self.onUnitPillage)
		eventManager.addEventHandler("vassalState", self.onVassalState)
		eventManager.addEventHandler("selectionGroupPushMission", self.onSelectionGroupPushMission)

		self.eventMgr = eventManager
		self.fOdds = 0.0
		self.iBattleWonDefending = 0
		self.iBattleLostDefending = 0
		self.iBattleWonAttacking = 0
		self.iBattleLostAttacking = 0
		self.iBattleWdlAttacking = 0
		self.iBattleEscAttacking = 0

		self.bHumanPlaying = False
		self.bHumanEndTurn = False
		self.bAIsTurn = False

		self.UnitKilled = 0
		self.WonLastRound = 0
		self.WdlAttacker = None
		self.WdlDefender = None
		
		self.CIVAttitude = None
		self.CIVCivics = None
		self.CIVReligion = None
		self.CityWhipCounter = None
		self.CityConscriptCounter = None

	def onKbdEvent(self, argsList):
		eventType,key,mx,my,px,py = argsList
		if ( eventType == self.eventMgr.EventKeyDown ):
			theKey=int(key)
			'Check if ALT + E was hit == echoes to text log and in-game log'
			if (theKey == int(InputTypes.KB_E)
			and self.eventMgr.bAlt
			and BugAutolog.isEnabled()
			and BugAutolog.isLoggingOn()):
				self.eventMgr.beginEvent(CvUtil.EventCustomLogEntry)
				return 1

			'Check if ALT + L was hit == open in-game log'
			if (theKey == int(InputTypes.KB_L)
			and self.eventMgr.bAlt
			and BugAutolog.isEnabled()):
				if BugAutolog.isSilent():
					BugAutolog.setLoggingOn(True)
					StartLogger("")
				else:
					self.eventMgr.beginEvent(CvUtil.EventLogOpen)

				return 1

			'Check if ALT + B was hit == dump battle stats, and reset'
			if (theKey == int(InputTypes.KB_B)
			and self.eventMgr.bAlt
			and BugAutolog.isEnabled()
			and BugAutolog.isLoggingOn()):
				Logger.writeLog("")
				Logger.writeLog("Battle Stats:", vBold=True)
				message = BugUtil.getText("TXT_KEY_AUTOLOG_UNITS_VICTORIOUS_ATTACKING", (self.iBattleWonAttacking, ))
				Logger.writeLog(message, vColor="DarkRed")
				message = BugUtil.getText("TXT_KEY_AUTOLOG_UNITS_VICTORIOUS_DEFENDING", (self.iBattleWonDefending, ))
				Logger.writeLog(message, vColor="DarkRed")
				message = BugUtil.getText("TXT_KEY_AUTOLOG_UNITS_WITHDRAWING_ATTACKING", (self.iBattleWdlAttacking, ))
				Logger.writeLog(message, vColor="DarkRed")
				message = BugUtil.getText("TXT_KEY_AUTOLOG_UNITS_DEFEATED_ATTACKING", (self.iBattleLostAttacking, ))
				Logger.writeLog(message, vColor="Red")
				message = BugUtil.getText("TXT_KEY_AUTOLOG_UNITS_DEFEATED_DEFENDING", (self.iBattleLostDefending, ))
				Logger.writeLog(message, vColor="Red")
				message = BugUtil.getText("TXT_KEY_AUTOLOG_UNITS_ESCAPING_ATTACKING", (self.iBattleEscAttacking, ))
				Logger.writeLog(message, vColor="Red")

				self.iBattleWonDefending = 0
				self.iBattleLostDefending = 0
				self.iBattleWonAttacking = 0
				self.iBattleLostAttacking = 0
				self.iBattleWdlAttacking = 0
				self.iBattleEscAttacking = 0

				message = "Battle stats written to log & reset"
				CyInterface().addMessage(CyGame().getActivePlayer(), True, 10, message, None, 2, None, ColorTypes(8), 0, 0, False, False)
				return 1

			'Check if ALT + T was hit == testing!'
#			if (theKey == int(InputTypes.KB_T)
#			and self.eventMgr.bAlt):
#				message = "Civ / Civic %i %i %i" % (0, 0, self.CIVCivics[0])
#				CyInterface().addMessage(CyGame().getActivePlayer(), True, 10, message, None, 2, None, ColorTypes(8), 0, 0, False, False)

#				self.storeStuff()
#				return 1

			'Check if ALT + T was hit == testing!'
			if (theKey == int(InputTypes.KB_T)
			and self.eventMgr.bAlt):
				for i in range(0, 126):   #range(0,1000000):
					ci = gc.getColorInfo(i)
					ci2 = "XML Val %i %s" % (i, ci.getXmlVal())
					print ci2


	def onLoadGame(self, argsList):
		self.bHumanPlaying = True
		self.bHumanEndTurn = False
		self.bAIsTurn = False

		if (BugAutolog.isEnabled()
		and BugAutolog.isSilent()):
			BugAutolog.setLoggingOn(True)
			StartLogger("")
		else:
			BugAutolog.setLoggingOn(False)

		# initialize storage stuff
		self.initStuff()
		self.storeStuff()
		self.storeWhip()

	def onGameStart(self, argsList):
		self.bHumanPlaying = True
		self.bHumanEndTurn = False
		self.bAIsTurn = False

		if (BugAutolog.isEnabled()
		and BugAutolog.isSilent()):
			BugAutolog.setLoggingOn(True)
			StartLogger("")
		else:
			BugAutolog.setLoggingOn(False)

		# initialize storage stuff
		self.initStuff()
		self.storeStuff()
		self.storeWhip()

	def onGameEnd(self, argsList):
		'Called at the End of the game'

	def onEndGameTurn(self, argsList):
		iGameTurn = argsList[0]

		if BugAutolog.isLoggingOn():
			self.checkStuff()
#			self.dumpStuff()
			self.storeStuff()

			zcurrturn = gc.getGame().getElapsedGameTurns() + 1 + BugAutolog.get4000BCTurn()
			zmaxturn = gc.getGame().getMaxTurns()
			zturn = gc.getGame().getGameTurn() + 1
			zyear = gc.getGame().getTurnYear(zturn)
			if (zyear < 0):
				zyear = str(-zyear) + " BC"
			else:
				zyear = str(zyear) + " AD"
			zCurrDateTime = time.strftime("%d-%b-%Y %H:%M:%S")

			if (zmaxturn == 0):
				zsTurn = "%i" % (zcurrturn)
			else:
				zsTurn = "%i/%i" % (zcurrturn, zmaxturn)
				
			message = BugUtil.getText("TXT_KEY_AUTOLOG_TURN", (zsTurn, zyear, zCurrDateTime))

			Logger.writeLog_pending_flush()
			Logger.writeLog_pending("")
			Logger.writeLog_pending(message, vBold=True, vUnderline=True)

		self.bHumanPlaying = True
		self.bHumanEndTurn = False
		self.bAIsTurn = False

	def onBeginPlayerTurn(self, argsList):
		'Called at the beginning of a players turn'
		iGameTurn, iPlayer = argsList

		if iPlayer == CyGame().getActivePlayer():
			self.bHumanPlaying = False
			self.bHumanEndTurn = True
			self.bAIsTurn = False

		if not self.bHumanEndTurn:
			return

		if BugAutolog.isShowIBT():
#			Logger.writeLog_pending_flush()
			Logger.writeLog_pending("")
			Logger.writeLog_pending("After End Turn:", vBold=True)
#			Logger.writeLog("After End Turn-:", vBold=True)

		if BugAutolog.isLogCityWhipStatus():
			iPlayer = gc.getActivePlayer()
			for i in range(0, iPlayer.getNumCities(), 1):
				iCity = iPlayer.getCity(i)
				iCurrentWhipCounter = iCity.getHurryAngerTimer()
				iCurrentConstrictCounter = iCity.getConscriptAngerTimer()
#				if iCurrentWhipCounter != 0: iCurrentWhipCounter += 1  # onBeginPlayerTurn fires after whip counter has decreased by 1

#				message = "Whip Testing: %s, current(%i), prior(%i), flat(%i)" % (iCity.getName(), iCurrentWhipCounter, self.CityWhipCounter[i], iCity.flatHurryAngerLength())
#				Logger.writeLog(message)

				if iCurrentWhipCounter > self.CityWhipCounter[i]:
					message = BugUtil.getText("TXT_KEY_AUTOLOG_WHIP_APPLIED", (iCity.getName(), ))
					Logger.writeLog(message, vColor="Red")

				if iCurrentConstrictCounter > self.CityConscriptCounter[i]:
					message = BugUtil.getText("TXT_KEY_AUTOLOG_CONSCRIPT", (gc.getUnitInfo(iCity.getConscriptUnit()).getDescription(), iCity.getName()))
					Logger.writeLog(message, vColor="Red")

				if (self.CityWhipCounter[i] != 0
				and iCurrentWhipCounter < self.CityWhipCounter[i]
				and iCurrentWhipCounter % iCity.flatHurryAngerLength() == 0):
					message = BugUtil.getText("TXT_KEY_AUTOLOG_WHIP_ANGER_DECREASED", (iCity.getName(), ))
					Logger.writeLog(message, vColor="DarkRed")

				if (self.CityConscriptCounter[i] != 0
				and iCurrentConstrictCounter < self.CityConscriptCounter[i]
				and iCurrentConstrictCounter % iCity.flatConscriptAngerLength() == 0):
					message = BugUtil.getText("TXT_KEY_AUTOLOG_DRAFT_ANGER_DECREASED", (iCity.getName(), ))
					Logger.writeLog(message, vColor="DarkRed")

			self.storeWhip()

	def onEndPlayerTurn(self, argsList):
		'Called at the end of a players turn'
		iGameTurn, iPlayer = argsList

		if (self.bHumanEndTurn
		and BugAutolog.isShowIBT()):
			Logger.writeLog_pending_flush()
			Logger.writeLog_pending("")
			Logger.writeLog_pending("Other Player Actions:", vBold=True)
#			Logger.writeLog("Other Player Actions-:", vBold=True)

		if iPlayer == CyGame().getActivePlayer():
			self.bHumanPlaying = False
			self.bHumanEndTurn = False
			self.bAIsTurn = True

	def onFirstContact(self, argsList):
		if (BugAutolog.isLogContact()):
			iTeamX,iHasMetTeamY = argsList
			if (iTeamX == 0
			and gc.getGame().getGameTurn() > 0):
					civMet = PyPlayer(gc.getTeam(iHasMetTeamY).getLeaderID())
					message = BugUtil.getText("TXT_KEY_AUTOLOG_FIRST_CONTACT", (civMet.getCivilizationName(), ))
					Logger.writeLog(message, vColor="Brown")

	def onCombatLogCalc(self, argsList):
		if (BugAutolog.isLogCombat()):
			genericArgs = argsList[0][0]
			cdAttacker = genericArgs[0]
			cdDefender = genericArgs[1]
			iCombatOdds = genericArgs[2]

			self.fOdds = float(iCombatOdds)/10

			self.UnitKilled = 0
			self.WonLastRound = 0

	def onCombatResult(self, argsList):
		if (BugAutolog.isLogCombat()):

			self.UnitKilled = 1

			pWinner,pLoser = argsList
			if (pWinner.getOwner() == CyGame().getActivePlayer()
			or pLoser.getOwner() == CyGame().getActivePlayer()):
				playerX = PyPlayer(pWinner.getOwner())
				playerY = PyPlayer(pLoser.getOwner())
				winnerHealth = float(pWinner.baseCombatStr()) * float(pWinner.currHitPoints()) / float(pWinner.maxHitPoints())
				zsBattleLocn = self.getUnitLocation(pWinner)
				text1 = "%.2f" % winnerHealth
				text2 = "%.1f" % self.fOdds

				if (pWinner.getOwner() == CyGame().getActivePlayer()):
					if (self.bHumanPlaying):
						message = BugUtil.getText("TXT_KEY_AUTOLOG_WHILE_ATTACKING_DEFEATS", (zsBattleLocn, pWinner.getName(), text1, pWinner.baseCombatStr(), playerY.getCivilizationAdjective(), pLoser.getName(), text2, lPercent))
						self.iBattleWonAttacking = self.iBattleWonAttacking + 1
					else:
						self.fOdds = 100 - self.fOdds
						message = BugUtil.getText("TXT_KEY_AUTOLOG_WHILE_DEFENDING_DEFEATS", (zsBattleLocn, pWinner.getName(), text1, pWinner.baseCombatStr(), playerY.getCivilizationAdjective(), pLoser.getName(), text2, lPercent))
						self.iBattleWonDefending = self.iBattleWonDefending + 1

					Logger.writeLog(message, vColor="DarkRed")

				else:
					if (self.bHumanPlaying):
						message = BugUtil.getText("TXT_KEY_AUTOLOG_WHILE_ATTACKING_LOSES", (zsBattleLocn, pLoser.getName(), playerX.getCivilizationAdjective(), pWinner.getName(), text1, pWinner.baseCombatStr(), text2, lPercent))
						self.iBattleLostAttacking = self.iBattleLostAttacking + 1
					else:
						self.fOdds = 100 - self.fOdds
						message = BugUtil.getText("TXT_KEY_AUTOLOG_WHILE_DEFENDING_LOSES", (zsBattleLocn, pLoser.getName(), playerX.getCivilizationAdjective(), pWinner.getName(), text1, pWinner.baseCombatStr(), text2, lPercent))
						self.iBattleLostDefending = self.iBattleLostDefending + 1

					Logger.writeLog(message, vColor="Red")

	def onCombatLogHit(self, argsList):
		'Combat Message'
		genericArgs = argsList[0][0]
		cdAttacker = genericArgs[0]
		cdDefender = genericArgs[1]
		iIsAttacker = genericArgs[2]
		iDamage = genericArgs[3]

		self.WdlAttacker = cdAttacker
		self.WdlDefender = cdDefender
		
		if (iIsAttacker == 0):
			self.WonLastRound = 0
			
		elif (iIsAttacker == 1):
			self.WonLastRound = 1

	def onSelectionGroupPushMission(self, argsList):
		'selection group mission'
		eOwner = argsList[0]
		eMission = argsList[1]
		iNumUnits = argsList[2]
		listUnitIds = argsList[3]

#		print eOwner, eMission, iNumUnits, listUnitIds

		if self.WdlDefender == None: return

		if (BugAutolog.isLogCombat()
		and gc.getPlayer(eOwner).getTeam() == gc.getActivePlayer().getTeam()):

			playerX = PyPlayer(self.WdlDefender.eOwner)
			defCivName = playerX.getCivilizationAdjective()

			if self.UnitKilled == 0:
				if self.WonLastRound == 1:
					sAction = "escapes from"
					message = "While attacking, %s %s %s %s (Prob Victory: %.1f%s)" %(self.WdlAttacker.sUnitName, sAction, defCivName, self.WdlDefender.sUnitName, self.fOdds, lPercent)
					Logger.writeLog(message, vColor="Red")
					self.iBattleEscAttacking = self.iBattleEscAttacking + 1
				else:
					sAction = "decimates"
					message = "While attacking, %s %s %s %s (Prob Victory: %.1f%s)" %(self.WdlAttacker.sUnitName, sAction, defCivName, self.WdlDefender.sUnitName, self.fOdds, lPercent)
					Logger.writeLog(message, vColor="DarkRed")
					self.iBattleWdlAttacking = self.iBattleWdlAttacking + 1

		self.WdlDefender = None

	def getUnitLocation(self, objUnit):
		iX = objUnit.getX()
		iY = objUnit.getY()
		pPlot = CyMap().plot(iX,iY)
		zOwner = pPlot.getOwner()
		if (zOwner == -1):
			if (pPlot.isWater()):
				if (pPlot.isLake()):
					zsLocn1 = "on a lake"
				elif (pPlot.isAdjacentToLand()):
					zsLocn1 = "just off shore"
				else:
					zsLocn1 = "on the high seas"
			else:
				zsLocn1 = "in the wild"
		else:
			playerX = PyPlayer(zOwner)
			zsLocn1 = "in %s territory" %(playerX.getCivilizationAdjective())

		for iiX in range(iX-1, iX+2, 1):
			for iiY in range(iY-1, iY+2, 1):
				pPlot = CyMap().plot(iiX,iiY)
				if (pPlot.isCity()):
					zsCity = pPlot.getPlotCity()
					return "%s at %s" % (zsLocn1, zsCity.getName())

		for iiX in range(iX-4, iX+5, 1):
			for iiY in range(iY-4, iY+5, 1):
				pPlot = CyMap().plot(iiX,iiY)
				if (pPlot.isCity()):
					zsCity = pPlot.getPlotCity()
					return "%s near %s" % (zsLocn1, zsCity.getName())

		return zsLocn1

	def onBuildingBuilt(self, argsList):
		if (BugAutolog.isLogBuildCompleted()):
			pCity, iBuildingType = argsList
			if pCity.getOwner() == CyGame().getActivePlayer():
				message = "%s finishes: %s"%(pCity.getName(),gc.getBuildingInfo(iBuildingType).getDescription())
				Logger.writeLog(message, vColor="Purple")

	def onProjectBuilt(self, argsList):
		if (BugAutolog.isLogBuildCompleted()):
			pCity, iProjectType = argsList
			if pCity.getOwner() == CyGame().getActivePlayer():
				message = "%s finishes: %s"%(pCity.getName(),gc.getProjectInfo(iProjectType).getDescription())
				Logger.writeLog(message, vColor="Purple")

	def onUnitBuilt(self, argsList):
		if (BugAutolog.isLogBuildCompleted()):
			city = argsList[0]
			unit = argsList[1]
			if city.getOwner() == CyGame().getActivePlayer():
				message = "%s finishes: %s"%(city.getName(),gc.getUnitInfo(unit.getUnitType()).getDescription())
				Logger.writeLog(message, vColor="Purple")

	def onUnitPromoted(self, argsList):
		if (BugAutolog.isLogPromotion()):
			pUnit, iPromotion = argsList
			if pUnit.getOwner() == CyGame().getActivePlayer():
				message = "%s promoted: %s" % (pUnit.getName(), PyInfo.PromotionInfo(iPromotion).getDescription())
				Logger.writeLog(message, vColor="DarkOrange")

	def onGoodyReceived(self, argsList):
		if (BugAutolog.isLogTribalVillage()):
			iPlayer, pPlot, pUnit, iGoodyType = argsList
			if iPlayer == CyGame().getActivePlayer():
				GoodyTypeMap = {
						-1: 'nothing',
						0:	'a little gold',
						1:	'lots of gold',
						2:	'map',
						3:	'settler',
						4:	'warrior',
						5:	'scout',
						6:	'worker',
						7:	'experience',
						8:	'healing',
						9:	'technology',
						10:	'weak hostiles',
						11: 'strong hostiles'
					}
				message = "Tribal village results: %s" % (GoodyTypeMap[iGoodyType])
				Logger.writeLog(message, vColor="Brown")

	def onGreatPersonBorn(self, argsList):
		if (BugAutolog.isLogGreatPeople()):
			pUnit, iPlayer, pCity = argsList
			if iPlayer == CyGame().getActivePlayer():
				message = "%s born in %s" % (pUnit.getName(), pCity.getName())
				Logger.writeLog(message, vColor="Brown")

	def onTechAcquired(self, argsList):
		if gc.getGame().getGameTurn() == 0:
			return
		
		if (BugAutolog.isLogTechnology()):
			iTechType, iTeam, iPlayer, bAnnounce = argsList

			bWrite = False
			if iPlayer == CyGame().getActivePlayer():
				bWrite = True

				if self.bHumanEndTurn:
					message = "Tech research finished: %s"%(PyInfo.TechnologyInfo(iTechType).getDescription())
				else:
					message = "Tech acquired (trade, lightbulb, hut, espionage): %s"%(PyInfo.TechnologyInfo(iTechType).getDescription())
			else:
				if self.bHumanPlaying:
					bWrite = True
					zsCiv = gc.getPlayer(iPlayer).getName() + "(" + gc.getPlayer(iPlayer).getCivilizationShortDescription(0) + ")"
					message = "Tech traded to %s: %s"%(zsCiv, PyInfo.TechnologyInfo(iTechType).getDescription())

			if bWrite:
				Logger.writeLog(message, vColor="Green")

	def onTechSelected(self, argsList):
		if (BugAutolog.isLogTechnology()):
			iTechType, iPlayer = argsList
			if iPlayer == CyGame().getActivePlayer():
				researchProgress = gc.getTeam(gc.getPlayer(iPlayer).getTeam()).getResearchProgress(gc.getPlayer(iPlayer).getCurrentResearch())
				overflowResearch = (gc.getPlayer(iPlayer).getOverflowResearch() * gc.getPlayer(iPlayer).calculateResearchModifier(gc.getPlayer(iPlayer).getCurrentResearch()))/100
				researchCost = gc.getTeam(gc.getPlayer(iPlayer).getTeam()).getResearchCost(gc.getPlayer(iPlayer).getCurrentResearch())
				researchRate = gc.getPlayer(iPlayer).calculateResearchRate(-1)
				zTurns = (researchCost - researchProgress - overflowResearch) / researchRate + 1

				message = "Research begun: %s (%i Turns)" %(PyInfo.TechnologyInfo(iTechType).getDescription(), zTurns)
				Logger.writeLog(message, vColor="Green")

	def onReligionFounded(self, argsList):
		if (BugAutolog.isLogReligion()):
			iReligion, iFounder = argsList
			player = PyPlayer(iFounder)
			iCityId = gc.getGame().getHolyCity(iReligion).getID()
			if (player.getTeamID() == 0):
				messageEnd = gc.getPlayer(iFounder).getCity(iCityId).getName()
			else:
				messageEnd = "a distant land"
			message = "%s founded in %s" % (gc.getReligionInfo(iReligion).getDescription(), messageEnd)
			Logger.writeLog(message, vColor="DarkOrange")

	def onReligionSpread(self, argsList):
		if (BugAutolog.isLogReligion()):
			iReligion, iOwner, pSpreadCity = argsList
			player = PyPlayer(iOwner)

			if gc.getGame().getHolyCity(iReligion).getOwner() == CyGame().getActivePlayer() or pSpreadCity.getOwner() == CyGame().getActivePlayer():
				if (pSpreadCity.getOwner() == CyGame().getActivePlayer()):
					message = "%s has spread: %s" % (gc.getReligionInfo(iReligion).getDescription(), pSpreadCity.getName())
				else:
					message = "%s has spread: %s (%s)" % (gc.getReligionInfo(iReligion).getDescription(), pSpreadCity.getName(), player.getCivilizationName())
				Logger.writeLog(message, vColor="DarkOrange")

	def onReligionRemove(self, argsList):
		if (BugAutolog.isLogReligion()):
			iReligion, iOwner, pRemoveCity = argsList
			player = PyPlayer(iOwner)

			if gc.getGame().getHolyCity(iReligion).getOwner() == CyGame().getActivePlayer() or pRemoveCity.getOwner() == CyGame().getActivePlayer():
				if (pRemoveCity.getOwner() == CyGame().getActivePlayer()):
					message = "%s has been removed: %s" % (gc.getReligionInfo(iReligion).getDescription(), pRemoveCity.getName())
				else:
					message = "%s has been removed: %s (%s)" % (gc.getReligionInfo(iReligion).getDescription(), pRemoveCity.getName(), player.getCivilizationName())
				Logger.writeLog(message, vColor="DarkOrange")

	def onCorporationFounded(self, argsList):
		if (BugAutolog.isLogCorporation()):
			iCorporation, iFounder = argsList
			player = PyPlayer(iFounder)
			iCityId = gc.getGame().getHeadquarters(iCorporation).getID()
			if (player.getTeamID() == 0):
				messageEnd = gc.getPlayer(iFounder).getCity(iCityId).getName()
			else:
				messageEnd = "a distant land"
			message = "%s founded in %s" % (gc.getCorporationInfo(iCorporation).getDescription(), messageEnd)
			Logger.writeLog(message, vColor="DarkOrange")

	def onCorporationSpread(self, argsList):
		if (BugAutolog.isLogCorporation()):
			iCorporation, iOwner, pSpreadCity = argsList
			player = PyPlayer(iOwner)

			if gc.getGame().getHeadquarters(iCorporation).getOwner() == CyGame().getActivePlayer() or pSpreadCity.getOwner() == CyGame().getActivePlayer():
				if (pSpreadCity.getOwner() == CyGame().getActivePlayer()):
					message = "%s has spread: %s" % (gc.getCorporationInfo(iCorporation).getDescription(), pSpreadCity.getName())
				else:
					message = "%s has spread: %s (%s)" % (gc.getCorporationInfo(iCorporation).getDescription(), pSpreadCity.getName(), player.getCivilizationName())
				Logger.writeLog(message, vColor="DarkOrange")

	def onCorporationRemove(self, argsList):
		if (BugAutolog.isLogCorporation()):
			iCorporation, iOwner, pRemoveCity = argsList
			player = PyPlayer(iOwner)

			if gc.getGame().getHeadquarters(iCorporation).getOwner() == CyGame().getActivePlayer() or pRemoveCity.getOwner() == CyGame().getActivePlayer():
				if (pRemoveCity.getOwner() == CyGame().getActivePlayer()):
					message = "%s has been removed: %s" % (gc.getCorporationInfo(iCorporation).getDescription(), pRemoveCity.getName())
				else:
					message = "%s has been removed: %s (%s)" % (gc.getCorporationInfo(iCorporation).getDescription(), pRemoveCity.getName(), player.getCivilizationName())
				Logger.writeLog(message, vColor="DarkOrange")

	def onGoldenAge(self, argsList):
		if (BugAutolog.isLogGoldenAge()):
			iPlayer = argsList[0]
			if iPlayer == CyGame().getActivePlayer():
				message = "Golden Age begins"
				Logger.writeLog(message, vColor="Brown")

	def onEndGoldenAge(self, argsList):
		if (BugAutolog.isLogGoldenAge()):
			iPlayer = argsList[0]
			if iPlayer == CyGame().getActivePlayer():
				message = "Golden Age ends"
				Logger.writeLog(message, vColor="Brown")

	def onChangeWar(self, argsList):
		bIsWar = argsList[0]
		iPlayer = argsList[1]
		iRivalTeam = argsList[2]

		if (gc.getGame().isFinalInitialized()
		and BugAutolog.isLogWar()):

#			Civ1 declares war on Civ2
			iCiv1 = iPlayer
			iCiv2 = gc.getTeam(iRivalTeam).getLeaderID()
			zsCiv1 = gc.getPlayer(iCiv1).getName() + "(" + gc.getPlayer(iCiv1).getCivilizationShortDescription(0) + ")"
			zsCiv2 = gc.getPlayer(iCiv2).getName() + "(" + gc.getPlayer(iCiv2).getCivilizationShortDescription(0) + ")"

			if (gc.getTeam(gc.getPlayer(iCiv1).getTeam()).isHasMet(gc.getActivePlayer().getTeam())
			and gc.getTeam(gc.getPlayer(iCiv2).getTeam()).isHasMet(gc.getActivePlayer().getTeam())):
				if (bIsWar):
					message = "%s declares war on %s" % (zsCiv1, zsCiv2)
					Logger.writeLog(message, vColor="Red")
				else:
					message = "%s and %s have signed a peace treaty" % (zsCiv1, zsCiv2)
					Logger.writeLog(message, vColor="DarkRed")

	def onSetPlayerAlive(self, argsList):
		if (BugAutolog.isLogWar()):
			iPlayerID = argsList[0]
			bNewValue = argsList[1]
			if not (bNewValue):
				if (gc.getTeam(gc.getPlayer(iPlayerID).getTeam()).isHasMet(gc.getActivePlayer().getTeam())):
					message = "%s has been eliminated" % (PyPlayer(iPlayerID).getCivDescription())
				else:
					message = "Another civilization has been eliminated"

				Logger.writeLog(message, vColor="Red")

	def onCityBuilt(self, argsList):
		if (BugAutolog.isLogCityFounded()):
			city = argsList[0]
			if city.getOwner() == CyGame().getActivePlayer():
				message = "%s founded"%(city.getName())
				Logger.writeLog(message, vColor="RoyalBlue")

	def onCityRazed(self, argsList):
		if (BugAutolog.isLogCityRazed()):
			city, iPlayer = argsList
			owner = PyPlayer(city.getOwner())
			razor = PyPlayer(iPlayer)
			if (iPlayer == CyGame().getActivePlayer()):
				message = "Razed %s" % (city.getName())
				Logger.writeLog(message, vColor="RoyalBlue")

			elif (city.getOwner() == CyGame().getActivePlayer()):
				message = "%s razed by %s" % (city.getName(), razor.getCivilizationName())
				Logger.writeLog(message, vColor="RoyalBlue")

	def onCityAcquired(self, argsList):
		if (BugAutolog.isLogCityOwner()):
			owner,playerType,city,bConquest,bTrade = argsList
			if city.getOwner() == CyGame().getActivePlayer():
				if (bConquest):
					message = "Captured %s (%s)" % (city.getName(), PyPlayer(owner).getName())
				elif (bTrade): ## city trade not tested
					message = "Traded for %s (%s)" % (city.getName(), PyPlayer(owner).getName())
				else:
					message = "%s (%s) culture flips" % (city.getName(), PyPlayer(owner).getName())

				Logger.writeLog(message, vColor="RoyalBlue")

	def onCityLost(self, argsList):
		if (BugAutolog.isLogCityOwner()):
			city = argsList[0]
			if city.getOwner() == CyGame().getActivePlayer():
				message = "%s lost" % (city.getName())
				Logger.writeLog(message, vColor="RoyalBlue")

	def onCultureExpansion(self, argsList):
		if (BugAutolog.isLogCityBorders()):
			pCity = argsList[0]
			iPlayer = argsList[1]
			if pCity.getOwner() == CyGame().getActivePlayer():
				message = "%s's borders expand" % (pCity.getName())
				Logger.writeLog(message, vColor="RoyalBlue")

	def onCityGrowth(self, argsList):
		if (BugAutolog.isLogCityGrowth()):
			pCity = argsList[0]
			iPlayer = argsList[1]
			#CvUtil.pyPrint("%s has grown to size %i" %(pCity.getName(),pCity.getPopulation()))
			if pCity.getOwner() == CyGame().getActivePlayer():
				message = "grows"
				message = "%s %s to size %i" %(pCity.getName(), message, pCity.getPopulation())
				Logger.writeLog(message, vColor="RoyalBlue")

	def onCityBuildingUnit(self, argsList):
		if (BugAutolog.isLogBuildStarted()):
			pCity = argsList[0]
			iUnitType = argsList[1]
			if pCity.getOwner() == CyGame().getActivePlayer():
				zTurns = pCity.getUnitProductionTurnsLeft(iUnitType, 1)
				message = "%s begins: %s (%i turns)" %(pCity.getName(),gc.getUnitInfo(iUnitType).getDescription(), zTurns)
				Logger.writeLog(message, vColor="Purple")

	def onCityBuildingBuilding(self, argsList):
		if (BugAutolog.isLogBuildStarted()):
			pCity = argsList[0]
			iBuildingType = argsList[1]
			if pCity.getOwner() == CyGame().getActivePlayer():
				zTurns = pCity.getBuildingProductionTurnsLeft(iBuildingType, 1)
				message = "%s begins: %s (%i turns)" %(pCity.getName(),gc.getBuildingInfo(iBuildingType).getDescription(), zTurns)
				Logger.writeLog(message, vColor="Purple")

	def onImprovementBuilt(self, argsList):
		'Improvement Built'
		iImprovement, iX, iY = argsList

		if (PyInfo.ImprovementInfo(iImprovement).getDescription() == "Tribal Village"
		or PyInfo.ImprovementInfo(iImprovement).getDescription() == "City Ruins"):
			return

		pPlot = CyMap().plot(iX,iY)

		if (BugAutolog.isLogImprovements()
		and pPlot.getOwner() == CyGame().getActivePlayer()):
			message = "A %s was built" % (PyInfo.ImprovementInfo(iImprovement).getDescription())
			zsLocn = ""
			for iiX in range(iX-2, iX+3, 1):
				for iiY in range(iY-2, iY+3, 1):
					pPlot = CyMap().plot(iiX,iiY)
					if (pPlot.isCity()):
						zsCity = pPlot.getPlotCity()
						zsLocn = " near %s" % (zsCity.getName())

			message = message + zsLocn
			Logger.writeLog(message, vColor="RoyalBlue")

	def onImprovementDestroyed(self, argsList):
		'Improvement Destroyed'
		iImprovement, iOwner, iX, iY = argsList

		if (PyInfo.ImprovementInfo(iImprovement).getDescription() == "Tribal Village"
		or PyInfo.ImprovementInfo(iImprovement).getDescription() == "City Ruins"):
			return

		pPlot = CyMap().plot(iX,iY)

		if (BugAutolog.isLogImprovements()
		and pPlot.getOwner() == CyGame().getActivePlayer()):
			message = "A %s was destroyed" % (PyInfo.ImprovementInfo(iImprovement).getDescription())
			zsLocn = ""
			for iiX in range(iX-2, iX+3, 1):
				for iiY in range(iY-2, iY+3, 1):
					pPlot = CyMap().plot(iiX,iiY)
					if (pPlot.isCity()):
						zsCity = pPlot.getPlotCity()
						zsLocn = " near %s" % (zsCity.getName())

			message = message + zsLocn
			Logger.writeLog(message, vColor="RoyalBlue")

	def onUnitPillage(self, argsList):
		'Unit pillages a plot'
		pUnit, iImprovement, iRoute, iOwner = argsList
		iX = pUnit.getX()
		iY = pUnit.getY()
		pPlot = CyMap().plot(iX,iY)

		if (BugAutolog.isLogPillage()
		and (pPlot.getOwner() == CyGame().getActivePlayer()
		or   pUnit.getOwner() == CyGame().getActivePlayer())):
			if (iImprovement != -1):
				message = "A %s" % (gc.getImprovementInfo(iImprovement).getDescription())
			elif (iRoute != -1):
				message = "A %s" % (gc.getRouteInfo(iRoute).getDescription())
			else:
				message = "An improvement"
			zsLocn = ""
			for iiX in range(iX-2, iX+3, 1):
				for iiY in range(iY-2, iY+3, 1):
					pPlot = CyMap().plot(iiX,iiY)
					if (pPlot.isCity()):
						zsCity = pPlot.getPlotCity()
						zsLocn = " near %s" % (zsCity.getName())

			message = message + zsLocn
			message = message + " was destroyed by %s %s" %(PyPlayer(iOwner).getCivilizationAdjective(), pUnit.getName())

			if self.bHumanPlaying:
				Logger.writeLog(message, vColor="DarkRed")
			else:
				Logger.writeLog(message, vColor="Red")

	def onVassalState(self, argsList):
		'Vassal State'
		iMaster, iVassal, bVassal = argsList
		
		if (BugAutolog.isLogVassals()
		and gc.getTeam(iMaster).isHasMet(gc.getActivePlayer().getTeam())
		and gc.getTeam(iVassal).isHasMet(gc.getActivePlayer().getTeam())):

			zsMaster = gc.getTeam(iMaster).getName()
			zsVassal = gc.getTeam(iVassal).getName()

			if (bVassal):
				message = "%s becomes a Vassal State of %s" % (zsVassal, zsMaster)
			else:
				message = "%s revolts and is no longer a Vassal State of %s" % (zsVassal, zsMaster)

			Logger.writeLog(message, vColor="Red")

	def initStuff(self):
		#set up variables to hold stuff
		ziMaxCiv = gc.getGame().countCivPlayersEverAlive()

		self.CIVAttitude = [""] * ziMaxCiv * ziMaxCiv
		self.CIVCivics = [0] * ziMaxCiv * 5
		self.CIVReligion = [-1] * ziMaxCiv
		self.CityWhipCounter = [0] * 1000
		self.CityConscriptCounter = [0] * 1000

	def storeStuff(self):
		ziMaxCiv = gc.getGame().countCivPlayersEverAlive()
		if (not self.CIVReligion):
			self.initStuff()

		# store civ state religion
		for iCiv in range(0, ziMaxCiv, 1):
			self.CIVReligion[iCiv] = gc.getPlayer(iCiv).getStateReligion()

		# store civ attitudes
		for iCiv1 in range(0, ziMaxCiv, 1):
			for iCiv2 in range(0, ziMaxCiv, 1):
				zKey = ziMaxCiv * iCiv1 + iCiv2
				self.CIVAttitude[zKey] = gc.getAttitudeInfo(gc.getPlayer(iCiv1).AI_getAttitude(iCiv2)).getDescription()

		# store the civ's civics
		for iCiv in range(0, ziMaxCiv, 1):
			if PyPlayer(iCiv).isAlive():
				for iCivic in range(0, 5, 1):
					zKey = 5 * iCiv + iCivic
					self.CIVCivics[zKey] = gc.getPlayer(iCiv).getCivics(iCivic)

		return 0

	def storeWhip(self):
		# store the city whip counter
		iPlayer = gc.getActivePlayer()
		for i in range(0, iPlayer.getNumCities(), 1):
			iCity = iPlayer.getCity(i)
			self.CityWhipCounter[i] = iCity.getHurryAngerTimer()
			self.CityConscriptCounter[i] = iCity.getConscriptAngerTimer()

	def checkStuff(self):
		ziMaxCiv = gc.getGame().countCivPlayersEverAlive()
		if (not self.CIVReligion):
			self.storeStuff()

		# check if civ state religion has changed
		if (BugAutolog.isLogReligion()):
			for iCiv in range(0, ziMaxCiv, 1):
				if (gc.getTeam(gc.getPlayer(iCiv).getTeam()).isHasMet(gc.getActivePlayer().getTeam())
				and self.CIVReligion[iCiv] != gc.getPlayer(iCiv).getStateReligion()
				and PyPlayer(iCiv).isAlive()):
					zsCiv = gc.getPlayer(iCiv).getName() + "(" + gc.getPlayer(iCiv).getCivilizationShortDescription(0) + ")"
					if self.CIVReligion[iCiv] == -1:
						zsOldRel = "no State Religion"
					else:
						zsOldRel = gc.getReligionInfo(self.CIVReligion[iCiv]).getDescription()
					if gc.getPlayer(iCiv).getStateReligion() == -1:
						zsNewRel = "no State Religion"
					else:
						zsNewRel = gc.getReligionInfo(gc.getPlayer(iCiv).getStateReligion()).getDescription()
					message = "State Religion Change: %s from '%s' to '%s'" % (zsCiv, zsOldRel, zsNewRel)
					Logger.writeLog(message, vColor="DarkOrange")

		# check if the attitude has changed
		if (BugAutolog.isLogAttitude()):
			for iCiv1 in range(0, ziMaxCiv, 1):
				for iCiv2 in range(0, ziMaxCiv, 1):
					zKey = ziMaxCiv * iCiv1 + iCiv2
					zsNewAttitude = gc.getAttitudeInfo(gc.getPlayer(iCiv1).AI_getAttitude(iCiv2)).getDescription()

					if (gc.getTeam(gc.getPlayer(iCiv1).getTeam()).isHasMet(gc.getActivePlayer().getTeam())
					and gc.getTeam(gc.getPlayer(iCiv2).getTeam()).isHasMet(gc.getActivePlayer().getTeam())
					and self.CIVAttitude[zKey] != zsNewAttitude
					and iCiv1 != gc.getGame().getActivePlayer()
					and PyPlayer(iCiv1).isAlive()
					and PyPlayer(iCiv2).isAlive()):
						zsCiv1 = gc.getPlayer(iCiv1).getName() + "(" + gc.getPlayer(iCiv1).getCivilizationShortDescription(0) + ")"
						zsCiv2 = gc.getPlayer(iCiv2).getName() + "(" + gc.getPlayer(iCiv2).getCivilizationShortDescription(0) + ")"
						message = "Attitude Change: %s towards %s, from '%s' to '%s'" % (zsCiv1, zsCiv2, self.CIVAttitude[zKey], zsNewAttitude)
						Logger.writeLog(message, vColor="Blue")

		# check if the civ's civics have changed
		if (BugAutolog.isLogCivics()):
			for iCiv in range(0, ziMaxCiv, 1):
				zsCiv = gc.getPlayer(iCiv).getName() + "(" + gc.getPlayer(iCiv).getCivilizationShortDescription(0) + ")"
				if (PyPlayer(iCiv).isAlive()
				and gc.getTeam(gc.getPlayer(iCiv).getTeam()).isHasMet(gc.getActivePlayer().getTeam())):
					for iCivic in range(0, 5, 1):
						zKey = 5 * iCiv + iCivic
						if (self.CIVCivics[zKey] != gc.getPlayer(iCiv).getCivics(iCivic)):
							zsOldCiv = gc.getCivicInfo(self.CIVCivics[zKey]).getDescription()
							zsNewCiv = gc.getCivicInfo(gc.getPlayer(iCiv).getCivics(iCivic)).getDescription()
							message = "Civics Change: %s from '%s' to '%s'" % (zsCiv, zsOldCiv, zsNewCiv)
							Logger.writeLog(message, vColor="SeaGreen")
		return 0

	def dumpStuff(self):
		ziMaxCiv = gc.getGame().countCivPlayersEverAlive()
		if (not self.CIVReligion):
			self.storeStuff()
		
		Logger.writeLog("")
		Logger.writeLog("dumpStuff")
		Logger.writeLog("state religion")

		# dump civ state religion
		for iCiv in range(0, ziMaxCiv, 1):
			zsCiv = gc.getPlayer(iCiv).getCivilizationShortDescription(0)
			message = "zsCiv %s, %i, %i" % (zsCiv, self.CIVReligion[iCiv], gc.getPlayer(iCiv).getStateReligion())
			Logger.writeLog(message)

		Logger.writeLog("")
		Logger.writeLog("attitude")

		# dump attitude
		for iCiv1 in range(0, ziMaxCiv, 1):
			for iCiv2 in range(0, ziMaxCiv, 1):
				zsCiv1 = gc.getPlayer(iCiv1).getCivilizationAdjective(0)  #getCivilizationShortDescription(0)
				zsCiv2 = gc.getPlayer(iCiv2).getCivilizationAdjective(0)  #getCivilizationShortDescription(0)
				zsNewAttitude = gc.getAttitudeInfo(gc.getPlayer(iCiv1).AI_getAttitude(iCiv2)).getDescription()
				zKey = ziMaxCiv * iCiv1 + iCiv2
				message = "Attitude, %s, %s, %s, %s" % (zsCiv1, zsCiv2, self.CIVAttitude[zKey], zsNewAttitude)
				Logger.writeLog(message)

		Logger.writeLog("")
		Logger.writeLog("civics")

		# dump civ's civics
		for iCiv in range(0, ziMaxCiv, 1):
			zsCiv = gc.getPlayer(iCiv).getCivilizationShortDescription(0)
			for iCivic in range(0, 5, 1):
				zKey = 5 * iCiv + iCivic
				zsOldCiv = gc.getCivicInfo(self.CIVCivics[zKey]).getDescription()
				zsNewCiv = gc.getCivicInfo(gc.getPlayer(iCiv).getCivics(iCivic)).getDescription()
				message = "Civics, %s, %s, %s" % (zsCiv, zsOldCiv, zsNewCiv)
				Logger.writeLog(message)

		Logger.writeLog("")
		Logger.writeLog("City Whip Counter")

		# dump the city whip counter
		iPlayer = gc.getActivePlayer()
		for i in range(0, iPlayer.getNumCities(), 1):
			iCity = iPlayer.getCity(i)
			message = "Whip Counter, %s, %s, %s" % (iCity.getName(), self.CityWhipCounter[i], iCity.getHurryAngerTimer())
			Logger.writeLog(message)

		Logger.writeLog("")

		return 0
