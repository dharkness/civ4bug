## BugConfig
##
## Parses a BUG Config XML file into a collection of configuration objects
## including Mods, IniFiles, Options, Screens, Tabs and Events.
##
## TODO:
##  - Remove IniFile
##  - Move Mod to BugOptions/BugGame
##  - Add Mod.module; used as default wherever a module is required
##  - Same for screens and tabs
##  - Make sure inits and events run after options (?)
##  - Change separator from "__" to "." (fix XML and tabs)
##
##  - Build an internal representation (partially done already) of the XML files
##    and then process everything in the correct order
##  - Later pickle it if reading separate XML files turns out to be slow
##    Would still need to detect changed XML files (stat)
##
## Copyright (c) 2008 The BUG Mod.
##
## Author: EmperorFool

import xmllib
import BugInit
import BugOptions
import BugPath
import BugUtil
from configobj import ConfigObj
import InputUtil
import CvEventInterface
import CvScreensInterface

MOD_OPTION_SEP = "__"

TYPE_REPLACE = { "bool": "boolean",
			 	 "bit": "boolean",
			 	 "str": "string",
				 "integer": "int",
				 "long": "int",
				 "number": "int",
				 "real": "float",
				 "double": "float",
				 "decimal": "float",
				 "vector": "tuple",
				 "map": "dict",
				 "keys": "key" }
TYPE_DEFAULT = { "boolean": False,
			 	 "string": "",
				 "int": 0,
				 "float": 0.0,
				 "key": "" }
TYPE_DEFAULT_FUNC = { "tuple": tuple,
					  "list": list,
					  "set": set,
					  "dict": dict }
TYPE_EVAL = { "boolean": lambda x: bool(x),
			  "string": lambda x: x,
			  "int": lambda x: int(x),
			  "float": lambda x: float(x),
			  "tuple": lambda x: eval("(%s,)" % x),
			  "list": lambda x: eval("[%s]" % x),
			  "set": lambda x: eval("set([%s])" % x),
			  "dict": lambda x: eval("{%s}" % x),
			  "key": lambda x: InputUtil.stringToKeystrokes(x) }

g_builder = None

def makeOptionId(modId, optionId):
	"""Concatenates the mod and option ID with a separator of the option ID
	doesn't already have one.
	
	Returns a fully qualified option ID.
	"""
	if optionId is not None and modId is not None:
		if optionId.find(MOD_OPTION_SEP) == -1:
			return modId + MOD_OPTION_SEP + optionId
	return optionId

