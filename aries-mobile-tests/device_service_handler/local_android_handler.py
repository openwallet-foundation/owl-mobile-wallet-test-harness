"""
Class for actual Sauce Labs Device Service Handling
"""

from device_service_handler.device_service_handler_interface import DeviceServiceHandlerInterface
import json
from decouple import config
from appium import webdriver
import shutil


class LocalAndroidHandler(DeviceServiceHandlerInterface):

    _desired_capabilities: dict
    _url: str

    def set_device_service_specific_options(self, options:dict=None, command_executor_url:str=None):
        """set any specific device options before initialize_driver is called """
        if command_executor_url == None:
            #if no dockerhost then we are probably running local. 
            host = config('DOCKERHOST', default='0.0.0.0')
            self._url = f'http://{host}:4723/wd/hub'
        else:
            self._url = command_executor_url

    def set_desired_capabilities(self, config: dict):
        """set extra capabilities above what was in the config file"""
        # Handle common options and capabilities
        for item in config:
            self._CONFIG['capabilities'][item] = config[item]
        self._desired_capabilities = self._CONFIG['capabilities']
        print("\n\nDesired Capabilities passed to Appium:")
        print(json.dumps(self._desired_capabilities, indent=4))


    def inject_qrcode(self, image):
        """pass the qrcode image to the device in a way that allows for the device to scan it when the camera opens"""
        # get the android home environment variable
        android_home = config('ANDROID_HOME')
        # write the qrcode png to the {android_home}/emulator/resources

        shutil.copy(
            "qrcode.png", f"{android_home}/emulator/resources/qrcode.png")

    def biometrics_authenticate(self, bool):
        """authenticate when biometrics, ie fingerprint or faceid, true is success, false is fail biometrics"""
        self._driver.finger_print(1)

    def supports_test_result(self) -> bool:
        """return true if the device service supports setting a pass or fail flag in thier platform"""
        return False

    def set_test_result(self, passed: bool):
        """set the test result on the device platform. True is pass, False is failure"""
        pass
