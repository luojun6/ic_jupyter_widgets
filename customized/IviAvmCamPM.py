import logging
import ipywidgets as widgets
from utils.loggers import Logger, OutputWidgetHandler
from components.UIRadioButtons import UISDCard, UISavingEnergyMode
from components.UIForeground import UISimpleForeground
from components.UISpeed import UISpeedSlider
from components.UICamera import MPDCameraSet
from components.AVMCameraPM import AVMCameraPM

logging_handler = OutputWidgetHandler()
_logger = Logger(logger_name=__file__, 
                 log_handler=logging_handler, 
                 logging_level=logging.DEBUG)


# TODO: To add forbidding to enter 360 in high speed
class IviAvmCamPM:
    
    def __init__(self, 
                 logger=_logger, 
                 foreground=UISimpleForeground(),
                 avm_cam_pm=AVMCameraPM(),
                 speed=UISpeedSlider()
                 ):
        self.logger = logger
        self.__foreground = foreground
        self.__avm_cam_pm = avm_cam_pm
        self.__speed = speed
        self.__speed_close_threshold = widgets.IntText(value=75, 
                                                       description="CLOSE_SPEED", 
                                                       disabled=True)
        self.__speed_open_threshold = widgets.Dropdown(options=['15', '25', '35'], 
                                                       value='35', 
                                                       description="OPEN_SPEED")
        self.__speed_control = widgets.VBox([self.__speed, 
                                             self.__speed_close_threshold, 
                                             self.__speed_open_threshold])
        self.__control = None
        self.__display = None
                
        self.__speed.observe(self.on_change_speed_callback, "value")
        self.__speed_open_threshold.observe(self.__on_change_speed_open_threshold_callback, "value")
        self.__foreground.set_on_clink_avm360_button_callback(self.on_click_avm360_button)
        
        self.construct()
        
    # To be overriden
    def construct(self):
        
        self.__control = widgets.VBox([self.__avm_cam_pm.show(), self.__speed_control])
        self.__display = widgets.HBox([self.__foreground.show(), self.__control])
        
    def on_click_avm360_button(self, btn):
        if int(self.__speed.value) > int(self.__speed_open_threshold.value):
            self.logger.debug(f"{__class__.__name__} forbid to enter avm360 in speed of {self.__speed.value}.")
        else:
            self.__foreground.set_avm360_page()        
    
    def on_change_speed_callback(self, change):
        new_value = int(change["new"])
        if new_value > int(self.__speed_open_threshold.value):
            if self.__foreground.value == self.__foreground.AVM360:
                self.__foreground.set_home_page()
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

    @property
    def foreground(self):
        return self.__foreground
        
    @property
    def avm_cam_pm(self):
        return self.__avm_cam_pm
    
    @property
    def speed_control(self):
        return self.__speed_control
        
    @property
    def control(self):
        return self.__control
    
    @property
    def display(self):
        return self.__display
    
    @control.setter
    def control(self, new_control):
        self.__control = new_control
        
    @display.setter
    def display(self, new_display):
        self.__display = new_display
        
    @property
    def speed_close_threshold(self):
        return self.__speed_close_threshold
        
    @property
    def speed_open_threshold(self):
        return self.__speed_open_threshold
    
    @property
    def speed(self):
        return self.__speed
    

class IviAvmCamPM_DVR(IviAvmCamPM):
    # SD_CARD_PLUGED = "SD_CARD_PLUGED"
    # SD_CARD_NOT_PLUGED = "SD_CARD_NOT_PLUGED"
    
    def __init__(self, 
                 logger=_logger, 
                 foreground=UISimpleForeground(),
                 avm_cam_pm=AVMCameraPM(),
                 speed=UISpeedSlider()):
        # self.__sd_card = widgets.RadioButtons(
        #     options=[self.SD_CARD_NOT_PLUGED, self.SD_CARD_PLUGED],
        #     value=self.SD_CARD_NOT_PLUGED,
        #     layout={'width': 'max-content'},
        #     description='SD Card Slot',
        #     )
        self.__sd_card = UISDCard()
        super().__init__(logger, foreground=foreground, avm_cam_pm=avm_cam_pm, speed=speed)
        self.__sd_card.observe(self.on_change_sd_card_plugin, "value")
        
    def construct(self):
        buttom_control = widgets.HBox([self.speed_control, self.__sd_card])
        self.control = widgets.VBox([self.avm_cam_pm.show(), buttom_control])
        self.display = widgets.HBox([self.foreground.show(), self.control])
        
    def on_change_speed_callback(self, change):
        if self.__sd_card.value == self.__sd_card.SD_CARD_NOT_PLUGED:
            super().on_change_speed_callback(change)
            
    def on_change_sd_card_plugin(self, change):
        new_value = change["new"]
        if new_value is self.__sd_card.SD_CARD_PLUGED:
            self.avm_cam_pm.power_on()
            
    @property
    def sd_card(self):
        return self.__sd_card
            
            