class GameBuilder:
	"Builds each of the objects read by the XML parser."
	
	def __init__(self, game=None, attrs=None):
		if game is None:
			game = Game()
		self.game = game
		self.eventManager = CvEventInterface.getEventManager()
		self.options = BugOptions.getOptions()
		self.optionsScreen = CvScreensInterface.getBugOptionsScreen()
		
		self.attrs = attrs
		self.mod = None
		self.iniFile = None
		self.section = None
		self.option = None
		self.screen = None

	def createBuilder(self, module, clazz=None, attrs=None):
		if not clazz:
			clazz = module
		return BugUtil.callFunction(module, clazz, self.game, attrs)
	
	def loadMod(self, name):
		BugInit.loadMod(name)
	
	def createMod(self, id, name, author=None, url=None, version=None, build=None, releaseDate=None, attrs=None):
		self.mod = Mod(id, name, author, url, version, build, releaseDate, attrs)
		self.game.addMod(self.mod)
		return self.mod
	
	
	def createIniFile(self, id, name, attrs=None):
		self.iniFile = BugOptions.IniFile(id, name)
		self.iniFile.attrs = attrs
		self.options.addFile(self.iniFile)
		return self.iniFile
	
	def createSection(self, id, attrs=None):
		self.section = id
	
	
	def createLinkedOption(self, id, linkId, getter=None, setter=None, attrs=None):
		id = makeOptionId(self.mod.id, id)
		linkId = makeOptionId(self.mod.id, linkId)
		option = self.options.getOption(linkId)
		if option is not None:
			link = option.createLinkedOption(id, self.iniFile)
			self.options.addOption(link)
			link.createAccessorPair(getter, setter)
			return link
		else:
			BugUtil.debug("ERR: link option %s not found" % linkId)
			return None
	
	def createOption(self, id, type, key=None, default=None, andId=None, 
					 title=None, tooltip=None, dirtyBit=None, getter=None, setter=None, 
					 attrs=None):
		if type == "color":
			return self.createOptionList(id, type, key, default, andId, type, None, None, title, tooltip, dirtyBit, getter, setter, attrs)
		id = makeOptionId(self.mod.id, id)
		andId = makeOptionId(self.mod.id, andId)
		if key is None:
			self.option = BugOptions.UnsavedOption(self.iniFile, id, type, 
													  default, andId, title, tooltip, dirtyBit)
		else:
			self.option = BugOptions.IniOption(self.iniFile, id, self.section, key, type, 
												  default, andId, title, tooltip, dirtyBit)
		self.option.attrs = attrs
		self.options.addOption(self.option)
		self.option.createAccessorPair(getter, setter)
		return self.option
	
	def createOptionList(self, id, type, key=None, default=None, andId=None, 
						 listType=None, values=None, format=None, 
						 title=None, tooltip=None, dirtyBit=None, getter=None, setter=None, 
						 attrs=None):
		id = makeOptionId(self.mod.id, id)
		andId = makeOptionId(self.mod.id, andId)
		if key is None:
			self.option = BugOptions.UnsavedListOption(self.iniFile, id, type, 
														  default, andId, listType, values, format, 
														  title, tooltip, dirtyBit)
		else:
			self.option = BugOptions.IniListOption(self.iniFile, id, self.section, key, type, 
													  default, andId, listType, values, format, 
													  title, tooltip, dirtyBit)
		self.option.attrs = attrs
		self.options.addOption(self.option)
		self.option.createAccessorPair(getter, setter)
		return self.option
	
	def createChangeDirtyBit(self, dirtyBit):
		self.option.addDirtyBit(dirtyBit)
	
	def createChangeFunction(self, module, function):
		self.option.addDirtyFunction(BugUtil.getFunction(module, function))
	
	def createChoice(self, id, getter=None, setter=None):
		self.option.addValue(id, getter, setter)
	
	def createAccessor(self, id, getter=None, setter=None, attrs=None):
		self.iniFile.createParameterizedAccessorPair(id, getter, setter)
	
	
	def createScreen(self, id, attrs=None):
		self.screen = OptionsScreen(id, attrs)
		self.game.addScreen(self.screen)
		return self.screen
	
	def createTab(self, screenId, id, module, clazz=None, attrs=None):
		if screenId:
			screen = self.game.getScreen(screenId)
		else:
			screen = self.screen
		if not screen:
			raise BugUtil.ConfigError("<tab> must be in <screen> or have screenId")
		if not clazz:
			clazz = module
		tab = BugUtil.callFunction(module, clazz, self.optionsScreen)
		tab.attrs = attrs
		screen.addTab(tab)
		self.optionsScreen.addTab(tab)
		return tab
	
	
	def createInit(self, module, function="init", args=(), kwargs={}, attrs=None):
		BugInit.addInit(module, BugUtil.getFunction(module, function, *args, **kwargs))
	
	def createEvent(self, eventType, module, function, args=(), kwargs={}, attrs=None):
		self.eventManager.addEventHandler(eventType, BugUtil.getFunction(module, function, *args, **kwargs))
	
	def createEvents(self, module, function=None, args=(), kwargs={}, attrs=None):
		if not function:
			function = module
		return BugUtil.callFunction(module, function, self.eventManager, *args, **kwargs)
	
	def createArgument(self, name, type=None, value=None, attrs=None):
		if type:
			type = type.lower()
			if type in TYPE_REPLACE:
				type = TYPE_REPLACE[type]
			if value is None:
				if type in TYPE_DEFAULT:
					return TYPE_DEFAULT[type]
				elif type in TYPE_DEFAULT_FUNC:
					return TYPE_DEFAULT_FUNC[type]()
				else:
					raise BugUtil.ConfigError("type %s requires a value" % type)
			else:
				value = value.replace("\n", " ")
				if type in TYPE_EVAL:
					return TYPE_EVAL[type](value)
		return eval(value)

