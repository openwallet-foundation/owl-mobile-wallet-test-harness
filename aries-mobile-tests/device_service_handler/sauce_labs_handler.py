"""
Class for actual Sauce Labs Device Service Handling
"""

from device_service_handler.device_service_handler_interface import DeviceServiceHandlerInterface
import json
from decouple import config
from appium import webdriver


class SauceLabsHandler(DeviceServiceHandlerInterface):

    _url: str
    _desired_capabilities: dict
    _driver: webdriver

    def set_desired_capabilities(self, config: dict = None):
        """set extra capabilities above what was in the config file"""

        # Handle posiible special options
        if 'name' in config:
            self._CONFIG['capabilities']['sauce:options'] = {
                'name': config['name']
            }
        config.pop('name')

        # Handle common options and capabilities
        for item in config:
            self._CONFIG['capabilities'][item] = config[item]
        #self._CONFIG['capabilities']['fullReset'] = True
        self._desired_capabilities = self._CONFIG['capabilities']
        print("\n\nDesired Capabilities passed to Appium:")
        print(json.dumps(self._desired_capabilities, indent=4))

    def set_device_service_specific_options(self, options: dict = None, command_executor_url: str = None):
        """set any specific device options before initialize_driver is called """
        """Order of presededence is options parameter, then the config.json file, then environment variables"""
        # if username, access key, and region are not in the config, check the environment.
        if options and 'SAUCE_USERNAME' in options:
            username = options['SAUCE_USERNAME']
        else:
            if 'SAUCE_USERNAME' in self._CONFIG:
                username = self._CONFIG['SAUCE_USERNAME']
            else:
                username = config('SAUCE_USERNAME')

        if options and 'SAUCE_ACCESS_KEY' in options:
            username = options['SAUCE_ACCESS_KEY']
        else:
            if 'SAUCE_ACCESS_KEY' in self._CONFIG:
                access_key = self._CONFIG['SAUCE_ACCESS_KEY']
            else:
                access_key = config('SAUCE_ACCESS_KEY')

        if options and 'SL_REGION' in options:
            username = options['SL_REGION']
        else:
            if 'SL_REGION' in self._CONFIG:
                access_key = self._CONFIG['SL_REGION']
            else:
                region = config('SL_REGION')

        if command_executor_url == None:
            self._url = 'http://%s:%s@ondemand.%s.saucelabs.com:80/wd/hub' % (
                username, access_key, region)
        else:
            self._url = command_executor_url

        # print(url)


    def inject_qrcode(self, image):
        """pass the qrcode image to the device in a way that allows for the device to scan it when the camera opens"""
        self._driver.execute_script(f"sauce:inject-image={image}")

    def biometrics_authenticate(self, authenticate:bool):
        """authenticate when biometrics, ie fingerprint or faceid, true is success, false is fail biometrics"""
        if authenticate:
            self._driver.execute_script('sauce:biometrics-authenticate=true')
        else:
            self._driver.execute_script('sauce:biometrics-authenticate=false')

    def supports_test_result(self) -> bool:
        """return true if the device service supports setting a pass or fail flag in thier platform"""
        return True

    def set_test_result(self, passed: bool):
        """set the test result on the device platform. True is pass, False is failure"""
        if passed == False:
            self._driver.execute_script('sauce:job-result=failed')
        elif passed == True:
            self._driver.execute_script('sauce:job-result=passed')
