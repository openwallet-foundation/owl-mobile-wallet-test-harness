from time import sleep

from appium.webdriver.common.touch_action import TouchAction
from pageobjects.basepage import WaitCondition
from pageobjects.bc_wallet.pinsetup import PINSetupPage
from pageobjects.bc_wallet.termsandconditions import TermsAndConditionsPage
from pageobjects.qc_wallet.pinsetup import PINSetupPageQC


# These classes can inherit from a BasePage to do commone setup and functions
class TermsAndConditionsPageQC(TermsAndConditionsPage):
    """Terms and Conditions QC page object"""

    def __init__(self, driver):
        super().__init__(driver)

    def select_accept(self):
        if self.on_this_page():
            el_visible = self.is_element_visible(self.terms_and_conditions_accept_locator)
            timeout=30
            while not el_visible and timeout > 0:
                self.swipe_down()
                el_visible = self.is_element_visible(self.terms_and_conditions_accept_locator)
                timeout-=1
            # try:
            #     self.scroll_to_element(self.back_aid_locator[1])
            # except:
            #     # Sometimes it seems that scrolling may try to access the element by accessibility id before it appears
            #     # if we get this failure then just sleep and try again. 
            #     sleep(5)
            #     self.scroll_to_element(self.back_aid_locator[1])
            self.find_by(self.terms_and_conditions_accept_locator).click()
            return True
        else:
            raise Exception(f"App not on the {type(self)} page")

    def select_continue(self):
        if self.on_this_page():
            el_visible = self.is_element_visible(self.continue_button_locator)
            timeout=30
            while not el_visible and timeout > 0:
                self.swipe_down()
                el_visible = self.is_element_visible(self.continue_button_locator)
                timeout-=1
            # try:
            #     self.scroll_to_element(self.back_aid_locator[1])
            # except:
            #     # Sometimes it seems that scrolling may try to access the element by accessibility id before it appears
            #     # if we get this failure then just sleep and try again. 
            #     sleep(5)
            #     self.scroll_to_element(self.back_aid_locator[1])
            self.find_by(self.continue_button_locator).click()

            # Maybe should check if it is checked or let the test call is_accept_checked()? 
            # return a new page object? The Pin Setup page.
            return PINSetupPageQC(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")
