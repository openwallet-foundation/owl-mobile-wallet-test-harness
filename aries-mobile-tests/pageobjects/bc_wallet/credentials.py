import time
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pageobjects.basepage import BasePage


# These classes can inherit from a BasePage to do common setup and functions
class CredentialsPage(BasePage):
    """Credentials page object"""

    # Locators
    on_this_page_text_locator = (MobileBy.ACCESSIBILITY_ID, "Credentials")

    # this is the one that contains all the text for that particular credential
    credential_locator = (MobileBy.ID, "com.ariesbifold:id/CredentialCard")
    
    #avatar_locator = (MobileBy.ID, "com.ariesbifold:id/AvatarName")
    credential_name_locator = (MobileBy.ID, "com.ariesbifold:id/CredentialHeader")
    #credential_version_locator = (MobileBy.ID, "com.ariesbifold:id/CredentialVersion")
    credential_issued_date_locator = (MobileBy.ID, "com.ariesbifold:id/CredentialFooter")

    def on_this_page(self):

        return super().on_this_page(self.credential_locator)

    def get_credentials(self):
        if self.on_this_page():
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
            #return CredentialDetailsPage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")

    def credential_exists(self, cred_name):
        return cred_name in self.driver.page_source