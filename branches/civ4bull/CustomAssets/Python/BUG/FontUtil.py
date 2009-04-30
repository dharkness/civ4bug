## FontUtil
##
## Utilities for dealing with FontSymbols.
##
## Notes
##   - Must be initialized externally by calling init()
##
## Copyright (c) 2008 The BUG Mod.
##
## Author: EmperorFool

from CvPythonExtensions import *
import CvUtil
import BugUtil

UNKNOWN_CHAR = "?"

gc = CyGlobalContext()

nextSymbolID = int(FontSymbols.MAX_NUM_SYMBOLS)

# key -> symbol (FontSymbols)
keySymbols = {}
# symbol -> primary key (string)
symbolPrimaryKeys = {}
# symbol -> ordinal (int)
symbolOrdinals = {}
# symbol -> character (unicode string)
symbolChars = {}

def init():
	symbolNames = {}
	for name, symbol in FontSymbols.__dict__.iteritems():
		if name.endswith("_CHAR") and isinstance(symbol, FontSymbols):
			symbolNames[symbol] = name
	for key, symbol in CvUtil.OtherFontIcons.iteritems():
		addBuiltinSymbol(key, symbol)
		if symbol in symbolNames:
			name = symbolNames[symbol]
			registerSymbolSynonym(key, symbol, name[:-5])
			registerSymbolSynonym(key, symbol, name)
#			del symbolNames[symbol]
	# add the FontSymbols that aren't in CvUtil
#	for symbol, name in symbolNames:
#		addBuiltinSymbol()
	
	for count, getInfo in (
		(YieldTypes.NUM_YIELD_TYPES, gc.getYieldInfo),
		(CommerceTypes.NUM_COMMERCE_TYPES, gc.getCommerceInfo),
	):
		for enum in range(count):
			info = getInfo(enum)
			addSymbol(info.getType().lower().replace("_", " "), 
					info.getChar(), info.getType())

def addBuiltinSymbol(key, symbol):
	registerSymbol(key, symbol, gc.getGame().getSymbolID(symbol))

def addOffsetSymbol(key, symbolOrKey, offset, name=None):
	return addSymbol(key, getOrdinal(getSymbol(symbolOrKey)) + offset, name)

def addSymbol(key, ordinal, name=None):
	if not name:
		name = key.upper().replace(" ", "_")
	else:
		name = name.upper().replace(" ", "_")
	symbolName = name + "_CHAR"
	symbol = findOrCreateSymbol(symbolName)
	registerSymbol(key, symbol, ordinal)
	registerSymbolSynonym(key, symbol, name)
	registerSymbolSynonym(key, symbol, symbolName)
	return symbol

def findOrCreateSymbol(name):
	try:
		symbol = getattr(FontSymbols, name)
		if isinstance(symbol, FontSymbols):
			BugUtil.debug("FontUtil - found FontSymbols name %s", name)
			return symbol
	except AttributeError:
		pass
	# create a FontSymbols enum for it
	global nextSymbolID
	symbol = FontSymbols(nextSymbolID)
	nextSymbolID += 1
	BugUtil.debug("FontUtil - created FontSymbols.%s", name)
	setattr(FontSymbols, name, symbol)
	return symbol

def registerSymbol(key, symbol, ordinal):
	BugUtil.info("FontUtil - registering symbol '%s' for %d", key, ordinal)
	if key in keySymbols:
		raise BugUtil.ConfigError("duplicate font symbol key '%s'" % key)
	if symbol in symbolPrimaryKeys:
		raise BugUtil.ConfigError("duplicate font symbol for key '%s'" % key)
	keySymbols[key] = symbol
	symbolPrimaryKeys[symbol] = key
	symbolOrdinals[symbol] = ordinal
	symbolChars[symbol] = u"%c" % ordinal
	
def registerSymbolSynonym(key, symbol, synonym):
	if synonym in keySymbols:
		BugUtil.warn("FontUtil - ignoring duplicate synonym '%s' for key '%s'", synonym, key)
	else:
		BugUtil.debug("FontUtil - registering synonym '%s'", synonym)
		keySymbols[synonym] = symbol


def getSymbol(symbolOrKey):
	if isinstance(symbolOrKey, FontSymbols):
		return symbolOrKey
	try:
		return keySymbols[symbolOrKey]
	except KeyError:
		try:
			return keySymbols[symbolOrKey.upper() + "_CHAR"]
		except KeyError:
			raise BugUtil.ConfigError("unknown font symbol or key '%s'" % str(symbolOrKey))

def getOrdinal(symbolOrKey):
	try:
		return symbolOrdinals[getSymbol(symbolOrKey)]
	except KeyError:
		raise BugUtil.ConfigError("unknown font symbol or key '%s'" % str(symbolOrKey))

def getChar(symbolOrKey):
	try:
		return symbolChars[getSymbol(symbolOrKey)]
	except KeyError:
		raise BugUtil.ConfigError("unknown font symbol or key '%s'" % str(symbolOrKey))
