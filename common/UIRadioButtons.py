import ipywidgets as widgets

class UISDCard(widgets.RadioButtons):
    SD_CARD_PLUGED = "SD_CARD_PLUGED"
    SD_CARD_NOT_PLUGED = "SD_CARD_NOT_PLUGED"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.options=[self.SD_CARD_NOT_PLUGED, self.SD_CARD_PLUGED]
        self.value=self.SD_CARD_NOT_PLUGED
        self.layout={'width': 'max-content'}
        self.description='SD Card Slot'
        
        
class UISavingEnergyMode(widgets.RadioButtons):
    SUPER_ECO = "SUPER_ECO"
    NORMAL = "NORMAL"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.options=[self.SUPER_ECO, self.NORMAL]
        self.value=self.NORMAL
        self.layout={'width': 'max-content'}
        self.description='Energy Mode'