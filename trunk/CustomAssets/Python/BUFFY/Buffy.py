## Buffy
##
## Collection of utility functions for dealing with BUFFY.
##
## General
##
##   - isPresent()
##     Returns True if the BUFFY is present.
##
## Notes
##   - Must be initialized externally by calling init()
##
## Copyright (c) 2009 The BUG Mod.
##
## Author: Ruff_Hi

from CvPythonExtensions import *
import BugUtil

gc = CyGlobalContext()

IS_PRESENT = True

def isPresent():
	return IS_PRESENT

def init():
	"""
	Checks for the presence of the BUG / BUFFY DLL and grabs its Python API version if found.
	"""
	try:
		if gc.isBuffy():
			global IS_PRESENT
			IS_PRESENT = True
			BugUtil.debug("BUFFY is present")
	except:
		IS_PRESENT = False
#		IS_PRESENT = True  # waiting for BULL to contain gc.isBuffy test - always true for the time being
		BugUtil.debug("BUFFY not present")
