"""
Class for actual Sauce Labs Device Service Handling
"""

from device_service_handler.device_service_handler_interface import DeviceServiceHandlerInterface
import json
from decouple import config
from appium import webdriver
import shutil
import requests
import subprocess


class LocalAndroidHandler(DeviceServiceHandlerInterface):

    _desired_capabilities: dict
    _url: str

    def set_device_service_specific_options(self, options: dict = None, command_executor_url: str = None):
        """set any specific device options before initialize_driver is called """
        if command_executor_url == None:
            # if no dockerhost then we are probably running local.
            host = config('DOCKERHOST', default='0.0.0.0')
            self._url = f'http://{host}:4723/wd/hub'
        else:
            self._url = command_executor_url

    def _set_appium_options_from_desired_capabilities(self):
        """set the appium options from the desired capabilities"""
        # self._options = webdriver.AppiumOptions()
        for key in self._desired_capabilities:
            self._options.set_capability(key, self._desired_capabilities[key])

    def set_desired_capabilities(self, config: dict):
        """set extra capabilities above what was in the config file"""
        # Handle common options and capabilities
        for item in config:
            self._CONFIG['capabilities'][item] = config[item]
        self._desired_capabilities = self._CONFIG['capabilities']
        print("\n\nDesired Capabilities passed to Appium:")
        print(json.dumps(self._desired_capabilities, indent=4))
        self._set_appium_options_from_desired_capabilities()


    def inject_qrcode(self, image):
        """pass the qrcode image to the device in a way that allows for the device to scan it when the camera opens"""
        # get the android home environment variable
        android_home = config('ANDROID_HOME')
        # write the qrcode png to the {android_home}/emulator/resources

        shutil.copy(
            "qrcode.png", f"{android_home}/emulator/resources/qrcode.png")

    def supports_biometrics(self) -> bool:
        return True

    def biometrics_authenticate(self, authenticate: bool, finger_id: int = 1):
        """authenticate when biometrics, ie fingerprint or faceid, true is success, false is fail biometrics"""
        if authenticate:
            # option 1 - use driver
            self._driver.finger_print(finger_id)

            # option 2 - use appium API call
            appium_api_call = f"{self._url}/session/{self._driver.session_id}/appium/device/finger_print"
            fingerprint_data = {
                "fingerprintId": finger_id
            }
            response = requests.post(appium_api_call, data = fingerprint_data)
            print(response)

            # option 3 - Use adb
            adb_command = f"adb -e emu finger touch {finger_id}"
            subprocess.call(adb_command, shell=True)

            # option 4 - ?

        else:
            self._driver.finger_print(10)

    def supports_test_result(self) -> bool:
        """return true if the device service supports setting a pass or fail flag in thier platform"""
        return False

    def set_test_result(self, passed: bool):
        """set the test result on the device platform. True is pass, False is failure"""
        pass
