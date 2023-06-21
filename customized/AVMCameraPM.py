import logging
from ipywidgets import VBox, Label, Select
from common.UICamera import AVMCameraSet, CAMERA_STATUS
from utils.loggers import Logger, OutputWidgetHandler

logging_handler = OutputWidgetHandler()
_logger = Logger(logger_name="AVMCameraPM", log_handler=logging_handler, logging_level=logging.DEBUG)


class AVMCameraPM:
    def __init__(self):
        self.logger = _logger
        self.__avm_cameras = AVMCameraSet()
        self.__power_select = Select(options=CAMERA_STATUS, 
                                     value=CAMERA_STATUS[0])
        self.__power_select.observe(self.__on_change_callback, "value")
        self.__select_label = Label()
        self.__power_control = VBox([self.__select_label, self.__power_select])
        
        self.__display = VBox([self.__avm_cameras.display(), self.__power_control])
        
    def display(self):
        return self.__display
    
    def power_on(self):
        self.__power_select.value = CAMERA_STATUS[1]
        
    def power_off(self):
        self.__power_select.value = CAMERA_STATUS[0]
        
    def __on_change_callback(self, change):
        new_value = change["new"]
        self.logger.debug(f"Select new change: {new_value}")
        if new_value == CAMERA_STATUS[0]:
            self.__avm_cameras.power_off_all()
            
        elif new_value == CAMERA_STATUS[1]:
            self.__avm_cameras.power_on_all()
            
        else:
            self.__avm_cameras.power_off_all()
            self.logger.error("[AVMCameraSet] is error!")
    
            
        
        