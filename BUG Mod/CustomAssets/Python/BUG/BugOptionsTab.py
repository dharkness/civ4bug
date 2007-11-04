## BugOptionsTab
## Base class for all tabs in the BUG Options Screen
## BUG Mod - Copyright 2007

from CvPythonExtensions import *
import ColorUtil

localText = CyTranslator()

class BugOptionsTab:
	"BUG Options Screen screen"
	
	def __init__(self, name, title):
		self.name = name
		self.tab = self.name + "Tab"
		self.title = title
		self.callbackIFace = "CvOptionsScreenCallbackInterface"

	def getName (self):
		return self.name

	def getTitle (self):
		return self.title


	def setOptions (self, options):
		self.options = options

	def getOption (self, name):
		return self.options.getOption(name)


	def create (self, screen):
		"Creates the full options screen"
		pass

	def createTab (self, screen):
		"Creates and returns the options tab"
		screen.attachTabItem(self.tab, self.title)
		
		return self.tab

	def createMainPanel (self, screen):
		"Creates and returns the options tab panel with Exit button"
		# VBox with two blocks: scrolling control panel and Exit button with separator
		vbox = self.name + "VBox"
		screen.attachVBox(self.tab, vbox)		
		
		# scrollpane
		scrollpane = self.name + "Scroll"
		screen.attachScrollPanel(vbox, scrollpane)
		screen.setLayoutFlag(scrollpane, "LAYOUT_SIZE_HEXPANDING")
		screen.setLayoutFlag(scrollpane, "LAYOUT_SIZE_VEXPANDING")
		
		# panel for option controls
		panel = self.name + "Panel"
		screen.attachPanel(scrollpane, panel)
		screen.setStyle(panel, "Panel_Tan15_Style")
		screen.setLayoutFlag(panel, "LAYOUT_SIZE_HPREFERREDEXPANDING")
		screen.setLayoutFlag(panel, "LAYOUT_SIZE_VPREFERREDEXPANDING")
		
		# panel for Exit button
		screen.attachHSeparator(vbox, "RM_ExitSeparator")
		exitPanel = self.name + "ExitBox"
		screen.attachHBox(vbox, exitPanel)
		screen.setLayoutFlag(exitPanel, "LAYOUT_HCENTER")
		
		# Exit button
		szOptionDesc = localText.getText("TXT_KEY_PEDIA_SCREEN_EXIT", ())
		exitButton = self.name + "ExitButton"
		screen.attachButton(exitPanel, exitButton, szOptionDesc, self.callbackIFace, "handleBugExitButtonInput", exitButton)
		screen.setLayoutFlag(exitButton, "LAYOUT_HCENTER")
		
		return panel

	def addOneColumnLayout (self, screen, parent, panel=None):
		"Creates an HBox containing a single VBox for a list of controls"
		if (panel is None):
			panel = parent
		hbox = panel + "HBox"
		screen.attachHBox(parent, hbox)
		screen.setLayoutFlag(hbox, "LAYOUT_SIZE_HPREFERREDEXPANDING")
		screen.setLayoutFlag(hbox, "LAYOUT_SIZE_VPREFERREDEXPANDING")
		
		column = panel + "VBox"
		screen.attachVBox(hbox, column)
		screen.setLayoutFlag(column, "LAYOUT_SIZE_HMIN")
		screen.setLayoutFlag(column, "LAYOUT_SIZE_VPREFERREDEXPANDING")
		
		return column

	def addTwoColumnLayout (self, screen, parent, panel=None, separator=False):
		"Creates an HBox containing two VBoxes for two lists of controls"
		if (panel is None):
			panel = parent
		hbox = panel + "HBox"
		screen.attachHBox(parent, hbox)
		screen.setLayoutFlag(hbox, "LAYOUT_SIZE_HPREFERREDEXPANDING")
		screen.setLayoutFlag(hbox, "LAYOUT_SIZE_VPREFERREDEXPANDING")
		
		leftColumn = panel + "Left"
		screen.attachVBox(hbox, leftColumn)
		screen.setLayoutFlag(leftColumn, "LAYOUT_SIZE_HMIN")
		screen.setLayoutFlag(leftColumn, "LAYOUT_SIZE_VPREFERREDEXPANDING")
		
		if (separator):
			sep = panel + "Sep"
			screen.attachVSeparator(hbox, sep)
			screen.setLayoutFlag(sep, "LAYOUT_LEFT")
		
		rightColumn = panel + "Right"
		screen.attachVBox(hbox, rightColumn)
		screen.setLayoutFlag(rightColumn, "LAYOUT_SIZE_HMIN")
		screen.setLayoutFlag(rightColumn, "LAYOUT_SIZE_VPREFERREDEXPANDING")
		
		return leftColumn, rightColumn

	def addThreeColumnLayout (self, screen, parent, panel=None, separator=False):
		"Creates an HBox containing three VBoxes for lists of controls"
		return self.addMultiColumnLayout(screen, parent, 3, panel, separator)

	def addMultiColumnLayout (self, screen, parent, count=2, panel=None, separator=False):
		"Creates an HBox containing multiple VBoxes for lists of controls"
		if (count <= 2):
			return self.addTwoColumnLayout(screen, parent, panel, separator)
		
		if (panel is None):
			panel = parent
		hbox = panel + "HBox"
		screen.attachHBox(parent, hbox)
		screen.setLayoutFlag(hbox, "LAYOUT_SIZE_HPREFERREDEXPANDING")
		screen.setLayoutFlag(hbox, "LAYOUT_SIZE_VPREFERREDEXPANDING")
		
		columns = []
		first = True
		for i in range(count):
			if (separator and not first):
				sep = panel + "Sep%d" % i
				screen.attachVSeparator(hbox, sep)
				#screen.setLayoutFlag(sep, "LAYOUT_LEFT")
			first = False
			
			column = panel + "Col%d" % i
			screen.attachVBox(hbox, column)
			screen.setLayoutFlag(column, "LAYOUT_SIZE_HMIN")
			screen.setLayoutFlag(column, "LAYOUT_SIZE_VPREFERREDEXPANDING")
			columns.append(column)
		
		return columns


	def addCheckbox (self, screen, panel, name):
		option = self.getOption(name)
		if (option):
			control = name + "Check"
			value = self.options.getBoolean(name)
			screen.attachCheckBox(panel, control, option.getTitle(), self.callbackIFace, "handleBugCheckboxClicked", name, value)
			screen.setToolTip(control, option.getTooltip())
			return control
		else:
			self.addMissingOption(screen, panel, name)

	def addTextEdit (self, screen, labelPanel, controlPanel, name):
		option = self.getOption(name)
		if (option):
			# create label
			if (labelPanel == controlPanel):
				box = name + "HBox"
				screen.attachHBox(labelPanel, box)
				screen.setLayoutFlag(box, "LAYOUT_SIZE_HPREFERREDEXPANDING")
				labelPanel = box
				controlPanel = box
			if (labelPanel is not None):
				label = name + "Label"
				screen.attachLabel(labelPanel, label, option.getTitle())
			
			# create textedit
			control = name + "Edit"
			value = self.options.getString(name)
			screen.attachEdit(controlPanel, control, value, self.callbackIFace, "handleBugTextEditChange", name)
			screen.setToolTip(control, option.getTooltip())
			screen.setLayoutFlag(control, "LAYOUT_SIZE_HPREFERREDEXPANDING")
		else:
			self.addMissingOption(screen, labelPanel, name)


	def addDropdown (self, screen, labelPanel, controlPanel, name, spacer, elements, index, callback):
		option = self.getOption(name)
		if (option):
			# create label
			if (labelPanel is not None):
				if (labelPanel == controlPanel or spacer):
					box = name + "HBox"
					screen.attachHBox(labelPanel, box)
					#screen.setLayoutFlag(box, "LAYOUT_SIZE_HPREFERREDEXPANDING")
					if (spacer):
						screen.attachSpacer(box)
					if (labelPanel == controlPanel):
						controlPanel = box
					labelPanel = box
				label = name + "Label"
				screen.attachLabel(labelPanel, label, option.getTitle())
				
			# create dropdown
			control = name + "Dropdown"
			screen.attachDropDown(controlPanel, control, "", elements, self.callbackIFace, callback, name, index)
			screen.setToolTip(control, option.getTooltip())
			return control
		else:
			self.addMissingOption(screen, controlPanel, name)

	def addTextDropdown (self, screen, labelPanel, controlPanel, name, spacer=False):
		option = self.getOption(name)
		if (option):
			value = self.options.getInt(name) # the actual index
			values = option.getValues()
			elements = ()
			for v in values:
				elements += (v,)
			return self.addDropdown(screen, labelPanel, controlPanel, name, spacer, elements, value, "handleBugDropdownChange")
		else:
			self.addMissingOption(screen, controlPanel, name)

	def addIntDropdown (self, screen, labelPanel, controlPanel, name, spacer=False):
		option = self.getOption(name)
		if (option):
			value = self.options.getInt(name)
			values = option.getValues()
			elements = ()
			index = -1
			bestDelta = 100000
			for i in range(len(values)):
				elements += (str(values[i]),)
				delta = abs(value - values[i])
				if (delta < bestDelta):
					index = i
					bestDelta = delta
			control = self.addDropdown(screen, labelPanel, controlPanel, name, spacer, elements, index, "handleBugIntDropdownChange")
			screen.setLayoutFlag(control, "LAYOUT_RIGHT")
			return control
		else:
			self.addMissingOption(screen, controlPanel, name)

	def addFloatDropdown (self, screen, labelPanel, controlPanel, name, spacer=False):
		option = self.getOption(name)
		if (option):
			value = self.options.getFloat(name)
			values = option.getValues()
			format = option.getFormat()
			if (format is None):
				format = "%f"
			elements = ()
			index = -1
			bestDelta = 100000
			for i in range(len(values)):
				elements += (format % values[i],)
				delta = abs(value - values[i])
				if (delta < bestDelta):
					index = i
					bestDelta = delta
			control = self.addDropdown(screen, labelPanel, controlPanel, name, spacer, elements, index, "handleBugFloatDropdownChange")
			screen.setLayoutFlag(control, "LAYOUT_RIGHT")
			return control
		else:
			self.addMissingOption(screen, controlPanel, name)

	def addColorDropdown (self, screen, labelPanel, controlPanel, name, spacer=False):
		option = self.getOption(name)
		if (option):
			value = self.options.getString(name)
			index = ColorUtil.keyToIndex(value)
			elements = ColorUtil.getColorDisplayNames()
			return self.addDropdown(screen, labelPanel, controlPanel, name, spacer, elements, index, "handleBugColorDropdownChange")
		else:
			self.addMissingOption(screen, controlPanel, name)
	

	def addCheckboxDropdown (self, screen, checkPanel, dropPanel, checkName, dropName, elements, index, callback):
		"Adds a dropdown with a checkbox for a label."
		checkOption = self.getOption(checkName)
		dropOption = self.getOption(dropName)
		if (checkOption and dropOption):
			# create checkbox
			if (checkPanel == dropPanel):
				box = checkPanel + "HBox"
				screen.attachHBox(checkPanel, box)
				#screen.setLayoutFlag(box, "LAYOUT_SIZE_HPREFERREDEXPANDING")
				checkPanel = box
				dropPanel = box
			checkControl = self.addCheckbox(screen, checkPanel, checkName)
			
			# create dropdown
			dropControl = dropName + "Dropdown"
			screen.attachDropDown(dropPanel, dropControl, "", elements, self.callbackIFace, callback, dropName, index)
			screen.setToolTip(dropControl, dropOption.getTooltip())
			return checkControl, dropControl
		else:
			if (not checkOption):
				self.addMissingOption(screen, controlPanel, checkOption)
			if (not dropOption):
				self.addMissingOption(screen, controlPanel, dropOption)

	def addCheckboxIntDropdown (self, screen, checkPanel, dropPanel, checkName, dropName):
		checkOption = self.getOption(checkName)
		dropOption = self.getOption(dropName)
		if (checkOption and dropOption):
			value = self.options.getInt(dropName)
			values = dropOption.getValues()
			elements = ()
			index = -1
			bestDelta = 100000
			for i in range(len(values)):
				elements += (str(values[i]),)
				delta = abs(value - values[i])
				if (delta < bestDelta):
					index = i
					bestDelta = delta
			checkControl, dropControl = self.addCheckboxDropdown(screen, checkPanel, dropPanel, checkName, dropName, elements, index, "handleBugIntDropdownChange")
			screen.setLayoutFlag(dropControl, "LAYOUT_RIGHT")
			return checkControl, dropControl
		else:
			if (not checkOption):
				self.addMissingOption(screen, checkPanel, checkOption)
			if (not dropOption):
				self.addMissingOption(screen, dropPanel, dropOption)

	def addCheckboxFloatDropdown (self, screen, checkPanel, dropPanel, checkName, dropName):
		checkOption = self.getOption(checkName)
		dropOption = self.getOption(dropName)
		if (checkOption and dropOption):
			value = self.options.getFloat(dropName)
			values = dropOption.getValues()
			format = dropOption.getFormat()
			if (format is None):
				format = "%f"
			elements = ()
			index = -1
			bestDelta = 100000
			for i in range(len(values)):
				elements += (format % values[i],)
				delta = abs(value - values[i])
				if (delta < bestDelta):
					index = i
					bestDelta = delta
			checkControl, dropControl = self.addCheckboxDropdown(screen, checkPanel, dropPanel, checkName, dropName, elements, index, "handleBugFloatDropdownChange")
			screen.setLayoutFlag(dropControl, "LAYOUT_RIGHT")
			return checkControl, dropControl
		else:
			if (not checkOption):
				self.addMissingOption(screen, checkPanel, checkOption)
			if (not dropOption):
				self.addMissingOption(screen, dropPanel, dropOption)


	def addMissingOption (self, screen, panel, name):
		screen.attachLabel(panel, name + "Missing", "Missing: " + name)
