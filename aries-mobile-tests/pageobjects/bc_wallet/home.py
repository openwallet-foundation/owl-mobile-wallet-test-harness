import time
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pageobjects.basepage import BasePage
from pageobjects.bc_wallet.contacts import ContactsPage
from pageobjects.bc_wallet.connecting import ConnectingPage
from pageobjects.bc_wallet.settings import SettingsPage
from pageobjects.bc_wallet.credential_offer import CredentialOfferPage
from time import sleep


class HomePage(BasePage):
    """Home page object"""

    # Locators
    on_this_page_text_locator = "Welcome"
    on_this_page_notification_locator = "New Credential Offer"
    view_notification_button_locator = "View"
    home_locator = "Home"
    scan_locator = "Scan"
    credentials_locator = "Credentials"
    settings_locator = "Settings"
    contacts_locator = "Contacts"

    def on_this_page(self):
        #print(self.driver.page_source)
        return super().on_this_page(self.on_this_page_text_locator)

    def select_credential_offer_notification(self):
        if super().on_this_page(self.on_this_page_notification_locator):
            sleep(20)
            print(self.driver.page_source)
            # if self.current_platform == "iOS":
            self.find_by_accessibility_id(self.view_notification_button_locator).click()
            # else:
            #     self.find_by_element_id(self.view_notification_button_locator).click()

            # return a new page objectfor the Contacts page
            return CredentialOfferPage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)}")

    def select_contacts(self):
        if self.on_this_page():
            self.find_by_accessibility_id(self.contacts_locator).click()

            # return a new page objectfor the Contacts page
            return ContactsPage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)}")
        # return ContactsPage

    def inject_connection_invite_qr_code(self, image):
        # Read the file from your project and transform it to a base64 string
        # const qrCodeImage = readFileSync(join(process.cwd(), 'assets/qr-code.png'), 'base64');

        # Provide the base64 string image to the device
        self.driver.execute_script(f"sauce:inject-image={image}")

    def select_scan(self):
        if self.on_this_page():
            # Inject image
            self.find_by_accessibility_id(self.scan_locator).click()

            # return a new page object? The scan page.
            return ConnectingPage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")

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
