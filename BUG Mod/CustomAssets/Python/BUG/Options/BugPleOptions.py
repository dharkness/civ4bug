## BugPleOptions
## Facade for accessing PLE options
## BUG Mod - Copyright 2008

from CvPythonExtensions import *
from BugOptions import OptionsFacade, Option, OptionList

class BugPleOptions(OptionsFacade):

	def __init__(self):
		OptionsFacade.__init__(self)
		self.addOption(Option("PLE_Enabled",
							  "PlotList", "Enabled", True,
							  "Enabled",
							  "Enables the Plot List Enhancements mod and the rest of the options on this tab.",
							  InterfaceDirtyBits.PlotListButtons_DIRTY_BIT))
		
		# Modes and Filters
		self.addOption(Option("PLE_Show_Buttons",
							  "PlotList", "Show Buttons", True,
							  "Show Buttons",
							  "When checked, the buttons for changing the view, grouping and filter modes are displayed above the action buttons.",
							  InterfaceDirtyBits.PlotListButtons_DIRTY_BIT))
		self.addOption(OptionList("PLE_Default_View_Mode",
							 	 "PlotList", "Default View Mode", 1,
								  "Default View",
								  "Sets the view mode used when you start Civ IV.",
								  ['Single Row', 'Multiple Rows', 'Vertical Groups', 'Horizontal Groups'], None,
								  None))
		self.addOption(OptionList("PLE_Default_Group_Mode",
							 	 "PlotList", "Default Grouping Mode", 0,
								  "Default Grouping",
								  "Sets the grouping mode used when you start Civ IV.",
								  ['Unit Type', 'Selection Group'], None,
								  None))
		self.addOption(OptionList("PLE_Filter_Behavior",
							 	 "PlotList", "Filter Behavior", 1,
								  "Filter Behavior",
								  "Sets the filter behavior.",
								  ['PLE', 'BUG'], None,
								  InterfaceDirtyBits.PlotListButtons_DIRTY_BIT))
		
		# Health Bar
		self.addOption(Option("PLE_Health_Bar",
							  "PlotList", "Health Bar", True,
							  "Health Bar",
							  "Shows a bar above the unit icon displaying the unit's health and damage.",
							  InterfaceDirtyBits.PlotListButtons_DIRTY_BIT))
		self.addOption(Option("PLE_Hide_Health_Fighting",
							  "PlotList", "Hide Health Bar While Fighting", True,
							  "Hide During Combat",
							  "Hides the Health Bar when a unit is in combat.",
							  None))
		self.addOption(Option("PLE_Healthy_Color",
							  "PlotList", "Healthy Color", "COLOR_GREEN",
							  "Healthy",
							  "The color to use for the healthy portion of the bar.",
							  InterfaceDirtyBits.PlotListButtons_DIRTY_BIT))
		self.addOption(Option("PLE_Wounded_Color",
							  "PlotList", "Wounded Color", "COLOR_RED",
							  "Wounded",
							  "The color to use for the wounded portion of the bar.",
							  InterfaceDirtyBits.PlotListButtons_DIRTY_BIT))
		
		# Move Bar
		self.addOption(Option("PLE_Move_Bar",
							  "PlotList", "Move Bar", True,
							  "Movement Bar",
							  "Shows a bar above the unit icon displaying the unit's movement points.",
							  InterfaceDirtyBits.PlotListButtons_DIRTY_BIT))
		self.addOption(Option("PLE_Full_Movement_Color",
							  "PlotList", "Full Movement Color", "COLOR_BLUE",
							  "Available",
							  "The color to use for the available movement portion of the bar.",
							  InterfaceDirtyBits.PlotListButtons_DIRTY_BIT))
		self.addOption(Option("PLE_Has_Moved_Color",
							  "PlotList", "Has Moved Color", "COLOR_YELLOW",
							  "Used",
							  "The color to use for the used movement portion of the bar.",
							  InterfaceDirtyBits.PlotListButtons_DIRTY_BIT))
		self.addOption(Option("PLE_No_Movement_Color",
							  "PlotList", "No Movement Color", "COLOR_BLACK",
							  "Cannot Move",
							  "The color to use for the whole bar when the unit cannot move anymore.",
							  InterfaceDirtyBits.PlotListButtons_DIRTY_BIT))
		
		# Indicators
		self.addOption(Option("PLE_Wounded_Indicator",
							  "PlotList", "Wounded Indicator", True,
							  "Wounded Dot",
							  "Darkens the dot in the upper-left corner of units that are wounded.",
							  InterfaceDirtyBits.PlotListButtons_DIRTY_BIT))
		self.addOption(Option("PLE_Lead_By_GG_Indicator",
							  "PlotList", "Great General Indicator", True,
							  "Great General",
							  "Places a star on units that are lead by a Great General.",
							  InterfaceDirtyBits.PlotListButtons_DIRTY_BIT))
		self.addOption(Option("PLE_Promotion_Indicator",
							  "PlotList", "Promotion Indicator", True,
							  "Promotion Available",
							  "Places a light blue border around units that can be promoted.",
							  InterfaceDirtyBits.PlotListButtons_DIRTY_BIT))
		self.addOption(Option("PLE_Upgrade_Indicator",
							  "PlotList", "Upgrade Indicator", True,
							  "Upgrade Available",
							  "Places an orange up arrow on the lower-right corner of units that can be upgraded, ignoring cost.",
							  InterfaceDirtyBits.PlotListButtons_DIRTY_BIT))
		self.addOption(Option("PLE_Mission_Info",
							  "PlotList", "Mission Info", True,
							  "Mission Tag",
							  "Places a tag below units showing their current mission (action).",
							  InterfaceDirtyBits.PlotListButtons_DIRTY_BIT))
		
		# Button Spacing
		self.addOption(Option("PLE_Horizontal_Spacing",
							  "PlotList", "Horizontal Item Spacing", 34,
							  "Horizontal Spacing",
							  "Specifies the horizontal spacing between icons (default:  34).",
							  InterfaceDirtyBits.PlotListButtons_DIRTY_BIT))
		self.addOption(Option("PLE_Vertical_Spacing",
							  "PlotList", "Vertical Item Spacing", 42,
							  "Vertical Spacing",
							  "Specifies the vertical spacing between icons (default:  42).",
							  InterfaceDirtyBits.PlotListButtons_DIRTY_BIT))
		
		# Unit Info Hover Pane
		self.addOption(Option("PLE_Info_Pane",
							  "PlotList", "Unit Info Hover", True,
							  "Unit Info Tooltip",
							  "Replaces the default Unit Info displayed when you hover over a unit.",
							  InterfaceDirtyBits.PlotListButtons_DIRTY_BIT))
		self.addOption(Option("PLE_Info_Pane_X",
							  "PlotList", "Info Pane X Position", 5,
							  "Horizontal Position",
							  "Specifies the horizontal position of the Unit Info hover pane (default:  5).",
							  None))
		self.addOption(Option("PLE_Info_Pane_Y",
							  "PlotList", "Info Pane Y Position", 160,
							  "Vertical Position",
							  "Specifies the vertical position of the Unit Info hover pane (default:  160).",
							  None))
		self.addOption(Option("PLE_Info_Pane_Width",
							  "PlotList", "Info Pane X Size", 5,
							  "Width",
							  "Specifies the width of the Unit Info hover pane (default:  290).",
							  None))
		self.addOption(Option("PLE_Info_Pane_Standard_Line_Height",
							  "PlotList", "Pixel Per Line Type 1", 24,
							  "Standard Line Height",
							  "Specifies the height of a standard line of text (default:  24).",
							  None))
		self.addOption(Option("PLE_Info_Pane_Bulleted_Line_Height",
							  "PlotList", "Pixel Per Line Type 2", 19,
							  "Bulleted Line Height",
							  "Specifies the height of a bulleted line of text (default:  19).",
							  None))
		
		self.addOption(Option("PLE_Unit_Name_Color",
							  "PlotList", "Unit Name Color", "COLOR_YELLOW",
							  "Unit Name",
							  "Default COLOR_YELLOW",
							  None))
		self.addOption(Option("PLE_Upgrade_Possible_Color",
							  "PlotList", "Upgrade Possible Color", "COLOR_GREEN",
							  "Can Upgrade",
							  "Default COLOR_GREEN",
							  None))
		self.addOption(Option("PLE_Upgrade_Not_Possible_Color",
							  "PlotList", "Upgrade Not Possible Color", "COLOR_RED",
							  "Can't Upgrade",
							  "Default COLOR_RED",
							  None))
		self.addOption(Option("PLE_Unit_Type_Specialties_Color",
							  "PlotList", "Unit Type Specialties Color", "COLOR_WHITE",
							  "Unit Type Specialties",
							  "Default COLOR_WHITE",
							  None))
		self.addOption(Option("PLE_Promotion_Specialties_Color",
							  "PlotList", "Promotion Specialties Color", "COLOR_LIGHT_GREY",
							  "Promotion Specialties",
							  "Default COLOR_LIGHT_GREY",
							  None))
		
		# Move Highlighter
		self.addOption(Option("PLE_Move_Highlighter",
							  "PlotList", "Move Highlighter", True,
							  "Move Highlighter",
							  "Highlights the moves a unit can make when you hover the mouse over the units icon while holding [ALT].",
							  None))
		
		self.addOption(Option("PLE_MH_Color_Impassable_Terrain",
							  "PlotList", "Color Impassable Terrain", "COLOR_CLEAR",
							  "Impassable Terrain",
							  "Default COLOR_CLEAR",
							  None))
		self.addOption(Option("PLE_MH_Color_Passable_Terrain",
							  "PlotList", "Color Passable Terrain", "COLOR_WHITE",
							  "Passable Terrain",
							  "Default COLOR_WHITE",
							  None))
		self.addOption(Option("PLE_MH_Color_Passable_Neutral_Territory",
							  "PlotList", "Color Passable Neutral Territory", "COLOR_PLAYER_DARK_YELLOW",
							  "Passable Neutral Territory",
							  "Default COLOR_PLAYER_DARK_YELLOW",
							  None))
		self.addOption(Option("PLE_MH_Color_Passable_Enemy_Territory",
							  "PlotList", "Color Passable Enemy Territory", "COLOR_PLAYER_DARK_RED",
							  "Passable Enemy Territory",
							  "Default COLOR_PLAYER_DARK_RED",
							  None))
		self.addOption(Option("PLE_MH_Color_Passable_Barbarian_Territory",
							  "PlotList", "Color Passable Barbarian Territory", "COLOR_PLAYER_DARK_CYAN",
							  "Passable Barbarian Territory",
							  "Default COLOR_PLAYER_DARK_CYAN",
							  None))
		self.addOption(Option("PLE_MH_Color_Neutral_Unit",
							  "PlotList", "Color Neutral Unit", "COLOR_YELLOW",
							  "Neutral Unit",
							  "Default COLOR_YELLOW",
							  None))
		self.addOption(Option("PLE_MH_Color_Enemy_Unit",
							  "PlotList", "Color Enemy Unit", "COLOR_RED",
							  "Enemy Unit",
							  "Default COLOR_RED",
							  None))
		self.addOption(Option("PLE_MH_Color_Barbarian_Unit",
							  "PlotList", "Color Barbarian Unit", "COLOR_CYAN",
							  "Barbarian Unit",
							  "Default COLOR_CYAN",
							  None))


	# Master Switch
	
	def isEnabled(self):
		return self.getBoolean('PLE_Enabled')  # not yet
	
	# Modes and Filters
	
	def isShowButtons(self):
		return self.getBoolean('PLE_Show_Buttons')
	def getDefaultViewMode(self):
		return self.getInt('PLE_Default_View_Mode')
	def getDefaultGroupMode(self):
		return self.getInt('PLE_Default_Group_Mode')
	def getFilterBehavior(self):
		return self.getInt('PLE_Filter_Behavior')
	def isPleFilterBehavior(self):
		return self.getFilterBehavior() == 0
	def isBugFilterBehavior(self):
		return self.getFilterBehavior() == 1
	
	# Health Bar
	
	def isShowHealthBar(self):
		return self.getBoolean('PLE_Health_Bar')
	def isHideHealthFighting(self):
		return self.getBoolean('PLE_Hide_Health_Fighting')
	def getHealthyColor(self):
		return self.getString('PLE_Healthy_Color')
	def getWoundedColor(self):
		return self.getString('PLE_Wounded_Color')
	
	# Move Bar
	
	def isShowMoveBar(self):
		return self.getBoolean('PLE_Move_Bar')
	def getFullMovementColor(self):
		return self.getString('PLE_Full_Movement_Color')
	def getHasMovedColor(self):
		return self.getString('PLE_Has_Moved_Color')
	def getNoMovementColor(self):
		return self.getString('PLE_No_Movement_Color')  # not yet
	
	# Indicators
	
	def isShowWoundedIndicator(self):
		return self.getBoolean('PLE_Wounded_Indicator')
	def isShowGreatGeneralIndicator(self):
		return self.getBoolean('PLE_Lead_By_GG_Indicator')
	def isShowPromotionIndicator(self):
		return self.getBoolean('PLE_Promotion_Indicator')
	def isShowUpgradeIndicator(self):
		return self.getBoolean('PLE_Upgrade_Indicator')
	def isShowMissionInfo(self):
		return self.getBoolean('PLE_Mission_Info')
	
	# Button Spacing
	
	def getHoriztonalSpacing(self):
		return self.getInt('PLE_Horizontal_Spacing')
	def getVerticalSpacing(self):
		return self.getInt('PLE_Vertical_Spacing')
	
	# Unit Info Hover Pane
	
	def isShowInfoPane(self):
		return self.getBoolean('PLE_Info_Pane')  # not yet
	def getInfoPaneX(self):
		return self.getInt('PLE_Info_Pane_X')
	def getInfoPaneY(self):
		return self.getInt('PLE_Info_Pane_Y')
	def getInfoPaneWidth(self):
		return self.getInt('PLE_Info_Pane_Width')
	def getInfoPaneStandardLineHeight(self):
		return self.getInt('PLE_Info_Pane_Standard_Line_Height')
	def getInfoPaneBulletedLineHeight(self):
		return self.getInt('PLE_Info_Pane_Bulleted_Line_Height')
	
	def getUnitNameColor(self):
		return self.getString('PLE_Unit_Name_Color')
	def getUpgradePossibleColor(self):
		return self.getString('PLE_Upgrade_Possible_Color')
	def getUpgradeNotPossibleColor(self):
		return self.getString('PLE_Upgrade_Not_Possible_Color')
	def getUnitTypeSpecialtiesColor(self):
		return self.getString('PLE_Unit_Type_Specialties_Color')
	def getPromotionSpecialtiesColor(self):
		return self.getString('PLE_Promotion_Specialties_Color')
	
	# Move Highlighter
	
	def isShowMoveHighlighter(self):
		return self.getBoolean('PLE_Move_Highlighter')
	
	def getImpassableTerrainColor(self):
		return self.getString('PLE_MH_Color_Impassable_Terrain')
	def getPassableTerrainColor(self):
		return self.getString('PLE_MH_Color_Passable_Terrain')
	def getNeutralTerritoryColor(self):
		return self.getString('PLE_MH_Color_Passable_Neutral_Territory')
	def getEnemyTerritoryColor(self):
		return self.getString('PLE_MH_Color_Passable_Enemy_Territory')
	def getBarbarianTerritoryColor(self):
		return self.getString('PLE_MH_Color_Passable_Barbarian_Territory')
	def getNeutralUnitColor(self):
		return self.getString('PLE_MH_Color_Neutral_Unit')
	def getEnemyUnitColor(self):
		return self.getString('PLE_MH_Color_Enemy_Unit')
	def getBarbarianUnitColor(self):
		return self.getString('PLE_MH_Color_Barbarian_Unit')

# The singleton BugPleOptions object

__g_options = BugPleOptions()
def getOptions():
	return __g_options

