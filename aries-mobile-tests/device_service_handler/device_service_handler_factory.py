"""
Factory class to create Device Service Handlers
given the device service type passed in.
"""
from device_service_handler.device_service_map import device_service_map_dict
from device_service_handler.device_service_handler_interface import DeviceServiceHandlerInterface
from device_service_handler.sauce_labs_handler import SauceLabsHandler
from device_service_handler.local_android_handler import LocalAndroidHandler

class DeviceServiceHandlerFactory():

    def create_device_service_handler(self, device_service_type:str, config_file_path:str) -> DeviceServiceHandlerInterface:
        """create an issuer agent interface object of the type given"""
        return device_service_map_dict[device_service_type](config_file_path)
