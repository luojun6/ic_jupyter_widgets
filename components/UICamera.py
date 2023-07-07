import logging
from ipywidgets import HBox, VBox
# from threading import Timer
from common.UIButton import UIButton
from utils.loggers import Logger, OutputWidgetHandler

logging_handler = OutputWidgetHandler()
_logger = Logger(logger_name=__file__, 
                 log_handler=logging_handler, 
                 logging_level=logging.DEBUG)

CAMERA_STATUS = ["OFF", "ON", "ERROR"]
STATUS_COLOR_MAP = {
    "OFF": "",
    "ON": "warning",
    "ERROR": "danger"
}


class UICamera(UIButton):
    def __init__(self, 
                 name=__file__, 
                 values=CAMERA_STATUS, 
                 default_value_index=0, 
                 internal_timer_callback=None, 
                 logger=_logger, 
                 **kwargs):
        super().__init__(name, values, default_value_index, internal_timer_callback, logger, **kwargs)
        self.set_on_change_callback(self.__on_change_callback)
        self.value = self.values[self.value_index]
        # self.button_style = STATUS_COLOR_MAP[values[default_value_index]]
        self.disabled = False
        self.icon = "camera"
        
        
    def power_on(self):
        self.set_value_index(1)
        
    def power_off(self):
        self.set_value_index(0)

    def show_error(self):
        self.set_value_index(2)
        
    def __on_change_callback(self, change):
        self.button_style = STATUS_COLOR_MAP[self.value]
        

class AVMCameraSet:
    def __init__(self, default_power_state=1):
        avm_camera_names = ["front_avm_cam", 
                            "left_avm_cam", 
                            "right_avm_cam", 
                            "rear_avm_cam"]
        self.logger = _logger
        self.__cameras = [UICamera(name=cam, default_value_index=default_power_state) for cam in avm_camera_names]
        self.__show = HBox(self.__cameras)
        
        
    def show(self):
        return self.__show
    
    def power_on_all(self):
        self.logger.debug(f"{__file__}: [AVMCameraSet] power_on_all.")
        for cam in self.__cameras:
            cam.power_on()
            
    def power_off_all(self):
        self.logger.debug(f"{__file__}: [AVMCameraSet] power_off_all.")
        for cam in self.__cameras:
            cam.power_off()

    def show_error_all(self):
        self.logger.debug(f"{__file__}: [AVMCameraSet] power_off_error!")
        for cam in self.__cameras:
            cam.show_error()


class MPDCameraSet:
    def __init__(self, default_power_state=1):
        self.__avm_cam_set = AVMCameraSet(default_power_state=default_power_state)
        self.__fov_cam = UICamera(name="fov_cam", default_value_index=default_power_state)
        self.__show = VBox([self.__avm_cam_set.show(), self.__fov_cam])
        
    def show(self):
        return self.__show
    
    def power_on(self):
        self.power_on_all()
        
    def power_off(self):
        self.power_off_all()
        
    def show_error(self):
        self.show_error_all()
    
    def power_on_all(self):
        self.__avm_cam_set.power_on_all()
        self.__fov_cam.power_on()
        
    def power_off_all(self):
        self.__avm_cam_set.power_off_all()
        self.__fov_cam.power_off()
        
    def show_error_all(self):
        self.__avm_cam_set.show_error_all()
        self.__fov_cam.show_error()