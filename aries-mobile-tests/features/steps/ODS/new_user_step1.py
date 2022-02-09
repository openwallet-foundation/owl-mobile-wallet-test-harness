"""
-----------------------------------------------------------
Behave Step Definitions for a onboarding a new user.

-----------------------------------------------------------
"""
from behave import given, when, then
from typing import TypeVar

# PageObject
from pageobjects.ODS.onboarding.initialOnboarding import initialOnboarding
from pageobjects.ODS.onboarding.termsAndConditions import termsAndConditions
from pageobjects.ODS.onboarding.explainerPages import explainerPages
from pageobjects.ODS.onboarding.touchIDBiometrics import touchIDBiometrics

"""
    @DID-372
    Scenario: New user navigates to device's security settings

"""


@given("I am on Get started screen")
def stepGivenNewUser1(context) -> None:
    context.initialOnboarding = initialOnboarding(context)
    assert (
        context.initialOnboarding.selectGetStartedBtn() is True
    ), "We are not on the onboard screen"


@when("I click on Check your device's security settings")
def stepWhenNewUser1(context) -> None:
    assert (
        context.initialOnboarding.selectSecuritySettings() is True
    ), "Unable to navigate to the security setting page"


@then("I land on Device settings screen")
def stepThenNewUser1(context) -> None:
    # INFO: Weak test as I don't know what the general accessibility_id would be (think and rework)
    # link object
    assert (
        context.initialOnboarding.selectGetStartedBtn() is False
    ), "We are still on the onboard screen"


# multiple and are essentially a repeat of the previous1


