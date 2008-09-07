## Scoreboard
##
## Holds the information used to display the scoreboard.
##
## Copyright (c) 2007-2008 The BUG Mod.
##
## Author: EmperorFool

from CvPythonExtensions import *
import BugCore
import TradeUtil
import CvUtil
import re
import string

# Globals
ScoresOpt = BugCore.game.Scores
gc = CyGlobalContext()

# Constants
ICON_SIZE = 24
ROW_HEIGHT = 22
Z_DEPTH = -0.3

# Columns: War Power Tech Espionage Network OpenBorders DefesivePact Religion Attitude
ALIVE = 0
PLAYER = ALIVE + 1
SCORE = PLAYER + 1
SCORE_DELTA = SCORE + 1
NAME = SCORE_DELTA + 1
NOT_MET = NAME + 1
WAR = NOT_MET + 1
POWER = WAR + 1
RESEARCH = POWER + 1
RESEARCH_TURNS = RESEARCH + 1
ESPIONAGE = RESEARCH_TURNS + 1
TRADE = ESPIONAGE + 1
BORDERS = TRADE + 1
PACT = BORDERS + 1
RELIGION = PACT + 1
ATTITUDE = RELIGION + 1
WORST_ENEMY = ATTITUDE + 1
WAITING = WORST_ENEMY + 1
NET_STATS = WAITING + 1
OOS = NET_STATS + 1

NUM_PARTS = OOS + 1

# Types
SKIP = 0
FIXED = 1
DYNAMIC = 2
SPECIAL = 3

bInitDone = False
columns = []
columnsByKey = {}
ordered = [ SCORE, SCORE_DELTA, NOT_MET, WAR, 
			ESPIONAGE, POWER, RESEARCH, RESEARCH_TURNS, 
			TRADE, BORDERS, PACT, RELIGION, ATTITUDE, WORST_ENEMY, 
			WAITING, NET_STATS, OOS ]
ordered.reverse()

TRADE_TYPES = (
	TradeableItems.TRADE_OPEN_BORDERS,
	TradeableItems.TRADE_DEFENSIVE_PACT,
	TradeableItems.TRADE_PERMANENT_ALLIANCE,
	TradeableItems.TRADE_PEACE_TREATY,
)

