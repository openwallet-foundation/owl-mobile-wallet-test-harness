import logging

from pageobjects.basepage import WaitCondition
from pageobjects.bc_wallet.initialization import InitializationPage
from selenium.common.exceptions import TimeoutException


class InitializationPageQC(InitializationPage):
    """QC Wallet initialization page that appears after setting up pin or entering pin"""

    def __init__(self, driver):
        super().__init__(driver)

    def wait_until_initialized(self, timeout=100, retry_attempts=1):
        logger = logging.getLogger(__name__)

        for i in range(retry_attempts):
            try:
                if self.still_initializing():
                    self.find_by(
                        self.loading_locator,
                        timeout,
                        WaitCondition.INVISIBILITY_OF_ELEMENT_LOCATED,
                    )
                    logger.debug("Loading indicator disappeared")
                else:
                    from pageobjects.qc_wallet.home import HomePageQC

                    return HomePageQC(self.driver)
            except TimeoutException:
                try:
                    self.still_initializing()
                except Exception as e:
                    if "Oops! Something went wrong" in str(e):
                        logger.error(e)
                        self.oops_something_went_wrong_modal.select_retry()
                    else:
                        raise
            except Exception as e:
                if "Oops! Something went wrong" in str(e):
                    logger.error(e)
                    self.oops_something_went_wrong_modal.select_retry()
                else:
                    raise
        from pageobjects.qc_wallet.home import HomePageQC

        return HomePageQC(self.driver)
