import threading
import ipywidgets as widgets

# from typing import Type
from common.UISignal import UISignal
from components.DualDisplay import DualDisplay
from signals.enum_signals import EnhancedUISignalEnum
from signals.saic_signals import *

signals_list = [SysPwrMd, VehLckngSts]


class SignalsCluster(widgets.VBox):
    def __init__(
        self, signals_list=signals_list, label="Vehicle Signals Cluster", **kwargs
    ):
        self.layout = widgets.Layout(
            border="solid",
            # display="flex",
            flex_flow="wrap",
            justify_content="space-around",
            align_items="center",
        )
        self.__label = widgets.HTML(f"<h2 style='font-weight:bold'>{label}</h2>")
        self.__signals_list = signals_list
        self.__signal_widgets_dict = dict()
        self.__construct_signal_widgets()
        self.__signal_widgets = widgets.HBox(list(self.__signal_widgets_dict.values()))

        super().__init__(
            children=[
                self.__label,
                self.__signal_widgets,
            ],
            **kwargs,
        )

    def __construct_signal_widgets(self):
        for signal in self.__signals_list:
            self.__signal_widgets_dict[signal.__name__] = EnhancedUISignalEnum(signal)

    def append_signal_widget(self, signal_widget: UISignal):
        self.__signal_widgets.children += (signal_widget,)

    @property
    def signal_widgets(self):
        return self.__signal_widgets

    @property
    def signal_wigdets_dict(self):
        return self.__signal_widgets_dict


default_dual_display = DualDisplay()
default_signals_cluster = SignalsCluster()


class VirtualCluster(widgets.VBox):
    def __init__(
        self,
        dual_display=default_dual_display,
        signals_cluster=default_signals_cluster,
        **kwargs,
    ):
        self.__dual_display = dual_display
        self.__signals_cluster = signals_cluster

        super().__init__([self.__dual_display, self.__signals_cluster], **kwargs)
        self.__key_off_event = threading.Event()

        self.__signals_cluster.signal_wigdets_dict["SysPwrMd"].set_on_change_callback(
            self.__on_change_SysPwrMd
        )
        self.__signals_cluster.signal_wigdets_dict[
            "VehLckngSts"
        ].set_on_change_callback(self.__on_change_VehLckngSts)

    def __on_change_SysPwrMd(self, change):
        new_value = change["new"]

        if new_value == get_class_by_name("SysPwrMd").RUN.value:
            self.__dual_display.power_up()

        elif new_value == get_class_by_name("SysPwrMd").OFF.value:
            self.__key_off_event.set()

    def __on_change_VehLckngSts(self, change):
        new_value = change["new"]

        if new_value == get_class_by_name("VehLckngSts").Super_Locked.value:
            if self.__key_off_event.is_set():
                self.__dual_display.power_off()
