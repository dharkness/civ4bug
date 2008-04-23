## BugPath
##
## Helps locate INI and other setup files for the BUG Mod.
## Based on CvPath by Dr. Elmer Jiggles.
##
## Copyright 2008 (c) BUG Mod

import os
import os.path
import sys

modName = None
try:
	import CvModName
	modName = CvModName.modName
except:
	pass

# Determine the base user directory (e.g. "C:\...\My Documents\My Games").
userDir = None
if (sys.platform == 'darwin'):
	"Mac OS X"
	userDir = os.path.join(os.environ['HOME'], "Documents")
else:
	import _winreg
	"Windows"
	def __getRegValue(root, subkey, name):
		key = _winreg.OpenKey(root, subkey)
		try:
			value = _winreg.QueryValueEx(key, name)
			return value[0]
		finally:
			key.Close()
	
	myDocuments = __getRegValue(_winreg.HKEY_CURRENT_USER, 
			r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders",
			"Personal")
	userDir = os.path.join(myDocuments, "My Games")

# Determine the root directory that holds the executable and mods
# as well as the directory inside "My Games" that holds CustomAssets and mods.
rootDir = None
appName = "Beyond the Sword"
if (sys.executable):
	rootDir = os.path.dirname(sys.executable)
	appName = os.path.basename(rootDir)

# Create an ordered list of paths which are searched for INI files.
iniFileSearchPaths = []
def addIniFileSearchPath(path):
	"Adds the given path to the search list if it is a directory."
	if (os.path.isdir(path)):
		iniFileSearchPaths.append(path)

if (userDir):
	if (modName):
		addIniFileSearchPath(os.path.join(userDir, modName))
		addIniFileSearchPath(os.path.join(userDir, appName, "Mods", modName))
	addIniFileSearchPath(os.path.join(userDir, appName))
if (rootDir):
	if (modName):
		addIniFileSearchPath(os.path.join(rootDir, "Mods", modName))
	addIniFileSearchPath(os.path.join(rootDir))

if (not iniFileSearchPaths):
	pass

def findIniFile(name, subdir=None):
	"Locates the named configuration file using the search paths above."
	for dir in iniFileSearchPaths:
		if (subdir):
			file = os.path.join(dir, subdir, name)
		else:
			file = os.path.join(dir, name)
		if (os.path.isfile(file)):
			return file
	return None

def findMainModIniFile():
	"Locates the main INI file for the mod."
	if (modName):
		return findIniFile(modName + ".ini")
	else:
		return None
