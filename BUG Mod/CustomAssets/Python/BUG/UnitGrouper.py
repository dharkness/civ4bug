## UnitGrouper
## Builds groups of units for use in reporting or screens.
## Copyright (c) 2008 The BUG Mod.

from CvPythonExtensions import *

# globals
gc = CyGlobalContext()

# Base grouping classes

class Grouper:
	"""
	Holds all Grouping definitions.
	"""
	def __init__(self):
		self.groupings = []
		self.groupingsByKey = {}
	
	def _addGrouping(self, grouping):
		grouping.index = len(self.groupings)
		self.groupings.append(grouping)
		self.groupingsByKey[grouping.key] = grouping
	
	def getGrouping(self, key):
		if key in self.groupingsByKey:
			return self.groupingsByKey[key]
		else:
			return None

class Grouping:
	"""
	Applies a formula to place units into groups.
	
	key: used for sorting groupings; must be in the range [0, 999] inclusive
	title: used to display the group
	"""
	def __init__(self, key, title):
		self.index = None
		self.key = key
		self.title = title
		self.groups = {}
	
	def _addGroup(self, group):
		self.groups[group.key] = group
	
	def calcGroupKey(self, unit, player, team):
		return None

class Group:
	"""
	Represents a single group value within a grouping.
	
	key: used for sorting groups; must be in the range [0, 999] inclusive
	title: used to display the group
	"""
	def __init__(self, grouping, key, title):
		self.grouping = grouping
		self.key = key
		self.title = title
	
	def getTitle(self):
		return self.title


# Grouping definitions

class UnitTypeGrouping(Grouping):
	"""
	Groups units by their unit type.
	Ex: Warrior, Maceman, Panzer
	"""
	def __init__(self):
		Grouping.__init__(self, "type", "Unit Type")
		
		for i in range(gc.getNumUnitInfos()):
			info = gc.getUnitInfo(i)
			if info:
				self._addGroup(Group(self, i, info.getDescription()))
	
	def calcGroupKey(self, unit, player, team):
		return unit.getUnitType()

class UnitCombatGrouping(Grouping):
	"""
	Groups units by their combat type.
	Ex: None, Melee, Gunpowder, Naval
	"""
	def __init__(self):
		Grouping.__init__(self, "combat", "Combat Type")
		self.NONE = 0
		
		self._addGroup(Group(self, self.NONE, "None"))
		for i in range(gc.getNumUnitCombatInfos()):
			info = gc.getUnitCombatInfo(i)
			if info:
				self._addGroup(Group(self, i + 1, info.getDescription()))
	
	def calcGroupKey(self, unit, player, team):
		return gc.getUnitInfo(unit.getUnitType()).getUnitCombatType() + 1

class PromotionGrouping(Grouping):
	"""
	Groups units by their promotions.
	Ex: Combat 1, Cover, Tactics
	"""
	def __init__(self):
		Grouping.__init__(self, "promo", "Promotion")
		self.NONE = 0
		
		self._addGroup(Group(self, 0, "None"))
		for i in range(gc.getNumPromotionInfos()):
			info = gc.getPromotionInfo(i)
			if info:
				self._addGroup(Group(self, i + 1, info.getDescription()))
	
	def calcGroupKey(self, unit, player, team):
		# Find first promo until we have multi-select groupings
		for iPromo in range(gc.getNumPromotionInfos()):
			if unit.isHasPromotion(iPromo):
				return iPromo + 1
		return self.NONE

