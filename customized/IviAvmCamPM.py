from faulthandler import disable
import imp
import logging
import ipywidgets as widgets
from utils.loggers import Logger, OutputWidgetHandler
from common.UIForeground import UISimpleForeground
from common.UISpeed import UISpeedSlider
from customized.AVMCameraPM import AVMCameraPM

logging_handler = OutputWidgetHandler()
_logger = Logger(logger_name=__file__, 
                 log_handler=logging_handler, 
                 logging_level=logging.DEBUG)


class IviAvmCamPM:
    
    def __init__(self, logger=_logger):
        self.logger = logger
        self.__foreground = UISimpleForeground()
        self.__avm_cam_pm = AVMCameraPM()
        self.__speed = UISpeedSlider()
        self.__speed_close_threshold = widgets.IntText(value=50, 
                                                       description="close_speed", 
                                                       disabled=True)
        self.__speed_open_threshold = widgets.Dropdown(options=['15', '25', '35'], 
                                                       value='25', 
                                                       description="open_speed")
        self.__speed_control = widgets.VBox([self.__speed, 
                                             self.__speed_close_threshold, 
                                             self.__speed_open_threshold])
        self.__control_box = widgets.VBox([self.__avm_cam_pm.show(), self.__speed_control])
        self.__show_box = widgets.HBox([self.__foreground.show(), self.__control_box])
        
        self.__speed.observe(self.__on_change_speed_callback, "value")
        self.__speed_open_threshold.observe(self.__on_change_speed_open_threshold_callback, "value")
        
    def show(self):
        return self.__show_box
    
    def __on_change_speed_callback(self, change):
        new_value = int(change["new"])
        if new_value > int(self.__speed_close_threshold.value):
            self.__avm_cam_pm.power_off()
            
        elif new_value <= int(self.__speed_open_threshold.value):
            self.__avm_cam_pm.power_on()
            
        else:
            pass
        
    def __on_change_speed_open_threshold_callback(self, change):
        new_value = change["new"]
        if new_value == '35':
            self.__speed_close_threshold.value = 75
        else:
            self.__speed_close_threshold.value = 50



