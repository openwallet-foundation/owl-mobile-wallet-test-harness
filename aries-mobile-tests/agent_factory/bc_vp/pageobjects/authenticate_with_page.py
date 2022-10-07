from agent_factory.candy_uvp.pageobjects.webbasepage import WebBasePage
from selenium.webdriver.common.by import By
from agent_factory.bc_vp.pageobjects.authenticate_page import AuthenticatePage

# These classes can inherit from a BasePage to do commone setup and functions
class AuthenticateWithPage(WebBasePage):
    """BC VP Issuer Authenticate With page object"""

    # Locators
    on_this_page_text_locator = "Authenticate with"
    idir_locator = (By.ID, 'zocial-idir')
    github_locator = (By.ID, 'zocial-github')
    bc_service_card_locator = (By.ID, 'zocial-bcsc')
    verifiable_credential_locator = (By.ID, 'zocial-verifiable-credential')

    def on_this_page(self):   
        return super().on_this_page(self.on_this_page_text_locator, timeout=1000) 

    def github(self):
        if self.on_this_page():
            self.find_by(self.github_locator).click()
            return AuthenticatePage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")
