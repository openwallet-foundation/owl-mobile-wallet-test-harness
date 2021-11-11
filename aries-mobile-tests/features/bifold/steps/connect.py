# -----------------------------------------------------------
# Behave Step Definitions for Connecting an issuer to a wallet user
# 
# -----------------------------------------------------------

from behave import given, when, then
import json

# Local Imports
from agent_controller_client import agent_controller_GET, agent_controller_POST, expected_agent_state, setup_already_connected
# import Page Objects needed
from pageobjects.bifold.termsofservice import TermsOfServicePage
from pageobjects.bifold.pinsetup import PINSetupPage
from pageobjects.bifold.home import HomePage

# Instantiate the page objects needed
# Can I pass the context here on instantiation or should we do it in the steps? 
# We could put a page factory somewhere that instantiates all pages for a given app. 
thisTermOfServicePage = TermsOfServicePage()
thisPINSetupPage = PINSetupPage()
thisHomePage = HomePage()

@given('the terms of service has been accepted')
def step_impl(context):
    thisTermOfServicePage.select_accept(context)
    thisPINSetupPage = thisTermOfServicePage.submit(context)

@given('a PIN has been set up')
def step_impl(context):
    # TODO Move the data into the feature file
    thisPINSetupPage.enter_pin(context, "369369")
    thisPINSetupPage.enter_second_pin(context, "369369")
    thisHomePage = thisPINSetupPage.create_pin(context)

@when('the wallet user scans the QR code sent by the issuer')
def step_impl(context):
    thisScanPage = thisHomePage.select_scan(context)
    #thisScanPage.

@when('accepts the connection')
def step_impl(context):
    # click yes on notification? 
    pass

@then('there is a connection between Issuer and wallet user')
def step_impl(context):
    # Check the connections for a new connection
    pass
    
