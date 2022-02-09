"""
-----------------------------------------------------------
Behave Step Definitions for a onboarding a new user.

-----------------------------------------------------------
"""
from behave import given, when, then
from typing import TypeVar
from onboarding import initialOnboarding


"""
    @DID-372
    Scenario: New user navigates to device's security settings

"""

@given("I am on Get started screen")
def stepGivenNewUser1(context) -> None:
    context.initialOnboarding = initialOnboarding(context)
        assert (
        context.initialOnboarding.selectGetStartedBtn() == True
    ), "We are not on the onboard screen"


@when("I click on Check your device's security settings")
def stepWhenNewUser1(context) -> None:
    assert (
        context.initialOnboarding.selectSecuritySettings() == True
    ), "Unable to navigate to the security setting page"


@then("I land on Device settings screen")
def stepThenNewUser1(context) -> None:
    # INFO: Weak test as I don't know what the general accessibility_id would be (think and rework)
    # link object
    assert (
        context.initialOnboarding.selectGetStartedBtn() == False
    ), "We are still on the onboard screen"

    # multiple and are essentially a repeat of the previous1


"""
  @DID-
  Scenario: New user reviews all explainer screens 

"""
@given("My langauage has been set")
def stepGivenNewUser2(context) -> None:
    pass 


@given("My langauage has been set")
def stepGivenNewUser2And1(context) -> None:
    pass

@when("I click on Get started")
def stepWhenNewUser2(context) -> None:
