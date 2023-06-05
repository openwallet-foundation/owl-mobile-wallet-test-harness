from bc_wallet.credential_offer import *
from override_steps import overrides
from pageobjects.qc_wallet.credential_offer import CredentialOfferPageQC

@overrides('holder is brought to the credential offer screen', 'then')
def cred_offer_step_impl(context):
    # Workaround for bug 645
    context.execute_steps(f'''
        When the connection takes too long reopen app and select notification
    ''')

    context.thisCredentialOfferPage = CredentialOfferPageQC(context.driver)
    assert context.thisCredentialOfferPage.on_this_page()

@when('they select Decline the credential')
def decline_impl(context):
    context.thisDeclineCredentialOffer = context.thisCredentialOfferPage.select_decline(
        scroll=True)
    context.thisHomePage = context.thisDeclineCredentialOffer.select_decline()
