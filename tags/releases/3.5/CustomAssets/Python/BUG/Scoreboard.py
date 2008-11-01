## Scoreboard
##
## Holds the information used to display the scoreboard.
##
## Notes
##   - Must be initialized externally by calling init()
##   - Add 'DealCanceled' event for onDealCanceled()
##
## Copyright (c) 2007-2008 The BUG Mod.
##
## Author: EmperorFool

from CvPythonExtensions import *
import BugCore
import BugUtil
import DealUtil
import PlayerUtil
import CvUtil
import re
import string

# Globals
ScoreOpt = BugCore.game.Scores
gc = CyGlobalContext()

# Constants
ICON_SIZE = 24
ROW_HEIGHT = 22
Z_DEPTH = -0.3

# Columns IDs
NUM_PARTS = 21
(
	ALIVE,
	WAR,
	SCORE,
	SCORE_DELTA,
	MASTER,
	NAME,
	NOT_MET,
	POWER,
	RESEARCH,
	RESEARCH_TURNS,
	ESPIONAGE,
	TRADE,
	BORDERS,
	PACT,
	RELIGION,
	ATTITUDE,
	WORST_ENEMY,
	WHEOOH,
	WAITING,
	NET_STATS,
	OOS
) = range(NUM_PARTS)

# Types
SKIP = 0
FIXED = 1
DYNAMIC = 2
SPECIAL = 3

# Column Definitions
columns = []
columnsByKey = {}

TRADE_TYPES = (
	TradeableItems.TRADE_OPEN_BORDERS,
	TradeableItems.TRADE_DEFENSIVE_PACT,
	TradeableItems.TRADE_PERMANENT_ALLIANCE,
	TradeableItems.TRADE_PEACE_TREATY,
)

def init():
	"""Initializes the strings used to display the scoreboard."""
	global columns
	game = CyGame()
	
	# Used keys:
	# ABCDEHLMNOPRSTUVWZ*?
	# FGIJKQXY
	columns.append(Column('', ALIVE))
	columns.append(Column('S', SCORE, DYNAMIC))
	columns.append(Column('Z', SCORE_DELTA, DYNAMIC))
	columns.append(Column('V', MASTER, FIXED, u"<font=2>%c</font>" % game.getSymbolID(FontSymbols.SILVER_STAR_CHAR)))
	columns.append(Column('C', NAME, DYNAMIC))
	columns.append(Column('?', NOT_MET, FIXED, u"<font=2>?</font>"))
	columns.append(Column('W', WAR, DYNAMIC))
	columns.append(Column('P', POWER, DYNAMIC))
	columns.append(Column('T', RESEARCH, SPECIAL))
	columns.append(Column('U', RESEARCH_TURNS, DYNAMIC))
	columns.append(Column('E', ESPIONAGE, FIXED, u"<font=2>%c</font>" %(gc.getCommerceInfo(CommerceTypes.COMMERCE_ESPIONAGE).getChar())))
	columns.append(Column('N', TRADE, FIXED, u"<font=2>%c</font>" % game.getSymbolID(FontSymbols.TRADE_CHAR)))
	columns.append(Column('B', BORDERS, FIXED, u"<font=2>%c</font>" % game.getSymbolID(FontSymbols.OPEN_BORDERS_CHAR)))
	columns.append(Column('D', PACT, FIXED, u"<font=2>%c</font>" % game.getSymbolID(FontSymbols.DEFENSIVE_PACT_CHAR)))
	columns.append(Column('R', RELIGION, DYNAMIC))
	columns.append(Column('A', ATTITUDE, DYNAMIC))
	columns.append(Column('H', WORST_ENEMY, FIXED, u"<font=2>%c</font>" % game.getSymbolID(FontSymbols.ANGRY_POP_CHAR)))
	columns.append(Column('M', WHEOOH, FIXED, u"<font=2>%c</font>" % game.getSymbolID(FontSymbols.OCCUPATION_CHAR)))
	columns.append(Column('*', WAITING, FIXED, u"<font=2>*</font>"))
	columns.append(Column('L', NET_STATS, DYNAMIC))
	columns.append(Column('O', OOS, DYNAMIC))
	
	global WAR_ICON, PEACE_ICON
	WAR_ICON = u"<font=2>%c</font>" %(gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getChar() + 25)
	PEACE_ICON = u"<font=2>%c</font>" %(gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getChar() + 26)
	
	global VASSAL_PREFIX, VASSAL_POSTFIX
	VASSAL_PREFIX = u" - "   # u" %c " % game.getSymbolID(FontSymbols.BULLET_CHAR)
	VASSAL_POSTFIX = u" - "   # u" %c " % game.getSymbolID(FontSymbols.BULLET_CHAR)

