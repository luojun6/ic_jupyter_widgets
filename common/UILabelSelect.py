from msilib.schema import Error
import ipywidgets as widgets
from IPython.core.display import display


class LabelSelect:
    
    def __init__(self, select_object=None, label="A Select Object"):
        self.__select = select_object
        self.__label = widgets.Label(label)
        self.__out = widgets.Output(layout={'border': '1px solid black'})
        if not self.__label:
            raise Error("")
        with self.__out:
            display(widgets.VBox([self.__label, self.__select]))
        
    
    @property
    def select(self):
        return self.__select
    
    @property
    def label(self):
        return self.__label