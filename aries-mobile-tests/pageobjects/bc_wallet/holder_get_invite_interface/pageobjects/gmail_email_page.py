from agent_factory.candy_uvp.pageobjects.webbasepage import WebBasePage
from selenium.webdriver.common.by import By
import re
#from agent_factory.bc_vp.pageobjects.invite_page import InvitePage
from pageobjects.basepage import WaitCondition
from pageobjects.bc_wallet.holder_get_invite_interface.pageobjects.bc_vc_invitation_agree_page import BCVCInvitationAgreePage

# These classes can inherit from a BasePage to do commone setup and functions


class GmailEmailPage(WebBasePage):
    """BC VP Holder email page object"""

    # Locators
    on_this_page_text_locator = "Primary"
    latest_email_locator = (By.ID, ":24")
    delete_locator = (By.XPATH, "//div[@aria-label='Delete']//div[@class='asa']")
    # auth code email locator - //body[1]/div[7]/div[3]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[8]/div[1]/div[1]/div[2]/div[1]/table[1]/tbody[1]/tr[1]/td[5]/div[1]/div[1]/div[1]/span[1]/span[1]
    auth_code_body_text_locator = (By.XPATH, "//div[contains(text(),'Verification code')]")
    # <span class="bqe" data-thread-id="#thread-f:1745870413865589327" data-legacy-thread-id="183a93e432529a4f" data-legacy-last-message-id="183aa57ef028fb34" data-legacy-last-non-draft-message-id="183aa57ef028fb34">Invite from BC VC Pilot Issuer TEST</span>
    #//*[@id=":24"]
    #//*[@id=":2b"]
    #//*[@id=":2c"]/span
    #invitation_link_locator = (By.XPATH, '//*[@id=":8r"]/p/b/a')
    
    invitation_link_locator = (By.XPATH, "//a[contains(@href, 'https://bcvcpilot-issuer-test.apps.silver.devops.gov.bc.ca/?invite_token=')]")
    #//*[@id=":8s"]/p/b/a
    #https://bcvcpilot-issuer-test.apps.silver.devops.gov.bc.ca/?invite_token=e2ab167c-a0d6-4eb3-bc40-f4a3c61a750e

    def on_this_page(self):
        return super().on_this_page(self.on_this_page_text_locator, timeout=1000)

    def select_invitation_link(self):
        #if self.on_this_page():
        if super().on_this_page(self.invitation_link_locator, timeout=2000):
            self.find_by(self.invitation_link_locator, wait_condition=WaitCondition.VISIBILITY_OF_ELEMENT_LOCATED).click()
            return BCVCInvitationAgreePage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")

    def open_latest_email(self):
        if self.on_this_page():
            self.find_by(self.latest_email_locator, timeout=50).click()
            #return InvitePage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")

    def get_auth_code(self):
        #if self.on_this_page():
        if super().on_this_page(self.auth_code_body_text_locator, timeout=1000):
            email_body = self.find_by(self.auth_code_body_text_locator).text
            auth_code = re.sub("\D", "", email_body)
            return auth_code
        else:
            raise Exception(f"App not on the {type(self)} page")

    
    def delete_opened_email(self):
        self.find_by(self.delete_locator, 50).click()