def onDealCanceled(argsList):
	"""Sets the scoreboard dirty bit so it will redraw."""
	CyInterface().setDirty(InterfaceDirtyBits.Score_DIRTY_BIT, True)


class Column:
	
	def __init__(self, key, id, type=SKIP, text=None, alt=None):
		self.key = key
		self.id = id
		self.type = type
		self.text = text
		self.alt = alt
		if (type == FIXED):
			self.width = CyInterface().determineWidth( text )
		else:
			self.width = 0
		if (key):
			columnsByKey[key] = self
	
	def isSkip(self):
		return self.type == SKIP
	
	def isFixed(self):
		return self.type == FIXED
	
	def isDynamic(self):
		return self.type == DYNAMIC
	
	def isSpecial(self):
		return self.type == SPECIAL
	
	def isDynamic(self):
		return self.type == DYNAMIC


class Scoreboard:
	"""Holds and builds the ScoreCards."""
	
	def __init__(self):
		self._activePlayer = gc.getGame().getActivePlayer()
		self._teamScores = []
		self._playerScores = []
		self._teamScoresByID = {}
		self._anyHas = [ False ] * NUM_PARTS
		self._currTeamScores = None
		self._currPlayerScore = None
		self._deals = DealUtil.findDealsByPlayerAndType(self._activePlayer, TRADE_TYPES)
		
	def addTeam(self, team, rank):
		self._currTeamScores = TeamScores(self, team, rank)
		self._teamScores.append(self._currTeamScores)
		self._teamScoresByID[team.getID()] = self._currTeamScores
		self._currPlayerScore = None
		
	def getTeamScores(self, eTeam):
		return self._teamScoresByID.get(eTeam, None)
		
	def addPlayer(self, player, rank):
		if self._currTeamScores:
			self._currPlayerScore = self._currTeamScores.addPlayer(player, rank)
			self._playerScores.append(self._currPlayerScore)
		
	def size(self):
		return len(self._playerScores)
		
		
	def setAlive(self):
		self._set(ALIVE)
		
	def setMaster(self):
		self._set(MASTER)
		
	def setScore(self, value):
		self._set(SCORE, u"<font=2>%s</font>" % value)
		
	def setScoreDelta(self, value):
		self._set(SCORE_DELTA, u"<font=2>%s</font>" % value)
		
	def setName(self, value):
		self._set(NAME, u"<font=2>%s</font>" % value)
		
	def setNotMet(self):
		self._set(NOT_MET)
		
	def setWHEOOH(self):
		self._set(WHEOOH)
		
	def setWar(self):
		self._set(WAR, WAR_ICON)
		
	def setPeace(self):
		self._set(WAR, PEACE_ICON, self._getDealWidget(TradeableItems.TRADE_PEACE_TREATY))
		
	def setPower(self, value):
		self._set(POWER, u"<font=2>%s</font>" % value)
		
	def setResearch(self, tech, turns):
		if (ScoreOpt.isShowResearchIcons()):
			self._set(RESEARCH, tech)
		else:
			self._set(RESEARCH, u"<font=2>%s</font>" % gc.getTechInfo(tech).getDescription())
		self._set(RESEARCH_TURNS, u"<font=2> (%d)</font>" % turns)
		
	def setEspionage(self):
		self._set(ESPIONAGE)
		
	def setTrade(self):
		self._set(TRADE)
		
	def setBorders(self):
		self._set(BORDERS, True, self._getDealWidget(TradeableItems.TRADE_OPEN_BORDERS))
		
	def setPact(self):
		self._set(PACT, True, self._getDealWidget(TradeableItems.TRADE_DEFENSIVE_PACT))
		
	def setReligion(self, value):
		self._set(RELIGION, u"<font=2>%s</font>" % value)
		
	def setAttitude(self, value):
		self._set(ATTITUDE, u"<font=2>%s</font>" % value)
		
	def setWorstEnemy(self):
		self._set(WORST_ENEMY)
		
		
	def setWaiting(self):
		self._set(WAITING)
		
	def setNetStats(self, value):
		self._set(NET_STATS, u"<font=2>%s</font>" % value)
		
	def setOOS(self, value):
		self._set(OOS, u"<font=2>%s</font>" % value)
		
		
	def _getDealWidget(self, type):
		# lookup the Deal containing the given tradeable item type
		deals = self._deals.get(self._currPlayerScore.getID(), None)
		if deals:
			deal = deals.get(type, None)
			if deal:
				return (WidgetTypes.WIDGET_DEAL_KILL, deal.getID(), -1)
		return (WidgetTypes.WIDGET_DEAL_KILL, -1, -1)
		
	def _set(self, part, value=True, widget=None):
		self._anyHas[part] = True
		self._currPlayerScore.set(part, value, widget)
		
		
	def gatherVassals(self):
		for teamScores in self._teamScores:
			teamScores.gatherVassals()
		
	def sort(self):
		"""Sorts the list by pulling any vassals up below their masters."""
		if ScoreOpt.isGroupVassals():
			self._playerScores.sort(lambda x, y: cmp(x.sortKey(), y.sortKey()))
			self._playerScores.reverse()
		
	def hide(self, screen):
		"""Hides the text from the screen before building the scoreboard."""
		screen.hide( "ScoreBackground" )
		for p in range( gc.getMAX_CIV_PLAYERS() ):
			name = "ScoreText%d" %( p ) # the part that flashes? holds the score and name
			screen.hide( name )
			for c in range( NUM_PARTS ):
				name = "ScoreText%d-%d" %( p, c )
				screen.hide( name )
		
	def draw(self, screen):
		"""Sorts and draws the scoreboard right-to-left, bottom-to-top."""
		timer = BugUtil.Timer("scores")
		self.hide(screen)
		self.gatherVassals()
		self.sort()
		interface = CyInterface()
		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()
		
		x = xResolution - 12 # start here and shift left with each column
		if ( interface.getShowInterface() == InterfaceVisibility.INTERFACE_SHOW or interface.isInAdvancedStart()):
			y = yResolution - 206
		else:
			y = yResolution - 88
		totalWidth = 0
		if (ScoreOpt.isShowResearchIcons()):
			height = ROW_HEIGHT
		else:
			height = ROW_HEIGHT
		
		defaultSpacing = ScoreOpt.getDefaultSpacing()
		spacing = defaultSpacing
		format = re.findall('(-?[0-9]+|[^0-9])', ScoreOpt.getDisplayOrder().replace(' ', '').upper())
		format.reverse()
		for k in format:
			if k == '-':
				spacing = 0
				continue
			if k[0] in string.digits or k[0] == '-':
				spacing = int(k)
				continue
			if (not columnsByKey.has_key(k)):
				spacing = defaultSpacing
				continue
			column = columnsByKey[k]
			c = column.id
			if (not self._anyHas[c]):
				spacing = defaultSpacing
				continue
			type = column.type
			if (c == RESEARCH and not ScoreOpt.isShowResearchIcons()):
				# switch SPECIAL research icon to DYNAMIC name
				type = DYNAMIC
			
			if (type == SKIP):
				spacing = defaultSpacing
				continue
			
			elif (type == FIXED):
				width = column.width
				value = column.text
				x -= spacing
				for p, playerScore in enumerate(self._playerScores):
					if (playerScore.has(c) and playerScore.value(c)):
						name = "ScoreText%d-%d" %( p, c )
						widget = playerScore.widget(c)
						if widget is None:
							if (playerScore.value(ALIVE)):
								widget = (WidgetTypes.WIDGET_CONTACT_CIV, playerScore.getID(), -1)
							else:
								widget = (WidgetTypes.WIDGET_GENERAL, -1, -1)
						screen.setText( name, "Background", value, CvUtil.FONT_RIGHT_JUSTIFY, 
										x, y - p * height, Z_DEPTH, 
										FontTypes.SMALL_FONT, *widget )
						screen.show( name )
				x -= width
				totalWidth += width + spacing
				spacing = defaultSpacing
			
			elif (type == DYNAMIC):
				width = 0
				for playerScore in self._playerScores:
					if (playerScore.has(c)):
						value = playerScore.value(c)
						if (c == NAME and playerScore.isVassal() and ScoreOpt.isGroupVassals()):
							if (ScoreOpt.isLeftAlignName()):
								value = VASSAL_PREFIX + value
							else:
								value += VASSAL_POSTFIX
						newWidth = interface.determineWidth( value )
						if (newWidth > width):
							width = newWidth
				if (width == 0):
					spacing = defaultSpacing
					continue
				x -= spacing
				for p, playerScore in enumerate(self._playerScores):
					if (playerScore.has(c)):
						name = "ScoreText%d-%d" %( p, c )
						value = playerScore.value(c)
						if (c == NAME and playerScore.isVassal() and ScoreOpt.isGroupVassals()):
							if (ScoreOpt.isLeftAlignName()):
								value = VASSAL_PREFIX + value
							else:
								value += VASSAL_POSTFIX
						align = CvUtil.FONT_RIGHT_JUSTIFY
						adjustX = 0
						if (c == NAME):
							name = "ScoreText%d" % p
							if (ScoreOpt.isLeftAlignName()):
								align = CvUtil.FONT_LEFT_JUSTIFY
								adjustX = width
						widget = playerScore.widget(c)
						if widget is None:
							if (playerScore.value(ALIVE)):
								widget = (WidgetTypes.WIDGET_CONTACT_CIV, playerScore.getID(), -1)
							else:
								widget = (WidgetTypes.WIDGET_GENERAL, -1, -1)
						screen.setText( name, "Background", value, align, 
										x - adjustX, y - p * height, Z_DEPTH, 
										FontTypes.SMALL_FONT, *widget )
						screen.show( name )
				x -= width
				totalWidth += width + spacing
				spacing = defaultSpacing
			
			else: # SPECIAL
				if (c == RESEARCH):
					x -= spacing
					for p, playerScore in enumerate(self._playerScores):
						if (playerScore.has(c)):
							tech = playerScore.value(c)
							name = "ScoreTech%d" % p
							info = gc.getTechInfo(tech)
							screen.addDDSGFC( name, info.getButton(), x - ICON_SIZE, y - p * height - 1, ICON_SIZE, ICON_SIZE, 
											  WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, tech, -1 )
					x -= ICON_SIZE
					totalWidth += ICON_SIZE + spacing
					spacing = defaultSpacing
		
		for playerScore in self._playerScores:
			interface.checkFlashReset( playerScore.getID() )
		
		if ( interface.getShowInterface() == InterfaceVisibility.INTERFACE_SHOW or interface.isInAdvancedStart()):
			y = yResolution - 186
		else:
			y = yResolution - 68
		screen.setPanelSize( "ScoreBackground", xResolution - 21 - totalWidth, y - (height * self.size()) - 4, 
							 totalWidth + 12, (height * self.size()) + 8 )
		screen.show( "ScoreBackground" )
		timer.log()


