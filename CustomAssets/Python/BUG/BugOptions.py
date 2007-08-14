## BugOptions
## Provides access to all options and a facade base class for option sets
## BUG Mod - Copyright 2007

import RuffModControl

#__all__ = [ getOptions, Option, OptionList, OptionsFacade ]

class BugOptions(object):

	def __init__(self):
		self.config = RuffModControl.RuffModConfig()
		self.options = {}


	def getOption(self, name):
		if (name in self.options):
			return self.options[name]
		return None

	def addOption(self, option):
		self.options[option.getName()] = option


	def getValue(self, name):
		option = self.getOption(name)
		if (option):
			return self.config.get_str(option.getSection(), option.getKey(), option.getDefault())

	def getString(self, name):
		return self.getValue(name)

	def getBoolean(self, name):
		option = self.getOption(name)
		if (option):
			return self.config.get_boolean(option.getSection(), option.getKey(), option.getDefault())

	def getInt(self, name):
		option = self.getOption(name)
		if (option):
			return self.config.get_int(option.getSection(), option.getKey(), option.getDefault())

	def getFloat(self, name):
		option = self.getOption(name)
		if (option):
			return self.config.get_float(option.getSection(), option.getKey(), option.getDefault())


	def setValue(self, name, value):
		option = self.getOption(name)
		if (option):
			self.config.set_str(option.getSection(), option.getKey(), value)

	def setString(self, name, value):
		self.setValue(name, value)

	def setBoolean(self, name, value):
		option = self.getOption(name)
		if (option):
			self.config.set_boolean(option.getSection(), option.getKey(), value)

	def setInt(self, name, value):
		option = self.getOption(name)
		if (option):
			self.config.set_int(option.getSection(), option.getKey(), value)

	def setFloat(self, name, value):
		option = self.getOption(name)
		if (option):
			self.config.set_float(option.getSection(), option.getKey(), value)


	def read(self):
		RuffModControl.RuffModConfigFile = RuffModControl.read_ConfigFile()

	def write(self):
		RuffModControl.write_ConfigFile()


# The singleton BugOptions object

__g_options = BugOptions()
def getOptions():
	return __g_options


class OptionsFacade(object):

	def __init__(self):
		self.options = getOptions()


	def addOption(self, option):
		self.options.addOption(option)


	def getValue(self, name):
		return self.options.getValue(name)

	def getString(self, name):
		return self.options.getString(name)

	def getBoolean(self, name):
		return self.options.getBoolean(name)

	def getInt(self, name):
		return self.options.getInt(name)

	def getFloat(self, name):
		return self.options.getFloat(name)


	def setValue(self, name, value):
		self.options.setValue(name, value)


class Option(object):
	"Holds the metadata for a single option"

	def __init__(self, name, section, key, default, title, tooltip, dirtyBit=None):
		if (name is not None):
			self.name = name
		else:
			self.name = self.section + "_" + self.key
		self.section = section
		self.key = key
		self.default = default
		self.title = title
		self.tooltip = tooltip
		self.dirtyBit = dirtyBit

	def getName(self):
		return self.name

	def getSection(self):
		return self.section

	def getKey(self):
		return self.key

	def getDefault(self):
		return self.default

	def getTitle(self):
		return self.title

	def getTooltip(self):
		return self.tooltip

	def getDirtyBit(self):
		return self.dirtyBit


class OptionList(Option):
	"Adds a list of possible values for a single option"

	def __init__(self, name, section, key, default, title, tooltip, values, format=None, dirtyBit=None):
		Option.__init__(self, name, section, key, default, title, tooltip, dirtyBit)
		self.values = values
		self.format = format

	def getValues(self):
		return self.values

	def getFormat(self):
		return self.format

	def isValid(self, value):
		return value in self.values
