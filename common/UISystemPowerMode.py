import logging
import ipywidgets as widgets
from utils.loggers import Logger, OutputWidgetHandler



logging_handler = OutputWidgetHandler()
_logger = Logger(logger_name=__file__, 
                 log_handler=logging_handler, 
                 logging_level=logging.DEBUG)

SYSTEM_POWER_MODE_OPTIONS = [
    ("OFF", 0),
    ("ACC", 1),
    ("RUN", 2),
    ("CRANK", 3)
]

DESCRIPTION = "PowerMode"


class UISystemPowerModeDropdown(widgets.Dropdown):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.options = SYSTEM_POWER_MODE_OPTIONS
        self.value = 0
        self.description = DESCRIPTION