def setGameBuilder(builder=None):
	global g_builder
	if builder is None:
		builder = GameBuilder()
	g_builder = builder


class Game:
	"Tracks the Mods and other top-level objects that make up the game itself."
	
	def __init__(self):
		self.mods = {}
		self.iniFiles = {}
		self.screens = {}
	
	def getMod(self, id):
		return self.mods[id]
	
	def addMod(self, mod):
		self.mods[mod.id] = mod
	
	def getIniFile(self, id):
		return self.iniFiles[id]
	
	def addIniFile(self, iniFile):
		self.iniFiles[iniFile.id] = iniFile
	
	def getScreen(self, id):
		return self.screens[id]
	
	def addScreen(self, screen):
		self.screens[screen.id] = screen


class Mod:
	
	def __init__(self, id, name, author=None, url=None, 
				 version=None, build=None, releaseDate=None, attrs=None):
		self.id = id
		self.name = name
		self.author = author
		self.url = url
		self.version = version
		self.build = build
		self.releaseDate = releaseDate
		self.attrs = attrs


class IniFile:
	
	def __init__(self, id, name, attrs=None):
		self.id = id
		self.name = name
		self.attrs = attrs
		
		self.options = []
		
		path = BugPath.findIniFile(name)
		if not path:
			raise BugUtil.ConfigError("File %s not found" % name)
		self.config = ConfigObj(path)
	
	def getConfig(self):
		return self.config
	
	def addOptions(self, options):
		self.options.append(options)


class OptionsScreen:
	
	def __init__(self, id, attrs=None):
		self.id = id
		self.attrs = attrs
		
		self.tabs = []
	
	def addTab(self, tab):
		self.tabs.append(tab)


ID = "id"

BUILDER = "builder"

LOAD = "load"

MOD = "mod"
NAME = "name"
AUTHOR = "author"
VERSION = "version"
BUILD = "build"
DATE = "date"
URL = "�rl"

OPTIONS = "options"
FILE = "file"

SECTION = "section"

ACCESSOR = "accessor"
GETTER = "get"
SETTER = "set"

OPTION = "option"
LINK = "link"
KEY = "key"
TYPE = "type"
DEFAULT = "default"
AND = "and"
TITLE = "label"
TOOLTIP = "help"
DIRTYBIT = "dirtyBit"

LIST = "list"
LISTTYPE = "listType"
VALUES = "values"
FORMAT = "format"

CHOICE = "choice"
CHANGE = "change"

SCREEN = "screen"
TAB = "tab"

INIT = "init"
EVENT = "event"
EVENTS = "events"

ARG = "arg"
VALUE = "value"

MODULE = "module"
CLASS = "class"
FUNCTION = "function"

