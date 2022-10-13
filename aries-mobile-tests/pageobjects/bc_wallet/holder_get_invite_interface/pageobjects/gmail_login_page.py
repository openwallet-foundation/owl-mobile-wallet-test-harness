from agent_factory.candy_uvp.pageobjects.webbasepage import WebBasePage
from selenium.webdriver.common.by import By
from pageobjects.bc_wallet.holder_get_invite_interface.pageobjects.gmail_email_page import GmailEmailPage

# These classes can inherit from a BasePage to do commone setup and functions
class GmailLoginPage(WebBasePage):
    """BC VP Holder Gmail Authenticate page object"""

    # Locators
    on_this_page_text_locator = "Sign in"
    username_locator = (By.ID, 'identifierId')
    #next_locator = (By.XPATH, '//*[@id="identifierNext"]/div/button/div[3]')
    next_locator = (By.ID, 'identifierNext')
    #//*[@id="identifierId"]
    #password_locator = (By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input')
    password_locator = (By.XPATH, ' //input[@name="Passwd"]')
    #//input[@name='Passwd']
    #input[name='Passwd']
    password_next_locator = (By.ID, 'passwordNext')
    #password_next_locator = (By.XPATH, '//*[@id="passwordNext"]/div/button/div[3]')
    

    def on_this_page(self):     
        return super().on_this_page(self.on_this_page_text_locator) 

    def enter_username(self, username):
        if self.on_this_page():
            self.find_by(self.username_locator).send_keys(username)
            return True
        else:
            raise Exception(f"App not on the {type(self)} page")
    
    def enter_password(self, password):
        if super().on_this_page("Enter your password", timeout=5000) :
            self.driver.implicitly_wait(10)
            self.find_by(self.password_locator).send_keys(password)
            return True
        else:
            raise Exception(f"App not on the {type(self)} page")

    def next(self):
        if self.on_this_page():
            self.find_by(self.next_locator).click()
            #return InvitesPage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")

    def sign_in(self):
        if super().on_this_page("Welcome"):
            self.find_by(self.password_next_locator).click()
            return GmailEmailPage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")