class LocationGrouping(Grouping):
	"""
	Groups units by their location on the map.
	Ex: Domestic City, Friendly City, Enemy Territory
	"""
	def __init__(self):
		Grouping.__init__(self, "loc", "Location")
		self.DOMESTIC_CITY = 0
		self.DOMESTIC_TERRITORY = self.DOMESTIC_CITY + 1
		self.TEAM_CITY = self.DOMESTIC_TERRITORY + 1
		self.TEAM_TERRITORY = self.TEAM_CITY + 1
		self.FRIENDLY_CITY = self.TEAM_TERRITORY + 1
		self.FRIENDLY_TERRITORY = self.FRIENDLY_CITY + 1
		self.NEUTRAL_TERRITORY = self.FRIENDLY_TERRITORY + 1
		self.ENEMY_TERRITORY = self.NEUTRAL_TERRITORY + 1
		self.BARBARIAN_TERRITORY = self.ENEMY_TERRITORY + 1
		
		self._addGroup(Group(self, self.DOMESTIC_CITY, "Domestic City"))
		self._addGroup(Group(self, self.DOMESTIC_TERRITORY, "Domestic Territory"))
		self._addGroup(Group(self, self.TEAM_CITY, "Team City"))
		self._addGroup(Group(self, self.TEAM_TERRITORY, "Team Territory"))
		self._addGroup(Group(self, self.FRIENDLY_CITY, "Friendly City"))
		self._addGroup(Group(self, self.FRIENDLY_TERRITORY, "Friendly Territory"))
		self._addGroup(Group(self, self.NEUTRAL_TERRITORY, "Neutral Territory"))
		self._addGroup(Group(self, self.ENEMY_TERRITORY, "Enemy Territory"))
		self._addGroup(Group(self, self.BARBARIAN_TERRITORY, "Barbarian Territory"))
	
	def calcGroupKey(self, unit, player, team):
		plot = unit.plot()
		if not plot or plot.isNone():
			return None
		if plot.isBarbarian():
			return self.BARBARIAN_TERRITORY
		teamId = team.getID()
		ownerId = plot.getRevealedOwner(teamId, False)
		if ownerId == -1:
			return self.NEUTRAL_TERRITORY
		elif ownerId == player.getID():
			if plot.isCity():
				return self.DOMESTIC_CITY
			else:
				return self.DOMESTIC_TERRITORY
		else:
			owner = gc.getPlayer(ownerId)
			ownerTeamId = owner.getTeam()
			if ownerTeamId == teamId:
				if plot.isCity():
					return self.TEAM_CITY
				else:
					return self.TEAM_TERRITORY
			elif team.isAtWar(ownerTeamId):
				return self.ENEMY_TERRITORY
			else:
				if plot.isCity():
					return self.FRIENDLY_CITY
				else:
					return self.FRIENDLY_TERRITORY

class StandardGrouper(Grouper):
	def __init__(self):
		Grouper.__init__(self)
		
		self._addGrouping(UnitTypeGrouping())
		self._addGrouping(UnitCombatGrouping())
		self._addGrouping(PromotionGrouping())
		self._addGrouping(LocationGrouping())


# Classes for tracking stats about groups and units

class GrouperStats:
	"""
	Holds stats for a set of groupings.
	"""
	def __init__(self, grouper):
		self.grouper = grouper
		self.groupings = {}

		for grouping in self.grouper.groupings:
			self._addGrouping(GroupingStats(grouping))
	
	def _addGrouping(self, grouping):
		self.groupings[grouping.grouping.key] = grouping
	
	def processUnit(self, player, team, unit):
		stats = UnitStats(unit.getOwner(), unit.getID(), unit)
		for grouping in self.groupings.itervalues():
			grouping._processUnit(player, team, stats)
		return stats
	
	def getGrouping(self, key):
		if key in self.groupings:
			return self.groupings[key]
		else:
			return None
	
	def itergroupings(self):
		return self.groupings.itervalues()

class GroupingStats:
	"""
	Holds stats for a grouping.
	"""
	def __init__(self, grouping):
		self.grouping = grouping
		self.groups = {}
		
		for group in self.grouping.groups.itervalues():
			self._addGroup(GroupStats(group))
	
	def _addGroup(self, group):
		self.groups[group.group.key] = group
	
	def _processUnit(self, player, team, unitStats):
		key = self.grouping.calcGroupKey(unitStats.unit, player, team)
		if key is not None:
			self.groups[key]._addUnit(unitStats)
	
	def itergroups(self):
		return self.groups.itervalues()

class GroupStats:
	"""
	Holds stats for a group of units.
	"""
	def __init__(self, group):
		self.group = group
		self.units = set()
	
	def _addUnit(self, unitStats):
		self.units.add(unitStats)
	
	def title(self):
		return self.group.title
	
	def size(self):
		return len(self.units)
	
	def isEmpty(self):
		return self.size() == 0

class UnitStats:
	"""
	Holds stats about a single unit.
	"""
	def __init__(self, playerId, unitId, unit):
		self.key = (playerId, unitId)
		self.unit = unit

	def __hash__(self):
		return hash(self.key)

	def __eq__(self, other):
		return self.key == other.key
