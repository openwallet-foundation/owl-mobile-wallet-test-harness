"""
Class for interfacing with gmail client getting a IDIM Verified Person Credential certificate invitation
"""
from sys import platform
from decouple import config
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
# import Page Objects needed
from pageobjects.bc_wallet.holder_get_invite_interface.pageobjects.gmail_login_page import GmailLoginPage
from pageobjects.bc_wallet.holder_get_invite_interface.pageobjects.gmail_email_page import GmailEmailPage
from pageobjects.bc_wallet.holder_get_invite_interface.pageobjects.bc_vc_invitation_agree_page import BCVCInvitationAgreePage
from pageobjects.bc_wallet.holder_get_invite_interface.pageobjects.bc_vc_invitation_request_credential_page import BCVCInvitationRequestCredentialPage
from pageobjects.bc_wallet.holder_get_invite_interface.pageobjects.bc_vc_invitation_review_page import BCVCInvitationReviewPage
from pageobjects.bc_wallet.holder_get_invite_interface.pageobjects.connect_with_issuer_page import ConnectWithIssuerPage


class BCVPIssuerGetAuthCodeInterface():

    _gmail_login_page: GmailLoginPage
    _gmail_email_page: GmailEmailPage
    _bc_vc_invitation_agree_page: BCVCInvitationAgreePage
    _bc_vc_request_credential_page: BCVCInvitationRequestCredentialPage
    _bc_vc_invitation_review_page: BCVCInvitationReviewPage
    _bc_vc_qrcode_page: ConnectWithIssuerPage
    endpoint: str

    def __init__(self, endpoint):
        # Standup Selenuim Driver with endpoint
        self.endpoint = endpoint
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
        self._gmail_login_page = GmailLoginPage(self.driver)
        # make sure we are on the first page, the authenticate with page
        if not self._gmail_login_page.on_this_page():
            raise Exception(
                'Something is wrong, not on the Gmail login Page for the BC VP Issuer')
        username = config('BC_VP_USERNAME')
        password = config('BC_VP_HOLDER_EMAIL_PASSWORD')
        self._login(username, password)

    def _open_auth_code_email(self):
        """send a credential to the holder, return True if invite is successfully sent to email"""
        self._gmail_email_page.open_latest_email()
        return True

    def get_auth_code(self):
        """send a credential to the holder, return True if invite is successfully sent to email"""
        self._gmail_email_page.open_latest_email()
        auth_code = self._gmail_email_page.get_auth_code()
        self._gmail_email_page.delete_opened_email()
        return auth_code


    def _login(self, username: str, password: str):
        if not self._gmail_login_page.on_this_page():
            raise Exception(
                'Something is wrong, not on the Gmail login Page for the BC VP Issuer')

        self._gmail_login_page.enter_username(username)
        self._gmail_login_page.next()
        self._gmail_login_page.enter_password(password)
        self._gmail_email_page = self._gmail_login_page.sign_in()

        if not self._gmail_email_page.on_this_page():
            raise Exception(
                'Something is wrong, not logged in to gmail')
