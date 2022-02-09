"""
-----------------------------------------------------------
Behave Step Definitions for a onboarding a new user.

-----------------------------------------------------------
"""
from behave import given, when, then
from typing import TypeVar

# PageObject
from onboarding import initialOnboarding
from termsAndConditions import termsAndConditions
from explainerPages import explainerPages
from touchIDBiometrics import touchIDBiometrics

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


"""
  @DID-
  Scenario: New user reviews all explainer screens 

"""


@given("My language has been set")
def stepGivenNewUser2(context) -> None:
    pass


@given("I am on Get started screen")
def stepGivenNewUser2And1(context) -> None:
    context.initialOnboarding = initialOnboarding(context)
    assert (
        context.initialOnboarding.rightPage() is True
    ), "You are not on the Get Started Page"


@when("I click on Get started")
def stepWhenNewUser2(context) -> None:
    assert (
        context.initialOnboarding.selectGetStartedBtn() is True
    ), "Can't find or click the Get started Btn"


@when("I accept Terms of service")
def stepWhenNewUser2And1(context) -> None:
    context.termsAndConditions = termsAndConditions(context)
    context.termsAndConditions.checkTOSBox()


@when("I click Continue on Terms of Use")
def stepWhenNewUser2And2(context) -> None:
    context.termsAndConditions.selectContinueBtn()


@when("I land on Store credentials screen")
def stepWhenNewUser2And3(context) -> None:
    # BUG: what is the store credential screen? explainerscreens?
    context.explainerPages = explainerPages(context)
    context.index = 0


@when("I click Next")
def stepWhenNewUser2And4(context) -> None:
    context.index = context.explainerPages.selectNextBtn(context.index)
    assert context.index == 1, "something went wrong in moving forward"


@when("I land on Share only necessary screen")
def stepWhenNewUser2And5(context) -> None:
    pass


@when("I click Next")
def stepWhenNewUser2And6(context) -> None:
    context.index = context.explainerPages.selectNextBtn(context.index)
    assert context.index == 2, "something went wrong in moving forward"


@when("I land on Keep track of what you shared screen")
def stepWhenNewUser2And7(context) -> None:
    pass


@when("I click Done")
def stepWhenNewUser2And8(context) -> None:
    context.explainerPages.selectNextBtn(context.index)
    assert context.index == 2, "something went wrong in moving forward"


@then("I am on Confirm your biometrics screen")
def stepThenNewUser2(context) -> None:
    context.touchIDBiometrics = touchIDBiometrics(context)
    assert context.touchIDBiometrics is True, "You are not on the biometric page"
