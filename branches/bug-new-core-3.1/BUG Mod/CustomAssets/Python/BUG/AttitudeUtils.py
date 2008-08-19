## AttitudeUtils
##
## Utility functions for dealing with AI Attitudes.
##
## Notes
##   - Must be initialized externally by calling init()
##
## Copyright (c) 2008 The BUG Mod.
##
## Author: Ruff_hi, EmperorFool

from CvPythonExtensions import *
import BugUtil
import re

DEFAULT_COLORS = (
	"COLOR_RED", 
	"COLOR_CYAN", 
	"COLOR_CLEAR", 
	"COLOR_GREEN", 
	"COLOR_YELLOW",
)
ATTITUDE_COLORS = None
ATTITUDE_ICONS = None

# globals
gc = CyGlobalContext()

def init (colors=DEFAULT_COLORS):
	global ATTITUDE_ICONS
	ATTITUDE_ICONS = (unichr(CyGame().getSymbolID(FontSymbols.POWER_CHAR) + 4 + i) 
					  for i in range(5))
	global ATTITUDE_COLORS
	ATTITUDE_COLORS = map(gc.getInfoTypeForString, colors)
	invalidCount = ATTITUDE_COLORS.count(-1)
	if invalidCount > 0:
		raise BugUtil.ConfigError("%d invalid color(s)" % invalidCount)

def getAttitudeString (nPlayer, nTarget):
	if (nPlayer != nTarget
	and gc.getTeam(gc.getPlayer(nPlayer).getTeam()).isHasMet(gc.getPlayer(nTarget).getTeam())):
		return CyGameTextMgr().getAttitudeString(nPlayer, nTarget)

def getAttitudeCategory (nPlayer, nTarget):
	if (nPlayer != nTarget
	and gc.getTeam(gc.getPlayer(nPlayer).getTeam()).isHasMet(gc.getPlayer(nTarget).getTeam())):
		return gc.getPlayer(nPlayer).AI_getAttitude(nTarget)

def getAttitudeColor (nPlayer, nTarget):
	return ATTITUDE_COLORS[getAttitudeCategory(nPlayer, nTarget)]

def getAttitudeIcon (nPlayer, nTarget):
	if (nPlayer != nTarget
	and gc.getTeam(gc.getPlayer(nPlayer).getTeam()).isHasMet(gc.getPlayer(nTarget).getTeam())):
		return ATTITUDE_ICONS[getAttitudeCategory(nPlayer, nTarget)]

def getAttitudeCount (nPlayer, nTarget):
	sAttStr = getAttitudeString(nPlayer, nTarget)
	if sAttStr == None:
		return
	nAtt = 0
	# TODO: Replace with simple line-by-line handling
	#	   (so it doesn't get tricked by leader names)
	ltPlusAndMinuses = re.findall ("[-+][0-9]+", sAttStr)
	for i in range (len (ltPlusAndMinuses)):
		nAtt += int (ltPlusAndMinuses[i])
	return nAtt


def getAttitudeText (nPlayer, nTarget, vNumbers, vSmilies, vWorstEnemy, vWarPeace):
	nAttitude = getAttitudeCount (nPlayer, nTarget)
	if nAttitude == None:
		return None
	
	if vNumbers:
		szText = str (nAttitude)
		if nAttitude > 0:
			szText = "+" + szText
		if vSmilies:
			szText = "[" + szText + "] "
		else:
			szText = "<font=3>   " + szText + "</font> "
	else:
		szText = ""
	
	iColor = getAttitudeColor (nPlayer, nTarget)
	szText = BugUtil.colorText(szText, iColor)
	
	if vSmilies:
		szText = getAttitudeIcon(nPlayer, nTarget) + " " + szText
	
	pPlayer = gc.getPlayer(nPlayer)
	pTarget = gc.getPlayer(nTarget)
	if vWorstEnemy:
		szWorstEnemy = pPlayer.getWorstEnemyName()
		if szWorstEnemy and pTarget.getName() == szWorstEnemy:
			szText +=  u"%c" %(CyGame().getSymbolID(FontSymbols.ANGRY_POP_CHAR))
	
	if vWarPeace:
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
