from typing import Union
from pageobjects.basepage import BasePage

class explainerPages(BasePage):
    """ 
    Figma: 
        Category: Onboarding
        Sub Section: Explainer Screens
        status: WIP
    """
    # Locators
    nextBtnLocator: str = 'Next'
    doneBtnLocator: str =  "00000000-0000-002d-ffff-ffff000001bd" #BUG: undefined for now
    backBtnLocator: str = "00000000-0000-001d-ffff-ffff000000f6"
    skipBtnLocator: str = "00000000-0000-001d-ffff-ffff0000012c" # BUG: cannot find the accessibility name
    # TODO: check the sub-title at each movement
    subTitleList: list = [
        "Store credentials",
        "Share only what's neccesary",
        "Keep track of what you shared"
    ]

    # INFO: test for swipping too?
    def rightPage(self,index: int) -> Union[bool,None]:
        if self.on_the_right_page(self.subTitleList[index]):
            return True
        else:
            raise Exception("Not on the terms of service page")

    def selectSkipButton(self) -> None:
        self.find_by_element_id(self.skipBtnLocator).click()
        return

    def selectNextBtn(self, index: int) -> Union[int,None]:
        if index == 2 and self.rightPage(index):
            self.find_by_element_id(self.doneBtnLocator).click()
            return None

        elif self.rightPage(index): 
            self.find_by_element_id(self.nextBtnLocator).click()
            index += 1 
            return index

        else: 
            raise Exception("Wher are thou?")

    def selectBackBtn(self, index:int) -> Union[int,None]:
        if index == 0 and self.rightPage(index):
            self.find_by_element_id(self.backBtnLocator).click()

            return None
        else: 
            self.find_by_element_id(self.backBtnLocator).click()

            index -= 1
            return index

