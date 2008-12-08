###############################################
## CvStrategyOverlayScreenUtils.py
## Created on : 10-20-08
## By Del69 for Strategy Overlay mod 
##
## Class derived from CvScreenUtils for custom handling of CvOverlayScreen
## Placed in CustomAssets/Python/Contrib for Bug mod use
###############################################
from CvPythonExtensions import *
import CvOverlayScreen
import CvScreenUtils
from CvStrategyOverlayScreenEnums import *

overlayScreen = CvOverlayScreen.CvOverlayScreen()
def showOverlayScreen():
	"""
	Shows the Overlay Screen from CvOverlayScreen.py
	"""
	overlayScreen.interfaceScreen()

class CvOverlayScreenUtils:
	"""
	Derived CvScreenUtils class for custom handling of mod screens
	@cvar HandleInputMap: Maps the screen's enum to its class for passing off input handlers for widget events
	"""
	
	HandleInputMap = {
					SO_OVERLAY_SCREEN : overlayScreen, # Pass off input to the overlay screen for it to handle
					}

	def leftMouseDown (self, argsList):
		# return 1 to consume the input
		screenEnum = argsList[0]
		if (screenEnum == SO_OVERLAY_SCREEN):
			overlayScreen.LeftMouseDown(argsList)
			return 1
		return 0
			
	def rightMouseDown (self, argsList):
		# return 1 to consume the input
		screenEnum = argsList[0]
			
		return 0

	def mouseOverPlot(self, argsList):
		# return 1 to consume the input
		# CyInterface().addImmediateMessage("Mouse Over Plot called", "")
		screenEnum = argsList[0]
		# consuming the input would probably prevent the engine from highlighting the square
		if (screenEnum == SO_OVERLAY_SCREEN):
			overlayScreen.MouseOverPlot(argsList)
		return 0

	def update(self, argsList):
		"""
		Updates a screen
		
		@param argsList: First item is the screen's enum value, second one is passed to the screens update method
		@return: 0 to let the event keep going, 1 to consume it
		"""
		screenEnum = argsList[0]
		if (screenEnum == SO_OVERLAY_SCREEN):
			overlayScreen.update(argsList)
		return 0

	def handleInput (self, argsList):
		"""
		Called when a screen is up
		Gets the active screen from the HandleInputMap Dictionary and calls the handle input on that screen
		"""
		screenEnum, inputClass = argsList
		if (self.HandleInputMap and inputClass and self.HandleInputMap.has_key(screenEnum)):
			# get the screen that is active from the HandleInputMap Dictionary
			screen = self.HandleInputMap.get( inputClass.getPythonFile() )
		
			# call handle input on that screen
			if ( screen ):
				# return 1 to consume input
				return screen.handleInput(inputClass)
		return 0

	# Screen closing
	def onClose (self, argsList):
		screenEnum = argsList[0]
		return 0

	# Forced screen update
	def forceScreenUpdate (self, argsList):
		screenEnum = argsList[0]
		# place call to update function here
		return 0

	# Forced redraw
	def forceScreenRedraw (self, argsList):
		screenEnum = argsList[0]
		# place call to redraw function here

		return 0

	# Minimap Clicked
	def minimapClicked(self, argsList):
		screenEnum = argsList[0]
		# place call to mini map function here
		return 0
	
