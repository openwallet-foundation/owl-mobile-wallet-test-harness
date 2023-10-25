from agent_factory.candy_uvp.pageobjects.webbasepage import WebBasePage
from selenium.webdriver.common.by import By
from agent_factory.bc_vp.pageobjects.invite_page import InvitePage

# These classes can inherit from a BasePage to do commone setup and functions


class InvitesPage(WebBasePage):
    """BC VP Issuer Invites page object"""

    # Locators
    on_this_page_text_locator = "Invites"
    #new_invite_locator = (By.CLASS_NAME, "v-btn__content")
    new_invite_locator = (
        By.XPATH, '//*[@id="app"]/div/main/div/div/div/div/header/div/a')
    #search_locator = (By.CLASS_NAME, "v-input--selection-controls__ripple")
    search_locator = (By.XPATH, "(//input[@type='text'])[1]")
    row_locator = (By.CLASS_NAME, "v-input--selection-controls__ripple")
    edit_invite_locator = (By.XPATH, "(//button[@type='button'])[2]")
    credential_has_been_issued_locator = (By.XPATH, "(//div[@class='v-input--selection-controls__ripple'])[1]")
    save_locator = (By.XPATH, "//button[@class='v-btn v-btn--outlined theme--light v-size--default success--text']")
    #invitation_url_locator = (By.XPATH, '(//a[contains(text(),'https://bcvcpilot-issuer-test.apps.silver.devops.gov.bc.ca')])[1]')
    invitation_url_locator = (By.PARTIAL_LINK_TEXT, 'https://bcvcpilot-issuer-test.apps.silver.devops.gov.bc.ca')

    def on_this_page(self):
        return super().on_this_page(self.on_this_page_text_locator, timeout=1000)

    def search(self, search_term: str):
        if self.on_this_page():
            self.find_by(self.search_locator).send_keys(search_term)
            return True
        else:
            raise Exception(f"App not on the {type(self)} page")

    def new_invite(self):
        if self.on_this_page():
            self.find_by(self.new_invite_locator).click()
            return InvitePage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")

    def uncheck_issued(self):
        checkbox = self.find_by(self.credential_has_been_issued_locator)
    
        if checkbox.is_selected():
            checkbox.click()
            if checkbox.is_selected():
                raise Exception("Could not uncheck the 'Credential has been issued' checkbox")
        
        return True

    def save_invite(self):
        self.find_by(self.save_locator).click()
        return True

    def select_edit_invite(self, row: int):
        self.find_by(self.edit_invite_locator).click()
        return True

    def get_invitation_url(self):
        return self.find_by(self.invitation_url_locator).text