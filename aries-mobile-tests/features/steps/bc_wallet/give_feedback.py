# -----------------------------------------------------------
# Behave Step Definitions for Wallet Users giving feedback
#
# -----------------------------------------------------------

from behave import given, when, then
import json

# Local Imports

# import Page Objects needed


@given('the wallet user has just onboarded')
def step_impl(context):
    context.execute_steps('''
      Given the User has completed on-boarding
      And the User has accepted the Terms and Conditions
      And a PIN has been set up with "369369"
      And the User allows notifications
      And the Holder has selected to use biometrics to unlock BC Wallet
    ''')


@given('they are on on the landing page')
def step_impl(context):
    context.execute_steps('''
        Then they land on the Home screen
    ''')


@when('they select Give Feedback')
def step_impl(context):
    context.thisFeedbackPage = context.thisHomePage.select_give_feedback()


@then('they are taken to the Feedback form')
def step_impl(context):
    assert context.thisFeedbackPage.on_this_page()
    # select exit to go back to the home page
    context.thisFeedbackPage.select_exit()
    # assert we are back on the home page
    assert context.thisHomePage.on_this_page()

