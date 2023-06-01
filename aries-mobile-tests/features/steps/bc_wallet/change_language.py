# -----------------------------------------------------------
# Behave Step Definitions for Changing language
# 
# -----------------------------------------------------------

from time import sleep, time
from behave import given, when, then

# Local Imports
from agent_controller_client import agent_controller_GET, agent_controller_POST, expected_agent_state, setup_already_connected
from agent_test_utils import get_qr_code_from_invitation
from pageobjects.bc_wallet.biometrics import BiometricsPage
from pageobjects.bc_wallet.home import HomePage
from pageobjects.bc_wallet.pin import PINPage
# import Page Objects needed
# from pageobjects.bc_wallet.languagesplash import LanguageSplashPage

@given('the holder has initially selected "{language}" as the language')
def initial_lang_step_impl(context, language):
    if str(context.driver.capabilities['platformName']).lower() == 'Android'.lower():
        language_from_capabitilies = "English" if context.driver.capabilities["language"] == "en" else "French"
    else:
        language_from_capabitilies = "English" if "en" in context.driver.capabilities["locale"] else "French"
    assert language == language_from_capabitilies 

@given('the holder is in the language settings')
def lang_settings_step_impl(context):
    context.execute_steps(f'''
            Given the User has skipped on-boarding
            And the User has accepted the Terms and Conditions
            And a PIN has been set up with "369369"
            And the Holder has selected to use PIN only to unlock BC Wallet
            Then they land on the Home screen
        ''') 

@given('they have selected "{different_language}"')
@when('the holder changes app language to "{different_language}"')
def change_lang_step_impl(context, different_language):
    if hasattr(context, 'thisHomePage') == False:
        context.thisHomePage = HomePage(context.driver)

    context.thisSettingsPage = context.thisHomePage.select_settings()
    context.thisLanguageFormPage = context.thisSettingsPage.select_language()
    context.thisLanguageFormPage.select_language(different_language)

@then('the language changes automatically to "{different_language}"')
def confirm_lang_change_step_impl(context, different_language):
    assert context.thisLanguageFormPage.get_title(different_language)

@then('the language is set to "{different_language}"')
def verify_lang_change_on_relaunch_app_step_impl(context, different_language):
    sleep(5)
    if context.device_service_handler.supports_biometrics():
        context.thisBiometricsPage = BiometricsPage(context.driver)
        assert context.thisBiometricsPage.on_this_page(different_language)
    else:
        context.thisPINPage = PINPage(context.driver)
        assert context.thisPINPage.on_this_page(different_language)


