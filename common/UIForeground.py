import os
import logging
from pydoc import describe
from IPython.core.display import display
import ipywidgets as widgets
from utils.loggers import Logger, OutputWidgetHandler
from utils.files_mgmt import res_dir

logging_handler = OutputWidgetHandler()
_logger = Logger(logger_name=__file__, 
                 log_handler=logging_handler, 
                 logging_level=logging.DEBUG)

        
def create_faked_home_page(image_file:str):
    image_type = image_file.split(".")[-1]
    
    image_path = os.path.join(res_dir, "images", image_file)
    image = open(image_path, "rb").read()
    return widgets.Image(
            value=image ,
            format="jpg",
            width=300,
            height=180,
            )
    
    
class UISimpleForeground:
    
    def __init__(self, logger=_logger):
        self.logger = logger
        self.__out = widgets.Output(
            layout={
                "border": "1px solid black", 
                "height": "240px", 
                "width": "320px"
                }
        )
        
        #TODO: To be optimized by using Command Pattern
        self.__home_page = create_faked_home_page("ivi_home_example.jpg")
        self.__avm360_page = create_faked_home_page("avm360_example.jpg")
        self.__home_button = widgets.Button(
            description = "Home",
            layout=widgets.Layout(width='50%', height='30px', margin="top")
        )

        with self.__out:
            display(self.__home_page)

        self.logger.debug(f"[{self.__class__.__name__}] has been constructed.")
        
    def show(self):
        return self.__out
    
    def set_home_page(self):
        self.logger.debug(f"[{self.__class__.__name__}] {__name__}.")
        self.__out.clear_output()
        with self.__out:
            display(self.__home_page)
            
    def set_avm360_page(self):
        self.logger.debug(f"[{self.__class__.__name__}] {__name__}.")
        self.__out.clear_output()
        with self.__out:
            # display()
            display(widgets.VBox([self.__avm360_page, self.__home_button, self.__home_button]))

    
