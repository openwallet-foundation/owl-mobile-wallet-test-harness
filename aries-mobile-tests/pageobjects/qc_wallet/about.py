from pageobjects.basepage import BasePage

class AboutPageQC(BasePage):
    """About Page """
    
        # Locators
    en_title_text_locator = "About"
    fr_title_text_locator = "À propos"
    
    def on_this_page(self):     
        return super().on_this_page(self.en_title_text_locator) or super().on_this_page(self.fr_title_text_locator)
