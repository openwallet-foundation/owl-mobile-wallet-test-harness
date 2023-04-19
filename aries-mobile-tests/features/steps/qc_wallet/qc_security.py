from time import sleep
from bc_wallet.security import *
from override_steps import overrides
from pageobjects.qc_wallet.biometrics import BiometricsPageQC

@overrides('authenticates with thier biometrics', 'when')
def auth_biometrics_step_impl(context):
    # Check to see if the Biometrics page is displayed
    #if ('autoGrantPermissions' in context.driver.capabilities and context.driver.capabilities['autoGrantPermissions'] == False) or (context.driver.capabilities['platformName'] == 'iOS'):
    context.thisBiometricsPage = BiometricsPageQC(context.driver)
    assert context.thisBiometricsPage.on_this_page()
    context.device_service_handler.biometrics_authenticate(True)
    assert context.thisBiometricsPage.on_this_page() == False
    context.thisInitializationPage.wait_until_initialized()

@overrides('fails to authenticate with thier biometrics once', 'when')
def fails_biometrics_step_impl(context):
    if hasattr(context, 'thisBiometricsPage') == False:
        context.thisBiometricsPage = BiometricsPageQC(context.driver)

    assert context.thisBiometricsPage.on_this_page()
    context.device_service_handler.biometrics_authenticate(False)
    context.thisBiometricsPage.dismiss_biometrics_modal()
    #assert context.thisBiometricsPage.on_this_page()


@then('they select visibility toggle on the first PIN as "{pin}"')
def visibility_toggle_first_pin_step_impl(context, pin):
    assert pin == context.thisPINSetupPage.get_pin()

@then('they select visibility toggle on the second PIN as "{pin}"')
def visibility_toggle_second_pin_step_impl(context, pin):
    assert pin == context.thisPINSetupPage.get_second_pin()

@overrides('the User selects Create PIN', 'when')
@overrides('the User selects Create PIN', 'then')
def create_pin_step_impl(context):
    if "TCL_PNG_ACC_002.1" in context.tags or "T005-Security" in context.tags:
        context.thisPINSetupPage.create_pin_throw_error()
    else:
        context.thisOnboardingBiometricsPage = context.thisPINSetupPage.create_pin()
        context.thisOnboardingBiometricsPage.on_this_page()
    # next_page = context.thisPINSetupPage.create_pin()
    # if type(next_page) == OnboardingBiometricsPage: 
    #     context.thisOnboardingBiometricsPage = next_page
    #     context.thisOnboardingBiometricsPage.on_this_page()

@then('they select ok on PINs error')
def select_ok_on_error_step_impl(context):
    context.thisPINSetupPage.select_ok_on_modal()

@overrides('they are informed that the PINs do not match', 'then')
def step_impl(context):
    assert context.thisPINSetupPage.get_pin_error() == "PINs do not match"


@overrides('they land on the Home screen', 'then')
@overrides('initialization ends (failing silently)', 'when')
@overrides('they have access to the app', 'then')
@overrides('the User has successfully created a PIN', 'then')
def special_step_impl(context):
    # The Home page will not show until the initialization page is done. 
    #assert context.thisInitializationPage.on_this_page()
    context.thisHomePage = context.thisInitializationPage.wait_until_initialized()
    context.thisNavBar = NavBar(context.driver)
    if context.thisHomePage.on_this_page() == False:
        sleep(3)
        assert context.thisHomePage.on_this_page()
    else:
        assert context.thisHomePage.on_this_page()

