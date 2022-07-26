import time
import os
import base64
import shutil
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pageobjects.basepage import BasePage
from pageobjects.bc_wallet.contacts import ContactsPage
from pageobjects.bc_wallet.connecting import ConnectingPage
from pageobjects.bc_wallet.settings import SettingsPage
from pageobjects.bc_wallet.credential_offer import CredentialOfferPage
from time import sleep


class NavBar(BasePage):
    """Nav Bar Footer object"""

    # Locators
    scan_locator = "Scan"
    credentials_locator = "Credentials"
    settings_locator = "Settings"
    contacts_locator = "Contacts"

    def select_contacts(self):
        if self.on_this_page():
            self.find_by_accessibility_id(self.contacts_locator).click()

            # return a new page objectfor the Contacts page
            return ContactsPage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)}")
        # return ContactsPage


    def select_scan(self):
        # if self.on_this_page():

        self.find_by_accessibility_id(self.scan_locator).click()

        # return a new page object? The scan page.
        return ConnectingPage(self.driver)
        
        # else:
        #     raise Exception(f"App not on the {type(self)} page")

    def select_credentials(self):

        return CredentialsPage

    def select_settings(self):
        if self.on_this_page():
            self.find_by_accessibility_id(self.settings_locator).click()

            # return a new page objectfor the settings page
            return SettingsPage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")
        # return SettingsPage
