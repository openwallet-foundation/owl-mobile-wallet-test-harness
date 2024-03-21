# -----------------------------------------------------------
# Behave Step Definitions for wallet naming.
# 
# -----------------------------------------------------------

from behave import given, when, then, step
import json
import os
from decouple import config

# Local Imports
from agent_controller_client import agent_controller_GET, agent_controller_POST, expected_agent_state, setup_already_connected
# import Page Objects needed
from pageobjects.bc_wallet.biometrics import BiometricsPage
from pageobjects.bc_wallet.camera_privacy_policy import CameraPrivacyPolicyPage
from pageobjects.bc_wallet.scan_my_qr_code import ScanMyQRCodePage
from pageobjects.bc_wallet.settings import SettingsPage


@step('an existing {actor} wallet user')
@step('an existing wallet user')
def an_existing_wallet_user(context, actor=None):
    """ This is a user who has already setup a wallet (onboarded and setup security), and has closed and reopened the app and authenticated. """
    
    # If the actor is provided then we will need that for later in whatever scenario is being executed.
    # needed for Showcase tests
    if actor is not None:
        context.actor = actor

    # Get PIN and Biometrics setup from context table
    pin = context.table[0]['pin']
    biometrics = context.table[0]['biometrics']
    
    context.execute_steps(f'''
        Given the User has completed on-boarding
        And the User has accepted the Terms and Conditions
        And a PIN has been set up with "{pin}"
    ''')
    if biometrics == 'on':
        context.execute_steps('''
            Given the Holder has selected to use biometrics to unlock BC Wallet
        ''')
    else:
        context.execute_steps('''
            Given the User has choosen not to use biometrics to unlock BC Wallet
        ''')

    context.execute_steps('''
        Given they have closed the app
        When they relaunch the app
    ''')

    if context.biometrics_choosen == True:
        context.thisBiometricsPage = BiometricsPage(context.driver)
        context.execute_steps('''
            When authenticates with thier biometrics
        ''')          
    else:      
        context.execute_steps(f'''
            When they enter thier PIN as "{pin}"
        ''')

    # TODO this step takes a long time, fix it.
    context.execute_steps('''
        Then they have access to the app
    ''')



@step('the wallet user is in {user_state}')
def the_wallet_user_is_in_state_for_wallet_name_change(context, user_state):
    """ This will take a user to with menu or the scan my QA code page. """
    """ It is expected that the user is on the Home page at this point. """
    context.thisSettingsPage = context.thisHomePage.select_settings()
    # We need to turn on developer settings to get at this feature.
    context.thisSettingsPage.enable_developer_mode()
    context.thisDeveloperSettingsPage = context.thisSettingsPage.select_developer()
    context.thisDeveloperSettingsPage.select_use_connection_inviter_capability()
    context.thisSettingsPage = context.thisDeveloperSettingsPage.select_back()
    # Scroll to top differently on iOS and Android
    if context.driver.capabilities['platformName'] == 'iOS':
        #context.thisSettingsPage.scroll_to_element(context.thisSettingsPage.settings_locator[1], direction='up')
        context.thisSettingsPage.scroll_to_top()
    else:
        context.thisSettingsPage.scroll_to_element(context.thisSettingsPage.contacts_aid_locator[1], direction='up')
    
    context.user_state = user_state
    if user_state == 'the menu':
        # We have to get to the settins/menu page for the scan my qr code anyway so no need to do anything extra here.
        assert context.thisSettingsPage.on_this_page(), 'The user is not on the settings/menu page.'
    elif user_state == 'Scan my QR code':
        context.thisScanMyQRCodePage = context.thisSettingsPage.select_scan_my_qr_code()
        # check if the Camera Privacy Policy is displayed and accept it if it is
        # If this is the first time the user selects scan, then they will get a Camera Privacy Policy that needs to be dismissed
        # TODO only do this if the platorm is iOS. Android is not showing the policy page at present in Sauce Labs becasue we have autoGrantPermissions on. 
        if context.driver.capabilities['platformName'] == 'iOS':
            context.thisCameraPrivacyPolicyPage = CameraPrivacyPolicyPage(context.driver)
            if context.thisCameraPrivacyPolicyPage.on_this_page():
                context.thisCameraPrivacyPolicyPage.select_allow()

        assert context.thisScanMyQRCodePage.on_this_page(), 'The user is not on the Scan my QR code page.'
    else:
        assert False, f'"{user_state}" is not a valid user state. Please use "the menu" or "Scan my QR code".'


