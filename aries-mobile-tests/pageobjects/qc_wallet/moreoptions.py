from appium.webdriver.common.appiumby import AppiumBy
from pageobjects.basepage import BasePage, WaitCondition
from pageobjects.qc_wallet.settings import SettingsPageQC
from pageobjects.qc_wallet.contacts import ContactsPageQC
from pageobjects.qc_wallet.help import HelpPageQC
from pageobjects.qc_wallet.about import AboutPageQC

class MoreOptionsPageQC(BasePage):
    """more options page object"""

    #Locators
    on_this_page_text_locator = "More Options"
    application_settings_locator = (AppiumBy.ID, "com.ariesbifold:id/AppParams")
    contacts_locator = (AppiumBy.ID, "com.ariesbifold:id/AppContacts")
    help_locator = (AppiumBy.ID, "com.ariesbifold:id/HelpCenter")
    about_locator = (AppiumBy.ID, "com.ariesbifold:id/About")

    def on_this_page(self):
        return super().on_this_page(self.on_this_page_text_locator)

    def select_applicationSettings(self):
        if self.on_this_page():
            self.find_by(self.application_settings_locator).click()

            # return a new page object for the settings page
            return SettingsPageQC(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")


    def select_contacts(self):
        if self.on_this_page():
            self.find_by(self.contacts_locator).click()
            return ContactsPageQC(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")
        
    def select_help(self):
        if self.on_this_page():
            self.find_by(self.help_locator, wait_condition=WaitCondition.ELEMENT_TO_BE_CLICKABLE,).click()
            return HelpPageQC(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")
               
    def select_about(self):
        if self.on_this_page():
            self.find_by(self.about_locator).click()
            return AboutPageQC(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")