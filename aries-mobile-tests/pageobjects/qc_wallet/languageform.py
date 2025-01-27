import logging
from pageobjects.basepage import BasePage
from pageobjects.bc_wallet.languageform import LanguageFormPage
from appium.webdriver.common.appiumby import AppiumBy

# These classes can inherit from a BasePage to do common setup and functions
class LanguageFormPageQC(LanguageFormPage):
    """Language Form page object """

    # english_title_locator = "Language"
    # french_title_locator = "Langue"
    english_title_locator = (AppiumBy.NAME, "Language") 
    french_title_locator = (AppiumBy.NAME, "Langue") 

    english_button_locator = (AppiumBy.ID, "com.ariesbifold:id/en") 
    french_button_locator = (AppiumBy.ID, "com.ariesbifold:id/fr") 

    def get_title(self, language):
        return super().get_title(self, language)

    def on_this_page(self):
        return super().on_this_page()
          
  
    def select_language(self, language):
        if self.on_this_page():
            if language == 'English':
                self.find_by(self.english_button_locator).click()
            elif language == 'French':
                self.find_by(self.french_button_locator).click()
        else:
            raise Exception(f"App not on the {type(self)} page")
            
    def get_current_language(self):
        if self.is_displayed(self.english_title_locator):
            return "English"
        elif self.is_displayed(self.french_title_locator):
            return "French"
        else:
            raise Exception(f"Unable to determine the current language on the {type(self)} page")
 
    def is_displayed(self, locator):
        try:
            element = self.find_by(locator)
            return element.is_displayed()
        except Exception:
            return False