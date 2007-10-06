## BugUnitNameOptionsTab
## Tab for the BUG Unit Name Options
## BUG Mod - Copyright 2007

import BugOptionsTab

class BugUnitNameOptionsTab(BugOptionsTab.BugOptionsTab):
	"BUG Unit Name Options Screen Tab"
	
	def __init__(self, screen):
		BugOptionsTab.BugOptionsTab.__init__(self, "UnitName", "Unit Naming")

	def create(self, screen):
		tab = self.createTab(screen)
		panel = self.createMainPanel(screen)
		column = self.addOneColumnLayout(screen, panel)
	
		self.addCheckbox(screen, column, "UnitName_Enabled")
#		tab.addMissingOption(screen, column, "")
#		screen.attachLabel(column, "AdvancedLabel", "There are also naming options in the ini file that take up too much room here.")
#	def addMissingOption (self, screen, panel, name):
#		self.addCheckbox(screen, column, "UnitName_UseAdvanced")

		self.addTextEdit(screen, column, column, "UnitName_Default")
		self.addTextEdit(screen, column, column, "UnitName_Combat_AIR")
		self.addTextEdit(screen, column, column, "UnitName_Combat_ARCHER")
		self.addTextEdit(screen, column, column, "UnitName_Combat_ARMOR")
		self.addTextEdit(screen, column, column, "UnitName_Combat_GUN")
		self.addTextEdit(screen, column, column, "UnitName_Combat_HELICOPTER")
		self.addTextEdit(screen, column, column, "UnitName_Combat_MELEE")
		self.addTextEdit(screen, column, column, "UnitName_Combat_MOUNTED")
		self.addTextEdit(screen, column, column, "UnitName_Combat_NAVAL")
		self.addTextEdit(screen, column, column, "UnitName_Combat_None")
		self.addTextEdit(screen, column, column, "UnitName_Combat_RECON")
		self.addTextEdit(screen, column, column, "UnitName_Combat_SIEGE")
