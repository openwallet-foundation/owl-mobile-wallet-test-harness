# -----------------------------------------------------------
# Behave environtment file used to hold test hooks to do
# Setup and Tear Downs at different levels
# For more info see:
# https://behave.readthedocs.io/en/latest/tutorial.html#environmental-controls
#  
# -----------------------------------------------------------
from appium import webdriver
from decouple import config

# from browserstack.local import Local
import os, json

config_file_path = os.path.join(os.path.dirname(__file__), '..', "config.json")
print("Path to the SauceLabs config file = %s" % (config_file_path))
with open(config_file_path) as config_file:
    CONFIG = json.load(config_file)

# Take user credentials from environment variables if they are defined

CONFIG['capabilities']['sauce:options']['username'] = config('SL_USERNAME')
CONFIG['capabilities']['sauce:options']['accesskey'] = config('SL_ACCESS_KEY')
region = config('SL_REGION')

def before_feature(context, feature):

        desired_capabilities = CONFIG['capabilities'] 

        url = f'https://@ondemand.{region}.saucelabs.com:443/wd/hub'

        context.browser = webdriver.Remote(
                desired_capabilities= desired_capabilities,
                command_executor=url,
                keep_alive=True) 

def after_feature(context, feature):
    # Invoke driver.quit() after the test is done to indicate to BrowserStack 
    # that the test is completed. Otherwise, test will appear as timed out on BrowserStack.
    context.browser.quit()


