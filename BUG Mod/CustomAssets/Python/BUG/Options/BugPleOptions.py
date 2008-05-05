## BugPleOptions
## Facade for accessing PLE options
## BUG Mod - Copyright 2008

from CvPythonExtensions import *
from BugOptions import OptionsFacade, Option, OptionList

class BugPleOptions(OptionsFacade):

	def __init__(self):
		OptionsFacade.__init__(self)
		self.addOption(Option("PLE_Highlighter",
							  "PlotList", "Move Highlighter", True,
							  "Move Highlighter",
							  "Highlights the moves a unit can make when you hover the mouse over the units icon, while holding the Alt-key.",
							   InterfaceDirtyBits.PlotListButtons_DIRTY_BIT))
		self.addOption(Option("PLE_Mission_Info",
							  "PlotList", "Mission Info", True,
							  "Mission Info",
							  "Shows what the units current mission is.",
							   InterfaceDirtyBits.PlotListButtons_DIRTY_BIT))
		self.addOption(Option("PLE_Health_Bar",
							  "PlotList", "Health Bar", True,
							  "Health Bar",
							  "Show the Health Bar below the unit icon.",
							   InterfaceDirtyBits.PlotListButtons_DIRTY_BIT))
		self.addOption(Option("PLE_Hide_Health_Fighting",
							  "PlotList", "Hide Health bar while fighting", True,
							  "Hide Health Bar during Battle",
							  "Hides the extra Health Bar when your unit is in combat.",
							   InterfaceDirtyBits.PlotListButtons_DIRTY_BIT))
		self.addOption(Option("PLE_Move_Bar",
							  "PlotList", "Move Bar", True,
							  "Show Movement Bar",
							  "s a bar below the units health bar, ing how much movement is left.",
							   InterfaceDirtyBits.PlotListButtons_DIRTY_BIT))
		self.addOption(Option("PLE_Upgrade_Indicator",
							  "PlotList", "Upgrade Indicator", True,
							  "Upgrade Indicator",
							  "s an Orange Up-Arrow when a unit can be upgrade, regardless if you can afford to upgrade.",
							   InterfaceDirtyBits.PlotListButtons_DIRTY_BIT))
		self.addOption(Option("PLE_Promotion_Indicator",
							  "PlotList", "Promotion Indicator", True,
							  "Promotion Indicator",
							  "Highlights a unit that can be promoted with a light blue border.",
							   InterfaceDirtyBits.PlotListButtons_DIRTY_BIT))
		self.addOption(Option("PLE_Wounded_Indicator",
							  "PlotList", "Wounded Indicator", True,
							  "Wounded Indicator",
							  "Changes",
							   InterfaceDirtyBits.PlotListButtons_DIRTY_BIT))
		self.addOption(Option("PLE_Vertical_Spacing",
							  "PlotList", "Vertical Item Spacing", 42,
							  "Vertical Spacing",
							  "Specify the vertical spacing between icons (default value is 42).",
							   InterfaceDirtyBits.PlotListButtons_DIRTY_BIT))
		self.addOption(Option("PLE_Horizontal_Spacing",
							  "PlotList", "Horizontal Item Spacing", 34,
							  "Horizontal Spacing",
							  "Specify the horizontal spacing between icons (default value is 34).",
							   InterfaceDirtyBits.PlotListButtons_DIRTY_BIT))
		self.addOption(Option("PLE_Info_Pane_X",
							  "PlotList", "Info Pane X Position", 5,
							  "Info Pane X",
							  "(default 5)",
							   InterfaceDirtyBits.PlotListButtons_DIRTY_BIT))
		self.addOption(Option("PLE_Info_Pane_Y",
							  "PlotList", "Info Pane Y Position", 160,
							  "Info Pane Y",
							  "(default 160)",
							   InterfaceDirtyBits.PlotListButtons_DIRTY_BIT))
		self.addOption(Option("PLE_Unit_Name_Color",
							  "PlotList", "Unit Name Color", "COLOR_YELLOW",
							  "Unit Name Color",
							  "Default COLOR_YELLOW",
							   InterfaceDirtyBits.PlotListButtons_DIRTY_BIT))
		self.addOption(Option("PLE_Upgrade_Possible_Color",
							  "PlotList", "Upgrade Possible Color", "COLOR_GREEN",
							  "Can Upgrade Unit Color",
							  "Default COLOR_GREEN",
							   InterfaceDirtyBits.PlotListButtons_DIRTY_BIT))
		self.addOption(Option("PLE_Upgrade_Not_Possible_Color",
							  "PlotList", "Upgrade Not Possible Color", "COLOR_RED",
							  "Can't Upgrade Unit Color",
							  "Default COLOR_RED",
							   InterfaceDirtyBits.PlotListButtons_DIRTY_BIT))
		self.addOption(Option("PLE_Promotion_Specialties_Color",
							  "PlotList", "Promotion Specialties Color", "COLOR_LIGHT_GREY",
							  "Promotion Specialties Color",
							  "Default COLOR_LIGHT_GREY",
							   InterfaceDirtyBits.PlotListButtons_DIRTY_BIT))
		self.addOption(Option("PLE_Unit_Type_Specialties_Color",
							  "PlotList", "Unit Type Specialties Color", "COLOR_WHITE",
							  "Unit Type Specialties Color",
							  "Default COLOR_WHITE",
							   InterfaceDirtyBits.PlotListButtons_DIRTY_BIT))
		self.addOption(Option("PLE_Healthy_Color",
							  "PlotList", "Healthy Color", "COLOR_GREEN",
							  "Healthy Color",
							  "Default COLOR_GREEN",
							   InterfaceDirtyBits.PlotListButtons_DIRTY_BIT))
		self.addOption(Option("PLE_Wounded_Color",
							  "PlotList", "Wounded Color", "COLOR_RED",
							  "Wounded Color",
							  "Default COLOR_RED",
							   InterfaceDirtyBits.PlotListButtons_DIRTY_BIT))
		self.addOption(Option("PLE_Full_Movement_Color",
							  "PlotList", "Full Movement Color", "COLOR_BLUE",
							  "Full Movement Color",
							  "Default COLOR_BLUE",
							   InterfaceDirtyBits.PlotListButtons_DIRTY_BIT))
		self.addOption(Option("PLE_Has_Moved_Color",
							  "PlotList", "Has Moved Color", "COLOR_YELLOW",
							  "Has Moved Color",
							  "Default COLOR_YELLOW",
							   InterfaceDirtyBits.PlotListButtons_DIRTY_BIT))
		self.addOption(Option("PLE_No_Movement_Color",
							  "PlotList", "No Movement Color", "COLOR_BLACK",
							  "No Movement Color",
							  "Default COLOR_BLACK",
							   InterfaceDirtyBits.PlotListButtons_DIRTY_BIT))
		self.addOption(Option("PLE_MH_Color_Impassable_Terrain",
							  "PlotList", "Color Impassable Terrain", "COLOR_CLEAR",
							  "Color Impassable Terrain",
							  "Default COLOR_CLEAR",
							   InterfaceDirtyBits.PlotListButtons_DIRTY_BIT))
		self.addOption(Option("PLE_MH_Color_Passable_Terrain",
							  "PlotList", "Color Passable Terrain", "COLOR_WHITE",
							  "Color Passable Terrain",
							  "Default COLOR_WHITE",
							   InterfaceDirtyBits.PlotListButtons_DIRTY_BIT))
		self.addOption(Option("PLE_MH_Color_Passable_Neutral_Territory",
							  "PlotList", "Color Passable Neutral Territory", "COLOR_PLAYER_DARK_YELLOW",
							  "Color Passable Neutral Territory",
							  "Default COLOR_PLAYER_DARK_YELLOW",
							   InterfaceDirtyBits.PlotListButtons_DIRTY_BIT))
		self.addOption(Option("PLE_MH_Color_Passable_Enemy_Territory",
							  "PlotList", "Color Passable Enemy Territory", "COLOR_PLAYER_DARK_RED",
							  "Color Passable Enemy Territory",
							  "Default COLOR_PLAYER_DARK_RED",
							   InterfaceDirtyBits.PlotListButtons_DIRTY_BIT))
		self.addOption(Option("PLE_MH_Color_Passable_Barbarian_Territory",
							  "PlotList", "Color Passable Barbarian Territory", "COLOR_PLAYER_DARK_CYAN",
							  "Color Passable Barbarian Territory",
							  "Default COLOR_PLAYER_DARK_CYAN",
							   InterfaceDirtyBits.PlotListButtons_DIRTY_BIT))
		self.addOption(Option("PLE_MH_Color_Neutral_Unit",
							  "PlotList", "Color Neutral Unit", "COLOR_YELLOW",
							  "Color Neutral Unit",
							  "Default COLOR_YELLOW",
							   InterfaceDirtyBits.PlotListButtons_DIRTY_BIT))
		self.addOption(Option("PLE_MH_Color_Enemy_Unit",
							  "PlotList", "Color Enemy Unit", "COLOR_RED",
							  "Color Enemy Unit",
							  "Default COLOR_RED",
							   InterfaceDirtyBits.PlotListButtons_DIRTY_BIT))
		self.addOption(Option("PLE_MH_Color_Barbarian_Unit",
							  "PlotList", "Color Barbarian Unit", "COLOR_CYAN",
							  "Color Barbarian Unit",
							  "Default COLOR_CYAN",
							   InterfaceDirtyBits.PlotListButtons_DIRTY_BIT))

	

	def isShowMoveHighlighter(self):
		return self.getBoolean('PLE_Highlighter')
	
	def isShowMissionInfo(self):
		return self.getBoolean('PLE_Mission_Info')
	def isShowHealthBar(self):
		return self.getBoolean('PLE_Health_Bar')
	def isHideHealthFighting(self):
		return self.getBoolean('PLE_Hide_Health_Fighting')
	def isShowMoveBar(self):
		return self.getBoolean('PLE_Move_Bar')
	def isShowUpgradeIndicator(self):
		return self.getBoolean('PLE_Upgrade_Indicator')
	def isShowPromotionIndicator(self):
		return self.getBoolean('PLE_Promotion_Indicator')
	def isShowWoundedIndicator(self):
		return self.getBoolean('PLE_Wounded_Indicator')
	
	def getVerticalSpacing(self):
		return self.getInt('PLE_Vertical_Spacing')
	def getHoriztonalSpacing(self):
		return self.getInt('PLE_Horiztonal_Spacing')
	
	def getInfoPaneX(self):
		return self.getInt('PLE_Info_Pane_X')
	def getInfoPaneY(self):
		return self.getInt('PLE_Info_Pane_Y')
	
	def getUnitNameColor(self):
		return self.getString('PLE_Unit_Name_Color')
	def getUpgradePossibleColor(self):
		return self.getString('PLE_Upgrade_Possible_Color')
	def getUpgradeNotPossibleColor(self):
		return self.getString('PLE_Upgrade_Not_Possible_Color')
	def getPromotionSpecialtiesColor(self):
		return self.getString('PLE_Promotion_Specialties_Color')
	def getUnitTypeSpecialtiesColor(self):
		return self.getString('PLE_Unit_Type_Specialties_Color')
	
	def getHealthyColor(self):
		return self.getString('PLE_Healthy_Color')
	def getWoundedColor(self):
		return self.getString('PLE_Wounded_Color')
	def getFullMovementColor(self):
		return self.getString('PLE_Full_Movement_Color')
	def getHasMovedColor(self):
		return self.getString('PLE_Has_Moved_Color')
	def getNoMovementColor(self):
		return self.getString('PLE_No_Movement_Color')
	
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

