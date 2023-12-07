"""
Class for BC Showcase issuer agent for Student and Lawer Showcase Credentials
"""
import base64
import io
import time
from agent_factory.issuer_agent_interface import IssuerAgentInterface
from agent_test_utils import add_border_to_qr_code
from sys import platform
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
# import Page Objects needed
from agent_factory.bc_showcase.pageobjects.bc_wallet_showcase_main_page import BCWalletShowcaseMainPage
from agent_factory.bc_showcase.pageobjects.who_do_you_want_to_be_page import WhoDoYouWantToBePage
from agent_factory.bc_showcase.pageobjects.lets_get_started_page import LetsGetStartedPage
#from agent_factory.bc_showcase.pageobjects.going_digital_page import GoingDigitalPage

# Lawyer Showcase Page Objects
#from agent_factory.bc_showcase.pageobjects.accessing_court_materials_page import AccessingCourtMaterialsPage
#from agent_factory.bc_showcase.pageobjects.get_your_lawyer_credential_page import GetYourLawyerCredentialPage

# Student Showcase Page Objects
from agent_factory.bc_showcase.pageobjects.install_bc_wallet_page import InstallBCWalletPage
#from agent_factory.bc_showcase.pageobjects.connect_withbest_bc_college_page import ConnectWithBestBCCollegePage


class BCShowcaseIssuerAgentInterface(IssuerAgentInterface):

    _actor : str
    _bc_wallet_showcase_main_page: BCWalletShowcaseMainPage
    _who_do_you_want_to_be_page: WhoDoYouWantToBePage
    _lets_get_started_page: LetsGetStartedPage
    _install_bc_wallet_page: InstallBCWalletPage
    #_going_digital_page: GoingDigitalPage
    #_accessing_court_materials_page: AccessingCourtMaterialsPage
    #_get_your_lawyer_credential_page: GetYourLawyerCredentialPage
    _install_bc_wallet_page: InstallBCWalletPage
    #_connect_with_best_bc_college_page: ConnectWithBestBCCollegePage

    def __init__(self, endpoint):
        # Standup Selenuim Driver with endpoint
        super().__init__(endpoint)
        if platform == "linux" or platform == "linux2":
            print("Starting Chromium on linux for BC Showcase Issuer Agent")
            options = Options()
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--headless")
            options.add_argument("--enable-javascript")
            self.driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()))
        else:
            print("Starting Chrome on Mac or Windows for Issuer Agent")
            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        # go to the issuer endpoint in the browser
        self.driver.get(self.endpoint)
        # instantiate intial page objects
        self._bc_wallet_showcase_main_page = BCWalletShowcaseMainPage(self.driver)
        self.driver.save_screenshot('BCWalletShowcaseMainPage.png')
        # make sure we are on the first page, the terms of service page
        if not self._bc_wallet_showcase_main_page.on_this_page():
            raise Exception('Something is wrong, not on the BC Wallet Showcase Main Page')

    def get_issuer_type(self) -> str:
        """return the type of issuer as a string BCShowcaseIssuer"""
        return "BCShowcaseIssuer"

    def create_invitation(self, oob=False, print_qrcode=False, save_qrcode=False, qr_code_border=40):
        # This is not supported on the BC Showcase Issuer. Connection is made when sending the credential
        # If called, send an exception back on this one and let the test handle it. Maybe a IssuerInterfaceFunctionNotSupported error.
        return Exception('Function not supported for BC Showcase Issuer')
        
    def connected(self):
        """return true if connected"""
        # Check Issuing Credential Page for  "Connected to the Issuer Agent"
        return self._connect_with_best_bc_college_page.connected()


    def send_credential(self, actor:str, credential_offer=None, version=1, schema=None, revokable=False):
        """send a credential to the holder, returns a qr code for holder to connect to"""
        self._who_do_you_want_to_be_page = self._bc_wallet_showcase_main_page.select_get_started()
        #self.driver.minimize_window()
        self.driver.maximize_window()
        #pause 3 second to let page loads
        time.sleep(3)
        self.driver.save_screenshot('who_do_you_want_to_be_page.png')
        if actor == "Student":
            self._who_do_you_want_to_be_page.select_student()
        elif actor == "Lawyer":
            self._who_do_you_want_to_be_page.select_lawyer()
        else:
            raise Exception(f"Unknown actor type {actor}")
        #self.driver.minimize_window()
        self.driver.maximize_window()
        #pause 3 second to let page loads
        time.sleep(3)
        self.driver.save_screenshot('who_do_you_want_to_be_page_actor_select.png')
        self._lets_get_started_page = self._who_do_you_want_to_be_page.select_next()
        #pause 3 second to let page loads
        time.sleep(3)
        self.driver.save_screenshot('lets_get_started_page.png')
        self._install_bc_wallet_page = self._lets_get_started_page.select_next()
        #pause 3 second to let page loads
        time.sleep(3)
        self.driver.save_screenshot('install_bc_wallet_page.png')
        self._connect_with_best_bc_college_page = self._install_bc_wallet_page.select_skip()
        #self.driver.minimize_window()
        self.driver.maximize_window()
        #pause 3 second to let page loads
        time.sleep(3)
        self.driver.save_screenshot('connect_with_best_bc_college_page.png')
        qrcode = self._connect_with_best_bc_college_page.get_qr_code()
        return add_border_to_qr_code(qrcode)


    def revoke_credential(self, publish_immediately=True, notify_holder=False):
        """revoke a credential"""
        return Exception('Function not supported for BC Showcase Issuer')