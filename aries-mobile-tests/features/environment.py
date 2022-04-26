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

config_file_path = os.path.join(os.path.dirname(__file__), '..', "config.json")
print("Path to the config file = %s" % (config_file_path))
with open(config_file_path) as config_file:
    CONFIG = json.load(config_file)

# Take user credentials from environment variables if they are defined
#if 'BROWSERSTACK_USERNAME' in os.environ: CONFIG['capabilities']['browserstack.user'] = os.environ['BROWSERSTACK_USERNAME'] 
#if 'BROWSERSTACK_ACCESS_KEY' in os.environ: CONFIG['capabilities']['browserstack.key'] = os.environ['BROWSERSTACK_ACCESS_KEY']

# Take user credentials and sauce region from environment variables if they are defined
# TODO this should be in a separate module that handles device service specific variable settings.
username = config('SAUCE_USERNAME')
access_key = config('SAUCE_ACCESS_KEY')
#if 'SAUCE_USERNAME' in os.environ: username = os.environ['SAUCE_USERNAME'] 
#if 'SAUCE_ACCESS_KEY' in os.environ: access_key = os.environ['SAUCE_ACCESS_KEY']
#url = 'http://%s:%s@ondemand.saucelabs.com:80/wd/hub' % (username, access_key)
region = config('SL_REGION')
url = 'http://%s:%s@ondemand.%s.saucelabs.com:80/wd/hub' % (username, access_key, region)
print(url)

def before_feature(context, feature):
    # TODO there is an issue where calling driver.reset does not reset the app on iOS. Until a solution is found for this issue
    # moving the driver creation and driver.quit() to the before and after scenario methods. 

    # CONFIG['capabilities']['name'] = feature.name
    # CONFIG['capabilities']['fullReset'] = True
    # desired_capabilities = CONFIG['capabilities']
    # print(desired_capabilities)

    # context.driver = webdriver.Remote(
    #     desired_capabilities=desired_capabilities,
    #     command_executor=url,
    #     keep_alive=False
    # )
    # print(json.dumps(context.driver.capabilities))

    # Set the Issuer and Verfier URLs
    # TODO these two lines can be removed once the Agent Factory is fully in place. 
    #context.issuer_url = context.config.userdata.get("Issuer")
    #context.verifier_url = context.config.userdata.get("Verifier")

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
    context.save_qr_code_on_creation = eval(context.config.userdata['save_qr_code_on_creation'])



def before_scenario(context, scenario):
    # TODO go through the sceanrio tags and find the unique id, starts with T, and prefix it to the name. 
    # maybe put the feature in it as well like Feature:TestID:Scenario
    CONFIG['capabilities']['name'] = scenario.name
    CONFIG['capabilities']['fullReset'] = True
    desired_capabilities = CONFIG['capabilities']
    print("\n\nDesired Capabilities passed to Appium:")
    print(json.dumps(desired_capabilities,indent=4))
    
    context.driver = webdriver.Remote(
        desired_capabilities=desired_capabilities,
        command_executor=url,
        keep_alive=False
    )
    print("\nActual Capabilities used by Appium:")
    print(json.dumps(context.driver.capabilities,indent=4))


def after_scenario(context, scenario):

    if hasattr(context, 'driver') and scenario.status == Status.failed and context.print_page_source_on_failure:
        print(context.driver.page_source)


    device_cloud_service = os.environ['DEVICE_CLOUD']
    if device_cloud_service == "SauceLabs" and hasattr(context, 'driver'):

        # set the status of the test in Sauce Labs
        #context.driver.execute_script(f'sauce:job-result={scenario.status}')
        if scenario.status == Status.failed:
            context.driver.execute_script('sauce:job-result=failed')
        elif scenario.status == Status.passed:
            context.driver.execute_script('sauce:job-result=passed')

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

    # elif device_cloud_service == "something else in the future":
    
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