class TeamScores:
	def __init__(self, scoreboard, team, rank):
		self._scoreboard = scoreboard
		self._team = team
		self._rank = rank
		self._playerScores = []
		self._isVassal = team.isAVassal()
		self._master = None
		self._vassalTeamScores = []
		
	def team(self):
		return self._team
		
	def rank(self):
		if self.isVassal():
			return self._master.rank()
		else:
			return self._rank
		
	def isVassal(self):
		return self._isVassal
	
	def addPlayer(self, player, rank):
		playerScore = PlayerScore(self, player, rank)
		self._playerScores.append(playerScore)
		return playerScore
	
	def addVassal(self, teamScore):
		self._vassalTeamScores.append(teamScore)
		
	def gatherVassals(self):
		if self._team.isAVassal():
			for eTeam in range( gc.getMAX_TEAMS() ):
				teamScores = self._scoreboard.getTeamScores(eTeam)
				if teamScores and self._team.isVassal(eTeam):
					teamScores.addVassal(self)
					self._master = teamScores
					for playerScore in teamScores._playerScores:
						playerScore.set(MASTER)
					self._scoreboard._anyHas[MASTER] = True


class PlayerScore:
	def __init__(self, teamScore, player, rank):
		self._teamScore = teamScore
		self._isVassal = teamScore.isVassal()
		self._player = player
		self._rank = rank
		self._has = [False] * NUM_PARTS
		self._values = [None] * NUM_PARTS
		self._widgets = [None] * NUM_PARTS
		self._sortKey = None
		
	def player(self):
		return self._player
		
	def rank(self):
		return self._rank
		
	def isVassal(self):
		return self._isVassal
	
	def getID(self):
		return self._player.getID()
		
	def sortKey(self):
		if self._sortKey is None:
				self._sortKey = (self._teamScore.rank(), self._isVassal, self._rank)
		return self._sortKey
		
	def set(self, part, value=True, widget=None):
		self._has[part] = True
		self._values[part] = value
		self._widgets[part] = widget
		
	def has(self, part):
		return self._has[part]
		
	def value(self, part):
		return self._values[part]
		
	def widget(self, part):
		return self._widgets[part]