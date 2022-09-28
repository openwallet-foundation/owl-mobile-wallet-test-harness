from PIL import Image
from agent_factory.candy_uvp.pageobjects.webbasepage import WebBasePage
from selenium.webdriver.common.by import By
import base64
#from candy_uvp.pageobjects.connect_with_issuer_page import ConnectWithIssuerPage

# These classes can inherit from a BasePage to do commone setup and functions
class ConnectWithIssuerPage(WebBasePage):
    """CANdy UVP Issuer Connect with Issuer page object"""

    # Locators
    on_this_page_text_locator = "Connect with Issuer"
    qr_code_locator = (By.XPATH, '//*[@id="app"]/div/main/div/div/div/img')


    def on_this_page(self):   
        return super().on_this_page(self.on_this_page_text_locator) 

    def get_qr_code(self):
        if self.on_this_page():
            qrcode_element = self.find_by(self.qr_code_locator)
            self.driver.save_screenshot("qrcode.png")
            #qrcode = Image.open("qrcode.png")
            qrcode = base64.b64encode(open("qrcode.png", "rb").read())
            return qrcode.decode('utf-8')
            
        else:
            raise Exception(f"App not on the {type(self)} page")
