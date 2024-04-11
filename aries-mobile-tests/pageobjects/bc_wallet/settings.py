import time

from appium.webdriver.common.appiumby import AppiumBy
from pageobjects.basepage import BasePage, WaitCondition
from pageobjects.bc_wallet.change_pin import ChangePINPage
from pageobjects.bc_wallet.contacts import ContactsPage
from pageobjects.bc_wallet.developer_settings import DeveloperSettingsPage
from pageobjects.bc_wallet.languageform import LanguageFormPage
from pageobjects.bc_wallet.scan_my_qr_code import ScanMyQRCodePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class SettingsPage(BasePage):
    """Settings page object"""

    # Locators
    on_this_page_text_locator = "App Settings"
    on_this_page_locator = (AppiumBy.NAME, "App Settings")
    back_locator = (AppiumBy.ID, "com.ariesbifold:id/Back")
    contacts_locator = (AppiumBy.ID, "com.ariesbifold:id/Contacts")
    language_locator = (AppiumBy.ID, "com.ariesbifold:id/Language")
    contacts_aid_locator = (AppiumBy.ACCESSIBILITY_ID, "Contacts")
    version_locator = (AppiumBy.ID, "com.ariesbifold:id/Version")
    version_partial_aid_locator = (AppiumBy.ACCESSIBILITY_ID, "Version")
    intro_aid_locator = (AppiumBy.ACCESSIBILITY_ID, "Introduction to the app")
    intro_locator = (AppiumBy.ID, "com.ariesbifold:id/IntroductionToTheApp")
    developer_locator = (AppiumBy.ID, "com.ariesbifold:id/DeveloperOptions")
    # change_pin_locator = (AppiumBy.ID, "com.ariesbifold:id/ChangePIN")
    change_pin_locator = (AppiumBy.ACCESSIBILITY_ID, "Change PIN")
    edit_wallet_name_locator = (AppiumBy.ID, "com.ariesbifold:id/EditWalletName")
    wallet_name_locator = (AppiumBy.ID, "com.ariesbifold:id/WalletName")
    scan_my_qr_code_locator = (AppiumBy.ID, "com.ariesbifold:id/ScanMyQR")

    def on_this_page(self):
        if self.current_platform.lower() == "Android".lower():
            return super().on_this_page(self.on_this_page_text_locator)
        return super().on_this_page(self.on_this_page_locator)

    def select_language(self):
        if self.on_this_page():
            self.find_by(self.language_locator).click()
            return LanguageFormPage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")

    def enable_developer_mode(self):
        # TODO check if Developer Mode is already enabled

        # Check if the app is on the correct page
        if not self.on_this_page():
            raise Exception(f"App not on the {type(self)} page")

        # if self.current_platform == "iOS":
        #     self.scroll_to_element(self.version_locator)
        # else:
        self.scroll_to_bottom()

        if (
            self.current_platform == "iOS"
            and self.driver.capabilities["platformVersion"] <= "15"
        ):
            # Need to find the element py partial text or accessibility id for iOS 14 and lower
            version_elements = self.driver.find_elements(
                AppiumBy.XPATH,
                "//*[contains(@label, '{}')]".format(
                    self.version_partial_aid_locator[1]
                ),
            )
            # take the last one on the page
            version_element = version_elements[len(version_elements) - 1]
        else:
            # this works for iOS 15+ and Android only
            version_element = self.find_by(self.version_locator)

        # Click the version element 10 times to enable Developer Mode
        for i in range(10):
            version_element.click()

        # TODO: check if Developer Mode is now enabled

    def select_developer(self):
        # if self.on_this_page():
        self.find_by(self.developer_locator).click()

        return DeveloperSettingsPage(self.driver)
        # else:
        #     raise Exception(f"App not on the {type(self)} page")

    def select_change_pin(self):
        self.find_by(self.change_pin_locator).click()

        return ChangePINPage(self.driver)

    def select_edit_wallet_name(self):
        # we need to scroll up to the top of the page to see the Edit Wallet Name button

        # self.scroll_to_element(self.edit_wallet_name_aid_locator[1], direction='up')
        # self.scroll_to_top()
        self.find_by(
            self.edit_wallet_name_locator,
            wait_condition=WaitCondition.ELEMENT_TO_BE_CLICKABLE,
        ).click()

        # return a new page object for the Edit Wallet Name page
        from pageobjects.bc_wallet.name_your_wallet import NameYourWalletPage

        return NameYourWalletPage(self.driver, calling_page=self)

    def get_wallet_name(self):
        return self.find_by(self.wallet_name_locator).text

    def select_scan_my_qr_code(self):
        self.find_by(self.scan_my_qr_code_locator).click()

        # return a new page object for the Scan My QR Code page
        return ScanMyQRCodePage(self.driver)

    def select_back(self):
        # Don't check if on this page becasue android (unless you scroll back to the top) can't see the App Settings accessibility ID
        # if self.on_this_page():
        self.find_by(self.back_locator).click()
        from pageobjects.bc_wallet.home import HomePage

        return HomePage(self.driver)
        # else:
        #     raise Exception(f"App not on the {type(self)} page")

    def select_notification(self, context):
        search_element = WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located(
                (AppiumBy.ACCESSIBILITY_ID, "Search Wikipedia")
            )
        )
        search_element.click()
        search_input = WebDriverWait(context.driver, 30).until(
            EC.element_to_be_clickable(
                (AppiumBy.ID, "org.wikipedia.alpha:id/search_src_text")
            )
        )
        search_input.send_keys(keyword)
        time.sleep(5)

    def select_contacts(self):
        if self.on_this_page():
            self.find_by(self.contacts_locator).click()

            # return a new page object for the Contacts page
            return ContactsPage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)}")

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
