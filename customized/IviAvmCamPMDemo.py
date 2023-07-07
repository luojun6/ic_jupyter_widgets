
from typing import Type
import ipywidgets as widgets

from common.AbstractState import Context as ContextButton
from common.AbstractState import State as StateButton
from customized.IviAvmCamPM import IviAvmCamPM, IviAvmCamPM_DVR, IviAvmCamPM_MPD

import logging
from utils.loggers import Logger, OutputWidgetHandler
logging_handler = OutputWidgetHandler()
_logger = Logger(logger_name=__file__, 
                 log_handler=logging_handler, 
                 logging_level=logging.DEBUG)


class IviAvmCamPMDemo(widgets.VBox):
    def __init__(self, avm_pm: IviAvmCamPM, state_list: Type[StateButton], **kwargs):
        self.__avm_pm = avm_pm()
        self.__state_list = state_list
        self.__state_name_list = [state.__name__ for state in self.__state_list]
        self.__state_instances = self.__construct_state_list_instances()
        self.__context = ContextButton(self.__state_instances[0])
        self.__context.value = self.__state_name_list[0]
        self.__context.observe(self.__on_change_context, "value")
        
        self.__state_dropdown = widgets.Dropdown(
            options=self.__state_name_list,
            value=self.__state_name_list[0],
            description="state"
        )
        self.__state_hbox = widgets.HBox(
            [self.__context.hbox_buttons, self.__state_dropdown], 
            layout={'border': '2px solid lightblue'}
            )
        
        widgets.link((self.__context, 'value'), (self.__state_dropdown , 'value'))
        
        
        super().__init__([self.__avm_pm.display, self.__state_hbox], **kwargs)
        
    def __construct_state_list_instances(self):
        
        state_instance_list = list()
        state_number = len(self.__state_list)
        
        for i in list(range(state_number)):
            state_instance = self.__state_list[i](ivi_avm_pm=self.__avm_pm)
            state_instance_list.append(state_instance)
            
        for i in list(range(0, state_number-1)):
            state_instance_list[i].next_state = state_instance_list[i+1]
            
        state_instance_list[-1].next_state = state_instance_list[0]          
        return state_instance_list
    
    def __on_change_context(self, change):
        _logger.debug(f"{__class__.__name__} context value changed to {self.__context.value}.")
            
        
        
        
class State00_Init(StateButton):
    
    def __init__(self, ivi_avm_pm: IviAvmCamPM) -> None:
        super().__init__()
        self.__ivi_avm_pm = ivi_avm_pm
        self.__next_state = None
        
        
    @property
    def key(self):
        return self.__key       
        
    @property
    def next_state(self):
        return self.__next_state
    
    @next_state.setter
    def next_state(self, state: StateButton):
        self.__next_state = state
        
    @property
    def ivi_avm_pm(self):
        return self.__ivi_avm_pm
    
    def handle_next_button_click(self):
        _logger.debug(f"{__class__.__name__} executes handle_next_button_click() for next_state: {type(self.__next_state).__name__}.")
        if self.__next_state:
            self.__next_state.execute()
            self.context.value = self.__next_state.__class__.__name__
            self.context.transition_to(self.__next_state)
        
    def handle_reset_button_click(self):
        pass
    
    def execute(self):
        self.ivi_avm_pm.speed.value = 0
        

class State01_OverSpeedClose(State00_Init):
    
    def execute(self):
        self.ivi_avm_pm.speed.value = 100
        
class State02_LowSpeedReopen(State00_Init):
    
    def execute(self):
        self.ivi_avm_pm.speed.value = 12
        
class State03_EnterAVM360(State00_Init):
    
    def execute(self):
        self.ivi_avm_pm.foreground.set_avm360_page()
        
class State04_OverSpeedCloseIn360Page(State00_Init):
    
    def execute(self):
        self.ivi_avm_pm.speed.value = 100
        

state_list = [
    State00_Init, 
    State01_OverSpeedClose,
    State02_LowSpeedReopen,
    State03_EnterAVM360,
    State04_OverSpeedCloseIn360Page
    ]