
from typing import Type
import ipywidgets as widgets

from common.AbstractState import Context as ContextButton
from common.AbstractState import State as StateButton
from customized.IviAvmCamPM import IviAvmCamPM, IviAvmCamPM_DVR, IviAvmCamPM_MPD
from customized.IviAvmCamPMStates import *

import logging
from utils.loggers import Logger, OutputWidgetHandler
logging_handler = OutputWidgetHandler()
_logger = Logger(logger_name=__file__, 
                 log_handler=logging_handler, 
                 logging_level=logging.DEBUG)


class IviAvmCamPMDemo(widgets.VBox):
    def __init__(self, avm_pm: IviAvmCamPM, state_list: Type[StateButton], logger=_logger,**kwargs):
        self.logger=_logger
        self.__avm_pm = avm_pm()
        self.__state_list = state_list
        self.__state_name_list = [state.__name__ for state in self.__state_list]
        self.__state_instances = self.__construct_state_list_instances()
        self.__context = ContextButton(self.__state_instances[0])
        self.__context.value = self.__state_name_list[0]
        self.__context.set_on_click_reset_button_additional_callback(self.__on_click_reset_button)
        
        
        self.__state_dropdown = widgets.Dropdown(
            options=self.__state_name_list,
            value=self.__state_name_list[0],
            description="state"
        )
        self.__state_dropdown.observe(self.__on_change_dropdown, "value")
        
        self.__state_hbox = widgets.HBox(
            [self.__context.hbox_buttons, self.__state_dropdown], 
            layout={'border': '2px solid lightblue'}
            )
        
        widgets.link((self.__context, 'value'), (self.__state_dropdown , 'value'))
        
        
        super().__init__([self.__avm_pm.display, self.__state_hbox], **kwargs)
        
    def __on_click_reset_button(self):
        self.__state_dropdown.value = self.__state_name_list[0]
        
    def __construct_state_list_instances(self):
        
        state_instance_list = list()
        state_number = len(self.__state_list)
        
        for i in list(range(state_number)):
            state_instance = self.__state_list[i](ivi_avm_pm=self.__avm_pm, key=i, logger=self.logger)
            state_instance_list.append(state_instance)
            
        for i in list(range(0, state_number-1)):
            state_instance_list[i].next_state = state_instance_list[i+1]
            
        state_instance_list[-1].next_state = state_instance_list[0]          
        return state_instance_list
    
    # def __on_change_context(self, change):
    #     new_value = change["new"]
    #     self.logger.debug(f"{__class__.__name__} context value changed to {new_value}.")
    #     index = self.__state_name_list.index(new_value)
    #     self.__context.transition_to(self.__state_list[index])

    def __on_change_dropdown(self, change):
        new_value = change["new"]
        self.logger.debug(f"{__class__.__name__} state select dropdown value changed to {new_value}.")
        self.__context.value = new_value
        self.logger.debug(f"{__class__.__name__} context value changed to {self.__context.value}.")
        index = self.__state_name_list.index(new_value)
        self.__state_instances[index].execute()
        self.__context.transition_to(self.__state_instances[index])
        
        
        

        

state_list = [
    State000_Init, 
    State001_OverSpeedClose,
    State002_LowSpeedReopen,
    State003_EnterAVM360,
    State004_OverSpeedCloseIn360Page,
    State006_OverSpeedCloseSetIn25kmh,
    State007_LowSpeedReopenSetIn25kmh,
    State008_OverSpeedCloseSetIn15kmh,
    State009_LowSpeedReopenSetIn15kmh
    ]

state_list_dvr_extended = [
    State100_DVR_InitPlugin,
    State101_DVR_PluginOverSpeed,
    State102_DVR_PullOutOverSpeed,
    State103_DVR_NotPluginLowSpeed,
    State104_DVR_NotPluginOverSpeed,
    State101_DVR_PluginOverSpeed
]


state_list_dvr = state_list.copy() 
state_list_dvr.extend(state_list_dvr_extended)

state_list_mpd = state_list_dvr.copy()


class IviAvmCamPMDemo_Platform(widgets.Tab):
    TABS = ["AVM_ONLY", "AVM_DVR", "AVM_via_MPD"]
    
    
    def __init__(self, **kwargs):
        
        self.__avm = IviAvmCamPMDemo(avm_pm=IviAvmCamPM, state_list=state_list)
        self.__avm_dvr = IviAvmCamPMDemo(avm_pm=IviAvmCamPM_DVR, state_list=state_list_dvr)
        self.__avm_mpd = IviAvmCamPMDemo(avm_pm=IviAvmCamPM_MPD, state_list=state_list_mpd)
        
        super().__init__(

            children=[
                self.__avm,
                self.__avm_dvr,
                self.__avm_mpd
            ],
            **kwargs)
        [self.set_title(i, title) for i, title in enumerate(self.TABS)]