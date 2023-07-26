from agent_factory.candy_uvp.pageobjects.webbasepage import WebBasePage
from selenium.webdriver.common.by import By
from pageobjects.basepage import WaitCondition
from agent_factory.candy_uvp.pageobjects.review_and_confirm_page import ReviewAndConfirmPage

# These classes can inherit from a BasePage to do commone setup and functions
class RequestCredentialPage(WebBasePage):
    """CANdy UVP Issuer Terms of Service page object"""

    # Locators
    on_this_page_text_locator = "Request Credential"
    first_name_locator = (By.ID, "sq_100i")
    last_name_locator = (By.ID, "sq_101i")
    dob_locator = (By.ID, "sq_102i")
    street_address_locator = (By.ID, "sq_103i")
    postal_code_locator = (By.ID, "sq_104i")
    city_locator = (By.ID, "sq_105i")
    province_locator = (By.ID, "sq_106i")
    request_credential_button_locator = (By.CLASS_NAME, "sv_complete_btn")

    def on_this_page(self):   
        #print(self.driver.page_source)     
        return super().on_this_page(self.on_this_page_text_locator) 

    def enter_first_name(self, first_name):
        # if self.on_this_page():
        self.find_by(self.first_name_locator, wait_condition=WaitCondition.ELEMENT_TO_BE_CLICKABLE).send_keys(first_name)
        return True
        # else:
        #     raise Exception(f"App not on the {type(self)} page")

    def enter_last_name(self, last_name):
        if self.on_this_page():
            self.find_by(self.last_name_locator).send_keys(last_name)
            return True
        else:
            raise Exception(f"App not on the {type(self)} page")

    def enter_dob(self, dob):
        if self.on_this_page():
            self.find_by(self.dob_locator).send_keys(dob)
            return True
        else:
            raise Exception(f"App not on the {type(self)} page")

    def enter_street_address(self, street_address):
        if self.on_this_page():
            self.find_by(self.street_address_locator).send_keys(street_address)
            return True
        else:
            raise Exception(f"App not on the {type(self)} page")

    def enter_postal_code(self, postal_code):
        if self.on_this_page():
            self.find_by(self.postal_code_locator).send_keys(postal_code)
            return True
        else:
            raise Exception(f"App not on the {type(self)} page")

    def enter_city(self, city):
        if self.on_this_page():
            self.find_by(self.city_locator).send_keys(city)
            return True
        else:
            raise Exception(f"App not on the {type(self)} page")

    def enter_province(self, province):
        if self.on_this_page():
            self.find_by(self.province_locator).send_keys(province)
            return True
        else:
            raise Exception(f"App not on the {type(self)} page")

    def request_credential(self):
        if self.on_this_page():
            self.find_by(self.request_credential_button_locator).click()

            return ReviewAndConfirmPage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")
