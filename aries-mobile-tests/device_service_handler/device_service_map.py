"""
Mapping of device service names to thier classes
"""
from device_service_handler.lambda_test_handler import LambdaTestHandler
from device_service_handler.sauce_labs_handler import SauceLabsHandler
from device_service_handler.local_android_handler import LocalAndroidHandler

device_service_map_dict = {
    "SauceLabs": SauceLabsHandler,
    "LocalAndroid": LocalAndroidHandler,
    "LambdaTest": LambdaTestHandler
}
