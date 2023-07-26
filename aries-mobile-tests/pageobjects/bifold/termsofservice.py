import time
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pageobjects.basepage import BasePage
from pageobjects.bifold.pinsetup import PINSetupPage

# These classes can inherit from a BasePage to do commone setup and functions
class TermsOfServicePage(BasePage):
    """Terms of Service page object"""

    # Locators
    # TODO: We could create a locator module that has all the locators. Given a specific app we could load the locators for that app. 
    # not sure this would be a use case that would be common. Leaving locators with the page objects for now.
    title_locator = "Terms of Service"
    terms_of_service_agree_locator = "I Agree to the Terms of Service"
    submit_button_locator = "Submit"


    def select_accept(self):
        if self.on_the_right_page(self.title_locator):
            #self.driver.swipe(100, 150, 100, 2000)
            self.driver.swipe(500, 2000, 500, 100)
            #self.find_by_element_id(self.terms_of_service_agree_locator).click()
            self.find_by_accessibility_id(self.terms_of_service_agree_locator).click()
            return True
        else:
            raise Exception(f"App not on the {self.title_locator} page")
        #     driver.manage(). timeouts().implicitlyWait(10, TimeUnit.SECONDS);
        #     driver. findElement (MobileBy.AccessibilityId ("Login Screen")).clickO:
        #     driver. findElement(MobileBy.AccessibilityId("username")).sendKeys("alice");
        #     driver. findElement (MobileBy.AccessibilityId("password")). sendKeys ("mypassword");
        #     driver. findElement(MobileBy.AccessibilityId("loginBtn")).click():
        #     driver.findElement(By.xpath("//*[@text='Logout']")).click();

        # search_element = WebDriverWait(context.driver, 10).until(
        #     EC.presence_of_element_located((MobileBy.ACCESSIBILITY_ID, "Search Wikipedia"))
        # )
        # search_element.click()
        # search_input = WebDriverWait(context.driver, 30).until(
        #     EC.element_to_be_clickable((MobileBy.ID, "org.wikipedia.alpha:id/search_src_text"))
        # )
        # search_input.send_keys(keyword)
        # time.sleep(5)

    def submit(self):
        if self.on_the_right_page(self.title_locator):
            self.find_by_accessibility_id(self.submit_button_locator).click()

            # Maybe should check if it is checked or let the test call is_accept_checked()? 
            # return a new page object? The Pin Setup page.
            return PINSetupPage(self.driver)
        else:
            raise Exception(f"App not on the {self.title_locator} page")