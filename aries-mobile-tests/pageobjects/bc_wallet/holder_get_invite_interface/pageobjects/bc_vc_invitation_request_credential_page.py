from agent_factory.candy_uvp.pageobjects.webbasepage import WebBasePage
from selenium.webdriver.common.by import By
from pageobjects.bc_wallet.holder_get_invite_interface.pageobjects.bc_vc_invitation_review_page import BCVCInvitationReviewPage

# These classes can inherit from a BasePage to do commone setup and functions
class BCVCInvitationRequestCredentialPage(WebBasePage):
    """CANdy UVP Issuer Review and Confirm page object"""

    # Locators
    on_this_page_text_locator = "Request Credential"
    #i_agree_locator = (By.XPATH, '//*[@id="app"]/div/main/div/div/div/div[2]/div[1]/div/div/div/div[1]/div/div')

    request_credential_locator = (By.XPATH, '//*[@id="app"]/div/main/div/div/div/form/div[2]/div/div[2]/input[3]')
    #//*[@id="app"]/div/main/div/div/div/div[2]/div[2]/div/a
    #/html/body/div/div/main/div/div/div/div[2]/div[2]/div/a


    def on_this_page(self):    
        return super().on_this_page(self.on_this_page_text_locator) 

    def request_credential(self):
        if self.on_this_page():
            self.find_by(self.request_credential_locator).click()
            return BCVCInvitationReviewPage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")
