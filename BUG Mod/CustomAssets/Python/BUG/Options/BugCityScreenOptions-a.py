## BugCityScreenOptions								
## Facade for accessing City Screen options								
## BUG Mod - Copyright 2007								
								
from CvPythonExtensions import *								
from BugOptions import OptionsFacade, Option, OptionList								
localText = CyTranslator()
								
class BugCityScreenOptions(OptionsFacade):								
								
	def __init__(self):							
		OptionsFacade.__init__(self)						
								
		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_CITY_RAWCOMMERCE_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_CITY_RAWCOMMERCE_HOVER", ())						
		self.addOption(Option("City_RawCommerce",						
							  "City Screen", "Raw Commerce", False, zs_Text, zsHover,
							  InterfaceDirtyBits.CityScreen_DIRTY_BIT))	

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_CITY_CULTURETURNS_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_CITY_CULTURETURNS_HOVER", ())						
		self.addOption(Option("City_CultureTurns",						
							  "City Screen", "Culture Turns", False, zs_Text, zsHover,
							  InterfaceDirtyBits.CityScreen_DIRTY_BIT))	

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_CITY_GREATPERSONTURNS_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_CITY_GREATPERSONTURNS_HOVER", ())						
		self.addOption(Option("City_GreatPersonTurns",						
							  "City Screen", "Great Person Turns", False, zs_Text, zsHover,
							  InterfaceDirtyBits.CityScreen_DIRTY_BIT))	

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_CITY_GREATPERSONINFO_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_CITY_GREATPERSONINFO_HOVER", ())						
		self.addOption(Option("City_GreatPersonInfo",						
							  "City Screen", "Great Person Info", False, zs_Text, zsHover,
							  InterfaceDirtyBits.CityScreen_DIRTY_BIT))	

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_CITY_ANGER_COUNTER_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_CITY_ANGER_COUNTER_HOVER", ())						
		self.addOption(Option("City_Anger_Counter",						
							  "Screens", "Anger Counter", True, zs_Text, zsHover, 
							  InterfaceDirtyBits.MiscButtons_DIRTY_BIT))	

		zs_Text = localText.getText("TXT_KEY_BUGOPTIONS_CITY_SPECIALISTS_TEXT", ())						
		zsHover = localText.getText("TXT_KEY_BUGOPTIONS_CITY_SPECIALISTS_HOVER", ())						
		self.addOption(OptionList("City_Specialists",						
								  "City Screen", "City Specialists", 0, zs_Text, zsHover,
								  ['Default', 'Stacker', 'Chevron'], None,
								  InterfaceDirtyBits.GameData_DIRTY_BIT))


	def isShowRawCommerce(self):							
		return self.getBoolean('City_RawCommerce')						
								
	def isShowCultureTurns(self):							
		return self.getBoolean('City_CultureTurns')						
								
	def isShowGreatPersonTurns(self):							
		return self.getBoolean('City_GreatPersonTurns')						
								
	def isShowCityGreatPersonInfo(self):							
		return self.getBoolean('City_GreatPersonInfo')						
								
	def isShowAngerCounter(self):							
		return self.getBoolean('City_Anger_Counter')						
								
	def getCitySpecialist(self):							
		return self.getInt('City_Specialists')						
								
	def isCitySpecialist_Default(self):							
		return self.getCitySpecialist() == 0						
								
	def isCitySpecialist_Stacker(self):							
		return self.getCitySpecialist() == 1						
								
	def isCitySpecialist_Chevron(self):							
		return self.getCitySpecialist() == 2						
								
								
# The singleton BugCityScreenOptions object								
								
__g_options = BugCityScreenOptions()								
def getOptions():								
	return __g_options							
