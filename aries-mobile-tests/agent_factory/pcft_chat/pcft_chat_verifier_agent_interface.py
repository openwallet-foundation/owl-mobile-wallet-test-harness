"""
Class for actual PCFT Verifier agent
"""

from agent_factory.verifier_agent_interface import VerifierAgentInterface
from sys import platform
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
# import Page Objects needed
from agent_factory.pcft_chat.pageobjects.terms_of_service_page import TermsOfServicePage
from agent_factory.pcft_chat.pageobjects.enter_chat_page import EnterChatPage
from agent_factory.pcft_chat.pageobjects.authentication_required_page import AuthenticationRequiredPage
from agent_factory.pcft_chat.pageobjects.chat_page import ChatPage

class PCFT_Chat_VerifierAgentInterface(VerifierAgentInterface):

    _terms_of_service_page: TermsOfServicePage
    _enter_chat_page: EnterChatPage
    _authentication_required_page: AuthenticationRequiredPage
    _chat_page: ChatPage


    def __init__(self, endpoint):
        # Standup Selenuim Driver with endpoint
        super().__init__(endpoint)
        if platform == "linux" or platform == "linux2":
            print("Starting Chromium on linux for Verifier Agent")
            options = Options()
            options.add_argument("--no-sandbox")
            #options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--headless")
            self.driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()))
            #self.driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
        else:
            print("Starting Chrome on Mac or Windows for Verifier Agent")
            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        # go to the issuer endpoint in the browser
        self.driver.get(self.endpoint)
        # instantiate intial page objects
        self._terms_of_service_page = TermsOfServicePage(self.driver)
        # make sure we are on the first page, the terms of service page
        if not self._terms_of_service_page.on_this_page():
            raise Exception('Something is wrong, not on the Terms of Service Page for the PCFT Chat Verification')

    def get_issuer_type(self) -> str:
        """return the type of issuer as a string AATHVerifier"""
        return "PCFTChatVerifier"

    def create_invitation(self, oob=False, print_qrcode=False, save_qrcode=False):
        return Exception('Function not supported for PCFT Chat Verifier')

    def connected(self):
        return Exception('Function not supported for PCFT Chat Verifier')

    def send_proof_request(self, version=1, request_for_proof=None, connectionless=False):
        """create a proof request """

        self._terms_of_service_page.select_i_agree()
        self._enter_chat_page = self._terms_of_service_page.agree()

        self._authentication_required_page = self._enter_chat_page.enter()

        return self._authentication_required_page.get_qr_code()

    def proof_request_verified(self):
        self._chat_page = ChatPage(self.driver)
        return self._chat_page.on_this_page()