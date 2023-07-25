from common.AbstractState import State as StateButton
from components.IviAvmCamPM import IviAvmCamPM
from components.UIRadioButtons import UISDCard, UISavingEnergyMode
from utils.loggers import Logger


# TODO: Wait for refactor with common.Demonstrator framework


class State000_Init(StateButton):
    def __init__(self, ivi_avm_pm: IviAvmCamPM, key: int, logger: Logger) -> None:
        super().__init__()
        self.logger = logger
        self.__ivi_avm_pm = ivi_avm_pm
        self.__next_state = None
        self.__key = key

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
        self.logger.debug(
            f"{__class__.__name__} executes handle_next_button_click() for next_state: {type(self.__next_state).__name__}."
        )
        if self.__next_state:
            self.__next_state.execute()
            self.context.value = self.__next_state.__class__.__name__
            self.context.transition_to(self.__next_state)

    def execute(self):
        self.ivi_avm_pm.speed.value = 0


class State001_OverSpeedClose(State000_Init):
    def execute(self):
        self.ivi_avm_pm.speed.value = 100


class State002_LowSpeedReopen(State000_Init):
    def execute(self):
        self.ivi_avm_pm.speed.value = 12


class State003_EnterAVM360(State000_Init):
    def execute(self):
        self.ivi_avm_pm.foreground.set_avm360_page()


class State004_OverSpeedCloseIn360Page(State000_Init):
    def execute(self):
        self.ivi_avm_pm.speed.value = 100


class State005_SetIn25kmhOnLowSpeed(State000_Init):
    def execute(self):
        self.ivi_avm_pm.speed.value = 12
        self.ivi_avm_pm.speed_open_threshold.value = "25"


class State006_OverSpeedCloseSetIn25kmh(State000_Init):
    def execute(self):
        self.ivi_avm_pm.speed.value = 75


class State007_LowSpeedReopenSetIn25kmh(State000_Init):
    def execute(self):
        self.ivi_avm_pm.speed_open_threshold.value = "25"
        self.ivi_avm_pm.speed.value = 20


class State008_OverSpeedCloseSetIn15kmh(State000_Init):
    def execute(self):
        self.ivi_avm_pm.speed_open_threshold.value = "15"
        self.ivi_avm_pm.speed.value = 60


class State009_LowSpeedReopenSetIn15kmh(State000_Init):
    def execute(self):
        self.ivi_avm_pm.speed_open_threshold.value = "15"
        self.ivi_avm_pm.speed.value = 12


class State100_DVR_InitPlugin(State000_Init):
    def execute(self):
        self.ivi_avm_pm.sd_card.value = UISDCard.SD_CARD_PLUGED
        self.ivi_avm_pm.speed.value = 0
        self.ivi_avm_pm.speed_open_threshold.value = "25"


class State101_DVR_PluginOverSpeed(State000_Init):
    def execute(self):
        self.ivi_avm_pm.sd_card.value = UISDCard.SD_CARD_PLUGED
        self.ivi_avm_pm.speed.value = 120
        self.ivi_avm_pm.speed_open_threshold.value = "25"


class State102_DVR_PullOutOverSpeed(State000_Init):
    def execute(self):
        self.ivi_avm_pm.sd_card.value = UISDCard.SD_CARD_NOT_PLUGED
        self.ivi_avm_pm.speed.value = 120
        self.ivi_avm_pm.speed_open_threshold.value = "25"


class State103_DVR_NotPluginLowSpeed(State000_Init):
    def execute(self):
        self.ivi_avm_pm.sd_card.value = UISDCard.SD_CARD_NOT_PLUGED
        self.ivi_avm_pm.speed.value = 20
        self.ivi_avm_pm.speed_open_threshold.value = "25"


class State104_DVR_NotPluginOverSpeed(State000_Init):
    def execute(self):
        self.ivi_avm_pm.sd_card.value = UISDCard.SD_CARD_NOT_PLUGED
        self.ivi_avm_pm.speed.value = 100
        self.ivi_avm_pm.speed_open_threshold.value = "25"


class State105_DVR_InsertInOverSpeed(State000_Init):
    def execute(self):
        self.ivi_avm_pm.sd_card.value = UISDCard.SD_CARD_PLUGED
        self.ivi_avm_pm.speed.value = 100
        self.ivi_avm_pm.speed_open_threshold.value = "25"


class State200_MPD_SuperECO_Init(State000_Init):
    def execute(self):
        self.ivi_avm_pm.sd_card.value = UISDCard.SD_CARD_PLUGED
        self.ivi_avm_pm.speed.value = 0
        self.ivi_avm_pm.speed_open_threshold.value = "25"
        self.ivi_avm_pm.energy_mode.value = UISavingEnergyMode.SUPER_ECO


class State201_MPD_SuperECO_PluginOverSpeed(State000_Init):
    def execute(self):
        self.ivi_avm_pm.sd_card.value = UISDCard.SD_CARD_PLUGED
        self.ivi_avm_pm.speed.value = 120
        self.ivi_avm_pm.speed_open_threshold.value = "25"
        self.ivi_avm_pm.energy_mode.value = UISavingEnergyMode.SUPER_ECO


class State202_MPD_SuperECO_PullOutOverSpeed(State000_Init):
    def execute(self):
        self.ivi_avm_pm.sd_card.value = UISDCard.SD_CARD_NOT_PLUGED
        self.ivi_avm_pm.speed.value = 120
        self.ivi_avm_pm.speed_open_threshold.value = "25"
        self.ivi_avm_pm.energy_mode.value = UISavingEnergyMode.SUPER_ECO


class State203_MPD_SuperECO_NotPluginLowSpeed(State000_Init):
    def execute(self):
        self.ivi_avm_pm.sd_card.value = UISDCard.SD_CARD_NOT_PLUGED
        self.ivi_avm_pm.speed.value = 20
        self.ivi_avm_pm.speed_open_threshold.value = "25"
        self.ivi_avm_pm.energy_mode.value = UISavingEnergyMode.SUPER_ECO


class State204_MPD_SuperECO_NotPluginOverSpeed(State000_Init):
    def execute(self):
        self.ivi_avm_pm.sd_card.value = UISDCard.SD_CARD_NOT_PLUGED
        self.ivi_avm_pm.speed.value = 100
        self.ivi_avm_pm.speed_open_threshold.value = "25"
        self.ivi_avm_pm.energy_mode.value = UISavingEnergyMode.SUPER_ECO


class State205_MPD_SuperECO_InsertInOverSpeed(State000_Init):
    def execute(self):
        self.ivi_avm_pm.sd_card.value = UISDCard.SD_CARD_PLUGED
        self.ivi_avm_pm.speed.value = 100
        self.ivi_avm_pm.speed_open_threshold.value = "25"
        self.ivi_avm_pm.energy_mode.value = UISavingEnergyMode.SUPER_ECO
