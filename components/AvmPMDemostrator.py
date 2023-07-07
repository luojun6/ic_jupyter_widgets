import ipywidgets as widgets
from IPython.core.display import display

from utils.files_mgmt import get_file_by_suffix

DIR_NAME = "res/images/avmpm_screenshots"

SCENARIO_PNG_DICT = get_file_by_suffix(suffix_name="png", dir_name=DIR_NAME, inclusive_keyword="scenario")


class AvmPMDemostrator(widgets.ValueWidget):
    
    def __init__(self, display_png_dict=SCENARIO_PNG_DICT):
        
        self.__button = widgets.Button(
            description="NEXT", 
            button_style="info", 
            icon="arrow-right"
            )
        
        self.__out = widgets.Output(
            layout={
                "border": "1px solid black", 
                # "height": "240px", 
                # "width": "320px"
                }
            )
        
        self.__display_png_dict = display_png_dict
        
        self.__label = widgets.Label("Demonstrate the AVM Cameras Power Management here!")
        self.__image = None
        self.__display_number = 0
        
        self.value = list(self.__display_png_dict)[self.__display_number]
        
        self.__display_box = widgets.VBox([self.__label], layout={"border": "1px solid black"})
        self.__button.on_click(self.__on_click)
        
        with self.__out:
            display(widgets.HBox([self.__button, self.__display_box]))
            
    def show(self):
        return self.__out
            
    
    def __on_click(self, btn):
        self.__out.clear_output()
        value = list(self.__display_png_dict)[self.__display_number]
        image_path = self.__display_png_dict[value]
        image = open(image_path, "rb").read()
        self.__image = widgets.Image(
            value=image,
            format="png",
        )
        self.__label.value = value
        self.__display_box = widgets.VBox([self.__label, self.__image], 
                                          layout={"border": "1px solid black"})
        
        with self.__out:
            display(widgets.HBox([self.__button, self.__display_box]))
        
        
        
        
        