class XmlParser(xmllib.XMLParser):

	def __init__(self):
		xmllib.XMLParser.__init__(self)
		self.option = None
		self.saving = False
		self.savedText = None
		self.arg_container_attrs = None
		self.arg_attrs = None
		self.args = None
		self.kwargs = None
		setGameBuilder(g_builder)

	def parse(self, path):
		try:
			file = open(path)
			try:
				while True:
					s = file.read(512)
					if not s:
						break
					self.feed(s)
			finally:
				file.close()
		except IOError:
			BugUtil.debug("BUG: IOError parsing %s" % path)
		except BugUtil.ConfigError:
			BugUtil.debug("ERROR: failure parsing %s at line %d" % (path, self.lineno))
		self.close()
	
	def syntax_error(self, message):
		BugUtil.debug(message)
	
	def unknown_starttag(self, tag, attrs):
		BugUtil.debug("XML start %s with %d attributes" % (tag, len(attrs)))
	
	def unknown_endtag(self, tag):
		BugUtil.debug("XML end %s" % tag)
	
	def handle_data(self, data):
		if self.saving:
			self.savedText += data
	
	
	def start_builder(self, attrs):
		module = self.getRequiredAttribute(attrs, MODULE, BUILDER)
		clazz = self.getAttribute(attrs, CLASS, module)
		builder = g_builder.createBuilder(module, clazz, attrs)
		if builder:
			setGameBuilder(builder)
	
	def end_builder(self):
		pass
	
	
	def start_load(self, attrs):
		name = self.getRequiredAttribute(attrs, MOD, LOAD)
		g_builder.loadMod(name)
	
	def end_load(self):
		pass
	
	
	def start_mod(self, attrs):
		id = self.getRequiredAttribute(attrs, ID, MOD)
		name = self.getAttribute(attrs, NAME)
		author = self.getAttribute(attrs, AUTHOR)
		version = self.getAttribute(attrs, VERSION)
		build = self.getAttribute(attrs, BUILD)
		date = self.getAttribute(attrs, DATE)
		url = self.getAttribute(attrs, URL)
		mod = g_builder.createMod(id, name, author, url, 
								  version, build, date, attrs)
	
	def end_mod(self):
		pass
	
	
	def start_options(self, attrs):
		id = self.getRequiredAttribute(attrs, ID, OPTIONS)
		file = self.getRequiredAttribute(attrs, FILE, OPTIONS)
		iniFile = g_builder.createIniFile(id, file, attrs)
	
	def end_options(self):
		pass
	
	def start_section(self, attrs):
		id = self.getRequiredAttribute(attrs, ID, SECTION)
		section = g_builder.createSection(id)
	
	def end_section(self):
		pass
	
	
	def start_option(self, attrs):
		id = self.getRequiredAttribute(attrs, ID, OPTION)
		link = self.getAttribute(attrs, LINK)
		if link:
			getter = self.getAttribute(attrs, GETTER)
			setter = self.getAttribute(attrs, SETTER)
			option = g_builder.createLinkedOption(id, link, getter, setter, attrs)
		else:
			type = self.getRequiredAttribute(attrs, TYPE, OPTION)
			key = self.getAttribute(attrs, KEY)
			default = self.getAttribute(attrs, DEFAULT)
			andId = self.getAttribute(attrs, AND)
			dirtyBit = self.getAttribute(attrs, DIRTYBIT)
			title = self.getAttribute(attrs, TITLE)
			tooltip = self.getAttribute(attrs, TOOLTIP)
			getter = self.getAttribute(attrs, GETTER)
			setter = self.getAttribute(attrs, SETTER)
			option = g_builder.createOption(id, type, key, default, andId, title, tooltip, dirtyBit, getter, setter, attrs)
	
	def end_option(self):
		pass
	
	def start_change(self, attrs):
		dirtyBit = self.getAttribute(attrs, DIRTYBIT)
		if dirtyBit:
			g_builder.createChangeDirtyBit(dirtyBit)
		else:
			module = self.getRequiredAttribute(attrs, MODULE, CHANGE)
			function = self.getRequiredAttribute(attrs, FUNCTION, CHANGE)
			g_builder.createChangeFunction(module, function)
	
	def end_change(self):
		pass
	
	def start_list(self, attrs):
		id = self.getRequiredAttribute(attrs, ID, LIST)
		type = self.getAttribute(attrs, TYPE)
		key = self.getAttribute(attrs, KEY)
		if type is None:
			listType = self.getRequiredAttribute(attrs, LISTTYPE, LIST)
		else:
			listType = self.getAttribute(attrs, LISTTYPE)
		default = self.getAttribute(attrs, DEFAULT)
		andId = self.getAttribute(attrs, AND)
		values = self.getAttribute(attrs, VALUES)
		format = self.getAttribute(attrs, FORMAT)
		dirtyBit = self.getAttribute(attrs, DIRTYBIT)
		title = self.getAttribute(attrs, TITLE)
		tooltip = self.getAttribute(attrs, TOOLTIP)
		getter = self.getAttribute(attrs, GETTER)
		setter = self.getAttribute(attrs, SETTER)
		self.option = g_builder.createOptionList(id, type, key, default, andId, listType, values, format, title, tooltip, dirtyBit, getter, setter, attrs)
	
	def end_list(self):
		self.option.createComparers()
	
	def start_choice(self, attrs):
		id = self.getRequiredAttribute(attrs, ID, CHOICE)
		getter = self.getAttribute(attrs, GETTER)
		setter = self.getAttribute(attrs, SETTER)
		g_builder.createChoice(id, getter, setter)
	
	def end_choice(self):
		pass
	
	def start_accessor(self, attrs):
		id = self.getRequiredAttribute(attrs, ID, ACCESSOR)
		getter = self.getRequiredAttribute(attrs, GETTER, ACCESSOR)
		setter = self.getAttribute(attrs, SETTER)
		g_builder.createAccessor(id, getter, setter, attrs)
	
	def end_accessor(self):
		pass
	
	
	def start_screen(self, attrs):
		id = self.getRequiredAttribute(attrs, ID, SCREEN)
		screen = g_builder.createScreen(id, attrs)
	
	def end_screen(self):
		pass

	def start_tab(self, attrs):
		screenId = self.getAttribute(attrs, SCREEN)
		module = self.getRequiredAttribute(attrs, MODULE, TAB)
		clazz = self.getAttribute(attrs, CLASS, module)
		id = self.getAttribute(attrs, ID, module)
		tab = g_builder.createTab(screenId, id, module, clazz, attrs)
	
	def end_tab(self):
		pass
	
	
	def start_init(self, attrs):
		self.startArgs(attrs)
	
	def end_init(self):
		attrs, args, kwargs = self.endArgs()
		module = self.getRequiredAttribute(attrs, MODULE, INIT)
		function = self.getAttribute(attrs, FUNCTION, "init")
		g_builder.createInit(module, function, args, kwargs, attrs)
	
	def start_event(self, attrs):
		self.startArgs(attrs)
	
	def end_event(self):
		attrs, args, kwargs = self.endArgs()
		eventType = self.getRequiredAttribute(attrs, TYPE, EVENT)
		module = self.getRequiredAttribute(attrs, MODULE, EVENT)
		function = self.getRequiredAttribute(attrs, FUNCTION, EVENT)
		g_builder.createEvent(eventType, module, function, args, kwargs, attrs)
	
	def start_events(self, attrs):
		self.startArgs(attrs)
	
	def end_events(self):
		attrs, args, kwargs = self.endArgs()
		module = self.getRequiredAttribute(attrs, MODULE, EVENTS)
		function = self.getAttribute(attrs, FUNCTION, module)
		clazz = self.getAttribute(attrs, CLASS, function)
		g_builder.createEvents(module, clazz, args, kwargs, attrs)
	
	
	def start_arg(self, attrs):
		self.arg_attrs = attrs
		value = self.getAttribute(attrs, VALUE)
		if value is None:
			self.startText()
	
	def end_arg(self):
		name = self.getAttribute(self.arg_attrs, NAME)
		type = self.getAttribute(self.arg_attrs, TYPE)
		value = self.getAttribute(self.arg_attrs, VALUE)
		if value is None:
			value = self.endText()
		arg = g_builder.createArgument(name, type, value)
		BugUtil.debug("BUG: %s argument %s = %r" % (type, name, arg))
		if arg is not None:
			if name:
				self.kwargs[name] = arg
			else:
				self.args.append(arg)
	
	
	def getAttribute(self, attrs, key, default=None):
		if key in attrs:
			return attrs[key]
		else:
			return default
	
	def getRequiredAttribute(self, attrs, key, tag):
		if key in attrs:
			return attrs[key]
		else:
			raise BugUtil.ConfigError("<%s>.%s is required" % (tag, key))
	
	def startText(self):
		if self.saving:
			BugUtil.debug("ERROR: already saving text in XML parser")
		self.saving = True
		self.savedText = ""
	
	def endText(self):
		if not self.saving:
			BugUtil.debug("ERROR: not saving text in XML parser")
			return ""
		self.saving = False
		return self.savedText
	
	def startArgs(self, attrs):
		self.arg_container_attrs = attrs
		self.args = []
		self.kwargs = {}
	
	def endArgs(self):
		return self.arg_container_attrs, self.args, self.kwargs


