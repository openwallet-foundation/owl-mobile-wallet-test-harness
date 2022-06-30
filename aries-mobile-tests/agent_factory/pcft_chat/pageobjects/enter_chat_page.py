from agent_factory.candy_uvp.pageobjects.webbasepage import WebBasePage
from selenium.webdriver.common.by import By
from agent_factory.pcft_chat.pageobjects.authentication_required_page import AuthenticationRequiredPage

# These classes can inherit from a BasePage to do commone setup and functions
class EnterChatPage(WebBasePage):
    """PCFT Chat enter chat page object"""

    # Locators
    on_this_page_text_locator = "Use your credential to join the conversation."
    #enter_button_locator = (By.CLASS_NAME, "btn btn btn-outline-success")
    enter_button_locator = (By.XPATH, '//*[@id="signup"]')
    


    def on_this_page(self):   
        #print(self.driver.page_source)     
        return super().on_this_page(self.on_this_page_text_locator) 

    def enter(self):
        if self.on_this_page():
            self.find_by(self.enter_button_locator).click()

            return AuthenticationRequiredPage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")
