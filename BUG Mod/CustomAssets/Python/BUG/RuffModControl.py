## RuffModControl.py - used to control access to RuffMod ini file.
## modified from HOF MOD V1.61.001
## Hall of Fame Mod Context
## Used to access Mod Ini file

import os
import os.path
from types import *
from configobj import ConfigObj
import CvUtil
import CvPath
from CvPythonExtensions import *

def get_AutoLog_Path():
    try:
        AutoLogPath = RuffModConfigFile['AUTOLOG']['AutoLogPath']
    except:
        AutoLogPath = os.path.join(CvPath.userDir, 'AutoLog')
    if (AutoLogPath == 'Default'):
        AutoLogPath = os.path.join(CvPath.userDir, 'AutoLog')
    if not os.path.isdir(AutoLogPath) and not os.path.isfile(AutoLogPath):
        os.makedirs(AutoLogPath)
    return AutoLogPath

def read_AdvUnitNameFile():
    return ConfigObj(AdvUnitNameFile)

def read_ConfigFile():
    return ConfigObj(FileName)

def write_ConfigFile():
	try:
		RuffModConfigFile.write()
	except:
		pass

try:
    import CvModName
    mod = CvModName.modName
except:
    mod = "BUG Mod"
FileName = CvPath.get_INI_File(mod + ".ini")
RuffModConfigFile = read_ConfigFile()

AdvUnitNameFile = CvPath.get_INI_File("Adv Unit Naming.ini")
RuffModAdvUnitNameFile = read_AdvUnitNameFile()

##----------------------------------------------------------------
class RuffModConfig:
    def __init__(self):
        pass
        
## Private Functions
    def __get_keyvalue(self, section, key, default):
        try: keyvalue = RuffModConfigFile[section][key]
        except: keyvalue = default
        return keyvalue

    def __set_keyvalue(self, section, key, keyvalue):
        RuffModConfigFile[section][key] = keyvalue
        return
    
    def __get_boolkeyvalue(self, section, key, default):
        try: keyvalue = RuffModConfigFile[section].as_bool(key)
        except: keyvalue = default
        return keyvalue
    
## Get Functions
    def get_int(self, section, key, default):
        keyvalue = self.__get_keyvalue(section, key, default)
        try: keyvalue = int(keyvalue)
        except: keyvalue = default
        return keyvalue

    def get_str(self, section, key, default):
        keyvalue = self.__get_keyvalue(section, key, default)
        if not isinstance(keyvalue, StringTypes) : keyvalue = default
        return keyvalue

    def get_boolean(self, section, key, default):
        keyvalue = self.__get_boolkeyvalue(section, key, default)
        if keyvalue == False :
            return False
        elif keyvalue == True :
            return True
        else :
            return default
        
    def get_float(self, section, key, default):
        keyvalue = self.__get_keyvalue(section, key, default)
        try: keyvalue = float(keyvalue)
        except: keyvalue = default
        return keyvalue
    
    def get_advunitname(self, section, key, default):
        keyvalue = RuffModAdvUnitNameFile[section][key]
        if not isinstance(keyvalue, StringTypes) : keyvalue = default
        return keyvalue

## Set Functions
    def set_int(self, section, key, keyvalue):
        self.__set_keyvalue(section, key, keyvalue)
        return
        
    def set_str(self, section, key, keyvalue):
        self.__set_keyvalue(section, key, keyvalue)
        return

    def set_boolean(self, section, key, keyvalue):
        self.__set_keyvalue(section, key, keyvalue)
        return

    def set_float(self, section, key, keyvalue):
        self.__set_keyvalue(section, key, keyvalue)
        return

