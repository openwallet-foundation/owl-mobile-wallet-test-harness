import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pageobjects.basepage import BasePage
from pageobjects.basepage import WaitCondition
from pageobjects.bc_wallet.edit_wallet_name import EditWalletNamePage



class ScanMyQRCodePage(BasePage):
    """Settings page object"""

    # Locators
    on_this_page_text_locator = "My QR code"
    back_locator = (AppiumBy.ID, "com.ariesbifold:id/Back")
    edit_wallet_name_locator = (AppiumBy.ID, "com.ariesbifold:id/EditWalletName")
    scan_qr_code_locator = (AppiumBy.ID, "com.ariesbifold:id/ScanQRCode")
    my_qr_code_locator = (AppiumBy.ID, "com.ariesbifold:id/MyQRCode")
    qr_code_locator = (AppiumBy.ID, "com.ariesbifold:id/QRCode")

    def on_this_page(self):     
        return super().on_this_page(self.on_this_page_text_locator) 


    def select_edit_wallet_name(self):
        self.find_by(self.edit_wallet_name_locator).click()

        # return a new page object for the Edit Wallet Name page
        return EditWalletNamePage(self.driver, calling_page=self)
    

    def select_scan_qr_code(self):
        self.find_by(self.scan_qr_code_locator).click()
    

    def select_back(self):
        # Don't check if on this page becasue android (unless you scroll back to the top) can't see the App Settings accessibility ID
        # if self.on_this_page():
        self.find_by(self.back_locator).click()
        from pageobjects.bc_wallet.home import HomePage
        return HomePage(self.driver)
        # else:
        #     raise Exception(f"App not on the {type(self)} page")


    def get_my_qr_code(self):
        # get the QR code image from the page
        qr_code = self.find_by(self.qr_code_locator)
        # return the QR code image
        return qr_code
    
    def select_my_qr_code(self):
        self.find_by(self.my_qr_code_locator).click()

