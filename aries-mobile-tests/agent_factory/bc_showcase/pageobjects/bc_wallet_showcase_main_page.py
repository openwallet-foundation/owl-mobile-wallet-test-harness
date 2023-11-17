from agent_factory.candy_uvp.pageobjects.webbasepage import WebBasePage
from selenium.webdriver.common.by import By
from pageobjects.basepage import WaitCondition
from agent_factory.bc_showcase.pageobjects.who_do_you_want_to_be_page import WhoDoYouWantToBePage

# These classes can inherit from a BasePage to do commone setup and functions
class BCWalletShowcaseMainPage(WebBasePage):
    """BC Wallet Showcase Main Entry page object"""

    # Locators
    on_this_page_text_locator = "BC Wallet Showcase"
    #on_this_page_locator = (By.XPATH, '//*[@id="app"]/div/main/div/div/div/div[1]/div/div/h3[1]/strong')
    #get_started_locator = (By.XPATH, '//button[@class='bg-bcgov-blue dark:bg-bcgov-white text-bcgov-white dark:text-bcgov-black py-3 px-5 rounded-lg font-semibold shadow-sm dark:shadow-none select-none ']')
    get_started_locator = (By.CLASS_NAME, "bg-bcgov-blue")


    def on_this_page(self):   
        #return super().on_this_page(self.on_this_page_locator, timeout=20)    
        return super().on_this_page(self.on_this_page_text_locator, timeout=20) 

    def select_get_started(self) -> WhoDoYouWantToBePage:
        if self.on_this_page():
            self.find_by(self.get_started_locator).click()
            return WhoDoYouWantToBePage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")

