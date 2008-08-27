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

NUM_ATTITUDES = 5

FURIOUS = 0
ANNOYED = 1
CAUTIOUS = 2
PLEASED = 3
FRIENDLY = 4

DEFAULT_COLORS = (
	"COLOR_RED", 
	"COLOR_CYAN", 
	"COLOR_CLEAR", 
	"COLOR_GREEN", 
	"COLOR_YELLOW",
)
ATTITUDE_COLORS = None
ATTITUDE_ICONS = None

gc = CyGlobalContext()

def init (colors=DEFAULT_COLORS):
	"""Initializes this module, raising ConfigError if any problems occur."""
	# create font icons for each attitude level
	global ATTITUDE_ICONS
	ATTITUDE_ICONS = [unichr(CyGame().getSymbolID(FontSymbols.POWER_CHAR) + 4 + i) 
					  for i in range(5)]
	if len(ATTITUDE_ICONS) != NUM_ATTITUDES:
		raise BugUtil.ConfigError("Failed to create attitude icons")
	
	# convert colors to type IDs
	if len(colors) != NUM_ATTITUDES:
		raise BugUtil.ConfigError("Expected %d colors" % NUM_ATTITUDES)
	global ATTITUDE_COLORS
	ATTITUDE_COLORS = map(gc.getInfoTypeForString, colors)
	invalidCount = ATTITUDE_COLORS.count(-1)
	if invalidCount > 0:
		invalid = []
		for id, color in zip(ATTITUDE_COLORS, colors):
			if id == -1:
				invalid.append(color)
		raise BugUtil.ConfigError("Given %d invalid colors: %s" % (invalidCount, str(invalid)))


def hasAttitude (nPlayer, nTarget):
	"""Returns True if nTarget can see nPlayer's attitude toward them."""
	return (nPlayer != nTarget
	        and gc.getTeam(gc.getPlayer(nPlayer).getTeam()).isHasMet(gc.getPlayer(nTarget).getTeam()))

def getAttitudeString (nPlayer, nTarget):
	"""Returns the full hover text with attitude modifiers nPlayer has toward nTarget."""
	if hasAttitude(nPlayer, nTarget):
		return CyGameTextMgr().getAttitudeString(nPlayer, nTarget)
	return None

def getAttitudeCategory (nPlayer, nTarget):
	"""Returns the attitude level nPlayer has toward nTarget [0,4]."""
	if hasAttitude(nPlayer, nTarget):
		return gc.getPlayer(nPlayer).AI_getAttitude(nTarget)
	return None

def getAttitudeColor (nPlayer, nTarget):
	"""Returns the color of the attitude nPlayer has toward nTarget."""
	iCategory = getAttitudeCategory(nPlayer, nTarget)
	if iCategory is not None:
		return ATTITUDE_COLORS[iCategory]
	return -1

def getAttitudeIcon (nPlayer, nTarget):
	"""Returns the font icon of the attitude nPlayer has toward nTarget."""
	iCategory = getAttitudeCategory(nPlayer, nTarget)
	if iCategory is not None:
		return ATTITUDE_ICONS[iCategory]
	return ""

def getAttitudeCount (nPlayer, nTarget):
	"""Returns the total attitude modifiers nPlayer has toward nTarget."""
	sAttStr = getAttitudeString(nPlayer, nTarget)
	if sAttStr == None:
		return
	nAtt = 0
	# TODO: Replace with simple line-by-line handling
	#	    so it doesn't get tricked by leader names (": " fixes issue)
	ltPlusAndMinuses = re.findall ("[-+][0-9]+: ", sAttStr)
	for i in range (len (ltPlusAndMinuses)):
		nAtt += int (ltPlusAndMinuses[i][:-2])
	return nAtt


def getAttitudeText (nPlayer, nTarget, bNumber, bSmily, bWorstEnemy, bWarPeace):
	"""Returns a string describing the attitude nPlayer has toward nTarget."""
	nAttitude = getAttitudeCount (nPlayer, nTarget)
	if nAttitude == None:
		return None
	
	if bNumber:
		szText = str (nAttitude)
		if nAttitude > 0:
			szText = "+" + szText
		if bSmily:
			szText = "[" + szText + "] "
		else:
			szText = "<font=3>   " + szText + "</font> "
	else:
		szText = ""
	
	iColor = getAttitudeColor (nPlayer, nTarget)
	szText = BugUtil.colorText(szText, iColor)
	
	if bSmily:
		szText = getAttitudeIcon(nPlayer, nTarget) + " " + szText
	
	pPlayer = gc.getPlayer(nPlayer)
	pTarget = gc.getPlayer(nTarget)
	if bWorstEnemy:
		szWorstEnemy = pPlayer.getWorstEnemyName()
		if szWorstEnemy and pTarget.getName() == szWorstEnemy:
			szText +=  u"%c" %(CyGame().getSymbolID(FontSymbols.ANGRY_POP_CHAR))
	
	if bWarPeace:
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
