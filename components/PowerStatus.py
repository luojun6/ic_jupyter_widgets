from common.UIButton import UIPowerButton
import ipywidgets as widgets


class PowerStatus(widgets.VBox):
    def __init__(self, button_label, dropdown_label, **kwargs):
        self.__power_button = UIPowerButton(name=button_label)
        self.__power_button.layout = {"width": "300px", "height": "60px"}
        self.__title = widgets.HTML(f"<h4>{dropdown_label}</h4>")
        self.__dropdown = widgets.Dropdown(
            options=self.__power_button.POWER_STATUS, value=self.__power_button.value
        )

        super().__init__([self.__power_button, self.__title, self.__dropdown], **kwargs)

        self.__dropdown.observe(self.__on_change_dropdown, "value")

    def __on_change_dropdown(self, change):
        self.__power_button.button_style = self.__power_button.STATUS_COLOR_MAP[
            change["new"]
        ]
