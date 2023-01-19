from agent_factory.candy_uvp.pageobjects.webbasepage import WebBasePage
from selenium.webdriver.common.by import By
from pageobjects.basepage import WaitCondition
from agent_factory.candy_uvp.pageobjects.request_credential_page import RequestCredentialPage

# These classes can inherit from a BasePage to do commone setup and functions
class TermsOfServicePage(WebBasePage):
    """CANdy UVP Issuer Terms of Service page object"""

    # Locators
    on_this_page_text_locator = "Terms of Service"
    on_this_page_locator = (By.XPATH, '//*[@id="app"]/div/main/div/div/div/div[1]/div/div/h3[1]/strong')
    i_agree_locator = (By.CLASS_NAME, 'v-input--selection-controls__ripple')
    agree_button_locator = (By.CLASS_NAME, "v-btn__content")


    def on_this_page(self):   
        return super().on_this_page(self.on_this_page_locator, timeout=20)    
        #return super().on_this_page(self.on_this_page_text_locator, timeout=20) 

    def select_i_agree(self):
        if self.on_this_page():
            self.find_by(self.i_agree_locator).click()
            return True
        else:
            raise Exception(f"App not on the {type(self)} page")


    def agree(self):
        if self.on_this_page():
            self.find_by(self.agree_button_locator, wait_condition=WaitCondition.ELEMENT_TO_BE_CLICKABLE).click()

            # Maybe should check if it is checked or let the test call is_accept_checked()? 
            # return a new page object? The Pin Setup page.
            return RequestCredentialPage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")
