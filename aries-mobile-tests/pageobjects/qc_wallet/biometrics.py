from appium.webdriver.common.appiumby import AppiumBy
from pageobjects.bc_wallet.biometrics import BiometricsPage
from pageobjects.qc_wallet.initialization import InitializationPageQC


class BiometricsPageQC(BiometricsPage):
    """Biometrics enter page QC object"""

    # Locators
    dismiss_biometrics_modal_locator = (
        AppiumBy.ID,
        "com.android.systemui:id/button_negative",
    )

    on_this_page_text_locator = "Biometrics"
    biometrics_toggle_locator = (AppiumBy.ID, "com.ariesbifold:id/ToggleBiometrics")
    continue_button_locator = (AppiumBy.ID, "com.ariesbifold:id/Continue")


    def on_this_page(self):     
       return super().on_this_page()

    def __init__(self, driver):
        super().__init__(driver)

    def dismiss_biometrics_modal(self):
        if self.driver.capabilities["platformName"] == "Android":
            self.find_by(self.dismiss_biometrics_modal_locator).click()
            return True
        else:
            pass

    def select_continue(self):
        if self.on_this_page():
            self.find_by(self.continue_button_locator).click()
            # # return the wallet initialization page
            return InitializationPageQC(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")

    def select_biometrics(self):
        if self.on_this_page():
            self.find_by(self.biometrics_toggle_locator).click()
            return True
        else:
            raise Exception(f"App not on the {type(self)} page")