from typing import Type

from common.Demonstrator import DemoState, Demonstrator
from components.DABPM import DABPM
from customized.DABAMStates import *


class DABPMDemo(Demonstrator):
    def __init__(self, demo_box: DABPM, state_list: Type[DemoState], **kwargs):
        super().__init__(demo_box, state_list, **kwargs)


state_list = [
    State000_Init,
    State001_EnterRadiosPageAtBeginning,
    State002_RunDABAtBeginning,
    State003_BackToHomenDABRunning,
    State004_EnterSettingPage,
    State005_TryToDisableDAB,
    State006_BackToHomeOnDABRunning,
    State007_EnterRadiosPagenDABRunning,
    State008_StopDAB,
    State009_DABEnergySavingPrompt,
    State010_BackToHomeOnDABStopped,
    State011_EnterRadiosPagenDABStopped,
    State012_RunDABOnEnergySavingMode,
]

dab_demo = DABPMDemo(demo_box=DABPM, state_list=state_list)
