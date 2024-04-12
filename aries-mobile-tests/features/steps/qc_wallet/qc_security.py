from time import sleep, time

from bc_wallet.security import *
from override_steps import overrides
from pageobjects.qc_wallet.biometrics import BiometricsPageQC
from pageobjects.qc_wallet.pin import PINPageQC


@overrides("the User allows notifications", "step")
def step_enable_notifications(context):
    pass


@overrides("the Holder has selected to use PIN only to unlock BC Wallet", "given")
def user_selects_only_pin_auth_step_impl(context):
    assert context.thisOnboardingBiometricsPage.on_this_page()
    context.thisInitializationPage = (
        context.thisOnboardingBiometricsPage.select_continue()
    )


@overrides("the User selects to use Biometrics", "when")
def user_selects_biometrics_step_impl(context):
    if context.device_service_handler.supports_biometrics():
        assert context.thisOnboardingBiometricsPage.select_biometrics()
        context.device_service_handler.biometrics_authenticate(True)
        context.thisInitializationPage = (
            context.thisOnboardingBiometricsPage.select_continue()
        )
    else:
        context.thisInitializationPage = (
            context.thisOnboardingBiometricsPage.select_continue()
        )
        sleep(3)


@overrides("authenticates with thier biometrics", "when")
def auth_biometrics_step_impl(context):
    # Check to see if the Biometrics page is displayed
    # if ('autoGrantPermissions' in context.driver.capabilities and context.driver.capabilities['autoGrantPermissions'] == False) or (context.driver.capabilities['platformName'] == 'iOS'):
    if context.device_service_handler.supports_biometrics():
        context.thisBiometricsPage = BiometricsPageQC(context.driver)
        context.device_service_handler.biometrics_authenticate(True)
        assert context.thisBiometricsPage.on_this_page() == False
        context.thisInitializationPage.wait_until_initialized()
    else:
        context.execute_steps(
            f"""
            When authenticates with thier PIN as "369369"
            Then they have access to the app
        """
        )


@overrides("fails to authenticate with thier biometrics once", "when")
def fails_biometrics_step_impl(context):
    if context.device_service_handler.supports_biometrics():
        if hasattr(context, "thisBiometricsPage") == False:
            context.thisBiometricsPage = BiometricsPageQC(context.driver)

        context.device_service_handler.biometrics_authenticate(False)
        assert context.thisBiometricsPage.on_this_page() == True
        sleep(10)
        context.thisBiometricsPage.dismiss_biometrics_modal()
    else:
        pass


@overrides("the Holder authenticates with thier incorrect PIN as {pin}", "when")
def user_enters_wrong_pin_step_impl(context, pin):
    if hasattr(context, "thisPINPage") == False:
        context.thisPINPage = PINPageQC(context.driver)
    context.thisPINPage.enter_pin(pin)
    context.thisPINPage.select_enter()


@overrides('they enter thier PIN as "{pin}"', "when")
def user_enter_their_pin_step_impl(context, pin):
    print("user enter their pin")
    if hasattr(context, "thisPINPage") == False:
        context.thisPINPage = PINPageQC(context.driver)

    context.thisPINPage.enter_pin(pin)

    context.thisInitializationPage = context.thisPINPage.select_enter()


@then('they select visibility toggle on the first PIN as "{pin}"')
def visibility_toggle_first_pin_step_impl(context, pin):
    assert pin == context.thisPINSetupPage.get_pin()


@then('they select visibility toggle on the second PIN as "{pin}"')
def visibility_toggle_second_pin_step_impl(context, pin):
    assert pin == context.thisPINSetupPage.get_second_pin()


@overrides("the User selects Create PIN", "when")
@overrides("the User selects Create PIN", "then")
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


@then("they select ok on PINs error")
def select_ok_on_error_step_impl(context):
    if hasattr(context, "thisPINPage") == True:
        context.thisPINPage.select_ok_on_modal()
    else:
        context.thisPINSetupPage.select_ok_on_modal()


@overrides("they are informed that the PINs do not match", "then")
def step_impl(context):
    assert context.thisPINSetupPage.get_error() == "PINs do not match"


@overrides("they have access to the app with the new PIN", "then")
def step_access_app_with_pin(context):
    assert context.thisSettingsPage.on_this_page()
    context.thisHomePage = context.thisSettingsPage.select_back()
    assert context.thisHomePage.on_this_page()

    context.execute_steps(
        """
        Given they have closed the app
        When they relaunch the app
    """
    )

    context.thisBiometricsPage = BiometricsPageQC(context.driver)
    if context.thisBiometricsPage.on_this_page():
        context.execute_steps(
            """
            When fails to authenticate with thier biometrics once
        """
        )

    context.execute_steps(
        """
        When they enter thier PIN as "963963"
        Then they have access to the app
    """
    )


@overrides("the User has successfully updated PIN", "when")
@overrides("the User has successfully updated PIN", "then")
def step_select_update_pin(context):
    assert context.thisChangePINPage.successfully_changed_pin_modal.is_displayed()
    context.thisSettingsPage = (
        context.thisChangePINPage.successfully_changed_pin_modal.select_okay()
    )


@overrides("they land on the Home screen", "then")
@overrides("initialization ends (failing silently)", "when")
@overrides("they have access to the app", "then")
@overrides("the User has successfully created a PIN", "then")
def special_step_impl(context):
    # The Home page will not show until the initialization page is done.
    # assert context.thisInitializationPage.on_this_page()
    context.thisHomePage = context.thisInitializationPage.wait_until_initialized()
    if context.thisHomePage.welcome_to_bc_wallet_modal.is_displayed():
        print("MODAL ON HOME PAGE")
        context.thisHomePage.welcome_to_bc_wallet_modal.select_dismiss()
        assert True
    else:
        assert context.thisHomePage.on_this_page()
    context.thisNavBar = NavBar(context.driver)
    if context.thisHomePage.on_this_page() == False:
        sleep(5)
    assert context.thisHomePage.on_this_page()


@when("the Holder stops interacting with the app")
def stop_interaction_impl(context):
    context.driver.background_app(-1)
    context.last_time_active = time()
    pass


@then("the app is locked for security reasons and a message is shown to the Holder")
def lock_app_impl(context):
    lock_timer = 0
    for row in context.table:
        lock_timer = int(row["lock_time"])
    sleep(lock_timer)
    if time() - context.last_time_active > 300:
        if str(context.driver.capabilities["platformName"]).lower() == "iOS".lower():
            context.driver.activate_app(context.driver.capabilities["bundleId"])
        else:
            context.driver.activate_app(context.driver.capabilities["appPackage"])

        if hasattr(context, "thisPINPage") == False:
            context.thisPINPage = PINPage(context.driver)
        lock_message = None
        for row in context.table:
            lock_message = row["lock_message"]
        assert context.thisPINPage.get_error() == lock_message
