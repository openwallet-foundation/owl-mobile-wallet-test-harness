from agent_factory.candy_uvp.pageobjects.webbasepage import WebBasePage
from selenium.webdriver.common.by import By
from agent_factory.bc_vp.pageobjects.invite_page import InvitePage

# These classes can inherit from a BasePage to do commone setup and functions


class InvitesPage(WebBasePage):
    """BC VP Issuer Invites page object"""

    # Locators
    on_this_page_text_locator = "Invites"
    #new_invite_locator = (By.CLASS_NAME, "v-btn__content")
    new_invite_locator = (
        By.XPATH, '//*[@id="app"]/div/main/div/div/div/div/header/div/a')
    #search_locator = (By.CLASS_NAME, "v-input--selection-controls__ripple")
    search_locator = (By.ID, "input-1277")
    row_locator = (By.CLASS_NAME, "v-input--selection-controls__ripple")

    def on_this_page(self):
        return super().on_this_page(self.on_this_page_text_locator, timeout=1000)

    def search(self, search_term: str):
        if self.on_this_page():
            self.find_by(self.search_locator).send_keys(search_term)
            return True
        else:
            raise Exception(f"App not on the {type(self)} page")

    def new_invite(self):
        if self.on_this_page():
            self.find_by(self.new_invite_locator).click()
            return InvitePage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")
