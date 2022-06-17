from agent_factory.candy_uvp.pageobjects.webbasepage import WebBasePage
from selenium.webdriver.common.by import By
from agent_factory.pcft_chat.pageobjects.enter_chat_page import EnterChatPage

# These classes can inherit from a BasePage to do commone setup and functions
class TermsOfServicePage(WebBasePage):
    """PCFT Chat Terms of Service page object"""

    # Locators
    on_this_page_text_locator = "Terms of Service"
    i_agree_locator = (By.ID, 'agree')
    agree_button_locator = (By.CLASS_NAME, "btn btn btn-outline-success")


    def on_this_page(self):   
        #print(self.driver.page_source)     
        return super().on_this_page(self.on_this_page_text_locator) 

    def select_i_agree(self):
        if self.on_this_page():
            self.find_by(self.i_agree_locator).click()
            return True
        else:
            raise Exception(f"App not on the {type(self)} page")


    def agree(self):
        if self.on_this_page():
            self.find_by(self.agree_button_locator).click()

            # Maybe should check if it is checked or let the test call is_accept_checked()? 
            # return a new page object? The Pin Setup page.
            return EnterChatPage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")