"""
Regexps for options Python -> XML

<option>
self.addOption\(Option\("[A-Za-z0-9]+_([^"]+)",[ \t\r\n]*"([^"]+)", "([^"]+)", ([^,]+),[ \t\r\n]*"([^"]+)",[ \t\r\n]*"([^"]+)",[ \t\r\n]*InterfaceDirtyBits.([^\n\r]+)_DIRTY_BIT\)\)
<option id="$1" key="$3" \R\t\t\t\t\ttype="boolean" default="$4" \R\t\t\t\t\tget="" set="" dirtyBit="$7" \R\t\t\t\t\tlabel="$5" \R\t\t\t\t\thelp="$6"/>
<option id="$1" key="$3" \R\t\t\t\t\ttype="boolean" default="$4" \R\t\t\t\t\tget="" set="" dirtyBit="$7"/>

<option> no dirty bit
self.addOption\(Option\("[A-Za-z0-9]+_([^"]+)",[ \t\r\n]*"([^"]+)", "([^"]+)", ([^,]+),[ \t\r\n]*"([^"]+)",[ \t\r\n]*"([^"]+)"\)\)
<option id="$1" key="$3" \R\t\t\t\t\ttype="boolean" default="$4" \R\t\t\t\t\tget="" set="" \R\t\t\t\t\tlabel="$5" \R\t\t\t\t\thelp="$6"/>
<option id="$1" key="$3" \R\t\t\t\t\ttype="boolean" default="$4" \R\t\t\t\t\tget=""/>

<list>
self.addOption\(OptionList\("[A-Za-z0-9]+_([^"]+)",[ \t\r\n]*"([^"]+)", "([^"]+)", ([^,]+),[ \t\r\n]*"([^"]+)",[ \t\r\n]*"([^"]+)",[ \t\r\n]*\[([^]]+)\],[ \t\r\n]*"([^"]+)",[ \t\r\n]*InterfaceDirtyBits.([^\n\r]+)_DIRTY_BIT\)\)
<list   id="$1" key="$3" \R\t\t\t\t\ttype="int" default="$4" listType="int" \R\t\t\t\t\tvalues="$7" format="$8" \R\t\t\t\t\tget="" set="" dirtyBit="$9" \R\t\t\t\t\tlabel="$5" \R\t\t\t\t\thelp="$6"/>

<list> no dirty bit
self.addOption\(OptionList\("[A-Za-z0-9]+_([^"]+)",[ \t\r\n]*"([^"]+)", "([^"]+)", ([^,]+),[ \t\r\n]*"([^"]+)",[ \t\r\n]*"([^"]+)",[ \t\r\n]*\[([^]]+)\],[ \t\r\n]*"([^"]+)"\)\)
<list   id="$1" key="$3" \R\t\t\t\t\ttype="int" default="$4" listType="int" \R\t\t\t\t\tvalues="$7" format="$8" \R\t\t\t\t\tget="" set="" \R\t\t\t\t\tlabel="$5" \R\t\t\t\t\thelp="$6"/>

<list> no format
self.addOption\(OptionList\("[A-Za-z0-9]+_([^"]+)",[ \t\r\n]*"([^"]+)", "([^"]+)", ([^,]+),[ \t\r\n]*"([^"]+)",[ \t\r\n]*"([^"]+)",[ \t\r\n]*\[([^]]+)\], None,[ \t\r\n]*InterfaceDirtyBits.([^\n\r]+)_DIRTY_BIT\)\)
<list   id="$1" key="$3" \R\t\t\t\t\ttype="int" default="$4" listType="string" \R\t\t\t\t\tvalues="$7" \R\t\t\t\t\tget="" set="" dirtyBit="$8" \R\t\t\t\t\tlabel="$5" \R\t\t\t\t\thelp="$6"/>
<list   id="$1" key="$3" \R\t\t\t\t\ttype="int" default="$4" listType="string" \R\t\t\t\t\tvalues="$7" \R\t\t\t\t\tget="" set="" dirtyBit="$8"/>

<list> no format or dirty bit
self.addOption\(OptionList\("[A-Za-z0-9]+_([^"]+)",[ \t\r\n]*"([^"]+)", "([^"]+)", ([^,]+),[ \t\r\n]*"([^"]+)",[ \t\r\n]*"([^"]+)",[ \t\r\n]*\[([^]]+)\](, None)?\)\)
<list   id="$1" key="$3" \R\t\t\t\t\ttype="int" default="$4" listType="string" \R\t\t\t\t\tvalues="$7" \R\t\t\t\t\tget="" set="" \R\t\t\t\t\tlabel="$5" \R\t\t\t\t\thelp="$6"/>

accessors
get="(is|get)([^"]+)"
get="$1$2" set="set$2"
"""
