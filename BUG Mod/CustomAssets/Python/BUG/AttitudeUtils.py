#
# Attitude tools
# version 0.1
# By: Ruff_hi
#


from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums
import math

import CvForeignAdvisor
import DomPyHelpers
import TechTree

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()










import re

import BugScreensOptions
BugScreens = BugScreensOptions.getOptions()


ATTITUDE_DICT = {
    "COLOR_YELLOW": re.sub (":", "|", localText.getText ("TXT_KEY_ATTITUDE_FRIENDLY", ())),
    "COLOR_GREEN" : re.sub (":", "|", localText.getText ("TXT_KEY_ATTITUDE_PLEASED", ())),
    "COLOR_CYAN" : re.sub (":", "|", localText.getText ("TXT_KEY_ATTITUDE_ANNOYED", ())),
    "COLOR_RED" : re.sub (":", "|", localText.getText ("TXT_KEY_ATTITUDE_FURIOUS", ())),
    }


#iAtt = gc.getPlayer(ePlayer).AI_getAttitude(gc.getGame().getActivePlayer())
#cAtt =  unichr(ord(unichr(CyGame().getSymbolID(FontSymbols.POWER_CHAR) + 4)) + iAtt)

def getAttitudeString (nPlayer, nTarget):
    if (nPlayer != nTarget
    and gc.getTeam(gc.getPlayer(nPlayer).getTeam()).isHasMet(gc.getPlayer(nTarget).getTeam())):
        return CyGameTextMgr().getAttitudeString(nPlayer, nTarget)

def getAttitudeCategory (nPlayer, nTarget):
    if (nPlayer != nTarget
    and gc.getTeam(gc.getPlayer(nPlayer).getTeam()).isHasMet(gc.getPlayer(nTarget).getTeam())):
        return gc.getPlayer(nPlayer).AI_getAttitude(nTarget)

def getAttitudeColor (nPlayer, nTarget):
    COLOR_ARRAY = ["COLOR_RED", "COLOR_CYAN", "COLOR_CLEAR", "COLOR_GREEN", "COLOR_YELLOW"]
    return COLOR_ARRAY[getAttitudeCategory (nPlayer, nTarget)]

def getAttitudeIcon (nPlayer, nTarget):
    if (nPlayer != nTarget
    and gc.getTeam(gc.getPlayer(nPlayer).getTeam()).isHasMet(gc.getPlayer(nTarget).getTeam())):
        iAtt = getAttitudeCategory (nPlayer, nTarget)
        return unichr(ord(unichr(CyGame().getSymbolID(FontSymbols.POWER_CHAR) + 4)) + iAtt)



#cAtt =  unichr(ord(unichr(CyGame().getSymbolID(FontSymbols.POWER_CHAR) + 4)) + iAtt)



def getAttitudeCount (nPlayer, nTarget):
    sAttStr = getAttitudeString(nPlayer, nTarget)
    if sAttStr == None:
        return

    nAtt = 0
    ltPlusAndMinuses = re.findall ("[-+][0-9]+", sAttStr)
    for i in range (len (ltPlusAndMinuses)):
        nAtt += int (ltPlusAndMinuses[i])

    return nAtt



def getAttitudeText (nPlayer, nTarget, vOnlyNumbers = True):
    nAttitude = getAttitudeCount (nPlayer, nTarget)

    if nAttitude == None:
        return None

    szText = str (nAttitude)

    if nAttitude > 0:
        szText = "+" + szText

    if vOnlyNumbers:
        return szText

    if BugScreens.isShowGlanceSmilies():
        szText = "[" + szText + "] "
    else:
        szText = "<font=3>   " + szText + "</font> "

    sColor = getAttitudeColor (nPlayer, nTarget)
    szText = localText.changeTextColor (szText, gc.getInfoTypeForString(sColor))

    pPlayer = gc.getPlayer(nPlayer)
    pTarget = gc.getPlayer(nTarget)
    if BugScreens.isShowGlanceSmilies():
        iAtt = pPlayer.AI_getAttitude(nTarget)
        szSmilie = unichr(ord(unichr(CyGame().getSymbolID(FontSymbols.POWER_CHAR) + 4)) + iAtt)
        szText = szSmilie + " " + szText
    
    szWorstEnemy = pPlayer.getWorstEnemyName()
    if szWorstEnemy and pTarget.getName() == szWorstEnemy:
        szText +=  u"%c" %(CyGame().getSymbolID(FontSymbols.ANGRY_POP_CHAR))
    
    nTeam = pPlayer.getTeam()
    pTeam = gc.getTeam(nTeam)
    nTargetTeam = pTarget.getTeam()
    pTargetTeam = gc.getTeam(nTargetTeam)
    if pTeam.isAtWar(nTargetTeam):
        szText += u"%c" % (gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getChar() + 25)
    elif gc.getGame().getActiveTeam() in (nTeam, nTargetTeam):
        bPeace = False
        if pTeam.isForcePeace(nTargetTeam):
            bPeace = True
        elif pTargetTeam.isAVassal():
            for nOwnerTeam in range(gc.getMAX_TEAMS()):
                if pTargetTeam.isVassal(nOwnerTeam) and pTeam.isForcePeace(nOwnerTeam):
                    bPeace = True
                    break
        if bPeace:
            szText += u"%c" % (gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getChar() + 26)

    return szText
