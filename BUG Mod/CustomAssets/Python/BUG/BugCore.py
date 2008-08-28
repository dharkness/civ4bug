## BugCore
##
## Provides a top-level Game that manages the Mods and their Options.
##
## Copyright (c) 2008 The BUG Mod.
##
## Author: EmperorFool

import BugUtil

MOD_OPTION_SEP = "__"

class Game(object):
	"""Manages a set of Mods."""
	
	def __init__(self):
		self._mods = {}
		self._emptyMods = {}
		self._screens = {}
		self._inited = False
	
	def _createMod(self, id):
		if self._inited:
			raise BugUtil.ConfigError("Cannot create mod '%s' after initialization" % id)
		else:
			return self._newMod(id)
	
	def _newMod(self, id):
		mod = Mod(id)
		self._emptyMods[id] = mod
		self._mods[id] = mod
		return mod
	
	def _getMod(self, id):
		if id in self._mods:
			return self._mods[id]
		elif not self._inited:
			BugUtil.debug("INFO: creating uninitialized mod %s" % id)
			return self._newMod(id)
		else:
			BugUtil.debug("ERROR: invalid mod %s" % id)
	
	def _addMod(self, mod):
		id = mod._getID()
		if self._inited:
			BugUtil.debug("WARN: cannot add mod %s post-init" % id)
		elif id in self._emptyMods:
			if not mod._inited:
				BugUtil.debug("ERROR: mod %s not initialized" % id)
			del self._emptyMods[id]
		elif id in self._mods:
			BugUtil.debug("ERROR: mod %s already exists" % id)
		else:
			self._mods[id] = mod
	
	def _removeMod(self, id):
		if id in self._mods:
			del self._mods[id]
	
	def _initDone(self):
		if self._inited:
			BugUtil.debug("WARN: game already initialized")
		else:
			for mod in self._emptyMods.values():
				id = mod._getID()
				if mod._inited:
					BugUtil.debug("WARN: mod %s not added; adding" % id)
					del self._emptyMods[id]
				else:
					BugUtil.debug("WARN: mod %s not initialized; removing" % id)
					self._removeMod(id)
			self._inited = True
	
	def __getattr__(self, id):
		"""Returns the Mod with the given ID."""
		if not id.startswith("_"):
			mod = self._getMod(id)
			if mod is not None:
				return mod
		raise AttributeError(id)
	
	def _getScreen(self, id):
		return self._screens[id]
	
	def _addScreen(self, screen):
		self._screens[screen.id] = screen


class Mod(object):
	"""Provides Option accessors."""
	
	def __init__(self, id):
		self._id = id
		self._options = {}
		self._inited = False
	
	def _getID(self):
		return self._id
	
	def _addOption(self, option):
		self._options[option.getID()] = option
	
	def _hasOption(self, id):
		return id in self._options
	
	def _getOption(self, id):
		if not self._hasOption(id):
			if self._inited:
				BugUtil.debug("ERROR: option %s not found" % id)
		else:
			return self._options[id]  # BugOptions.getOption[self._id + "__" + id]
	
	def _initDone(self):
		if self._inited:
			BugUtil.debug("WARN: mod already initialized")
		else:
			self._inited = True
	
	def __getattr__(self, id):
		"""Returns the Option with the given ID or False for is/getters
		and None for setters that don't exist."""
		if not id.startswith("_"):
			# Try bare option
			if self._hasOption(id):
				return self._getOption(id)
			# Try option with Mod ID prefix
			fullId = self._id + MOD_OPTION_SEP + id
			if self._hasOption(fullId):
				return self._getOption(fullId)
			# If not yet initialized, return False for getters and setters
			if not self._inited:
				if id.startswith("get") or id.startswith("is"):
					return lambda *ignored: False
				if id.startswith("set"):
					return lambda *ignored: False
		raise AttributeError(id)
	
	
	def _createParameterizedAccessorPair(self, id, getter=None, setter=None, values=None):
		id = self._id + MOD_OPTION_SEP + id
		if getter:
			if values is None:
				def get(*args):
					option = self._getOption(id % args)
					if option.isColor():
						return option.getColor()
					else:
						return option.getValue()
			else:
				def equals(*args):
					option = self._getOption(id % args)
					return option.getValue() in values
			setattr(self, getter, get)
		
		if setter:
			def set(*args):
				option = self._getOption(id % args)
				option.setValue(value)
			setattr(self, setter, set)


game = Game()

def initDone():
	game._initDone()