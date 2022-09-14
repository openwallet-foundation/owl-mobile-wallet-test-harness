# -----------------------------------------------------------
# Behave Step Definitions for Offline Handling Steps.
#
# -----------------------------------------------------------

from behave import given, when, then
import json
import os
from time import sleep

# Local Imports
from agent_controller_client import agent_controller_GET, agent_controller_POST, expected_agent_state, setup_already_connected
from agent_test_utils import get_qr_code_from_invitation
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.touch_action import TouchAction
# import Page Objects needed
from pageobjects.bc_wallet.no_internet_toast_notification import NoInternetConnectionToastNotification

@when('the mobile phone does not have an internet connection')
@given('the mobile phone does not have an internet connection')
def step_impl(context):
    if context.driver.capabilities['platformName'] == 'iOS':
        height = WebDriverWait(context.driver, 30).until(
                EC.presence_of_element_located((MobileBy.CLASS_NAME, "UIAWindow"))
            ).size["height"]
        width = WebDriverWait(context.driver, 30).until(
                EC.presence_of_element_located((MobileBy.CLASS_NAME, "UIAWindow"))
            ).size["width"]
        if '6' in context.driver.capabilities['testobject_device_name']:
            # Access Control panel with a swipe up from the bottom
            #context.driver.swipe(width-(width * .13), 0, height-(height * .60), height*.75, 500)
            #context.driver.swipe(width-(width * .5), 0, height-(height * .50), height*.5, 500)
            context.driver.swipe(width-100, height, width-100, height-200, 500);
            actions = TouchAction(context.driver)
            actions.tap(x = width * .25, y = height * .30).release().perform() #Wi-Fi
            #actions.tap(x = width * .50, y = height * .65).release().perform() #Click ok on possible turn off for a day.
            actions.tap(x = width * .75, y = height * .75).release().perform() # close control panel 
        else:
            # Access Control Center by Swiping down from the upper right corner

            # window_size = context.driver.get_window_size()  # this returns dictionary
            # el = context.driver.find_element(*self.configuration.CommonScreen.WEB_VIEW)
            # action = TouchAction(self.driver)
            # start_x = window_size["width"] * 0.5
            # start_y = window_size["height"]
            # end_x = window_size["width"] * 0.5
            # end_y = window_size["height"] * 0.5
            # action.press(el, start_x, start_y).wait(100).move_to(el, end_x, end_y).release().perform()

            # height = context.driver.findElementByClassName(
            #     "UIAWindow").getSize().getHeight()

            # width = context.driver.findElementByClassName(
            #     "UIAWindow").getSize().getWidth()

            # Swipe up from the bottom - older iphones
            #context.driver.swipe(width-100, height, width-100, height-200, 500)
            # Swipe down from the top right - newer iphones
            #context.driver.swipe(width-50, 0, width-50, 0+200, 500)
            context.driver.swipe(width-(width * .13), 0, height-(height * .60), height*.75, 500)
            #context.driver.swipe(width, startPoint, width, endPoint, duration)
            # context.driver.findElementByAccessibilityId("Wi-Fi").click()

            actions = TouchAction(context.driver)
            #actions.tap(x = width * .25, y = height * .25).release().perform() #airplane mode
            actions.tap(x = width * .25, y = height * .30).release().perform() #Wi-Fi
            actions.tap(x = width * .50, y = height * .65).release().perform() #Click ok on possible turn off for a day.
            actions.tap(x = width * .75, y = height * .75).release().perform() # close control panel 
            # actions.tap_and_hold(20, 20)
            # actions.move_to(10, 100)
            # actions.release()
            # actions.perform()

    else:
        context.driver.set_network_connection(0)


@when('BC Wallet suddenly goes back online')
def step_impl(context):
    if context.driver.capabilities['platformName'] == 'iOS':
        # Get screen height
        height = WebDriverWait(context.driver, 30).until(
            EC.presence_of_element_located((MobileBy.CLASS_NAME, "UIAWindow"))
        ).size["height"]
        # Get screen width
        width = WebDriverWait(context.driver, 30).until(
            EC.presence_of_element_located((MobileBy.CLASS_NAME, "UIAWindow"))
        ).size["width"]

        # swipe down on the right to open control center
        context.driver.swipe(width-50, 0, width-50, 0+200, 500)

        action = TouchAction(context.driver)
        # tap Wi-Fi to turn on
        action.tap(x = width * .25, y = height * .30).release().perform()
        # tap in empty space to close control center
        action.tap(x = width * .75, y = height * .75).release().perform() # close control panel 

    else:
        context.driver.set_network_connection(6)


@then('they are presented with a dismissible "{no_internet_connection_msg}" toast notification')
def step_impl(context, no_internet_connection_msg):
    if hasattr(context, 'thisNoInternetNotification') == False:
        context.thisNoInternetNotification = NoInternetConnectionToastNotification(context.driver)

    # Notification Should be displayed
    assert context.thisNoInternetNotification.on_this_page()
    # Close the notification by clicking on it
    context.thisNoInternetNotification.dismiss_notification()
    # Check to make sure the notification is gone
    sleep(5)
    assert context.thisNoInternetNotification.on_this_page() == False


@given('the holder is {using_the_app}')
@given('the holder is "{using_the_app}"')
def step_impl(context, using_the_app):
    if using_the_app == "Onboarding":
        context.execute_steps(f'''
            Given the new user has opened the app for the first time
            And the user is on the onboarding {'Share only what is neccessary screen'}
        ''')
    elif using_the_app == "PIN Setup":
        context.execute_steps(f'''
            Given the User has skipped on-boarding
            And the User has accepted the Terms and Conditions
            And the User is on the PIN creation screen
        ''')
    elif using_the_app == "Receiving Credential":
        context.execute_steps(f'''
            Given the User has skipped on-boarding
            And the User has accepted the Terms and Conditions
            And a PIN has been set up with "369369"
            And the Holder has selected to use biometrics to unlock BC Wallet
            And a connection has been successfully made
            And the user has a credential offer
            When they select Accept
            And the holder is informed that their credential is on the way with an indication of loading
        ''')
    elif using_the_app == "Presenting Proof":
        context.execute_steps(f'''
            Given the User has skipped on-boarding
            And the User has accepted the Terms and Conditions
            And a PIN has been set up with "369369"
            And the Holder has selected to use biometrics to unlock BC Wallet
            And a connection has been successfully made
            And the holder has a Non-Revocable credential
                | issuer_agent_type | credential_name                           |
                | AATHIssuer        | Default AATH Issuer Credential Definition |
            And the user has a proof request
            When they select Share
            And the holder is informed that they are sending information securely
        ''')

