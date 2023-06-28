import logging
import ipywidgets as widgets
from utils.loggers import Logger, OutputWidgetHandler


logging_handler = OutputWidgetHandler()
_logger = Logger(logger_name=__file__, 
                 log_handler=logging_handler, 
                 logging_level=logging.DEBUG)

MIN_SPEED = 0
MAX_SPEED = 180
DEFAULT_STEP = 1
SPEED_LEVEL_A = 10
SPEED_LEVEL_B = 35
STEP_LEVEL_1 = 1
STEP_LEVEL_2 = 3
STEP_LEVEL_3 = 5


class UISpeedSlider(widgets.IntSlider):

    def __init__(self, 
                 value=MIN_SPEED, 
                 min=MIN_SPEED, 
                 max=MAX_SPEED, 
                 step=DEFAULT_STEP, 
                 description="Speed",
                 orientation='horizontal',
                 logger=_logger
                 ):
        super().__init__(value, min, max, step)
        self.description = description
        self.orientation = orientation
        self.logger = logger
        self.observe(self.on_change_value_callback)


    def on_change_value_callback(self, change):
        self.__auto_adjust_step()

    
    def __auto_adjust_step(self):

        self.logger.debug(f"{__file__} received new value: {self.value}")

        if self.value <= SPEED_LEVEL_A:
            self.step = STEP_LEVEL_1

        elif (self.value > SPEED_LEVEL_A) & (self.value < SPEED_LEVEL_B):
            self.step = STEP_LEVEL_2

        else:
            self.step = STEP_LEVEL_3
        