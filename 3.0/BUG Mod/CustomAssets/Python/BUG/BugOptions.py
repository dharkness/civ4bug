## BugOptions
## Provides access to all options and a facade base class for option sets
## BUG Mod - Copyright 2007

from BugPath import findMainModIniFile
import BugConfigTracker
import BugUtil
from configobj import ConfigObj

#__all__ = [ getOptions, Option, OptionList, OptionsFacade ]

class BugOptions(object):
	
	"""
	Manages a dictionary of Option objects which describe the options that
	control the mod, provides methods for getting/setting values for them,
	and reading/writing them from/to an INI file.
	"""

	def __init__(self):
		"Initializes an empty dictionary of options and reads the main INI file."
		self.options = {}
		self.iniFile = None
		self.config = None
		
		self.read()


	def getOption(self, name):
		if (name in self.options):
			return self.options[name]
		else:
			BugUtil.debug("Missing option: %s" % name)
			return None

	def addOption(self, option):
		self.options[option.getName()] = option


	def getString(self, name):
		option = self.getOption(name)
		if (option):
			return self.getRawString(option.getSection(), option.getKey(), option.getDefault())
		else:
			return ""

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


	def setString(self, name, value):
		self._setValue(name, str(value))

	def setBoolean(self, name, value):
		self._setValue(name, bool(value))

	def setInt(self, name, value):
		self._setValue(name, int(value))

	def setFloat(self, name, value):
		self._setValue(name, float(value))

	def _setValue(self, name, value):
		if (self.config):
			option = self.getOption(name)
			if (option):
				try:
					self.config[option.getSection()][option.getKey()] = value
				except:
					pass


	def getRawString(self, section, key, default=None):
		try:
			value = self.config[section][key]
			if (isinstance(value, str)):
				return value
		except:
			pass
		return default

	def getRawBoolean(self, section, key, default=None):
		try:
			return self.config[section].as_bool(key)
		except:
			return default

	def getRawInt(self, section, key, default=None):
		try:
			return self.config[section].as_int(key)
		except:
			return default

	def getRawFloat(self, section, key, default=None):
		try:
			return self.config[section].as_float(key)
		except:
			return default


	def read(self):
		try:
			self.iniFile = findMainModIniFile()
			self.config = ConfigObj(self.iniFile)
			BugConfigTracker.add("BUG_Mod_Config", self.iniFile)
		except:
			self.iniFile = None
			self.config = None
			BugUtil.debug("Couldn't find INI file")

	def write(self):
		if (self.config):
			try:
				self.config.write()
			except:
				BugUtil.debug("Failed writing to INI file")
		else:
			BugUtil.debug("INI file wasn't read")
	
	def isLoaded(self):
		if (self.iniFile):
			return True
		else:
			return False
	
	
	def clearAllTranslations(self):
		"Clear the translations of all options in response to the user choosing a language"
		for option in self.options.itervalues():
			option.clearTranslation()


# The singleton BugOptions object

__g_options = BugOptions()
def getOptions():
	return __g_options


class OptionsFacade(object):
	
	"""
	Facade wrapper to the global set of all options. Allows each submod to group
	its options together independently of other mods yet have all options stored
	in a single INI file.
	"""

	def __init__(self):
		self.options = getOptions()


	def getOption(self, name):
		return self.options.getOption(name)

	def addOption(self, option):
		self.options.addOption(option)


	def getString(self, name):
		return self.options.getString(name)

	def getBoolean(self, name):
		return self.options.getBoolean(name)

	def getInt(self, name):
		return self.options.getInt(name)

	def getFloat(self, name):
		return self.options.getFloat(name)


	def getRawString(self, section, key, default=None):
		return self.options.getRawString(section, key, default)

	def getRawBoolean(self, section, key, default=None):
		return self.options.getRawBoolean(section, key, default)

	def getRawInt(self, section, key, default=None):
		return self.options.getRawInt(section, key, default)

	def getRawFloat(self, section, key, default=None):
		return self.options.getRawFloat(section, key, default)


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
	
	"""
	Holds the metadata for a single option:
	- A name which is used to access the option. This must be unique for all options.
	- A section and key used to store it in an INI file.
	- A default value used when no value is found in the INI file.
	- A title and tooltip (hover text) used to display it in the Options Screen.
	  Both are now stored in an external XML file and accessed using its name.
	- A Civ4 dirty-bit that is set when the option is changed. This allows changing
	  the option to force certain aspects of the interface to redraw themselves.
	"""

	def __init__(self, name, section, key, default, title, tooltip, dirtyBit=None):
		if (name is not None):
			self.name = name
		else:
			self.name = self.section + "_" + self.key
		self.section = section
		self.key = key
		self.default = default
		
		self.xmlKey = "TXT_KEY_BUG_OPT_" + self.name.upper()
		self.title = title
		self.tooltip = tooltip
		self.dirtyBit = dirtyBit
		
		self.translated = False

	def getName(self):
		return self.name

	def getSection(self):
		return self.section

	def getKey(self):
		return self.key

	def getDefault(self):
		return self.default

	def getTitle(self):
		if (not self.translated):
			self.translate()
		return self.title

	def getTooltip(self):
		if (not self.translated):
			self.translate()
		return self.tooltip

	def getDirtyBit(self):
		return self.dirtyBit
	
	def translate(self):
		self.title = BugUtil.getPlainText(self.xmlKey + "_TEXT", self.title)
		self.tooltip = BugUtil.getPlainText(self.xmlKey + "_HOVER", self.tooltip)
		self.translated = True
	
	def clearTranslation(self):
		"Marks this option so that it will be translated again the next time it is accessed"
		self.translated = False


class OptionList(Option):
	
	"""
	Adds a list of possible values to a single option and a display format to use
	when creating the dropdown listbox in the Options Screen.
	The values are not yet stored in the XML file for translation.
	"""

	def __init__(self, name, section, key, default, title, tooltip, values, format=None, dirtyBit=None):
		Option.__init__(self, name, section, key, default, title, tooltip, dirtyBit)
		self.values = values
		self.format = format
		self.displayValues = None

	def getValues(self):
		return self.values

	def getFormat(self):
		return self.format

	def getDisplayValues(self):
		if (not self.translated):
			self.translate()
		return self.displayValues
	
	def translate(self):
		list = BugUtil.getPlainText(self.xmlKey + "_LIST")
		if (list):
			self.displayValues = []
			for item in list.split("|"):
				self.displayValues.append(item)
		else:
			self.displayValues = self.values
		Option.translate(self)

	def isValid(self, value):
		return value in self.values
