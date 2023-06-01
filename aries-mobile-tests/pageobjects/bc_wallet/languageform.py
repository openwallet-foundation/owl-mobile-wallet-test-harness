from pageobjects.basepage import BasePage
from appium.webdriver.common.appiumby import AppiumBy

# These classes can inherit from a BasePage to do common setup and functions
class LanguageFormPage(BasePage):
    """Language Form page object """

    english_title_locator = "Language"
    french_title_locator = "Langue"
    english_button_locator = (AppiumBy.ID, "com.ariesbifold:id/en")
    french_button_locator = (AppiumBy.ID, "com.ariesbifold:id/fr")

    def get_title(self, language):
        if language == 'English':
            return super().on_this_page(self.english_title_locator)
        else:
            return super().on_this_page(self.french_title_locator)

    def on_this_page(self):
        if super().on_this_page(self.english_title_locator) or super().on_this_page(self.french_title_locator):
            return True
        else:
            return False

    def select_language(self, language):
        if self.on_this_page():
            if language == 'English':
                self.find_by(self.english_button_locator).click()
            elif language == 'French':
                self.find_by(self.french_button_locator).click()
        else:
            raise Exception(f"App not on the {type(self)} page")

