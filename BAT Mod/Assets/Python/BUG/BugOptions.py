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
			return self.getRawString(option.getSection(), option.getKey(), option.getDefault())
		else:
			return ""

	def getString(self, name):
		return self.getValue(name)

	def getBoolean(self, name):
		option = self.getOption(name)
		if (option):
			return self.getRawBoolean(option.getSection(), option.getKey(), option.getDefault())
		else:
			return False

	def getInt(self, name):
		option = self.getOption(name)
		if (option):
			return self.getRawInt(option.getSection(), option.getKey(), option.getDefault())
		else:
			return 0

	def getFloat(self, name):
		option = self.getOption(name)
		if (option):
			return self.getRawFloat(option.getSection(), option.getKey(), option.getDefault())
		else:
			return 0.0


	def setValue(self, name, value):
		option = self.getOption(name)
		if (option):
			try:
				self.config.set_str(option.getSection(), option.getKey(), value)
			except:
				pass

	def setString(self, name, value):
		self.setValue(name, value)

	def setBoolean(self, name, value):
		option = self.getOption(name)
		if (option):
			try:
				self.config.set_boolean(option.getSection(), option.getKey(), value)
			except:
				pass

	def setInt(self, name, value):
		option = self.getOption(name)
		if (option):
			try:
				self.config.set_int(option.getSection(), option.getKey(), value)
			except:
				pass

	def setFloat(self, name, value):
		option = self.getOption(name)
		if (option):
			try:
				self.config.set_float(option.getSection(), option.getKey(), value)
			except:
				pass


	def getRawValue(self, section, key, default=None):
		try:
			return self.config.get_str(section, key, default)
		except:
			return default

	def getRawString(self, section, key, default=None):
		return self.getRawValue(section, key, default)

	def getRawBoolean(self, section, key, default=None):
		try:
			return self.config.get_boolean(section, key, default)
		except:
			return default

	def getRawInt(self, section, key, default=None):
		try:
			return self.config.get_int(section, key, default)
		except:
			return default

	def getRawFloat(self, section, key, default=None):
		try:
			return self.config.get_float(section, key, default)
		except:
			return default


	def getAdvUnitName(self, section, key, default=None):
		try:
			return self.config.get_advunitname(section, key, default)
		except:
			return default


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


	def getOption(self, name):
		return self.options.getOption(name)

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


	def getRawValue(self, section, key, default=None):
		return self.options.getRawValue(section, key, default)

	def getRawString(self, section, key, default=None):
		return self.options.getRawValue(section, key, default)

	def getRawBoolean(self, section, key, default=None):
		return self.options.getRawBoolean(section, key, default)

	def getRawInt(self, section, key, default=None):
		return self.options.getRawInt(section, key, default)

	def getRawFloat(self, section, key, default=None):
		return self.options.getRawFloat(section, key, default)


	def getAdvUnitName(self, section, key, default=None):
		return self.options.getAdvUnitName(section, key, default)


	def setValue(self, name, value):
		self.options.setValue(name, value)

	def setString(self, name, value):
		self.options.setString(name, value)

	def setBoolean(self, name, value):
		self.options.setBoolean(name, value)

	def setInt(self, name, value):
		self.options.setInt(name, value)

	def setFloat(self, name, value):
		self.options.setFloat(name, value)


	def write(self):
		self.options.write()


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
