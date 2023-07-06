# import logging
import ipywidgets as widgets
# from utils.loggers import Logger, OutputWidgetHandler



# logging_handler = OutputWidgetHandler()
# _logger = Logger(logger_name=__file__, 
#                  log_handler=logging_handler, 
#                  logging_level=logging.DEBUG)



class UIVehicleSystemPowerModeDropdown(widgets.Dropdown):
    VEHICLE_SYSTEM_POWER_MODE_OPTIONS = [
        ("OFF", 0),
        ("ACC", 1),
        ("RUN", 2),
        ("CRANK", 3)
    ]

    VEHICLE_SYSTEM_POWER_MODE_DESCRIPTION = "SysPowerMode"
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.options = self.VEHICLE_SYSTEM_POWER_MODE_OPTIONS
        self.value = 0
        self.description = self.VEHICLE_SYSTEM_POWER_MODE_DESCRIPTION
        self.layout = widgets.Layout(display='flex', flex_flow='row',
    justify_content='space-between')
        

class UIHeadUnitSystemPowerState(widgets.Select):
    HU_SYSTEM_POWER_MODE_OPTIONS = [
        ("PWR_MODE_NONE", 0),
        ("PWR_MODE_OFF", 1),
        ("PWR_MODE_STANDBY", 2),
        ("PWR_MODE_RUN", 3), 
        ("PWR_MODE_SLEEP", 4), 
        ("PWR_MODE_ABNORMAL", 5), 
        ("PWR_MODE_TEMP_ON", 6)
    ]
    HU_SYSTEM_POWER_MODE_DESCRIPTION = "StateMachine"
