## ScoreCard
## Holds the information used to display the scoreboard.
## Copyright 2007 EmperorFool @ civfanatics.com

from CvPythonExtensions import *
import CvUtil
import BugScoreOptions

# Globals
BugOpt = BugScoreOptions.getOptions()
gc = CyGlobalContext()

# Constants
ICON_SIZE = 24
ROW_HEIGHT = 22
Z_DEPTH = -0.3

# Columns: War Power Tech Espionage Network OpenBorders DefesivePact Religion Attitude
ALIVE = 0
PLAYER = ALIVE + 1
SCORE = PLAYER + 1
NAME = SCORE + 1
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
ordered = [ SCORE, NOT_MET, WAR, ESPIONAGE, POWER, RESEARCH, RESEARCH_TURNS, 
			TRADE, BORDERS, PACT, RELIGION, ATTITUDE, WORST_ENEMY, 
			WAITING, NET_STATS, OOS ]
ordered.reverse()

def _init():
	"""Initializes the strings used to display the scoreboard.
	
	This is called from constructor instead of when the module is loaded
	because GC isn't fully set up otherwise."""
	global bInitDone
	if (bInitDone):
		return
	
	global parts
	game = CyGame()
	
	columns.append(Column('', ALIVE))
	columns.append(Column('', PLAYER))
	columns.append(Column('S', SCORE, DYNAMIC))
	columns.append(Column('C', NAME, DYNAMIC))
	columns.append(Column('?', NOT_MET, FIXED, u"<font=2>?</font>"))
	columns.append(Column('W', WAR, FIXED, u"<font=2>%c</font>" % game.getSymbolID(FontSymbols.OCCUPATION_CHAR)))
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
		self.has = []
		self.values = []
		self.hasAny = [ False ] * NUM_PARTS
		self.currHas = None
		self.currValues = None
		self.count = 0
		
	def addPlayer(self, player):
		self.currHas = [ False ] * NUM_PARTS
		self.currValues = [ None ] * NUM_PARTS
		self.has.append(self.currHas)
		self.values.append(self.currValues)
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
		
	def setName(self, value):
		self._set(NAME, u"<font=2>%s</font>" % value)
		
	def setNotMet(self):
		self._set(NOT_MET)
		
	def setWar(self):
		self._set(WAR)
		
	def setPower(self, value):
		self._set(POWER, u"<font=2>%s</font>" % value)
		
	def setResearch(self, tech, turns):
		if (BugOpt.isShowResearchIcons()):
			self._set(RESEARCH, tech)
		else:
			self._set(RESEARCH, u"<font=2>%s</font>" % gc.getTechInfo(tech).getDescription())
		self._set(RESEARCH_TURNS, u"<font=2> (%d)</font>" % turns)
		
	def setEspionage(self):
		self._set(ESPIONAGE)
		
	def setTrade(self):
		self._set(TRADE)
		
	def setBorders(self):
		self._set(BORDERS)
		
	def setPact(self):
		self._set(PACT)
		
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
		
		
	def _set(self, part, value=True):
		self.hasAny[part] = True
		self.currHas[part] = True
		self.currValues[part] = value
		
		
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
		if (BugOpt.isShowResearchIcons()):
			height = ROW_HEIGHT
		else:
			height = ROW_HEIGHT
		
		format = [ l for l in BugOpt.getDisplayOrder().upper() ]
		format.reverse()
		for k in format:
			if (not columnsByKey.has_key(k)):
				continue
			column = columnsByKey[k]
			c = column.id
			if (not self.hasAny[c]):
				continue
			type = column.type
			if (c == RESEARCH and not BugOpt.isShowResearchIcons()):
				# switch SPECIAL research icon to DYNAMIC name
				type = DYNAMIC
			
			if (type == SKIP):
				continue
			
			elif (type == FIXED):
				width = column.width
				value = column.text
				for p in range( self.count ):
					if (self.has[p][c] and self.values[p][c]):
						name = "ScoreText%d-%d" %( p, c )
						if (self.values[p][ALIVE]):
							widget = WidgetTypes.WIDGET_CONTACT_CIV
							player = self.values[p][PLAYER]
						else:
							widget = WidgetTypes.WIDGET_GENERAL
							player = -1
						screen.setText( name, "Background", value, CvUtil.FONT_RIGHT_JUSTIFY, 
										x, y - p * height, Z_DEPTH, 
										FontTypes.SMALL_FONT, widget, player, -1 )
						screen.show( name )
				x -= width
				totalWidth += width
			
			elif (type == DYNAMIC):
				width = 0
				for p in range( self.count ):
					if (self.has[p][c]):
						value = self.values[p][c]
						newWidth = interface.determineWidth( value )
						if (newWidth > width):
							width = newWidth
				if (width == 0):
					continue
				for p in range( self.count ):
					if (self.has[p][c]):
						name = "ScoreText%d-%d" %( p, c )
						value = self.values[p][c]
						align = CvUtil.FONT_RIGHT_JUSTIFY
						adjustX = 0
						if (c == NAME or c == SCORE):
							if (c == NAME):
								name = "ScoreText%d" % p
								if (BugOpt.isLeftAlignName()):
									align = CvUtil.FONT_LEFT_JUSTIFY
									adjustX = width
						if (self.values[p][ALIVE]):
							widget = WidgetTypes.WIDGET_CONTACT_CIV
							player = self.values[p][PLAYER]
						else:
							widget = WidgetTypes.WIDGET_GENERAL
							player = -1
						screen.setText( name, "Background", value, align, 
										x - adjustX, y - p * height, Z_DEPTH, 
										FontTypes.SMALL_FONT, widget, player, -1 )
						screen.show( name )
				x -= width
				totalWidth += width
			
			else: # SPECIAL
				if (c == RESEARCH):
					for p in range( self.count ):
						if (self.has[p][c]):
							tech = self.values[p][c]
							name = "ScoreTech%d" % p
							info = gc.getTechInfo(tech)
							screen.addDDSGFC( name, info.getButton(), x - ICON_SIZE, y - p * height - 1, ICON_SIZE, ICON_SIZE, 
											  WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, tech, -1 )
					x -= ICON_SIZE
					totalWidth += ICON_SIZE
		
		for p in range( self.count ):
			interface.checkFlashReset( self.values[p][PLAYER] )
		
		if ( interface.getShowInterface() == InterfaceVisibility.INTERFACE_SHOW or interface.isInAdvancedStart()):
			y = yResolution - 186
		else:
			y = yResolution - 68
		screen.setPanelSize( "ScoreBackground", xResolution - 21 - totalWidth, y - (height * self.count) - 4, 
							 totalWidth + 12, (height * self.count) + 8 )
		screen.show( "ScoreBackground" )
