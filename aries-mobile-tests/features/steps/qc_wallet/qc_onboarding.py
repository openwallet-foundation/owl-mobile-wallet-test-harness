from behave import given, then, when
from pageobjects.qc_wallet.onboardingsharenecessary import \
    OnboardingShareNecessaryPageQC
from pageobjects.qc_wallet.onboardingstorecredssecurely import \
    OnboardingStoreCredsSecurelyPageQC
from pageobjects.qc_wallet.onboardingtakecontrol import \
    OnboardingTakeControlPageQC
from pageobjects.qc_wallet.onboardingwelcome import OnboardingWelcomePageQC


@given("the new user has opened the app for the first time")
def special_step_impl(context):
    # App opened already buy appium.
    # Intialize the page we should be on
    context.thisOnboardingWelcomePage = OnboardingWelcomePageQC(context.driver)


@given("the user is on the onboarding Welcome screen")
def user_is_on_welcome_screen_impl(context):
    assert context.thisOnboardingWelcomePage.on_this_page()
    # set a current onboarding page so the select Next step can be reused across these pages
    context.currentOnboardingPage = context.thisOnboardingWelcomePage


@when("the user selects Next")
def step_impl(context):
    thisOnboardingPage = context.currentOnboardingPage.select_next()
    if type(thisOnboardingPage) == OnboardingStoreCredsSecurelyPageQC:
        context.thisOnboardingStoreCredsSecurelyPage = thisOnboardingPage
    elif type(thisOnboardingPage) == OnboardingTakeControlPageQC:
        context.thisOnboardingTakeControlPage = thisOnboardingPage
    elif type(thisOnboardingPage) == OnboardingShareNecessaryPageQC:
        context.thisOnboardingShareNecessaryPage = thisOnboardingPage


@when("they are brought to the Store your credentials securely screen")
def on_cred_secure_screen_step_impl(context):
    assert context.thisOnboardingStoreCredsSecurelyPage.on_this_page()
    # set a current onboarding page so the select Next step can be reused across these pages
    context.currentOnboardingPage = context.thisOnboardingStoreCredsSecurelyPage


@when("they are brought to the Share only what is neccessary screen")
def on_share_only_necessary_screen_step_impl(context):
    assert context.thisOnboardingShareNecessaryPage.on_this_page()
    # set a current onboarding page so the select Next step can be reused across these pages
    context.currentOnboardingPage = context.thisOnboardingShareNecessaryPage


@when("they are brought to the Take control of your information screen")
def on_take_control_info_screen_step_impl(context):
    assert context.thisOnboardingTakeControlPage.on_this_page()
    # set a current onboarding page so the select Next step can be reused across these pages
    context.currentOnboardingPage = context.thisOnboardingTakeControlPage


@then("they can select Get started")
def get_started_step_impl(context):
    context.thisOnboardingTakeControlPage = OnboardingTakeControlPageQC(context.driver)
    context.thisTermsAndConditionsPage = (
        context.thisOnboardingTakeControlPage.select_get_started()
    )


@then("are brought to the Terms and Conditions screen")
def on_terms_and_conditions_screen_step_impl(context):
    assert context.thisTermsAndConditionsPage.on_this_page()


@given('the user is on the "{screen}"')
@given("the user is on the onboarding {screen}")
def user_is_on_screen_step_impl(context, screen):
    # Assume for now they start on the welcome screen

    # Detemrine what onboarding screen they are on, then migrate them to the screen passed in.
    if screen == "Welcome screen":
        # at the start of a test call the intial steps.
        context.execute_steps(
            f"""
            Given the user is on the onboarding Welcome screen
        """
        )

    elif screen == "Store your credentials securely screen":
        context.execute_steps(
            f"""
            Given the user is on the onboarding Welcome screen
            When the user selects Next
            And they are brought to the Store your credentials securely screen
        """
        )

    elif screen == "Share only what is neccessary screen":
        context.execute_steps(
            f"""
            Given the user is on the onboarding Welcome screen
            When the user selects Next
            And they are brought to the Store your credentials securely screen
            And the user selects Next
            And they are brought to the Share only what is neccessary screen
        """
        )
    elif screen == "Take control of your information screen":
        context.execute_steps(
            f"""
            Given the user is on the onboarding Welcome screen
            When the user selects Next
            And they are brought to the Store your credentials securely screen
            And the user selects Next
            And they are brought to the Share only what is neccessary screen
            And the user selects Next
            And they are brought to the Take control of your information screen
        """
        )
    else:
        raise Exception(f"Unexpected screen, {screen}")


@when("the user selects Skip")
def user_skips_onboarding_step_impl(context):
    context.thisTermsAndConditionsPage = context.currentOnboardingPage.select_skip()


@when("the user selects Back")
def user_selects_back_on_onboarding_screens_step_impl(context):
    thisOnboardingPage = context.currentOnboardingPage.select_back()
    if type(thisOnboardingPage) == OnboardingWelcomePageQC:
        context.thisOnboardingWelcomePage = thisOnboardingPage
        context.currentOnboardingPage = context.thisOnboardingWelcomePage
    if type(thisOnboardingPage) == OnboardingStoreCredsSecurelyPageQC:
        context.thisOnboardingStoreCredsSecurelyPage = thisOnboardingPage
        context.currentOnboardingPage = context.thisOnboardingStoreCredsSecurelyPage
    elif type(thisOnboardingPage) == OnboardingTakeControlPageQC:
        context.thisOnboardingTakeControlPage = thisOnboardingPage
        context.currentOnboardingPage = context.thisOnboardingTakeControlPage
    elif type(thisOnboardingPage) == OnboardingShareNecessaryPageQC:
        context.thisOnboardingShareNecessaryPage = thisOnboardingPage
        context.currentOnboardingPage = context.thisOnboardingShareNecessaryPage


@then("are brought to the {previous_screen}")
def user_is_taken_to_prev_screen_step_impl(context, previous_screen):
    if previous_screen == "Welcome screen":
        assert context.thisOnboardingWelcomePage.on_this_page()
    elif previous_screen == "Store your credentials securely screen":
        assert context.thisOnboardingStoreCredsSecurelyPage.on_this_page()
    elif previous_screen == "Share only what is neccessary screen":
        assert context.thisOnboardingShareNecessaryPage.on_this_page()


@when("the user quits the app")
def user_quits_app_step_impl(context):
    # close the app and reopen
    context.driver.reset()


@when("they reopen the app")
def user_reopen_app_step_impl(context):
    # app was opened in the driver.reset() call in the last step.
    pass


@then("they land on the Welcome screen")
def step_impl(context):
    context.execute_steps(
        f"""
        Given the new user has opened the app for the first time
        Given the user is on the onboarding Welcome screen
    """
    )
