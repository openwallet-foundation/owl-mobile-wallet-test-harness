from agent_factory.candy_uvp.pageobjects.webbasepage import WebBasePage
from selenium.webdriver.common.by import By
from pageobjects.bc_wallet.holder_get_invite_interface.pageobjects.bc_vc_invitation_request_credential_page import BCVCInvitationRequestCredentialPage

# These classes can inherit from a BasePage to do commone setup and functions
class BCVCInvitationAgreePage(WebBasePage):
    """CANdy UVP Issuer Review and Confirm page object"""

    # Locators
    on_this_page_text_locator = "Person credential invitation"
    #i_agree_locator = (By.XPATH, '//*[@id="app"]/div/main/div/div/div/div[2]/div[1]/div/div/div/div[1]/div/div')
    i_agree_locator = (By.XPATH, '//div[@class="v-input--selection-controls__ripple"]')

    #agree_locator = (By.XPATH, '//*[@id="app"]/div/main/div/div/div/div[2]/div[2]/div/a')
    agree_locator = (By.XPATH, '//a[@class="v-btn v-btn--outlined v-btn--router theme--light v-size--default success--text"]')


    def on_this_page(self):    
        return super().on_this_page(self.on_this_page_text_locator, timeout=1000) 

    def i_agree(self):
        if self.on_this_page():
            self.find_by(self.i_agree_locator).click()
            return True
        else:
            raise Exception(f"App not on the {type(self)} page")


    def agree(self):
        if self.on_this_page():
            self.find_by(self.agree_locator).click()
            return BCVCInvitationRequestCredentialPage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")
