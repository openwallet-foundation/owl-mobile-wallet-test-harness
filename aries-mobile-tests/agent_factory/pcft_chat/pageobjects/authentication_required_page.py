from PIL import Image
from agent_factory.candy_uvp.pageobjects.webbasepage import WebBasePage
from selenium.webdriver.common.by import By
import base64
#from candy_uvp.pageobjects.connect_with_issuer_page import ConnectWithIssuerPage

# These classes can inherit from a BasePage to do commone setup and functions
class AuthenticationRequiredPage(WebBasePage):
    """PCFT Chat Authentication Required page object"""

    # Locators
    on_this_page_text_locator = "Please provide your Verifiable Credentials"
    qr_code_locator = (By.XPATH, '//*[@id="app"]/div/div/div/div/div/canvas')


    def on_this_page(self):       
        return super().on_this_page(self.on_this_page_text_locator) 

    def get_qr_code(self):
        if self.on_this_page():
            self.driver.save_screenshot("qrcode.png")
            qrcode = base64.b64encode(open("qrcode.png", "rb").read())
            return qrcode.decode('utf-8')
        else:
            raise Exception(f"App not on the {type(self)} page")