@when(u'the user changes thier wallet name')
def step_change_wallet_name(context, wallet_name=None):
    # Check whether we are on the settings/menu page or the Scan my QR code page.
    if context.user_state == 'the menu':
        # This is commented out until we have a testID on the Wallet Name, issue 1557
        if hasattr(context, 'original_wallet_name') == False:
            context.original_wallet_name = context.thisSettingsPage.get_wallet_name()
        context.thisEditWalletNamePage = context.thisSettingsPage.select_edit_wallet_name()
    elif context.user_state == 'Scan my QR code':
        if hasattr(context, 'original_wallet_name') == False:
            context.original_wallet_name = context.thisScanMyQRCodePage.get_wallet_name()
        context.thisEditWalletNamePage = context.thisScanMyQRCodePage.select_edit_wallet_name()
    
    # Get the new wallet name from the context table or use the wallet_name parameter
    if wallet_name is None:
        context.new_wallet_name = context.table[0]['wallet_name']
    else:
        context.new_wallet_name = wallet_name
    # Set the new wallet name
    context.thisEditWalletNamePage.enter_wallet_name(context.new_wallet_name)

@when(u'saves the wallet name change')
def step_impl(context):
    context.thisEditWalletNamePage.select_save()


@when(u'changes the wallet name back to the original name')
def step_impl(context):
    step_change_wallet_name(context, wallet_name=context.original_wallet_name)
    context.thisEditWalletNamePage.select_save()

@when(u'cancels the wallet name change')
def step_impl(context):
    context.thisEditWalletNamePage.select_cancel()

@then(u'the name of the wallet is changed everywhere it is presented')
def step_impl(context):
    for row in context.table:
        # Get the new wallet name from the context table or use the wallet_name parameter
        location = row['wallet_name_location']
        if location == 'the menu':
            if "thisSettingsPage" not in context:
                context.thisSettingsPage = SettingsPage(context.driver)
            if context.thisSettingsPage.on_this_page() == False:
                # we are probably on the Scan my QR code page so go back to the menu
                context.thisSettingsPage = context.thisScanMyQRCodePage.select_back()
            assert context.thisSettingsPage.on_this_page(), 'The user is not on the settings/menu page.'
            # This is commented out until we have a testID on the Wallet Name, issue 1557
            assert context.thisSettingsPage.get_wallet_name() == context.new_wallet_name, f'The wallet name is not correct on the settings/menu page. {context.thisSettingsPage.get_wallet_name()} should equal {context.new_wallet_name}'
        elif location == 'Scan my QR code':
            if "thisScanMyQRCodePage" not in context:
                context.thisScanMyQRCodePage = ScanMyQRCodePage(context.driver) 
            if context.thisScanMyQRCodePage.on_this_page() == False:
                # we are probably on the settings page so go back to the Scan my QR code page
                context.thisScanMyQRCodePage = context.thisSettingsPage.select_scan_my_qr_code()
                if context.driver.capabilities['platformName'] == 'iOS':
                    context.thisCameraPrivacyPolicyPage = CameraPrivacyPolicyPage(context.driver)
                    if context.thisCameraPrivacyPolicyPage.on_this_page():
                        context.thisCameraPrivacyPolicyPage.select_allow()
            assert context.thisScanMyQRCodePage.on_this_page(), 'The user is not on the Scan my QR code page.'
            # This is commented out until we have a testID on the Wallet Name, issue 1557
            assert context.thisScanMyQRCodePage.get_wallet_name() == context.new_wallet_name, f'The wallet name is not correct on the Scan my QR code page. {context.thisScanMyQRCodePage.get_wallet_name()} should equal {context.new_wallet_name}'
        else:
            assert False, f'"{location}" is not a valid location. Please use "the menu" or "Scan my QR code".'

