# """
# -----------------------------------------------------------
# Behave Step Definitions for a onboarding a new user.

# -----------------------------------------------------------
# """
# from behave import given, when, then

# # PageObject
# from pageobjects.ODS.onboarding.initialOnboarding import initialOnboarding
# from pageobjects.ODS.onboarding.termsAndConditions import termsAndConditions
# from pageobjects.ODS.onboarding.explainerPages import explainerPages
# from pageobjects.ODS.onboarding.touchIDBiometrics import touchIDBiometrics

# """
#   @DID-
#   Scenario: New user reviews all explainer screens 

# """


# @given("My language has been set")
# def stepGivenNewUser2(context) -> None:
#     pass


# @given("I am on Get started screen")
# def stepGivenNewUser2And1(context) -> None:
#     context.initialOnboarding = initialOnboarding(context)
#     assert (
#         context.initialOnboarding.rightPage() is True
#     ), "You are not on the Get Started Page"


# @when("I click on Get started")
# def stepWhenNewUser2(context) -> None:
#     assert (
#         context.initialOnboarding.selectGetStartedBtn() is True
#     ), "Can't find or click the Get started Btn"


# @when("I accept Terms of service")
# def stepWhenNewUser2And1(context) -> None:
#     context.termsAndConditions = termsAndConditions(context)
#     context.termsAndConditions.checkTOSBox()


# @when("I click Continue on Terms of Use")
# def stepWhenNewUser2And2(context) -> None:
#     context.termsAndConditions.selectContinueBtn()


# @when("I land on Store credentials screen")
# def stepWhenNewUser2And3(context) -> None:
#     # BUG: what is the store credential screen? explainerscreens?
#     context.explainerPages = explainerPages(context)
#     context.index = 0


# @when("I click Next")
# def stepWhenNewUser2And4(context) -> None:
#     context.index = context.explainerPages.selectNextBtn(context.index)
#     assert context.index == 1, "something went wrong in moving forward"


# @when("I land on Share only necessary screen")
# def stepWhenNewUser2And5(context) -> None:
#     pass


# @when("I click Next")
# def stepWhenNewUser2And6(context) -> None:
#     context.index = context.explainerPages.selectNextBtn(context.index)
#     assert context.index == 2, "something went wrong in moving forward"


# @when("I land on Keep track of what you shared screen")
# def stepWhenNewUser2And7(context) -> None:
#     pass


# @when("I click Done")
# def stepWhenNewUser2And8(context) -> None:
#     context.explainerPages.selectNextBtn(context.index)
#     assert context.index == 2, "something went wrong in moving forward"


# @then("I am on Confirm your biometrics screen")
# def stepThenNewUser2(context) -> None:
#     context.touchIDBiometrics = touchIDBiometrics(context)
#     assert context.touchIDBiometrics is True, "You are not on the biometric page"

