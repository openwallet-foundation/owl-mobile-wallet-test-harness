"""
Absctact Base Class for actual device service handler interfaces to implement
"""

from abc import ABC, abstractmethod
from appium import webdriver
import os
import json


class DeviceServiceHandlerInterface(ABC):

    _CONFIG: dict
    _driver: webdriver

    def __init__(self, config_file_path: str):
        print("Path to the config file = %s" % (config_file_path))
        with open(config_file_path) as config_file:
            self._CONFIG = json.load(config_file)
        
        # Set the device service specific options to default. 
        # This can be overridden if the user calls this method again with parameters.
        self.set_device_service_specific_options()

    @abstractmethod
    def set_device_service_specific_options(self, options:dict=None, command_executor_url:str=None):
        """set any specific device options before initialize_driver is called """

    @abstractmethod
    def set_desired_capabilities(self, config: dict):
        """set the capabilities for this device handler"""

    def initialize_driver(self, command_executor_url:str=None) -> webdriver:
        """create the appium webdriver with the given capabilities """
        if command_executor_url == None:
            url = self._url
        else:
            url = command_executor_url
        self._driver = webdriver.Remote(
            desired_capabilities=self._desired_capabilities,
            command_executor=url,
            keep_alive=False
        )
        return self._driver

    @abstractmethod
    def inject_qrcode(self, image):
        """pass the qrcode image to the device in a way that allows for the device to scan it when the camera opens"""

    @abstractmethod
    def biometrics_authenticate(self, authenticate:bool):
        """authenticate when biometrics, ie fingerprint or faceid, true is success, false is fail biometrics"""

    @abstractmethod
    def supports_test_result(self) -> bool:
        """return true if the device service supports setting a pass or fail flag in thier platform"""

    @abstractmethod
    def set_test_result(self, passed: bool):
        """set the test result on the device platform. True is pass, False is failure"""
