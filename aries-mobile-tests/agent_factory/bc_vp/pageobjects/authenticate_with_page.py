from agent_factory.candy_uvp.pageobjects.webbasepage import WebBasePage
from selenium.webdriver.common.by import By
from agent_factory.bc_vp.pageobjects.authenticate_page import AuthenticatePage
from agent_factory.bc_vp.pageobjects.invites_page import InvitesPage

# These classes can inherit from a BasePage to do commone setup and functions
class AuthenticateWithPage(WebBasePage):
    """BC VP Issuer Authenticate With page object"""

    # Locators
    #on_this_page_text_locator = "Authenticate with"
    on_this_page_text_locator = "Sign in to your account"
    idir_locator = (By.ID, 'social-idir')
    github_locator = (By.ID, 'social-github')
    username_locator = (By.ID, 'username')
    password_locator = (By.ID, 'password')
    sign_in_locator = (By.ID, 'kc-login')

    def on_this_page(self):   
        return super().on_this_page(self.on_this_page_text_locator, timeout=1000) 

    def github(self):
        if self.on_this_page():
            self.find_by(self.github_locator).click()
            return AuthenticatePage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")

    def enter_username(self, username):
        if self.on_this_page():
            self.find_by(self.username_locator).send_keys(username)
            return True
        else:
            raise Exception(f"App not on the {type(self)} page")
    
    def enter_password(self, password):
        if self.on_this_page():
            self.find_by(self.password_locator).send_keys(password)
            return True
        else:
            raise Exception(f"App not on the {type(self)} page")

    def sign_in(self):
        if self.on_this_page():
            self.find_by(self.sign_in_locator).click()
            return InvitesPage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")