from agent_factory.candy_uvp.pageobjects.webbasepage import WebBasePage
from selenium.webdriver.common.by import By

# These classes can inherit from a WebBasePage to do commone setup and functions
class ChatPage(WebBasePage):
    """PCFT Chat page object"""

    # Locators
    on_this_page_text_locator = "Chat"
    chat_entry_locator = (By.CLASS_NAME, "form-control")
    send_chat_locator = (By.CLASS_NAME, "btn btn-outline-primary")


    def on_this_page(self):   
        #print(self.driver.page_source)     
        return super().on_this_page(self.on_this_page_text_locator) 

