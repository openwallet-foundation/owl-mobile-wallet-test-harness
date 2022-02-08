
"""
-----------------------------------------------------------
Behave Step Definitions for a onboarding a new user.

-----------------------------------------------------------

"""
# 
from behave import given, when, then
from typing import TypeVar
import sys
# pageObject Imports
# Why are Python imports still so terrible?
sys.path.append("../../pageobjects/ODS/onboarding")
from onboarding import onboarding


T = TypeVar('T')
"""
    Scenario: New user navigates to device's security settings

"""
@given('I am on Get started screen')
def step_1(context:T) -> None:
    context.initialOnboarding = OB.initialOnboarding()
    print('strongly typed > loosely typed')

    # multiple and are essentially a repeat of the previous1
