from typing import Type

from common.Demonstrator import DemoState, Demonstrator
from components.DABPM import DABPM
from customized.DABAMStates import *


class DABPMDemo(Demonstrator):
    def __init__(self, demo_box: DABPM, state_list: Type[DemoState], **kwargs):
        super().__init__(demo_box, state_list, **kwargs)


state_list = [
    State000_Init,
    State001_EnterRadiosPage,
    State002_RunDAB,
    State003_BackToHome,
    State004_EnterSettingPage,
    State005_TryToDisableDAB,
    State003_BackToHome,
    State001_EnterRadiosPage,
    State006_StopDAB,
    State003_BackToHome,
    State004_EnterSettingPage,
    State005_TryToDisableDAB,
    State007_DABEnergySaving,
]

dab_demo = DABPMDemo(demo_box=DABPM, state_list=state_list)
