"""
Class for BC Showcase verifier agent for Student and Lawer Showcase Proofs
"""

from asyncio import sleep
from agent_factory.verifier_agent_interface import VerifierAgentInterface
from sys import platform
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
import json
from agent_test_utils import get_qr_code_from_invitation
from agent_controller_client import agent_controller_GET, agent_controller_POST, expected_agent_state, setup_already_connected
# import Page Objects needed
from agent_factory.bc_showcase.pageobjects.bc_wallet_showcase_main_page import BCWalletShowcaseMainPage
from agent_factory.bc_showcase.pageobjects.who_do_you_want_to_be_page import WhoDoYouWantToBePage
from agent_factory.bc_showcase.pageobjects.lets_get_started_page import LetsGetStartedPage
from agent_factory.bc_showcase.pageobjects.install_bc_wallet_page import InstallBCWalletPage
from agent_factory.bc_showcase.pageobjects.connect_with_best_bc_college_page import ConnectWithBestBCCollegePage
from agent_factory.bc_showcase.pageobjects.youre_all_set_page import YoureAllSetPage
from agent_factory.bc_showcase.pageobjects.using_your_credentials_page import UsingYourCredentialsPage
from agent_factory.bc_showcase.pageobjects.getting_a_student_discount_page import GettingAStudentDiscountPage
from agent_factory.bc_showcase.pageobjects.start_proving_youre_a_student_page import StartProvingYoureAStudentPage
from agent_factory.bc_showcase.pageobjects.book_a_study_room_page import BookAStudyRoomPage
from agent_factory.bc_showcase.pageobjects.start_booking_the_room_page import StartBookingTheRoomPage

class BCShowcaseVerifierAgentInterface(VerifierAgentInterface):

    _actor : str
    _bc_wallet_showcase_main_page: BCWalletShowcaseMainPage
    _who_do_you_want_to_be_page: WhoDoYouWantToBePage
    _lets_get_started_page: LetsGetStartedPage
    _install_bc_wallet_page: InstallBCWalletPage
    _connect_with_best_bc_college_page: ConnectWithBestBCCollegePage
    _youre_all_set_page: YoureAllSetPage
    _using_your_credentials_page: UsingYourCredentialsPage

    # Cool Clothes Online Page Objects
    _getting_a_student_discount_page: GettingAStudentDiscountPage
    _start_proving_youre_a_student_page: StartProvingYoureAStudentPage

    # BestBC College Page Objects
    _book_a_study_room_page: BookAStudyRoomPage
    _start_booking_the_room_page: StartBookingTheRoomPage


    def __init__(self, endpoint):
        # Standup Selenuim Driver with endpoint
        super().__init__(endpoint)
        if platform == "linux" or platform == "linux2":
            print("Starting Chromium on linux for BC Showcase Issuer Agent")
            options = Options()
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--headless")
            self.driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()))
        else:
            print("Starting Chrome on Mac or Windows for Issuer Agent")
            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        # go to the issuer endpoint in the browser
        self.driver.get(self.endpoint)
        # instantiate intial page objects and navigate to the Proof portion of the BC Wallet Showcase
        self._bc_wallet_showcase_main_page = BCWalletShowcaseMainPage(self.driver)

        # make sure we are on the page for proofs in the Showcase.
        if not self._bc_wallet_showcase_main_page.on_this_page():
            raise Exception('Something is wrong, not on the BC Wallet Showcase Main Page')


    def get_issuer_type(self) -> str:
        """return the type of issuer as a string BCShowcaseVerifier"""
        return "BCShowcaseVerifier"

    def create_invitation(self, oob=False, print_qrcode=False, save_qrcode=False, qr_code_border=40):
        # This is not supported on the BC Showcase Verifier. Connection is made when sending the proof request
        # If called, send an exception back on this one and let the test handle it. Maybe a VerifierInterfaceFunctionNotSupported error.
        return Exception('Function not supported for BC Showcase Verifier')

    def connected(self):
        """return True/False indicating if this issuer is connected to the wallet holder """
        """return true if connected"""
        return self._connect_with_best_bc_college_page.connected()


    def send_proof_request(self, actor:str, proof:str, version=1, request_for_proof=None, connectionless=False):
        """create a proof request """
        self._who_do_you_want_to_be_page = self._bc_wallet_showcase_main_page.select_get_started()
        self.driver.minimize_window()
        self.driver.maximize_window()
        if actor == "Student":
            self._who_do_you_want_to_be_page.select_student()
        elif actor == "Lawyer":
            self._who_do_you_want_to_be_page.select_lawyer()
        else:
            raise Exception(f"Unknown actor type {actor}")
        self.driver.minimize_window()
        self.driver.maximize_window()
        self._lets_get_started_page = self._who_do_you_want_to_be_page.select_next()
        self._install_bc_wallet_page = self._lets_get_started_page.select_next()
        self._connect_with_best_bc_college_page = self._install_bc_wallet_page.select_skip()
        self.driver.minimize_window()
        self.driver.maximize_window()
        self._youre_all_set_page = self._connect_with_best_bc_college_page.select_i_already_have_my_credential()
        self._using_your_credentials_page = self._youre_all_set_page.select_finish()

        if proof == "Cool Clothes Online":
            self._getting_a_student_discount_page = self._using_your_credentials_page.select_cool_clothes_online_start()
            self.driver.minimize_window()
            self.driver.maximize_window()
            self._start_proving_youre_a_student_page = self._getting_a_student_discount_page.select_start()
            self.driver.minimize_window()
            self.driver.maximize_window()
            qrcode = self._start_proving_youre_a_student_page.get_qr_code()
        elif proof == "BestBC College":
            self._book_a_study_room_page = self._using_your_credentials_page.select_bestbc_college_start()
            self.driver.minimize_window()
            self.driver.maximize_window()
            self._start_booking_the_room_page = self._book_a_study_room_page.select_start()
            self.driver.minimize_window()
            self.driver.maximize_window()
            qrcode = self._start_booking_the_room_page.get_qr_code()

        contents = qrcode.screenshot_as_base64.encode('utf-8')
        return contents.decode('utf-8')


    def proof_success(self, proof_result):
        if proof_result == "Discount":
            return self._start_proving_youre_a_student_page.proof_success()
        elif proof_result == "Room Booked":
            return self._start_booking_the_room_page.proof_success()
        elif proof_result == "Court Services":
            pass
        else:
            raise Exception(f"Invalid proof result: {proof_result} expected Discount, Room Booked, or Court Services")
