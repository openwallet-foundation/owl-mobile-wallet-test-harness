from bc_wallet.terms import *
from override_steps import overrides


@overrides("the User has completed on-boarding", "given")
def user_has_completed_onboarding_step_impl(context):
    context.execute_steps(
        f"""
            Given the new user has opened the app for the first time
            And the user is on the onboarding Welcome screen
            When the user selects Next
            And they are brought to the Store your credentials securely screen
            And the user selects Next
            And they are brought to the Share only what is neccessary screen
            And the user selects Next
            And they are brought to the Take control of your information screen
            Then they can select Get started
        """
    )


@given("the User has skipped on-boarding")
def step_impl(context):
    context.execute_steps(
        f"""
            Given the new user has opened the app for the first time
            And the user is on the onboarding Welcome screen
            When the user selects Skip
            Then are brought to the Terms and Conditions screen 
        """
    )


@overrides("the users accepts the Terms and Conditions", "given")
@overrides("the users accepts the Terms and Conditions", "when")
def accept_terms_step_impl(context):
    context.thisTermsAndConditionsPage.select_accept()


@overrides("the user was taken back to the on-boarding screen", "given")
@overrides("the User goes back to the last on-boarding screen they viewed", "then")
def user_goes_back_to_onboarding_or_back_to_last_onboarding_screen_step_impl(context):
    assert context.thisOnboardingTakeControlPage.on_this_page()
