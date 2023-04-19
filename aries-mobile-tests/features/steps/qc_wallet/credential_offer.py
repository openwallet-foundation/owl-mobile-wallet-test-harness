from bc_wallet.credential_offer import *
from override_steps import overrides
from pageobjects.qc_wallet.credential_offer import CredentialOfferPageQC

@overrides('holder is brought to the credential offer screen', 'then')
def cred_offer_step_impl(context):
    # Workaround for bug 645
    context.execute_steps(f'''
        When the connection takes too long reopen app and select notification
    ''')

    #assert context.thisConnectingPage.wait_for_connection()

    context.thisCredentialOfferPage = CredentialOfferPageQC(context.driver)
    assert context.thisCredentialOfferPage.on_this_page()

@when('they select Decline the credential')
def decline_impl(context):
    context.isDeclining = True
    context.thisAreYouSureDeclineCredentialRequest = context.thisCredentialOfferPage.select_decline(scroll=True)

@then('they are brought to the confirm decline page')
def confirm_decline_page_impl(context):
    assert context.thisAreYouSureDeclineCredentialRequest.on_this_page() 

@then('they select Yes, decline this credential')
def decline_cred_impl(context):
    context.thisCredentialDeclinedPage = context.thisAreYouSureDeclineCredentialRequest.select_confirm()

@overrides('they select Done', 'when')
def at_home_step_impl(context):
    if hasattr(context, 'isDeclining') == True: 
        context.thisHomePage = context.thisCredentialDeclinedPage.select_done()
    elif hasattr(context, 'thisCredentialsPage') == False:
        context.thisCredentialAddedPage = CredentialAddedPage(context.driver)
        context.thisCredentialsPage = context.thisCredentialAddedPage.select_done()
