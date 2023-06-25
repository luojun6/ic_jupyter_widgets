import logging
import ipywidgets as widgets
from utils.loggers import Logger, OutputWidgetHandler

logging_handler = OutputWidgetHandler()
_logger = Logger(logger_name=__file__, 
                 log_handler=logging_handler, 
                 logging_level=logging.DEBUG)

default_switch_values = ["invalid", "inactive", "active"]


class UIButton(widgets.Button, widgets.ValueWidget):
    def __init__(self,
                 name=__file__, 
                 values = default_switch_values,
                 default_value_index = 0,
                 internal_timer_callback=None,
                 logger=_logger, **kwargs):
        super().__init__(**kwargs)
        self.logger = logger
        self.description = name
        # self.disabled = False
        self.__name = name
        self.__values = values
        self.__value_index = default_value_index
        self.__values_len = len(values)
        self.value = values[default_value_index]
        self.__internal_timer_callback = internal_timer_callback
        self.__external_on_click_callback = None
        self.__external_on_change_callback = None
        self.on_click(self.__on_click_callback)
        self.observe(self.__on_change_callback)
        
    @property
    def values(self):
        return self.__values
    
    @property
    def value_index(self):
        return self.__value_index
        
    def set_value_index(self, index):
        if index > self.__values_len:
            self.logger.error(f"Input index {index} has been exceeded the range of values as {self.__values_len}.")
            return 
        self.__value_index = index
        self.value = self.__values[index]
        
        
    def set_on_click_callback(self, callback):
        self.__external_on_click_callback = callback
        self.on_click(self.__on_click_callback)
        
    def set_on_change_callback(self, callback):
        self.__external_on_change_callback = callback
        self.observe(self.__on_change_callback)
        self.logger.debug(f"{self.__name} updated on_change_callback function.")
        
    def __internal_on_click_callback(self):
        # self.logger.debug(f"{self.__name} on_click_callback executing.")
        
        if self.__value_index < (self.__values_len - 1):
            self.__value_index += 1
        else:
            self.__value_index = 0
            
        self.value = self.__values[self.__value_index]
        self.logger.debug(f"{self.__name} on_click_callback executed with new value {self.value}:{self.__value_index}.")   
        
        if self.__internal_timer_callback:
            self.__internal_timer_callback(self.value)    
        
    def __on_click_callback(self, btn):
        self.__internal_on_click_callback()
        if self.__external_on_click_callback:
            self.__external_on_click_callback(btn)
            
    def __internal_on_change_callback(self):
        self.logger.debug(f"{self.__name} on_change_callback executed with new value {self.value}:{self.__value_index}.")
        
    def __on_change_callback(self, change):
        self.__internal_on_change_callback()
        if self.__external_on_change_callback:
            self.__external_on_change_callback(change)