class IviAvmCamPM_MPD(IviAvmCamPM_DVR):
    CAMERA_OCCUPIED_SIGNAL = ["undefined", "not_occupied", "occupied"]
    
    def __init__(self, 
                 logger=_logger, 
                 foreground=UISimpleForeground(),
                 avm_cam_pm=MPDCameraSet(),
                 speed=UISpeedSlider()
                 ):
        
        self.__cam_occupied_signal_select = widgets.Select(
            options=self.CAMERA_OCCUPIED_SIGNAL, 
            value=self.CAMERA_OCCUPIED_SIGNAL[2],
            disabled=True
            )
        self.__select_label = widgets.Label("Simulated CAMERA_OCCUPIED_SIGNAL")
        self.__cam_occupied_signal_control = widgets.HBox([self.__select_label, self.__cam_occupied_signal_select])
        # self.__cam_occupied_signal_select.disabled = True
        
        self.__energy_mode = UISavingEnergyMode()
        self.__energy_mode.observe(self.on_change_energy_mode, "value")
        self.__cam_occupied_signal_select.observe(self.on_change_cam_occupied_signal, "value")
        
        super().__init__(logger, foreground=foreground, avm_cam_pm=avm_cam_pm, speed=speed)
        
    def construct(self):
        top_control = widgets.VBox([self.avm_cam_pm.show(), self.__cam_occupied_signal_control])
        buttom_control = widgets.HBox([self.speed_control, 
                                       widgets.VBox([self.sd_card, self.__energy_mode])])
        self.control = widgets.VBox([top_control, buttom_control])
        
        self.display = widgets.HBox([self.foreground.show(), self.control])
        
    def on_change_speed_callback(self, change):
        if self.sd_card.value == self.sd_card.SD_CARD_NOT_PLUGED:
            new_value = int(change["new"])
            if new_value > int(self.speed_close_threshold.value):
                if self.foreground.value == self.foreground.AVM360:
                    self.foreground.set_home_page()
                # self.__avm_cam_pm.power_off()
                self.__cam_occupied_signal_select.value = self.CAMERA_OCCUPIED_SIGNAL[1]
                
            elif new_value <= int(self.speed_open_threshold.value):
                # self.__avm_cam_pm.power_on()
                self.__cam_occupied_signal_select.value = self.CAMERA_OCCUPIED_SIGNAL[2]
                
            else:
                pass
            
    def on_change_energy_mode(self, change):
        new_value = change["new"]
        if new_value == self.__energy_mode.SUPER_ECO:
            self.logger.debug(f"{__class__.__name__}: energy_mode changed to {self.__energy_mode.SUPER_ECO}.")
            if self.__cam_occupied_signal_select.value != self.CAMERA_OCCUPIED_SIGNAL[2]:
                self.logger.debug(f"{__class__.__name__}: MPD power off all cameras.")
                self.avm_cam_pm.power_off()
            else:
                self.logger.debug(f"{__class__.__name__}: cameras are occupied, unable to power off cameras.")
                
        elif new_value == self.__energy_mode.NORMAL:
            self.logger.debug(f"{__class__.__name__}: energy_mode changed to {self.__energy_mode.NORMAL}.")
            self.logger.debug(f"{__class__.__name__}: MPD power on all cameras.")
            self.avm_cam_pm.power_on()
            
    def on_change_sd_card_plugin(self, change):
        new_value = change["new"]
        if new_value is self.sd_card.SD_CARD_PLUGED:
            self.__cam_occupied_signal_select.value = self.CAMERA_OCCUPIED_SIGNAL[2]
            
    def on_change_cam_occupied_signal(self, change):
        new_value = change["new"]
        if (new_value != self.CAMERA_OCCUPIED_SIGNAL[2]) and (self.__energy_mode.value == self.__energy_mode.SUPER_ECO):
            self.avm_cam_pm.power_off()
        else:
            self.avm_cam_pm.power_on()
        
        

class IviAvmCamPM_Platform(widgets.Tab):
    TABS = ["AVM_ONLY", "AVM_DVR", "AVM_via_MPD"]
    
    
    def __init__(self, **kwargs):
        
        self.__avm = IviAvmCamPM()
        self.__avm_dvr = IviAvmCamPM_DVR()
        self.__avm_mpd = IviAvmCamPM_MPD()
        
        super().__init__(
            # children=[
            #     IviAvmCamPM().display,
            #     IviAvmCamPM_DVR().display,
            #     IviAvmCamPM_MPD().display
            # ], 
            children=[
                self.__avm.display,
                self.__avm_dvr.display,
                self.__avm_mpd.display
            ],
            **kwargs)
        [self.set_title(i, title) for i, title in enumerate(self.TABS)]
        
        