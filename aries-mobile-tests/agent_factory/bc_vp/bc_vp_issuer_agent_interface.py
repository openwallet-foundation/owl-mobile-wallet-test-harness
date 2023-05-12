"""
Class for actual IDIM Verified Person Credetial issuer agent
"""
from time import sleep
from agent_factory.issuer_agent_interface import IssuerAgentInterface
from sys import platform
from decouple import config
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
# import Page Objects needed
from pageobjects.bc_wallet.issuer_get_authcode_interface.bc_vp_issuer_get_authcode_interface_gapi import BCVPIssuerGetAuthCodeInterface
from agent_factory.bc_vp.pageobjects.authenticate_with_page import AuthenticateWithPage
from agent_factory.bc_vp.pageobjects.authenticate_page import AuthenticatePage
from agent_factory.bc_vp.pageobjects.authcode_page import AuthCodePage
from agent_factory.bc_vp.pageobjects.invites_page import InvitesPage
from agent_factory.bc_vp.pageobjects.invite_page import InvitePage
from enum import Enum
from enum import auto

class LoginBy(Enum):
    USERNAME_PASSWORD = auto()
    IDIM = auto()
    GITHUB = auto()

class BC_VP_IssuerAgentInterface(IssuerAgentInterface):

    _authenticate_with_page: AuthenticateWithPage
    _authenticate_page: AuthenticatePage
    _invites_page: InvitesPage
    _invite_page: InvitePage
    _invitation_url: str

    # Default schema and cred
    DEFAULT_CREDENTIAL_DATA = {
        "name": "vctester",
        "email": "vc.tester.extra@gmail.com",
        "program": "IDIM Testing",
    }

    # Default invitation url for reuse
    DEFAULT_INVITATION_URL = "https://bcvcpilot-issuer-test.apps.silver.devops.gov.bc.ca/?invite_token=23974aa6-009d-405a-a60b-0891c55cf277"

    def __init__(self, endpoint):
        # Standup Selenuim Driver with endpoint
        super().__init__(endpoint)
        if platform == "linux" or platform == "linux2":
            print("Starting Chromium on linux for Issuer Agent")
            options = Options()
            options.add_argument("--no-sandbox")
            # options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--headless")
            self.driver = webdriver.Chrome(options=options, service=Service(
                ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()))
            #self.driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
        else:
            print("Starting Chrome on Mac or Windows for Issuer Agent")
            self.driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()))
        # go to the issuer endpoint in the browser
        self.driver.get(self.endpoint)
        # instantiate intial page objects
        self._authenticate_with_page = AuthenticateWithPage(self.driver)
        # make sure we are on the first page, the authenticate with page
        if not self._authenticate_with_page.on_this_page():
            # self.driver.get_screenshot_as_file( 'authenticate_page_screenshot.png' )
            # print("Screenshot saved to screenshot.png")
            raise Exception(
                'Something is wrong, not on the Authenticate With Page for the BC VP Issuer')
        username = config('BC_VP_USERNAME')
        password = config('BC_VP_PASSWORD')
        self._login(username, password)

    def get_issuer_type(self) -> str:
        """return the type of issuer as a string BCVPIssuer"""
        return "BCVPIssuer"

    def create_invitation(self, oob=False, print_qrcode=False, save_qrcode=False):
        # This is not supported on BC VP Issuer. Connection is made when creating the credential
        # If called, send an exception back on this one and let the test handle it. Maybe a IssuerInterfaceFunctionNotSupported error.
        return Exception('Function not supported for BC VP Issuer')

    def connected(self):
        """return true if connected"""
        # Check the invites page for Issued Credential Check. 
        # This doesn't tell us if they are connected. This call is sometimes before a credential 
        # is fully issued. So return not supported for now. 
        #return self._invites_page.connected()
        return Exception('Function not supported for BC VP Issuer')

    def send_credential(self, version=1, schema=None, credential_offer=None, revokable=False, reuse_invitation=False):
        """send a credential to the holder, return True if invite is successfully sent to email"""
        
        if reuse_invitation:
            # Search for and edit based on the email address on the invites page
            # Set the credential issued flag to off and save the page
            # This is a temporary fix until search is fixed in the Issuer page
            self._invites_page.search(self.DEFAULT_CREDENTIAL_DATA["email"])
            sleep(5)
            self._invites_page.select_edit_invite(1)
            self._invites_page.uncheck_issued()
            self._invites_page.save_invite()

            # set the invitation url to the one we are reusing
            self._invitation_url = self.DEFAULT_INVITATION_URL
        else:
            self._invite_page = self._invites_page.new_invite()

            if credential_offer:
                # Make credential_offer format into name value pairs
                credential_data = self._create_name_value_pairs_from_credential_offer(
                    credential_offer)
                self._invite_page.enter_name(
                    credential_data["first_name"])
                self._request_credential_page.enter_email(
                    credential_data["email"])
                self._request_credential_page.enter_program(
                    credential_data["program"])
            else:
                self._invite_page.enter_name(
                    self.DEFAULT_CREDENTIAL_DATA["name"])
                self._invite_page.enter_email(
                    self.DEFAULT_CREDENTIAL_DATA["email"])
                self._invite_page.enter_program(
                    self.DEFAULT_CREDENTIAL_DATA["program"])

            self._invites_page = self._invite_page.save()
            if not self._invites_page.on_this_page():
                raise Exception(
                    'Something is wrong, on the Invites Page after sending invite for the BC VP Issuer')


            self._invitation_url= self._get_invitation_url()

        return True
        
    def _get_invitation_url(self):
        # Get the invitation url from the invites page
        self._invites_page.search(self.DEFAULT_CREDENTIAL_DATA["email"])
        sleep(5)
        self._invites_page.select_edit_invite(1)
        return self._invites_page.get_invitation_url()
    
    def get_invitation_url(self):
        return self._invitation_url

    def restart_issue_credential(self):
        # go to the issuer endpoint in the browser
        self.driver.get(self.endpoint)
        # make sure we are on the first page, the invites page
        if not self._invites_page.on_this_page():
            raise Exception(
                'Something is wrong, on the Invites Page for the BC VP Issuer')

    def revoke_credential(self, publish_immediately=True, notify_holder=False):
        """revoke a credential"""
        return Exception('Function not supported for BC VP Issuer')

    def _create_name_value_pairs_from_credential_offer(self, credential_offer):
        credential_data = {}
        for attribute in credential_offer["attributes"]:
            credential_data[attribute["name"]] = attribute["value"]
        return credential_data

    def _login(self, username: str, password: str, login_by:LoginBy=LoginBy.USERNAME_PASSWORD):
        if login_by == LoginBy.USERNAME_PASSWORD:
            self._login_with_unpw(username, password)
        elif login_by == LoginBy.GITHUB:
            self._login_with_github(username, password)
        elif login_by == LoginBy.IDIM:
            raise Exception(
                'Login to BCVC Pilot Issuer by IDIM account is not implemented')
        else:
            raise Exception(
                'Invalid login_by for Login to BCVC Pilot Issuer')

    def _login_with_unpw(self, username: str, password: str):
        self._authenticate_with_page.enter_username(username)
        #self.driver.get_screenshot_as_file( 'Invites_page_username_screenshot.png' )
        self._authenticate_with_page.enter_password(password)
        #self.driver.get_screenshot_as_file( 'Invites_page_password_screenshot.png' )
        self._invites_page = self._authenticate_with_page.sign_in()

        if not self._invites_page.on_this_page():
            # self.driver.get_screenshot_as_file( 'Invites_page_screenshot.png' )
            # print("Invites page screenshot saved to Invites_page_screenshot.png")
            raise Exception(
                'Something is wrong, not logged in on the Invites Page for the BC VP Issuer')

    def _login_with_github(self, username: str, password: str):
        self._authenticate_page = self._authenticate_with_page.github()
        if not self._authenticate_page.on_this_page():
            raise Exception(
                'Something is wrong, not on the Authenticate with github Page for the BC VP Issuer')

        self._authenticate_page.enter_username(username)
        self._authenticate_page.enter_password(password)
        self._invites_page = self._authenticate_page.sign_in()

        # if github login wants an auth code
        auth_code_page = AuthCodePage(self.driver)
        if auth_code_page.on_this_page():
            issuerGetAuthCodeInterface = BCVPIssuerGetAuthCodeInterface("http://www.gmail.com")
            auth_code =  issuerGetAuthCodeInterface.get_auth_code()
            # close the get auth code driver
            #issuerGetAuthCodeInterface.driver.close()
            auth_code_page = AuthCodePage(self.driver)
            auth_code_page.enter_auth_code(auth_code)

        if not self._invites_page.on_this_page():
            # self.driver.get_screenshot_as_file( 'Invites_page_screenshot.png' )
            # print("Screenshot saved to screenshot.png")
            raise Exception(
                'Something is wrong, not logged in on the Invites Page for the BC VP Issuer')