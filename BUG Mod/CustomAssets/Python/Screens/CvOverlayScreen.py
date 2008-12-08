#-------------------------------------------------------------------------------
# Name:        CvOverlayScreen.py
# Purpose:     Custom Screen for the strategy overlay
#              Contains:
#              -Dot Mapper
#              -Categorized signs
#              -
#
# Author:      Del69
#
# Created:     23/10/2008
#-------------------------------------------------------------------------------

from CvPythonExtensions import *
from SdToolkit import *
import ColorUtil
import CvEventInterface
import CvUtil
#-------------------------------------------------------------------------------
# Popup Enum
#-------------------------------------------------------------------------------
EventOverlayAddSign = CvUtil.getNewEventID("StrategyOverlay.AddSign")
#-------------------------------------------------------------------------------
# Globals
#-------------------------------------------------------------------------------
g_GC = CyGlobalContext()
g_ArtFileMgr = CyArtFileMgr()
g_LocalText = None
g_bScreenUp = False

#-------------------------------------------------------------------------------
# Keyboard event handler to show or close screen
#-------------------------------------------------------------------------------

class CvOverlayScreen:
	"""
	   Screen for the strategy overlay
	"""

	def __init__(self, screenID):
		self.screenID = screenID
		self.SCREEN_NAME = "StrategyOverlayScreen"
		#---------------------------------------------------------------------------
		# Panel IDS
		#---------------------------------------------------------------------------
		self.PREFIX = "StratOverlay"
		self.MAIN_PANEL_ID = self.PREFIX + "MainPanel"
		self.COLOR_PANEL_ID = self.PREFIX + "ColorPanel"
		self.LINE_PANEL_ID = self.PREFIX + "LinePanel"
		self.SIGN_PANEL_ID = self.PREFIX + "SignPanel"
		self.DOT_PANEL_ID = self.PREFIX + "DotPanel"
		#---------------------------------------------------------------------------
		# Misc IDS
		#---------------------------------------------------------------------------
		self.HEADER_ID = self.PREFIX + "Header"
		self.EXIT_ID = self.PREFIX + "Exit"
		self.BACKGROUND_ID = self.PREFIX + "Background"
		#---------------------------------------------------------------------------
		# Saving IDS
		#---------------------------------------------------------------------------
		self.MOD_SAVE_ID = "StrategyOverlay"
		self.CITY_SAVE_ID = "CityDataDict"
		self.SIGN_SAVE_ID = "SignDataDict"
		#-------------------------------------------------------------------------------
		# Main Panel IDS
		#-------------------------------------------------------------------------------
		self.MAIN_TITLE_ID = self.MAIN_PANEL_ID + "Title"
		self.MAIN_DOT_BUTTON_ID = self.MAIN_PANEL_ID + "WidgetDotMapper"
		self.MAIN_SIGN_BUTTON_ID = self.MAIN_PANEL_ID + "WidgetSigns"
		#---------------------------------------------------------------------------
		# Main Panel Coordinates
		#---------------------------------------------------------------------------
		self.PANEL_MARGIN = 15
		self.TITLE_HEIGHT = 16
		self.TEXT_HEIGHT = 16
		self.TXT_SPACING = 5
		self.MAIN_PANEL_X = 10
		self.MAIN_PANEL_Y = 75
		self.MAIN_PANEL_W = 200
		self.MAIN_PANEL_H = self.PANEL_MARGIN * 2 + self.TITLE_HEIGHT * 2 + 2 * self.TEXT_HEIGHT + 3 * self.TXT_SPACING
		self.MAIN_TXT_X = self.MAIN_PANEL_X + self.MAIN_PANEL_W/2
		self.MAIN_TXT_Y = self.MAIN_PANEL_Y + self.PANEL_MARGIN + self.TITLE_HEIGHT + self.TXT_SPACING
		self.MAIN_TITLE_X = self.MAIN_TXT_X
		self.MAIN_TITLE_Y = self.MAIN_PANEL_Y + self.PANEL_MARGIN
		self.EXIT_TXT_X = self.MAIN_TXT_X
		self.EXIT_TXT_Y = self.MAIN_PANEL_Y + self.MAIN_PANEL_H - self.TITLE_HEIGHT - self.PANEL_MARGIN
		self.PANEL_SPACING = 5
		self.Z_TXT = -0.3
		self.Z_CONTROL = -0.3
		#---------------------------------------------------------------------------
		# Color Values
		#---------------------------------------------------------------------------
		ColorUtil.init()
		self.COLOR_KEYS = ColorUtil.getColorKeys()
		self.COLOR_TEXT = ColorUtil.getColorDisplayNames()
		#---------------------------------------------------------------------------
		# Color Panel Widgets
		#---------------------------------------------------------------------------
		self.COLOR_WIDGET_PREFIX = self.COLOR_PANEL_ID + "Widget"
		self.COLOR_WIDGET_IDS = []
		#---------------------------------------------------------------------------
		# Color Panel Coordinates
		#---------------------------------------------------------------------------
		self.COLOR_PANEL_HEADER_H = 15
		self.COLOR_PANEL_X = self.MAIN_PANEL_X
		self.COLOR_PANEL_Y = self.MAIN_PANEL_Y + self.MAIN_PANEL_H + self.PANEL_SPACING
		self.COLOR_PANEL_TXT_X = self.COLOR_PANEL_X + self.PANEL_MARGIN
		self.COLOR_PANEL_TXT_Y = self.COLOR_PANEL_Y + self.PANEL_MARGIN
		self.COLOR_PANEL_W = 0
		self.COLOR_PANEL_H = len(self.COLOR_KEYS) * self.TEXT_HEIGHT + len(self.COLOR_KEYS) * self.TXT_SPACING + self.PANEL_MARGIN * 2
	    #---------------------------------------------------------------------------
		# DOT Mapper Panel Widgets
		#---------------------------------------------------------------------------
		self.DOT_PLACE_BUTTON_ID = self.DOT_PANEL_ID + "WidgetPlaceButton"
		self.DOT_REMOVE_BUTTON_ID = self.DOT_PANEL_ID + "WidgetRemoveButton"
		#---------------------------------------------------------------------------
		# DOT Mapper Panel Coordinates
		#---------------------------------------------------------------------------
		self.DOT_PANEL_Y = self.COLOR_PANEL_Y
		self.DOT_PANEL_W = 0
		self.DOT_PANEL_TXT_Y = self.DOT_PANEL_Y + self.PANEL_MARGIN
		self.DOT_PANEL_TXT_SPACING = self.TXT_SPACING
		self.DOT_PANEL_H = 2 * self.TEXT_HEIGHT + 2 * self.PANEL_MARGIN + self.DOT_PANEL_TXT_SPACING
		#-------------------------------------------------------------------------------
		# Sign Panel Widgets
		#-------------------------------------------------------------------------------
		self.SIGN_PLACE_ID = self.SIGN_PANEL_ID + "WidgetPlaceButton"
		self.SIGN_REMOVE_ID = self.SIGN_PANEL_ID + "WidgetRemoveButton"
		#-------------------------------------------------------------------------------
		# Sign Panel Coordinates
		#-------------------------------------------------------------------------------
		self.SIGN_PANEL_Y = self.COLOR_PANEL_Y
		self.SIGN_PANEL_W = 0
		self.SIGN_PANEL_TXT_X = 0
		self.SIGN_PANEL_TXT_Y = self.SIGN_PANEL_Y + self.PANEL_MARGIN
		self.SIGN_PANEL_H = 2 * self.TEXT_HEIGHT + 2 * self.PANEL_MARGIN + self.TXT_SPACING
		#---------------------------------------------------------------------------
		# State variables
		#---------------------------------------------------------------------------
		self.currentColor = 0
		self.bDotMapper = False
		self.bSign = False
		self.bDotPlacing = False
		self.bDotRemoving = False
		self.bSignPlacing = False
		self.bSignRemoving = False
		self.bLeftMouseDown = False
		self.bInitPos = False
		self.currentPlot = 0
		self.currentPlotX = 0
		self.currentPlotY = 0
		self.currentLayer = 0
		#-------------------------------------------------------------------------------
		# Constants
		#-------------------------------------------------------------------------------
		self.PLOT_LAYER = PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_RECOMMENDED_PLOTS
		self.DOT_STYLE = PlotStyles.PLOT_STYLE_DOT_TARGET
		self.DOT_ALPHA = 1.0
		#-------------------------------------------------------------------------------
		# Widget Input Mapping
		#-------------------------------------------------------------------------------
		self.inputMap = {
			self.MAIN_DOT_BUTTON_ID : self.onMainDotButton,
			self.MAIN_SIGN_BUTTON_ID : self.onMainSignButton,
			self.SIGN_PLACE_ID : self.onPlaceSignButton,
			self.SIGN_REMOVE_ID : self.onRemoveSignButton,
			self.COLOR_WIDGET_PREFIX : self.onColorButton,
			self.DOT_PLACE_BUTTON_ID  : self.onPlaceCityButton,
			self.DOT_REMOVE_BUTTON_ID : self.onRemoveCityButton,
			self.EXIT_ID : self.onExitButton,
		}
	#-------------------------------------------------------------------------------
	# Initilization Functions
	#-------------------------------------------------------------------------------
	def initVars(self):
		"""
		   Initializes the variables for the screen
		"""
		g_LocalText = CyTranslator()
		for index in range(len(self.COLOR_KEYS)):
			self.COLOR_WIDGET_IDS.append(self.COLOR_WIDGET_PREFIX + str(index))
		#-----------------------------------------------------------------------
		# Text Initilization
		#-----------------------------------------------------------------------
		self.MAIN_DOT_TXT = g_LocalText.getText("TXT_KEY_STRATOVERLAY_DOTMAPPER",())
		self.MAIN_TITLE_TXT = "<font=4>" + g_LocalText.getText("TXT_KEY_STRATOVERLAY_TITLE",()).upper() + "</font>"
		self.DOT_TITLE_TXT = "<font=4>" + g_LocalText.getText("TXT_KEY_STRATOVERLAY_DOTMAPPER",()).upper() + "</font>"
		self.DOT_PLACE_BUTTON_TXT = g_LocalText.getText("TXT_KEY_STRATOVERLAY_PLACECITY",())
		self.DOT_REMOVE_BUTTON_TXT = g_LocalText.getText("TXT_KEY_STRATOVERLAY_REMOVECITY",())
		self.EXIT_TXT = "<font=4>" + g_LocalText.getText("TXT_KEY_PEDIA_SCREEN_EXIT",()).upper() + "</font>"
		self.MAIN_SIGN_TXT = g_LocalText.getText("TXT_KEY_STRATOVERLAY_SIGNS",())
		self.SIGN_PLACE_TXT = g_LocalText.getText("TXT_KEY_STRATOVERLAY_ADDSIGN",())
		self.SIGN_REMOVE_TXT = g_LocalText.getText("TXT_KEY_STRATOVERLAY_REMOVESIGN",())
		#-----------------------------------------------------------------------
		# Coordinate Initilizations
		#-----------------------------------------------------------------------
		if not self.bInitPos:
			for colorTxt in self.COLOR_TEXT:
				if (CyInterface().determineWidth(colorTxt) > self.COLOR_PANEL_W):
					self.COLOR_PANEL_W = CyInterface().determineWidth(colorTxt)
			self.COLOR_PANEL_W += 2 * self.PANEL_MARGIN
			self.DOT_PANEL_W = CyInterface().determineWidth(self.DOT_PLACE_BUTTON_TXT)
			if CyInterface().determineWidth(self.DOT_REMOVE_BUTTON_TXT) > self.DOT_PANEL_W:
				self.DOT_PANEL_W = CyInterface().determineWidth(self.DOT_REMOVE_BUTTON_TXT)
			self.DOT_PANEL_W += 2 * self.PANEL_MARGIN
			self.DOT_PANEL_X = self.COLOR_PANEL_X + self.COLOR_PANEL_W + self.PANEL_SPACING
			self.DOT_PANEL_TITLE_X = self.DOT_PANEL_X + (self.DOT_PANEL_W / 2)
			self.DOT_PANEL_TXT_X = self.DOT_PANEL_X + self.PANEL_MARGIN
			self.SIGN_PANEL_W = CyInterface().determineWidth(self.SIGN_PLACE_TXT)
			if CyInterface().determineWidth(self.SIGN_REMOVE_TXT) > self.SIGN_PANEL_W:
				self.SIGN_PANEL_W = CyInterface().determineWidth(self.SIGN_REMOVE_TXT)
			self.SIGN_PANEL_W += 2 * self.PANEL_MARGIN
			self.SIGN_PANEL_X = self.COLOR_PANEL_X + self.COLOR_PANEL_W + self.PANEL_SPACING
			self.SIGN_PANEL_TXT_X = self.SIGN_PANEL_X + self.PANEL_MARGIN
			self.bInitPos = True

	def isOpen(self):
		"""
		Public accessor to check if screen is open or not
		"""
		return self.getScreen().isActive()
	#-------------------------------------------------------------------------------
	# Required civ4 functions
	#-------------------------------------------------------------------------------
	def getScreen(self):
		"""
		    Gets the CyGInterfaceScreen Object for this screen
		"""
		return CyGInterfaceScreen(self.SCREEN_NAME, self.screenID)

	def hideScreen(self):
		"""
		    Hides the Screen
		"""
		self.saveVars()
		self.removeSigns()
		self.clearAllLayers()
		CyInterface().setInterfaceMode(InterfaceModeTypes.INTERFACEMODE_SELECTION)
		screen = self.getScreen()
		screen.hideScreen()

	def update(self, fDelta):
		"""
			called each update cycle, checks for Left mouse button clicks when screen is up
		"""
		if CyInterface().isLeftMouseDown():
			if not self.bLeftMouseDown:
				self.onLeftMouseDown()
			self.bLeftMouseDown = True
		else:
			self.bLeftMouseDown = False
		return

	def handleInput(self, inputClass):
		"""
		    Handles screens widget input
		"""
		if(self.inputMap.has_key(inputClass.getFunctionName())):
			self.inputMap.get(inputClass.getFunctionName())(inputClass)
			return 1
		return 0

	def interfaceScreen(self):
		"""
		    Initializes and shows the screen
		"""
		screen = self.getScreen()
		if screen.isActive():
			return
		#-------------------------------------------------------------------------------
		# Init vars and load saved vars
		#-------------------------------------------------------------------------------
		self.initVars()
		self.loadVars()
		#-----------------------------------------------------------------------
		# Add panels and Title
		# TODO : Use attached panels instead?
		#-----------------------------------------------------------------------
		screen.addPanel(self.MAIN_PANEL_ID,u"",u"",False,False,self.MAIN_PANEL_X,self.MAIN_PANEL_Y,self.MAIN_PANEL_W,self.MAIN_PANEL_H,PanelStyles.PANEL_STYLE_MAIN)
		screen.setLabel(self.MAIN_TITLE_ID,self.MAIN_PANEL_ID,self.MAIN_TITLE_TXT,CvUtil.FONT_CENTER_JUSTIFY,self.MAIN_TITLE_X,self.MAIN_TITLE_Y,self.Z_TXT,FontTypes.TITLE_FONT,WidgetTypes.WIDGET_GENERAL,-1,-1)
		screen.setText(self.MAIN_DOT_BUTTON_ID,self.MAIN_PANEL_ID,self.MAIN_DOT_TXT,CvUtil.FONT_CENTER_JUSTIFY,self.MAIN_TXT_X,self.MAIN_TXT_Y,self.Z_TXT,FontTypes.SMALL_FONT,WidgetTypes.WIDGET_GENERAL,-1,-1)
		screen.setText(self.EXIT_ID,self.MAIN_PANEL_ID,self.EXIT_TXT,CvUtil.FONT_CENTER_JUSTIFY,self.EXIT_TXT_X,self.EXIT_TXT_Y,self.Z_TXT,FontTypes.TITLE_FONT,WidgetTypes.WIDGET_GENERAL,-1,-1)
		screen.addPanel(self.COLOR_PANEL_ID,u"",u"",True,False,self.COLOR_PANEL_X,self.COLOR_PANEL_Y,self.COLOR_PANEL_W,self.COLOR_PANEL_H,PanelStyles.PANEL_STYLE_MAIN)
		screen.addPanel(self.DOT_PANEL_ID,u"",u"",True,False,self.DOT_PANEL_X,self.DOT_PANEL_Y,self.DOT_PANEL_W,self.DOT_PANEL_H,PanelStyles.PANEL_STYLE_MAIN)
		screen.addPanel(self.SIGN_PANEL_ID,u"",u"",True,False,self.SIGN_PANEL_X,self.SIGN_PANEL_Y,self.SIGN_PANEL_W,self.SIGN_PANEL_H,PanelStyles.PANEL_STYLE_MAIN)
		txtY = self.MAIN_TXT_Y + self.TXT_SPACING + self.TEXT_HEIGHT
		screen.setText(self.MAIN_SIGN_BUTTON_ID,self.MAIN_PANEL_ID,self.MAIN_SIGN_TXT,CvUtil.FONT_CENTER_JUSTIFY,self.MAIN_TXT_X,txtY,self.Z_TXT,FontTypes.SMALL_FONT,WidgetTypes.WIDGET_GENERAL,-1,-1)
		#-------------------------------------------------------------------------------
		# Add controls and update them
		#-------------------------------------------------------------------------------
		self.addColorControls()
		self.updateColorControls(self.currentColor)
		self.addDotMapperControls()
		self.updateDotMapperControls()
		self.addSignControls()
		self.updateSignControls()
		#-------------------------------------------------------------------------------
		# Set the screen size and show it
		#-------------------------------------------------------------------------------
		screen.setDimensions(0,0,screen.getXResolution(),screen.getYResolution())
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, True)
		#-------------------------------------------------------------------------------
		# Draw all the saved data on the screen
		#-------------------------------------------------------------------------------
		self.redrawDotMap()
		self.addAllSigns()

	#-------------------------------------------------------------------------------
	#   Widget Adding/Updating Functions
	#-------------------------------------------------------------------------------
	def addColorControls(self):
		"""
		    Adds the color selection texts to the color selection panel
		"""
		screen = self.getScreen()
		for index in range(len(self.COLOR_KEYS)):
			txtY = self.COLOR_PANEL_TXT_Y + index*self.TXT_SPACING + index*self.TEXT_HEIGHT
			screen.setText(self.COLOR_WIDGET_PREFIX + str(index),self.COLOR_PANEL_ID,self.COLOR_TEXT[index],CvUtil.FONT_LEFT_JUSTIFY,self.COLOR_PANEL_TXT_X,txtY,self.Z_TXT,FontTypes.SMALL_FONT,WidgetTypes.WIDGET_GENERAL,-1,-1)

	def updateColorControls(self,selectedColorIndex):
		"""
			Highlights the passed in color index and dehighlights the old one
		"""
		screen = self.getScreen()
		oldColorTxt = self.COLOR_TEXT[self.currentColor]
		newColorTxt = " <color=0,255,0>%s</color> " % (self.COLOR_TEXT[selectedColorIndex])
		yOld = self.COLOR_PANEL_TXT_Y + self.currentColor*self.TXT_SPACING + self.currentColor*self.TEXT_HEIGHT
		yNew = self.COLOR_PANEL_TXT_Y + selectedColorIndex*self.TXT_SPACING + selectedColorIndex*self.TEXT_HEIGHT
		screen.setText(self.COLOR_WIDGET_PREFIX + str(self.currentColor),self.COLOR_PANEL_ID,oldColorTxt,CvUtil.FONT_LEFT_JUSTIFY,self.COLOR_PANEL_TXT_X,yOld,self.Z_TXT,FontTypes.SMALL_FONT,WidgetTypes.WIDGET_GENERAL,-1,-1)
		screen.setText(self.COLOR_WIDGET_PREFIX + str(selectedColorIndex),self.COLOR_PANEL_ID,newColorTxt,CvUtil.FONT_LEFT_JUSTIFY,self.COLOR_PANEL_TXT_X,yNew,self.Z_TXT,FontTypes.SMALL_FONT,WidgetTypes.WIDGET_GENERAL,-1,-1)
		screen.setState(self.COLOR_WIDGET_IDS[selectedColorIndex],True)
		screen.setState(self.COLOR_WIDGET_IDS[self.currentColor],False)
		self.currentColor = selectedColorIndex
		self.currentLayer = selectedColorIndex
		if self.currentLayer >= 5:
			self.currentLayer += 1

	def addDotMapperControls(self):
		"""
		    Adds the place/remove buttons and text to the dot mapper panel
		"""
		screen = self.getScreen()
		screen.setText(self.DOT_PLACE_BUTTON_ID,self.DOT_PANEL_ID,self.DOT_PLACE_BUTTON_TXT,CvUtil.FONT_LEFT_JUSTIFY,self.DOT_PANEL_TXT_X,self.DOT_PANEL_TXT_Y,self.Z_TXT,FontTypes.SMALL_FONT,WidgetTypes.WIDGET_GENERAL,-1,-1)
		screen.setText(self.DOT_REMOVE_BUTTON_ID,self.DOT_PANEL_ID,self.DOT_REMOVE_BUTTON_TXT,CvUtil.FONT_LEFT_JUSTIFY,self.DOT_PANEL_TXT_X,self.DOT_PANEL_TXT_Y+self.TEXT_HEIGHT+self.DOT_PANEL_TXT_SPACING,self.Z_TXT,FontTypes.SMALL_FONT,WidgetTypes.WIDGET_GENERAL,-1,-1)

	def updateDotMapperControls(self):
		"""
		    Updates the dot mapper controls based on selection
		"""
		screen = self.getScreen()
		if not self.bDotMapper:
			screen.hide(self.DOT_PLACE_BUTTON_ID)
			screen.hide(self.DOT_REMOVE_BUTTON_ID)
			screen.hide(self.DOT_PANEL_ID)
			screen.setText(self.MAIN_DOT_BUTTON_ID,self.MAIN_PANEL_ID,self.MAIN_DOT_TXT,CvUtil.FONT_CENTER_JUSTIFY,self.MAIN_TXT_X,self.MAIN_TXT_Y,self.Z_TXT,FontTypes.SMALL_FONT,WidgetTypes.WIDGET_GENERAL,-1,-1)
			return
		screen.setState(self.DOT_PLACE_BUTTON_ID,self.bDotRemoving)
		screen.setState(self.DOT_REMOVE_BUTTON_ID,self.bDotPlacing)
		text = " <color=0,255,0>%s</color>" % (self.MAIN_DOT_TXT)
		screen.setText(self.MAIN_DOT_BUTTON_ID,self.MAIN_PANEL_ID,text,CvUtil.FONT_CENTER_JUSTIFY,self.MAIN_TXT_X,self.MAIN_TXT_Y,self.Z_TXT,FontTypes.SMALL_FONT,WidgetTypes.WIDGET_GENERAL,-1,-1)
		if self.bDotPlacing:
			text = " <color=0,255,0>%s</color> " % (self.DOT_PLACE_BUTTON_TXT)
			screen.setText(self.DOT_PLACE_BUTTON_ID,self.DOT_PANEL_ID,text,CvUtil.FONT_LEFT_JUSTIFY,self.DOT_PANEL_TXT_X,self.DOT_PANEL_TXT_Y,self.Z_TXT,FontTypes.SMALL_FONT,WidgetTypes.WIDGET_GENERAL,-1,-1)
			screen.setText(self.DOT_REMOVE_BUTTON_ID,self.DOT_PANEL_ID,self.DOT_REMOVE_BUTTON_TXT,CvUtil.FONT_LEFT_JUSTIFY,self.DOT_PANEL_TXT_X,self.DOT_PANEL_TXT_Y+self.TEXT_HEIGHT+self.DOT_PANEL_TXT_SPACING,self.Z_TXT,FontTypes.SMALL_FONT,WidgetTypes.WIDGET_GENERAL,-1,-1)
		elif self.bDotRemoving:
			text = " <color=0,255,0>%s</color> " % (self.DOT_REMOVE_BUTTON_TXT)
			screen.setText(self.DOT_REMOVE_BUTTON_ID,self.DOT_PANEL_ID,text,CvUtil.FONT_LEFT_JUSTIFY,self.DOT_PANEL_TXT_X,self.DOT_PANEL_TXT_Y+self.TEXT_HEIGHT+self.DOT_PANEL_TXT_SPACING,self.Z_TXT,FontTypes.SMALL_FONT,WidgetTypes.WIDGET_GENERAL,-1,-1)
			screen.setText(self.DOT_PLACE_BUTTON_ID,self.DOT_PANEL_ID,self.DOT_PLACE_BUTTON_TXT,CvUtil.FONT_LEFT_JUSTIFY,self.DOT_PANEL_TXT_X,self.DOT_PANEL_TXT_Y,self.Z_TXT,FontTypes.SMALL_FONT,WidgetTypes.WIDGET_GENERAL,-1,-1)
		else:
			screen.setText(self.DOT_PLACE_BUTTON_ID,self.DOT_PANEL_ID,self.DOT_PLACE_BUTTON_TXT,CvUtil.FONT_LEFT_JUSTIFY,self.DOT_PANEL_TXT_X,self.DOT_PANEL_TXT_Y,self.Z_TXT,FontTypes.SMALL_FONT,WidgetTypes.WIDGET_GENERAL,-1,-1)
			screen.setText(self.DOT_REMOVE_BUTTON_ID,self.DOT_PANEL_ID,self.DOT_REMOVE_BUTTON_TXT,CvUtil.FONT_LEFT_JUSTIFY,self.DOT_PANEL_TXT_X,self.DOT_PANEL_TXT_Y+self.TEXT_HEIGHT+self.DOT_PANEL_TXT_SPACING,self.Z_TXT,FontTypes.SMALL_FONT,WidgetTypes.WIDGET_GENERAL,-1,-1)

	def addSignControls(self):
		"""
		Adds the place/remove buttons to the sign panel
		"""
		screen = self.getScreen()
		screen.setText(self.SIGN_PLACE_ID,self.SIGN_PANEL_ID,self.SIGN_PLACE_TXT,CvUtil.FONT_LEFT_JUSTIFY,self.SIGN_PANEL_TXT_X,self.SIGN_PANEL_TXT_Y,self.Z_TXT,FontTypes.SMALL_FONT,WidgetTypes.WIDGET_GENERAL,-1,-1)
		screen.setText(self.SIGN_REMOVE_ID,self.SIGN_PANEL_ID,self.SIGN_REMOVE_TXT,CvUtil.FONT_LEFT_JUSTIFY,self.SIGN_PANEL_TXT_X,self.SIGN_PANEL_TXT_Y+self.TEXT_HEIGHT+self.TXT_SPACING,self.Z_TXT,FontTypes.SMALL_FONT,WidgetTypes.WIDGET_GENERAL,-1,-1)

	def updateSignControls(self):
		"""
		Updates the Sign Controls based on selection
		"""
		screen = self.getScreen()
		if not self.bSign:
			screen.hide(self.SIGN_PLACE_ID)
			screen.hide(self.SIGN_REMOVE_ID)
			screen.hide(self.SIGN_PANEL_ID)
			txtY = self.MAIN_TXT_Y + self.TXT_SPACING + self.TEXT_HEIGHT
			screen.setText(self.MAIN_SIGN_BUTTON_ID,self.MAIN_PANEL_ID,self.MAIN_SIGN_TXT,CvUtil.FONT_CENTER_JUSTIFY,self.MAIN_TXT_X,txtY,self.Z_TXT,FontTypes.SMALL_FONT,WidgetTypes.WIDGET_GENERAL,-1,-1)
			return
		screen.show(self.SIGN_PLACE_ID)
		screen.show(self.SIGN_REMOVE_ID)
		screen.show(self.SIGN_PANEL_ID)
		screen.setState(self.SIGN_PLACE_ID, self.bSignPlacing)
		screen.setState(self.SIGN_REMOVE_ID, self.bSignRemoving)
		text = " <color=0,255,0>%s</color> " % (self.MAIN_SIGN_TXT)
		txtY = self.MAIN_TXT_Y + self.TXT_SPACING + self.TEXT_HEIGHT
		screen.setText(self.MAIN_SIGN_BUTTON_ID,self.MAIN_PANEL_ID,text,CvUtil.FONT_CENTER_JUSTIFY,self.MAIN_TXT_X,txtY,self.Z_TXT,FontTypes.SMALL_FONT,WidgetTypes.WIDGET_GENERAL,-1,-1)
		if self.bSignPlacing:
			text = " <color=0,255,0>%s</color> " % (self.SIGN_PLACE_TXT)
			screen.setText(self.SIGN_PLACE_ID,self.SIGN_PANEL_ID,text,CvUtil.FONT_LEFT_JUSTIFY,self.SIGN_PANEL_TXT_X,self.SIGN_PANEL_TXT_Y,self.Z_TXT,FontTypes.SMALL_FONT,WidgetTypes.WIDGET_GENERAL,-1,-1)
			screen.setText(self.SIGN_REMOVE_ID,self.SIGN_PANEL_ID,self.SIGN_REMOVE_TXT,CvUtil.FONT_LEFT_JUSTIFY,self.SIGN_PANEL_TXT_X,self.SIGN_PANEL_TXT_Y+self.TEXT_HEIGHT+self.TXT_SPACING,self.Z_TXT,FontTypes.SMALL_FONT,WidgetTypes.WIDGET_GENERAL,-1,-1)
		elif self.bSignRemoving:
			text = " <color=0,255,0>%s</color> " % (self.SIGN_REMOVE_TXT)
			screen.setText(self.SIGN_PLACE_ID,self.SIGN_PANEL_ID,self.SIGN_PLACE_TXT,CvUtil.FONT_LEFT_JUSTIFY,self.SIGN_PANEL_TXT_X,self.SIGN_PANEL_TXT_Y,self.Z_TXT,FontTypes.SMALL_FONT,WidgetTypes.WIDGET_GENERAL,-1,-1)
			screen.setText(self.SIGN_REMOVE_ID,self.SIGN_PANEL_ID,text,CvUtil.FONT_LEFT_JUSTIFY,self.SIGN_PANEL_TXT_X,self.SIGN_PANEL_TXT_Y+self.TEXT_HEIGHT+self.TXT_SPACING,self.Z_TXT,FontTypes.SMALL_FONT,WidgetTypes.WIDGET_GENERAL,-1,-1)
		else:
			screen.setText(self.SIGN_PLACE_ID,self.SIGN_PANEL_ID,self.SIGN_PLACE_TXT,CvUtil.FONT_LEFT_JUSTIFY,self.SIGN_PANEL_TXT_X,self.SIGN_PANEL_TXT_Y,self.Z_TXT,FontTypes.SMALL_FONT,WidgetTypes.WIDGET_GENERAL,-1,-1)
			screen.setText(self.SIGN_REMOVE_ID,self.SIGN_PANEL_ID,self.SIGN_REMOVE_TXT,CvUtil.FONT_LEFT_JUSTIFY,self.SIGN_PANEL_TXT_X,self.SIGN_PANEL_TXT_Y+self.TEXT_HEIGHT+self.TXT_SPACING,self.Z_TXT,FontTypes.SMALL_FONT,WidgetTypes.WIDGET_GENERAL,-1,-1)

	#-------------------------------------------------------------------------------
	#   Input handlers
	#-------------------------------------------------------------------------------
	def onMainDotButton(self,inputClass):
		"""
		    Called on Main dot mapper button input
		"""
		if inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED:
			screen = self.getScreen()
			if self.bDotMapper:
				self.bDotMapper = False
				screen.hide(self.DOT_PANEL_ID)
				screen.hide(self.DOT_PLACE_BUTTON_ID)
				screen.hide(self.DOT_REMOVE_BUTTON_ID)
				screen.setText(self.MAIN_DOT_BUTTON_ID,self.MAIN_PANEL_ID,self.MAIN_DOT_TXT,CvUtil.FONT_CENTER_JUSTIFY,self.MAIN_TXT_X,self.MAIN_TXT_Y,self.Z_TXT,FontTypes.SMALL_FONT,WidgetTypes.WIDGET_GENERAL,-1,-1)
				CyInterface().setInterfaceMode(InterfaceModeTypes.INTERFACEMODE_SELECTION)
			else:
				self.bDotMapper = True
				self.bSignPlacing = False
				self.bSign = False
				self.bSignRemoving = False
				self.updateSignControls()
				text = " <color=0,255,0>%s</color>" % (self.MAIN_DOT_TXT)
				screen.setText(self.MAIN_DOT_BUTTON_ID,self.MAIN_PANEL_ID,text,CvUtil.FONT_CENTER_JUSTIFY,self.MAIN_TXT_X,self.MAIN_TXT_Y,self.Z_TXT,FontTypes.SMALL_FONT,WidgetTypes.WIDGET_GENERAL,-1,-1)
				screen.show(self.DOT_PANEL_ID)
				screen.show(self.DOT_PLACE_BUTTON_ID)
				screen.show(self.DOT_REMOVE_BUTTON_ID)
				if self.bDotPlacing or self.bDotRemoving:
					if CyInterface().getInterfaceMode() != InterfaceModeTypes.INTERFACEMODE_PYTHON_PICK_PLOT:
						CyInterface().setInterfaceMode(InterfaceModeTypes.INTERFACEMODE_PYTHON_PICK_PLOT)

	def onMainSignButton(self,inputClass):
		"""
		    Called on main sign button input
		"""
		if inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED:
			screen = self.getScreen()
			if self.bSign:
				self.bSign = False
				self.updateSignControls()
				txtY = self.MAIN_TXT_Y + self.TXT_SPACING + self.TEXT_HEIGHT
				screen.setText(self.MAIN_SIGN_BUTTON_ID,self.MAIN_PANEL_ID,self.MAIN_SIGN_TXT,CvUtil.FONT_CENTER_JUSTIFY,self.MAIN_TXT_X,txtY,self.Z_TXT,FontTypes.SMALL_FONT,WidgetTypes.WIDGET_GENERAL,-1,-1)
				CyInterface().setInterfaceMode(InterfaceModeTypes.INTERFACEMODE_SELECTION)
			else:
				self.bSign = True
				self.bDotMapper = False
				self.bDotPlacing = False
				self.bDotRemoving = False
				self.updateDotMapperControls()
				self.updateSignControls()
				text = " <color=0,255,0>%s</color> " % (self.MAIN_SIGN_TXT)
				txtY = self.MAIN_TXT_Y + self.TXT_SPACING + self.TEXT_HEIGHT
				screen.setText(self.MAIN_SIGN_BUTTON_ID,self.MAIN_PANEL_ID,text,CvUtil.FONT_CENTER_JUSTIFY,self.MAIN_TXT_X,txtY,self.Z_TXT,FontTypes.SMALL_FONT,WidgetTypes.WIDGET_GENERAL,-1,-1)
				if self.bSignPlacing or self.bSignRemoving:
					if CyInterface().getInterfaceMode() != InterfaceModeTypes.INTERFACEMODE_PYTHON_PICK_PLOT:
						CyInterface().setInterfaceMode(InterfaceModeTypes.INTERFACEMODE_PYTHON_PICK_PLOT)


	def onColorButton(self,inputClass):
		"""
			Called on Color Button input
		"""
		if inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED:
			self.updateColorControls(inputClass.getID())

	def onPlaceCityButton(self,inputClass):
		"""
			Called on Place City button input
		"""
		if inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED:
			if not self.bDotPlacing:
				if CyInterface().getInterfaceMode() != InterfaceModeTypes.INTERFACEMODE_PYTHON_PICK_PLOT:
					CyInterface().setInterfaceMode(InterfaceModeTypes.INTERFACEMODE_PYTHON_PICK_PLOT)
			else:
				CyInterface().setInterfaceMode(InterfaceModeTypes.INTERFACEMODE_SELECTION)
			self.bDotPlacing = not self.bDotPlacing
			if self.bDotRemoving:
				self.bDotRemoving = False
			self.updateDotMapperControls()

	def onRemoveCityButton(self,inputClass):
		"""
			Called on Remove City button input
		"""
		if inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED:
			if not self.bDotRemoving:
				if CyInterface().getInterfaceMode() != InterfaceModeTypes.INTERFACEMODE_PYTHON_PICK_PLOT:
					CyInterface().setInterfaceMode(InterfaceModeTypes.INTERFACEMODE_PYTHON_PICK_PLOT)
			else:
				CyInterface().setInterfaceMode(InterfaceModeTypes.INTERFACEMODE_SELECTION)
			self.bDotRemoving = not self.bDotRemoving
			if self.bDotPlacing:
				self.bDotPlacing = False
			self.updateDotMapperControls()

	def onPlaceSignButton(self,inputClass):
		"""
		    Called on Place Sign button input
		"""
		if inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED:
			if not self.bSignPlacing:
				if CyInterface().getInterfaceMode() != InterfaceModeTypes.INTERFACEMODE_PYTHON_PICK_PLOT:
					CyInterface().setInterfaceMode(InterfaceModeTypes.INTERFACEMODE_PYTHON_PICK_PLOT)
			else:
				CyInterface().setInterfaceMode(InterfaceModeTypes.INTERFACEMODE_SELECTION)
			self.bSignPlacing = not self.bSignPlacing
			if self.bSignRemoving:
				self.bSignRemoving = False
			self.updateSignControls()

	def onRemoveSignButton(self,inputClass):
		"""
		    Called on Remove Sign button input
		"""
		if inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED:
			if not self.bSignRemoving:
				if CyInterface().getInterfaceMode() != InterfaceModeTypes.INTERFACEMODE_PYTHON_PICK_PLOT:
					CyInterface().setInterfaceMode(InterfaceModeTypes.INTERFACEMODE_PYTHON_PICK_PLOT)
			else:
				CyInterface().setInterfaceMode(InterfaceModeTypes.INTERFACEMODE_SELECTION)
			self.bSignRemoving = not self.bSignRemoving
			if self.bSignPlacing:
				self.bSignPlacing = False
			self.updateSignControls()

	def onExitButton(self,inputClass):
		"""
			Called on exit button input
		"""
		self.hideScreen()

	def onLeftMouseDown(self):
		"""
			Called on left mouse click on the main ui
		"""
		if self.currentPlot != 0:
			if self.bDotPlacing:
				if self.cityData.has_key((self.currentPlotX,self.currentPlotY)):
					self.eraseDotMap(self.currentPlotX,self.currentPlotY)
				self.drawDotMap(self.currentPlotX,self.currentPlotY)
				if CyInterface().getInterfaceMode() != InterfaceModeTypes.INTERFACEMODE_PYTHON_PICK_PLOT:
					CyInterface().setInterfaceMode(InterfaceModeTypes.INTERFACEMODE_PYTHON_PICK_PLOT)
			elif self.bDotRemoving:
				if self.cityData.has_key((self.currentPlotX,self.currentPlotY)):
					self.eraseDotMap(self.currentPlotX,self.currentPlotY)
				if CyInterface().getInterfaceMode() != InterfaceModeTypes.INTERFACEMODE_PYTHON_PICK_PLOT:
					CyInterface().setInterfaceMode(InterfaceModeTypes.INTERFACEMODE_PYTHON_PICK_PLOT)
			elif self.bSignPlacing:
				if self.signData.has_key((self.currentPlotX,self.currentPlotY)):
					text, playerID = self.signData.get((self.currentPlotX, self.currentPlotY))
					CyEngine().removeSign(self.currentPlot, playerID)
					del self.signData[(self.currentPlotX, self.currentPlotY)]
				CvEventInterface.getEventManager().beginEvent(EventOverlayAddSign, (self.currentPlotX,self.currentPlotY))
				if CyInterface().getInterfaceMode() != InterfaceModeTypes.INTERFACEMODE_PYTHON_PICK_PLOT:
					CyInterface().setInterfaceMode(InterfaceModeTypes.INTERFACEMODE_PYTHON_PICK_PLOT)
			elif self.bSignRemoving:
				if self.signData.has_key((self.currentPlotX, self.currentPlotY)):
					CyEngine().removeSign(self.currentPlot,g_GC.getGame().getActivePlayer())
					del self.signData[(self.currentPlotX, self.currentPlotY)]
				if CyInterface().getInterfaceMode() != InterfaceModeTypes.INTERFACEMODE_PYTHON_PICK_PLOT:
					CyInterface().setInterfaceMode(InterfaceModeTypes.INTERFACEMODE_PYTHON_PICK_PLOT)

	def onMouseOverPlot(self, argsList):
		"""
		Called from CVOverlayScreenUtils when mousing over a plot when the screen is active
		Updates the current plot and its x/y location
		"""
		self.currentPlot = CyInterface().getMouseOverPlot()
		self.currentPlotX = self.currentPlot.getX()
		self.currentPlotY = self.currentPlot.getY()

	#-------------------------------------------------------------------------------
	#   Dot mapping functions
	#-------------------------------------------------------------------------------
	def drawDotMap(self,x,y):
		"""
		    Draws a dot map at a location x,y
		"""
		for cx in range(x-2,x+3):
			for cy in range(y-2,y+3):
				if ( not (cx == x+2 or cx == x-2) or not (cy == y+2 or cy == y-2)):
					CyEngine().fillAreaBorderPlotAlt(cx,cy,self.currentLayer,self.COLOR_KEYS[self.currentColor],self.DOT_ALPHA)
		CyEngine().addColoredPlotAlt(x,y,self.DOT_STYLE,self.PLOT_LAYER,self.COLOR_KEYS[self.currentColor],self.DOT_ALPHA)
		self.cityData[(x,y)] = (self.currentColor, self.currentLayer)

	def eraseDotMap(self,x,y):
		"""
		    Erases a dot map at a location x,y
		"""
		cityColor, cityLayer = self.cityData.get((x,y))
		del self.cityData[(x,y)]
		self.clearDots()
		self.clearLayer(cityLayer)
		self.redrawDotMap()

	def clearDots(self):
		"""
		    Clears all the dots from screen
		"""
		CyEngine().clearColoredPlots(self.PLOT_LAYER)

	def clearLayer(self,index):
		"""
		    Clears the indexed border layer
		"""
		CyEngine().clearAreaBorderPlots(index)

	def clearAllLayers(self):
		"""
		    Clears all the layers and dots
		"""
		for index in range(len(self.COLOR_KEYS)+1):
			self.clearLayer(index)
		self.clearDots()

	def redrawDotMap(self):
		"""
		    Redraws the dot map from the current cityData
		"""
		tempColor = self.currentColor
		tempLayer = self.currentLayer
		for location,data in self.cityData.iteritems():
			cityX,cityY = location
			self.currentColor, self.currentLayer = data
			self.drawDotMap(cityX,cityY)
		self.currentColor = tempColor
		self.currentLayer = tempLayer

	def saveSign(self, x, y, signText, player):
		self.signData[(x, y)] = (signText, player)

	def removeSigns(self):
		for key, value in self.signData.iteritems():
			x,y = key
			text,player = value
			plot = g_GC.getMap().plot(x,y)
			CyEngine().removeSign(plot,player)

	def addAllSigns(self):
		for key, value in self.signData.iteritems():
			x,y = key
			text,player = value
			plot = g_GC.getMap().plot(x,y)
			CyEngine().addSign(plot, player, text)

	#-------------------------------------------------------------------------------
	#   Saving and loading functions
	#-------------------------------------------------------------------------------
	def loadVars(self):
		"""
		    Loads saved city data
		"""
		self.cityData = sdGetGlobal(self.MOD_SAVE_ID, self.CITY_SAVE_ID)
		if not self.cityData:
			self.cityData = {}
		self.signData = sdGetGlobal(self.MOD_SAVE_ID, self.SIGN_SAVE_ID)
		if not self.signData:
			self.signData = {}

	def saveVars(self):
		"""
		Saves mapped cities
		Called on closing of screen
		"""
		sdSetGlobal(self.MOD_SAVE_ID, self.CITY_SAVE_ID, self.cityData)
		sdSetGlobal(self.MOD_SAVE_ID, self.SIGN_SAVE_ID, self.signData)
