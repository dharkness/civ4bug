##################################################
## CvOverlayScreen.py
##
## Screen to display for additional strategy layer
## Allows for dot mapping of cities
## Author: Del69
## Date: 10/20/08 
## 
## Placed in CustomAssets/Python/Screens/ for bug mod use
##################################################

from CvPythonExtensions import *
import CvUtil
import CvScreensInterface
import CvStrategyOverlayScreenEnums
import ScreenInput
from SdToolKit import *

# globals

gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

class CvOverlayScreen:
	"""
	Screen for the strategy overlay
	"""
	def __init__(self):
		# Unique Text IDS
		self.PREFIX = "OverlayScreen"
		self.MANAGER_ID = self.PREFIX + "MainWindow"
		self.BACKGROUND_ID = self.PREFIX + "Background"
		self.EXIT_ID = self.PREFIX + "ExitWidget"
		self.WIDGET_ID = self.PREFIX + "Widget"
		self.BUTTON_ID = self.PREFIX + "Button"
		self.HEADER_ID = self.WIDGET_ID + "Header"
		self.PLACE_BUTTON = self.BUTTON_ID + "PlaceCity"
		self.REMOVE_BUTTON = self.BUTTON_ID + "RemoveCity"
		self.COLOR_ID = self.PREFIX + "ColorPanel"
		self.COLOR_BUTTON_ID = self.BUTTON_ID + "Color"
		
		################################
		## Debug stuff
		################################
		self.DEBUGGING = False
		self.DEBUGTXT = "Strategy Overlay Debug: "
		
		################################
		## Variable Saving IDS
		################################
		self.MODNAME = "StrategyOverlay"
		self.DICTNAME = "CityDataDict"
		
		################################
		## POSITIONS
		################################
		
		# Button Panel Size
		self.X_PANEL = 10
		self.Y_PANEL = 75
		self.W_PANEL = 200
		self.H_PANEL = 130
		self.Border = 10
		# Exit Button Text
		self.X_EXIT = self.X_PANEL + self.Border
		self.Y_EXIT = self.Y_PANEL + self.H_PANEL - 40
		# Title
		self.Y_TITLE = self.Y_PANEL + self.Border
		self.X_TITLE = self.X_PANEL + self.W_PANEL/2
		# Z Depth of controls and background
		self.Z_BACKGROUND = -.1
		self.Z_CONTROLS = self.Z_BACKGROUND - 0.2
		self.DZ = -0.2
		# Buttons
		self.ButtonSize = 24
		self.ButtonMargin = 5
		self.X_BUTTON = self.X_PANEL + self.Border
		self.Y_BUTTON = self.Y_PANEL + 40
		self.X_CAPTION = self.X_BUTTON + self.ButtonSize
		self.Y_CAPTION = self.Y_BUTTON + self.ButtonSize / 2 - self.Border
		
		# Colors, each color is on a diff layer
		self.Colors = [
			'COLOR_WHITE',
			'COLOR_BLACK',
			'COLOR_RED',
			'COLOR_GREEN',
			'COLOR_CYAN',
			'COLOR_BLUE',
			'COLOR_YELLOW',
			'COLOR_MAGENTA']
		# Text to display for each color
		self.ColorText = [
			"White",
			"Black",
			"Red",
			"Green",
			"Cyan",
			"Blue",
			"Yellow",
			"Magenta"]
		self.CurrentColor = "COLOR_WHITE"
		self.NumColors = 8

		# Color Button Size 
		self.SZ_COLOR_BUTTON = 20
		# Color Panel
		self.COLOR_MARGIN = 10
		self.X_COLOR = self.X_PANEL
		self.Y_COLOR = self.Y_PANEL + self.H_PANEL + self.Border
		self.W_COLOR = self.W_PANEL
		self.H_COLOR = self.NumColors * (self.SZ_COLOR_BUTTON) + 40 
		# Color Title
		self.X_COLOR_TITLE = self.X_COLOR + self.W_COLOR/2
		self.Y_COLOR_TITLE = self.Y_COLOR + self.COLOR_MARGIN
		# Color Text Position
		self.X_COLOR_TEXT = self.X_COLOR_TITLE
		self.Y_COLOR_TEXT = self.Y_COLOR_TITLE + self.COLOR_MARGIN
		
		#######################
		# States
		#######################
		
		# Place or remove buttons on
		self.bPlace = False
		self.bRemove = False
		self.bLeftMouseDown = False
		self.bFirstRun = True
		# Current Plot 
		self.CurrentPlot = 0
		# Current Plot coordinates being mousedover
		self.CurrentPlotX = 0
		self.CurrentPlotY = 0
		# Current Layer
		self.CurrentLayer = 0
		self.PlotLayer = PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_RECOMMENDED_PLOTS
		# Plot style to use for city dots
		self.CurrentPlotStyle = PlotStyles.PLOT_STYLE_DOT_TARGET
		# List of city's layers
		self.CurrentCityNum = 0
		# contains a city layer, key is a x,y tuple and value is a tuple of the layer and color 
		self.CityData = {}
		# alpha value to use when drawing
		self.CurrentAlpha = 1.0
		
		# Input mapping - each widget is mapped to a function to call on clicking it or other input
		self.OverlayScreenInputMap = {
			self.COLOR_BUTTON_ID : self.ColorButtons,
			self.PLACE_BUTTON  : self.PlaceCity,
			self.REMOVE_BUTTON : self.RemoveCity,
			self.EXIT_ID : self.ExitScreen,
		}

	def getScreen(self):
		"""
		Gets the screen interface object
		"""
		return CyGInterfaceScreen(self.MANAGER_ID, CvStrategyOverlayScreenEnums.SO_OVERLAY_SCREEN )
		
	def hideScreen(self):
		"""
		Hides the screen, call to clear overlay is needed in case esc was used to close the screen
		"""
		self.ClearOverlay()
		self.SaveVars()
		screen = self.getScreen()
		screen.hideScreen()
		return None
	
	def update(self, fDelta):
		"""
		intercepts the clicks on the main ui, if bLeftMouseDown is True the mouse button hasn't been released since
		the function was called, fDelta is passed as a dummy since LeftMouseDown doesn't use the arglist at all
		"""
		if CyInterface().isLeftMouseDown():
			if not self.bLeftMouseDown:
				self.LeftMouseDown(fDelta)
			self.bLeftMouseDown = True
		else:
			self.bLeftMouseDown = False
		return
	
	def handleInput(self, inputClass):
		"""
		Handles the input to the screen
		Checks the key map for the widget name and executes the mapped function
		"""
		if(self.OverlayScreenInputMap.has_key(inputClass.getFunctionName())):
			self.OverlayScreenInputMap.get(inputClass.getFunctionName())(inputClass)
			return 1
		return 0
		
	def interfaceScreen(self):
		"""
		Creates the screen and adds the widgets to it then displays it
		"""
		screen = self.getScreen()
		if screen.isActive():
			return
		self.EXIT_TEXT = u"<font=4>" + localText.getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + "</font>"
		self.TITLE_TEXT = u"<font=4>" + "Strategy Overlay".upper() + "</font>"
		
		#Set up the background panel and buttons
		screen.addPanel("OverlayScreenBG",u"",u"",True,False,self.X_PANEL,self.Y_PANEL,self.W_PANEL,self.H_PANEL,PanelStyles.PANEL_STYLE_MAIN)
		screen.setText(self.EXIT_ID, "", self.EXIT_TEXT, CvUtil.FONT_LEFT_JUSTIFY, self.X_EXIT, self.Y_EXIT, -1.9, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1)
		#Header  
		screen.setLabel(self.HEADER_ID,"OverlayScreenBG", self.TITLE_TEXT, CvUtil.FONT_CENTER_JUSTIFY, self.X_TITLE, self.Y_TITLE, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		#Buttons
		screen.addCheckBoxGFC(self.PLACE_BUTTON, ArtFileMgr.getInterfaceArtInfo("WORLDBUILDER_TOGGLE_CITY_EDIT_MODE").getPath(), ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),self.X_BUTTON, self.Y_BUTTON, self.ButtonSize, self.ButtonSize, WidgetTypes.WIDGET_GENERAL, -1, -1, ButtonStyles.BUTTON_STYLE_LABEL)
		screen.setLabel("",self.PLACE_BUTTON,"Place City", CvUtil.FONT_LEFT_JUSTIFY, self.X_CAPTION, self.Y_CAPTION, -.2,FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.addCheckBoxGFC(self.REMOVE_BUTTON, ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_CANCEL").getPath(), ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),self.X_BUTTON, self.Y_BUTTON + self.ButtonSize + self.ButtonMargin, self.ButtonSize, self.ButtonSize, WidgetTypes.WIDGET_GENERAL, -1, -1, ButtonStyles.BUTTON_STYLE_LABEL)
		screen.setLabel("",self.PLACE_BUTTON,"Remove City", CvUtil.FONT_LEFT_JUSTIFY, self.X_CAPTION, self.Y_CAPTION + self.ButtonSize + self.ButtonMargin, -.2,FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		#Color selection panel
		screen.addPanel(self.COLOR_ID, u"",u"",True,False,self.X_COLOR,self.Y_COLOR,self.W_COLOR,self.H_COLOR,PanelStyles.PANEL_STYLE_MAIN)
		screen.setLabel("",self.COLOR_ID, "<font=4>Color Selection</font>", CvUtil.FONT_CENTER_JUSTIFY,self.X_COLOR_TITLE, self.Y_COLOR_TITLE, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1) 
		#Color Buttons
		for index in range(self.NumColors):
			self.ButtonName = self.COLOR_BUTTON_ID + str(index)
			screen.setText(self.ButtonName, "", self.ColorText[index], CvUtil.FONT_CENTER_JUSTIFY, self.X_COLOR_TEXT, self.Y_COLOR_TEXT + index*self.SZ_COLOR_BUTTON + self.COLOR_MARGIN, -1.9, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)               
		
		#Don't Close Screen On Escape
		screen.setCloseOnEscape(False)
		#set screen dimensions to whole screen so we can intercept events?
		screen.setDimensions(0,0,screen.getXResolution(),screen.getYResolution())
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, True)
		
		#load up cities since last and draw them
		self.InitVars()
	
	def InitVars(self):
		"""
		Sets the place/remove flags correctly for when the screen opens up since the buttons are
		unselected when first opened up
		"""
		self.bPlace = False
		self.bRemove = False
		self.LoadVars()
	
	def LoadVars(self):
		"""
		Loads the saved cities and draws them on the map if there
		Called on opening of screen
		"""
		self.CityData = sdGetGlobal(self.MODNAME, self.DICTNAME)
		if self.CityData:
			self.RedrawCities()
		else:
			self.CityData = {}
			
	def SaveVars(self):
		"""
		Saves mapped cities
		Called on closing of screen
		"""
		sdSetGlobal(self.MODNAME, self.DICTNAME, self.CityData)
		
	def ExitScreen(self, inputClass):
		"""
		Exits the screen, wrapper for hideScreen() to be called from the input handler with a inputClass parameter
		"""
		self.hideScreen()
		
	def PlaceCity(self, inputClass):
		"""
		Called when the place city button is clicked
		Checks the place/remove flags and adjusts them and the widget highlights accordingly
		Also sets the interface mode to pick mode or regular if turned on or off respectivly 
		"""
		screen = self.getScreen()
		if(inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED):
			if self.bRemove:
				screen.setState(self.REMOVE_BUTTON,False)
				self.bRemove = False
				CyInterface().setInterfaceMode(InterfaceModeTypes.INTERFACEMODE_SELECTION)
			if self.bPlace:
				screen.setState(self.PLACE_BUTTON,False)
				self.bPlace = False
				CyInterface().setInterfaceMode(InterfaceModeTypes.INTERFACEMODE_SELECTION)
			else:
				screen.setState(self.PLACE_BUTTON,True)
				self.bPlace = True
				CyInterface().setInterfaceMode(InterfaceModeTypes.INTERFACEMODE_PYTHON_PICK_PLOT)
		if self.DEBUGGING:
			sdEcho(self.DEBUGTXT + "Removing: " + str(self.bRemove) + ", Placing: " + str(self.bPlace))
		return 0
		
	def RemoveCity(self, inputClass):
		"""
		Called when the remove city button is clicked
		Checks the place/remove flags and adjusts them and the widget highlights accordingly
		Also sets the interface mode to pick mode or regular if turned on or off respectivly 
		"""
		screen = self.getScreen()
		if(inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED):
			if self.bPlace:
				screen.setState(self.PLACE_BUTTON,False)
				self.bPlace = False
				CyInterface().setInterfaceMode(InterfaceModeTypes.INTERFACEMODE_SELECTION)
			if self.bRemove:                
				screen.setState(self.REMOVE_BUTTON,False)
				self.bRemove = False
				CyInterface().setInterfaceMode(InterfaceModeTypes.INTERFACEMODE_SELECTION)
			else:
				screen.setState(self.REMOVE_BUTTON,True)
				self.bRemove = True
				CyInterface().setInterfaceMode(InterfaceModeTypes.INTERFACEMODE_PYTHON_PICK_PLOT)
		if self.DEBUGGING:
			sdEcho(self.DEBUGTXT + "Removing: " + str(self.bRemove) + ", Placing: " + str(self.bPlace))
		return 0
	
	def ColorButtons(self, inputClass):
		"""
		Handler for clicking on a color selection button
		Sets the current color and layer to use based on the selection
		"""
		if(inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED):
			self.CurrentColor = self.Colors[inputClass.getID()]
			self.CurrentLayer = inputClass.getID()
			#apparently layer 5 is the one the picker uses so we'll increment above that
			if self.CurrentLayer >= 5:
				self.CurrentLayer += 1
		if self.DEBUGGING:
			sdEcho(self.DEBUGTXT + "Color: " + str(self.CurrentColor) + ", Layer: " + str(self.CurrentLayer))
		
	def DrawCity(self, x, y):
		"""
		Draws the Big Fat Cross of a city and a dot in the middle
		@Param x: Map X of the city
		@Param y: Map Y of the city
		@Param alpha: Alpha value to use, from 0.0 to 1.0?
		"""
		for cx in range(x-2,x+3):
			for cy in range(y-2,y+3):
				if ( not (cx == x+2 or cx == x-2) or not (cy == y+2 or cy == y-2)): 
					CyEngine().fillAreaBorderPlotAlt(cx,cy,self.CurrentLayer,self.CurrentColor,self.CurrentAlpha)
		CyEngine().addColoredPlotAlt(x, y, self.CurrentPlotStyle, self.PlotLayer, self.CurrentColor, self.CurrentAlpha)
		
	def DrawCityDot(self, x, y):
		"""
		Draws just the dot of a cities big fat cross, used to redraw all the city dots placed after erasing one
		@param x: X Location of the city
		@param y: Y Location of the city
		"""
		CyEngine().addColoredPlotAlt(x,y,self.CurrentPlotStyle, self.PlotLayer, self.CurrentColor, self.CurrentAlpha)

	def RedrawCities(self):
		"""
		Redraws all the cities stored in the Dictionary
		Need to do this since all the dots are on the same layer and clearing one clears them all.
		Also done to redraw all the mapped cities after closing and reopening the screen
		"""
		#save current layer and color
		tempCol = self.CurrentColor
		tempLayer = self.CurrentLayer
		for location,data in self.CityData.iteritems():
			cityx, cityy = location
			layer, color = data
			self.CurrentColor = color
			self.CurrentLayer = layer
			self.DrawCity(cityx, cityy)
		#restore layer and color
		self.CurrentColor = tempCol
		self.CurrentLayer = tempLayer

	def ClearOverlay(self):
		"""
		Clears all the overlays
		Iterates through each layer and clears it, does one above the number of colors since layer 5
		is the one the Picker uses and is skipped over when actually drawing
		"""
		for index in range(self.NumColors+1):
			CyEngine().clearAreaBorderPlots(index)            
		CyEngine().clearColoredPlots(self.PlotLayer)
		
	def EraseCity(self, x, y):
		"""
		Clears a city
		Since the clear function clears all the overlays 
		Iterates through the city's x,y vals and replace the dots since they all get cleared on the call to clear one
		@param x: X location of the city
		@param y: Y Location of the city
		"""
		# Get Layer to erase from the dict
		layerToErase, cityColor = self.CityData.get((x,y))
		# delete the entry out of the dict
		del self.CityData[(x,y)]
		#clear the overlays
		self.ClearOverlay()
		# Iterate through the city data and replace the ones not erased
		self.RedrawCities()
			
	def MouseOverPlot(self, argsList):
		"""
		Called from CVOverlayScreenUtils when mousing over a plot when the screen is active
		Updates the current plot and its x/y location
		""" 
		self.CurrentPlot = CyInterface().getMouseOverPlot()
		self.CurrentPlotX = self.CurrentPlot.getX()
		self.CurrentPlotY = self.CurrentPlot.getY()
		
		
	def LeftMouseDown(self, argsList):
		"""
		Called on left mouse click on the game surface from the update handler
		"""
		if (self.CurrentPlot != 0) and (self.bPlace): #see if we're placing
			if self.CityData.has_key((self.CurrentPlotX,self.CurrentPlotY)): #erase the city thats there if present
				self.EraseCity(self.CurrentPlotX,self.CurrentPlotY)
			self.CityData[(self.CurrentPlotX,self.CurrentPlotY)] = (self.CurrentLayer, self.CurrentColor)
			self.DrawCity(self.CurrentPlotX, self.CurrentPlotY)
			# reactivate the picker since we're not exiting the place mode
			CyInterface().setInterfaceMode(InterfaceModeTypes.INTERFACEMODE_PYTHON_PICK_PLOT)
		elif (self.CurrentPlot != 0) and (self.bRemove): #removing the city?
			if(self.CityData.has_key((self.CurrentPlotX,self.CurrentPlotY))): #check if there is a city at the pick point
				self.EraseCity(self.CurrentPlotX, self.CurrentPlotY)
			#if there isn't a city at the pick just reset to picking mode
			CyInterface().setInterfaceMode(InterfaceModeTypes.INTERFACEMODE_PYTHON_PICK_PLOT)
		elif (self.bRemove or self.bPlace):
			CyInterface().setInterfaceMode(InterfaceModeTypes.INTERFACEMODE_PYTHON_PICK_PLOT)
		
