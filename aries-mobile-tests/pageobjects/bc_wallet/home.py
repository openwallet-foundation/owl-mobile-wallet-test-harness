from appium.webdriver.common.appiumby import AppiumBy
from pageobjects.basepage import BasePage
from pageobjects.basepage import WaitCondition
from pageobjects.bc_wallet.connecting import ConnectingPage
from pageobjects.bc_wallet.settings import SettingsPage
from pageobjects.bc_wallet.credential_offer import CredentialOfferPage
from pageobjects.bc_wallet.proof_request import ProofRequestPage
from pageobjects.bc_wallet.get_person_credential import GetPersonCredentialPage
from pageobjects.bc_wallet.credential_details import CredentialDetailsPage
from pageobjects.bc_wallet.welcome_to_bc_wallet import WelcomeToBCWalletModal
from time import sleep


class HomePage(BasePage):
    """Home page object"""

    # Locators
    on_this_page_text_locator = "Home"
    on_this_page_notification_locator = "New Credential Offer"
    on_this_page_proof_notification_locator = "New Proof Request"
    on_this_page_revocation_notification_locator = "Credential revoked"
    view_notification_button_locator = (AppiumBy.ID, "com.ariesbifold:id/View")
    view_credential_offer_notification_button_locator = (AppiumBy.ID, "com.ariesbifold:id/ViewOffer")
    view_proof_notification_button_locator = (AppiumBy.ID, "com.ariesbifold:id/ViewProofRecord")
    view_revocation_notification_button_locator = (AppiumBy.ID, "com.ariesbifold:id/ViewRevocation")
    view_revocation_notification_button_aid_locator = (AppiumBy.ACCESSIBILITY_ID, "View")
    scan_locator = (AppiumBy.ID, "com.ariesbifold:id/Scan")
    credentials_locator = "Credentials"
    settings_tid_locator = "com.ariesbifold:id/Settings"
    settings_locator = (AppiumBy.ID, "com.ariesbifold:id/Settings")
    #get_bc_digital_id_locator = (AppiumBy.ID, "com.ariesbifold:id/GetBCID")
    get_bc_digital_id_locator = (AppiumBy.ID, "com.ariesbifold:id/ViewCustom")

    # Modals and Alerts for Home page
    welcome_to_bc_wallet_modal = WelcomeToBCWalletModal
    
    def __init__(self, driver):
        super().__init__(driver)
        self.welcome_to_bc_wallet_modal = WelcomeToBCWalletModal(driver)


    def on_this_page(self):
        return super().on_this_page(self.on_this_page_text_locator)


    def select_credential_offer_notification(self):
        if super().on_this_page(self.on_this_page_notification_locator):
            self.find_by(self.view_credential_offer_notification_button_locator, wait_condition=WaitCondition.ELEMENT_TO_BE_CLICKABLE).click()
            # if self.current_platform == "iOS":
            #     self.find_by_accessibility_id(self.view_notification_button_locator).click()
            # else:
            #     self.find_by_element_id(self.view_notification_button_locator).click()

            # return a new page objectfor the Contacts page
            return CredentialOfferPage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)}")


    def select_revocation_notification(self):
        if super().on_this_page(self.on_this_page_revocation_notification_locator, timeout=20):
            if self.current_platform == "iOS" and self.driver.capabilities['platformVersion'] <= '15':
                #self.find_by(self.view_revocation_notification_button_aid_locator, wait_condition=WaitCondition.ELEMENT_TO_BE_CLICKABLE).click()
                # Need to find the element py partial text or accessibility id for iOS 14 and lower
                view_notification_elements = self.driver.find_elements(AppiumBy.XPATH, "//*[contains(@label, '{}')]".format(self.view_revocation_notification_button_aid_locator[1]))
                # take the last one on the page
                view_notification_element = view_notification_elements[len(view_notification_elements)-5]
                view_notification_element.click()
            else:
                self.find_by(self.view_revocation_notification_button_locator, wait_condition=WaitCondition.ELEMENT_TO_BE_CLICKABLE).click()

            # return a new page object for the Revocation page
            return CredentialDetailsPage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)}")


    def is_revocation_notification_present(self) -> bool:
        return super().on_this_page(self.on_this_page_revocation_notification_locator)


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

        self.find_by(self.scan_locator).click()

        # return a new page object? The scan page.
        return ConnectingPage(self.driver)

        # else:
        #     raise Exception(f"App not on the {type(self)} page")

    def select_get_bc_digital_id(self):
        if self.on_this_page():
            self.find_by(self.get_bc_digital_id_locator).click()
            return GetPersonCredentialPage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")

    def select_settings(self):
        if self.on_this_page():
            self.find_by(self.settings_locator).click()

            # return a new page object for the settings page
            return SettingsPage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")
