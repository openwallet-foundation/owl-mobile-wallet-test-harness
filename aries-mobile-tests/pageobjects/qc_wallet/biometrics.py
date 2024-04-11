from appium.webdriver.common.appiumby import AppiumBy
from pageobjects.bc_wallet.biometrics import BiometricsPage


class BiometricsPageQC(BiometricsPage):
    """Biometrics enter page QC object"""

    # Locators
    dismiss_biometrics_modal_locator = (
        AppiumBy.ID,
        "com.android.systemui:id/button_negative",
    )

    def __init__(self, driver):
        super().__init__(driver)

    def dismiss_biometrics_modal(self):
        if self.driver.capabilities["platformName"] == "Android":
            self.find_by(self.dismiss_biometrics_modal_locator).click()
            return True
        else:
            pass
