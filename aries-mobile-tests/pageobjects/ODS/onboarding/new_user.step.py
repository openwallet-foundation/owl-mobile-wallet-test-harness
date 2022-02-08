
"""
-----------------------------------------------------------
Behave Step Definitions for a onboarding a new user.

-----------------------------------------------------------

"""
# 
from behave import given, when, then
from typing import TypeVar
# pageObject Imports
# Why are Python imports still so terrible?
# INFO: I give up with sys append and path lib and
# https://stackoverflow.com/questions/14132789/relative-imports-for-the-billionth-time

from  onboarding import initialOnboarding


T = TypeVar('T')
"""
    Scenario: New user navigates to device's security settings

"""
@given('I am on Get started screen')
def stepGiven1(context) -> None:
    context.initialOnboarding = initialOnboarding(context)
    context.initialOnboarding.selectGetStartedBtn()

@when("I click on Check your device's security settings")

    # multiple and are essentially a repeat of the previous1