@then(u'the name of the wallet is unchanged everywhere it is presented')
def step_impl(context):
    for row in context.table:
        # Get the new wallet name from the context table or use the wallet_name parameter
        location = row['wallet_name_location']
        if location == 'the menu':
            if hasattr(context, 'thisSettingsPage') == False:
                context.thisSettingsPage = SettingsPage(context.driver)
            if context.thisSettingsPage.on_this_page() == False:
                # we are probably on the Scan my QR code page so go back to the menu
                context.thisSettingsPage = context.thisScanMyQRCodePage.select_back()
            assert context.thisSettingsPage.on_this_page(), 'The user is not on the settings/menu page.'
            assert context.thisSettingsPage.get_wallet_name() == context.original_wallet_name, f'The wallet name has been changed on the settings/menu page. {context.thisSettingsPage.get_wallet_name()} should equal {context.original_wallet_name}'
        elif location == 'Scan my QR code':
            if hasattr(context, 'thisScanMyQRCodePage') == False:
                context.thisScanMyQRCodePage = ScanMyQRCodePage(context.driver)
            if context.thisScanMyQRCodePage.on_this_page() == False:
                # we are probably on the settings page so go back to the Scan my QR code page
                context.thisScanMyQRCodePage = context.thisSettingsPage.select_scan_my_qr_code()
                if context.driver.capabilities['platformName'] == 'iOS':
                    context.thisCameraPrivacyPolicyPage = CameraPrivacyPolicyPage(context.driver)
                    if context.thisCameraPrivacyPolicyPage.on_this_page():
                        context.thisCameraPrivacyPolicyPage.select_allow()
            assert context.thisScanMyQRCodePage.on_this_page(), 'The user is not on the Scan my QR code page.'
            # This is commented out until we have a testID on the Wallet Name, issue 1557
            assert context.thisScanMyQRCodePage.get_wallet_name() == context.original_wallet_name, f'The wallet name has been changed on the Scan my QR code page. {context.thisScanMyQRCodePage.get_wallet_name()} should equal {context.original_wallet_name}'
        else:
            assert False, f'"{location}" is not a valid location. Please use "the menu" or "Scan my QR code".'


@when(u'the user changes thier wallet name following conventions')
@when(u'the user changes thier wallet name not following conventions')
def step_change_wallet_name_not_following_conventions(context):

    if hasattr(context, 'original_wallet_name') == False:
        context.original_wallet_name = context.thisSettingsPage.get_wallet_name()
    context.thisEditWalletNamePage = context.thisSettingsPage.select_edit_wallet_name()


@then(u'the user will be informed on the wallet name conventions')
def step_informed_of_conventions(context):
    # for each row in the context.table we will check the wallet name conventions
    for row in context.table:
        # Get the new wallet name from the context table or use the wallet_name parameter
        wallet_name = row['wallet_name']
        wallet_name_error = row['wallet_name_error']
        # Set the new wallet name
        context.thisEditWalletNamePage.enter_wallet_name(wallet_name)
        context.thisEditWalletNamePage.select_save()
        # Check if the wallet name error modal is displayed
        if context.thisEditWalletNamePage.wallet_name_error_modal.is_displayed():
            assert context.thisEditWalletNamePage.wallet_name_error_modal.get_error_title() == wallet_name_error, 'The wallet name error message is not correct.'
            # Select the OK button on the modal
            context.thisEditWalletNamePage.wallet_name_error_modal.select_okay()
        else:
            assert False, 'The wallet name error modal is not displayed.'


@then(u'the name of the wallet is successfully changed')
def step_Successful_change_of_wallet_name(context):
    # for each row in the context.table we will check the wallet name conventions
    for row in context.table:
        # Get the new wallet name from the context table or use the wallet_name parameter
        wallet_name = row['wallet_name']
        # Set the new wallet name
        context.thisEditWalletNamePage.enter_wallet_name(wallet_name)
        context.thisEditWalletNamePage.select_save()

        # check if the wallet name is changed
        assert context.thisSettingsPage.get_wallet_name() == wallet_name, f'The wallet name didnt stick for {wallet_name}.'

        # Call "the user changes thier wallet name not following conventions" step to get back to get into edit wallet name page
        context.execute_steps('''
            When the user changes thier wallet name not following conventions
        ''')