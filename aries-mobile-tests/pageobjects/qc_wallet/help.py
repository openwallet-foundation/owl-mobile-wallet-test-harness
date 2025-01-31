from appium.webdriver.common.appiumby import AppiumBy
from pageobjects.basepage import BasePage
from pageobjects.qc_wallet.qc_help_center_pages.what_is_a_pin import WhatIsAPINPageQC
from pageobjects.qc_wallet.qc_help_center_pages.what_is_biometrics import WhatIsBiometricsPageQC
from pageobjects.qc_wallet.qc_help_center_pages.what_is_a_history import WhatIsAHistoryPageQC
from pageobjects.qc_wallet.qc_help_center_pages.what_is_png import WhatIsPNGPageQC
from pageobjects.qc_wallet.qc_help_center_pages.how_to_respond_to_a_request import HowToRespondToARequestPageQC
from pageobjects.qc_wallet.qc_help_center_pages.receive_a_certificate_offer_info_page import ReceiveACertificateOfferInfoPageQC
from pageobjects.qc_wallet.qc_help_center_pages.scan_a_qr_code_info_page import ScanAQRCodeInfoPageQC
from pageobjects.qc_wallet.qc_help_center_pages.delete_a_certificate_info_page import DeleteACertificateInfoPageQC


class HelpPageQC(BasePage):
    """Help Page QC page object"""

    # Locators
    en_title_text_locator = "Help Center"
    fr_title_text_locator = "Center d'aide"
    nip_selector = (AppiumBy.ID, "com.ariesbifold:id/PIN")
    biometrics_selector = (AppiumBy.ID, "com.ariesbifold:id/Biometrics")
    activities_selector = (AppiumBy.ID, "com.ariesbifold:id/Activities")
    png_selector = (AppiumBy.ID, "com.ariesbifold:id/PNG")
    presentation_request_selector = (AppiumBy.ID, "com.ariesbifold:id/Receive a presentation request")
    certificate_offer_selector = (AppiumBy.ID, "com.ariesbifold:id/Receive a Certificate Offer")
    scan_qr_code_selector = (AppiumBy.ID, "com.ariesbifold:id/Scan a QR code")
    delete_certificate_selector = (AppiumBy.ID, "com.ariesbifold:id/Delete a certificate")


    def on_this_page(self):     
        return super().on_this_page(self.en_title_text_locator) or super().on_this_page(self.fr_title_text_locator)
    
    def select_nip(self):
        if self.on_this_page():
            self.find_by(self.nip_selector).click()
            return WhatIsAPINPageQC(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")
        
    def select_biometrics(self):
        if self.on_this_page():
            self.find_by(self.biometrics_selector).click()
            return WhatIsBiometricsPageQC(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")

    def select_activities(self):
        if self.on_this_page():
            self.find_by(self.activities_selector).click()
            return WhatIsAHistoryPageQC(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")
        
    def select_png(self):
        if self.on_this_page():
            self.find_by(self.png_selector).click()
            return WhatIsPNGPageQC(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")

    def select_presentation_request(self):
        if self.on_this_page():
            self.find_by(self.presentation_request_selector).click()
            return HowToRespondToARequestPageQC(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")

    def select_certificate_offer(self):
        if self.on_this_page():
            self.find_by(self.certificate_offer_selector).click()
            return ReceiveACertificateOfferInfoPageQC(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")

    def select_scan_qr_code(self):
        if self.on_this_page():
            self.find_by(self.scan_qr_code_selector).click()
            return ScanAQRCodeInfoPageQC(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")
        
    def select_delete_certificate(self):
        if self.on_this_page():
            self.find_by(self.delete_certificate_selector).click()
            return DeleteACertificateInfoPageQC(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")