import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pageobjects.basepage import BasePage
from pageobjects.bc_wallet.credential_details import CredentialDetailsPage


# These classes can inherit from a BasePage to do common setup and functions
class CredentialsPage(BasePage):
    """Credentials page object"""

    # Locators
    on_this_page_text_locator = (AppiumBy.ACCESSIBILITY_ID, "Credentials")

    # this is the one that contains all the text for that particular credential
    credential_locator = (AppiumBy.ID, "com.ariesbifold:id/CredentialCard")
    
    #avatar_locator = (MobileBy.ID, "com.ariesbifold:id/AvatarName")
    # get credential name from CredentialCardHeader on iOS for AATH and BC UVP creds
    #credential_card_header_locator = (MobileBy.ID, "com.ariesbifold:id/CredentialCardHeader")
    #BCSC seems to have a differnt TestID
    credential_card_header_locator = (AppiumBy.ID, "com.ariesbifold:id/CredentialCard")
    # get credential name from CredentialName on Android
    credential_name_locator = (AppiumBy.ID, "com.ariesbifold:id/CredentialName")
    #credential_version_locator = (MobileBy.ID, "com.ariesbifold:id/CredentialVersion")
    credential_issued_date_locator = (AppiumBy.ID, "com.ariesbifold:id/CredentialCardFooter")

    def on_this_page(self):
        # TODO for iOS we are not getting testIDs for AATH creds. Use accessibilty ID for iOS instead.
        if self.driver.capabilities['platformName'] == 'iOS':
            return super().on_this_page(self.on_this_page_text_locator)
        else:
            return super().on_this_page(self.credential_locator)

    def get_credentials(self):
        if self.on_this_page():
            if self.current_platform == "iOS":
                elems = self.find_multiple_by(self.credential_card_header_locator)
            else:
                elems = self.find_multiple_by(self.credential_name_locator)
            json_elems = {
                "credentials": [
                ],
            }
            for elem in elems:
                json_elems["credentials"].append({"text":elem.text})
            return json_elems
        else:
            raise Exception(f"App not on the {type(self)} page")

    def get_top_credential(self):
        if self.on_this_page():
            json_elems = self.get_credentials()
            return json_elems["credentials"][0]
        else:
            raise Exception(f"App not on the {type(self)} page")

    def select_top_credential(self):
        if self.on_this_page():
            self.find_multiple_by(self.credential_locator)[0].click()
            return CredentialDetailsPage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")

    def credential_exists(self, cred_name):
        return cred_name in self.driver.page_source