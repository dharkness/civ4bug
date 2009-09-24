## BugPath
##
## Helps locate INI and other setup files for the BUG Mod.
## Based on CvPath by Dr. Elmer Jiggles.
##
## Copyright (c) 2008 The BUG Mod.
##
## Author: EmperorFool

# This module locates INI and other configuration files and directories.
# It exposes several useful variables:
#
# modName
#   Pulled from CvModName
#
# userDir
#   Typically the "My Documents\My Games" folder on Windows and the "Documents"
#   folder on MacOS X. Both are in the user's private documents area.
#
# rootDir
#   Location of the Civ4 executable (CIV4BeyondSword.exe on Windows)
#
# appName
#   The final component in rootDir, typically "Beyond the Sword"
#
# iniFileSearchPaths
#   A set of existing directories in which this module searches for configuration
#   files and directories.
#
#   The preference order is
#
#     1. <user-dir>\<mod-name>
#     2. <user-dir>\<app-name>\Mods\<mod-name>
#     3. <user-dir>\<app-name>\<mod-name>
#     3. <user-dir>\<app-name>
#     4. <root-dir>\<app-name>\Mods\<mod-name>
#     5. <root-dir>\<app-name>\<mod-name>
#     5. <root-dir>\<app-name>
#
# mainModIniDir
#   If the main INI file is loaded, this holds the directory where it was found.
#   It will be one of the directories in iniFileSearchPaths. It can be used as a
#   preference for where to store new files.
#
# All directory variables exposed are guaranteed to be existing directories when
# they were found. Otherwise they will be the Python None value.

import os
import os.path
import sys
import BugConfigTracker
import BugUtil

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
	BugUtil.debug("BugPath - My Documents dir is '%s'", myDocuments)
	userDir = os.path.join(myDocuments, "My Games")
BugUtil.debug("BugPath - user dir is '%s'", userDir)

# Determine the root directory that holds the executable and mods
# as well as the directory inside "My Games" that holds CustomAssets and mods.
rootDir = None
appName = "Beyond the Sword"
if (sys.executable):
	rootDir = os.path.dirname(sys.executable)
	appName = os.path.basename(rootDir)
	BugUtil.debug("BugPath - root dir is '%s'", rootDir)
	BugUtil.debug("BugPath - app name is '%s'", appName)

# Create an ordered list of paths which are searched for INI files.
iniFileSearchPaths = []
def addIniFileSearchPath(path):
	"""Adds the given path to the search list if it is a valid directory."""
	if (os.path.isdir(path)):
		BugUtil.info("BugPath - adding search path '%s'", path)
		iniFileSearchPaths.append(path)

if (userDir):
	if (modName):
		addIniFileSearchPath(os.path.join(userDir, modName))
		addIniFileSearchPath(os.path.join(userDir, appName, modName))
		addIniFileSearchPath(os.path.join(userDir, appName, "Mods", modName))
	addIniFileSearchPath(os.path.join(userDir, appName))
if (rootDir):
	if (modName):
		addIniFileSearchPath(os.path.join(rootDir, modName))
		addIniFileSearchPath(os.path.join(rootDir, "Mods", modName))
	addIniFileSearchPath(os.path.join(rootDir))

if (iniFileSearchPaths):
	BugConfigTracker.add("Config_Search_Paths", iniFileSearchPaths)
else:
	pass

def findIniFile(name, subdir=None):
	"Locates the named configuration file using the search paths above."
	for dir in iniFileSearchPaths:
		if (subdir):
			path = os.path.join(dir, subdir, name)
		else:
			path = os.path.join(dir, name)
		if (os.path.isfile(path)):
			return path
	return None

def createIniFile(name, subdir=None):
	"Returns the path for the default location of the named INI file so it can be created."
	if iniFileSearchPaths:
		dir = iniFileSearchPaths[0]
		if (subdir):
			return os.path.join(dir, subdir, name)
		else:
			return os.path.join(dir, name)
	if (subdir):
		return os.path.join(subdir, name)
	else:
		return name

mainModIniDir = None
def findMainModIniFile():
	"Locates the main INI file for the mod."
	if (modName):
		file = findIniFile(modName + ".ini")
		if (file):
			mainModIniDir = os.path.dirname(file)
		return file
	else:
		return None

def findDir(name):
	"Locates the named directory using the INI file search paths above."
	for dir in iniFileSearchPaths:
		path = os.path.join(dir, name)
		if (os.path.isdir(path)):
			return path
	return None

def makeDir(name):
	"Creates a new directory where the INI file was found or the first directory in the search path."
	if (mainModIniDir):
		path = os.path.join(mainModIniDir, name)
	elif (iniFileSearchPaths):
		path = os.path.join(iniFileSearchPaths[0], name)
	else:
		path = name
	if (not os.path.isdir(path)):
		os.makedirs(path)
	return path

def findOrMakeDir(name):
	"Locates or creates the specified directory."
	dir = findDir(name)
	if (not dir):
		dir = makeDir(name)
	return dir


# Create an ordered list of paths which are searched for asset files.
assetFileSearchPaths = []
def addAssetFileSearchPath(path):
	"Adds the given path to the search list if it is a directory."
	if (os.path.isdir(path)):
		assetFileSearchPaths.append(path)

if (userDir):
	addAssetFileSearchPath(os.path.join(userDir, appName, "CustomAssets"))
	if (modName):
		addAssetFileSearchPath(os.path.join(userDir, appName, "Mods", modName, "Assets"))
if (rootDir):
	if (modName):
		addAssetFileSearchPath(os.path.join(rootDir, "Mods", modName, "Assets"))
	addAssetFileSearchPath(os.path.join(rootDir, "Assets"))

if (assetFileSearchPaths):
	BugConfigTracker.add("Asset_Search_Paths", assetFileSearchPaths)
else:
	pass

def findAssetFile(name, subdir=None):
	"Locates the named asset file using the search paths above."
	for dir in assetFileSearchPaths:
		if (subdir):
			path = os.path.join(dir, subdir, name)
		else:
			path = os.path.join(dir, name)
		if (os.path.isfile(path)):
			return path
	if (subdir):
		BugUtil.warn("BugPath - cannot find asset file %s in %s", name, subdir)
	else:
		BugUtil.warn("BugPath - cannot find asset file %s", name)
	return None