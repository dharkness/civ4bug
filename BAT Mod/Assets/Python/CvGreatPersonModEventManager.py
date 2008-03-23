#
# GreatPersonMod BTS
# CvGreatPersonModEventManager
# 

from CvPythonExtensions import *

import CvUtil
import CvEventManager
import sys
import PyHelpers
import CvGreatPersonScreen
import RandomNameUtils
import CvConfigParser
# Change the value to enable or disable the features from the Great Person Mod.
# Default value is true
g_bGreatPersonModFeaturesEnabled = true

gc = CyGlobalContext()

PyPlayer = PyHelpers.PyPlayer

g_iCount = 0     # autoincrement global used as the primary key for dictionary
g_dict = dict()  # holds information transferred from here to CvGreatPersonScreen.py

class CvGreatPersonModEventManager:

	def __init__(self, eventManager):

		GreatPerson(eventManager)

class AbstractGreatPerson(object):

	def __init__(self, eventManager, *args, **kwargs):
		super(AbstractGreatPerson, self).__init__(*args, **kwargs)

class GreatPerson(AbstractGreatPerson):

	def __init__(self, eventManager, *args, **kwargs):
		super(GreatPerson, self).__init__(eventManager, *args, **kwargs)

		eventManager.addEventHandler("greatPersonBorn", self.onGreatPersonBorn)

		self.eventMgr = eventManager

		# Begin Test Code
		""" # Uncomment this block to enable test code
		eventManager.addEventHandler("kbdEvent", self.onKbdEvent)

	# Test (ok cheat...) code to make sure that we can go through the vanilla great person
	# names and test the random names.
	## Changed event from just clicking mouse to hitting ALT-SHIFT-G. Test code not multiplayer compatible.
	## def onMouseEvent(self, argsList):
	def onKbdEvent(self, argsList):
		eventType,key,mx,my,px,py = argsList

		if(not g_bGreatPersonModFeaturesEnabled):
			return

		if ( eventType == self.eventMgr.EventKeyDown ):
			theKey=int(key)
			
			# Check if ALT + Shift + G was hit
			if (theKey == int(InputTypes.KB_G) and self.eventMgr.bAlt and self.eventMgr.bShift):	
				gc.getActivePlayer().getCapitalCity().createGreatPeople(gc.getInfoTypeForString("UNIT_GENERAL"), False, False)
				return 1
			
			# Check if CTRL + Shift + G was hit
			if (theKey == int(InputTypes.KB_G) and self.eventMgr.bCtrl and self.eventMgr.bShift):	
				gc.getActivePlayer().getCapitalCity().createGreatPeople(gc.getInfoTypeForString("UNIT_GREAT_SPY"), False, False)
				return 1
		return 0
		"""
		# End Test Code


	def onGreatPersonBorn(self, argsList):
		'Great Person Born'

		if(not g_bGreatPersonModFeaturesEnabled):
			return
		
		pUnit, iPlayer, pCity = argsList
		player = gc.getPlayer(iPlayer)
        
		# Check if we should even show the popup:
		if pUnit.isNone() or pCity.isNone():
			return
		
		#CvUtil.pyPrint("Great Person Born: Name:<%s> Player:<%s> City:<%s>"%(pUnit.getNameNoDesc(), player.getName(), pCity.getName()))
		    
		#If Person doesn't have unique name, give him a random one
		if(len(pUnit.getNameNoDesc()) == 0):
			iCivilizationType = player.getCivilizationType()
			pUnit.setName(RandomNameUtils.getRandomCivilizationName(iCivilizationType))

		#Show fancy lil popup if a human got the great person:
		if player.isHuman():
		
			global g_dict
			global g_iCount
			
			g_dict[g_iCount] = (pUnit, iPlayer, pCity)
			
			#CvUtil.pyPrint("Great Person Born 2: Name:<%s> iPlayer:<%d> City:<%s>"%(g_dict[g_iCount][0].getNameNoDesc(), g_dict[g_iCount][1], g_dict[g_iCount][2].getName()))
			
			popupInfo = CyPopupInfo()
			popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON_SCREEN)
			popupInfo.setData1(g_iCount)
			g_iCount += 1
			popupInfo.setText(u"showGreatPersonScreen")
			popupInfo.addPopup(iPlayer)