from agent_factory.candy_uvp.pageobjects.webbasepage import WebBasePage
from selenium.webdriver.common.by import By
from pageobjects.basepage import WaitCondition
from agent_factory.candy_uvp.pageobjects.connect_with_issuer_page import ConnectWithIssuerPage

# These classes can inherit from a BasePage to do commone setup and functions
class ReviewAndConfirmPage(WebBasePage):
    """CANdy UVP Issuer Review and Confirm page object"""

    # Locators
    on_this_page_text_locator = "Review and Confirm"
    i_confirm_locator = (By.CLASS_NAME, "v-input--selection-controls__ripple")
    #proceed_button_locator = (By.CLASS_NAME, "v-btn__content")
    proceed_button_locator = (By.XPATH, '//*[@id="app"]/div/main/div/div/div/div[3]/div[2]/div[2]/a/span')


    def on_this_page(self):   
        #print(self.driver.page_source)     
        return super().on_this_page(self.on_this_page_text_locator) 

    def select_i_confirm(self):
        # if self.on_this_page():
        self.find_by(self.i_confirm_locator, wait_condition=WaitCondition.ELEMENT_TO_BE_CLICKABLE).click()
        return True
        # else:
        #     raise Exception(f"App not on the {type(self)} page")


    def proceed(self):
        if self.on_this_page():
            self.find_by(self.proceed_button_locator).click()
            return ConnectWithIssuerPage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")
