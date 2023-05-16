# -----------------------------------------------------------
# Behave environtment file used to hold test hooks to do
# Setup and Tear Downs at different levels
# For more info see:
# https://behave.readthedocs.io/en/latest/tutorial.html#environmental-controls
#  
# -----------------------------------------------------------
from appium import webdriver
from behave.model_core import Status
import allure
from sauceclient import SauceClient
from decouple import config
import os, json
import hmac
from hashlib import md5
from agent_factory.agent_interface_factory import AgentInterfaceFactory
from device_service_handler.device_service_handler_factory import DeviceServiceHandlerFactory
from behave.contrib.scenario_autoretry import patch_scenario_with_autoretry

# Get teh Device Cloud Service passed in from manage
device_cloud_service = config('DEVICE_CLOUD')

# Get the Device Platform
device_platform_name = config('DEVICE_PLATFORM')

# Check if there is a config file override. If not, use the default
try: 
    config_file_path = config('CONFIG_FILE_OVERRIDE')
except:
    config_file_path = os.path.join(os.path.dirname(__file__), '..', "config.json")
# Create the Device Service Handler requested 
dcshf = DeviceServiceHandlerFactory()
device_service_handler = dcshf.create_device_service_handler(device_cloud_service, config_file_path)


def before_feature(context, feature):
    # TODO there is an issue where calling driver.reset does not reset the app on iOS. Until a solution is found for this issue
    # moving the driver creation and driver.quit() to the before and after scenario methods. 

    # Add the Device handler to the test context so tests can do device specific calls. 
    context.device_service_handler = device_service_handler

    # Get the issuer endpoint and the issuer type and create an issuer interface from the agent factory
    issuer_info = context.config.userdata.get("Issuer").split(";")
    issuer_type = issuer_info[0]
    issuer_endpoint = issuer_info[1]
    verifier_info = context.config.userdata.get("Verifier").split(";")
    verifier_type = verifier_info[0]
    verifier_endpoint = verifier_info[1]
    aif = AgentInterfaceFactory()
    context.issuer = aif.create_issuer_agent_interface(issuer_type, issuer_endpoint)
    context.verifier = aif.create_verifier_agent_interface(verifier_type, verifier_endpoint)
    context.print_page_source_on_failure = eval(context.config.userdata['print_page_source_on_failure'])
    context.print_qr_code_on_creation = eval(context.config.userdata['print_qr_code_on_creation'])
    context.save_qr_code_on_creation = True if device_cloud_service == 'LocalAndroid' or device_cloud_service == 'LambdaTest' else eval(context.config.userdata['save_qr_code_on_creation'])

    # retry failed tests 
    try: 
        test_retry_attempts = int(config('TEST_RETRY_ATTEMPTS_OVERRIDE'))
    except:
        test_retry_attempts = int(eval(context.config.userdata['test_retry_attempts']))
    for scenario in feature.scenarios:
        patch_scenario_with_autoretry(scenario, max_attempts=test_retry_attempts)



def before_scenario(context, scenario):
    # TODO go through the sceanrio tags and find the unique id, starts with T, and prefix it to the name. 
    # maybe put the feature in it as well like Feature:TestID:Scenario
    
    # pass some extra capabilities and options to the device service. If it can't do anything with them then fine.
    # ie. Local devices won't do anything with a scenario name.
    # TODO fullReset may have to be moved to the config files, if dev starts to use the Test Harness they may
    # want tests with previous state maintained. 
    extra_desired_capabilities = {
        'name': scenario.name
    }
    device_service_handler.set_desired_capabilities(extra_desired_capabilities)

    context.driver = device_service_handler.initialize_driver()

    print("\nActual Capabilities used by Appium:")
    print(json.dumps(context.driver.capabilities,indent=4))


def after_scenario(context, scenario):

    if hasattr(context, 'driver') and scenario.status == Status.failed and context.print_page_source_on_failure:
        print(context.driver.page_source)

    if device_service_handler.supports_test_result():
        if scenario.status == Status.failed:
            device_service_handler.set_test_result(False)
        elif scenario.status == Status.passed:
            device_service_handler.set_test_result(True)



        if device_cloud_service == 'SauceLabs':
            # Add the sauce Labs results and video url to the allure results
            # Link that requires a sauce labs account and login
            testobject_test_report_url = context.driver.capabilities["testobject_test_report_url"]
            allure.attach(testobject_test_report_url, "Sauce Labs Report and Video (Login required)")
            print(f"Sauce Labs Report and Video (Login required): {testobject_test_report_url}")

            # Since every test scenario is a new session with potentially a different device
            # write the capabilities info as an attachment to the test scenario to keep track
            allure.attach(json.dumps(context.driver.capabilities,indent=4), "Complete Appium/Sauce Labs Test Environment Configuration")

            # Link does not require a sauce labs account and login. Token generated.
            # # TODO This isn't working. Have contacted Sauce Labs. 
            # test_id = testobject_test_report_url.rpartition('/')[-1]
            # session_id = context.driver.session_id
            # key = f"{username}:{access_key}"
            # sl_token = hmac.new(key.encode("ascii"), None, md5).hexdigest()
            # url = f"{testobject_test_report_url}?auth={sl_token}"
            # allure.attach(url, "Public Sauce Labs Report and Video (Login not required) (Nonfunctional at this time)")
            # print(f"Public Sauce Labs Report and Video (Login not required): {url} (Nonfunctional at this time)")

        # elif device_cloud_service == "LambdaTest":
            # TODO 

        # if context.driver.capabilities['platformName'] == "iOS":
        #     context.driver.close_app()
        #     context.driver.launch_app()
        # else:
        #     context.driver.reset()

    if hasattr(context, 'driver'):
        context.driver.quit()

# def after_feature(context, feature):
#     # Invoke driver.quit() after the test is done to indicate to BrowserStack 
#     # that the test is completed. Otherwise, test will appear as timed out on BrowserStack.
#     # if context does not contain browser then something went wrong on initialization and no need to call quit.
#     if hasattr(context, 'driver'):
#         context.driver.quit()


