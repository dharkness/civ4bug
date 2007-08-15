##-------------------------------------------------------------------
## Ruff Debug Echo
##-------------------------------------------------------------------

from CvPythonExtensions import *
import CvUtil
import RuffModControl
RuffMod = RuffModControl.RuffModConfig()

def RuffEcho(echoString, printToScr, printToLog):
	if (RuffMod.get_boolean('DEBUG', 'ShowMessages', False)):
		szMessage = "%s" %(echoString)
		if (printToScr):
			CyInterface().addMessage(CyGame().getActivePlayer(), True, 10, szMessage, "", 2, None, ColorTypes(8), 0, 0, False, False)
		if (printToLog):
			CvUtil.pyPrint(szMessage)
		return 0

#VOID addMessage(PlayerType ePlayer,
#	BOOL bForce,
#	INT iLength,
#	STRING szString,
#	STRING szSound,
#	InterfaceMessageType eType,
#	STRING szIcon,
#	ColorType eFlashColor,
#	INT iFlashX,
#	INT iFlashY,
#	BOOL bShowOffScreenArrows,
#	BOOL bShowOnScreenArrows)
