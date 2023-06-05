# -----------------------------------------------------------
# Behave Step Definitions for Terms and Conditions rejection or acceptance.
# 
# -----------------------------------------------------------

from time import sleep
from behave import given, when, then
import json
import os

# Local Imports
from agent_controller_client import agent_controller_GET, agent_controller_POST, expected_agent_state, setup_already_connected
from agent_test_utils import get_qr_code_from_invitation
from pageobjects.bc_wallet.temporarily_locked import TemporarilyLockedPage
# import Page Objects needed
from pageobjects.bc_wallet.termsandconditions import TermsAndConditionsPage
from pageobjects.bc_wallet.secure import SecurePage
from pageobjects.bc_wallet.home import HomePage
from pageobjects.bc_wallet.navbar import NavBar
from pageobjects.bc_wallet.pinsetup import PINSetupPage
from pageobjects.bc_wallet.biometrics import BiometricsPage
from pageobjects.bc_wallet.pin import PINPage


@given('the User has accepted the Terms and Conditions')
def step_impl(context):
    context.execute_steps(f'''
        Given the User is on the Terms and Conditions screen
        And the users accepts the Terms and Conditions
        And the user clicks continue
    ''')


@when('the User enters the first PIN as {pin}')
@when('the User enters the first PIN as "{pin}"')
def step_impl(context, pin):
    context.thisPINSetupPage.enter_pin(pin)
    # TODO remove comment here when Test IDs are on the visibility toggle
    #assert pin == context.thisPINSetupPage.get_pin()


@when('the User re-enters the PIN as {pin}')
@then('the User re-enters the PIN as "{pin}"')
@when('the User re-enters the PIN as "{pin}"')
def step_impl(context, pin):
    context.thisPINSetupPage.enter_second_pin(pin)
    # TODO remove comment here when Test IDs are on the visibility toggle
    #assert pin == context.thisPINSetupPage.get_second_pin()


@then('the User selects Create PIN')
@when('the User selects Create PIN')
def step_impl(context):
    context.thisOnboardingBiometricsPage = context.thisPINSetupPage.create_pin()
    context.thisOnboardingBiometricsPage.on_this_page()

@given('the Holder has selected to use PIN only to unlock BC Wallet')
def step_impl(context):
    context.thisInitializationPage = context.thisOnboardingBiometricsPage.select_continue()
    sleep(3)

@when('the User selects to use Biometrics')
def step_impl(context):
    if context.device_service_handler.supports_biometrics():
        assert context.thisOnboardingBiometricsPage.select_biometrics()
        context.thisInitializationPage = context.thisOnboardingBiometricsPage.select_continue()
        context.device_service_handler.biometrics_authenticate(True)
    else:
        context.thisInitializationPage = context.thisOnboardingBiometricsPage.select_continue()
        sleep(3)

@then('they have access to the app')
def step_impl(context):
    # The Home page will not show until the initialization page is done. 
    #assert context.thisInitializationPage.on_this_page()
    context.thisHomePage = context.thisInitializationPage.wait_until_initialized()
    if context.thisHomePage.welcome_to_bc_wallet_modal.is_displayed():
        #context.thisHomePage.welcome_to_bc_wallet_modal.select_dismiss()
        assert True
    else:
        assert context.thisHomePage.on_this_page()

@then('they land on the Home screen')
@when('initialization ends (failing silently)')
def step_impl(context):
    # The Home page will not show until the initialization page is done. 
    #assert context.thisInitializationPage.on_this_page()
    context.thisHomePage = context.thisInitializationPage.wait_until_initialized()
    context.thisNavBar = NavBar(context.driver)
    if context.thisHomePage.welcome_to_bc_wallet_modal.is_displayed():
        context.thisHomePage.welcome_to_bc_wallet_modal.select_dismiss()
    assert context.thisHomePage.on_this_page()

    # set the environment to TEST instead of PROD which is default as of build 575
    env = "Test"
    context.execute_steps(f'''
        Given the App environment is set to {env}
    ''')


