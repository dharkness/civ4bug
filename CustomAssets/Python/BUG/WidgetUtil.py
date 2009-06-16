## WidgetUtil
##
## Provides functions to create new WidgetTypes and supply hover text for them.
##
## WidgetTypes
##
##   createWidget(name)
##     Creates and returns a new unique WidgetTypes constant named <name>.
##
##       <widget name="<name>"/>
##
## Hover Help Text
##
##   setWidgetHelpText(widget, text)
##     Uses static <text> string for the hover help text of <widget>.
##
##       <widget name="<widget-name>" text="<text>"/>
##
##   setWidgetHelpXml(widget, key)
##     Uses <TEXT> CIV4GameText.xml element matching <key> for the hover text of <widget>.
##     This form allows you to use translated strings as it's looked up each time it's shown.
##
##       <widget name="<widget-name>" key="<key>"/>
##
##   setWidgetHelpFunction(widget, func)
##     Calls <func> to get the hover text of <widget> each time it's shown.
##     Use this method when you want the displayed text to change based on game conditions.
##     The function should have this signature:
##       func(eWidget, iData1, iData2, bOption)
##
##       <widget name="<widget-name>" module="<module-name>" function="<function-name>"/>
##
## Copyright (c) 2009 The BUG Mod.
##
## Author: EmperorFool

from CvPythonExtensions import *
import BugUtil


## Widget Types

g_nextWidget = WidgetTypes.NUM_WIDGET_TYPES

def createWidget(name):
	"""
	Creates and returns the next unique WidgetTypes constant to be used with custom UI widgets.
	
	If <name> already exists, a warning is logged. Otherwise the new widget is
	assigned to WidgetTypes.<name>.
	"""
	global g_nextWidget
	widget = WidgetTypes(g_nextWidget)
	if name:
		if hasattr(WidgetTypes, name):
			BugUtil.warn("WidgetTypes.%s already exists", name)
		else:
			BugUtil.info("WidgetUtil - WidgetTypes.%s = %d", name, g_nextWidget)
			setattr(WidgetTypes, name, widget)
	g_nextWidget += 1
	return widget


## Hover Text

(
	WIDGET_HELP_TEXT, 
	WIDGET_HELP_XML, 
	WIDGET_HELP_FUNCTION,
) = range(3)

WIDGET_HELP_TYPES = (
	"Text",
	"XML",
	"Function",
)

g_widgetHelp = {}

def setWidgetHelpText(widget, text):
	"""
	Assigns the literal <text> to be used as the hover text for <widget>.
	"""
	setWidgetHelp(widget, WIDGET_HELP_TEXT, text)

def setWidgetHelpXml(widget, key):
	"""
	Assigns the XML <key> to be used to lookup the translated hover text for <widget>.
	"""
	setWidgetHelp(widget, WIDGET_HELP_XML, key)

def setWidgetHelpFunction(widget, func):
	"""
	Assigns the function <func> to be called to get the hover text for <widget>.
	
	The function will be called each time the hover text is needed with these parameters:
	
		eWidgetType         WidgetTypes constant
		data1               int
		data2               int
		bOption             boolean
	
	The first three are the ones used when creating the UI widget.
	I have no idea what <bOption> is or where it comes from.
	"""
	setWidgetHelp(widget, WIDGET_HELP_FUNCTION, func)

def setWidgetHelp(widget, type, value):
	"""
	Registers the hover text type and value for <widget> if it hasn't been already.
	"""
	if widget in g_widgetHelp:
		BugUtil.warn("WidgetTypes %d help already registered", widget)
	else:
		BugUtil.debug("WidgetUtil - registering %s hover help for WidgetTypes %d: %s", WIDGET_HELP_TYPES[type], widget, value)
		g_widgetHelp[widget] = (type, value)

	
def getWidgetHelp(argsList):
	"""
	Returns the hover help text for <eWidgetType> if registered, otherwise returns an empty string.
	"""
	eWidgetType, iData1, iData2, bOption = argsList
	entry = g_widgetHelp.get(eWidgetType)
	if entry:
		(type, value) = entry
		if type == WIDGET_HELP_TEXT:
			return value
		elif type == WIDGET_HELP_XML:
			return BugUtil.getPlainText(value)
		elif type == WIDGET_HELP_FUNCTION:
			return value(eWidgetType, iData1, iData2, bOption)
	return u""
