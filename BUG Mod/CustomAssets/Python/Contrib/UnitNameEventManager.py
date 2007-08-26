## UnitName
## by Ruff_Hi
## for BUG Mod
##-------------------------------------------------------------------
## Reorganized to work via CvCustomEventManager
## using Civ4lerts as template.
## CvCustomEventManager & Civ4lerts by Gillmer J. Derge
##-------------------------------------------------------------------
##
## TODO:
## - Use onPlayerChangeStateReligion event

from CvPythonExtensions import *
import CvUtil
import PyHelpers
import BugUnitNameOptions

gc = CyGlobalContext()
BugUnitName = BugUnitNameOptions.BugUnitNameOptions()

class UnitNameEventManager:

	def __init__(self, eventManager):

		BuildUnitName(eventManager)

class AbstractBuildUnitName(object):

	def __init__(self, eventManager, *args, **kwargs):
		super(AbstractBuildUnitName, self).__init__(*args, **kwargs)

class BuildUnitName(AbstractBuildUnitName):

	def __init__(self, eventManager, *args, **kwargs):
		super(BuildUnitName, self).__init__(eventManager, *args, **kwargs)

		eventManager.addEventHandler("unitBuilt", self.onUnitBuilt)

		self.eventMgr = eventManager

	def onUnitBuilt(self, argsList):
		'Unit Completed'

		city = argsList[0]
		unit = argsList[1]
#		iOwner = gc.getPlayer(unit.getOwner())

		if (not unit.getOwner() == CyGame().getActivePlayer()
		or not BugUnitName.isEnabled()
		or BugUnitName.isAdvanced()):
			return

		civtype = iOwner.getCivilizationType()

		zsUnitNameConv = BugUnitName.getCombat(unit.getUnitCombatType)
		if zsUnitNameConv == 'DEFAULT':
			zsUnitNameConv = BugUnitName.getDefault()

		unit.setName(zsUnitNameConv)

		return
