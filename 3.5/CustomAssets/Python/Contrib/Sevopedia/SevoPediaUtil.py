## SevoPediaUtil
##
## Loads the SevoPedia options before the BUG core has been initialized
## and stores them into UnsavedOptions for use from the main menu.
##
## Copyright (c) 2008 The BUG Mod.
##
## Author: EmperorFool

import BugCore
import BugOptions
import BugPath
import BugUtil
import configobj

AdvisorOpt = BugCore.game.Advisors
enabledOption = None
sortOption = None
needToLoad = False

if not AdvisorOpt._hasOption("Sevopedia"):
	BugUtil.debug("BUG: creating stub Sevopedia option")
	enabledOption = BugOptions.UnsavedOption(AdvisorOpt, "Sevopedia", "boolean", True)
	AdvisorOpt._addOption(enabledOption)
	needToLoad = True

if not AdvisorOpt._hasOption("SevopediaSortItemList"):
	BugUtil.debug("BUG: creating stub Sevopedia Sort option")
	sortOption = BugOptions.UnsavedOption(AdvisorOpt, "SevopediaSortItemList", "boolean", True)
	AdvisorOpt._addOption(sortOption)
	needToLoad = True

if needToLoad:
	path = BugPath.findIniFile("BUG Advisors.ini")
	if path:
		BugUtil.debug("BUG: loading options from '%s'" % path)
		config = configobj.ConfigObj(path)
		if "Advisors" in config:
			section = config["Advisors"]
			if enabledOption is not None and "Sevopedia" in section:
				enabledOption.setValue(section.as_bool("Sevopedia"))
			if sortOption is not None and "Sevopedia Sort" in section:
				sortOption.setValue(section.as_bool("Sevopedia Sort"))
