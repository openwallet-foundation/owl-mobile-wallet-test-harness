"""
Class for actual LambdaTest Device Service Handling
"""

from device_service_handler.device_service_handler_interface import DeviceServiceHandlerInterface
import json
from decouple import config
from appium import webdriver
import requests
import aiohttp
import asyncio
import os 



class LambdaTestHandler(DeviceServiceHandlerInterface):

    _url: str
    _desired_capabilities: dict
    _driver: webdriver
    _api_endpoint: str
    _lambda_username: str
    _lambda_access_key: str

    def __init__(self, config_file_path: str):
        super().__init__(config_file_path)
        self._api_endpoint = 'https://mobile-mgm.lambdatest.com/mfs/v1.0/media/upload'

    def set_desired_capabilities(self, config: dict = None):
        """set extra capabilities above what was in the config file"""

        # Handle posiible special options
        if 'name' in config:
            self._CONFIG['capabilities']['lt:options']['name'] = config['name']
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
        if options and 'LAMBDA_USERNAME' in options:
            self._lambda_username = options['LAMBDA_USERNAME']
        else:
            if 'LAMBDA_USERNAME' in self._CONFIG:
                self._lambda_username = self._CONFIG['LAMBDA_USERNAME']
            else:
                self._lambda_username = config('LAMBDA_USERNAME')

        if options and 'LAMBDA_ACCESS_KEY' in options:
            self._lambda_access_key = options['LAMBDA_ACCESS_KEY']
        else:
            if 'LAMBDA_ACCESS_KEY' in self._CONFIG:
                self._lambda_access_key = self._CONFIG['LAMBDA_ACCESS_KEY']
            else:
                self._lambda_access_key = config('LAMBDA_ACCESS_KEY')

        if command_executor_url == None:
            self._url = 'http://%s:%s@mobile-hub.lambdatest.com/wd/hub' % (
                self._lambda_username, self._lambda_access_key)
        else:
            self._url = command_executor_url

        # print(url)

    async def save_qr_code_to_lambda_test(self, data):
        async with aiohttp.ClientSession() as session:
            async with session.post(self._api_endpoint, auth=aiohttp.BasicAuth(self._lambda_username, self._lambda_access_key), data=data) as resp:
                result = await resp.json()
                return result['media_url']



    def inject_qrcode(self, image):
        """save qrcode image to the device in lambda test in a way that allows for the device to scan it when the camera opens"""
        # get current directory
        with open(os.path.dirname(__file__) + '/../qrcode.png', 'rb') as img:
            print(img)
            payload = {
                'media_file': img,
                'type': 'image',
                'custom_id': 'QRCodeImage'
            }
            image_url = asyncio.run(self.save_qr_code_to_lambda_test(payload))
            self._driver.execute_script(f"lambda-image-injection={image_url}")

    def biometrics_authenticate(self, authenticate:bool):
        """authenticate when biometrics, ie fingerprint or faceid, true is success, false is fail biometrics"""
        return authenticate

    def supports_test_result(self) -> bool:
        """return true if the device service supports setting a pass or fail flag in thier platform"""
        return True

    def set_test_result(self, passed: bool):
        """set the test result on the device platform. True is pass, False is failure"""
        if passed == False:
            self._driver.execute_script('lambda-status=failed')
        elif passed == True:
            self._driver.execute_script('lambda-status=passed')
