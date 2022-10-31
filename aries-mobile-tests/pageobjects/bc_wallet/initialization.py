from time import sleep
from appium.webdriver.common.appiumby import AppiumBy
from pageobjects.basepage import BasePage
from pageobjects.bc_wallet.home import HomePage
import time


# These classes can inherit from a BasePage to do common setup and functions
class InitializationPage(BasePage):
    """Wallet initialization page that appears after setting up pin or entering pin"""

    # Locators
    #on_this_page_text_locator = (MobileBy.ID, "com.ariesbifold:id/LoadingActivityIndicator")
    loading_locator = (AppiumBy.ID, "com.ariesbifold:id/LoadingActivityIndicator")

    def on_this_page(self):
        #return super().on_this_page(self.on_this_page_text_locator)
        #print(self.driver.page_source)
        return self.still_initializing()

    def still_initializing(self):
        try:
            self.find_by(self.loading_locator)
            return True
        except:
            return False

    def wait_until_initialized(self, timeout=300):
        loading = True
        loop_timeout = time.time() + timeout
        # temporary sleep since it seems that accessing the initialization sceeen with appium has an affect on its ability to fully initialize
        sleep(10)
        while loading == True:
            if time.time() > loop_timeout:
                raise Exception(f"App Initialization taking longer than expected. Timing out at {timeout} seconds.")
            try:
                self.find_by(self.loading_locator, timeout=5)
            except Exception as e:
                if "Could not find element by" in str(e):
                    loading = False
                else:
                    raise e
        return HomePage(self.driver)

