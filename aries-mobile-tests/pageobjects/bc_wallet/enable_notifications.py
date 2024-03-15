from appium.webdriver.common.appiumby import AppiumBy
from pageobjects.basepage import BasePage, WaitCondition
from pageobjects.bc_wallet.onboarding_biometrics import OnboardingBiometricsPage

# These classes can inherit from a BasePage to do common setup and functions
class EnableNotificationsPage(BasePage):
    """While Onboarding the user is asked to Enable Notifications this is that screen's page object"""

    # Locators
    on_this_page_text_locator = "Enable Notifications to get instant alerts"
    on_this_page_locator = (AppiumBy.NAME, "Enable Notifications to get instant alerts")
    continue_locator = (AppiumBy.ID, "com.ariesbifold:id/PushNotificationContinue")

    def __init__(self, driver):
        super().__init__(driver)
        # Instantiate possible Modals and Alerts for this page
        self.enable_notifications_system_modal = EnableNotificationsSystemModal(driver)

    def on_this_page(self):   
        if self.current_platform == "Android":
            return super().on_this_page(self.on_this_page_text_locator) 
        return super().on_this_page(self.on_this_page_locator)

    def select_continue(self):
        self.find_by(self.continue_locator, wait_condition=WaitCondition.ELEMENT_TO_BE_CLICKABLE).click()

        return OnboardingBiometricsPage(self.driver)


class EnableNotificationsSystemModal(BasePage):
    """Enable Notifications System Modal page object"""

    # Locators
    on_this_page_text_locator = "Would Like to Send You Notifications"
    on_this_page_locator = (AppiumBy.ID, "com.ariesbifold:id/AllowNotifications")
    allow_button_locator = (AppiumBy.ID, "com.ariesbifold:id/Allow")
    dont_allow_button_locator = (AppiumBy.ID, "com.ariesbifold:id/DontAllow")

    def on_this_page(self):    
        return super().on_this_page(self.on_this_page_locator) 

    def select_allow(self):
        self.find_by(self.not_now_button_locator, wait_condition=WaitCondition.ELEMENT_TO_BE_CLICKABLE).click()

    def select_allow(self):
        self.find_by(self.allow_button_locator, wait_condition=WaitCondition.PRESENCE_OF_ELEMENT_LOCATED).click()
        return OnboardingBiometricsPage(self.driver)
    
        # if self.driver.capabilities['platformName'] == 'Android':
        #     self.select_system_allow_while_using_app()
        # return True

    def select_dont_allow(self):
        self.find_by(self.dont_allow_button_locator, wait_condition=WaitCondition.PRESENCE_OF_ELEMENT_LOCATED).click()
        return OnboardingBiometricsPage(self.driver)
    
    # def select_system_allow_while_using_app(self):
    #     self.find_by(self.system_allow_while_using_app, wait_condition=WaitCondition.ELEMENT_TO_BE_CLICKABLE).click()
