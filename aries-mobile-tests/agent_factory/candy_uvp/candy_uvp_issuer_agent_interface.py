"""
Class for actual CANdy Unverified Person Credetial issuer agent
"""
import base64
from agent_factory.issuer_agent_interface import IssuerAgentInterface
from sys import platform
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
# import Page Objects needed
from agent_factory.candy_uvp.pageobjects.terms_of_service_page import TermsOfServicePage
from agent_factory.candy_uvp.pageobjects.request_credential_page import RequestCredentialPage
from agent_factory.candy_uvp.pageobjects.review_and_confirm_page import ReviewAndConfirmPage
from agent_factory.candy_uvp.pageobjects.connect_with_issuer_page import ConnectWithIssuerPage
from agent_factory.candy_uvp.pageobjects.issuing_credential_page import IssuingCredentialPage

#import json
#from agent_test_utils import get_qr_code_from_invitation
#from random import randint

class CANdy_UVP_IssuerAgentInterface(IssuerAgentInterface):

    _terms_of_service_page: TermsOfServicePage
    _request_credential_page: RequestCredentialPage
    _review_and_confirm_page: ReviewAndConfirmPage
    _connect_with_issuer_page: ConnectWithIssuerPage
    _issuing_credential_page: IssuingCredentialPage

        # Default schema and cred
    DEFAULT_CREDENTIAL_DATA = {
        "first_name": "firstname",
        "last_name": "lastname",
        "date_of_birth": "1968-06-22",
        "street_address": "1968 oh six twenty two street",
        "postal_code": "K7P 2N3",
        "city": "Victoria",
        "province": "British Columbia",
    }

    def __init__(self, endpoint):
        # Standup Selenuim Driver with endpoint
        super().__init__(endpoint)
        if platform == "linux" or platform == "linux2":
            print("Starting Chromium on linux for Issuer Agent")
            options = Options()
            options.add_argument("--no-sandbox")
            #options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--headless")
            self.driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()))
            #self.driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
        else:
            print("Starting Chrome on Mac or Windows for Issuer Agent")
            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        # go to the issuer endpoint in the browser
        self.driver.get(self.endpoint)
        # instantiate intial page objects
        self._terms_of_service_page = TermsOfServicePage(self.driver)
        # make sure we are on the first page, the terms of service page
        if not self._terms_of_service_page.on_this_page():
            raise Exception('Something is wrong, not on the Terms of Service Page for the CANdy UVP Issuer')

    def get_issuer_type(self) -> str:
        """return the type of issuer as a string CANdyUVPIssuer"""
        return "CANdyUVPIssuer"

    def create_invitation(self, oob=False, print_qrcode=False, save_qrcode=False):
        # This is not supported on CANdy UVP Issuer. Connection is made when creating the credential
        # If called, send an exception back on this one and let the test handle it. Maybe a IssuerInterfaceFunctionNotSupported error.
        return Exception('Function not supported for CANdy UVP Issuer')
        
    def connected(self):
        """return true if connected"""
        # Check Issuing Credential Page for  "Connected to the Issuer Agent"
        return self._issuing_credential_page.connected()


    def send_credential(self, version=1, schema=None, credential_offer=None, revokable=False):
        """send a credential to the holder, returns a qr code for holder to connect to"""
        self._terms_of_service_page.select_i_agree()
        self._request_credential_page = self._terms_of_service_page.agree()

        if credential_offer:
            # Make credential_offer format into name value pairs
            credential_data = self._create_name_value_pairs_from_credential_offer(credential_offer)
            self._request_credential_page.enter_first_name(credential_data["first_name"])
            self._request_credential_page.enter_last_name(credential_data["last_name"])
            self._request_credential_page.enter_dob(credential_data["date_of_birth"])
            self._request_credential_page.enter_street_address(credential_data["street_address"])
            self._request_credential_page.enter_postal_code(credential_data["postal_code"])
            self._request_credential_page.enter_city(credential_data["city"])
            self._request_credential_page.enter_province(credential_data["province"])
        else:
            self._request_credential_page.enter_first_name(self.DEFAULT_CREDENTIAL_DATA["first_name"])
            self._request_credential_page.enter_last_name(self.DEFAULT_CREDENTIAL_DATA["last_name"])
            self._request_credential_page.enter_dob(self.DEFAULT_CREDENTIAL_DATA["date_of_birth"])
            self._request_credential_page.enter_street_address(self.DEFAULT_CREDENTIAL_DATA["street_address"])
            self._request_credential_page.enter_postal_code(self.DEFAULT_CREDENTIAL_DATA["postal_code"])
            self._request_credential_page.enter_city(self.DEFAULT_CREDENTIAL_DATA["city"])
            self._request_credential_page.enter_province(self.DEFAULT_CREDENTIAL_DATA["province"])

        self._review_and_confirm_page = self._request_credential_page.request_credential()

        self._review_and_confirm_page.select_i_confirm()
        self._connect_with_issuer_page = self._review_and_confirm_page.proceed()

        qrcode = self._connect_with_issuer_page.get_qr_code()
        self._issuing_credential_page = IssuingCredentialPage(self.driver)
        return qrcode


    def restart_issue_credential(self):
        # go to the issuer endpoint in the browser
        self.driver.get(self.endpoint)
        # make sure we are on the first page, the terms of service page
        if not self._terms_of_service_page.on_this_page():
            raise Exception('Something is wrong, not on the Terms of Service Page for the CANdy UVP Issuer')

    def revoke_credential(self, publish_immediately=True, notify_holder=False):
        """revoke a credential"""
        return Exception('Function not supported for CANdy UVP Issuer')

    def _create_name_value_pairs_from_credential_offer(self, credential_offer):
        credential_data = {}
        for attribute in credential_offer["attributes"]:
            credential_data[attribute["name"]] = attribute["value"]
        return credential_data