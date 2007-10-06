# Sid Meier's Civilization 4
# Copyright Firaxis Games 2005

#
# Sevopedia 2.3
#   sevotastic.blogspot.com
#   sevotastic@yahoo.com
#
# additional work by Gaurav, Progor, Ket, Vovan, Fitchn, LunarMongoose
# see ReadMe for details
#

from CvPythonExtensions import *
import string

import CvUtil
import ScreenInput
import SevoScreenEnums

import CvPediaScreen
import SevoPediaTech
import SevoPediaUnit
import SevoPediaBuilding
import SevoPediaPromotion
import SevoPediaUnitChart
import SevoPediaBonus
import SevoPediaTerrain
import SevoPediaFeature
import SevoPediaImprovement
import SevoPediaCivic
import SevoPediaCivilization
import SevoPediaLeader
import SevoPediaSpecialist
import SevoPediaHistory
import SevoPediaProject
import SevoPediaReligion
import SevoPediaCorporation

import UnitUpgradesGraph

import BugScreensOptions
BugScreens = BugScreensOptions.getOptions()

gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

class SevoPediaMain(CvPediaScreen.CvPediaScreen):

	def __init__(self):
		self.PEDIA_MAIN_SCREEN	= "PediaMainScreen"
		self.INTERFACE_ART_INFO	= "SCREEN_BG_OPAQUE"

		self.WIDGET_ID		= "PediaMainWidget"
		self.BACKGROUND_ID	= "PediaMainBackground"
		self.TOP_PANEL_ID	= "PediaMainTopPanel"
		self.BOT_PANEL_ID	= "PediaMainBottomPanel"
		self.HEAD_ID		= "PediaMainHeader"
		self.BACK_ID		= "PediaMainBack"
		self.NEXT_ID		= "PediaMainForward"
		self.EXIT_ID		= "PediaMainExit"
		self.CATEGORY_LIST_ID	= "PediaMainCategoryList"
		self.ITEM_LIST_ID	= "PediaMainItemList"
		self.UPGRADES_GRAPH_ID	= "PediaMainUpgradesGraph"

		self.X_SCREEN = 500
		self.Y_SCREEN = 396
		self.W_SCREEN = 1024
		self.H_SCREEN = 768

		self.H_PANEL = 55
		self.BUTTON_SIZE = 64
		self.BUTTON_COLUMNS = 9
		self.ITEMS_MARGIN = 18
		self.ITEMS_SEPARATION = 2

		self.X_TOP_PANEL = 0
		self.Y_TOP_PANEL = 0
		self.W_TOP_PANEL = self.W_SCREEN
		self.H_TOP_PANEL = self.H_PANEL

		self.X_BOT_PANEL = 0
		self.Y_BOT_PANEL = self.H_SCREEN - self.H_PANEL
		self.W_BOT_PANEL = self.W_SCREEN
		self.H_BOT_PANEL = self.H_PANEL

		self.X_CATEGORIES = 0
		self.Y_CATEGORIES = (self.Y_TOP_PANEL + self.H_TOP_PANEL) - 4
		self.W_CATEGORIES = 175
		self.H_CATEGORIES = (self.Y_BOT_PANEL + 3) - self.Y_CATEGORIES

		self.X_ITEMS = self.X_CATEGORIES + self.W_CATEGORIES + 2
		self.Y_ITEMS = self.Y_CATEGORIES
		self.W_ITEMS = 210
		self.H_ITEMS = self.H_CATEGORIES

		self.X_PEDIA_PAGE = self.X_ITEMS + self.W_ITEMS + 18
		self.Y_PEDIA_PAGE = self.Y_ITEMS + 13
		self.R_PEDIA_PAGE = self.W_SCREEN - 20
		self.B_PEDIA_PAGE = self.Y_ITEMS + self.H_ITEMS - 16
		self.W_PEDIA_PAGE = self.R_PEDIA_PAGE - self.X_PEDIA_PAGE
		self.H_PEDIA_PAGE = self.B_PEDIA_PAGE - self.Y_PEDIA_PAGE

		self.X_TITLE = self.X_SCREEN
		self.Y_TITLE = 8
		self.X_BACK = 75
		self.Y_BACK = 730
		self.X_NEXT = 210
		self.Y_NEXT = 730
		self.X_EXIT = 994
		self.Y_EXIT = 730

		self.iActivePlayer = -1
		self.nWidgetCount = 0

		self.categoryList = []
		self.categoryGraphics = []
		self.iCategory = -1
		self.pediaHistory = []
		self.pediaFuture = []

		self.mapListGenerators = {
			SevoScreenEnums.PEDIA_TECHS		: self.placeTechs,
			SevoScreenEnums.PEDIA_UNITS		: self.placeUnits,
			SevoScreenEnums.PEDIA_UNIT_UPGRADES	: self.placeUnitUpgrades,
			SevoScreenEnums.PEDIA_UNIT_CATEGORIES	: self.placeUnitCategories,
			SevoScreenEnums.PEDIA_PROMOTIONS		: self.placePromotions,
			SevoScreenEnums.PEDIA_PROMOTION_TREE	: self.placePromotionTree,
			SevoScreenEnums.PEDIA_BUILDINGS		: self.placeBuildings,
			SevoScreenEnums.PEDIA_NATIONAL_WONDERS	: self.placeNationalWonders,
			SevoScreenEnums.PEDIA_GREAT_WONDERS	: self.placeGreatWonders,
			SevoScreenEnums.PEDIA_PROJECTS		: self.placeProjects,
			SevoScreenEnums.PEDIA_SPECIALISTS		: self.placeSpecialists,
			SevoScreenEnums.PEDIA_TERRAINS		: self.placeTerrains,
			SevoScreenEnums.PEDIA_FEATURES		: self.placeFeatures,
			SevoScreenEnums.PEDIA_BONUSES		: self.placeBonuses,
			SevoScreenEnums.PEDIA_IMPROVEMENTS	: self.placeImprovements,
			SevoScreenEnums.PEDIA_CIVS		: self.placeCivs,
			SevoScreenEnums.PEDIA_LEADERS		: self.placeLeaders,
			SevoScreenEnums.PEDIA_CIVICS		: self.placeCivics,
			SevoScreenEnums.PEDIA_RELIGIONS		: self.placeReligions,
			SevoScreenEnums.PEDIA_CORPORATIONS	: self.placeCorporations,
			SevoScreenEnums.PEDIA_CONCEPTS		: self.placeConcepts,
			SevoScreenEnums.PEDIA_BTS_CONCEPTS	: self.placeBTSConcepts,
			SevoScreenEnums.PEDIA_HINTS		: self.placeHints,
			}

		self.mapScreenFunctions = {
			SevoScreenEnums.PEDIA_TECHS		: SevoPediaTech.SevoPediaTech(self),
			SevoScreenEnums.PEDIA_UNITS		: SevoPediaUnit.SevoPediaUnit(self),
			SevoScreenEnums.PEDIA_UNIT_CATEGORIES	: SevoPediaUnitChart.SevoPediaUnitChart(self),
			SevoScreenEnums.PEDIA_PROMOTIONS		: SevoPediaPromotion.SevoPediaPromotion(self),
			SevoScreenEnums.PEDIA_BUILDINGS		: SevoPediaBuilding.SevoPediaBuilding(self),
			SevoScreenEnums.PEDIA_NATIONAL_WONDERS	: SevoPediaBuilding.SevoPediaBuilding(self),
			SevoScreenEnums.PEDIA_GREAT_WONDERS	: SevoPediaBuilding.SevoPediaBuilding(self),
			SevoScreenEnums.PEDIA_PROJECTS		: SevoPediaProject.SevoPediaProject(self),
			SevoScreenEnums.PEDIA_SPECIALISTS		: SevoPediaSpecialist.SevoPediaSpecialist(self),
			SevoScreenEnums.PEDIA_TERRAINS		: SevoPediaTerrain.SevoPediaTerrain(self),
			SevoScreenEnums.PEDIA_FEATURES		: SevoPediaFeature.SevoPediaFeature(self),
			SevoScreenEnums.PEDIA_BONUSES		: SevoPediaBonus.SevoPediaBonus(self),
			SevoScreenEnums.PEDIA_IMPROVEMENTS	: SevoPediaImprovement.SevoPediaImprovement(self),
			SevoScreenEnums.PEDIA_CIVS		: SevoPediaCivilization.SevoPediaCivilization(self),
			SevoScreenEnums.PEDIA_LEADERS		: SevoPediaLeader.SevoPediaLeader(self),
			SevoScreenEnums.PEDIA_CIVICS		: SevoPediaCivic.SevoPediaCivic(self),
			SevoScreenEnums.PEDIA_RELIGIONS		: SevoPediaReligion.SevoPediaReligion(self),
			SevoScreenEnums.PEDIA_CORPORATIONS	: SevoPediaCorporation.SevoPediaCorporation(self),
			SevoScreenEnums.PEDIA_CONCEPTS		: SevoPediaHistory.SevoPediaHistory(self),
			SevoScreenEnums.PEDIA_BTS_CONCEPTS	: SevoPediaHistory.SevoPediaHistory(self),
			}

		self.pediaBuilding	= SevoPediaBuilding.SevoPediaBuilding(self)
		self.pediaLeader	= SevoPediaLeader.SevoPediaLeader(self)



	def getScreen(self):
		return CyGInterfaceScreen(self.PEDIA_MAIN_SCREEN, SevoScreenEnums.PEDIA_MAIN)



	def pediaShow(self):
		self.iActivePlayer = gc.getGame().getActivePlayer()
		self.iCategory = -1
		if (not self.pediaHistory):
			self.pediaHistory.append((SevoScreenEnums.PEDIA_MAIN, SevoScreenEnums.PEDIA_TECHS))
		current = self.pediaHistory.pop()
		self.pediaFuture = []
		self.pediaHistory = []
		self.pediaJump(current[0], current[1], False, True)



	def pediaJump(self, iCategory, iItem, bRemoveFwdList, bIsLink):
		if (self.pediaHistory == [] or iCategory != SevoScreenEnums.PEDIA_MAIN or iItem == SevoScreenEnums.PEDIA_UNIT_UPGRADES or iItem == SevoScreenEnums.PEDIA_PROMOTION_TREE or iItem == SevoScreenEnums.PEDIA_HINTS):
			self.pediaHistory.append((iCategory, iItem))
		if (bRemoveFwdList):
			self.pediaFuture = []

		screen = self.getScreen()
		if not screen.isActive():
			self.deleteAllWidgets()
			self.setPediaCommonWidgets()
			self.placeCategories()

		if (iCategory == SevoScreenEnums.PEDIA_MAIN):
			screen.setSelectedListBoxStringGFC(self.CATEGORY_LIST_ID, iItem - (SevoScreenEnums.PEDIA_MAIN + 1))
			self.deleteAllWidgets()
			self.mapListGenerators.get(iItem)()
			self.iCategory = iItem
			return

		if (iCategory == SevoScreenEnums.PEDIA_BUILDINGS):
			iCategory = iCategory + self.pediaBuilding.getBuildingType(iItem)

		if (iCategory != self.iCategory):
			screen.setSelectedListBoxStringGFC(self.CATEGORY_LIST_ID, iCategory - (SevoScreenEnums.PEDIA_MAIN + 1))

		if (iCategory != self.iCategory or bIsLink):
			self.mapListGenerators.get(iCategory)()

		if (iCategory != SevoScreenEnums.PEDIA_UNIT_UPGRADES and iCategory != SevoScreenEnums.PEDIA_PROMOTION_TREE and iCategory != SevoScreenEnums.PEDIA_HINTS):
			screen.enableSelect(self.ITEM_LIST_ID, True)
			if (iCategory != self.iCategory or bIsLink):
				i = 0
				for item in self.list:
					if (item[1] == iItem):
						screen.selectRow(self.ITEM_LIST_ID, i, True)
					i += 1

		if (iCategory != self.iCategory):
			self.iCategory = iCategory

		self.deleteAllWidgets()
		func = self.mapScreenFunctions.get(iCategory)
		func.interfaceScreen(iItem)



	def setPediaCommonWidgets(self):
		self.HEAD_TEXT = u"<font=4b>" + localText.getText("TXT_KEY_WIDGET_HELP",          ())         + u"</font>"
		self.BACK_TEXT = u"<font=4>"  + localText.getText("TXT_KEY_PEDIA_SCREEN_BACK",    ()).upper() + u"</font>"
		self.NEXT_TEXT = u"<font=4>"  + localText.getText("TXT_KEY_PEDIA_SCREEN_FORWARD", ()).upper() + u"</font>"
		self.EXIT_TEXT = u"<font=4>"  + localText.getText("TXT_KEY_PEDIA_SCREEN_EXIT",    ()).upper() + u"</font>"

		self.szCategoryTechs		= localText.getText("TXT_KEY_PEDIA_CATEGORY_TECH", ())
		self.szCategoryUnits		= localText.getText("TXT_KEY_PEDIA_CATEGORY_UNIT", ())
		self.szCategoryUnitUpgrades	= localText.getText("TXT_KEY_PEDIA_CATEGORY_UNIT_UPGRADES", ())
		self.szCategoryUnitCategories	= localText.getText("TXT_KEY_PEDIA_CATEGORY_UNIT_COMBAT", ())
		self.szCategoryPromotions	= localText.getText("TXT_KEY_PEDIA_CATEGORY_PROMOTION", ())
		self.szCategoryPromotionTree	= localText.getText("TXT_KEY_PEDIA_CATEGORY_PROMOTION_TREE", ())
		self.szCategoryBuildings	= localText.getText("TXT_KEY_PEDIA_CATEGORY_BUILDING", ())
		self.szCategoryNationalWonders	= localText.getText("TXT_KEY_PEDIA_CATEGORY_NATIONAL_WONDERS", ())
		self.szCategoryGreatWonders	= localText.getText("TXT_KEY_PEDIA_CATEGORY_GREAT_WONDERS", ())
		self.szCategoryProjects		= localText.getText("TXT_KEY_PEDIA_CATEGORY_PROJECT", ())
		self.szCategorySpecialists	= localText.getText("TXT_KEY_PEDIA_CATEGORY_SPECIALIST", ())
		self.szCategoryTerrains		= localText.getText("TXT_KEY_PEDIA_CATEGORY_TERRAIN", ())
		self.szCategoryFeatures		= localText.getText("TXT_KEY_PEDIA_CATEGORY_FEATURE", ())
		self.szCategoryBonuses		= localText.getText("TXT_KEY_PEDIA_CATEGORY_BONUS", ())
		self.szCategoryImprovements	= localText.getText("TXT_KEY_PEDIA_CATEGORY_IMPROVEMENT", ())
		self.szCategoryCivs		= localText.getText("TXT_KEY_PEDIA_CATEGORY_CIV", ())
		self.szCategoryLeaders		= localText.getText("TXT_KEY_PEDIA_CATEGORY_LEADER", ())
		self.szCategoryCivics		= localText.getText("TXT_KEY_PEDIA_CATEGORY_CIVIC", ())
		self.szCategoryReligions	= localText.getText("TXT_KEY_PEDIA_CATEGORY_RELIGION", ())
		self.szCategoryCorporations	= localText.getText("TXT_KEY_CONCEPT_CORPORATIONS", ())
		self.szCategoryConcepts		= localText.getText("TXT_KEY_PEDIA_CATEGORY_CONCEPT", ())
		self.szCategoryConceptsNew	= localText.getText("TXT_KEY_PEDIA_CATEGORY_CONCEPT_NEW", ())
		self.szCategoryHints		= localText.getText("TXT_KEY_PEDIA_CATEGORY_HINTS", ())

		self.categoryList = [
			["TECHS",	self.szCategoryTechs],
			["UNITS",	self.szCategoryUnits],
			["UNITS",	self.szCategoryUnitUpgrades],
			["UNITS",	self.szCategoryUnitCategories],
			["PROMOTIONS",	self.szCategoryPromotions],
			["PROMOTIONS",	self.szCategoryPromotionTree],
			["BUILDINGS",	self.szCategoryBuildings],
			["BUILDINGS",	self.szCategoryNationalWonders],
			["BUILDINGS",	self.szCategoryGreatWonders],
			["BUILDINGS",	self.szCategoryProjects],
			["SPECIALISTS",	self.szCategorySpecialists],
			["TERRAINS",	self.szCategoryTerrains],
			["TERRAINS",	self.szCategoryFeatures],
			["TERRAINS",	self.szCategoryBonuses],
			["TERRAINS",	self.szCategoryImprovements],
			["CIVS",	self.szCategoryCivs],
			["CIVS",	self.szCategoryLeaders],
			["CIVICS",	self.szCategoryCivics],
			["CIVICS",	self.szCategoryReligions],
			["CIVICS",	self.szCategoryCorporations],
			["HINTS",	self.szCategoryConcepts],
			["HINTS",	self.szCategoryConceptsNew],
			["HINTS",	self.szCategoryHints],
			]

		self.categoryGraphics = {
			"TECHS"		: u"%c  " %(gc.getCommerceInfo(CommerceTypes.COMMERCE_RESEARCH).getChar()),
			"UNITS"		: u"%c  " %(CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR)),
			"PROMOTIONS"	: u"%c  " %(CyGame().getSymbolID(FontSymbols.SILVER_STAR_CHAR)),
			"BUILDINGS"	: u"%c  " %(gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getChar()),
			"SPECIALISTS"	: u"%c  " %(CyGame().getSymbolID(FontSymbols.GREAT_PEOPLE_CHAR)),
			"TERRAINS"	: u"%c  " %(gc.getYieldInfo(YieldTypes.YIELD_FOOD).getChar()),
			"CIVS"		: u"%c  " %(CyGame().getSymbolID(FontSymbols.MAP_CHAR)),
			"CIVICS"	: u"%c  " %(gc.getCommerceInfo(CommerceTypes.COMMERCE_CULTURE).getChar()),
			"HINTS"		: u"%c  " %(gc.getYieldInfo(YieldTypes.YIELD_COMMERCE).getChar()),
			}

		screen = self.getScreen()
		screen.setRenderInterfaceOnly(True)
		screen.setScreenGroup(1)
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)

		screen.addDDSGFC(self.BACKGROUND_ID, ArtFileMgr.getInterfaceArtInfo("SCREEN_BG_OPAQUE").getPath(), 0, 0, self.W_SCREEN, self.H_SCREEN, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.addPanel(self.TOP_PANEL_ID, u"", u"", True, False, self.X_TOP_PANEL, self.Y_TOP_PANEL, self.W_TOP_PANEL, self.H_TOP_PANEL, PanelStyles.PANEL_STYLE_TOPBAR)
		screen.addPanel(self.BOT_PANEL_ID, u"", u"", True, False, self.X_BOT_PANEL, self.Y_BOT_PANEL, self.W_BOT_PANEL, self.H_BOT_PANEL, PanelStyles.PANEL_STYLE_BOTTOMBAR)
		screen.setDimensions(screen.centerX(0), screen.centerY(0), self.W_SCREEN, self.H_SCREEN)

		screen.setText(self.HEAD_ID, "Background", self.HEAD_TEXT, CvUtil.FONT_CENTER_JUSTIFY, self.X_TITLE, self.Y_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL,      -1, -1)
		screen.setText(self.BACK_ID, "Background", self.BACK_TEXT, CvUtil.FONT_LEFT_JUSTIFY,   self.X_BACK,  self.Y_BACK,  0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_PEDIA_BACK,    1, -1)
		screen.setText(self.NEXT_ID, "Background", self.NEXT_TEXT, CvUtil.FONT_LEFT_JUSTIFY,   self.X_NEXT,  self.Y_NEXT,  0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_PEDIA_FORWARD, 1, -1)
		screen.setText(self.EXIT_ID, "Background", self.EXIT_TEXT, CvUtil.FONT_RIGHT_JUSTIFY,  self.X_EXIT,  self.Y_EXIT,  0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1)

		screen.addListBoxGFC(self.CATEGORY_LIST_ID, "", self.X_CATEGORIES, self.Y_CATEGORIES, self.W_CATEGORIES, self.H_CATEGORIES, TableStyles.TABLE_STYLE_STANDARD)
		screen.enableSelect(self.CATEGORY_LIST_ID, True)
		screen.setStyle(self.CATEGORY_LIST_ID, "Table_StandardCiv_Style")



	def placeCategories(self):
		screen = self.getScreen()
		screen.clearListBoxGFC(self.CATEGORY_LIST_ID)
		i = 1
		for category in self.categoryList:
			graphic = self.categoryGraphics[category[0]]
			screen.appendListBoxStringNoUpdate(self.CATEGORY_LIST_ID, graphic + category[1], WidgetTypes.WIDGET_PEDIA_MAIN, SevoScreenEnums.PEDIA_MAIN + i, 0, CvUtil.FONT_LEFT_JUSTIFY)
			i += 1
		screen.updateListBox(self.CATEGORY_LIST_ID)



	def placeTechs(self):
		self.list = self.getSortedList(gc.getNumTechInfos(), gc.getTechInfo)
		self.placeItems(WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, gc.getTechInfo)


	def placeUnits(self):
		self.list = self.getSortedList(gc.getNumUnitInfos(), gc.getUnitInfo)
		self.placeItems(WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, gc.getUnitInfo)


	def placeUnitUpgrades(self):
		screen = self.getScreen()
		self.getScreen().deleteWidget("PediaMainItemList")
		self.UPGRADES_GRAPH_ID = self.getNextWidgetName()
		screen.addScrollPanel(self.UPGRADES_GRAPH_ID, u"", self.X_ITEMS, self.Y_PEDIA_PAGE - 13, self.W_SCREEN - self.X_ITEMS, self.H_PEDIA_PAGE + 2, PanelStyles.PANEL_STYLE_STANDARD)
		screen.setActivation(self.UPGRADES_GRAPH_ID, ActivationTypes.ACTIVATE_NORMAL)
		upgradesGraph = UnitUpgradesGraph.UnitUpgradesGraph(self)
		upgradesGraph.getGraph()
		upgradesGraph.drawGraph()


	def placeUnitCategories(self):
		self.list = self.getSortedList(gc.getNumUnitCombatInfos(), gc.getUnitCombatInfo)
		self.placeItems(WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT_COMBAT, gc.getUnitCombatInfo)


	def placePromotions(self):
		self.list = self.getSortedList(gc.getNumPromotionInfos(), gc.getPromotionInfo)
		self.placeItems(WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, gc.getPromotionInfo)


	def placePromotionTree(self):
		screen = self.getScreen()
		self.getScreen().deleteWidget("PediaMainItemList")
		self.UPGRADES_GRAPH_ID = self.getNextWidgetName()
		screen.addScrollPanel(self.UPGRADES_GRAPH_ID, u"", self.X_ITEMS, self.Y_PEDIA_PAGE - 13, self.W_SCREEN - self.X_ITEMS, self.H_PEDIA_PAGE + 2, PanelStyles.PANEL_STYLE_STANDARD)
		screen.setActivation(self.UPGRADES_GRAPH_ID, ActivationTypes.ACTIVATE_NORMAL)
		upgradesGraph = UnitUpgradesGraph.PromotionsGraph(self)
		upgradesGraph.getGraph()
		upgradesGraph.drawGraph()


	def placeBuildings(self):
		self.list = self.pediaBuilding.getBuildingSortedList(0)
		self.placeItems(WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, gc.getBuildingInfo)


	def placeNationalWonders(self):
		self.list = self.pediaBuilding.getBuildingSortedList(1)
		self.placeItems(WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, gc.getBuildingInfo)


	def placeGreatWonders(self):
		self.list = self.pediaBuilding.getBuildingSortedList(2)
		self.placeItems(WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, gc.getBuildingInfo)


	def placeProjects(self):
		self.list = self.getSortedList(gc.getNumProjectInfos(), gc.getProjectInfo)
		self.placeItems(WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROJECT, gc.getProjectInfo)


	def placeSpecialists(self):
		self.list = self.getSortedList(gc.getNumSpecialistInfos(), gc.getSpecialistInfo)
		self.placeItems(WidgetTypes.WIDGET_PEDIA_JUMP_TO_SPECIALIST, gc.getSpecialistInfo)


	def placeTerrains(self):
		self.list = self.getSortedList(gc.getNumTerrainInfos(), gc.getTerrainInfo)
		self.placeItems(WidgetTypes.WIDGET_PEDIA_JUMP_TO_TERRAIN, gc.getTerrainInfo)


	def placeFeatures(self):
		self.list = self.getSortedList(gc.getNumFeatureInfos(), gc.getFeatureInfo)
		self.placeItems(WidgetTypes.WIDGET_PEDIA_JUMP_TO_FEATURE, gc.getFeatureInfo)


	def placeBonuses(self):
		self.list = self.getSortedList(gc.getNumBonusInfos(), gc.getBonusInfo)
		self.placeItems(WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, gc.getBonusInfo)


	def placeImprovements(self):
		self.list = self.getSortedList(gc.getNumImprovementInfos(), gc.getImprovementInfo)
		self.placeItems(WidgetTypes.WIDGET_PEDIA_JUMP_TO_IMPROVEMENT, gc.getImprovementInfo)


	def placeCivs(self):
		self.list = self.getSortedList(gc.getNumCivilizationInfos(), gc.getCivilizationInfo)
		self.placeItems(WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIV, gc.getCivilizationInfo)


	def placeLeaders(self):
		self.list = self.getSortedList(gc.getNumLeaderHeadInfos(), gc.getLeaderHeadInfo)
		self.placeItems(WidgetTypes.WIDGET_PEDIA_JUMP_TO_LEADER, gc.getLeaderHeadInfo)


	def placeCivics(self):
		self.list = self.getSortedList(gc.getNumCivicInfos(), gc.getCivicInfo)
		self.placeItems(WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIVIC, gc.getCivicInfo)


	def placeReligions(self):
		self.list = self.getSortedList(gc.getNumReligionInfos(), gc.getReligionInfo)
		self.placeItems(WidgetTypes.WIDGET_PEDIA_JUMP_TO_RELIGION, gc.getReligionInfo)


	def placeCorporations(self):
		self.list = self.getSortedList(gc.getNumCorporationInfos(), gc.getCorporationInfo)
		self.placeItems(WidgetTypes.WIDGET_PEDIA_JUMP_TO_CORPORATION, gc.getCorporationInfo)


	def placeConcepts(self):
		self.list = self.getSortedList(gc.getNumConceptInfos(), gc.getConceptInfo)
		self.placeItems(WidgetTypes.WIDGET_PEDIA_DESCRIPTION, gc.getConceptInfo)


	def placeBTSConcepts(self):
		self.list = self.getSortedList(gc.getNumNewConceptInfos(), gc.getNewConceptInfo)
		self.placeItems(WidgetTypes.WIDGET_PEDIA_DESCRIPTION, gc.getNewConceptInfo)


	def placeItems(self, widget, info):
		screen = self.getScreen()
		screen.clearListBoxGFC(self.ITEM_LIST_ID)

		screen.addTableControlGFC(self.ITEM_LIST_ID, 1, self.X_ITEMS, self.Y_ITEMS, self.W_ITEMS, self.H_ITEMS, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
		screen.enableSelect(self.ITEM_LIST_ID, False)
		screen.setStyle(self.ITEM_LIST_ID, "Table_StandardCiv_Style")
		screen.setTableColumnHeader(self.ITEM_LIST_ID, 0, "", self.W_ITEMS)

		i = 0
		for item in self.list:
			if (info == gc.getConceptInfo):
				data1 = CivilopediaPageTypes.CIVILOPEDIA_PAGE_CONCEPT
				data2 = item[1]
			elif (info == gc.getNewConceptInfo):
				data1 = CivilopediaPageTypes.CIVILOPEDIA_PAGE_CONCEPT_NEW
				data2 = item[1]
			else:
				data1 = item[1]
				data2 = 1
			screen.appendTableRow(self.ITEM_LIST_ID)
			screen.setTableText(self.ITEM_LIST_ID, 0, i, u"<font=3>" + item[0] + u"</font>", info(item[1]).getButton(), widget, data1, data2, CvUtil.FONT_LEFT_JUSTIFY)
			i += 1
		screen.updateListBox(self.ITEM_LIST_ID)


	def placeHints(self):
		screen = self.getScreen()
		self.getScreen().deleteWidget("PediaMainItemList")
		szHintBox = self.getNextWidgetName()
		screen.addListBoxGFC(szHintBox, "", self.X_ITEMS, self.Y_PEDIA_PAGE - 10, self.W_SCREEN - self.X_ITEMS, self.H_PEDIA_PAGE + 23, TableStyles.TABLE_STYLE_STANDARD)
		screen.enableSelect(szHintBox, False)
		szHintsText = CyGameTextMgr().buildHintsList()
		hintText = string.split(szHintsText, "\n")
		for hint in hintText:
			if len(hint) != 0:
				screen.appendListBoxStringNoUpdate(szHintBox, hint, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.updateListBox(szHintBox)



	def back(self):
		if (len(self.pediaHistory) > 1):
			self.pediaFuture.append(self.pediaHistory.pop())
			current = self.pediaHistory.pop()
			self.pediaJump(current[0], current[1], False, True)
		return 1



	def forward(self):
		if (self.pediaFuture):
			current = self.pediaFuture.pop()
			self.pediaJump(current[0], current[1], False, True)
		return 1



	def link(self, szLink):
		if (szLink == "PEDIA_MAIN_TECH"):
			self.pediaJump(SevoScreenEnums.PEDIA_MAIN, SevoScreenEnums.PEDIA_TECHS, True, True)
		elif (szLink == "PEDIA_MAIN_UNIT"):
			self.pediaJump(SevoScreenEnums.PEDIA_MAIN, SevoScreenEnums.PEDIA_UNITS, True, True)
		elif (szLink == "PEDIA_MAIN_UNIT_GROUP"):
			self.pediaJump(SevoScreenEnums.PEDIA_MAIN, SevoScreenEnums.PEDIA_UNIT_CATEGORIES, True, True)
		elif (szLink == "PEDIA_MAIN_PROMOTION"):
			self.pediaJump(SevoScreenEnums.PEDIA_MAIN, SevoScreenEnums.PEDIA_PROMOTIONS, True, True)
		elif (szLink == "PEDIA_MAIN_BUILDING"):
			self.pediaJump(SevoScreenEnums.PEDIA_MAIN, SevoScreenEnums.PEDIA_BUILDINGS, True, True)
		elif (szLink == "PEDIA_MAIN_PROJECT"):
			self.pediaJump(SevoScreenEnums.PEDIA_MAIN, SevoScreenEnums.PEDIA_PROJECTS, True, True)
		elif (szLink == "PEDIA_MAIN_SPECIALIST"):
			self.pediaJump(SevoScreenEnums.PEDIA_MAIN, SevoScreenEnums.PEDIA_SPECIALISTS, True, True)
		elif (szLink == "PEDIA_MAIN_TERRAIN"):
			self.pediaJump(SevoScreenEnums.PEDIA_MAIN, SevoScreenEnums.PEDIA_TERRAINS, True, True)
		elif (szLink == "PEDIA_MAIN_FEATURE"):
			self.pediaJump(SevoScreenEnums.PEDIA_MAIN, SevoScreenEnums.PEDIA_FEATURES, True, True)
		elif (szLink == "PEDIA_MAIN_BONUS"):
			self.pediaJump(SevoScreenEnums.PEDIA_MAIN, SevoScreenEnums.PEDIA_BONUSES, True, True)
		elif (szLink == "PEDIA_MAIN_IMPROVEMENT"):
			self.pediaJump(SevoScreenEnums.PEDIA_MAIN, SevoScreenEnums.PEDIA_IMPROVEMENTS, True, True)
		elif (szLink == "PEDIA_MAIN_CIV"):
			self.pediaJump(SevoScreenEnums.PEDIA_MAIN, SevoScreenEnums.PEDIA_CIVS, True, True)
		elif (szLink == "PEDIA_MAIN_LEADER"):
			self.pediaJump(SevoScreenEnums.PEDIA_MAIN, SevoScreenEnums.PEDIA_LEADERS, True, True)
		elif (szLink == "PEDIA_MAIN_CIVIC"):
			self.pediaJump(SevoScreenEnums.PEDIA_MAIN, SevoScreenEnums.PEDIA_CIVICS, True, True)
		elif (szLink == "PEDIA_MAIN_RELIGION"):
			self.pediaJump(SevoScreenEnums.PEDIA_MAIN, SevoScreenEnums.PEDIA_RELIGIONS, True, True)
		elif (szLink == "PEDIA_MAIN_CONCEPT"):
			self.pediaJump(SevoScreenEnums.PEDIA_MAIN, SevoScreenEnums.PEDIA_CONCEPTS, True, True)
		elif (szLink == "PEDIA_MAIN_HINTS"):
			self.pediaJump(SevoScreenEnums.PEDIA_MAIN, SevoScreenEnums.PEDIA_HINTS, True, True)

		for i in range(gc.getNumTechInfos()):
			if (gc.getTechInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(SevoScreenEnums.PEDIA_TECHS, i, True, True)
		for i in range(gc.getNumUnitInfos()):
			if (gc.getUnitInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(SevoScreenEnums.PEDIA_UNITS, i, True, True)
		for i in range(gc.getNumUnitCombatInfos()):
			if (gc.getUnitCombatInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(SevoScreenEnums.PEDIA_UNIT_CATEGORIES, i, True, True)
		for i in range(gc.getNumPromotionInfos()):
			if (gc.getPromotionInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(SevoScreenEnums.PEDIA_PROMOTIONS, i, True, True)
		for i in range(gc.getNumBuildingInfos()):
			if (gc.getBuildingInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(SevoScreenEnums.PEDIA_BUILDINGS, i, True, True)
		for i in range(gc.getNumProjectInfos()):
			if (gc.getProjectInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(SevoScreenEnums.PEDIA_PROJECTS, i, True, True)
		for i in range(gc.getNumSpecialistInfos()):
			if (gc.getSpecialistInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(SevoScreenEnums.PEDIA_SPECIALISTS, i, True, True)
		for i in range(gc.getNumTerrainInfos()):
			if (gc.getTerrainInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(SevoScreenEnums.PEDIA_TERRAINS, i, True, True)
		for i in range(gc.getNumFeatureInfos()):
			if (gc.getFeatureInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(SevoScreenEnums.PEDIA_FEATURES, i, True, True)
		for i in range(gc.getNumBonusInfos()):
			if (gc.getBonusInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(SevoScreenEnums.PEDIA_BONUSES, i, True, True)
		for i in range(gc.getNumImprovementInfos()):
			if (gc.getImprovementInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(SevoScreenEnums.PEDIA_IMPROVEMENTS, i, True, True)
		for i in range(gc.getNumCivilizationInfos()):
			if (gc.getCivilizationInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(SevoScreenEnums.PEDIA_CIVS, i, True, True)
		for i in range(gc.getNumLeaderHeadInfos()):
			if (gc.getLeaderHeadInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(SevoScreenEnums.PEDIA_LEADERS, i, True, True)
		for i in range(gc.getNumCivicInfos()):
			if (gc.getCivicInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(SevoScreenEnums.PEDIA_CIVICS, i, True, True)
		for i in range(gc.getNumReligionInfos()):
			if (gc.getReligionInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(SevoScreenEnums.PEDIA_RELIGIONS, i, True, True)
		for i in range(gc.getNumCorporationInfos()):
			if (gc.getCorporationInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(SevoScreenEnums.PEDIA_CORPORATIONS, i, True, True)
		for i in range(gc.getNumConceptInfos()):
			if (gc.getConceptInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(SevoScreenEnums.PEDIA_CONCEPTS, i, True, True)
		for i in range(gc.getNumNewConceptInfos()):
			if (gc.getNewConceptInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(SevoScreenEnums.PEDIA_BTS_CONCEPTS, i, True, True)



	def handleInput (self, inputClass):
		if (inputClass.getPythonFile() == SevoScreenEnums.PEDIA_LEADERS):
			return self.pediaLeader.handleInput(inputClass)
		return 0



	def deleteAllWidgets(self):
		screen = self.getScreen()
		iNumWidgets = self.nWidgetCount
		self.nWidgetCount = 0
		for i in range(iNumWidgets):
			screen.deleteWidget(self.getNextWidgetName())
		self.nWidgetCount = 0


	def getNextWidgetName(self):
		szName = self.WIDGET_ID + str(self.nWidgetCount)
		self.nWidgetCount += 1
		return szName


	def isSortLists(self):
		return BugScreens.isSortSevopedia()

	def getSortedList(self, numInfos, getInfo):
		list = [(0,0)] * numInfos
		for i in range(numInfos):
			list[i] = (getInfo(i).getDescription(), i)
		if self.isSortLists():
			list.sort()
		return list