@given('the App environment is set to {env}')
def step_impl(context, env):
    context.thisSettingsPage = context.thisHomePage.select_settings()
    context.thisSettingsPage.enable_developer_mode()
    context.thisDeveloperSettingsPage = context.thisSettingsPage.select_developer()
    context.thisDeveloperSettingsPage.select_env(env)
    context.thisSettingsPage = context.thisDeveloperSettingsPage.select_back()
    context.thisSettingsPage.select_back()
    if context.thisHomePage.welcome_to_bc_wallet_modal.is_displayed():
        context.thisHomePage.welcome_to_bc_wallet_modal.select_dismiss()
    assert context.thisHomePage.on_this_page()


@given('the Holder has setup biometrics on thier device')
def step_impl(context):
    # Assume already setup. TODO May need to actually do the setup here eventually.
    pass

@given('the Holder has selected to use biometrics to unlock BC Wallet')
def step_impl(context):
    context.execute_steps('''
        When the User selects to use Biometrics
        Then they land on the Home screen
    ''')

@when('they have closed the app')
@given('they have closed the app')
def step_impl(context):
    if str(context.driver.capabilities['platformName']).lower() == 'iOS'.lower():
        context.driver.terminate_app(context.driver.capabilities['bundleId'])
        # print(context.driver.query_app_state(context.driver.capabilities['bundleId'])) 
        # it should return 1 : application is not running 
    else:
        context.driver.close_app()


@when('the holder opens BC Wallet')
@when('they relaunch the app')
def step_impl(context):
    if str(context.driver.capabilities['platformName']).lower() == 'iOS'.lower():
        # context.driver.launch_app() -> there is a bug where this method is not closing and relaunch in iOS. It just closes the app
        context.driver.activate_app(context.driver.capabilities['bundleId'])
    else:
        context.driver.activate_app(context.driver.capabilities['appPackage'])


@when('authenticates with thier biometrics')
def step_impl(context):
    # Check to see if the Biometrics page is displayed
    #if ('autoGrantPermissions' in context.driver.capabilities and context.driver.capabilities['autoGrantPermissions'] == False) or (context.driver.capabilities['platformName'] == 'iOS'):
    if (context.driver.capabilities['platformName'] == 'iOS'):
        context.thisBiometricsPage = BiometricsPage(context.driver)
        assert context.thisBiometricsPage.on_this_page()
        context.device_service_handler.biometrics_authenticate(True)
        assert context.thisBiometricsPage.on_this_page() == False
        context.thisInitialzationPage.wait_until_initialized()


@when('fails to authenticate with thier biometrics once')
def step_impl(context):
    if hasattr(context, 'thisBiometricsPage') == False:
        context.thisBiometricsPage = BiometricsPage(context.driver)

    assert context.thisBiometricsPage.on_this_page()
    context.device_service_handler.biometrics_authenticate(False)
    #assert context.thisBiometricsPage.on_this_page()


@when('the Holder authenticates with thier incorrect PIN as {pin}')
@when('authenticates with thier PIN as "{pin}"')
def step_impl(context, pin):
    if hasattr(context, 'thisPINPage') == False:
        context.thisPINPage = PINPage(context.driver)
    context.thisPINPage.enter_pin(pin)
    context.thisPINPage.select_enter()

@then('the application is locked for 1 minute')
def step_impl(context):
    context.thisTemporarilyLockedPage = TemporarilyLockedPage(context.driver)
    assert context.thisTemporarilyLockedPage.on_this_page()
    
@when('they enter thier PIN as "{pin}"')
def step_impl(context, pin):
    if hasattr(context, 'thisPINPage') == False:
        context.thisPINPage = PINPage(context.driver)

    context.thisPINPage.enter_pin(pin)

    context.thisInitializationPage = context.thisPINPage.select_enter()


@then('they are informed that the PINs do not match')
def step_impl(context):
    context.thisPINSetupPage.does_pin_match()


@then('they select ok on PINs do not match')
def step_impl(context):
    context.thisPINSetupPage.select_ok_on_modal()


@then('they are informed of {pin_error}')
def step_impl(context, pin_error):
    if hasattr(context, "thisPINPage") == True:
        assert context.thisPINPage.get_error() == pin_error
    else:
        assert context.thisPINSetupPage.get_error() == pin_error            
