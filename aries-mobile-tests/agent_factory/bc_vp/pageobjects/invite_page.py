from agent_factory.candy_uvp.pageobjects.webbasepage import WebBasePage
from selenium.webdriver.common.by import By

# These classes can inherit from a BasePage to do commone setup and functions
class InvitePage(WebBasePage):
    """BC VP Issuer Invites page object"""

    # Locators
    on_this_page_text_locator = "Invite"
    #name_locator = (By.ID, "sq_118i")
    #name_locator = (By.XPATH, '//*[@id="sq_100i"]')
    name_locator = (By.XPATH, '//input[@id="sq_100i"]')
    #first_email_locator = (By.ID, "input-1348")
    first_email_locator = (By.XPATH, '//*[@id="input-92"]')
    #second_email_locator = (By.ID, "sq_119i")
    second_email_locator = (By.XPATH, '//*[@id="sq_101i"]')
    #program_locator = (By.ID, "sq_120i")
    program_locator = (By.XPATH, '//*[@id="sq_102i"]')
    #save_button_locator = (By.CLASS_NAME, "v-btn v-btn--outlined theme--light v-size--default success--text")
    save_button_locator = (By.XPATH, '//*[@id="app"]/div/main/div/div/div/div[5]/div/div/button')

    def on_this_page(self):   
        return super().on_this_page(self.on_this_page_text_locator, timeout=100) 

    def enter_name(self, name):
        if self.on_this_page():
            self.find_by(self.name_locator).send_keys(name)
            return True
        else:
            raise Exception(f"App not on the {type(self)} page")

    def enter_email(self, email):
        if self.on_this_page():
            self.find_by(self.first_email_locator).send_keys(email)
            self.find_by(self.second_email_locator).send_keys(email)
            return True
        else:
            raise Exception(f"App not on the {type(self)} page")

    def enter_program(self, program):
        if self.on_this_page():
            self.find_by(self.program_locator).send_keys(program)
            return True
        else:
            raise Exception(f"App not on the {type(self)} page")

    def save(self):
        if self.on_this_page():
            self.find_by(self.save_button_locator).click()
            from agent_factory.bc_vp.pageobjects.invites_page import InvitesPage
            return InvitesPage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")