def _init():
	"""Initializes the strings used to display the scoreboard.
	
	This is called from constructor instead of when the module is loaded
	because GC isn't fully set up otherwise."""
	global bInitDone
	if (bInitDone):
		return
	
	global columns
	game = CyGame()
	
	# Used keys:
	# ABCDEHLNOPRSTUWZ*?
	# FGIJKMQVXY
	columns.append(Column('', ALIVE))
	columns.append(Column('', PLAYER))
	columns.append(Column('S', SCORE, DYNAMIC))
	columns.append(Column('Z', SCORE_DELTA, DYNAMIC))
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
	columns.append(Column('*', WAITING, FIXED, u"<font=2>*</font>"))
	columns.append(Column('L', NET_STATS, DYNAMIC))
	columns.append(Column('O', OOS, DYNAMIC))
	
	global WAR_ICON, PEACE_ICON
	WAR_ICON = u"<font=2>%c</font>" %(gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getChar() + 25)
	PEACE_ICON = u"<font=2>%c</font>" %(gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getChar() + 26)
	
	bInitDone = True


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
		_init()
		self.activePlayer = gc.getGame().getActivePlayer()
		self.has = []
		self.values = []
		self.widgets = []
		self.hasAny = [ False ] * NUM_PARTS
		self.currPlayer = -1
		self.currHas = None
		self.currValues = None
		self.currWidgets = None
		self.count = 0
		self.deals = TradeUtil.findDealsByPlayerAndType(self.activePlayer, TRADE_TYPES)
		
	def addPlayer(self, player):
		self.currPlayer = player
		self.currHas = [ False ] * NUM_PARTS
		self.currValues = [ None ] * NUM_PARTS
		self.currWidgets = [ None ] * NUM_PARTS
		self.has.append(self.currHas)
		self.values.append(self.currValues)
		self.widgets.append(self.currWidgets)
		self.count += 1
		self.setPlayer(player)
		
	def size(self):
		return self.count
		
		
	def setAlive(self):
		self._set(ALIVE)
		
	def setPlayer(self, value):
		self._set(PLAYER, value)
		
	def setScore(self, value):
		self._set(SCORE, u"<font=2>%s</font>" % value)
		
	def setScoreDelta(self, value):
		self._set(SCORE_DELTA, u"<font=2>%s</font>" % value)
		
	def setName(self, value):
		self._set(NAME, u"<font=2>%s</font>" % value)
		
	def setNotMet(self):
		self._set(NOT_MET)
		
	def setWar(self):
		self._set(WAR, WAR_ICON)
		
	def setPeace(self):
		self._set(WAR, PEACE_ICON, self._getDealWidget(TradeableItems.TRADE_PEACE_TREATY))
		
	def setPower(self, value):
		self._set(POWER, u"<font=2>%s</font>" % value)
		
	def setResearch(self, tech, turns):
		if (ScoresOpt.isShowResearchIcons()):
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
		deals = self.deals.get(self.currPlayer, None)
		if deals:
			deal = deals.get(type, None)
			if deal:
				return (WidgetTypes.WIDGET_DEAL_KILL, deal.getID(), -1)
		return (WidgetTypes.WIDGET_DEAL_KILL, -1, -1)
		
	def _set(self, part, value=True, widget=None):
		self.hasAny[part] = True
		self.currHas[part] = True
		self.currValues[part] = value
		self.currWidgets[part] = widget
		
		
	def hide(self, screen):
		"""Hides the text from the screen before building the scoreboard."""
		screen.hide( "ScoreBackground" )
		for p in range( gc.getMAX_PLAYERS() ):
			name = "ScoreText%d" %( p ) # the part that flashes? holds the score and name
			screen.hide( name )
			for c in range( NOT_MET, NUM_PARTS ):
				name = "ScoreText%d-%d" %( p, c )
				screen.hide( name )
		
	def draw(self, screen):
		"""Draws the scoreboard right-to-left, bottom-to-top."""
		interface = CyInterface()
		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()
		
		x = xResolution - 12 # start here and shift left with each column
		if ( interface.getShowInterface() == InterfaceVisibility.INTERFACE_SHOW or interface.isInAdvancedStart()):
			y = yResolution - 206
		else:
			y = yResolution - 88
		totalWidth = 0
		if (ScoresOpt.isShowResearchIcons()):
			height = ROW_HEIGHT
		else:
			height = ROW_HEIGHT
		
		defaultSpacing = ScoresOpt.getDefaultSpacing()
		spacing = defaultSpacing
		format = re.findall('([0-9]+|[^0-9])', ScoresOpt.getDisplayOrder().replace(' ', '').upper())
		format.reverse()
		for k in format:
			if k[0] in string.digits:
				spacing = int(k)
				continue
			if (not columnsByKey.has_key(k)):
				spacing = defaultSpacing
				continue
			column = columnsByKey[k]
			c = column.id
			if (not self.hasAny[c]):
				spacing = defaultSpacing
				continue
			type = column.type
			if (c == RESEARCH and not ScoresOpt.isShowResearchIcons()):
				# switch SPECIAL research icon to DYNAMIC name
				type = DYNAMIC
			
			if (type == SKIP):
				spacing = defaultSpacing
				continue
			
			elif (type == FIXED):
				width = column.width
				value = column.text
				x -= spacing
				for p in range( self.count ):
					if (self.has[p][c] and self.values[p][c]):
						name = "ScoreText%d-%d" %( p, c )
						widget = self.widgets[p][c]
						if widget is None:
							if (self.values[p][ALIVE]):
								widget = (WidgetTypes.WIDGET_CONTACT_CIV, self.values[p][PLAYER], -1)
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
				for p in range( self.count ):
					if (self.has[p][c]):
						value = self.values[p][c]
						newWidth = interface.determineWidth( value )
						if (newWidth > width):
							width = newWidth
				if (width == 0):
					spacing = defaultSpacing
					continue
				x -= spacing
				for p in range( self.count ):
					if (self.has[p][c]):
						name = "ScoreText%d-%d" %( p, c )
						value = self.values[p][c]
						align = CvUtil.FONT_RIGHT_JUSTIFY
						adjustX = 0
						if (c == NAME or c == SCORE):
							if (c == NAME):
								name = "ScoreText%d" % p
								if (ScoresOpt.isLeftAlignName()):
									align = CvUtil.FONT_LEFT_JUSTIFY
									adjustX = width
						widget = self.widgets[p][c]
						if widget is None:
							if (self.values[p][ALIVE]):
								widget = (WidgetTypes.WIDGET_CONTACT_CIV, self.values[p][PLAYER], -1)
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
					for p in range( self.count ):
						if (self.has[p][c]):
							tech = self.values[p][c]
							name = "ScoreTech%d" % p
							info = gc.getTechInfo(tech)
							screen.addDDSGFC( name, info.getButton(), x - ICON_SIZE, y - p * height - 1, ICON_SIZE, ICON_SIZE, 
											  WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, tech, -1 )
					x -= ICON_SIZE
					totalWidth += ICON_SIZE + spacing
					spacing = defaultSpacing
		
		for p in range( self.count ):
			interface.checkFlashReset( self.values[p][PLAYER] )
		
		if ( interface.getShowInterface() == InterfaceVisibility.INTERFACE_SHOW or interface.isInAdvancedStart()):
			y = yResolution - 186
		else:
			y = yResolution - 68
		screen.setPanelSize( "ScoreBackground", xResolution - 21 - totalWidth, y - (height * self.count) - 4, 
							 totalWidth + 12, (height * self.count) + 8 )
		screen.show( "ScoreBackground" )
