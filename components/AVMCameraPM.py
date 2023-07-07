import logging
from ipywidgets import VBox, HBox, Label, Select, IntText
from components.UICamera import AVMCameraSet, CAMERA_STATUS
from utils.loggers import Logger, OutputWidgetHandler

logging_handler = OutputWidgetHandler()
_logger = Logger(logger_name=__file__, 
                 log_handler=logging_handler, 
                 logging_level=logging.DEBUG)


class AVMCameraPM:
    def __init__(self, logger=_logger, ):
        self.logger = logger
        self.__avm_cameras = AVMCameraSet()
        self.__power_select = Select(options=CAMERA_STATUS, 
                                     value=CAMERA_STATUS[1])
        self.__power_select.observe(self.__on_change_callback, "value")
        self.__select_label = Label("AVM360 Cameras Status")
        self.__count = IntText(value=0, description="count", disable=True)
        self.__power_control = VBox([self.__select_label, self.__power_select])
        self.__power_control_box = HBox([self.__power_control, self.__count])
        
        self.__show = VBox([self.__avm_cameras.show(), self.__power_control_box])
        
    def show(self):
        return self.__show
    
    def power_on(self):
        self.__power_select.value = CAMERA_STATUS[1]
        
    def power_off(self):
        self.__power_select.value = CAMERA_STATUS[0]
        
    def __on_change_callback(self, change):
        
        self.__count.value = int(self.__count.value) + 1
        
        new_value = change["new"]
        self.logger.debug(f"Select new change: {new_value}")
        if new_value == CAMERA_STATUS[0]:
            self.__avm_cameras.power_off_all()
            
        elif new_value == CAMERA_STATUS[1]:
            self.__avm_cameras.power_on_all()
            
        else:
            # self.__avm_cameras.power_off_all()
            self.logger.error("[AVMCameraSet] is error!")
            self.__avm_cameras.show_error_all()
    
            
        
        