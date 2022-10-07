from agent_factory.candy_uvp.pageobjects.webbasepage import WebBasePage
from selenium.webdriver.common.by import By
from pageobjects.bc_wallet.holder_get_invite_interface.pageobjects.connect_with_issuer_page import ConnectWithIssuerPage

# These classes can inherit from a BasePage to do commone setup and functions
class BCVCInvitationReviewPage(WebBasePage):
    """CANdy UVP Issuer Review and Confirm page object"""

    # Locators
    on_this_page_text_locator = "Review and Confirm"
    #i_agree_locator = (By.XPATH, '//*[@id="app"]/div/main/div/div/div/div[2]/div[1]/div/div/div/div[1]/div/div')
    i_confirm_locator = (By.XPATH, '//*[@id="app"]/div/main/div/div/div/div[3]/div[1]/div[2]/div/div/div[1]/div/div')
    #self.find_by((By.XPATH, '//*[@id="app"]/div/main/div/div/div/div[2]/div[1]/div/div/div/div[1]/div/div')).click()

    proceed_locator = (By.XPATH, '//*[@id="app"]/div/main/div/div/div/div[3]/div[2]/div[2]/a')
    #//*[@id="app"]/div/main/div/div/div/div[2]/div[2]/div/a
    #/html/body/div/div/main/div/div/div/div[2]/div[2]/div/a


    def on_this_page(self):    
        return super().on_this_page(self.on_this_page_text_locator) 

    def i_confirm(self):
        if self.on_this_page():
            self.find_by(self.i_confirm_locator).click()
            return True
        else:
            raise Exception(f"App not on the {type(self)} page")


    def proceed(self):
        if self.on_this_page():
            self.find_by(self.proceed_locator).click()
            return ConnectWithIssuerPage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")
