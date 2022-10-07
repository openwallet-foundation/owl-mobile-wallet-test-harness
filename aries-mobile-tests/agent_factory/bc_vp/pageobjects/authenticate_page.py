from PIL import Image
from agent_factory.candy_uvp.pageobjects.webbasepage import WebBasePage
from selenium.webdriver.common.by import By
from agent_factory.bc_vp.pageobjects.invites_page import InvitesPage

# These classes can inherit from a BasePage to do commone setup and functions
class AuthenticatePage(WebBasePage):
    """BC VP Issuer GitHub Authenticate page object"""

    # Locators
    on_this_page_text_locator = "Sign in to GitHub"
    username_locator = (By.ID, 'login_field')
    password_locator = (By.ID, 'password')
    #sign_in_locator = (By.CLASS_NAME, 'btn btn-primary btn-block js-sign-in-button')
    sign_in_locator = (By.XPATH, '//*[@id="login"]/div[3]/form/div/input[11]')

    def on_this_page(self):     
        return super().on_this_page(self.on_this_page_text_locator) 

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