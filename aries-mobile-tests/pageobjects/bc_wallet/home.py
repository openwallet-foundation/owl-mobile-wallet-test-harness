from appium.webdriver.common.appiumby import AppiumBy
from pageobjects.basepage import BasePage
from pageobjects.bc_wallet.connecting import ConnectingPage
from pageobjects.bc_wallet.settings import SettingsPage
from pageobjects.bc_wallet.credential_offer import CredentialOfferPage
from pageobjects.bc_wallet.proof_request import ProofRequestPage
from time import sleep


class HomePage(BasePage):
    """Home page object"""

    # Locators
    on_this_page_text_locator = "Home"
    on_this_page_notification_locator = "New Credential Offer"
    on_this_page_proof_notification_locator = "New Proof Request"
    view_notification_button_locator = (AppiumBy.ID, "com.ariesbifold:id/View")
    home_locator = "Home"
    scan_locator = "Scan"
    credentials_locator = "Credentials"
    settings_tid_locator = "com.ariesbifold:id/Settings"
    get_bc_digital_id_locator = (AppiumBy.ID, "com.ariesbifold:id/GetBCID")

    def on_this_page(self):
        return super().on_this_page(self.on_this_page_text_locator)

    def select_credential_offer_notification(self):
        if super().on_this_page(self.on_this_page_notification_locator):
            #sleep(20)
            self.find_by(self.view_notification_button_locator).click()
            # if self.current_platform == "iOS":
            #     self.find_by_accessibility_id(self.view_notification_button_locator).click()
            # else:
            #     self.find_by_element_id(self.view_notification_button_locator).click()

            # return a new page objectfor the Contacts page
            return CredentialOfferPage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)}")

    def select_proof_request_notification(self):
        if super().on_this_page(self.on_this_page_proof_notification_locator):
            sleep(20)
            #print(self.driver.page_source)
            # if self.current_platform == "iOS":
            self.find_by(self.view_notification_button_locator).click()
            #self.find_by_accessibility_id(self.view_notification_button_locator).click()
            # else:
            #     self.find_by_element_id(self.view_notification_button_locator).click()

            # return a new page objectfor the Contacts page
            return ProofRequestPage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)}")


    def select_scan(self):
        # if self.on_this_page():

        self.find_by_accessibility_id(self.scan_locator).click()

        # return a new page object? The scan page.
        return ConnectingPage(self.driver)

        # else:
        #     raise Exception(f"App not on the {type(self)} page")

    def select_get_bc_digital_id(self):
        if self.on_this_page():
            self.find_by(self.get_bc_digital_id_locator).click()
            return True
        else:
            raise Exception(f"App not on the {type(self)} page")

    def select_settings(self):
        if self.on_this_page():
            self.find_by_element_id(self.settings_tid_locator).click()

            # return a new page object for the settings page
            return SettingsPage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")
