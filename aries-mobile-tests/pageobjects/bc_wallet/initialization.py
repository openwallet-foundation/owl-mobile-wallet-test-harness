from appium.webdriver.common.mobileby import MobileBy
from pageobjects.basepage import BasePage
from pageobjects.bc_wallet.home import HomePage
import time


# These classes can inherit from a BasePage to do common setup and functions
class InitializationPage(BasePage):
    """Wallet initialization page that appears after setting up pin or entering pin"""

    # Locators
    #on_this_page_text_locator = (MobileBy.ID, "com.ariesbifold:id/LoadingActivityIndicator")
    loading_locator = (MobileBy.ID, "com.ariesbifold:id/LoadingActivityIndicator")

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
        while loading == True:
            try:
                self.find_by(self.loading_locator, timeout=5)
            except Exception as e:
                if "Could not find element by" in str(e):
                    loading = False
                    if time.time() > loop_timeout:
                        raise Exception(f"App Initialization taking longer than expected. Timeing out at {timeout} seconds.")
                else:
                    raise e
        return HomePage(self.driver)

