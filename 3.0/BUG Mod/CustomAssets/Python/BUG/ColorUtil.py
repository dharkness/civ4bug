## ColorUtil
## Utility module for accessing Civ4 colors and managing a master dropdown dataset.
## BUG Mod - Copyright 2007
##
## Author:  EmperorFool
## Version: $revision$

from CvPythonExtensions import *

gc = CyGlobalContext()
localText = CyTranslator()

# tuple of interesting color names to be selectable from dropdowns
COLOR_KEYS = ( "COLOR_RED", "COLOR_YELLOW", "COLOR_CYAN", "COLOR_GREEN", 
			   "COLOR_BLUE", "COLOR_MAGENTA", "COLOR_WHITE", "COLOR_LIGHT_GREY", 
			   "COLOR_GREY", "COLOR_DARK_GREY", "COLOR_BLACK" )

COLOR_INDEX_IDX = 0
COLOR_TYPE_IDX = 1
COLOR_KEY_IDX = 2
COLOR_NAME_IDX = 3

# list of color tuples (index, type, key, display name)
COLORS = None

# Maps type # to color tuple
COLORS_BY_TYPE = None

# Maps key # to color tuple
COLORS_BY_KEY = None

# list of color translated display names
COLOR_DISPLAY_NAMES = None


def getColorDisplayNames ():
	"""Returns a tuple of the color display names from the color names above."""
	_createColors()
	return COLOR_DISPLAY_NAMES


def typeToIndex (type):
	"""Returns the index of the color from its info type, None if not found."""
	_createColors()
	try:
		return COLORS_BY_TYPE[type][COLOR_INDEX_IDX]
	except KeyError:
		return None

def indexToType (index):
	"""Returns the info type of the color from its index, None if not found."""
	_createColors()
	return COLORS[index][COLOR_TYPE_IDX]


def keyToIndex (key):
	"""Returns the index of the color from its key, None if not found."""
	_createColors()
	try:
		return COLORS_BY_KEY[key][COLOR_INDEX_IDX]
	except KeyError:
		return None

def indexToKey (index):
	"""Returns the key of the color from its index, None if not found."""
	_createColors()
	return COLORS[index][COLOR_KEY_IDX]


def keyToType (key):
	"""Returns the info type of the color from its key, None if not found."""
	_createColors()
	try:
		return COLORS_BY_KEY[key][COLOR_TYPE_IDX]
	except KeyError:
		return None


def _createColors ():
	"""Creates the color datasets if not already created.
	
	Cannot do this in __init__ because gc isn't initialized yet"""
	global COLOR_KEYS
	global COLORS
	global COLORS_BY_TYPE
	global COLORS_BY_KEY
	global COLOR_DISPLAY_NAMES
	
	if (COLORS):
		return
	
	COLORS = []
	COLORS_BY_TYPE = {}
	COLORS_BY_KEY = {}
#	COLOR_DISPLAY_NAMES = []
	for key in COLOR_KEYS:
		name = localText.getText("TXT_KEY_" + key, ())
		if (name):
			type = gc.getInfoTypeForString(key)
			if (type >= 0):
				info = gc.getColorInfo(type)
				if (info):
					color = (len(COLORS), type, key, name)
					COLORS.append(color)
					COLORS_BY_TYPE[type] = color
					COLORS_BY_KEY[key] = color
#					COLOR_DISPLAY_NAMES.append(name)
	
	COLOR_DISPLAY_NAMES = tuple([n for _, _, _, n in COLORS])
#	COLOR_DISPLAY_NAMES = tuple(COLOR_DISPLAY_NAMES)
