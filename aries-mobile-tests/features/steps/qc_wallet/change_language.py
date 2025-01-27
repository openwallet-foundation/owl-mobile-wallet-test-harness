# -----------------------------------------------------------
# Behave Step Definitions for Changing language
#
# -----------------------------------------------------------

from time import sleep, time

# Local Imports
from agent_controller_client import (
    agent_controller_GET,
    agent_controller_POST,
    expected_agent_state,
    setup_already_connected,
)
from agent_test_utils import get_qr_code_from_invitation
from behave import given, then, when
from pageobjects.bc_wallet.biometrics import BiometricsPage
from pageobjects.bc_wallet.pin import PINPage
from pageobjects.qc_wallet.home import HomePageQC
from pageobjects.qc_wallet.settings import SettingsPageQC
from pageobjects.qc_wallet.languageform import LanguageFormPageQC
from pageobjects.qc_wallet.moreoptions import MoreOptionsPageQC

# import Page Objects needed
# from pageobjects.bc_wallet.languagesplash import LanguageSplashPage


@given('the holder has initially selected "{language}" as the language')
def initial_lang_step_impl(context, language):
    if str(context.driver.capabilities["platformName"]).lower() == "Android".lower():
        language_from_capabitilies = (
            "English" if context.driver.capabilities["language"] == "en" else "French"
        )
    else:
        args_list = context.driver.capabilities["processArguments"]["args"]
        appleLanguagesIndex = args_list.index("-AppleLanguages")
        if (
            appleLanguagesIndex + 1 < len(args_list)
            and args_list[appleLanguagesIndex + 1] == "(en)"
        ):
            language_from_capabitilies = "English"
        else:
            language_from_capabitilies = "French"
    assert language == language_from_capabitilies


@given("the holder open the Application settings page")
def change_lang_step_impl(context):
    context.execute_steps(
        f"""
            Given the User has accepted the Terms and Conditions
            And a PIN has been set up with "369369"
            Then the User transitions to biometric screen
            When the user click continue on the biometrics screen 
            Then the user land on the Home screen
        """
    )
    context.thisMoreOptionsPageQC= context.thisHomePageQC.select_more()
    context.thisSettingsPageQC= context.thisMoreOptionsPageQC.select_applicationSettings()


@given('they have selected "{different_language}"')
@when('the holder changes app language to "{different_language}"')
def change_lang_step_impl(context, different_language):
    if hasattr(context, "thisSettingsPageQC") == False:
        context.thisSettingsPageQC = SettingsPageQC(context.driver)
    # context.thisSettingsPageQC = SettingsPageQC(context.driver)
    context.thisLanguageFormPageQC = context.thisSettingsPageQC.select_language()
    context.thisLanguageFormPageQC.select_language(different_language)


@then('the language changes automatically to "{different_language}"')
def confirm_lang_change_step_impl(context, different_language):
    assert context.thisLanguageFormPageQC.get_current_language() == different_language

@then('the language is set to "{different_language}"')
def verify_lang_change_on_relaunch_app_step_impl(context, different_language):
    # LambdaTest does not support biometric authentication
    if type(context.device_service_handler).__name__ != "LambdaTestHandler":
        sleep(5)
        context.thisBiometricsPage = BiometricsPage(context.driver)
        assert context.thisBiometricsPage.on_this_page(different_language)
    else:
        sleep(5)
        context.thisPINPage = PINPage(context.driver)
        assert context.thisPINPage.on_this_page(different_language)