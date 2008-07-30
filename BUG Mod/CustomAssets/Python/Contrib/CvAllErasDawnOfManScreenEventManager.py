## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
##
## All Eras Dawn Of Man Screen Mod by Jeckel.
##

from CvPythonExtensions import *
import Popup as PyPopup
import CvUtil

# globals
gc = CyGlobalContext()

class CvAllErasDawnOfManScreenEventManager:
	def __init__(self, eventManager):

		# initialize base class
		eventManager.addEventHandler("GameStart", self.onGameStart)

	def onGameStart(self, argsList):
		if ( gc.getGame().getGameTurnYear() != gc.getDefineINT("START_YEAR") ) :
			if (gc.getGame().getGameTurn() == gc.getGame().getStartTurn()) or (gc.getGame().countNumHumanGameTurnActive() == 0):
				for iPlayer in range(gc.getMAX_PLAYERS()):
					pPlayer = gc.getPlayer(iPlayer)
					if (pPlayer.isAlive()) and (pPlayer.isHuman()):
						popupInfo = CyPopupInfo()
						popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON_SCREEN)
						popupInfo.setText(u"showDawnOfMan")
						popupInfo.addPopup(iPlayer)
