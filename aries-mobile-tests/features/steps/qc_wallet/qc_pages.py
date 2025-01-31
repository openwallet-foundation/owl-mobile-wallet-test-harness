from behave import given, when, then
from pageobjects.qc_wallet.moreoptions import MoreOptionsPageQC
from pageobjects.qc_wallet.contacts import ContactsPageQC
from pageobjects.qc_wallet.help import HelpPageQC
from pageobjects.qc_wallet.about import AboutPageQC
from pageobjects.qc_wallet.qc_help_center_pages.what_is_a_pin import WhatIsAPINPageQC
from pageobjects.qc_wallet.qc_help_center_pages.what_is_biometrics import WhatIsBiometricsPageQC

@given("the Holder is on the help center page")
def step_impl(context):
    context.execute_steps(
        f"""
        Given the Holder has setup thier Wallet and land on the Home screen
        When the Holder opens more options page
        And the Holder open help center page
        Then Help Center page is displayed
    """
    )

@when("the Holder opens more options page")
def open_more_page_step_impl(context):
    context.thisMoreOptionsPageQC= context.thisHomePageQC.select_more()
    
@when("the Holder open contacts page")
def open_contacts_page_step_impl(context):
    context.thisContactsPageQC = context.thisMoreOptionsPageQC.select_contacts()
    
@then("the contacts page is displayed")
def contacts_page_step_impl(context):
    assert context.thisContactsPageQC.on_this_page()
    
@when("the Holder open help center page")
@given("the Holder open help center page")
def open_help_page_step_impl(context):
        context.thisHelpPageQC = context.thisMoreOptionsPageQC.select_help()
        
@then("Help Center page is displayed")
def help_page_step_impl(context):
    assert context.thisHelpPageQC.on_this_page()
    
@when("the Holder open the about page") 
def open_about_step_impl(context):
        context.thisAboutPageQC = context.thisMoreOptionsPageQC.select_about()

@then("the about page is displayed")
def help_page_step_impl(context):
    assert context.thisAboutPageQC.on_this_page()
    
@when("the Holder click on PIN")
def open_pin_step_impl(context):
        if context.thisHelpPageQC.on_this_page() == False:
            # sleep(5)
            context.thisHelpPageQC = context.thisMoreOptionsPageQC.select_help()

        context.thisWhatIsAPINPageQC= context.thisHelpPageQC.select_nip()

@then("What is a PIN info page is displayed") 
def pin_step_impl(context):
    assert context.thisWhatIsAPINPageQC.on_this_page()
    
@when("the Holder click on Biometrics")
def what_is_biometrics_step_impl(context):
    context.thisWhatIsBiometricsPageQC= context.thisHelpPageQC.select_biometrics()
    
@then("what is Biometrics info page is displayed")
def biometrics_step_impl(context):
    assert context.thisWhatIsBiometricsPageQC.on_this_page()
    
@when("the Holder click on activities")
def activities_step_impl(context):
    context.thisWhatIsAHistoryPageQC= context.thisHelpPageQC.select_activities()
    
@then("what is a history info page is displayed")
def biometrics_step_impl(context):
    assert context.thisWhatIsAHistoryPageQC.on_this_page()
    
@when("the Holder click on PNG")
def png_step_impl(context):
    context.thisWhatIsPNGPageQC= context.thisHelpPageQC.select_png()
    
@then("what is png info page is displayed")
def biometrics_step_impl(context):
    assert context.thisWhatIsPNGPageQC.on_this_page()
    
@when("the Holder click on Receive presentation request")
def presentation_request_step_impl(context):
    context.thisHowToRespondToARequestPageQC= context.thisHelpPageQC.select_presentation_request()
    
@then("Receive a presentation request info page is displayed")
def receive_presentation_step_impl(context):
    assert context.thisHowToRespondToARequestPageQC.on_this_page()
    
@when("the Holder click on Receive a Certificate Offer")
def certificate_offer_step_impl(context):
    context.thisReceiveACertificateOfferInfoPageQC= context.thisHelpPageQC.select_presentation_request()
    
@then("receive a certificate offer info page is displayed")
def receive_certificate_step_impl(context):
    assert context.thisReceiveACertificateOfferInfoPageQC.on_this_page()
    

@when("the Holder click on Scan a QR code") 
def scan_a_qr_code_step_impl(context):
    context.thisScanAQRcodeInfoPageQC= context.thisHelpPageQC.select_scan_qr_code()
    
@then("scan a QR code info page is displayed")
def scan_a_qr_step_impl(context):
    assert context.thisScanAQRcodeInfoPageQC.on_this_page()
    
@when("the Holder click on Delete a certificate") 
def delete_a_certificate_step_impl(context):
    context.thisDeleteACertificateInfoPageQC= context.thisHelpPageQC.select_delete_certificate()
    
@then("delete a certificate info page is displayed")
def certificate_deleted_step_impl(context):
    assert context.thisDeleteACertificateInfoPageQC.on_this_page()
    
@when("the Holder click on return to Help Center button")
def return_step_impl(context):
    if hasattr(context, "thisWhatIsAPINPageQC"):  
        context.thisWhatIsAPINPageQC.select_return()
        return
    if hasattr(context, "thisWhatIsBiometricsPageQC"):  
        context.thisWhatIsBiometricsPageQC.select_return()
        return
    if hasattr(context, "thisWhatIsAHistoryPageQC"):  
        context.thisWhatIsAHistoryPageQC.select_return()
        return
    if hasattr(context, "thisWhatIsPNGPageQC"):  
        context.thisWhatIsPNGPageQC.select_return()
        return
    if hasattr(context, "thisHowToRespondToARequestPageQC"):  
        context.thisHowToRespondToARequestPageQC.select_return()
        return
    if hasattr(context, "thisReceiveACertificateOfferInfoPageQC"):  
        context.thisReceiveACertificateOfferInfoPageQC.select_return()
        return
    if hasattr(context, "thisDeleteACertificateInfoPageQC"):  
        context.thisDeleteACertificateInfoPageQC.select_return()
        return
    if hasattr(context, "thisScanAQRcodeInfoPageQC"):  
        context.thisScanAQRcodeInfoPageQC.select_return()
        return
