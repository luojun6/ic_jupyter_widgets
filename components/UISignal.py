import ipywidgets as widgets
from typing import Type, Tuple


class UISignalEnum(widgets.VBox):
    def __init__(
        self,
        signal_name: str,
        tuples_option: Type[Tuple],
        initial_value=0,
        select_widget_type=widgets.Dropdown,
        disabled=False,
        **kwargs,
    ):
        self.__label = widgets.HTML(f"<h4 style='font-weight:bold'>{signal_name}</h4>")
        self.__value_widget = select_widget_type(
            options=tuples_option, value=initial_value, disabled=disabled
        )
        self.__checkbox = widgets.Checkbox(value=disabled, description="disabled")

        super().__init__(
            [widgets.HBox([self.__label, self.__checkbox]), self.__value_widget],
            **kwargs,
        )

        self.__checkbox.observe(self.__on_change_checkbox, "value")

    def __on_change_checkbox(self, change):
        self.__value_widget.disabled = change["new"]

    @property
    def value_widget(self):
        return self.__value_widget

    @property
    def check_box(self):
        return self.__checkbox
