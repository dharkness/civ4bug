## Unit Plot List Utilities
##
## Holds the information used to display the unit plot list
##
## Copyright (c) 2007-2009 The BUG Mod.
##
## Author: Ruff_Hi

from CvPythonExtensions import *
import MonkeyTools as mt
import BugUtil

iLeaderPromo = gc.getInfoTypeForString('PROMOTION_LEADER')

def updatePLEOptions():
	# Capture these for looping over the plot's units
	self.bShowWoundedIndicator = PleOpt.isShowWoundedIndicator()
	self.bShowGreatGeneralIndicator = PleOpt.isShowGreatGeneralIndicator()
	self.bShowPromotionIndicator = PleOpt.isShowPromotionIndicator()
	self.bShowUpgradeIndicator = PleOpt.isShowUpgradeIndicator()
	self.bShowMissionInfo = PleOpt.isShowMissionInfo()
	self.bShowHealthBar = PleOpt.isShowHealthBar()
	self.bHideHealthBarWhileFighting = PleOpt.isHideHealthFighting()
	self.bShowMoveBar = PleOpt.isShowMoveBar()


class UnitDisplay:
	def __init__(self, pUnit):
#		self.bSelected = ...
		self.eUnit = pUnit.getUnitType()
		self.sDot = _getDOTState(pUnit)
		self.sMission = _getMission(pUnit)
		self.bPromo = pUnit.isPromotionReady()
		self.bGG = iLeaderPromo != -1 and pUnit.isHasPromotion(iLeaderPromo)
		self.bUpgrade = mt.checkAnyUpgrade(pUnit)
		self.icurrHitPoints = pUnit.currHitPoints()
		self.imaxHitPoints = pUnit.maxHitPoints()
		self.iMovesLeft = pUnit.movesLeft()
		self.iMoves = pUnit.getMoves()

	def _getDOTState(self, pUnit):
		if ((pUnit.getTeam() != gc.getGame().getActiveTeam()) or pUnit.isWaiting()):
			# fortified
			szDotState = "OVERLAY_FORTIFY"
		elif (pUnit.canMove()):
			if (pUnit.hasMoved()):
				# unit moved, but some movement points are left
				szDotState = "OVERLAY_HASMOVED"
			else:
				# unit did not move yet
				szDotState = "OVERLAY_MOVE"
		else:
			# unit has no movement points left
			szDotState = "OVERLAY_NOMOVE"

		# Wounded units will get a darker colored button.
		if (self.bShowWoundedIndicator) and (pUnit.isHurt()):
			szDotState += "_INJURED"

		# Units lead by a GG will get a star instead of a dot.
		if (self.bShowGreatGeneralIndicator):
			# is unit lead by a GG?
			if (iLeaderPromo != -1 and pUnit.isHasPromotion(iLeaderPromo)):
				szDotState += "_GG"

		return szDotState

	def _getMission(self, pUnit):
		eActivityType = pUnit.getGroup().getActivityType()
		eAutomationType = pUnit.getGroup().getAutomateType()

		# is unit on air intercept mission
		if (eActivityType == ActivityTypes.ACTIVITY_INTERCEPT):
			return "OVERLAY_ACTION_INTERCEPT"
		# is unit on boat patrol coast mission
		elif (eActivityType == ActivityTypes.ACTIVITY_PATROL):
			return "OVERLAY_ACTION_PATROL"
		# is unit on boat blockade mission
		elif (eActivityType == ActivityTypes.ACTIVITY_PLUNDER):
			return "OVERLAY_ACTION_PLUNDER"
		# is unit fortified for healing (wake up when healed)
		elif (eActivityType == ActivityTypes.ACTIVITY_HEAL):
			return "OVERLAY_ACTION_HEAL"
		# is unit sentry (wake up when enemy in sight)
		elif (eActivityType == ActivityTypes.ACTIVITY_SENTRY):
			return "OVERLAY_ACTION_SENTRY"
		# is the turn for this unit skipped (wake up next turn)
		elif (eActivityType == ActivityTypes.ACTIVITY_HOLD):
			return "OVERLAY_ACTION_SKIP"
		# has unit exploration mission
		elif (eAutomationType == AutomateTypes.AUTOMATE_EXPLORE):
			return "OVERLAY_ACTION_EXPLORE"
		# is unit automated generally (only worker units)
		elif (eAutomationType == AutomateTypes.AUTOMATE_BUILD):
			return "OVERLAY_ACTION_AUTO_BUILD"
		# is unit automated for nearest city (only worker units)
		elif (eAutomationType == AutomateTypes.AUTOMATE_CITY):
			return "OVERLAY_ACTION_AUTO_CITY"
		# is unit automated for network (only worker units)
		elif (eAutomationType == AutomateTypes.AUTOMATE_NETWORK):
			return "OVERLAY_ACTION_AUTO_NETWORK"
		# is unit automated spread religion (only missionary units)
		elif (eAutomationType == AutomateTypes.AUTOMATE_RELIGION):
			return "OVERLAY_ACTION_AUTO_RELIGION"
		# has unit a mission
		elif (pUnit.getGroup().getLengthMissionQueue() > 0):
			eMissionType = pUnit.getGroup().getMissionType(0)
			# is the mission to build an improvement
			if (eMissionType == MissionTypes.MISSION_BUILD):
				return "OVERLAY_ACTION_BUILD"
			# is the mission a "move to" mission
			elif (eMissionType in UnitUtil.MOVE_TO_MISSIONS):
				return "OVERLAY_ACTION_GOTO"
		# if nothing of above, but unit is waiting -> unit is fortified
		elif (pUnit.isWaiting()):
			if (pUnit.isFortifyable()):
				return "OVERLAY_ACTION_FORTIFY"
			else:
				return "OVERLAY_ACTION_SLEEP"

		return ""
